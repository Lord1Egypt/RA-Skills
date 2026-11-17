#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coze_kernel.py — ct- 技能族 Coze 后端**横切内核**（单一真相源，ct-base §20.19.6）。

本模块承载所有 ct- Coze 客户端共享的横切关注点，取代过去每个技能各写一遍
的平行实现（全库曾重复 6-7 份：_query_origin / _skill_version / sanitize /
出站授权门控 / 限流 / _assess_contract）。

分发机制（§20.19.6）：ct-base 持有单一真相源 → publish_inject 注入各技能
adapters/coze_kernel.py → 客户端 import 注入副本（**禁运行时跨技能 import**，
技能是独立发布单元，用户机器未必装 ct-base）。

设计原则：内核函数全部**参数化**——算法保持单一，技能特有部分（env 名 /
品牌串 / config 路径 / SKILL.md 映射 / 响应别名表）通过 CozeKernelConfig 外置。
首个迁移样板见 ct-sdtm/adapters/coze_client.py。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import sys
import threading
import time
from pathlib import Path

__all__ = [
    "CozeKernelConfig",
    "query_origin",
    "sanitize",
    "rate_limit_wait",
    "skill_version",
    "check_outbound_authorization",
    "assess_contract",
]


class CozeKernelConfig:
    """技能特有配置（算法共用、差异外置）。

    各消费技能构造一个实例传入内核函数。默认值对齐 ct-sdtm（首个迁移样板）。
    """

    def __init__(
        self,
        brand: str = "coze",
        config_rel: str = "ct-sdtm/config/config.json",
        min_interval_env: str = "CT_COZE_MIN_INTERVAL",
        skill_md: dict = None,
        version_fallback: str = "0.0.0",
        response_aliases: dict = None,
    ):
        self.brand = brand
        self.config_rel = config_rel
        self.min_interval_env = min_interval_env
        self.skill_md = dict(skill_md) if skill_md else {}
        self.version_fallback = version_fallback
        self.response_aliases = dict(response_aliases) if response_aliases else {}

    def config_path(self) -> str:
        base = Path.home() / ".workbuddy" / "skills"
        if self.config_rel:
            return str(base / self.config_rel)
        return str(base / "ct-sdtm" / "config" / "config.json")


# ---------------------------------------------------------------------------
# R5（ct-base §23.2）：相邻两次 /run POST 间隔 >=1s；connect 快速失败 15s /
# read 允许长计算 600s。锁 + monotonic 时钟，env 名可覆写（<=0 仅调试）。
# ---------------------------------------------------------------------------
_MIN_INTERVAL_LOCK = threading.Lock()
_LAST_POST_MONO = [0.0]


def rate_limit_wait(cfg: CozeKernelConfig) -> None:
    """R5：相邻 POST 间隔不低于 cfg.min_interval_env（默认 1.0s）。"""
    try:
        interval = float(os.environ.get(cfg.min_interval_env, "1.0"))
    except ValueError:
        interval = 1.0
    if interval <= 0:
        return
    with _MIN_INTERVAL_LOCK:
        now = time.monotonic()
        wait = _LAST_POST_MONO[0] + interval - now
        if wait > 0:
            time.sleep(wait)
        _LAST_POST_MONO[0] = time.monotonic()


def query_origin() -> str:
    """R6：sha256:<64hex>，由客户端按 hostname 生成；禁 nonce 化（缓存键审计，§8.6）。"""
    host = socket.gethostname() or "unknown-host"
    return "sha256:" + hashlib.sha256(host.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# payload 脱敏（ct-base：发送前剥 PII；日志绝不回显明文）
# ---------------------------------------------------------------------------
_PII_PATTERNS = [
    (re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"), "<ID>"),
    (re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"), "<PHONE>"),
    (re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+(?![A-Za-z0-9])"), "<EMAIL>"),
]


def sanitize(obj):
    """递归剥离 PII（身份证/手机号/邮箱），返回脱敏副本（不改原对象）。"""
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize(v) for v in obj]
    if isinstance(obj, str):
        for pat, repl in _PII_PATTERNS:
            obj = pat.sub(repl, obj)
        return obj
    return obj


def skill_version(skill: str, cfg: CozeKernelConfig) -> str:
    """读对应技能 SKILL.md 的 version: 字段；失败回退 cfg.version_fallback。"""
    p = Path(cfg.skill_md.get(skill, next(iter(cfg.skill_md.values())) if cfg.skill_md else ""))
    if not str(p):
        return cfg.version_fallback
    try:
        m = re.search(r"^version:\s*(\S+)", p.read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1)
    except OSError:
        pass
    return cfg.version_fallback


# ---------------------------------------------------------------------------
# 出站授权（ct-base §5 · 精简自包含实现）。
# session_authorized：调用方持有的会话内存授权集合（agent 引导用户确认后加入）。
# ---------------------------------------------------------------------------
def check_outbound_authorization(
    endpoint: str,
    cfg: CozeKernelConfig,
    session_authorized: set = None,
) -> bool:
    """返回 True 放行；False 拦截（不发送）。白名单写入须由用户确认触发。"""
    if session_authorized is not None and endpoint in session_authorized:
        return True
    try:
        with open(cfg.config_path(), "r", encoding="utf-8") as f:
            eps = json.load(f).get("auto_approve_endpoints", [])
        if endpoint in [e for e in eps if isinstance(e, str)]:
            return True
    except (OSError, ValueError):
        pass
    sys.stderr.write(
        "[%s][AUTH-BLOCK] outbound to %s requires user confirmation.\n"
        "[%s] Only trial-design parameters (no personal data) are sent; "
        "declining disables cloud computation (caller must prompt to connect Coze).\n"
        % (cfg.brand, endpoint, cfg.brand)
    )
    return False


# ---------------------------------------------------------------------------
# 契约漂移自愈（ct-base §20.9 单入口；仅结构/数据内容漂移触发，版本差异不告警）。
# 别名表按技能不同（cfg.response_aliases 外置）。
# ---------------------------------------------------------------------------
def assess_contract(parsed: dict, cfg: CozeKernelConfig):
    """结构漂移自愈：识别已知字段别名并归一化。

    Returns: (parsed, drift_notes)。drift_notes 非空表示发生归一化，
    交由调用方在响应 notes 中透出（前端横幅提示升级），不产生 stderr 噪音。
    """
    if not isinstance(parsed, dict):
        return parsed, []
    drift = []
    out = dict(parsed)
    for canonical, aliases in cfg.response_aliases.items():
        if canonical not in out:
            for a in aliases:
                if a in out:
                    out[canonical] = out[a]
                    drift.append("alias %s->%s" % (a, canonical))
                    break
    return out, drift
