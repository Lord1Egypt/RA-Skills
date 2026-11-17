"""customer-crm Skill exec脚本 v1.0 (P0核心: 打通auto-delivery回调)

状态: 最小可用版本 (MVP) - 仅实现auto-delivery依赖的delivery_callback子命令
完整功能: 来源追踪(公众号/闲鱼/抖音/快手)/复购推荐/会员等级→ P1 backlog

设计原则:
- 满足铁律6(根因): 解决auto-delivery customer_crm.py不存在的硬性问题
- 满足铁律17(防简化): 实现auto-delivery必须的delivery_callback + 持久化存储
- 满足铁律4(容错): 子命令分发, 缺参返回error code, 不崩溃

用法:
    python customer_crm.py delivery_callback '{"buyer_id":"...", "product_name":"...", ...}'
    python customer_crm.py lookup '{"buyer_id":"..."}'
    python customer_crm.py list_recent '{"limit":10}'

返回:
    stdout: JSON {success, data, error, code}
    exit: 0=success, 1=arg error, 2=runtime error
"""
import json
import sys
import time
from pathlib import Path

from pathlib import Path as _Path
from typing import Any
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("customer-crm", source="skills/customer-crm/scripts/customer_crm.py")

ROOT = Path(__file__).resolve().parent.parent.parent.parent
CUSTOMER_DB = ROOT / "data" / "customer_crm" / "customers.jsonl"
CUSTOMER_DB.parent.mkdir(parents=True, exist_ok=True)


def load_customers() -> list[Any]:
    """加载 customers

    Returns:
        list[Any]: 返回值说明
    """
    if not CUSTOMER_DB.exists():
        return []
    out = []
    with open(CUSTOMER_DB, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return out


def save_customer(record: dict) -> None:
    """保存 customer

    Args:
        record (dict): 参数说明
    """
    with open(CUSTOMER_DB, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def calc_segment(total_spent: float, order_count: int) -> str:
    """简单分群: 新客(<¥10) / 常客(¥10-100) / VIP(>¥100)

    Args:
        total_spent (float): 参数说明
        order_count (int): 参数说明

    Returns:
        str: 返回值说明
    """
    if total_spent >= 100:
        return "VIP"
    if total_spent >= 10 or order_count >= 2:
        return "regular"
    return "new"


def calc_lifecycle(first_seen: str) -> str:
    """生命周期: 7天内=active, 30天内=warming, 超过=churned

    Args:
        first_seen (str): 参数说明

    Returns:
        str: 返回值说明
    """
    try:
        first_ts = time.mktime(time.strptime(first_seen[:19], "%Y-%m-%d %H:%M:%S"))
        days = (time.time() - first_ts) / 86400
    except Exception as e:
        logger.error(f"生命周期计算失败(first_seen={first_seen}): {e}")
        return "unknown"
    if days <= 7:
        return "active"
    if days <= 30:
        return "warming"
    return "churned"


def cmd_delivery_callback(data_str: str) -> dict[str, Any]:
    """auto-delivery发货后回调, 写入/更新客户档案

    Args:
        data_str (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        data = json.loads(data_str) if isinstance(data_str, str) else data_str
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse failed: {e}", "code": "INVALID_JSON"}

    buyer_id = str(data.get("buyer_id", "")).strip()
    if not buyer_id:
        return {"success": False, "error": "buyer_id is required", "code": "MISSING_BUYER_ID"}

    now = data.get("delivery_time") or time.strftime("%Y-%m-%d %H:%M:%S")
    price = float(data.get("price", 0) or 0)
    product = str(data.get("product_name", "")).strip()

    # 查找已有记录
    customers = load_customers()
    existing = None
    for c in customers:
        if str(c.get("buyer_id")) == buyer_id:
            existing = c
            break

    if existing:
        existing["last_order_at"] = now
        existing["last_product"] = product
        existing["order_count"] = existing.get("order_count", 0) + 1
        existing["total_spent"] = round(existing.get("total_spent", 0) + price, 2)
        existing["segment"] = calc_segment(existing["total_spent"], existing["order_count"])
        existing["lifecycle_stage"] = calc_lifecycle(existing.get("first_seen", now))
        existing["source"] = existing.get("source", data.get("source", "xianyu"))
        # 重写整行
        _rewrite_customer(existing)
        record = existing
    else:
        record = {
            "customer_id": f"C{buyer_id[-8:]}",
            "buyer_id": buyer_id,
            "first_seen": now,
            "last_order_at": now,
            "last_product": product,
            "order_count": 1,
            "total_spent": round(price, 2),
            "segment": calc_segment(price, 1),
            "lifecycle_stage": "active",
            "source": data.get("source", "xianyu"),
            "tags": [],
        }
        save_customer(record)

    return {
        "success": True,
        "data": {
            "customer_id": record["customer_id"],
            "segment": record["segment"],
            "lifecycle_stage": record["lifecycle_stage"],
            "order_count": record["order_count"],
            "total_spent": record["total_spent"],
        },
        "error": None,
        "code": None,
    }


def _rewrite_customer(updated: dict) -> None:
    """重写文件中指定buyer_id的客户行"""
    if not CUSTOMER_DB.exists():
        return
    lines = []
    found = False
    with open(CUSTOMER_DB, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line.strip())
                if rec.get("buyer_id") == updated.get("buyer_id"):
                    lines.append(json.dumps(updated, ensure_ascii=False))
                    found = True
                else:
                    lines.append(line.rstrip())
            except json.JSONDecodeError:
                lines.append(line.rstrip())
    if not found:
        lines.append(json.dumps(updated, ensure_ascii=False))
    with open(CUSTOMER_DB, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def cmd_lookup(data_str: str) -> dict[str, Any]:
    """cmd lookup

    Args:
        data_str (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        data = json.loads(data_str) if isinstance(data_str, str) else data_str
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse failed: {e}", "code": "INVALID_JSON"}
    buyer_id = str(data.get("buyer_id", "")).strip()
    if not buyer_id:
        return {"success": False, "error": "buyer_id is required", "code": "MISSING_BUYER_ID"}
    for c in load_customers():
        if str(c.get("buyer_id")) == buyer_id:
            return {"success": True, "data": c, "error": None, "code": None}
    return {"success": False, "error": "customer not found", "code": "NOT_FOUND"}


def cmd_list_recent(data_str: str) -> dict[str, Any]:
    """cmd list recent

    Args:
        data_str (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    try:
        data = json.loads(data_str) if isinstance(data_str, str) else data_str
    except (json.JSONDecodeError, TypeError):
        data = {}
    limit = int(data.get("limit", 10) or 10)
    customers = load_customers()
    # 按last_order_at降序
    customers.sort(key=lambda c: c.get("last_order_at", ""), reverse=True)
    return {
        "success": True,
        "data": {"customers": customers[:limit], "total": len(customers)},
        "error": None,
        "code": None,
    }


COMMANDS = {
    "delivery_callback": cmd_delivery_callback,
    "lookup": cmd_lookup,
    "list_recent": cmd_list_recent,
}


def main():
    """main"""
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "missing subcommand", "code": "MISSING_ARG"}))
        sys.exit(1)
    sub = sys.argv[1]
    if len(sys.argv) > 2:
        data_str = sys.argv[2]
    elif not sys.stdin.isatty():
        try:
            data_str = sys.stdin.read()
        except Exception as e:
            logger.error(f"stdin读取失败: {e}")
            data_str = "{}"
    else:
        data_str = "{}"
    fn = COMMANDS.get(sub)
    if not fn:
        print(json.dumps({"success": False, "error": f"unknown subcommand: {sub}", "code": "UNKNOWN_CMD"}))
        sys.exit(1)
    try:
        result = fn(data_str)
        sys.stdout.write(json.dumps(result, ensure_ascii=False))
        sys.stdout.flush()
        sys.exit(0 if result.get("success") else 1)
    except Exception as e:
        logger.error(f"customer crm异常: {e}", exc_info=True)
        sys.stdout.write(json.dumps({"success": False, "error": str(e)[:200], "code": "RUNTIME_ERROR"}))
        sys.stdout.flush()
        sys.exit(2)


if __name__ == "__main__":
    main()
