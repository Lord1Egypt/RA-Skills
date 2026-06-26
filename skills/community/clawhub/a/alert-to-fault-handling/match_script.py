#!/usr/bin/env python3
"""
告警与脚本匹配工具
根据告警信息、群组上下文匹配合适的故障处理脚本
"""

import json
import sys
from pathlib import Path

# 配置文件路径
SCRIPTS_MAP_FILE = Path(__file__).parent / ".scripts_map.json"


def load_scripts_map():
    """加载脚本映射配置"""
    try:
        with open(SCRIPTS_MAP_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 配置文件不存在: {SCRIPTS_MAP_FILE}", file=sys.stderr)
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}", file=sys.stderr)
        return {}


def match_script(alert_info, chat_id=None):
    """
    根据告警信息匹配脚本

    Args:
        alert_info: 告警信息字典，包含:
            - eventid: 告警ID
            - ip: 主机IP
            - description: 告警描述
            - classification: 监控分类ID
        chat_id: 当前飞书群组ID

    Returns:
        匹配到的脚本配置，如果没有匹配返回 None
    """
    scripts_map = load_scripts_map()

    # 获取告警描述和分类
    description = alert_info.get('description', '')
    classification = alert_info.get('classification')
    ip = alert_info.get('ip', '')
    eventid = alert_info.get('eventid', '')

    # 遍历所有脚本配置
    for script_key, script_config in scripts_map.items():
        # 检查群组是否匹配
        if chat_id and chat_id not in script_config.get('chat_groups', []):
            continue

        # 检查分类是否匹配
        if classification and classification not in script_config.get('classifications', []):
            continue

        # 检查关键词是否匹配
        keywords = script_config.get('keywords', [])
        keyword_matched = any(kw.lower() in description.lower() for kw in keywords)

        if keyword_matched:
            return {
                'key': script_key,
                'name': script_config['name'],
                'script_id': script_config['script_id'],
                'description': script_config['description'],
                'matched_keyword': next((kw for kw in keywords if kw.lower() in description.lower()), None)
            }

    return None


def list_all_scripts():
    """列出所有可用脚本"""
    scripts_map = load_scripts_map()
    result = []
    for key, config in scripts_map.items():
        result.append({
            'key': key,
            'name': config['name'],
            'script_id': config['script_id'],
            'keywords': config['keywords'],
            'classifications': config['classifications'],
            'description': config['description']
        })
    return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: match_script.py <command> [args]")
        print("命令:")
        print("  match <eventid> <ip> <description> [classification] [chat_id]")
        print("  list")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'match':
        if len(sys.argv) < 5:
            print("❌ 参数不足", file=sys.stderr)
            print("用法: match_script.py match <eventid> <ip> <description> [classification] [chat_id]")
            sys.exit(1)

        eventid = sys.argv[2]
        ip = sys.argv[3]
        description = sys.argv[4]
        classification = int(sys.argv[5]) if len(sys.argv) > 5 else None
        chat_id = sys.argv[6] if len(sys.argv) > 6 else None

        alert_info = {
            'eventid': eventid,
            'ip': ip,
            'description': description,
            'classification': classification
        }

        matched = match_script(alert_info, chat_id)

        if matched:
            print(f"✅ 匹配到脚本:")
            print(f"   名称: {matched['name']}")
            print(f"   脚本ID: {matched['script_id']}")
            print(f"   说明: {matched['description']}")
            print(f"   匹配关键词: {matched['matched_keyword']}")
            sys.exit(0)
        else:
            print("❌ 未找到匹配的脚本")
            sys.exit(1)

    elif command == 'list':
        scripts = list_all_scripts()
        print(f"📋 可用脚本列表 ({len(scripts)} 个):")
        for script in scripts:
            print(f"\n🔹 {script['name']} (ID: {script['script_id']})")
            print(f"   关键词: {', '.join(script['keywords'])}")
            print(f"   分类: {script['classifications']}")
            print(f"   说明: {script['description']}")
        sys.exit(0)

    else:
        print(f"❌ 未知命令: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
