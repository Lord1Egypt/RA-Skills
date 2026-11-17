"""avalanche_recovery.py - Cookie雪崩应急恢复模块 (T-A09)

来源: 30日远程值守运营优化方案v3.0 T-A09
规则: R20(赚钱链路完整性) / R74.4(降级标注三条件) / R72.4(partial_completed保护) / R72.1(Cron保护)
优先级: P0(闲鱼>抖音>小红书>B站>快手) / P1(知乎>头条>微博>百家号>其他) / P2(cnblogs>51cto>oschina>yuque>imooc)
降级模式(R74.4三条件): 1.暂停发布Cron(daily-plan-generator保留R72.1) 2.partial_completed保留(R72.4) 3.恢复后继续
"""
import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils import json_out
from mcps.shared.cookie_manager import COOKIES_DIR
from mcps.shared.db_logger import get_logger

logger = get_logger("cookie-avalanche", source="avalanche_recovery.py")
try:
    from notification import send_alert
except ImportError:
    send_alert = lambda m, l="WARN": logger.error(f"[alert:{l}] {m}")

STATE_FILE = PROJECT_ROOT / "data" / "content" / "avalanche_degradation.json"
AVALANCHE_THRESHOLD = 0.50  # 失效率>50%判定雪崩(>495/990)
# R72.1保护: 编排Cron不暂停 | R72.4保护: partial_completed状态保留
PRESERVED_CRONS = ["daily-plan-generator", "dispatcher-cycle", "self-heal-cycle",
                   "completion-report-generator", "leader-heartbeat",
                   "system-resource-guard", "fairness-debt-settler"]
PAUSED_CRONS = ["matrix-publish", "scheduled-content-publisher", "agency-content-publish",
                "opc-daily-news-broadcast", "opc-daily-promotion",
                "opc-daily-persona-video", "opc-daily-comic-drama"]


def _scan_all_cookies() -> tuple[int, int]:
    """扫描COOKIES_DIR下所有Cookie文件(含多租户),返回(总数,有效数)"""
    total, valid = 0, 0
    if not COOKIES_DIR.exists():
        return 0, 0
    now_ts = datetime.now().timestamp()
    for f in COOKIES_DIR.rglob("*.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if "cookies" not in data:
                continue  # 非Cookie文件跳过
            total += 1
            for c in data.get("cookies", []):
                exp = c.get("expires", -1)
                if exp == -1 or exp > now_ts:  # session cookie或未过期
                    valid += 1
                    break
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue  # 加密文件跳过,不触发误报
        except Exception:
            total += 1  # 不可读=过期
    return total, valid


def get_avalanche_status() -> dict:
    """检测是否处于雪崩状态(失效率>AVALANCHE_THRESHOLD判定)"""
    total, valid = _scan_all_cookies()
    expired = total - valid
    rate = expired / total if total > 0 else 0.0
    return {"is_avalanche": rate > AVALANCHE_THRESHOLD, "total": total,
            "valid": valid, "expired": expired, "failure_rate": round(rate, 4)}


def get_recovery_priority_matrix() -> list:
    """返回平台恢复优先级矩阵(P0赚钱核心5/P1赚钱次要14/P2低频5)"""
    return [
        {"priority": "P0", "platforms": ["xianyu", "douyin", "xiaohongshu", "bilibili", "kuaishou"],
         "description": "赚钱链路核心", "target_recovery_time": "30min"},
        {"priority": "P1", "platforms": ["zhihu", "toutiao", "weibo", "baijiahao", "shipinhao",
                                         "tiktok", "juejin", "csdn", "jianshu", "segmentfault",
                                         "douban", "xueqiu", "eastmoney", "smzdm"],
         "description": "赚钱链路次要", "target_recovery_time": "2h"},
        {"priority": "P2", "platforms": ["cnblogs", "51cto", "oschina", "yuque", "imooc"],
         "description": "低频平台", "target_recovery_time": "24h"},
    ]


def activate_degradation_mode(reason: str) -> dict:
    """激活降级模式(R74.4三条件: #DOWNGRADE注释+db_logger+downgraded字段)"""
    ts = datetime.now(timezone(timedelta(hours=8))).isoformat()
    # R74.4条件1:#DOWNGRADE注释 | R74.4条件2:db_logger记录
    logger.warning(f"#DOWNGRADE Cookie雪崩降级激活 | reason={reason} | paused={PAUSED_CRONS}")
    # R74.4条件3:downgraded=True字段 | R72.1:编排Cron保留 | R72.4:partial_completed不修改
    state = {"downgraded": True, "reason": reason, "activated_at": ts,
             "paused_crons": PAUSED_CRONS, "preserved_crons": PRESERVED_CRONS}
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    send_alert(f"Cookie雪崩降级激活 | 原因:{reason} | 暂停{len(PAUSED_CRONS)}个发布Cron | "
               f"保留{len(PRESERVED_CRONS)}个编排Cron(R72.1+R72.4)", level="CRITICAL")
    return {"activated": True, "paused_crons": PAUSED_CRONS,
            "preserved_crons": PRESERVED_CRONS, "timestamp": ts}


def deactivate_degradation_mode() -> dict:
    """解除降级模式,恢复Cron,partial_completed状态保留(R72.4)"""
    ts = datetime.now(timezone(timedelta(hours=8))).isoformat()
    if STATE_FILE.exists():
        STATE_FILE.unlink()
    logger.info(f"Cookie雪崩降级解除 | ts={ts} | partial_completed保留(R72.4) self-heal继续执行")
    send_alert(f"Cookie雪崩降级解除 | 恢复{len(PAUSED_CRONS)}个Cron | "
               f"partial_completed状态保留继续执行(R72.4)", level="INFO")
    return {"deactivated": True, "resumed_crons": PAUSED_CRONS, "timestamp": ts}


def get_recovery_plan() -> dict:
    """返回分批恢复计划(按优先级矩阵,每批并发25=T-A07 asyncio.Semaphore)"""
    batches = []
    for tier in get_recovery_priority_matrix():
        batches.append({"priority": tier["priority"], "platforms": tier["platforms"],
                        "estimated_time": tier["target_recovery_time"],
                        "concurrency": 25,  # T-A07 asyncio.Semaphore(25)
                        "action": "逐平台扫码恢复Cookie,cookie_keepalive验证有效性"})
    return {"batches": batches,
            "total_platforms": sum(len(b["platforms"]) for b in batches)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="T-A09 Cookie雪崩应急恢复")
    parser.add_argument("action", choices=["status", "matrix", "activate", "deactivate", "plan"])
    parser.add_argument("--reason", default="Cookie雪崩自动检测触发")
    args = parser.parse_args()
    try:
        if args.action == "status":
            result = get_avalanche_status()
        elif args.action == "matrix":
            result = {"matrix": get_recovery_priority_matrix()}
        elif args.action == "activate":
            result = activate_degradation_mode(args.reason)
        elif args.action == "deactivate":
            result = deactivate_degradation_mode()
        else:
            result = get_recovery_plan()
        json_out(True, data=result)
    except Exception as e:
        logger.error(f"avalanche_recovery异常: {e}")
        json_out(False, error=str(e), code="AVALANCHE_RECOVERY_ERROR")
