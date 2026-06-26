#!/usr/bin/env python3
"""
ClawPhone Direct P2P 演示（无需 ClawMesh）
"""

import asyncio
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from skills.clawphone.adapter import start_direct_mode, register, add_contact, call, on_message


async def main():
    print("=== ClawPhone Direct P2P Demo ===")

    # 1. 启动 Direct 模式（随机端口）
    my_addr = await start_direct_mode()
    print(f"[*] 本节点地址: {my_addr}")

    # 2. 注册号码
    alias = input("输入你的别名 (default: agent): ").strip() or "agent"
    phone_id = register(alias)
    print(f"[+] 你的号码: {phone_id}")

    # 3. 输入对方信息（通过带外交换获得）
    print("\n--- 添加联系人 ---")
    other_phone = input("对方号码 (13位): ").strip()
    other_addr = input("对方地址 (host:port): ").strip()
    success = add_contact(other_phone, address=other_addr)
    if not success:
        print("[!] 添加联系人失败")
        return

    print(f"[+] 已添加联系人: {other_phone} @ {other_addr}")

    # 4. 设置消息接收
    def on_msg(msg):
        print(f"\n[收到] {msg.get('from')}: {msg.get('content')}\n> ", end="")

    on_message(on_msg)

    print("\n--- 开始聊天 ---")
    print("输入消息内容，Ctrl+C 退出\n")

    try:
        while True:
            msg = await asyncio.to_thread(input, "> ")
            if msg:
                success = call(other_phone, msg)
                if not success:
                    print("[!] 发送失败，请检查对方是否在线")
    except KeyboardInterrupt:
        print("\n[*] 退出")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
