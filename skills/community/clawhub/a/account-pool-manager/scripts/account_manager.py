#!/usr/bin/env python3
"""
account_manager.py - 账号池管理 exec 脚本（账号注册/查询/轮换）
功能：按部门管理账号、智能选择发布账号、轮换策略
输出：{success:bool, data:{account_id, platforms:{...}}, error:str, code:str}

目录结构:
data/content/accounts/
├── pool_config.json          # 全局配置
├── self_media/               # 自媒体自营
├── social_dept/              # 社交部
├── ecommerce_dept/           # 电商部
└── clients/                  # 外包客户
"""
import json

import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("account-pool-manager", source="skills/account-pool-manager/scripts/account_manager.py")

# 导入统一Cookie管理器 (P1-2 Cookie统一迁移)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
from mcps.shared.cookie_manager import resolve_cookie_path
from mcps.shared.atomic_write import atomic_read_json, atomic_write_json

import logging
logger = get_logger("system", source="skills/account-pool-manager/scripts/account_manager.py")

BASE_DIR = Path(__file__).parent.parent.parent.parent / "data" / "content" / "accounts"
COOKIES_DIR = Path(__file__).parent.parent.parent.parent / "data" / "content" / "cookies"
BUSINESS_TYPE_MAP = {
    "self_media": "self_media", "social_dept": "social_dept",
    "ecommerce_dept": "ecommerce_dept",
}

# 多账号发布17分钟间隔规则（来源: 01电商运营手册§六6.2）
PUBLISH_COOLDOWN_SECONDS = 17 * 60  # 17分钟 = 1020秒
PUBLISH_TIMES_FILE = BASE_DIR / "account_publish_times.json"

# 健康度评分文件（由 account-nurturer 写入，DEF-27）
HEALTH_SCORES_FILE = BASE_DIR / "account_health_scores.json"

# 健康度阈值：低于此分数的账号标记为"不推荐发布"
HEALTH_SCORE_NOT_RECOMMEND = 30

def _load_publish_times() -> dict:
    """加载账号发布时间记录"""
    try:
        if PUBLISH_TIMES_FILE.exists():
            data = atomic_read_json(PUBLISH_TIMES_FILE)
            if data is not None:
                return data
            logger.warning("account_manager: safe_read_json返回None")
    except Exception as e:
        # DOWNGRADE: 账号池加载失败,降级返回空字典
        logger.error(f"降级: account_manager发布时间加载失败,返回空字典: {e}")
    return {}

def _save_publish_times(times: dict):
    """保存账号发布时间记录"""
    PUBLISH_TIMES_FILE.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(PUBLISH_TIMES_FILE, times, indent=2, ensure_ascii=False)

def _load_health_scores() -> dict:
    """加载账号健康度评分（由 account-nurturer 写入，DEF-27）"""
    try:
        if HEALTH_SCORES_FILE.exists():
            data = atomic_read_json(HEALTH_SCORES_FILE)
            if data is not None:
                return data
            logger.warning("account_manager: safe_read_json返回None")
    except Exception as e:
        # DOWNGRADE: 账号健康度加载失败,降级返回空字典
        logger.error(f"降级: account_manager健康度加载失败,返回空字典: {e}")
    return {}

def init_pool() -> None:
    """初始化账户池目录结构"""
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    COOKIES_DIR.mkdir(parents=True, exist_ok=True)
    for dept in ["self_media", "social_dept", "ecommerce_dept", "clients"]:
        (BASE_DIR / dept).mkdir(exist_ok=True)
    config_path = BASE_DIR / "pool_config.json"
    if not config_path.exists():
        atomic_write_json(config_path, {"version": "1.1", "created_at": datetime.utcnow().isoformat() + "Z",
                       "departments": ["self_media", "social_dept", "ecommerce_dept", "clients"],
                       "default_daily_limit": 10, "cookie_check_interval_hours": 24}, indent=2, ensure_ascii=False)

def get_publish_account(business_type: str, platforms: list) -> dict[str, Any]:
    """获取发布账号：按部门筛选 → 过滤可用账号 → 17分钟冷却检查 → 健康度排序 → 轮换选择

    Args:
        business_type (str): 参数说明
        platforms (list): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        init_pool()
        dept = BUSINESS_TYPE_MAP.get(business_type)
        if not dept:
            if business_type.startswith("client_"): dept = "clients"
            else:
                return {"success": False, "data": {}, "error": f"无效业务类型: {business_type}", "code": "AP-ERR-01"}
        dept_dir = BASE_DIR / dept
        if not dept_dir.exists():
            return {"success": False, "data": {}, "error": f"部门目录不存在: {dept}", "code": "AP-ERR-02"}
        accounts = []
        for account_file in dept_dir.glob("*.json"):
            account = atomic_read_json(account_file)
            if account is None:
                continue
            account_platforms = {}
            for platform in platforms:
                pi = account.get("platforms", {}).get(platform, {})
                if pi.get("status") == "active" and pi.get("publish_count_today", 0) < pi.get("daily_limit", 10):
                    account_platforms[platform] = {"cookie_path": pi.get("cookie_path", ""), "status": "active",
                                                   "publish_count_today": pi.get("publish_count_today", 0),
                                                   "daily_limit": pi.get("daily_limit", 10),
                                                   "last_publish": pi.get("last_publish")}
            if account_platforms:
                accounts.append({"account_id": account.get("account_id"), "account_file": str(account_file),
                                 "platforms": account_platforms})
        if not accounts:
            return {"success": False, "data": {}, "error": f"部门 {dept} 下无可用账号", "code": "AP-ERR-03"}

        # 17分钟冷却检查（来源: 01电商运营手册§六6.2，多账号发布间隔≥17分钟）
        publish_times = _load_publish_times()
        now = time.time()
        available = []
        for acc in accounts:
            last_publish_ts = publish_times.get(acc["account_id"], 0)
            elapsed = now - last_publish_ts
            if elapsed >= PUBLISH_COOLDOWN_SECONDS:
                available.append(acc)

        if not available:
            # 所有账号都在17分钟冷却期内，计算最快可用时间
            min_wait = min(
                PUBLISH_COOLDOWN_SECONDS - (now - publish_times.get(acc["account_id"], 0))
                for acc in accounts
            )
            return {"success": False, "data": {"min_wait_seconds": int(min_wait)},
                    "error": f"所有账号均在17分钟冷却期，最快{int(min_wait / 60)}分{int(min_wait % 60)}秒后可用",
                    "code": "ACCOUNT_COOLDOWN"}

        # 加载健康度评分（DEF-27: account-nurturer → account-pool-manager 健康度传递）
        health_scores = _load_health_scores()

        # 为每个可用账号附加健康度信息
        for acc in available:
            record = health_scores.get(acc["account_id"], {})
            acc["health_score"] = record.get("health_score", 60)  # 无记录时默认60分（基础分）

        # 按健康度降序排序（健康度高的优先选择）
        available.sort(key=lambda a: a["health_score"], reverse=True)

        # 检查健康度<30的账号，标记为"不推荐发布"
        not_recommended = [acc for acc in available if acc["health_score"] < HEALTH_SCORE_NOT_RECOMMEND]
        recommended = [acc for acc in available if acc["health_score"] >= HEALTH_SCORE_NOT_RECOMMEND]

        # 优先从推荐账号中选择，若无推荐账号则从不推荐中选择（降级策略）
        candidates = recommended if recommended else available

        # 从候选账号中，选择last_publish最早的（轮换策略）
        selected = min(candidates, key=lambda a: min((p.get("last_publish") or "1970-01-01") for p in a["platforms"].values()))

        result_data = {
            "account_id": selected["account_id"],
            "department": dept,
            "platforms": selected["platforms"],
            "health_score": selected["health_score"],
        }

        # 如果选中了不推荐账号，添加警告
        if selected["health_score"] < HEALTH_SCORE_NOT_RECOMMEND:
            result_data["health_warning"] = f"健康度{selected['health_score']}分<{HEALTH_SCORE_NOT_RECOMMEND}，不推荐发布"

        # 如果有不推荐账号，附加统计信息
        if not_recommended:
            result_data["not_recommended_count"] = len(not_recommended)
            result_data["not_recommended_accounts"] = [
                {"account_id": acc["account_id"], "health_score": acc["health_score"]}
                for acc in not_recommended
            ]

        return {"success": True, "data": result_data, "error": None, "code": "AP-SUCCESS-01"}
    except Exception as e:
        logger.error(f"account manager异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "AP-ERR-UNKNOWN"}

def register_account(account_data: dict) -> dict[str, Any]:
    """注册新账号（支持多租户）

    Args:
        account_data (dict): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        init_pool()
        account_id = account_data.get("account_id", "")
        department = account_data.get("department", "")
        tenant_id = account_data.get("tenant_id", "")
        if not account_id or not department:
            return {"success": False, "data": {}, "error": "缺少 account_id 或 department", "code": "AP-ERR-04"}
        dept_dir = BASE_DIR / department
        dept_dir.mkdir(parents=True, exist_ok=True)
        account_file = dept_dir / f"{account_id}.json"
        if account_file.exists():
            return {"success": False, "data": {}, "error": f"账号已存在: {account_id}", "code": "AP-ERR-05"}
        now = datetime.utcnow().isoformat() + "Z"
        platforms = {}
        for platform in account_data.get("platforms", {}):
            platforms[platform] = {"cookie_path": str(resolve_cookie_path(platform, account_id, tenant_id)),
                                   "status": "pending_cookie", "last_publish": None,
                                   "publish_count_today": 0, "daily_limit": account_data.get("daily_limit", 10)}
        account = {"account_id": account_id, "department": department, "tenant_id": tenant_id,
                   "platforms": platforms, "created_at": now, "notes": account_data.get("notes", "")}
        atomic_write_json(account_file, account, indent=2, ensure_ascii=False)
        return {"success": True, "data": {"account_id": account_id, "account_file": str(account_file)},
                "error": None, "code": "AP-SUCCESS-02"}
    except Exception as e:
        logger.error(f"account manager异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "AP-ERR-UNKNOWN"}

def record_publish(account_id: str) -> dict[str, Any]:
    """记录账号发布时间，用于17分钟冷却检查

    Args:
        account_id (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        publish_times = _load_publish_times()
        now = time.time()
        publish_times[account_id] = now
        _save_publish_times(publish_times)
        return {"success": True, "data": {"account_id": account_id, "published_at": now},
                "error": None, "code": "AP-SUCCESS-03"}
    except Exception as e:
        logger.error(f"account manager异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "AP-ERR-UNKNOWN"}

def main():
    """主入口"""
    try:
        if len(sys.argv) < 2:
            print(json.dumps({"success": False, "data": {}, "error": "用法: python account_manager.py <action> [args...]", "code": "AP-ERR-USAGE"}))
            sys.exit(1)
        action = sys.argv[1]
        if action == "get_publish_account":
            if len(sys.argv) < 4:
                print(json.dumps({"success": False, "data": {}, "error": "用法: python account_manager.py get_publish_account <business_type> <platforms>", "code": "AP-ERR-USAGE"}))
                sys.exit(1)
            result = get_publish_account(sys.argv[2], sys.argv[3].split(","))
        elif action == "register_account":
            if len(sys.argv) < 3:
                print(json.dumps({"success": False, "data": {}, "error": "用法: python account_manager.py register_account '<json>'", "code": "AP-ERR-USAGE"}))
                sys.exit(1)
            result = register_account(json.loads(sys.argv[2]))
        elif action == "record_publish":
            if len(sys.argv) < 3:
                print(json.dumps({"success": False, "data": {}, "error": "用法: python account_manager.py record_publish <account_id>", "code": "AP-ERR-USAGE"}))
                sys.exit(1)
            result = record_publish(sys.argv[2])
        else:
            result = {"success": False, "data": {}, "error": f"未知操作: {action}", "code": "AP-ERR-UNKNOWN"}
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        logger.error(f"account manager异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "AP-ERR-MAIN"}, ensure_ascii=False))
        sys.exit(2)

if __name__ == "__main__":
    main()
