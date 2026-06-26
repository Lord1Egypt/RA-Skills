"""飞书超级工具包 - 主入口

集成文件发送、日历、审批、多维表格、通讯录、考勤六大模块
"""

from __future__ import annotations

import sys
from pathlib import Path

# 确保 UTF-8 编码
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from feishu_supertoolkit import messaging_api
from feishu_supertoolkit import calendar_api
from feishu_supertoolkit import approval_api
from feishu_supertoolkit import bitable_api
from feishu_supertoolkit import contacts_api
from feishu_supertoolkit import attendance_api

app = FastAPI(
    title="Feishu SuperToolkit",
    description="飞书超级工具包 - 文件发送 + 办公自动化",
    version="1.0.0",
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(messaging_api.router, prefix="/messaging", tags=["消息发送"])
app.include_router(calendar_api.router, prefix="/calendar", tags=["日历"])
app.include_router(approval_api.router, prefix="/approval", tags=["审批"])
app.include_router(bitable_api.router, prefix="/bitable", tags=["多维表格"])
app.include_router(contacts_api.router, prefix="/contacts", tags=["通讯录"])
app.include_router(attendance_api.router, prefix="/attendance", tags=["考勤"])


@app.get("/ping")
def ping() -> dict:
    """健康检查"""
    return {"message": "pong"}


@app.get("/")
def root() -> dict:
    """根路径"""
    return {
        "service": "Feishu SuperToolkit",
        "version": "1.0.0",
        "modules": [
            "messaging",
            "calendar",
            "approval",
            "bitable",
            "contacts",
            "attendance",
        ],
    }
