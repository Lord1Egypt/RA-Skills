#!/usr/bin/env python3
"""
report_manager.py - Cookie 健康报告管理 exec 脚本
功能：生成健康报告、查询历史报告
输出：{success:bool, data:{report}, error:str, code:str}
"""
import json
import sys
from pathlib import Path
from datetime import datetime

from pathlib import Path as _Path
from typing import Any
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("account-pool-manager", source="skills/account-pool-manager/scripts/report_manager.py")
from mcps.shared.atomic_write import atomic_read_json, atomic_write_json


HEALTH_DIR = Path(__file__).parent.parent.parent.parent / "data" / "content" / "health"


def save_health_report(health_data: dict) -> dict[str, Any]:
    """保存健康报告到文件

    Args:
        health_data (dict): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        HEALTH_DIR.mkdir(parents=True, exist_ok=True)

        report = {
            "check_time": datetime.utcnow().isoformat() + "Z",
            "total_cookies": health_data.get("total_cookies", 0),
            "healthy": health_data.get("healthy", 0),
            "warning": health_data.get("warning", 0),
            "expired": health_data.get("expired", 0),
            "details": health_data.get("details", []),
        }

        report_path = HEALTH_DIR / "health_report.json"
        atomic_write_json(report_path, report, indent=2, ensure_ascii=False)

        return {
            "success": True,
            "data": {
                "health_report_path": str(report_path),
                "total_cookies": report["total_cookies"],
                "healthy": report["healthy"],
                "warning": report["warning"],
                "expired": report["expired"],
            },
            "error": None,
            "code": "AP-SUCCESS-03",
        }

    except Exception as e:
        logger.error(f"report manager异常: {e}", exc_info=True)
        return {
            "success": False,
            "data": {},
            "error": str(e),
            "code": "AP-ERR-UNKNOWN",
        }


def get_health_report() -> dict[str, Any]:
    """获取最新健康报告

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        report_path = HEALTH_DIR / "health_report.json"
        if not report_path.exists():
            return {
                "success": False,
                "data": {},
                "error": "无健康报告，请先运行 check_all",
                "code": "AP-ERR-08",
            }

        report = atomic_read_json(report_path)
        if report is None:
            return {
                "success": False,
                "data": {},
                "error": "健康报告读取失败",
                "code": "AP-ERR-09",
            }

        return {
            "success": True,
            "data": report,
            "error": None,
            "code": "AP-SUCCESS-07",
        }

    except Exception as e:
        logger.error(f"report manager异常: {e}", exc_info=True)
        return {
            "success": False,
            "data": {},
            "error": str(e),
            "code": "AP-ERR-UNKNOWN",
        }


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "data": {},
            "error": "用法: python report_manager.py <action> [args...]",
            "code": "RM-ERR-USAGE",
        }))
        sys.exit(1)

    action = sys.argv[1]

    if action == "get_report":
        result = get_health_report()
    else:
        result = {
            "success": False,
            "data": {},
            "error": f"未知操作: {action}",
            "code": "RM-ERR-UNKNOWN",
        }

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
