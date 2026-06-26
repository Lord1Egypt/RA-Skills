#!/usr/bin/env python3
"""
创建新客户

用法:
    python create_customer.py <name> <phone> [options]

示例:
    python create_customer.py "李雷" "13800001111" --email "lilei@example.com" --wechat_id "leilei123" --gender "男" --age 35
    python create_customer.py "王芳" "13900002222" --wechat_id "wangfang99"
"""

import os
import sys
import yaml
import argparse
import re
from datetime import datetime


def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def create_customer(name, phone, email=None, wechat_id=None, gender=None, age=None, level=None, source=None, tags=None):
    """
    创建新客户 YAML 文件
    
    Args:
        name: 客户姓名（主键）
        phone: 电话号码
        email: 邮箱地址（可选）
        wechat_id: 微信ID（可选）
        gender: 性别（可选）
        age: 年龄（可选）
        level: 等级（可选）
        source: 来源（可选）
        tags: 标签列表（可选）
    
    Returns:
        dict: 操作结果
    """
    # 验证邮箱格式（仅当提供时）
    if email and not validate_email(email):
        return {
            "success": False,
            "message": "邮箱格式无效，请提供有效的邮箱地址"
        }
    # 数据目录
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    os.makedirs(data_dir, exist_ok=True)
    
    # 检查客户是否已存在
    file_path = os.path.join(data_dir, f"{name}.yaml")
    if os.path.exists(file_path):
        return {
            "success": False,
            "message": f"客户 {name} 已存在，请使用更新功能"
        }
    
    # 构建客户记录
    record = {
        "name": name,
        "phone": phone,
        "email": email if email else "",
        "wechat_id": wechat_id if wechat_id else "",
        "gender": gender or "未知",
        "age": age,
        "level": level or "普通",
        "source": source or "",
        "tags": tags if tags else [],
        "status": "新增",
        "last_contact": None,
        "notes": [],
        "service_records": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 保存 YAML 文件
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(record, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    return {
        "success": True,
        "message": f"客户 {name} 已成功创建",
        "data": record
    }


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="创建新客户")
    parser.add_argument("name", help="客户姓名")
    parser.add_argument("phone", help="电话号码")
    parser.add_argument("--email", help="邮箱地址（可选）")
    parser.add_argument("--wechat_id", help="微信ID（可选）")
    parser.add_argument("--gender", help="性别")
    parser.add_argument("--age", type=int, help="年龄")
    parser.add_argument("--level", help="等级（普通/会员/VIP）")
    parser.add_argument("--source", help="来源")
    parser.add_argument("--tags", nargs="+", help="标签列表")
    
    args = parser.parse_args()
    
    result = create_customer(
        name=args.name,
        phone=args.phone,
        email=args.email,
        wechat_id=args.wechat_id,
        gender=args.gender,
        age=args.age,
        level=args.level,
        source=args.source,
        tags=args.tags
    )
    
    print(result["message"])
    if result["success"]:
        print(f"文件位置: data/customers/{args.name}.yaml")
    
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
