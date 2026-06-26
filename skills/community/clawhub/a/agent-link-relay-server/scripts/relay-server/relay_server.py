#!/usr/bin/env python3
"""
Agent Link - 中转服务器
支持跨设备 OpenClaw 实例和 Agent 的安全通讯
"""

import asyncio
import json
import hmac
import hashlib
import argparse
import logging
from datetime import datetime
from typing import Dict, Set, Optional
from dataclasses import dataclass

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("agent-link-relay")


@dataclass
class RegisteredInstance:
    """已注册的 OpenClaw 实例"""
    instance_id: str
    name: str
    public_key: str
    registered_at: datetime


@dataclass
class ConnectedClient:
    """已连接的客户端"""
    instance_id: str
    websocket: any
    connected_at: datetime


class RelayServer:
    """中转服务器核心类"""

    def __init__(self, secret: str, port: int = 8765):
        self.secret = secret
        self.port = port
        self.registered_instances: Dict[str, RegisteredInstance] = {}
        self.connected_clients: Dict[str, ConnectedClient] = {}
        self.message_history: Set[str] = set()  # 防止重复消息

    def verify_signature(self, message: str, signature: str) -> bool:
        """验证消息签名"""
        expected = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    def register_instance(self, instance_id: str, name: str, public_key: str) -> bool:
        """注册 OpenClaw 实例"""
        if instance_id in self.registered_instances:
            logger.warning(f"Instance {instance_id} already registered")
            return False

        self.registered_instances[instance_id] = RegisteredInstance(
            instance_id=instance_id,
            name=name,
            public_key=public_key,
            registered_at=datetime.now()
        )
        logger.info(f"Registered instance: {instance_id} ({name})")
        return True

    async def handle_client(self, websocket, path):
        """处理客户端连接"""
        client = None
        try:
            # 等待注册消息
            register_msg = await websocket.recv()
            data = json.loads(register_msg)

            if data.get("type") != "register":
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "First message must be register"
                }))
                return

            instance_id = data.get("instance_id")
            signature = data.get("signature")

            # 验证签名
            message_to_sign = f"register:{instance_id}:{datetime.now().isoformat()[:19]}"
            if not self.verify_signature(message_to_sign, signature):
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid signature"
                }))
                return

            # 检查实例是否注册
            if instance_id not in self.registered_instances:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Instance not registered"
                }))
                return

            # 注册连接
            client = ConnectedClient(
                instance_id=instance_id,
                websocket=websocket,
                connected_at=datetime.now()
            )
            self.connected_clients[instance_id] = client
            logger.info(f"Client connected: {instance_id}")

            await websocket.send(json.dumps({
                "type": "registered",
                "instance_id": instance_id
            }))

            # 处理消息循环
            async for message in websocket:
                await self.handle_message(client, message)

        except Exception as e:
            logger.error(f"Client error: {e}")
        finally:
            if client and client.instance_id in self.connected_clients:
                del self.connected_clients[client.instance_id]
                logger.info(f"Client disconnected: {client.instance_id}")

    async def handle_message(self, sender: ConnectedClient, message_str: str):
        """处理收到的消息"""
        try:
            data = json.loads(message_str)
            msg_type = data.get("type")

            if msg_type == "ping":
                await sender.websocket.send(json.dumps({"type": "pong"}))
                return

            if msg_type != "send":
                return

            # 验证消息签名
            from_agent = data.get("from")
            to_agent = data.get("to")
            message = data.get("message")
            signature = data.get("signature")

            message_to_sign = f"send:{from_agent}:{to_agent}:{message}"
            if not self.verify_signature(message_to_sign, signature):
                await sender.websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid signature"
                }))
                return

            # 防止重复消息
            msg_id = f"{from_agent}:{to_agent}:{hashlib.md5(message.encode()).hexdigest()}"
            if msg_id in self.message_history:
                return
            self.message_history.add(msg_id)

            # 解析目标
            if "/" in to_agent:
                target_instance, target_agent = to_agent.split("/", 1)
            else:
                # 如果只指定了 agent_id，假设是同一实例
                target_instance = sender.instance_id
                target_agent = to_agent

            # 查找目标实例
            if target_instance not in self.connected_clients:
                await sender.websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Target instance {target_instance} not connected"
                }))
                return

            # 转发消息
            target_client = self.connected_clients[target_instance]
            await target_client.websocket.send(json.dumps({
                "type": "message",
                "from": from_agent,
                "to": to_agent,
                "message": message
            }))

            # 发送确认
            await sender.websocket.send(json.dumps({
                "type": "delivered",
                "to": to_agent
            }))

            logger.info(f"Message forwarded: {from_agent} -> {to_agent}")

        except Exception as e:
            logger.error(f"Message handling error: {e}")

    async def start(self):
        """启动中转服务器"""
        try:
            import websockets
        except ImportError:
            logger.error("Please install websockets: pip install websockets")
            return

        server = await websockets.serve(
            self.handle_client,
            "0.0.0.0",
            self.port
        )
        logger.info(f"Relay server started on port {self.port}")
        await server.wait_closed()


def main():
    parser = argparse.ArgumentParser(description="Agent Link Relay Server")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on")
    parser.add_argument("--secret", type=str, required=True, help="Shared secret key")
    parser.add_argument("--config", type=str, help="Config file path")

    args = parser.parse_args()

    # 如果有配置文件，读取配置
    if args.config:
        import json
        with open(args.config, 'r') as f:
            config = json.load(f)
            if "port" in config:
                args.port = config["port"]
            if "secret" in config:
                args.secret = config["secret"]

    server = RelayServer(secret=args.secret, port=args.port)

    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")


if __name__ == "__main__":
    main()
