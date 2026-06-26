"""
主程序入口
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from .config import get_settings
from .database import db
from .api import app as api_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化
    print("正在初始化数据库...")
    await db.init()
    print("数据库初始化完成")
    
    yield
    
    # 关闭时清理
    print("正在关闭连接...")
    if db.engine:
        await db.engine.dispose()


# 创建主应用
app = FastAPI(
    title="阿里百炼用量统计代理",
    description="多人共享账号场景下的精细化用量统计方案",
    version="1.0.0",
    lifespan=lifespan
)

# 挂载API路由
app.mount("/", api_app)


def main():
    """主函数"""
    settings = get_settings()
    
    uvicorn.run(
        "app.main:app",
        host=settings.proxy_host,
        port=settings.proxy_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()
