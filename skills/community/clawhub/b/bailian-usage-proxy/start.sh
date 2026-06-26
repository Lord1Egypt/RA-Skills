#!/bin/bash
# 纯 Python 启动脚本（无需 Docker）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -q fastapi uvicorn httpx sqlalchemy aiosqlite pydantic python-dotenv jinja2 python-multipart

# 创建数据目录
mkdir -p data logs

# 初始化数据库
echo "初始化数据库..."
python3 scripts/init_db.py

# 创建默认用户（如果不存在）
echo "检查默认用户..."
python3 << 'EOF'
import sys
sys.path.insert(0, '.')
import asyncio
from app.database import db
from app.models import User
import uuid

async def init():
    await db.init()
    users = await db.list_users()
    if not users:
        print("创建默认管理员用户...")
        user = User(
            id=f"admin_{uuid.uuid4().hex[:8]}",
            name="管理员",
            department="IT",
            api_key=f"bl-admin-{uuid.uuid4().hex}",
            daily_limit=10000000,
            monthly_limit=100000000
        )
        await db.create_user(user)
        print(f"管理员 API Key: {user.api_key}")
    else:
        print(f"已有 {len(users)} 个用户")

asyncio.run(init())
EOF

echo ""
echo "========================================"
echo "启动阿里百炼用量统计代理服务"
echo "========================================"
echo ""
echo "API 地址: http://localhost:8080"
echo "管理后台: http://localhost:8081"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 启动服务
python3 -m app.main
