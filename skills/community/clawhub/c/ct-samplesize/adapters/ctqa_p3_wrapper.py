"""P3 提示词保真度 —— ct-samplesize 出站 payload 构造入口。

被 ct-base P3 套件加载（prompt.build_payload），负责把采样 env 构造成出站 payload。
深拷贝保护确保 P3-04（调用方 env 污染）检查不会误报。
"""
from __future__ import annotations

import argparse
import copy
import os
import sys

# 确保 adapters 目录在 sys.path 中（P3 套件通过 default_sys_path 已注入，此处为防御性冗余）
_ADAPTERS_DIR = os.path.dirname(os.path.abspath(__file__))
if _ADAPTERS_DIR not in sys.path:
    sys.path.insert(0, _ADAPTERS_DIR)
# compute_backend.py 在 scripts/ 目录
_SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(_ADAPTERS_DIR)), "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from coze_client import build_params  # type: ignore[import-untyped]


def build_payload(env: dict) -> dict:
    """从采样 env 构造出站 payload。

    流程：
    1. 深拷贝 env（P3-04 防护：确保不污染调用方传入的 sample dict）
    2. 把 env["args"] 转成 argparse.Namespace（build_params 内部用 vars(args)）
    3. 调用 coze_client.build_params(test, args, ctx) 构造出站 payload
    """
    env_copy = copy.deepcopy(env)
    test = env_copy.get("test", "ttest_ind")
    args_dict = env_copy.get("args", {})
    ctx = env_copy.get("ctx", {})

    # build_params 内部调用 vars(args)，需要 Namespace 对象
    args_obj = argparse.Namespace(**args_dict) if isinstance(args_dict, dict) else args_dict

    return build_params(test, args_obj, ctx)
