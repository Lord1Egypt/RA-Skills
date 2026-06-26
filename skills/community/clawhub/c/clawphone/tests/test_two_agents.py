"""
测试两个 ClawPhone Agent 互通
场景：
  - 启动 1 个 ClawMesh server
  - 启动 2 个 client（Alice, Bob）
  - 各自注册号码
  - Alice 呼叫 Bob（Bob 的 node_id 未知，需自动发现）
  - Bob 收到消息
"""

import asyncio
import json
import logging
import sys
import os

# 添加项目根目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from node.server import ClawMeshServer
from node.client import ClawMeshClient
from skills.clawphone.adapter.clawphone import ClawPhone, _phone as global_phone

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger("test")

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8765


async def start_server():
    server = ClawMeshServer(SERVER_HOST, SERVER_PORT)
    await server.start()
    logger.info(f"Server started on {SERVER_HOST}:{SERVER_PORT}")
    return server


async def start_client(node_id: str, phone_alias: str):
    client = ClawMeshClient(node_id, f"ws://{SERVER_HOST}:{SERVER_PORT}")
    await client.connect()
    logger.info(f"Client {node_id} connected")

    # 注入 ClawPhone
    phone = ClawPhone()
    phone.set_network(client)
    phone_id = phone.register(phone_alias)
    logger.info(f"{node_id} 注册号码: {phone_id}")

    return client, phone


async def main():
    # 1. 启动 server
    server = await start_server()

    # 2. 启动 Alice
    alice_client, alice_phone = await start_client("CL-ALICE-001", "alice")
    alice_phone_id = alice_phone.get_my_phone()
    logger.info(f"Alice 号码: {alice_phone_id}")

    # 3. 启动 Bob
    bob_client, bob_phone = await start_client("CL-BOB-001", "bob")
    bob_phone_id = bob_phone.get_my_phone()
    logger.info(f"Bob 号码: {bob_phone_id}")

    # 4. Bob 设置消息接收
    def bob_on_message(msg):
        logger.info(f"Bob 收到来自 {msg.get('from')} 的消息: {msg.get('content')}")

    bob_phone.on_message = bob_on_message

    # 5. Alice 呼叫 Bob（Bob 的 node_id 未知）
    logger.info("Alice 呼叫 Bob（自动发现 node_id）...")
    success = alice_phone.call(bob_phone_id, "Hello Bob! This is Alice.")
    logger.info(f"呼叫结果: {success}")

    # 6. 等待消息传递
    await asyncio.sleep(3)

    # 7. 清理
    await alice_client.disconnect()
    await bob_client.disconnect()
    await server.stop()
    logger.info("测试结束")


if __name__ == "__main__":
    asyncio.run(main())
