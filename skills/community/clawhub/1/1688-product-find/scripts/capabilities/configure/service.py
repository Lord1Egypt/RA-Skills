#!/usr/bin/env python3
"""AK 配置服务 — 校验、写入、删除、状态查询"""

import json
import os
import sys
from pathlib import Path
from typing import Tuple

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))
from _auth import AK_CONFIG_PATH as CONFIG_PATH, AK_CONFIG_PATH_CANDIDATES


def validate_ak(ak: str) -> Tuple[bool, str]:
    """校验明文 AK 格式，返回 (is_valid, error_msg)"""
    if not ak:
        return False, "AK 不能为空"
    if len(ak) < 32:
        return False, f"AK 长度不足（当前 {len(ak)}，需要至少 32 位）"
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-=")
    if not all(c in allowed for c in ak):
        return False, "AK 包含非法字符"
    return True, ""


def configure_ak(api_key: str) -> Tuple[bool, str]:
    """写入 AK 到本地配置文件。
    文件格式：{"ak": "..."}。返回 (success, storage_location)"""
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"ak": api_key}, f, ensure_ascii=False, indent=2)
        return True, str(CONFIG_PATH)
    except Exception:
        return False, ""


def remove_ak() -> bool:
    """删除本地 AK 配置文件。返回是否成功。"""
    try:
        if CONFIG_PATH.exists():
            CONFIG_PATH.unlink()
        return True
    except Exception:
        return False

def check_existing_config() -> Tuple[bool, str, str]:
    """检查是否已有 AK。返回 (has_ak, ak_value, source)"""
    env_ak = os.environ.get("ALI_1688_AK", "")
    if env_ak:
        return True, env_ak, "环境变量"

    for config_path in AK_CONFIG_PATH_CANDIDATES:
        if not config_path.exists():
            continue
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ak = data.get("ak")
            if isinstance(ak, str) and ak:
                return True, ak, f"配置文件 {config_path}"
        except Exception:
            continue
    return False, "", ""


def get_config_detail() -> dict:
    """获取当前 AK 配置的详细信息"""
    def _mask(ak: str) -> str:
        if len(ak) >= 8:
            return f"{ak[:4]}****{ak[-4:]}"
        return "****" if ak else "(空)"

    detail = {
        "env_var": {"available": False, "value": ""},
        "config_files": [],
        "write_path": str(CONFIG_PATH),
        "active_ak": None,
        "active_source": None,
    }

    # 1. 环境变量
    env_ak = os.environ.get("ALI_1688_AK", "")
    if env_ak:
        detail["env_var"] = {"available": True, "value": _mask(env_ak)}
        detail["active_ak"] = _mask(env_ak)
        detail["active_source"] = "环境变量 ALI_1688_AK"

    # 2. 遍历所有候选配置文件
    for config_path in AK_CONFIG_PATH_CANDIDATES:
        file_info = {
            "path": str(config_path),
            "exists": config_path.exists(),
            "is_write_target": (config_path == CONFIG_PATH),
            "available": False,
        }
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                ak = data.get("ak", "")
                file_info["ak"] = _mask(ak) if ak else ""
                file_info["available"] = bool(ak)
                if ak and not detail["active_ak"]:
                    detail["active_ak"] = _mask(ak)
                    detail["active_source"] = f"配置文件 `{config_path}`"
            except Exception as e:
                file_info["error"] = str(e)
        detail["config_files"].append(file_info)

    return detail