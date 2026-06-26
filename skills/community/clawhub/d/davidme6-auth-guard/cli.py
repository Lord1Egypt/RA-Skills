#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auth Guard 命令行工具
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from auth_guard import AuthGuard


def cmd_status(args):
    """显示状态"""
    guard = AuthGuard()
    
    print("🔐 Auth Guard 状态")
    print("=" * 60)
    print(f"启用状态：{'✅ 已启用' if guard.config.get('enabled') else '❌ 已禁用'}")
    print(f"运行模式：{guard.config.get('mode', 'STRICT')}")
    print(f"超时时间：{guard.config.get('timeout_seconds', 300)}秒")
    print(f"通知渠道：{guard.config.get('notification', {}).get('channel', 'none')}")
    print(f"API 密钥：{guard.config.get('security', {}).get('api_key', 'N/A')[:16]}...")
    print("=" * 60)


def cmd_pending(args):
    """查看待处理请求"""
    guard = AuthGuard()
    pending = guard.get_pending_requests()
    
    if not pending:
        print("✅ 没有待处理的授权请求")
        return
    
    print(f"📋 待处理请求 ({len(pending)})")
    print("=" * 60)
    
    for req in pending:
        print(f"\n请求 ID: {req.get('request_id')}")
        print(f"服务：{req.get('service')}")
        print(f"操作：{req.get('action')}")
        print(f"请求时间：{req.get('requested_at')}")
        print("-" * 60)


def cmd_approve(args):
    """批准请求"""
    decision_path = os.path.expanduser(f"~/.auth_guard/decisions/{args.request_id}.json")
    Path(decision_path).parent.mkdir(parents=True, exist_ok=True)
    
    decision = {
        "approved": True,
        "decided_at": datetime.utcnow().isoformat() + "Z",
        "ttl": args.ttl if hasattr(args, 'ttl') else 3600
    }
    
    with open(decision_path, 'w', encoding='utf-8') as f:
        json.dump(decision, f, indent=2)
    
    print(f"✅ 已批准请求 {args.request_id}")


def cmd_deny(args):
    """拒绝请求"""
    decision_path = os.path.expanduser(f"~/.auth_guard/decisions/{args.request_id}.json")
    Path(decision_path).parent.mkdir(parents=True, exist_ok=True)
    
    decision = {
        "approved": False,
        "reason": args.reason if hasattr(args, 'reason') else "用户拒绝",
        "decided_at": datetime.utcnow().isoformat() + "Z"
    }
    
    with open(decision_path, 'w', encoding='utf-8') as f:
        json.dump(decision, f, indent=2)
    
    print(f"❌ 已拒绝请求 {args.request_id}")


def cmd_audit(args):
    """查看审计日志"""
    audit_log_path = os.path.expanduser("~/.auth_guard/audit_log.jsonl")
    
    if not os.path.exists(audit_log_path):
        print("❌ 审计日志不存在")
        return
    
    print("📊 审计日志")
    print("=" * 60)
    
    count = 0
    with open(audit_log_path, 'r', encoding='utf-8') as f:
        for line in f:
            if args.today:
                entry = json.loads(line)
                entry_date = entry.get('timestamp', '')[:10]
                today = datetime.utcnow().strftime('%Y-%m-%d')
                if entry_date != today:
                    continue
            
            print(line.strip())
            count += 1
            
            if args.limit and count >= args.limit:
                break
    
    print("=" * 60)
    print(f"共 {count} 条记录")


def cmd_emergency_stop(args):
    """紧急停止"""
    guard = AuthGuard()
    guard.emergency_stop()


def cmd_config(args):
    """显示/编辑配置"""
    config_path = os.path.expanduser("~/.auth_guard/config.json")
    
    if args.show:
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
        else:
            print("❌ 配置文件不存在")
    elif args.init:
        guard = AuthGuard()
        guard._save_config()
        print(f"✅ 配置文件已创建：{config_path}")


def main():
    parser = argparse.ArgumentParser(description="Auth Guard 命令行工具")
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # status
    status_parser = subparsers.add_parser('status', help='显示状态')
    status_parser.set_defaults(func=cmd_status)
    
    # pending
    pending_parser = subparsers.add_parser('pending', help='查看待处理请求')
    pending_parser.set_defaults(func=cmd_pending)
    
    # approve
    approve_parser = subparsers.add_parser('approve', help='批准请求')
    approve_parser.add_argument('request_id', help='请求 ID')
    approve_parser.add_argument('--ttl', type=int, default=3600, help='授权有效期（秒）')
    approve_parser.set_defaults(func=cmd_approve)
    
    # deny
    deny_parser = subparsers.add_parser('deny', help='拒绝请求')
    deny_parser.add_argument('request_id', help='请求 ID')
    deny_parser.add_argument('--reason', default='用户拒绝', help='拒绝原因')
    deny_parser.set_defaults(func=cmd_deny)
    
    # audit
    audit_parser = subparsers.add_parser('audit', help='查看审计日志')
    audit_parser.add_argument('--today', action='store_true', help='仅显示今天')
    audit_parser.add_argument('--limit', type=int, help='显示条数限制')
    audit_parser.set_defaults(func=cmd_audit)
    
    # emergency-stop
    stop_parser = subparsers.add_parser('emergency-stop', help='紧急停止所有授权')
    stop_parser.set_defaults(func=cmd_emergency_stop)
    
    # config
    config_parser = subparsers.add_parser('config', help='配置管理')
    config_parser.add_argument('--show', action='store_true', help='显示配置')
    config_parser.add_argument('--init', action='store_true', help='初始化配置')
    config_parser.set_defaults(func=cmd_config)
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
