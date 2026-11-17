# -*- coding: utf-8 -*-
"""
Skill 配置模块（含路径常量）

注意：不要在模块级强制校验外部依赖（API 密钥、文件权限等）
改为惰性校验，仅在真实调用前触发，避免 import 即崩溃

环境变量覆盖：
  ORDER_INQUIRY_TOOL_TIMEOUT  - alibaba.1688.newton.order.batch.inquiry 超时（默认 100s）
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

    # alibaba.1688.newton.order.batch.inquiry 接口
    TOOL_PATH = "/api/alibaba.1688.newton.order.batch.inquiry/1.0.0"

    # 询盘结果查询接口
    INQUIRY_QUERY_PATH = "/api/alibaba.1688.ai.inquiry.query/1.0.0"

    # 图片批量上传接口
    IMG_UPLOAD_PATH = "/api/alibaba.1688.zongheng.batch.img.upload/1.0.0"
    IMG_UPLOAD_TIMEOUT = 30

    # 询盘对话配置接口（cbu_a2a 网关，按 serviceName 路由）
    A2A_GATEWAY_PATH = "/api/alibaba.1688.a2a.gateway/1.0.0"

    @property
    def TOOL_TIMEOUT(self):
        val = os.environ.get("ORDER_INQUIRY_TOOL_TIMEOUT")
        return int(val) if val else 100


settings = Settings()
