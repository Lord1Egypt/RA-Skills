"""P3 提示词保真度 —— ct-advisor 出站 payload 构造入口。

被 ct-base P3 套件加载（prompt.build_payload），负责把采样 env 构造成出站 payload。
深拷贝保护确保 P3-04（调用方 env 污染）检查不会误报。
"""
from __future__ import annotations

import copy
import os
import sys

# 确保 adapters 目录在 sys.path 中（P3 套件通过 default_sys_path 已注入，此处为防御性冗余）
_ADAPTERS_DIR = os.path.dirname(os.path.abspath(__file__))
if _ADAPTERS_DIR not in sys.path:
    sys.path.insert(0, _ADAPTERS_DIR)

from refiner import RefineRequest  # type: ignore[import-untyped]


def build_payload(env: dict) -> dict:
    """从采样 env 构造出站 payload。

    流程：
    1. 深拷贝 env（P3-04 防护：确保不污染调用方传入的 sample dict）
    2. 构造 RefineRequest
    3. 调用 to_payload() 经 normalize + validate 构造出站 payload
    """
    env_copy = copy.deepcopy(env)
    req = RefineRequest(**env_copy)
    return req.to_payload()
