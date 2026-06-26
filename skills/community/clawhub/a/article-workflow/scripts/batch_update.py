#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新工具 - 修复已有记录的字段

功能：
1. 批量添加负责人到所有记录
2. 更新来源平台映射
3. 补全缺失字段
"""

import json
import sys
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from field_mapper import load_config, format_person_field, map_source_platform


def print_header(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def batch_update_assignee(app_token: str, table_id: str, assignee_id: str, assignee_name: str = "用户"):
    """
    批量添加负责人到所有记录
    
    Args:
        app_token: Bitable App Token
        table_id: Table ID
        assignee_id: 负责人 open_id
        assignee_name: 负责人姓名
    """
    print_header(f"🔄 批量更新负责人")
    
    print(f"目标表格：{table_id}")
    print(f"负责人：{assignee_name} ({assignee_id})")
    print()
    
    # TODO: 调用飞书 API 获取所有记录
    # records = feishu_bitable_app_table_record(action="list", ...)
    
    print("⚠️  此功能需要飞书 API 支持")
    print("建议手动更新或使用飞书多维表格 API")
    print()
    
    # 示例代码
    print("示例代码：")
    print("""
from feishu_bitable_app_table_record import update_record

# 获取所有记录
records = list_all_records(app_token, table_id)

# 批量更新
for record in records:
    if '负责人' not in record['fields']:
        update_record(
            app_token=app_token,
            table_id=table_id,
            record_id=record['record_id'],
            fields={
                '负责人': format_person_field(assignee_id, assignee_name)
            }
        )
        print(f"✅ 更新记录：{record['fields'].get('标题', 'N/A')}")
    """)


def batch_update_source_mapping(app_token: str, table_id: str):
    """
    批量更新来源平台映射
    
    Args:
        app_token: Bitable App Token
        table_id: Table ID
    """
    print_header(f"🔄 批量更新来源平台")
    
    config = load_config()
    mapping = config.get('bitable_field_mapping', {}).get('source_platform', {})
    
    print("来源平台映射规则：")
    for original, mapped in mapping.items():
        print(f"  {original:15} → {mapped}")
    print()
    
    print("⚠️  此功能需要飞书 API 支持")
    print("建议手动更新或使用飞书多维表格 API")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：")
        print("  python batch_update.py assignee     # 批量添加负责人")
        print("  python batch_update.py source       # 批量更新来源")
        print("  python batch_update.py all          # 全部更新")
        sys.exit(1)
    
    config = load_config()
    app_token = config.get('bitable', {}).get('app_token')
    table_id = config.get('bitable', {}).get('table_id')
    assignee_id = config.get('auto_assign', {}).get('default_assignee', '')
    
    if not app_token or not table_id:
        print("❌ 配置不完整，请先配置 config.json")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "assignee":
        batch_update_assignee(app_token, table_id, assignee_id)
    
    elif command == "source":
        batch_update_source_mapping(app_token, table_id)
    
    elif command == "all":
        batch_update_assignee(app_token, table_id, assignee_id)
        print()
        batch_update_source_mapping(app_token, table_id)
    
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
