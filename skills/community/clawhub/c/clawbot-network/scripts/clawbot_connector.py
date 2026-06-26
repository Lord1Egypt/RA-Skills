#!/usr/bin/env python3
"""
ClawBot Network Connector
让任何设备上的 clawdbot 都能接入 Agent Network

用法:
1. 在 clawdbot 的 SOUL.md 或启动脚本中导入
2. 自动连接中央服务器
3. 接收来自其他 clawdbot 的消息和任务
"""

import asyncio
import json
import os
import sys
from typing import Optional, Callable, Dict, Any
from datetime import datetime

# 添加客户端路径
CLIENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'client')
sys.path.insert(0, CLIENT_DIR)

try:
    from python_client import AgentNetworkClient
except ImportError:
    print("❌ 请先安装 Python 客户端: pip install websockets requests")
    sys.exit(1)


class ClawBotConnector:
    """
    clawdbot 网络连接器
    
    让 clawdbot 能够:
    - 加入跨设备的群聊
    - 接收其他 clawdbot 的消息
    - 被其他设备 @提及
    - 接收分布式任务
    """
    
    def __init__(self, 
                 server_url: str = "ws://3.148.174.81:3002",
                 bot_id: Optional[str] = None,
                 bot_name: Optional[str] = None,
                 device_name: Optional[str] = None):
        """
        初始化连接器
        
        Args:
            server_url: Agent Network 服务器地址
            bot_id: clawdbot 唯一标识 (如 "clawdbot-macbook-001")
            bot_name: 显示名称 (如 "MacBook Bot")
            device_name: 设备名称 (如 "MacBook Pro")
        """
        self.server_url = server_url
        self.bot_id = bot_id or self._generate_bot_id()
        self.bot_name = bot_name or self._detect_bot_name()
        self.device_name = device_name or self._detect_device()
        
        self.client: Optional[AgentNetworkClient] = None
        self.connected = False
        self.message_handlers: list = []
        self.mention_handlers: list = []
        self.task_handlers: list = []
        
    def _generate_bot_id(self) -> str:
        """生成唯一 bot ID"""
        import socket
        hostname = socket.gethostname().replace('.', '-')
        return f"clawdbot-{hostname}"
    
    def _detect_bot_name(self) -> str:
        """检测 bot 名称"""
        # 尝试读取 SOUL.md 中的名称
        soul_path = os.path.expanduser('~/.openclaw/workspace-clawdbot/SOUL.md')
        if os.path.exists(soul_path):
            try:
                with open(soul_path) as f:
                    content = f.read()
                    # 查找 Name: xxx 或 - **Name:** xxx
                    import re
                    match = re.search(r'(?:Name:|\*\*Name:\*\*)\s*(.+)', content)
                    if match:
                        return match.group(1).strip()
            except:
                pass
        
        # 默认使用主机名
        import socket
        return f"ClawBot@{socket.gethostname()}"
    
    def _detect_device(self) -> str:
        """检测设备类型"""
        import platform
        system = platform.system()
        
        if system == "Darwin":
            # macOS - 检测是 MacBook 还是 Mac Mini
            try:
                result = os.popen("sysctl -n hw.model").read().strip()
                if "MacBook" in result:
                    return "MacBook"
                elif "Macmini" in result:
                    return "Mac Mini"
                return result
            except:
                return "Mac"
        elif system == "Linux":
            return "Linux Server"
        elif system == "Windows":
            return "Windows PC"
        return system
    
    async def connect(self) -> bool:
        """
        连接到 Agent Network
        
        Returns:
            是否连接成功
        """
        try:
            print(f"🔌 [{self.bot_name}] 正在连接 Agent Network...")
            print(f"   Server: {self.server_url}")
            print(f"   Bot ID: {self.bot_id}")
            
            self.client = AgentNetworkClient(self.server_url)
            
            await self.client.connect(
                agent_id=self.bot_id,
                name=self.bot_name,
                role="clawdbot",
                device=self.device_name
            )
            
            # 加入默认群组
            await self.client.join_group("clawdbots")
            
            # 设置消息处理器
            self._setup_handlers()
            
            self.connected = True
            print(f"✅ [{self.bot_name}] 已连接到网络!")
            
            # 发送上线通知
            await self.client.send_message(
                "clawdbots",
                f"🟢 {self.bot_name} ({self.device_name}) 已上线"
            )
            
            return True
            
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def _setup_handlers(self):
        """设置消息处理器"""
        
        @self.client.on("message")
        def on_message(msg):
            """处理群消息"""
            # 转发给注册的处理函数
            for handler in self.message_handlers:
                try:
                    handler(msg)
                except Exception as e:
                    print(f"Message handler error: {e}")
        
        @self.client.on("mention")
        def on_mention(msg):
            """处理 @提及"""
            print(f"🔔 [{self.bot_name}] 被 @{msg['fromName']} 提及")
            
            # 转发给提及处理函数
            for handler in self.mention_handlers:
                try:
                    handler(msg)
                except Exception as e:
                    print(f"Mention handler error: {e}")
        
        @self.client.on("task_assigned")
        def on_task(task):
            """处理任务指派"""
            print(f"📋 [{self.bot_name}] 收到新任务: {task['title']}")
            
            for handler in self.task_handlers:
                try:
                    handler(task)
                except Exception as e:
                    print(f"Task handler error: {e}")
        
        @self.client.on("disconnected")
        def on_disconnect():
            print(f"⚠️ [{self.bot_name}] 连接断开，尝试重连...")
            self.connected = False
    
    def on_message(self, handler: Callable):
        """注册消息处理器"""
        self.message_handlers.append(handler)
        return handler
    
    def on_mention(self, handler: Callable):
        """注册提及处理器"""
        self.mention_handlers.append(handler)
        return handler
    
    def on_task(self, handler: Callable):
        """注册任务处理器"""
        self.task_handlers.append(handler)
        return handler
    
    async def send_message(self, content: str, group: str = "clawdbots"):
        """发送群消息"""
        if self.client and self.connected:
            await self.client.send_message(group, content)
    
    async def reply_to(self, original_msg: Dict, content: str):
        """回复某条消息"""
        group_id = original_msg.get('groupId', 'clawdbots')
        from_name = original_msg.get('fromName', 'unknown')
        await self.send_message(f"@{from_name} {content}", group_id)
    
    async def broadcast(self, content: str):
        """广播消息到所有群"""
        await self.send_message(content, "clawdbots")
    
    def get_online_bots(self) -> list:
        """获取在线的 clawdbot 列表"""
        if self.client:
            return self.client.get_agents()
        return []
    
    async def run_forever(self):
        """保持运行（阻塞）"""
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print(f"\n👋 [{self.bot_name}] 断开连接")
            await self.disconnect()
    
    async def disconnect(self):
        """断开连接"""
        if self.client:
            # 发送离线通知
            try:
                await self.client.send_message(
                    "clawdbots",
                    f"🔴 {self.bot_name} 已离线"
                )
            except:
                pass
            self.client.disconnect()
            self.connected = False


# ============ 便捷函数 ============

_connector: Optional[ClawBotConnector] = None

async def connect_to_network(server_url: str = "ws://3.148.174.81:3002") -> ClawBotConnector:
    """
    快速连接到 Agent Network
    
    用法:
        from clawbot_connector import connect_to_network
        
        connector = await connect_to_network()
        
        @connector.on_message
        def handle(msg):
            print(f"收到: {msg['content']}")
    """
    global _connector
    _connector = ClawBotConnector(server_url=server_url)
    await _connector.connect()
    return _connector


def get_connector() -> Optional[ClawBotConnector]:
    """获取当前连接器实例"""
    return _connector


# ============ 示例用法 ============

async def example():
    """示例: clawdbot 接入网络"""
    
    # 连接到网络
    bot = await connect_to_network()
    
    # 处理收到的消息
    @bot.on_message
    def on_message(msg):
        content = msg.get('content', '')
        from_name = msg.get('fromName', 'unknown')
        
        # 可以在这里集成到 clawdbot 的消息处理流程
        print(f"[{from_name}] {content}")
        
        # 例如：如果消息包含特定关键词，执行操作
        if "status" in content.lower():
            # 回复状态
            asyncio.create_task(bot.reply_to(msg, "✅ 运行正常"))
    
    # 处理被 @提及
    @bot.on_mention
    def on_mention(msg):
        content = msg.get('content', '')
        # 可以触发 clawdbot 的响应逻辑
        print(f"被提及: {content}")
    
    # 处理任务指派
    @bot.on_task
    def on_task(task):
        print(f"新任务: {task['title']}")
        # 可以用 sessions_spawn 创建子任务
        # sessions_spawn(agentId="sub-agent", task=task['description'])
    
    # 保持运行
    await bot.run_forever()


if __name__ == "__main__":
    print("🤖 ClawBot Network Connector")
    print("=" * 40)
    print()
    print("用法示例:")
    print()
    print("  from clawbot_connector import connect_to_network")
    print()
    print("  async def main():")
    print("      bot = await connect_to_network()")
    print()
    print("      @bot.on_message")
    print("      def handle(msg):")
    print("          print(f'收到: {msg[\"content\"]}')")
    print()
    print("      await bot.run_forever()")
    print()
    print("=" * 40)
    
    # 运行示例
    asyncio.run(example())
