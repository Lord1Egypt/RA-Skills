#!/usr/bin/env python3
"""
CFM CLI - 跨框架通信命令行工具
用法：
  python3 cfm_cli.py send <to> <message>
  python3 cfm_cli.py listen <agent_id> [--timeout N]
  python3 cfm_cli.py discover
  python3 cfm_cli.py history <agent_id> [--limit N]
"""

import sys
import json
import argparse
from cfm_messenger import CFMMessenger, quick_send, quick_receive

def cmd_send(args):
    """发送消息"""
    try:
        msg_id = quick_send(args.to, args.message, args.from_agent)
        print(f"✅ 消息已发送 (ID: {msg_id})")
        print(f"   {args.from_agent} → {args.to}: {args.message}")
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        sys.exit(1)

def cmd_listen(args):
    """监听消息"""
    print(f"👂 {args.agent_id} 开始监听消息...")
    print(f"   超时: {args.timeout}秒")
    print("   (Ctrl+C 停止)")
    print("-" * 40)
    
    try:
        msg = quick_receive(args.agent_id, args.timeout)
        if msg:
            print(f"📨 收到消息!")
            print(f"   发送者: {msg['from']}")
            print(f"   类型: {msg['type']}")
            print(f"   时间: {msg['timestamp']}")
            print(f"   内容: {msg['content']}")
        else:
            print("⏰ 超时，未收到消息")
    except KeyboardInterrupt:
        print("\n👋 停止监听")
    except Exception as e:
        print(f"❌ 监听失败: {e}")
        sys.exit(1)

def cmd_discover(args):
    """发现agents"""
    try:
        with CFMMessenger("discover-cli") as messenger:
            agents = messenger.discover_agents()
            
            if agents:
                print(f"🔍 发现 {len(agents)} 个agents:")
                for agent in agents:
                    print(f"   - {agent.get('id', 'unknown')}: {agent.get('status', 'unknown')}")
            else:
                print("🔍 未发现其他agents")
    except Exception as e:
        print(f"❌ 发现失败: {e}")
        sys.exit(1)

def cmd_history(args):
    """查看消息历史"""
    try:
        with CFMMessenger(args.agent_id) as messenger:
            messages = messenger.get_messages(limit=args.limit)
            
            if messages:
                print(f"📚 {args.agent_id} 的消息历史 ({len(messages)} 条):")
                print("-" * 40)
                for msg in messages:
                    direction = "📤" if msg.get('from') == args.agent_id else "📥"
                    print(f"{direction} [{msg.get('timestamp', '?')}] {msg.get('from', '?')} → {msg.get('to', '?')}")
                    print(f"   {msg.get('content', '?')}")
                    print()
            else:
                print(f"📚 {args.agent_id} 没有消息历史")
    except Exception as e:
        print(f"❌ 获取历史失败: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="CFM CLI - 跨框架通信工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # send 命令
    send_parser = subparsers.add_parser("send", help="发送消息")
    send_parser.add_argument("to", help="目标agent ID")
    send_parser.add_argument("message", help="消息内容")
    send_parser.add_argument("--from", dest="from_agent", default="cli", help="发送者ID (默认: cli)")
    
    # listen 命令
    listen_parser = subparsers.add_parser("listen", help="监听消息")
    listen_parser.add_argument("agent_id", help="本agent的ID")
    listen_parser.add_argument("--timeout", type=int, default=10, help="超时秒数 (默认: 10)")
    
    # discover 命令
    discover_parser = subparsers.add_parser("discover", help="发现其他agents")
    
    # history 命令
    history_parser = subparsers.add_parser("history", help="查看消息历史")
    history_parser.add_argument("agent_id", help="agent ID")
    history_parser.add_argument("--limit", type=int, default=20, help="最大条数 (默认: 20)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行对应命令
    if args.command == "send":
        cmd_send(args)
    elif args.command == "listen":
        cmd_listen(args)
    elif args.command == "discover":
        cmd_discover(args)
    elif args.command == "history":
        cmd_history(args)

if __name__ == "__main__":
    main()
