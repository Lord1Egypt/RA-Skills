#!/usr/bin/env python3
"""
NLP服务记录 - 自然语言添加服务记录

用法:
    python nlp_service_record.py "今天给张三上了一节健身课，深蹲进步了10kg，60分钟"
    python nlp_service_record.py "王芳买了10次心理咨询课，3000块钱" --auto-tag
    python nlp_service_record.py "李四昨天体验课，进步很大" --confirm

功能:
1. 自然语言解析
2. 自动提取服务信息
3. 预览确认（可选--confirm）
4. 自动添加服务记录
5. 自动更新客户标签（可选--auto-tag）
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nlp_parser import parse_service_record, format_parsed_result
from add_service_record import add_service_record
from auto_tagger import add_auto_tags


def add_service_record_by_nlp(text, confirm=False, auto_tag=False):
    """
    通过自然语言添加服务记录
    
    Args:
        text: 自然语言描述
        confirm: 是否先预览确认再添加
        auto_tag: 是否自动更新客户标签
    
    Returns:
        dict: 操作结果
    """
    # 1. 解析自然语言
    parsed = parse_service_record(text)
    
    if not parsed["parsed"]:
        return {
            "success": False,
            "message": f"解析失败: {parsed.get('error', '未知错误')}"
        }
    
    # 2. 预览模式
    if confirm:
        print("=" * 60)
        print("服务记录预览")
        print("=" * 60)
        print(format_parsed_result(parsed))
        print("=" * 60)
        
        response = input("\n确认添加此服务记录？(y/n): ").strip().lower()
        if response != 'y':
            return {
                "success": False,
                "message": "已取消添加"
            }
    
    # 3. 添加服务记录
    result = add_service_record(
        name=parsed["customer"],
        type=parsed["type"],
        description=parsed["description"],
        attendance=parsed.get("attendance"),
        duration=parsed.get("duration"),
        progress=parsed.get("progress"),
        amount=parsed.get("amount"),
        outcome=parsed["outcome"],
        date=parsed["date"]
    )
    
    if not result["success"]:
        return result
    
    # 4. 自动标签（如果启用）
    tag_result = None
    if auto_tag:
        tag_result = add_auto_tags(parsed["customer"], dry_run=False)
    
    # 5. 构建完整结果
    final_result = {
        "success": True,
        "message": result["message"],
        "customer": parsed["customer"],
        "service_record": result["data"]["record"],
        "total_records": result["data"]["total_records"],
        "parsed_data": parsed
    }
    
    if tag_result and tag_result["success"]:
        final_result["auto_tags"] = tag_result.get("added_tags", [])
    
    return final_result


def main():
    # 修复 Windows 控制台输出编码问题
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    import argparse
    
    parser = argparse.ArgumentParser(description="自然语言添加服务记录")
    parser.add_argument("text", help="自然语言描述，如'今天给张三上了一节健身课'")
    parser.add_argument("--confirm", "-c", action="store_true", help="预览确认后再添加")
    parser.add_argument("--auto-tag", "-t", action="store_true", help="自动更新客户标签")
    
    args = parser.parse_args()
    
    result = add_service_record_by_nlp(
        text=args.text,
        confirm=args.confirm,
        auto_tag=args.auto_tag
    )
    
    print(result["message"])
    
    if result["success"]:
        print(f"\n客户: {result['customer']}")
        print(f"服务记录ID: {result['service_record']['id']}")
        print(f"当前共有: {result['total_records']} 条服务记录")
        
        if result.get("auto_tags"):
            print(f"\n自动添加标签: {', '.join(result['auto_tags'])}")
        
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
