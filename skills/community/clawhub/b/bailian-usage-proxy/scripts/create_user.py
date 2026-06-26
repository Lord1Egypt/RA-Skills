#!/usr/bin/env python3
"""
创建用户脚本
"""

import asyncio
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import db
from app.models import User
import uuid


async def create_user(name: str, department: str = None, daily_limit: int = 1000000, monthly_limit: int = 10000000):
    """创建用户"""
    await db.init()
    
    user_id = f"user_{uuid.uuid4().hex[:16]}"
    api_key = f"bl-{uuid.uuid4().hex}"
    
    user = User(
        id=user_id,
        name=name,
        department=department,
        api_key=api_key,
        daily_limit=daily_limit,
        monthly_limit=monthly_limit
    )
    
    await db.create_user(user)
    
    print(f"用户创建成功！")
    print(f"  用户ID: {user_id}")
    print(f"  名称: {name}")
    print(f"  部门: {department or '未设置'}")
    print(f"  API Key: {api_key}")
    print(f"  日限额: {daily_limit} tokens")
    print(f"  月限额: {monthly_limit} tokens")
    print()
    print("使用方式:")
    print(f'  base_url = "http://your-proxy-server:8080/v1"')
    print(f'  api_key = "{api_key}"')


def main():
    parser = argparse.ArgumentParser(description="创建阿里百炼代理用户")
    parser.add_argument("--name", required=True, help="用户名称")
    parser.add_argument("--department", help="部门")
    parser.add_argument("--daily-limit", type=int, default=1000000, help="日限额(tokens)")
    parser.add_argument("--monthly-limit", type=int, default=10000000, help="月限额(tokens)")
    
    args = parser.parse_args()
    
    asyncio.run(create_user(
        name=args.name,
        department=args.department,
        daily_limit=args.daily_limit,
        monthly_limit=args.monthly_limit
    ))


if __name__ == "__main__":
    main()
