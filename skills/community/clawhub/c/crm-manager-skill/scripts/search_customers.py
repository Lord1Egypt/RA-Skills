#!/usr/bin/env python3
"""
搜索客户

用法:
    python search_customers.py [--tags TAGS] [--status STATUS] [--level LEVEL] [--age-min AGE] [--age-max AGE]

示例:
    python search_customers.py --tags "高端产品"
    python search_customers.py --status "跟进中"
    python search_customers.py --level "VIP"
    python search_customers.py --age-min 30 --age-max 40
"""

import os
import sys
import yaml
import argparse


def load_all_customers():
    """加载所有客户数据"""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers')
    
    if not os.path.exists(data_dir):
        return []
    
    customers = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.yaml'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                record = yaml.safe_load(f)
                if record:
                    customers.append(record)
    
    return customers


def search_customers(tags=None, status=None, level=None, age_min=None, age_max=None, email=None):
    """
    搜索符合条件的客户
    
    Args:
        tags: 标签列表
        status: 状态
        level: 等级
        age_min: 最小年龄
        age_max: 最大年龄
        email: 邮箱搜索关键词
    
    Returns:
        list: 符合条件的客户列表
    """
    customers = load_all_customers()
    results = []
    
    for customer in customers:
        match = True
        
        # 标签过滤
        if tags:
            customer_tags = customer.get('tags', []) or []
            if not any(tag in customer_tags for tag in tags):
                match = False
        
        # 状态过滤
        if status and match:
            if customer.get('status') != status:
                match = False
        
        # 等级过滤
        if level and match:
            if customer.get('level') != level:
                match = False
        
        # 年龄范围过滤
        if match:
            age = customer.get('age')
            if age is not None:
                if age_min is not None and age < age_min:
                    match = False
                if age_max is not None and age > age_max:
                    match = False
            elif age_min is not None or age_max is not None:
                # 如果设置了年龄过滤但没有年龄数据，则不匹配
                match = False
        
        # 邮箱过滤
        if email and match:
            customer_email = customer.get('email', '') or ''
            if email not in customer_email:
                match = False
        
        if match:
            results.append(customer)
    
    return results


def main():
    # 修复 Windows 控制台输出编码问题
    import sys
    import io
    if sys.platform == 'win32' and sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="搜索客户")
    parser.add_argument("--tags", nargs="+", help="标签列表")
    parser.add_argument("--status", help="状态")
    parser.add_argument("--level", help="等级")
    parser.add_argument("--age-min", type=int, help="最小年龄")
    parser.add_argument("--age-max", type=int, help="最大年龄")
    parser.add_argument("--email", help="邮箱关键词")
    
    args = parser.parse_args()
    
    # 检查是否有搜索条件
    if not any([args.tags, args.status, args.level, args.age_min is not None, args.age_max is not None, args.email]):
        print("错误: 请至少提供一个搜索条件")
        parser.print_help()
        return 1
    
    results = search_customers(
        tags=args.tags,
        status=args.status,
        level=args.level,
        age_min=args.age_min,
        age_max=args.age_max,
        email=args.email
    )
    
    if not results:
        print("未找到符合条件的客户")
        return 0
    
    print(f"找到 {len(results)} 个客户:\n")
    
    for i, customer in enumerate(results, 1):
        print(f"{i}. {customer.get('name', 'N/A')}")
        print(f"   电话: {customer.get('phone', 'N/A')}")
        print(f"   等级: {customer.get('level', '普通')} | 状态: {customer.get('status', '新增')}")
        
        tags = customer.get('tags', [])
        if tags:
            print(f"   标签: {', '.join(tags)}")
        
        last_contact = customer.get('last_contact')
        if last_contact:
            print(f"   最后联系: {last_contact}")
        
        print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())