# -*- coding: utf-8 -*-
"""
Skill 配置模块（含路径常量）

注意：不要在模块级强制校验外部依赖（API 密钥、文件权限等）
改为惰性校验，仅在真实调用前触发，避免 import 即崩溃

环境变量覆盖：
  ORDER_INQUIRY_TOOL_TIMEOUT  - NewtonOrderBatchInquiry 超时（默认 100s）
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

    SKILL_NAME = "1688-supplychain-order-inquiry"
    SKILL_VERSION = "0.1.0"

    # NewtonOrderBatchInquiry 接口
    TOOL_PATH = "/api/NewtonOrderBatchInquiry/1.0.0"

    # 图片批量上传接口
    IMG_UPLOAD_PATH = "/api/zongheng_batch_img_upload/1.0.0"
    IMG_UPLOAD_TIMEOUT = 30

    @property
    def TOOL_TIMEOUT(self):
        val = os.environ.get("ORDER_INQUIRY_TOOL_TIMEOUT")
        return int(val) if val else 100


settings = Settings()
