# -*- coding: utf-8 -*-
"""
Skill 配置模块（含路径常量）

注意：不要在模块级强制校验外部依赖（API 密钥、文件权限等）
改为惰性校验，仅在真实调用前触发，避免 import 即崩溃

环境变量覆盖：
  COWBOY_API_TIMEOUT  - 通用接口超时（默认 30s）
"""

import os
from pathlib import Path

# ── 路径常量 ──────────────────────────────────────────────

# 技能根目录（scripts/ 的上一级）
SKILL_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 输出目录
OUTPUT_DIR = SKILL_DIR / "output"

# OpenClaw 配置文件路径（AK fallback）
OPENCLAW_CONFIG_PATH: Path = (
    Path(os.environ.get("OPENCLAW_CONFIG_DIR", str(Path.home() / ".openclaw")))
    / "openclaw.json"
)


class Settings:
    """Skill 配置类"""

    SKILL_NAME = "niuzai-receptionist"
    SKILL_VERSION = "1.0.0"
    SKILL_CHANNEL = "clawhub"

    # ── TPP 接口路径 ──────────────────────────────────────
    DAILY_REPORT_PATH = "api/cowboy_daily_report/1.0.0"
    KNOWLEDGE_QUERY_PATH = "api/cowboy_knowledge_query/1.0.0"
    KNOWLEDGE_ANSWER_PATH = "api/cowboy_knowledge_answer/1.0.0"
    CREATE_COWBOY_PATH = "api/create_cow_boy/1.0.0"
    UPDATE_COWBOY_PATH = "api/update_cow_boy/1.0.0"
    PAUSE_COWBOY_PATH = "api/pause_cow_boy/1.0.0"
    RESUME_COWBOY_PATH = "api/resume_cow_boy/1.0.0"
    LOAD_COWBOY_PATH = "api/cowboy_load_config/1.0.0"
    TEST_CHAT_PATH = "api/cowboy_test_chat/1.0.0"
    QUERY_INQUIRY_PATH = "api/query_transfer_inquiries/1.0.0"

    @property
    def API_TIMEOUT(self):
        val = os.environ.get("COWBOY_API_TIMEOUT")
        return int(val) if val else 30


settings = Settings()
