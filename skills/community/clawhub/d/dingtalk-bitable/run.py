#!/usr/bin/env python3
"""
钉钉多维表格技能 - 工具执行入口
"""

import sys
import json
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dingtalk_bitable import (
    bitable_list,
    bitable_get_meta,
    bitable_list_fields,
    bitable_list_records,
    bitable_get_record,
    bitable_create_record,
    bitable_update_record,
    bitable_delete_record,
    bitable_create_field,
    format_field,
    format_record,
)


def parse_args():
    """解析命令行参数"""
    if len(sys.argv) < 2:
        print("用法：python run.py <tool_name> [args...]")
        print("可用工具：bitable_list, bitable_get_meta, bitable_list_fields,")
        print("         bitable_list_records, bitable_get_record, bitable_create_record,")
        print("         bitable_update_record, bitable_delete_record, bitable_create_field")
        sys.exit(1)
    
    tool_name = sys.argv[1]
    args = {}
    
    # 解析 JSON 参数
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            # 尝试解析 JSON
            try:
                args[key] = json.loads(value)
            except json.JSONDecodeError:
                args[key] = value
    
    return tool_name, args


def main():
    tool_name, args = parse_args()
    
    result = None
    
    try:
        if tool_name == "bitable_list":
            space_id = args.get("space_id")
            limit = args.get("limit", 20)
            result = bitable_list(space_id=space_id, limit=limit)
        
        elif tool_name == "bitable_get_meta":
            app_token = args.get("app_token")
            if not app_token:
                raise ValueError("缺少必需参数：app_token")
            result = bitable_get_meta(app_token)
        
        elif tool_name == "bitable_list_fields":
            app_token = args.get("app_token")
            table_id = args.get("table_id")
            if not app_token or not table_id:
                raise ValueError("缺少必需参数：app_token, table_id")
            result = bitable_list_fields(app_token, table_id)
        
        elif tool_name == "bitable_list_records":
            app_token = args.get("app_token")
            table_id = args.get("table_id")
            filter_cond = args.get("filter")
            sort_cond = args.get("sort")
            page_size = args.get("page_size", 100)
            page_token = args.get("page_token")
            if not app_token or not table_id:
                raise ValueError("缺少必需参数：app_token, table_id")
            result = bitable_list_records(
                app_token, table_id,
                filter=filter_cond,
                sort=sort_cond,
                page_size=page_size,
                page_token=page_token
            )
        
        elif tool_name == "bitable_get_record":
            app_token = args.get("app_token")
            table_id = args.get("table_id")
            record_id = args.get("record_id")
            if not app_token or not table_id or not record_id:
                raise ValueError("缺少必需参数：app_token, table_id, record_id")
            result = bitable_get_record(app_token, table_id, record_id)
        
        elif tool_name == "bitable_create_record":
            app_token = args.get("app_token")
            table_id = args.get("table_id")
            fields = args.get("fields")
            if not app_token or not table_id or not fields:
                raise ValueError("缺少必需参数：app_token, table_id, fields")
            record_id = bitable_create_record(app_token, table_id, fields)
            result = {"recordId": record_id, "success": bool(record_id)}
        
        elif tool_name == "bitable_update_record":
            app_token = args.get("app_token")
            table_id = args.get("table_id")
            record_id = args.get("record_id")
            fields = args.get("fields")
            if not app_token or not table_id or not record_id or not fields:
                raise ValueError("缺少必需参数：app_token, table_id, record_id, fields")
            success = bitable_update_record(app_token, table_id, record_id, fields)
            result = {"success": success}
        
        elif tool_name == "bitable_delete_record":
            app_token = args.get("app_token")
            table_id = args.get("table_id")
            record_id = args.get("record_id")
            if not app_token or not table_id or not record_id:
                raise ValueError("缺少必需参数：app_token, table_id, record_id")
            success = bitable_delete_record(app_token, table_id, record_id)
            result = {"success": success}
        
        elif tool_name == "bitable_create_field":
            app_token = args.get("app_token")
            table_id = args.get("table_id")
            field_name = args.get("field_name")
            field_type = args.get("field_type", "Text")
            if not app_token or not table_id or not field_name:
                raise ValueError("缺少必需参数：app_token, table_id, field_name")
            field_id = bitable_create_field(app_token, table_id, field_name, field_type)
            result = {"fieldId": field_id, "success": bool(field_id)}
        
        else:
            print(f"未知工具：{tool_name}")
            sys.exit(1)
        
        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        error_result = {"error": str(e)}
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
