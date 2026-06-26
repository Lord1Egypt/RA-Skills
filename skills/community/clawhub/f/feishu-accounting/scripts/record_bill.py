#!/usr/bin/env python3
"""
账单记录脚本
将账单信息写入 bills/YYYY-MM-DD.md，同一天的记录累加追加。
支持可选 --feishu 同步到飞书多维表格（单表模式，类型字段区分收支）。

用法：
    python record_bill.py --amount 50.00 --type expense --category 餐饮 --note "午饭"
    python record_bill.py --amount 50.00 --type expense --category 餐饮 --note "午饭" --feishu
    python record_bill.py --list            # 列出今日账单
    python record_bill.py --list --date 2024-01-15
    python record_bill.py --summary --month 2024-01  # 月度汇总

环境变量（可选）：
    FEISHU_APP_ID            飞书应用 App ID
    FEISHU_APP_SECRET        飞书应用 App Secret
    FEISHU_BASE_TOKEN        多维表格 Base Token
    FEISHU_DETAIL_TABLE_ID   明细表 Table ID（单表，含类型字段区分收支）
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import date, datetime
from pathlib import Path

# ── 自动加载 skill 目录下的 .env ──────────────────────────────────────────
_SKILL_ENV = Path(__file__).parent.parent / ".env"
if _SKILL_ENV.exists():
    for line in _SKILL_ENV.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

# ── 配置 ─────────────────────────────────────────────────────────────────
BILLS_DIR = Path(__file__).parent.parent / "bills"
VALID_TYPES = {"expense": "支出", "income": "收入"}

# 飞书多维表格配置
FEISHU_BASE_TOKEN = os.environ.get("FEISHU_BASE_TOKEN", "")
FEISHU_DETAIL_TABLE_ID = os.environ.get("FEISHU_DETAIL_TABLE_ID", "")
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

# 本地分类名 → 飞书选项名映射
FEISHU_CATEGORY_MAP = {
    "餐饮": "餐饮", "购物": "购物", "交通": "交通", "娱乐": "娱乐",
    "通讯": "通讯", "生活": "生活", "医疗": "医疗", "住房": "住房",
    "教育": "教育", "服饰": "服饰", "数码": "数码", "运动": "运动",
    "宠物": "宠物", "其他": "其它", "银行": "其它",
    "工资": "工资", "奖金": "奖金", "兼职": "兼职", "投资": "投资",
}


# ── 工具函数 ──────────────────────────────────────────────────────────────

def get_today() -> str:
    return date.today().strftime("%Y-%m-%d")


def get_time_str() -> str:
    return datetime.now().strftime("%H:%M")


def validate_date(date_str: str) -> str:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError(f"日期格式错误，应为 YYYY-MM-DD，实际：{date_str}")


def bill_file_path(date_str: str) -> Path:
    return BILLS_DIR / f"{date_str}.md"


def _check_feishu_config() -> None:
    if not FEISHU_BASE_TOKEN or not FEISHU_DETAIL_TABLE_ID:
        raise RuntimeError(
            "飞书凭证未配置！请设置以下环境变量：\n"
            "  FEISHU_BASE_TOKEN        （多维表格 Base Token）\n"
            "  FEISHU_DETAIL_TABLE_ID   （明细表 Table ID）\n"
            "\n或在 .env 文件中配置。"
        )
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        raise RuntimeError(
            "飞书 App 凭证未配置！请设置以下环境变量：\n"
            "  FEISHU_APP_ID     （App ID）\n"
            "  FEISHU_APP_SECRET （App Secret）\n"
            "\n或在 .env 文件中配置。"
        )


def _get_tenant_token() -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        raise RuntimeError(f"获取 Tenant Token 失败: {result}")
    return result["tenant_access_token"]


def sync_to_feishu(amount: float, bill_type: str, category: str,
                    note: str, date_str: str) -> dict:
    """
    同步单条记录到飞书多维表格（单表模式）。
    字段：文本/月份/分类/金额/类型
    """
    month = date_str[:7]
    type_label = "支出" if bill_type == "expense" else "收入"
    feishu_category = FEISHU_CATEGORY_MAP.get(category, "其它")

    token = _get_tenant_token()
    url = (f"https://open.feishu.cn/open-apis/base/v3/bases/{FEISHU_BASE_TOKEN}"
           f"/tables/{FEISHU_DETAIL_TABLE_ID}/records")
    payload = {
        "月份": month,
        "分类": feishu_category,
        "金额": amount,
        "文本": f"{date_str} {get_time_str()}{note}",
        "类型": type_label,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            if result.get("code") == 0:
                return {"success": True}
            return {"success": False, "error": f"code={result.get('code')}, msg={result.get('msg')}"}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"success": False, "error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── 读取现有账单 ───────────────────────────────────────────────────────────

def parse_bill_file(file_path: Path) -> dict:
    """解析账单文件，返回记录列表和汇总数据"""
    if not file_path.exists():
        return {"records": [], "total_expense": 0.0, "total_income": 0.0}

    content = file_path.read_text(encoding="utf-8")
    records = []
    table_pattern = re.compile(
        r'^\|\s*(\d{2}:\d{2})\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|'
        r'\s*[¥￥]?([\d.]+)\s*\|\s*([^|]*?)\s*\|', re.MULTILINE)
    for m in table_pattern.finditer(content):
        time_str, type_str, category, amount_str, note = m.groups()
        try:
            records.append({
                "time": time_str.strip(),
                "type": "expense" if "支出" in type_str else "income",
                "type_label": type_str.strip(),
                "category": category.strip(),
                "amount": float(amount_str),
                "note": note.strip(),
            })
        except ValueError:
            continue

    total_expense = sum(r["amount"] for r in records if r["type"] == "expense")
    total_income = sum(r["amount"] for r in records if r["type"] == "income")
    return {"records": records, "total_expense": total_expense, "total_income": total_income}


# ── 生成账单文件内容 ────────────────────────────────────────────────────────

def build_bill_content(date_str: str, records: list[dict]) -> str:
    lines = [f"# 账单 {date_str}", "",
             "| 时间 | 类型 | 分类 | 金额 | 备注 |",
             "|------|------|------|------|------|"]
    for r in records:
        lines.append(f"| {r['time']} | {r['type_label']} | {r['category']} | ¥{r['amount']:.2f} | {r['note']} |")
    total_expense = sum(r["amount"] for r in records if r["type"] == "expense")
    total_income = sum(r["amount"] for r in records if r["type"] == "income")
    net = total_income - total_expense
    net_str = f"+¥{net:.2f}" if net >= 0 else f"-¥{abs(net):.2f}"
    lines += ["", "---",
              f"**今日支出：¥{total_expense:.2f} | 今日收入：¥{total_income:.2f} | 净额：{net_str}**", ""]
    return "\n".join(lines)


# ── 添加记录 ──────────────────────────────────────────────────────────────

def add_record(amount: float, bill_type: str, category: str,
               note: str, date_str: str, sync_feishu: bool = False) -> dict:
    """追加一条账单记录，返回操作结果"""
    BILLS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = bill_file_path(date_str)
    existing = parse_bill_file(file_path)

    type_label = VALID_TYPES[bill_type]
    new_record = {
        "time": get_time_str(), "type": bill_type, "type_label": type_label,
        "category": category, "amount": amount, "note": note,
    }
    records = existing["records"] + [new_record]
    file_path.write_text(build_bill_content(date_str, records), encoding="utf-8")

    total_expense = sum(r["amount"] for r in records if r["type"] == "expense")
    total_income = sum(r["amount"] for r in records if r["type"] == "income")

    result = {
        "success": True, "record": new_record, "date": date_str, "file": str(file_path),
        "today_total_expense": round(total_expense, 2),
        "today_total_income": round(total_income, 2),
        "today_net": round(total_income - total_expense, 2),
        "today_count": len(records),
    }

    # 同步飞书（单表模式：所有记录写入明细表，用类型字段区分收支）
    if sync_feishu:
        _check_feishu_config()
        feishu_result = sync_to_feishu(amount, bill_type, category, note, date_str)
        result["feishu"] = feishu_result
        if not feishu_result["success"]:
            result["warning"] = f"飞书同步失败: {feishu_result.get('error')}"

    return result


def _delete_from_feishu(record: dict, date_str: str) -> dict:
    """
    从飞书明细表删除匹配的记录。
    通过【文本前半段日期 + 金额 + 类型】三重校验定位，不依赖备注字段。
    - 找到 1 条匹配 → 删除并返回 record_id
    - 找到 0 条 → 警告（本地有记录但飞书找不到，可能已被手动删除）
    - 找到多条 → 警告（数据不一致，拒绝删除）
    """
    try:
        token = _get_tenant_token()
        target_date = date_str[:10]  # "YYYY-MM-DD"
        target_amount = record["amount"]
        target_type = record.get("type_label", "")  # '支出' 或 '收入'
        base = FEISHU_BASE_TOKEN
        tbl = FEISHU_DETAIL_TABLE_ID

        # 获取字段 ID 映射
        url_fields = (f"https://open.feishu.cn/open-apis/base/v3/bases/{base}"
                      f"/tables/{tbl}/fields")
        req_fields = urllib.request.Request(url_fields, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req_fields, timeout=15) as resp:
            fields_data = json.loads(resp.read())
        field_map = {}
        for f in fields_data.get("data", {}).get("fields", []):
            field_map[f["name"]] = f["id"]

        amount_fid = field_map.get("金额")
        type_fid = field_map.get("类型")
        text_fid = field_map.get("文本")
        if not all([amount_fid, type_fid, text_fid]):
            return {"success": False, "error": "飞书字段映射失败：金额/类型/文本"}

        # 翻页搜索匹配记录
        offset = 0
        candidates = []
        while True:
            url = (f"https://open.feishu.cn/open-apis/base/v3/bases/{base}"
                   f"/tables/{tbl}/records?page_size=100&offset={offset}")
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            field_ids = data["data"].get("field_id_list", [])
            records = data["data"]["data"]
            record_ids = data["data"]["record_id_list"]
            if not records:
                break

            amount_idx = type_idx = text_idx = None
            for i, fid in enumerate(field_ids):
                if fid == amount_fid:
                    amount_idx = i
                elif fid == type_fid:
                    type_idx = i
                elif fid == text_fid:
                    text_idx = i

            if amount_idx is None or type_idx is None or text_idx is None:
                return {"success": False, "error": "飞书字段索引定位失败"}

            for i, rec in enumerate(records):
                if len(rec) > max(amount_idx, type_idx, text_idx):
                    amount_val = rec[amount_idx] if rec[amount_idx] else 0
                    type_raw = rec[type_idx] if rec[type_idx] else ""
                    # 单选框字段返回可能是列表 ['支出'] 或字符串 '支出'
                    type_val = type_raw[0] if isinstance(type_raw, list) else str(type_raw)
                    text_val = str(rec[text_idx]) if rec[text_idx] else ""
                    rec_date = text_val[:10] if text_val else ""  # 从文本前半段取日期
                    if (abs(float(amount_val) - target_amount) < 0.01
                            and type_val == target_type
                            and rec_date == target_date):
                        candidates.append(record_ids[i])

            if len(records) < 100:
                break
            offset += len(records)

        if len(candidates) == 0:
            return {"success": False, "error": "飞书未找到匹配记录（可能被手动删除）"}
        if len(candidates) > 1:
            return {"success": False, "error": f"飞书找到 {len(candidates)} 条匹配记录（日期+金额+类型），数据不一致，拒绝删除"}

        # 唯一匹配，删除
        rid = candidates[0]
        del_url = (f"https://open.feishu.cn/open-apis/base/v3/bases/{base}"
                   f"/tables/{tbl}/records/{rid}")
        del_req = urllib.request.Request(del_url, method="DELETE",
                                         headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(del_req, timeout=15) as resp:
            del_r = json.loads(resp.read())
        if del_r.get("code") == 0:
            return {"success": True, "record_id": rid}
        return {"success": False, "error": f"飞书删除失败: {del_r.get('msg')}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def delete_record(date_str: str, index: int, sync_feishu: bool = True) -> dict:
    """删除指定日期的第 N 条记录，返回操作结果。先删飞书，确认成功后再删本地。"""
    BILLS_DIR.mkdir(parents=True, exist_ok=True)
    file_path = bill_file_path(date_str)
    existing = parse_bill_file(file_path)

    if not existing["records"]:
        return {"success": False, "error": f"{date_str} 没有记录"}
    if index < 1 or index > len(existing["records"]):
        return {"success": False, "error": f"序号 {index} 超出范围（1-{len(existing['records'])}）"}

    # 先找到要删的记录（不动本地文件）
    removed = existing["records"][index - 1]

    # 先删飞书，确认成功后再动本地
    feishu_result = None
    if sync_feishu:
        _check_feishu_config()
        feishu_result = _delete_from_feishu(removed, date_str)
        if not feishu_result["success"]:
            err = feishu_result.get("error", "")
            return {
                "success": False,
                "error": f"飞书删除失败：{err}；本地未删除",
                "deleted": removed,
                "date": date_str,
                "feishu_delete": feishu_result,
            }

    # 飞书确认删除 → 现在删本地
    existing["records"].pop(index - 1)
    if not existing["records"]:
        if file_path.exists():
            file_path.unlink()
    else:
        file_path.write_text(build_bill_content(date_str, existing["records"]), encoding="utf-8")

    total_expense = sum(r["amount"] for r in existing["records"] if r["type"] == "expense")
    total_income = sum(r["amount"] for r in existing["records"] if r["type"] == "income")

    result = {
        "success": True, "deleted": removed, "date": date_str,
        "file": str(file_path) if existing["records"] else "（已删除空文件）",
        "file_exists": file_path.exists(),
        "today_total_expense": round(total_expense, 2),
        "today_total_income": round(total_income, 2),
        "today_net": round(total_income - total_expense, 2),
        "today_count": len(existing["records"]),
    }
    if feishu_result:
        result["feishu_delete"] = feishu_result
    return result


# ── 查询功能 ──────────────────────────────────────────────────────────────

def list_records(date_str: str) -> dict:
    """列出指定日期的所有账单"""
    file_path = bill_file_path(date_str)
    data = parse_bill_file(file_path)
    records = [{"index": i + 1, **r} for i, r in enumerate(data["records"])]
    return {"success": True, "date": date_str, "records": records,
            "total_expense": round(data["total_expense"], 2),
            "total_income": round(data["total_income"], 2),
            "net": round(data["total_income"] - data["total_expense"], 2)}


def get_summary(month: str) -> dict:
    """查询指定月份的汇总数据"""
    month_str = f"# 账单 {month}"
    records = []
    for fpath in sorted(BILLS_DIR.glob("*.md")):
        content = fpath.read_text(encoding="utf-8")
        if month_str in content:
            data = parse_bill_file(fpath)
            records.extend(data["records"])

    total_expense = sum(r["amount"] for r in records if r["type"] == "expense")
    total_income = sum(r["amount"] for r in records if r["type"] == "income")

    # 按分类聚合
    expense_by_cat: dict[str, float] = {}
    income_by_cat: dict[str, float] = {}
    for r in records:
        cat = r["category"]
        if r["type"] == "expense":
            expense_by_cat[cat] = expense_by_cat.get(cat, 0) + r["amount"]
        else:
            income_by_cat[cat] = income_by_cat.get(cat, 0) + r["amount"]

    return {
        "success": True, "month": month,
        "total_expense": round(total_expense, 2),
        "total_income": round(total_income, 2),
        "net": round(total_income - total_expense, 2),
        "count": len(records),
        "expense_by_category": {k: round(v, 2) for k, v in sorted(expense_by_cat.items(), key=lambda x: -x[1])},
        "income_by_category": {k: round(v, 2) for k, v in sorted(income_by_cat.items(), key=lambda x: -x[1])},
    }


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="飞书记账脚本")
    parser.add_argument("--amount", type=float, help="金额")
    parser.add_argument("--type", choices=["expense", "income"], help="类型：支出/收入")
    parser.add_argument("--category", default="其他", help="分类")
    parser.add_argument("--note", default="", help="备注")
    parser.add_argument("--date", default=get_today(), help="日期 YYYY-MM-DD")
    parser.add_argument("--feishu", action="store_true", default=True,
                        help="同步飞书（默认开启）")
    parser.add_argument("--list", action="store_true", help="列出当日账单")
    parser.add_argument("--summary", action="store_true", help="月度汇总")
    parser.add_argument("--month", help="汇总月份 YYYY-MM（默认本月）")
    parser.add_argument("--delete", action="store_true", help="删除记录（需配合 --date 和 --index）")
    parser.add_argument("--index", type=int, help="要删除的记录序号（配合 --delete 使用，1起算）")
    args = parser.parse_args()

    if args.summary:
        month = args.month or get_today()[:7]
        result = get_summary(month)
        print(json.dumps(result, ensure_ascii=False))
        return

    if args.list:
        result = list_records(args.date)
        print(json.dumps(result, ensure_ascii=False))
        return

    if args.delete:
        if not args.index:
            parser.error("删除记录需要 --index 参数指定序号（1起算）")
        result = delete_record(args.date, args.index, sync_feishu=args.feishu)
        print(json.dumps(result, ensure_ascii=False))
        return

    if not args.amount or not args.type:
        parser.error("需要 --amount 和 --type 参数")

    result = add_record(args.amount, args.type, args.category,
                        args.note, args.date, sync_feishu=args.feishu)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
