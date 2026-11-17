#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pan-downloader — 纯引擎适配器（curl 直链 / 账号档位探测 / HTTP 步骤）。"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import os
import re
import shlex
import subprocess
from pathlib import Path

# 共享工具函数从 engine 懒加载（engine 的命令为懒代理，运行期才 import 本模块，避免循环引用）。
from pancli.engine import *  # noqa: F401,F403

def curl_basic_auth_step(argv, user, password):
    """用 curl --config - 从 stdin 读取 Basic Auth，避免密码出现在 argv/日志。"""
    step = {"engine": "curl", "argv": list(argv), "note": "curl 下载（凭据通过 stdin，不写入命令行）"}
    if user and password:
        escaped_user = str(user).replace("\\", "\\\\").replace('"', '\\"')
        escaped_pass = str(password).replace("\\", "\\\\").replace('"', '\\"')
        step["stdin"] = 'user = "%s:%s"\n' % (escaped_user, escaped_pass)
        step["argv"].insert(-1, "--config")
        step["argv"].insert(-1, "-")
    return step


# ---------------------------------------------------------------- 账号等级探测
def detect_account_tier(drive_key, drive_cfg, cfg):
    """尽力探测账号等级；无法可靠判断时返回空值，绝不把普通账号当会员。"""
    recorded = str(drive_cfg.get("account_tier") or "").strip().lower()
    if recorded in ("free", "vip"):
        return recorded, "配置记录"

    detector = str(drive_cfg.get("tier_detector") or "").strip()
    if not detector:
        return "", "未配置检测器"

    env = os.environ.copy()
    env["PAN_DRIVE"] = drive_key
    env["PAN_COOKIE_FILE"] = str(drive_cfg.get("cookie_file") or "")
    try:
        cmd = shlex.split(detector.format(drive=drive_key))
        if not cmd:
            return "", "检测器为空"
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10, env=env)
    except subprocess.TimeoutExpired:
        return "", "检测器超时"
    except (OSError, ValueError):
        return "", "检测器不可执行"

    text = ((proc.stdout or "") + "\n" + (proc.stderr or "")).lower()
    if re.search(r"(vip|会员|supervip|svip|premium|pro\b)", text):
        return "vip", "tier_detector（%s）" % detector
    if re.search(r"(free|免费|普通)", text):
        return "free", "tier_detector（%s）" % detector
    return "", "检测器未返回明确等级"


# ---------------------------------------------------------------- 计划构建
def http_step(url, target, cfg, tier):
    filename = filename_from_url(url)
    http = cfg.get("http", {})
    argv = [
        "curl", "-L", "--fail", "--retry", str(http.get("retries", 3)),
        "--retry-delay", str(http.get("retry_delay", 5)),
        "--connect-timeout", str(http.get("connect_timeout", 30)),
        "-C", "-", "-o", str(Path(target) / filename), url,
    ]
    return {"engine": "http", "argv": argv, "note": "curl 断点续传下载（免费/会员参数一致）"}


