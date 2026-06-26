#!/usr/bin/env python3
"""
执行日志记录工具
记录脚本执行历史，支持审计和复盘
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 日志文件路径
LOG_FILE = Path(__file__).parent / ".execution_log.json"


def load_log():
    """加载执行日志"""
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('executions', [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_log(executions):
    """保存执行日志"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'executions': executions,
            'last_updated': datetime.utcnow().isoformat() + 'Z'
        }, f, ensure_ascii=False, indent=2)


def add_execution(record):
    """
    添加执行记录

    Args:
        record: 执行记录字典，包含:
            - eventid: 告警ID (可选)
            - ip: 主机IP
            - script_id: 脚本ID
            - script_name: 脚本名称
            - status: 执行状态 (success/failed/timeout)
            - execution_id: 任务ID (可选)
            - user: 用户ID (可选)
            - output: 执行输出 (可选)
            - error: 错误信息 (可选)
    """
    executions = load_log()

    # 添加时间戳
    record['timestamp'] = datetime.utcnow().isoformat() + 'Z'

    # 添加到日志
    executions.append(record)

    # 保存
    save_log(executions)

    return record


def get_recent_executions(limit=10):
    """获取最近N条执行记录"""
    executions = load_log()
    # 按时间倒序
    executions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return executions[:limit]


def get_executions_by_ip(ip, limit=10):
    """获取指定IP的执行记录"""
    executions = load_log()
    filtered = [e for e in executions if e.get('ip') == ip]
    filtered.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    return filtered[:limit]


def get_executions_by_eventid(eventid):
    """获取指定告警ID的执行记录"""
    executions = load_log()
    return [e for e in executions if e.get('eventid') == eventid]


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: log_execution.py <command> [args]")
        print("命令:")
        print("  add <ip> <script_id> <script_name> <status> [execution_id] [eventid] [user]")
        print("  list [limit]")
        print("  by-ip <ip> [limit]")
        print("  by-event <eventid>")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) < 5:
            print("❌ 参数不足", file=sys.stderr)
            print("用法: log_execution.py add <ip> <script_id> <script_name> <status> [execution_id] [eventid] [user]")
            sys.exit(1)

        record = {
            'ip': sys.argv[2],
            'script_id': int(sys.argv[3]),
            'script_name': sys.argv[4],
            'status': sys.argv[5]
        }

        if len(sys.argv) > 6:
            record['execution_id'] = int(sys.argv[6])
        if len(sys.argv) > 7:
            record['eventid'] = sys.argv[7]
        if len(sys.argv) > 8:
            record['user'] = sys.argv[8]

        result = add_execution(record)
        print(f"✅ 已记录执行: {record['script_name']} @ {record['ip']} ({record['status']})")
        print(f"   时间: {result['timestamp']}")

    elif command == 'list':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        executions = get_recent_executions(limit)

        print(f"📋 最近 {len(executions)} 条执行记录:")
        for exe in executions:
            status_emoji = "✅" if exe.get('status') == 'success' else "❌"
            print(f"\n{status_emoji} {exe.get('timestamp', 'Unknown')}")
            print(f"   脚本: {exe.get('script_name', 'Unknown')} (ID: {exe.get('script_id', 'N/A')})")
            print(f"   主机: {exe.get('ip', 'Unknown')}")
            if exe.get('eventid'):
                print(f"   告警ID: {exe['eventid']}")
            if exe.get('execution_id'):
                print(f"   任务ID: {exe['execution_id']}")
            if exe.get('user'):
                print(f"   操作用户: {exe['user']}")

    elif command == 'by-ip':
        if len(sys.argv) < 3:
            print("❌ 参数不足", file=sys.stderr)
            print("用法: log_execution.py by-ip <ip> [limit]")
            sys.exit(1)

        ip = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        executions = get_executions_by_ip(ip, limit)

        print(f"📋 主机 {ip} 的执行记录 ({len(executions)} 条):")
        for exe in executions:
            status_emoji = "✅" if exe.get('status') == 'success' else "❌"
            print(f"\n{status_emoji} {exe.get('timestamp', 'Unknown')}")
            print(f"   脚本: {exe.get('script_name', 'Unknown')} (ID: {exe.get('script_id', 'N/A')})")

    elif command == 'by-event':
        if len(sys.argv) < 3:
            print("❌ 参数不足", file=sys.stderr)
            print("用法: log_execution.py by-event <eventid>")
            sys.exit(1)

        eventid = sys.argv[2]
        executions = get_executions_by_eventid(eventid)

        print(f"📋 告警 {eventid} 的执行记录 ({len(executions)} 条):")
        for exe in executions:
            status_emoji = "✅" if exe.get('status') == 'success' else "❌"
            print(f"\n{status_emoji} {exe.get('timestamp', 'Unknown')}")
            print(f"   脚本: {exe.get('script_name', 'Unknown')}")
            print(f"   主机: {exe.get('ip', 'Unknown')}")

    else:
        print(f"❌ 未知命令: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
