#!/usr/bin/env python3
"""
添加跟进记录

用法:
    python add_note.py <name> <note> [--status STATUS]

示例:
    python add_note.py "李雷" "客户说考虑一下" --status "跟进中"
"""

import os
import sys
import yaml
import argparse
from datetime import datetime


def add_note(name, note, status=None):
    """
    为客户添加跟进记录
    
    Args:
        name: 客户姓名
        note: 跟进内容
        status: 可选的状态更新
    
    Returns:
        dict: 操作结果
    """
    # 数据目录
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    file_path = os.path.join(data_dir, f"{name}.yaml")
    
    # 检查客户是否存在
    if not os.path.exists(file_path):
        return {
            "success": False,
            "message": f"客户 {name} 不存在"
        }
    
    # 读取现有记录
    with open(file_path, "r", encoding="utf-8") as f:
        record = yaml.safe_load(f)
    
    # 添加跟进记录
    today = datetime.now().strftime("%Y-%m-%d")
    note_entry = f"{today}: {note}"
    
    if "notes" not in record or record["notes"] is None:
        record["notes"] = []
    
    record["notes"].append(note_entry)
    
    # 更新最后联系时间和状态
    record["last_contact"] = today
    if status:
        record["status"] = status
    
    record["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 保存文件
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(record, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return {
        "success": True,
        "message": f"已为 {name} 添加跟进记录",
        "data": {
            "note": note_entry,
            "total_notes": len(record["notes"])
        }
    }


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="添加跟进记录")
    parser.add_argument("name", help="客户姓名")
    parser.add_argument("note", help="跟进内容")
    parser.add_argument("--status", help="更新状态")
    
    args = parser.parse_args()
    
    result = add_note(
        name=args.name,
        note=args.note,
        status=args.status
    )
    
    print(result["message"])
    if result["success"]:
        print(f"当前共有 {result['data']['total_notes']} 条跟进记录")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())