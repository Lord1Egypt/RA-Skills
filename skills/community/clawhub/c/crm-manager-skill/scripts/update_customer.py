#!/usr/bin/env python3
"""
更新客户信息

用法:
    python update_customer.py <name> [options]

示例:
    python update_customer.py "李雷" --gender "男" --age 35 --level "VIP"
"""

import os
import sys
import yaml
import argparse
from datetime import datetime


def update_customer(name, **kwargs):
    """
    更新客户信息
    
    Args:
        name: 客户姓名
        **kwargs: 要更新的字段
    
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
    
    # 更新字段
    updated_fields = []
    for key, value in kwargs.items():
        if value is not None and key in record:
            record[key] = value
            updated_fields.append(key)
    
    if not updated_fields:
        return {
            "success": False,
            "message": "没有提供要更新的字段"
        }
    
    # 更新时间戳
    record["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 保存文件
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(record, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return {
        "success": True,
        "message": f"客户 {name} 已更新: {', '.join(updated_fields)}",
        "data": record
    }


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="更新客户信息")
    parser.add_argument("name", help="客户姓名")
    parser.add_argument("--phone", help="电话号码")
    parser.add_argument("--email", help="邮箱地址")
    parser.add_argument("--wechat_id", help="微信ID")
    parser.add_argument("--gender", help="性别")
    parser.add_argument("--age", type=int, help="年龄")
    parser.add_argument("--level", help="等级（普通/会员/VIP）")
    parser.add_argument("--source", help="来源")
    parser.add_argument("--tags", nargs="+", help="标签列表（覆盖）")
    parser.add_argument("--status", help="状态（新增/跟进中/已成交/暂停/流失）")
    
    args = parser.parse_args()
    
    result = update_customer(
        name=args.name,
        phone=args.phone,
        email=args.email,
        wechat_id=args.wechat_id,
        gender=args.gender,
        age=args.age,
        level=args.level,
        source=args.source,
        tags=args.tags,
        status=args.status
    )
    
    print(result["message"])
    if result["success"]:
        print(f"更新时间: {result['data']['updated_at']}")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
