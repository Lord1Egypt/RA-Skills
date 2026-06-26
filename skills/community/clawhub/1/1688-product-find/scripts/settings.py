# -*- coding: utf-8 -*-
"""
Skill 业务参数配置

仅存放 service 层需要的业务参数。
系统常量（版本、路径、AK 名称）在 _const.py 中定义。
"""

from _const import SKILL_VERSION  # noqa: F401 — re-export 供 main.py 使用


class Settings:
    """Skill 配置类"""

    # ========== 基础配置 ==========
    SKILL_NAME = "1688-product-find"
    SKILL_VERSION = SKILL_VERSION
    DEFAULT_PLATFORM = "1688"
    DEFAULT_LIMIT = 10
    MAX_LIMIT = 20

    # ========== 图片搜索配置 ==========
    IMAGE_MAX_SIZE_MB = 5  # 上传图片最大体积
    IMAGE_STANDARD_SIZE = (800, 800)  # 标准尺寸


# 全局配置实例
settings = Settings()
