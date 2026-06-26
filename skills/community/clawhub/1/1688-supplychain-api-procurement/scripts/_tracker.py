#!/usr/bin/env python3
"""
Skill 埋点上报

职责：每次 CLI 命令执行时，向 skill 网关上报一次调用记录，用于统计 skill 调用次数。
上报失败不影响主流程，静默处理。
"""

import logging
import os

from settings import settings

logger = logging.getLogger("procurement_tracker")

# 发布渠道（可通过环境变量覆盖）
_CHANNEL = os.environ.get("SKILL_CHANNEL", "clawhub")


def report_skill_usage() -> None:
    """
    上报 skill 调用次数到网关。

    调用时机：每次 CLI 命令执行时调用一次（在 cli.py 的 main() 中触发）。
    失败时静默处理，不抛出异常，不影响主流程。
    """
    try:
        from _http import api_post

        api_post(
            "/api/reportSkillsUsage/1.0.0",
            {
                "apiName": None,
                "skillsName": settings.SKILL_NAME,
                "version": settings.SKILL_VERSION,
                "scene": "CLI",
                "channel": _CHANNEL,
            },
            retry=False,
        )
    except Exception as exc:
        logger.debug("埋点上报失败（已忽略）: %s", exc)
