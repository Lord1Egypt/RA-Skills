# -*- coding: utf-8 -*-
"""
Skill 配置模块

注意：不要在模块级强制校验外部依赖（//api 密钥、文件权限等）
改为惰性校验，仅在真实调用前触发，避免 import 即崩溃

环境变量覆盖：
  PROCUREMENT_TOOL_TIMEOUT    - DigitalHumanMainAgent 超时（默认 100s）
  PROCUREMENT_IMG_UPLOAD_TIMEOUT - 图片上传接口超时（默认 3000s）
"""

import os
from pathlib import Path

# OpenClaw 配置文件路径（AK fallback）
OPENCLAW_CONFIG_PATH: Path = (
    Path(os.environ.get("OPENCLAW_CONFIG_DIR", str(Path.home() / ".openclaw")))
    / "openclaw.json"
)


class Settings:
    """Skill 配置类"""

    SKILL_NAME = "1688-supplychain-api-procurement"
    SKILL_VERSION = "0.0.1"

    # DigitalHumanMainAgent tool 接口
    TOOL_PATH = "/api/DigitalHumanMainAgent/1.0.0"

    # 创建任务接口（ImChatGatewayHsfService）
    CREATE_TASK_PATH = "/api/ImChatGatewayHsfServiceV2/1.0.0"
    CREATE_TASK_METHOD = "aiDigitalHumanPurchaseCreateNewtonTaskServiceV2"
    CREATE_TASK_TIMEOUT = 15

    # 图片批量上传接口（zongheng_batch_img_upload）
    IMG_UPLOAD_PATH = "/api/zongheng_batch_img_upload/1.0.0"

    # 询盘数据查询接口（DigitalHumanInstanceData）
    INSTANCE_DATA_PATH = "/api/DigitalHumanInstanceData/1.0.0"

    @property
    def TOOL_TIMEOUT(self):
        val = os.environ.get("PROCUREMENT_TOOL_TIMEOUT")
        return int(val) if val else 100

    @property
    def IMG_UPLOAD_TIMEOUT(self):
        val = os.environ.get("PROCUREMENT_IMG_UPLOAD_TIMEOUT")
        return int(val) if val else 3000


settings = Settings()
