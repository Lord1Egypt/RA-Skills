

#### ✅ `skills/chat-ai/main.py`（OpenClaw 入口）
# -*- coding: utf-8 -*-
"""
OpenClaw Skill 入口：chat-ai
调用你原有项目的 AIChatOrchestrator 核心逻辑
"""
import os
import sys
from typing import Dict, Optional, Any

# 动态添加项目路径（关键！）
PROJECT_ROOT = r"D:\javaworkspace\Winner-Ai"
sys.path.insert(0, PROJECT_ROOT)

from app.services.ai_chat_orchestrator import AIChatOrchestrator
from app.schemas.text2sql import ResponseMessage
from app.agents.base import StreamResponseCollector
from app.core.redis_client import get_redis_client
from app.core.json_encoder import clean_message_data
import json
import uuid
import datetime

# 模拟一个轻量级 collector（无需 Redis/SSE）
class OpenClawCollector(StreamResponseCollector):
    def __init__(self):
        super().__init__()
        self.messages = []
        self.final_result = None

    async def message_callback(self, ctx, message, message_ctx):
        msg_dict = message.model_dump() if hasattr(message, "model_dump") else message.dict()
        msg_dict["timestamp"] = datetime.datetime.now().isoformat()
        self.messages.append(msg_dict)
        if msg_dict.get("is_final") and msg_dict.get("result"):
            self.final_result = msg_dict["result"]

    def set_callback(self, cb):
        # 重写为同步调用
        self.message_callback = cb

def run(query: str, db_config: str = "default", memory_id: str = None) -> Dict[str, Any]:
    """
    OpenClaw 调用入口函数
    """
    try:
        session_id = str(uuid.uuid4())
        memory_id = memory_id or session_id

        # 初始化 collector
        collector = OpenClawCollector()

        # 模拟用户输入回调（OpenClaw 会通过 message/poll 获取反馈）
        async def user_input_callback(prompt: str, ct=None):
            # 此处不阻塞，返回默认值；实际反馈由 OpenClaw 主动注入
            return "同意"  # 或留空，由外部控制

        # 创建编排器（注意：此处需根据你的 db_type 调整）
        orchestrator = AIChatOrchestrator(db_type="starrocks")  # ← 请按需修改

        # 模拟 check_cancelled（OpenClaw 无中止需求时可忽略）
        def check_cancelled():
            return False

        # 执行查询（同步包装）
        runtime = orchestrator.process_query(
            query=query,
            session_id=session_id,
            memory_id=memory_id,
            collector=collector,
            connection_id=None,
            check_cancelled=check_cancelled,
            user_id="openclaw",
            user_name="OpenClaw",
            user_feedback_enabled=False,
            enable_feishu_notification=False,
            db=None,  # 若需 DB，可传入 sqlalchemy engine
        )

        # 提取结果
        result = {
            "status": "success",
            "sql": "",
            "result": [],
            "summary": "",
            "regions": [],
            "raw_messages": [clean_message_data(m) for m in collector.messages]
        }

        # 从 messages 中提取关键字段
        for msg in collector.messages:
            if msg.get("source") == "sql_generator" and msg.get("content"):
                result["sql"] = msg["content"]
            if msg.get("region") == "chat" and msg.get("content"):
                result["summary"] = msg["content"]
            if msg.get("region") not in result["regions"]:
                result["regions"].append(msg.get("region"))

        if collector.final_result:
            result["result"] = collector.final_result

        return result

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "traceback": str(e.__class__.__name__)
        }