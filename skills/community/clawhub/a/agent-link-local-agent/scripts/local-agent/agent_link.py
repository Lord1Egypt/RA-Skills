#!/usr/bin/env python3
"""
Agent Link - 本地 Agent 客户端
连接中转服务器，发送和接收消息
"""

import asyncio
import json
import hmac
import hashlib
import argparse
import logging
import os
from datetime import datetime
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("agent-link-client")


@dataclass
class Message:
    """消息类"""
    from_agent: str
    to_agent: str
    message: str
    timestamp: datetime


class AgentLink:
    """Agent Link 客户端核心类"""

    def __init__(
        self,
        relay_url: str,
        secret: str,
        instance_id: str,
        agent_id: str,
        config_path: Optional[str] = None
    ):
        self.relay_url = relay_url
        self.secret = secret
        self.instance_id = instance_id
        self.agent_id = agent_id
        self.config_path = config_path

        self.websocket = None
        self.connected = False
        self.message_handlers: Dict[str, Callable] = {}
        self.connect_task = None
        self.reconnect_interval = 5  # 重连间隔（秒）
        self.auto_reconnect = True

    def sign_message(self, message: str) -> str:
        """签名消息"""
        return hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

    async def connect(self):
        """连接中转服务器"""
        try:
            import websockets
        except ImportError:
            logger.error("Please install websockets: pip install websockets")
            return False

        while True:
            try:
                logger.info(f"Connecting to relay server: {self.relay_url}")
                self.websocket = await websockets.connect(self.relay_url)

                # 发送注册消息
                register_msg = {
                    "type": "register",
                    "instance_id": self.instance_id,
                    "signature": self.sign_message(
                        f"register:{self.instance_id}:{datetime.now().isoformat()[:19]}"
                    )
                }
                await self.websocket.send(json.dumps(register_msg))

                # 等待注册响应
                response = await self.websocket.recv()
                data = json.loads(response)

                if data.get("type") == "error":
                    logger.error(f"Registration failed: {data.get('message')}")
                    return False

                if data.get("type") == "registered":
                    self.connected = True
                    logger.info(f"Connected to relay server as {self.instance_id}/{self.agent_id}")
                    await self.message_loop()
                    return True

            except Exception as e:
                logger.error(f"Connection error: {e}")
                if not self.auto_reconnect:
                    return False

                logger.info(f"Reconnecting in {self.reconnect_interval}s...")
                await asyncio.sleep(self.reconnect_interval)

    async def message_loop(self):
        """消息循环"""
        try:
            async for message in self.websocket:
                await self.handle_message(message)
        except Exception as e:
            logger.error(f"Message loop error: {e}")
            self.connected = False

    async def handle_message(self, message_str: str):
        """处理收到的消息"""
        try:
            data = json.loads(message_str)
            msg_type = data.get("type")

            if msg_type == "pong":
                return

            if msg_type == "delivered":
                logger.debug(f"Message delivered to {data.get('to')}")
                return

            if msg_type == "message":
                from_agent = data.get("from")
                to_agent = data.get("to")
                message = data.get("message")

                msg = Message(
                    from_agent=from_agent,
                    to_agent=to_agent,
                    message=message,
                    timestamp=datetime.now()
                )

                logger.info(f"Received message from {from_agent}: {message[:50]}...")

                # 调用消息处理器
                full_to = f"{self.instance_id}/{self.agent_id}"
                if to_agent == full_to or to_agent == self.agent_id:
                    for handler in self.message_handlers.values():
                        try:
                            handler(msg)
                        except Exception as e:
                            logger.error(f"Message handler error: {e}")

        except Exception as e:
            logger.error(f"Handle message error: {e}")

    async def send(self, to_agent: str, message: str):
        """发送消息"""
        if not self.connected or not self.websocket:
            logger.error("Not connected to relay server")
            return False

        try:
            # 如果 to_agent 不包含 instance_id，默认是同一实例
            if "/" not in to_agent:
                full_to = f"{self.instance_id}/{to_agent}"
            else:
                full_to = to_agent

            full_from = f"{self.instance_id}/{self.agent_id}"
            message_to_sign = f"send:{full_from}:{full_to}:{message}"

            send_msg = {
                "type": "send",
                "from": full_from,
                "to": full_to,
                "message": message,
                "signature": self.sign_message(message_to_sign)
            }

            await self.websocket.send(json.dumps(send_msg))
            logger.info(f"Sent message to {full_to}: {message[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Send message error: {e}")
            return False

    def on_message(self, handler: Callable[[Message], None]):
        """注册消息处理器"""
        handler_id = id(handler)
        self.message_handlers[handler_id] = handler
        return handler_id

    def remove_handler(self, handler_id: int):
        """移除消息处理器"""
        if handler_id in self.message_handlers:
            del self.message_handlers[handler_id]

    async def disconnect(self):
        """断开连接"""
        self.auto_reconnect = False
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info("Disconnected from relay server")

    @classmethod
    def from_config(cls, config_path: str):
        """从配置文件创建实例"""
        with open(config_path, 'r') as f:
            config = json.load(f)

        return cls(
            relay_url=config.get("relay_url"),
            secret=config.get("secret"),
            instance_id=config.get("instance_id"),
            agent_id=config.get("agent_id"),
            config_path=config_path
        )


def main():
    parser = argparse.ArgumentParser(description="Agent Link Client")
    parser.add_argument("--config", type=str, help="Config file path")
    parser.add_argument("--relay-url", type=str, help="Relay server URL")
    parser.add_argument("--secret", type=str, help="Shared secret key")
    parser.add_argument("--instance-id", type=str, help="Instance ID")
    parser.add_argument("--agent-id", type=str, help="Agent ID")
    parser.add_argument("--test", action="store_true", help="Run in test mode")

    args = parser.parse_args()

    # 创建客户端实例
    if args.config:
        client = AgentLink.from_config(args.config)
    else:
        if not all([args.relay_url, args.secret, args.instance_id, args.agent_id]):
            print("Error: --config or --relay-url/--secret/--instance-id/--agent-id required")
            return

        client = AgentLink(
            relay_url=args.relay_url,
            secret=args.secret,
            instance_id=args.instance_id,
            agent_id=args.agent_id
        )

    # 测试模式：注册一个简单的消息处理器
    if args.test:
        @client.on_message
        def handle_test_message(msg: Message):
            print(f"\n📨 Received from {msg.from_agent}: {msg.message}")
            print(f"⏰ Time: {msg.timestamp}")

        # 启动一个简单的交互界面
        async def test_sender():
            await asyncio.sleep(1)  # 等待连接
            print("\n" + "="*50)
            print("Agent Link Test Mode")
            print("="*50)
            print("Commands:")
            print("  send <to_agent> <message> - Send a message")
            print("  quit - Exit")
            print("="*50 + "\n")

            while True:
                try:
                    line = await asyncio.get_event_loop().run_in_executor(
                        None,
                        input,
                        "> "
                    )

                    if line.strip().lower() in ["quit", "exit", "q"]:
                        await client.disconnect()
                        break

                    if line.strip().startswith("send "):
                        parts = line.split(" ", 2)
                        if len(parts) >= 3:
                            to_agent = parts[1]
                            message = parts[2]
                            await client.send(to_agent, message)
                        else:
                            print("Usage: send <to_agent> <message>")

                except (EOFError, KeyboardInterrupt):
                    await client.disconnect()
                    break

        # 同时运行连接和测试发送器
        async def main_loop():
            connect_task = asyncio.create_task(client.connect())
            sender_task = asyncio.create_task(test_sender())

            done, pending = await asyncio.wait(
                [connect_task, sender_task],
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in pending:
                task.cancel()

        asyncio.run(main_loop())
    else:
        # 正常模式：只连接
        asyncio.run(client.connect())


if __name__ == "__main__":
    main()
