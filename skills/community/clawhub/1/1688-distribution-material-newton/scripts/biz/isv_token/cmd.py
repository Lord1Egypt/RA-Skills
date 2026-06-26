#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ISV Token 命令层

用法：
  python3 cli.py isv_token fetch --app_key=YOUR_APP_KEY [--expire_hours=24] [--force_refresh=true]
  python3 cli.py isv_token status --app_key=YOUR_APP_KEY
"""

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))
from scripts._sys._output import print_output, print_error
from scripts.biz.isv_token.service import fetch_isv_token as _fetch_isv_token
from scripts.biz.isv_token.service import check_token_status as _check_token_status


def fetch(app_key: str = "", expire_hours: str = "24", force_refresh: str = "false"):
    """获取 ISV Token"""
    try:
        if not app_key:
            print_output(False, "❌ 缺少必填参数 app_key", {})
            return

        token = _fetch_isv_token(
            app_key=app_key,
            expire_hours=int(expire_hours),
            force_refresh=force_refresh.lower() in ("true", "1", "yes"),
        )
        print_output(True, f"✅ ISV Token 获取成功（AppKey: {app_key}）", {"token": token})
    except Exception as e:
        print_error(e)


def status(app_key: str = ""):
    """查询 ISV Token 状态"""
    try:
        if not app_key:
            print_output(False, "❌ 缺少必填参数 app_key", {})
            return

        result = _check_token_status(app_key)

        if result["exists"] and not result["expired"]:
            md = f"✅ Token 有效（AppKey: {app_key}，剩余 {result['remainingHours']}h）"
        elif result["exists"] and result["expired"]:
            md = f"⚠️ Token 已过期（AppKey: {app_key}）"
        else:
            md = f"❌ 未找到 Token（AppKey: {app_key}）"

        print_output(True, md, result)
    except Exception as e:
        print_error(e)
