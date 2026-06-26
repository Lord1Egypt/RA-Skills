#!/usr/bin/env python3
"""
告警自动处理工作流主入口
协调告警检测、脚本匹配、用户确认、脚本执行、日志记录
"""

import json
import sys
import subprocess
from pathlib import Path

# 脚本目录
SCRIPT_DIR = Path(__file__).parent
FAULT_HANDLING_DIR = SCRIPT_DIR.parent / "fault-handling"
LERCLEE_API_DIR = SCRIPT_DIR.parent / "lerwee-api" / "scripts"


def extract_ip_from_alert(alert_info):
    """
    从告警信息中提取IP

    优先级:
    1. 告警信息中的 ip 字段
    2. 通过 objectid 查询主机详情获取 IP
    """
    # 1. 直接获取
    if 'ip' in alert_info and alert_info['ip']:
        return alert_info['ip']

    # 2. 通过 objectid 查询
    if 'objectid' in alert_info and alert_info['objectid']:
        try:
            result = subprocess.run(
                ['bash', LERCLEE_API_DIR / 'lerwee-api.sh', 'monitor', 'host-view',
                 json.dumps({'hostid': alert_info['objectid']})],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            if data.get('code') == 0 and 'ip' in data.get('data', {}):
                return data['data']['ip']
        except Exception as e:
            print(f"❌ 查询主机IP失败: {e}", file=sys.stderr)

    return None


def match_and_recommend(alert_info, chat_id=None):
    """
    匹配脚本并生成推荐消息

    Returns:
        (matched, message)
        - matched: 是否匹配到脚本
        - message: 推荐消息文本
    """
    ip = extract_ip_from_alert(alert_info)
    if not ip:
        return False, None

    # 构建告警描述
    description = alert_info.get('description', '')

    # 获取分类
    classification = alert_info.get('classification')

    # 调用匹配脚本
    try:
        result = subprocess.run(
            ['python3', SCRIPT_DIR / 'match_script.py', 'match',
             alert_info.get('eventid', ''),
             ip,
             description,
             str(classification) if classification else '',
             chat_id or ''],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            # 匹配成功
            lines = result.stdout.strip().split('\n')
            script_name = None
            script_id = None
            script_desc = None

            for line in lines:
                if line.startswith('   名称:'):
                    script_name = line.split(':', 1)[1].strip()
                elif line.startswith('   脚本ID:'):
                    script_id = line.split(':', 1)[1].strip()
                elif line.startswith('   说明:'):
                    script_desc = line.split(':', 1)[1].strip()

            message = f"""🤖 检测到告警可自动处理
📊 告警对象: {alert_info.get('hostname', 'Unknown')} ({ip})
🔑 告警ID: {alert_info.get('eventid', 'Unknown')}

💡 推荐操作: {script_name} (脚本ID: {script_id})
📝 说明: {script_desc}

👉 回复「执行」或「确认」自动运行脚本"""

            return True, message
        else:
            return False, None

    except Exception as e:
        print(f"❌ 脚本匹配失败: {e}", file=sys.stderr)
        return False, None


def execute_script(ip, script_id, eventid=None, user=None):
    """
    执行故障处理脚本

    Returns:
        执行结果字典
    """
    try:
        # 构建 fault-handling 命令
        cmd = [
            'python3',
            FAULT_HANDLING_DIR / 'run_script.py',
            '--hosts', ip,
            '--script-id', str(script_id)
        ]

        # 执行脚本
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=FAULT_HANDLING_DIR
        )

        # 解析输出
        output = result.stdout

        # 记录日志
        log_record = {
            'ip': ip,
            'script_id': script_id,
            'script_name': f'Script-{script_id}',
            'status': 'success' if result.returncode == 0 else 'failed',
            'eventid': eventid,
            'user': user,
            'output': output[:1000] if output else None  # 截取前1000字符
        }

        # 尝试解析 execution_id
        if output:
            import re
            match = re.search(r'任务ID[：:]\s*(\d+)', output)
            if match:
                log_record['execution_id'] = int(match.group(1))

        # 写入日志
        subprocess.run(
            ['python3', SCRIPT_DIR / 'log_execution.py', 'add',
             ip, str(script_id), log_record['script_name'], log_record['status'],
             str(log_record.get('execution_id', '')),
             eventid or '',
             user or ''],
            capture_output=True
        )

        return {
            'success': result.returncode == 0,
            'output': output,
            'log': log_record
        }

    except Exception as e:
        return {
            'success': False,
            'output': str(e),
            'log': None
        }


def close_alert(eventid, message="脚本执行成功，自动关闭告警"):
    """关闭告警"""
    try:
        result = subprocess.run(
            ['bash', LERCLEE_API_DIR / 'lerwee-api.sh', 'alert', 'problem-ack',
             json.dumps({
                 'eventid': eventid,
                 'action': 1,
                 'message': message
             })],
            capture_output=True,
            text=True
        )

        data = json.loads(result.stdout)
        return data.get('code') == 0

    except Exception as e:
        print(f"❌ 关闭告警失败: {e}", file=sys.stderr)
        return False


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: alert_workflow.py <command> [args]")
        print("Commands:")
        print("  check <eventid> <ip> <description> [classification] [chat_id]  # 检查并推荐脚本")
        print("  execute <ip> <script_id> [eventid] [user]                      # 执行脚本")
        print("  close <eventid> [message]                                       # 关闭告警")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'check':
        if len(sys.argv) < 5:
            print("❌ 参数不足", file=sys.stderr)
            sys.exit(1)

        alert_info = {
            'eventid': sys.argv[2],
            'ip': sys.argv[3],
            'description': sys.argv[4],
            'classification': int(sys.argv[5]) if len(sys.argv) > 5 else None,
            'objectid': None
        }
        chat_id = sys.argv[6] if len(sys.argv) > 6 else None

        matched, message = match_and_recommend(alert_info, chat_id)

        if matched:
            print(message)
            sys.exit(0)
        else:
            print("ℹ️ 未找到匹配的处理脚本")
            sys.exit(1)

    elif command == 'execute':
        if len(sys.argv) < 4:
            print("❌ 参数不足", file=sys.stderr)
            sys.exit(1)

        ip = sys.argv[2]
        script_id = int(sys.argv[3])
        eventid = sys.argv[4] if len(sys.argv) > 4 else None
        user = sys.argv[5] if len(sys.argv) > 5 else None

        print(f"🔧 正在为主机 {ip} 执行脚本...")
        result = execute_script(ip, script_id, eventid, user)

        if result['success']:
            print(result['output'])
            print("\n💾 已记录到执行日志")

            # 如果指定了 eventid，询问是否关闭告警
            if eventid:
                print(f"\n💡 提示: 告警 {eventid} 仍活跃，可手动关闭")
        else:
            print(f"❌ 执行失败: {result['output']}", file=sys.stderr)
            sys.exit(1)

    elif command == 'close':
        if len(sys.argv) < 3:
            print("❌ 参数不足", file=sys.stderr)
            sys.exit(1)

        eventid = sys.argv[2]
        message = sys.argv[3] if len(sys.argv) > 3 else "脚本执行成功，自动关闭告警"

        if close_alert(eventid, message):
            print(f"✅ 告警 {eventid} 已关闭")
        else:
            print(f"❌ 关闭告警失败", file=sys.stderr)
            sys.exit(1)

    else:
        print(f"❌ 未知命令: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
