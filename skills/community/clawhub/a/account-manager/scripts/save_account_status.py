#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""保存账号状态到 JSON 文件 - 重启不丢
从stdin或命令行参数读取账号状态数据，保存到 account_status.json
"""

import json

import os
import sys
from datetime import datetime

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("account-manager", source="skills/account-manager/scripts/save_account_status.py")
from mcps.shared.atomic_write import atomic_write_json

import logging
logger = get_logger("system", source="skills/account-manager/scripts/save_account_status.py")

ACCOUNT_STATUS_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "account_status.json")

def main():
    """保存账号状态
    
    Raises:
        ValueError: 异常说明
    """
    try:
        # 从stdin读取状态数据
        if not sys.stdin.isatty():
            state_data = sys.stdin.read().strip()
        elif len(sys.argv) > 1:
            state_data = sys.argv[1]
        else:
            raise ValueError("请从stdin传入状态JSON，或作为命令行参数传入")

        # 解析JSON
        try:
            state = json.loads(state_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"状态JSON格式错误: {str(e)}")

        # 验证必要字段
        if "accounts" not in state:
            raise ValueError("状态数据必须包含 'accounts' 字段")

        # 添加更新时间
        state["last_updated"] = datetime.now().isoformat()

        # 确保目录存在
        os.makedirs(os.path.dirname(ACCOUNT_STATUS_PATH), exist_ok=True)

        # 写入文件
        atomic_write_json(ACCOUNT_STATUS_PATH, state, indent=2, ensure_ascii=False)

        result = {
            "success": True,
            "data": {
                "saved_at": state["last_updated"],
                "path": ACCOUNT_STATUS_PATH,
                "accounts_count": len(state["accounts"]),
                "banned_count": sum(1 for a in state["accounts"].values() if a.get("status") == "banned"),
                "active_count": sum(1 for a in state["accounts"].values() if a.get("status") == "active")
            },
            "error": None,
            "code": "SAVE_SUCCESS"
        }
        print(json.dumps(result, ensure_ascii=False))

    except ValueError as e:
        logger.error(f"save account status异常: {e}", exc_info=True)
        result = {
            "success": False,
            "data": {},
            "error": f"参数错误: {str(e)}",
            "code": "INVALID_PARAM"
        }
        logger.error(json.dumps(result, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        logger.error(f"save account status异常: {e}", exc_info=True)
        result = {
            "success": False,
            "data": {},
            "error": f"保存异常: {str(e)}",
            "code": "SAVE_ERROR"
        }
        logger.error(json.dumps(result, ensure_ascii=False))
        sys.exit(2)

if __name__ == "__main__":
    main()
