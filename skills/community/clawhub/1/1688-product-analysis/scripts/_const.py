#!/usr/bin/env python3
"""
1688 商品诊断 skill 全局常量
"""

import base64
import json
import os
import re
from pathlib import Path
from typing import Optional

# Skill 版本
SKILL_VERSION = "1.0.0"

# ── OpenClaw 配置文件路径 ─────────────────────────────────────────────────────
# 优先读取 OPENCLAW_CONFIG_DIR 环境变量，默认 ~/.openclaw
OPENCLAW_CONFIG_PATH: Path = Path(
    os.environ.get("OPENCLAW_CONFIG_DIR", Path.home() / ".openclaw")
) / "openclaw.json"

# ── userId 解析 ──────────────────────────────────────────────────────────────

def _get_ak_raw_from_config() -> Optional[str]:
    """从 OpenClaw 配置文件读取 AK（Gateway 未重启时的 fallback）"""
    if not OPENCLAW_CONFIG_PATH.exists():
        return None
    try:
        with open(OPENCLAW_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        entries = config.get("skills", {}).get("entries", {})
        # 兼容多个可能的 skill 注册名
        for skill_name in (
            "1688-product-analysis",
            "1688-key-product-selection",
            "1688-shop-health-check",
            "1688-shop-operate",
            "1688-open-skill-template",
        ):
            skill = entries.get(skill_name)
            if not skill:
                continue
            ak = skill.get("apiKey") or skill.get("env", {}).get("ALI_1688_AK", "")
            if ak:
                return ak
        return None
    except Exception:
        return None

def _decode_ak(raw_input: str) -> Optional[str]:
    """
    解码 AK，返回 access_key_id 部分。

    AK 规则（与 shop-operate _auth.extract_ak_keys 对齐）：
      - 优先尝试 base64 url-safe 解码
      - 解码后前 32 位为 access_key_secret，32 位之后为 access_key_id
    """
    if not raw_input:
        return None
    try:
        decoded = base64.urlsafe_b64decode(raw_input).decode("utf-8")
        if decoded:
            raw_input = decoded
    except Exception:
        # 当前 AK 规范并不保证一定是 base64，可回退到原值按长度切分
        pass

    if len(raw_input) < 32:
        return None
    return raw_input[32:] or None

def _extract_user_id_from_ak_id(ak_id: str) -> Optional[int]:
    """
    从 access_key_id 中提取数字 userId。

    1688 AK 通常包含若干段以 `_` / `-` 等分隔的字段，userId 是其中一段
    纯数字串。这里取最长的连续数字串作为 userId。
    """
    if not ak_id:
        return None
    matches = re.findall(r"\d+", ak_id)
    if not matches:
        return None
    longest = max(matches, key=len)
    try:
        return int(longest)
    except (TypeError, ValueError):
        return None

def get_runtime_user_id() -> int:
    """
    读取运行时卖家 userId（用于 MCP 工具的 __userId__ 入参）。

    解析顺序（前者命中即返回）：
      1. 环境变量 USER_ID / X_USER_ID（显式覆盖，便于本地调试）
      2. 环境变量 ALI_1688_AK 解码后的 access_key_id 中的数字段
      3. OpenClaw 配置文件中的 ALI_1688_AK 解码结果
      4. 0（占位，调用方可据此判断未配置）
    """
    # 1. 显式注入
    raw_uid = os.environ.get("USER_ID") or os.environ.get("X_USER_ID")
    if raw_uid:
        try:
            return int(raw_uid)
        except (TypeError, ValueError):
            pass

    # 2 & 3. 从 AK 解码
    ak_raw = os.environ.get("ALI_1688_AK") or _get_ak_raw_from_config()
    if ak_raw:
        ak_id = _decode_ak(ak_raw)
        uid = _extract_user_id_from_ak_id(ak_id) if ak_id else None
        if uid:
            return uid

    return 0
