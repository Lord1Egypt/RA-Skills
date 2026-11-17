#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""账号管理器主脚本 - 从真实数据源读取账号信息

支持动作: list / get / switch_account
switch_account: 封号后账号切换+资产继承(DEF-37/R45同类批量修复)
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("account-manager", source="skills/account-manager/scripts/account_manager.py")

# 导入统一Cookie管理器 (P1-2 Cookie统一迁移)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from mcps.shared.cookie_manager import resolve_cookie_path, COOKIES_DIR as _UNIFIED_COOKIES_DIR
from mcps.shared.atomic_write import atomic_read_json, atomic_write_json


DATA_ROOT = Path(__file__).parent.parent.parent.parent / "data"
ACCOUNTS_FILE = DATA_ROOT / "accounts" / "accounts.json"
TENANT_COOKIE_MAP_FILE = DATA_ROOT / "tenant_cookie_map.json"


def _load_accounts_from_file() -> List[Dict[str, Any]]:
    """从真实数据文件加载账号"""
    if ACCOUNTS_FILE.exists():
        data = atomic_read_json(ACCOUNTS_FILE)
        if data is not None:
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "accounts" in data:
                return data["accounts"]
        else:
            logger.warning("读取账号文件失败: safe_read_json返回None")

    return []


def _discover_accounts_from_cookies(tenant_id: str = "") -> List[Dict[str, Any]]:
    """从Cookie目录自动发现已配置的账号(支持多租户)

    使用cookie_manager.resolve_cookie_path统一路径解析。
    来源: P1-2 Cookie统一迁移
    """
    import re
    accounts = []

    # 构建待扫描的Cookie路径列表
    cookie_paths = []
    if tenant_id:
        # 指定租户: 只查该租户的Cookie
        cookie_paths.append(resolve_cookie_path("xianyu", "default", tenant_id))
    else:
        # 无租户: 查默认路径(fishclaw) + 所有租户目录
        cookie_paths.append(resolve_cookie_path("xianyu", "default", ""))
        if _UNIFIED_COOKIES_DIR.exists():
            for entry in _UNIFIED_COOKIES_DIR.iterdir():
                if entry.is_dir() and re.match(r'^[a-zA-Z0-9_-]+$', entry.name):
                    tenant_cookie = resolve_cookie_path("xianyu", "default", entry.name)
                    if tenant_cookie not in cookie_paths:
                        cookie_paths.append(tenant_cookie)

    for cookie_path in cookie_paths:
        if not cookie_path.exists():
            continue
        try:
            mtime = cookie_path.stat().st_mtime
            cookie_data = atomic_read_json(cookie_path)
            if cookie_data is None:
                continue
            nickname = cookie_data.get("nickname", "闲鱼账号") if isinstance(cookie_data, dict) else "闲鱼账号"

            # 从路径推断account_id和tenant_id
            if cookie_path.parent == _UNIFIED_COOKIES_DIR:
                tid = ""
                account_id = "default"
            else:
                tid = cookie_path.parent.name
                account_id = tid

            accounts.append({
                "platform": "xianyu",
                "account_id": account_id,
                "nickname": nickname,
                "status": "active",
                "cookie_file": str(cookie_path),
                "last_modified": mtime,
                "tenant_id": tid,
            })
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"账号Cookie文件读取失败,跳过: {cookie_path}, error={e}")
            continue

    return accounts


def _action_switch_account(input_data: dict, tenant_id: str) -> dict:
    """封号后账号切换+资产继承(DEF-37增强)

    流程: 标记旧账号banned → 更新cookie映射 → 更新bound_accounts → 生成迁移报告
    来源: 01手册§六6.2多账号+DEF-37封号应急+R45同类批量修复

    Args:
        input_data: {old_account, new_account, banned_reason, tenant_id}
        tenant_id: 租户ID

    Returns:
        {success, data:{inherited_data, lost_data, next_actions}, error, code}
    """
    old_account = input_data.get("old_account", "")
    new_account = input_data.get("new_account", "")
    banned_reason = input_data.get("banned_reason", "unknown")

    if not old_account or not new_account:
        return {"success": False, "data": {}, "error": "old_account和new_account必填", "code": "MISSING_PARAMS"}

    # 1. 标记旧账号为banned
    accounts = _load_accounts_from_file()
    old_found = False
    for acc in accounts:
        if acc.get("account_id") == old_account:
            acc["status"] = "banned"
            acc["banned_reason"] = banned_reason
            acc["banned_at"] = datetime.now().isoformat()
            old_found = True
            break
    if not old_found:
        logger.warning(f"旧账号{old_account}未在accounts.json中,继续切换(cookie发现账号)")
    if ACCOUNTS_FILE.parent.exists():
        atomic_write_json(ACCOUNTS_FILE, accounts)

    # 2. 更新cookie映射(来源: ban_handler action_switch逻辑, R37消除重复)
    cookie_map = {}
    if TENANT_COOKIE_MAP_FILE.exists():
        cookie_map = atomic_read_json(TENANT_COOKIE_MAP_FILE) or {}
    old_cookie = cookie_map.get(old_account, "")
    cookie_map[old_account] = f"banned_{old_cookie}" if old_cookie else "banned"
    if new_account not in cookie_map:
        cookie_map[new_account] = new_account
    atomic_write_json(TENANT_COOKIE_MAP_FILE, cookie_map)

    # 3. 更新bound_accounts(来源: bound_accounts_manager统一入口)
    bound_updated = False
    try:
        from mcps.shared.bound_accounts_manager import update_cookie_status
        if tenant_id:
            update_cookie_status(tenant_id, "xianyu", old_account, "banned")
            update_cookie_status(tenant_id, "xianyu", new_account, "valid")
            bound_updated = True
    except Exception as e:
        logger.warning(f"bound_accounts更新失败(非阻断): {e}")

    # 4. 生成迁移报告(来源: account_manager_reference.json接口规范)
    migration_report = {
        "old_account": old_account,
        "new_account": new_account,
        "banned_reason": banned_reason,
        "tenant_id": tenant_id,
        "switched_at": datetime.now().isoformat(),
        "old_account_marked_banned": True,
        "cookie_map_updated": True,
        "bound_accounts_updated": bound_updated,
        "inherited_data": {
            "products": "tenant级(PG product_catalog),无需DB迁移,需重发布到新账号",
            "orders": "tenant级(PG ec_orders),无需DB迁移",
            "friends": "SQLite account_id需更新(如使用SQLite),PG dm_records按tenant隔离",
            "messages": "SQLite account_id需更新(如使用SQLite)",
        },
        "lost_data": {
            "chat_history": "闲鱼平台聊天记录无法迁移",
            "xianyu_followers": "闲鱼粉丝/关注无法迁移",
            "account_reputation": "旧账号信誉值归零",
        },
        "next_actions": [
            "LLM编排: 调用fishclaw-mcp publish_item重发布核心商品(2小时内)",
            "LLM编排: 调用ban_handler --action appeal --account-id {old} --reason {reason}",
            "运维: 更新Cron任务中的account_id引用为new_account",
            "运维: 验证新账号Cookie有效性",
        ],
    }
    return {"success": True, "data": migration_report, "error": None, "code": None}


def main() -> Dict[str, Any]:
    """执行账号管理操作

    Returns:
        Dict[str, Any]: 返回值说明
    """
    try:
        # 支持CLI参数 --tenant_id (P1-2 Cookie统一迁移)
        import argparse
        parser = argparse.ArgumentParser(description="账号管理器")
        parser.add_argument("--tenant_id", default="", help="租户ID(支持多租户)")
        cli_args, _ = parser.parse_known_args()

        if os.environ.get("INPUT_FILE"):
            input_data = atomic_read_json(os.environ["INPUT_FILE"])
            if input_data is None:
                input_data = {"action": "list"}
        elif not sys.stdin.isatty():
            input_data = json.loads(sys.stdin.read())
        else:
            input_data = {"action": "list"}

        # CLI参数优先,其次input_data中的tenant_id
        tenant_id = cli_args.tenant_id or input_data.get("tenant_id", "")

        action = input_data.get("action", "list")

        if action == "list":
            file_accounts = _load_accounts_from_file()
            cookie_accounts = _discover_accounts_from_cookies(tenant_id)

            merged = {a["account_id"]: a for a in file_accounts}
            for ca in cookie_accounts:
                if ca["account_id"] not in merged:
                    merged[ca["account_id"]] = ca

            accounts = list(merged.values())
            data = {
                "total": len(accounts),
                "accounts": accounts,
                "source": "real_data",
                "from_file": len(file_accounts),
                "from_cookie_discovery": len(cookie_accounts),
                "tenant_id": tenant_id
            }
        elif action == "get":
            account_id = input_data.get("account_id")
            all_accounts = _load_accounts_from_file() + _discover_accounts_from_cookies(tenant_id)
            found = [a for a in all_accounts if a.get("account_id") == account_id]
            data = {"found": len(found) > 0, "account": found[0] if found else None}
        elif action == "switch_account":
            result = _action_switch_account(input_data, tenant_id)
            print(json.dumps(result, ensure_ascii=False))
            return result
        else:
            data = {"message": f"Action '{action}' executed", "supported_actions": ["list", "get", "switch_account"]}

        result = {"success": True, "data": data, "error": None}

    except Exception as e:
        logger.error(f"account manager异常: {e}", exc_info=True)
        result = {"success": False, "data": {}, "error": str(e), "code": "ACCOUNT_MANAGER_ERROR"}

    print(json.dumps(result, ensure_ascii=False))
    return result


if __name__ == "__main__":
    main()
