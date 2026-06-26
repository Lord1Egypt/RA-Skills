"""Chat Client - 智能体间实时通讯客户端"""

import asyncio
import json
import uuid
from typing import AsyncIterator, Callable, Optional
import websockets
from websockets.exceptions import ConnectionClosed


class ChatClient:
    """Chat 通讯客户端"""
    
    def __init__(
        self,
        hub_url: str = "ws://localhost:8765",
        agent_id: str = None,
        api_key: str = None
    ):
        """
        初始化 Chat 客户端
        
        Args:
            hub_url: Hub WebSocket 地址
            agent_id: 智能体 ID
            api_key: API 密钥
        """
        self.hub_url = hub_url
        self.agent_id = agent_id or f"agent_{uuid.uuid4().hex[:8]}"
        self.api_key = api_key
        self._ws = None
        self._listen_task = None
        self._message_queue = asyncio.Queue()
    
    async def connect(self) -> bool:
        """连接到 Hub"""
        try:
            self._ws = await websockets.connect(
                self.hub_url,
                extra_headers={"X-Agent-Id": self.agent_id}
            )
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            return False
    
    async def disconnect(self):
        """断开连接"""
        if self._listen_task:
            self._listen_task.cancel()
            self._listen_task = None
        
        if self._ws:
            await self._ws.close()
            self._ws = None
    
    async def _listen(self):
        """监听消息"""
        try:
            async for message in self._ws:
                try:
                    data = json.loads(message)
                    await self._message_queue.put(data)
                except json.JSONDecodeError:
                    print(f"无效的 JSON: {message}")
        except ConnectionClosed:
            print("连接已关闭")
        except asyncio.CancelledError:
            print("监听任务取消")
    
    async def messages(self) -> AsyncIterator[dict]:
        """
        异步迭代器 - 获取实时消息
        
        Yields:
            消息字典
        """
        if not self._ws:
            await self.connect()
        
        if not self._listen_task:
            self._listen_task = asyncio.create_task(self._listen())
        
        while True:
            msg = await self._message_queue.get()
            yield msg
    
    async def send_message(
        self,
        target_agent: str,
        content: str,
        service_id: str = None,
        channel_id: str = None
    ) -> dict:
        """
        发送消息
        
        Args:
            target_agent: 目标智能体 ID
            content: 消息内容
            service_id: 服务 ID（可选）
            channel_id: 频道 ID（可选）
        
        Returns:
            发送结果
        """
        if not self._ws:
            await self.connect()
        
        message = {
            "type": "chat_message",
            "message_id": f"msg_{uuid.uuid4().hex[:12]}",
            "sender_id": self.agent_id,
            "target_agent": target_agent,
            "content": content,
        }
        
        if service_id:
            message["service_id"] = service_id
        if channel_id:
            message["channel_id"] = channel_id
        
        await self._ws.send(json.dumps(message))
        
        return {"status": "sent", "message_id": message["message_id"]}
    
    async def request_chat(
        self,
        service_id: str,
        provider_id: str = None
    ) -> dict:
        """
        请求通讯（Consumer → Provider）
        
        Args:
            service_id: 服务 ID
            provider_id: 提供者 ID（可选，从服务信息获取）
        
        Returns:
            请求结果
        """
        if not self._ws:
            await self.connect()
        
        message = {
            "type": "chat_request",
            "request_id": f"req_{uuid.uuid4().hex[:12]}",
            "consumer_id": self.agent_id,
            "service_id": service_id,
        }
        
        if provider_id:
            message["provider_id"] = provider_id
        
        await self._ws.send(json.dumps(message))
        
        # 等待响应
        async for msg in self.messages():
            if msg.get("type") == "chat_accept":
                return {"status": "accepted", "channel_id": msg.get("channel_id")}
            elif msg.get("type") == "chat_reject":
                return {"status": "rejected", "reason": msg.get("reason")}
        
        return {"status": "timeout"}
    
    async def accept_chat(
        self,
        consumer_id: str,
        channel_id: str = None
    ) -> dict:
        """
        接受通讯（Provider → Consumer）
        
        Args:
            consumer_id: 消费者 ID
            channel_id: 频道 ID（可选）
        
        Returns:
            接受结果
        """
        if not self._ws:
            await self.connect()
        
        message = {
            "type": "chat_accept",
            "provider_id": self.agent_id,
            "consumer_id": consumer_id,
        }
        
        if channel_id:
            message["channel_id"] = channel_id
        
        await self._ws.send(json.dumps(message))
        return {"status": "accepted"}
    
    async def reject_chat(
        self,
        consumer_id: str,
        reason: str = None
    ) -> dict:
        """
        拒绝通讯
        
        Args:
            consumer_id: 消费者 ID
            reason: 拒绝原因
        """
        if not self._ws:
            await self.connect()
        
        message = {
            "type": "chat_reject",
            "provider_id": self.agent_id,
            "consumer_id": consumer_id,
            "reason": reason or "Service unavailable"
        }
        
        await self._ws.send(json.dumps(message))
        return {"status": "rejected"}
    
    async def end_chat(self, channel_id: str) -> dict:
        """
        结束通讯
        
        Args:
            channel_id: 频道 ID
        """
        if not self._ws:
            await self.connect()
        
        message = {
            "type": "chat_end",
            "channel_id": channel_id,
            "agent_id": self.agent_id
        }
        
        await self._ws.send(json.dumps(message))
        return {"status": "ended"}
    
    async def get_history(
        self,
        channel_id: str = None,
        service_id: str = None,
        limit: int = 50
    ) -> list:
        """
        获取历史消息
        
        Args:
            channel_id: 频道 ID
            service_id: 服务 ID
            limit: 返回数量限制
        
        Returns:
            消息列表
        """
        if not self._ws:
            await self.connect()
        
        message = {
            "type": "chat_history",
            "agent_id": self.agent_id,
            "limit": limit
        }
        
        if channel_id:
            message["channel_id"] = channel_id
        if service_id:
            message["service_id"] = service_id
        
        await self._ws.send(json.dumps(message))
        
        # 等待响应
        try:
            response = await asyncio.wait_for(
                self._ws.recv(),
                timeout=5.0
            )
            data = json.loads(response)
            return data.get("messages", [])
        except asyncio.TimeoutError:
            return []
    
    async def listen_for_messages(
        self,
        callback: Callable[[dict], None]
    ):
        """
        简单的事件监听（同步回调）
        
        Args:
            callback: 消息回调函数
        """
        async for msg in self.messages():
            callback(msg)


# 便捷函数
async def quick_send(
    hub_url: str,
    agent_id: str,
    target_agent: str,
    content: str
) -> dict:
    """快速发送消息"""
    client = ChatClient(hub_url=hub_url, agent_id=agent_id)
    try:
        await client.connect()
        return await client.send_message(target_agent, content)
    finally:
        await client.disconnect()


if __name__ == "__main__":
    async def demo():
        # 示例用法
        client = ChatClient(
            hub_url="ws://localhost:8765",
            agent_id="demo-agent"
        )
        
        # 监听消息
        async def on_msg(msg):
            print(f"收到: {msg}")
        
        # 启动监听
        listener = asyncio.create_task(client.listen_for_messages(on_msg))
        
        # 发送消息
        await client.send_message(
            target_agent="other-agent",
            content="Hello!"
        )
        
        # 等待一段时间
        await asyncio.sleep(10)
        
        # 关闭
        listener.cancel()
        await client.disconnect()
    
    asyncio.run(demo())