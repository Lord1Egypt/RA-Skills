#!/usr/bin/env python3
"""
数据库初始化脚本
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import db


async def init_database():
    """初始化数据库"""
    print("正在初始化数据库...")
    await db.init()
    print("数据库初始化完成！")
    print(f"数据库URL: {db.settings.database_url}")


if __name__ == "__main__":
    asyncio.run(init_database())
