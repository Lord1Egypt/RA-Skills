#!/usr/bin/env python3
"""
Skill 埋点上报

职责：每次已识别 CLI 命令被分派时，向 skill 网关尽力上报一次调用记录，用于统计
CLI 命令分派尝试。CLI 级重试和批量商品处理会放大该指标，不能直接解释为用户漏斗转化。
网络超时或重试等传输不确定性还可能造成少记或重复，因此该指标仅适合观察调用分布。
上报失败不影响主流程，静默处理。

环境变量（从项目根目录 .env 读取）：
    SKILL_NAME     skill 名称，默认 1688-product-analysis
    SKILL_VERSION  skill 版本，默认 1.0.0
    SKILL_CHANNEL  发布渠道，默认 clawhubai
"""

import logging
import os
from pathlib import Path

logger = logging.getLogger("1688_product_analysis_tracker")

# 项目根目录（scripts/ 的上一级）
_ROOT_DIR = Path(__file__).parent.parent

def _load_env_file() -> None:
    """解析项目根目录的 .env 文件，将变量注入 os.environ（已有环境变量不覆盖）。"""
    env_path = _ROOT_DIR / ".env"
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # 已存在的环境变量（如 CI 注入）优先，不覆盖
            if key and key not in os.environ:
                os.environ[key] = value

# 模块加载时解析一次 .env
_load_env_file()

def _get_skill_env():
    """读取 skill 基础信息，返回 (skill_name, skill_version, channel)。"""
    skill_name = os.environ.get("SKILL_NAME", "1688-product-analysis")
    skill_version = os.environ.get("SKILL_VERSION", "1.0.0")
    channel = os.environ.get("SKILL_CHANNEL", "clawhubai")
    return skill_name, skill_version, channel

def report_skill_usage(api_name=None, scene="CLI") -> None:
    """
    上报一次 CLI 命令分派尝试到网关。

    CLI 级重试和批量商品处理会放大该指标，不能直接解释为用户漏斗转化；
    网络超时或重试等传输不确定性可能造成少记或重复。

    调用时机：已识别命令被分派后调用一次，即使业务命令异常退出也会尝试上报。
    失败时静默处理，不抛出异常，不影响主流程。
    """
    try:
        from _http import api_post
        skill_name, skill_version, channel = _get_skill_env()
        api_post(
            "/api/alibaba.1688.report.skills.usage/1.0.0",
            {
                "apiName": api_name,
                "skillsName": skill_name,
                "version": skill_version,
                "scene": scene,
                "channel": channel,
            },
        )
    except Exception as exc:
        logger.debug("埋点上报失败（已忽略）: %s", exc)
