from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path
from zipfile import ZipFile


@dataclass
class Transaction:
    platform: str
    timestamp: datetime
    raw_category: str
    merchant: str
    item: str
    direction: str
    amount: float
    payment_method: str
    status: str
    note: str
    scene: str = ""
    tag: str = ""
    habit_excluded_reason: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a local HTML spending report from Alipay and WeChat bills.")
    parser.add_argument("--input-dir", type=Path, default=Path.cwd(), help="Directory used to auto-discover native bill files")
    parser.add_argument("--alipay", type=Path, default=None, help="Path to the Alipay CSV bill")
    parser.add_argument("--wechat", type=Path, default=None, help="Path to the WeChat XLSX bill")
    parser.add_argument("--output", type=Path, default=None, help="Output HTML path")
    parser.add_argument("--open", action="store_true", help="Open the generated HTML report after writing it")
    return parser.parse_args()


def discover_bill_file(base_dir: Path, patterns: list[str]) -> Path | None:
    matches: list[Path] = []
    for pattern in patterns:
        matches.extend(candidate for candidate in base_dir.rglob(pattern) if candidate.is_file())
    if not matches:
        return None
    unique_matches = sorted({candidate.resolve() for candidate in matches}, key=lambda candidate: candidate.stat().st_mtime, reverse=True)
    return unique_matches[0]


def resolve_inputs(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    input_dir = args.input_dir.expanduser().resolve()
    alipay_path = args.alipay.expanduser().resolve() if args.alipay else discover_bill_file(input_dir, ["支付宝交易明细*.csv", "*支付宝*交易*.csv"])
    wechat_path = args.wechat.expanduser().resolve() if args.wechat else discover_bill_file(input_dir, ["微信支付账单流水文件*.xlsx", "*微信支付*账单*.xlsx", "*微信*账单*.xlsx"])

    if alipay_path is None:
        raise FileNotFoundError(f"未找到支付宝原生账单 CSV。请在 {input_dir} 下放入‘支付宝交易明细*.csv’，或显式传入 --alipay。")
    if wechat_path is None:
        zip_candidate = discover_bill_file(input_dir, ["微信支付账单流水文件*.zip", "*微信支付*账单*.zip", "*微信*账单*.zip"])
        if zip_candidate is not None:
            raise FileNotFoundError(
                "未找到可解析的微信 XLSX 账单，但发现了微信 ZIP。微信 ZIP 通常带密码，"
                f"请先在本地解压出 .xlsx 后重试：{zip_candidate}"
            )
        raise FileNotFoundError(f"未找到微信原生账单 XLSX。请在 {input_dir} 下放入‘微信支付账单流水文件*.xlsx’，或显式传入 --wechat。")

    if args.output:
        output_path = args.output.expanduser().resolve()
    else:
        output_path = input_dir / "reports" / "spending_report.html"

    return alipay_path, wechat_path, output_path


def parse_alipay(path: Path) -> list[Transaction]:
    with path.open("r", encoding="gb18030", newline="") as file:
        lines = file.readlines()

    header_index = next(index for index, line in enumerate(lines) if line.startswith("交易时间,交易分类,交易对方"))
    reader = csv.DictReader(lines[header_index:])
    rows: list[Transaction] = []

    for row in reader:
        if not row.get("交易时间"):
            continue
        rows.append(
            Transaction(
                platform="支付宝",
                timestamp=datetime.strptime(row["交易时间"].strip(), "%Y-%m-%d %H:%M:%S"),
                raw_category=row.get("交易分类", "").strip(),
                merchant=row.get("交易对方", "").strip(),
                item=row.get("商品说明", "").strip(),
                direction=row.get("收/支", "").strip(),
                amount=float(str(row.get("金额", "0")).replace(",", "") or 0),
                payment_method=row.get("收/付款方式", "").strip(),
                status=row.get("交易状态", "").strip(),
                note=row.get("备注", "").strip(),
            )
        )

    return rows


def column_index(cell_reference: str) -> int:
    letters = "".join(character for character in cell_reference if character.isalpha())
    index = 0
    for character in letters:
        index = index * 26 + ord(character.upper()) - 64
    return index - 1


def parse_wechat(path: Path) -> list[Transaction]:
    namespace = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(path) as workbook:
        shared_root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
        shared_strings = [
            "".join(text.text or "" for text in item.iterfind(".//a:t", namespace))
            for item in shared_root.findall("a:si", namespace)
        ]
        sheet_root = ET.fromstring(workbook.read("xl/worksheets/sheet1.xml"))

    table: list[list[str]] = []
    for row in sheet_root.findall(".//a:sheetData/a:row", namespace):
        values: dict[int, str] = {}
        for cell in row.findall("a:c", namespace):
            raw_value = cell.find("a:v", namespace)
            cell_type = cell.attrib.get("t")
            if raw_value is None:
                value = ""
            elif cell_type == "s":
                value = shared_strings[int(raw_value.text)]
            else:
                value = raw_value.text or ""
            values[column_index(cell.attrib["r"])] = value
        if values:
            current_row = [""] * (max(values) + 1)
            for key, value in values.items():
                current_row[key] = value
            table.append(current_row)

    header = ["交易时间", "交易类型", "交易对方", "商品", "收/支", "金额(元)", "支付方式", "当前状态", "交易单号", "商户单号", "备注"]
    header_index = next(index for index, row in enumerate(table) if row[: len(header)] == header)
    rows: list[Transaction] = []

    for row in table[header_index + 1 :]:
        if len(row) < 10 or not row[0]:
            continue
        if len(row[0]) < 19:
            continue
        rows.append(
            Transaction(
                platform="微信",
                timestamp=datetime.strptime(row[0].strip(), "%Y-%m-%d %H:%M:%S"),
                raw_category=row[1].strip(),
                merchant=row[2].strip(),
                item=row[3].strip(),
                direction=row[4].strip(),
                amount=float(str(row[5]).replace("¥", "").replace(",", "") or 0),
                payment_method=row[6].strip(),
                status=row[7].strip(),
                note=row[10].strip() if len(row) > 10 else "",
            )
        )

    return rows


def keep_spend(transaction: Transaction) -> bool:
    if transaction.direction != "支出":
        return False
    if transaction.platform == "支付宝":
        return transaction.status in {"交易成功", "等待确认收货"}
    return transaction.status not in {"已全额退款", "转账已退还", "已关闭"}


def classify_scene(transaction: Transaction) -> tuple[str, str]:
    text = " ".join([transaction.raw_category, transaction.merchant, transaction.item, transaction.note]).lower()

    if "缴税" in text or "个人所得税" in text:
        return "税费", "non_habit"
    if "房租" in text:
        return "房租", "non_habit"
    if any(keyword in text for keyword in ["铭品装饰", "设计师", "一期款"]):
        return "装修/家居", "non_habit"
    if any(keyword in text for keyword in ["转账", "红包", "小荷包", "群收款", "二维码收款"]):
        return "转账/社交往来", "non_habit"
    if any(keyword in text for keyword in ["北大湖", "滑雪", "雪湖居", "松花湖", "农家院", "云上草原", "滑呗"]):
        return "旅行/滑雪", "non_routine"
    if any(keyword in text for keyword in ["电费", "燃气", "水费", "供电局", "水务"]):
        return "居家账单", "routine"
    if any(keyword in text for keyword in ["停车", "打车", "地铁", "公交", "高速", "龙嘉机场", "高铁北站"]):
        return "通勤出行", "routine"
    if any(keyword in text for keyword in ["阿里云", "codex", "claude", "brave", "gemini", "百炼", "trae", "源码跳动"]):
        if transaction.amount >= 1000:
            return "AI/云工具", "non_routine"
        return "AI/云工具", "routine"
    if any(keyword in text for keyword in ["app store", "apple music", "todesk"]):
        return "数字订阅", "routine"
    if any(keyword in text for keyword in ["山姆", "盒马"]):
        return "商超采购", "routine"
    if any(keyword in text for keyword in ["citybox", "魔盒", "咖啡", "茶姬", "虎憩", "爷爷不泡茶", "好利来", "茶事", "烧饼"]):
        return "咖啡零食", "routine"
    if any(keyword in text for keyword in ["东郊到家", "嘉惠健康", "可儿健康", "共享健康椅"]):
        if transaction.amount >= 300:
            return "到家/健康服务", "non_routine"
        return "到家/健康服务", "routine"
    if any(keyword in text for keyword in ["莱茵体育", "体育生活馆"]):
        return "运动健身", "routine"
    if any(keyword in text for keyword in ["nike", "路由器", "保湿特润霜", "订单x", "日用百货", "数码电器", "自动发货", "北京弘盛铭达"]):
        if transaction.amount >= 1000:
            return "电商购物/装备", "non_routine"
        return "电商购物/装备", "routine"
    if any(keyword in text for keyword in ["电信", "话费"]):
        return "通讯充值", "routine"
    if any(keyword in text for keyword in ["寄件", "物流", "顺丰", "德邦"]):
        return "物流寄件", "routine"
    if any(keyword in text for keyword in ["洗车", "洗衣", "充电宝", "自助充值"]):
        return "生活服务", "routine"
    if transaction.raw_category == "餐饮美食" or any(keyword in text for keyword in ["容桂婆", "华饮会", "拉面", "饭", "面", "小吃"]):
        return "正餐餐饮", "routine"
    if transaction.raw_category == "医疗健康" or any(keyword in text for keyword in ["博士伦", "药店", "医院", "门诊"]):
        return "医疗健康", "routine"
    if transaction.amount >= 1000:
        return "线下其他消费", "non_routine"
    return "线下其他消费", "routine"


def annotate_transactions(transactions: list[Transaction]) -> None:
    for transaction in transactions:
        transaction.scene, transaction.tag = classify_scene(transaction)
        if transaction.scene in {"税费", "房租", "装修/家居", "转账/社交往来"}:
            transaction.habit_excluded_reason = transaction.scene
        elif transaction.scene in {"旅行/滑雪"}:
            transaction.habit_excluded_reason = "旅行/滑雪"
        elif transaction.amount >= 1000:
            transaction.habit_excluded_reason = "单笔>=1000的一次性大额项目"
        elif transaction.tag == "non_routine":
            transaction.habit_excluded_reason = "非日常项目"


def money(value: float) -> str:
    return f"¥{value:,.2f}"


def round2(value: float) -> float:
    return round(value + 1e-9, 2)


def percentage(value: float, total: float) -> float:
    if total == 0:
        return 0.0
    return round(value * 100 / total, 1)


def sum_amount(transactions: list[Transaction]) -> float:
    return round2(sum(transaction.amount for transaction in transactions))


def date_range(start: date, end: date) -> list[str]:
    current = start
    output: list[str] = []
    while current <= end:
        output.append(current.isoformat())
        current += timedelta(days=1)
    return output


def aggregate(transactions: list[Transaction], key_getter) -> list[dict[str, object]]:
    amounts: dict[str, float] = defaultdict(float)
    counts: Counter[str] = Counter()
    for transaction in transactions:
        key = key_getter(transaction)
        amounts[key] += transaction.amount
        counts[key] += 1
    return [
        {
            "label": label,
            "amount": round2(amount),
            "count": counts[label],
        }
        for label, amount in sorted(amounts.items(), key=lambda item: (-item[1], -counts[item[0]], item[0]))
    ]


def build_daily_series(transactions: list[Transaction], start: date, end: date) -> list[dict[str, object]]:
    totals: dict[str, float] = defaultdict(float)
    counts: Counter[str] = Counter()
    for transaction in transactions:
        day = transaction.timestamp.date().isoformat()
        totals[day] += transaction.amount
        counts[day] += 1
    return [
        {"date": day, "amount": round2(totals.get(day, 0.0)), "count": counts.get(day, 0)}
        for day in date_range(start, end)
    ]


def build_weekday_series(transactions: list[Transaction]) -> list[dict[str, object]]:
    names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    amounts: dict[int, float] = defaultdict(float)
    counts: Counter[int] = Counter()
    for transaction in transactions:
        weekday = transaction.timestamp.weekday()
        amounts[weekday] += transaction.amount
        counts[weekday] += 1
    return [
        {"label": names[index], "amount": round2(amounts.get(index, 0.0)), "count": counts.get(index, 0)}
        for index in range(7)
    ]


def build_time_bucket_series(transactions: list[Transaction]) -> list[dict[str, object]]:
    labels = ["深夜", "早晨", "午间", "下午", "晚上"]
    amounts: dict[str, float] = defaultdict(float)
    counts: Counter[str] = Counter()
    for transaction in transactions:
        hour = transaction.timestamp.hour
        if 0 <= hour < 5:
            bucket = "深夜"
        elif 5 <= hour < 11:
            bucket = "早晨"
        elif 11 <= hour < 14:
            bucket = "午间"
        elif 14 <= hour < 18:
            bucket = "下午"
        else:
            bucket = "晚上"
        amounts[bucket] += transaction.amount
        counts[bucket] += 1
    return [
        {"label": label, "amount": round2(amounts.get(label, 0.0)), "count": counts.get(label, 0)}
        for label in labels
    ]


def build_month_series(transactions: list[Transaction]) -> list[dict[str, object]]:
    return aggregate(transactions, lambda transaction: transaction.timestamp.strftime("%Y-%m"))


def build_heatmap(transactions: list[Transaction]) -> list[list[dict[str, object]]]:
    row_labels = ["深夜", "早晨", "午间", "下午", "晚上"]
    col_labels = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    totals: dict[tuple[str, int], float] = defaultdict(float)
    counts: Counter[tuple[str, int]] = Counter()
    for transaction in transactions:
        hour = transaction.timestamp.hour
        if hour < 5:
            row_label = "深夜"
        elif hour < 11:
            row_label = "早晨"
        elif hour < 14:
            row_label = "午间"
        elif hour < 18:
            row_label = "下午"
        else:
            row_label = "晚上"
        column_index = transaction.timestamp.weekday()
        totals[(row_label, column_index)] += transaction.amount
        counts[(row_label, column_index)] += 1
    matrix: list[list[dict[str, object]]] = []
    for row_label in row_labels:
        row_items: list[dict[str, object]] = []
        for column_index, column_label in enumerate(col_labels):
            row_items.append(
                {
                    "row": row_label,
                    "col": column_label,
                    "amount": round2(totals.get((row_label, column_index), 0.0)),
                    "count": counts.get((row_label, column_index), 0),
                }
            )
        matrix.append(row_items)
    return matrix


def build_recurring_merchants(transactions: list[Transaction]) -> list[dict[str, object]]:
    stats: dict[str, dict[str, object]] = defaultdict(lambda: {"amount": 0.0, "count": 0, "days": set(), "scene": ""})
    for transaction in transactions:
        entry = stats[transaction.merchant]
        entry["amount"] = float(entry["amount"]) + transaction.amount
        entry["count"] = int(entry["count"]) + 1
        entry["scene"] = transaction.scene
        cast_days = entry["days"]
        if isinstance(cast_days, set):
            cast_days.add(transaction.timestamp.date().isoformat())
    rows: list[dict[str, object]] = []
    for merchant, entry in stats.items():
        days = entry["days"]
        if isinstance(days, set) and int(entry["count"]) >= 3 and len(days) >= 3:
            rows.append(
                {
                    "merchant": merchant,
                    "scene": entry["scene"],
                    "amount": round2(float(entry["amount"])),
                    "count": int(entry["count"]),
                    "days": len(days),
                }
            )
    rows.sort(key=lambda row: (-float(row["amount"]), -int(row["count"]), str(row["merchant"])))
    return rows[:12]


def build_pool(transactions: list[Transaction], start: date, end: date) -> dict[str, object]:
    total_amount = sum_amount(transactions)
    daily_series = build_daily_series(transactions, start, end)
    active_daily_amounts = [float(item["amount"]) for item in daily_series if float(item["amount"]) > 0]
    spend_days = sum(1 for item in daily_series if float(item["amount"]) > 0)
    top_categories = aggregate(transactions, lambda transaction: transaction.scene)[:10]
    top_merchants = aggregate(transactions, lambda transaction: transaction.merchant)[:12]
    payment_methods = aggregate(transactions, lambda transaction: transaction.payment_method or "未标注")[:8]
    top_transactions = [
        {
            "date": transaction.timestamp.strftime("%Y-%m-%d %H:%M"),
            "amount": round2(transaction.amount),
            "scene": transaction.scene,
            "merchant": transaction.merchant,
            "item": transaction.item,
            "platform": transaction.platform,
            "status": transaction.status,
        }
        for transaction in sorted(transactions, key=lambda item: (-item.amount, item.timestamp))[:12]
    ]
    weekend_amount = round2(sum(transaction.amount for transaction in transactions if transaction.timestamp.weekday() >= 5))
    weekday_amount = round2(sum(transaction.amount for transaction in transactions if transaction.timestamp.weekday() < 5))

    return {
        "total": total_amount,
        "count": len(transactions),
        "average_ticket": round2(total_amount / len(transactions)) if transactions else 0.0,
        "daily_mean": round2(sum(active_daily_amounts) / len(active_daily_amounts)) if active_daily_amounts else 0.0,
        "daily_median": round2(statistics.median(active_daily_amounts)) if active_daily_amounts else 0.0,
        "spend_days": spend_days,
        "spend_day_ratio": round(100 * spend_days / len(daily_series), 1) if daily_series else 0.0,
        "weekend_amount": weekend_amount,
        "weekday_amount": weekday_amount,
        "weekend_share": percentage(weekend_amount, total_amount),
        "weekday_share": percentage(weekday_amount, total_amount),
        "top_categories": top_categories,
        "top_merchants": top_merchants,
        "payment_methods": payment_methods,
        "monthly": build_month_series(transactions),
        "weekday": build_weekday_series(transactions),
        "time_bucket": build_time_bucket_series(transactions),
        "daily": daily_series,
        "heatmap": build_heatmap(transactions),
        "recurring_merchants": build_recurring_merchants(transactions),
        "top_transactions": top_transactions,
    }


def build_insights(all_transactions: list[Transaction], consumption: list[Transaction], habit: list[Transaction], span_days: int) -> list[dict[str, str]]:
    all_total = sum_amount(all_transactions)
    habit_total = sum_amount(habit)
    housing_total = sum_amount([transaction for transaction in all_transactions if transaction.scene in {"房租", "装修/家居", "居家账单"}])
    tax_total = sum_amount([transaction for transaction in all_transactions if transaction.scene == "税费"])
    transfer_total = sum_amount([transaction for transaction in all_transactions if transaction.scene == "转账/社交往来"])
    small_transactions = [transaction for transaction in habit if transaction.amount <= 20]
    small_total = sum_amount(small_transactions)
    digital_total = sum_amount([transaction for transaction in consumption if transaction.scene in {"AI/云工具", "数字订阅"}])
    coffee_total = sum_amount([transaction for transaction in habit if transaction.scene == "咖啡零食"])
    shopping_total = sum_amount([transaction for transaction in consumption if transaction.scene == "电商购物/装备"])
    monthly_habit_run_rate = round2(habit_total / span_days * 30.4)
    monthly_digital_run_rate = round2(digital_total / span_days * 30.4)

    return [
        {
            "title": "你不是“被咖啡拖垮”型，真正的大头是项目型支出",
            "body": f"全部支出里，居住相关（房租+装修+居家账单）合计 {money(housing_total)}，税费 {money(tax_total)}，转账/往来 {money(transfer_total)}。这些远大于零碎吃喝，说明你的问题不在拿铁，而在大项目管理。",
        },
        {
            "title": "习惯池更接近日常真实消费",
            "body": f"把税费、转账、房租、装修、旅行和单笔大额项目剔除后，习惯池支出是 {money(habit_total)}，折合月均约 {money(monthly_habit_run_rate)}。这部分才是最值得优化的日常行为层。",
        },
        {
            "title": "小额高频很明显，但金额不算失控",
            "body": f"习惯池里单笔不超过 20 元的交易共有 {len(small_transactions)} 笔，合计 {money(small_total)}。其中咖啡零食类合计 {money(coffee_total)}，更像频繁补给而不是金额爆炸。",
        },
        {
            "title": "数字工具/订阅是值得设上限的第二战场",
            "body": f"AI/云工具和数字订阅合计 {money(digital_total)}，按当前周期折算月均约 {money(monthly_digital_run_rate)}。如果这些里有试用、重复开通或工作费用未报销，优化空间会比省奶茶更大。",
        },
        {
            "title": "购物/装备支出集中爆发，不是均匀渗透",
            "body": f"电商购物/装备合计 {money(shopping_total)}，明显集中在 1 月的装备采购和少数大额单笔，说明更适合上“冷静期”而不是天天记流水。",
        },
    ]


def build_optimizations(all_transactions: list[Transaction], consumption: list[Transaction], habit: list[Transaction], span_days: int) -> list[dict[str, str]]:
    small_discretionary = [
        transaction
        for transaction in habit
        if transaction.amount <= 20 and transaction.scene in {"咖啡零食", "线下其他消费", "生活服务", "正餐餐饮"}
    ]
    small_discretionary_monthly = round2(sum_amount(small_discretionary) / span_days * 30.4)
    digital_transactions = [transaction for transaction in consumption if transaction.scene in {"AI/云工具", "数字订阅"}]
    digital_monthly = round2(sum_amount(digital_transactions) / span_days * 30.4)
    gear_transactions = [
        transaction
        for transaction in consumption
        if transaction.scene in {"电商购物/装备", "到家/健康服务", "线下其他消费"} and transaction.amount >= 300
    ]
    gear_monthly = round2(sum_amount(gear_transactions) / span_days * 30.4)
    routine_total_monthly = round2(sum_amount(habit) / span_days * 30.4)

    return [
        {
            "action": "给零碎非必要消费做每周封顶",
            "why": f"可变动的小额消费折算月均约 {money(small_discretionary_monthly)}，压缩 30% 也不会明显影响生活体验。",
            "impact": f"预计每月可省 {money(round2(small_discretionary_monthly * 0.3))}",
            "how": "把咖啡/零食/充电宝/临时小买卖设成一周一个总额度，用完就停。",
        },
        {
            "action": "给 AI 工具和订阅设总预算",
            "why": f"AI/云工具 + 数字订阅折算月均约 {money(digital_monthly)}，而且存在多渠道分散付费。",
            "impact": f"若月上限压到 ¥700，预计每月可省 {money(max(round2(digital_monthly - 700), 0))}",
            "how": "分成“工作必需 / 尝鲜试用 / 可替代”三栏，每月底只保留真正常用的。",
        },
        {
            "action": "为 300 元以上的非刚需消费加 48 小时冷静期",
            "why": f"中高额可选消费折算月均约 {money(gear_monthly)}，集中于装备、到家服务和少数线下大额。",
            "impact": f"保守按 10% 避免冲动单估算，每月可省 {money(round2(gear_monthly * 0.1))}",
            "how": "把想买的先放进备忘录，48 小时后再下单；仍然想买再付款。",
        },
        {
            "action": "把转账、房租、装修与个人消费彻底分账",
            "why": f"全部流出里，非日常大项远高于日常习惯池；混在一起会掩盖真实消费结构。",
            "impact": f"不是直接省钱，但能把真正可优化的月均消费固定在约 {money(routine_total_monthly)} 这个量级上看。",
            "how": "至少拆成“生活固定支出 / 工作投入 / 日常消费 / 社交往来”四本账。",
        },
    ]


def build_summary_cards(all_transactions: list[Transaction], consumption: list[Transaction], habit: list[Transaction], span_days: int) -> list[dict[str, object]]:
    all_total = sum_amount(all_transactions)
    consumption_total = sum_amount(consumption)
    habit_total = sum_amount(habit)
    return [
        {
            "label": "账户总流出",
            "value": all_total,
            "description": "所有有效支出，包含税费、房租、装修、转账与日常消费。",
            "share": 100.0,
        },
        {
            "label": "消费型支出",
            "value": consumption_total,
            "description": "从总流出中剔除税费与纯转账后，更接近真正消费。",
            "share": percentage(consumption_total, all_total),
        },
        {
            "label": "习惯池",
            "value": habit_total,
            "description": f"从消费型支出中再剔除房租、装修、旅行与单笔>=1000 的一次性项目；折算月均约 {money(round2(habit_total / span_days * 30.4))}。",
            "share": percentage(habit_total, all_total),
        },
    ]


def build_exclusion_table(consumption: list[Transaction]) -> list[dict[str, object]]:
    excluded = [transaction for transaction in consumption if transaction.habit_excluded_reason]
    rows = [
        {
            "date": transaction.timestamp.strftime("%Y-%m-%d %H:%M"),
            "reason": transaction.habit_excluded_reason,
            "amount": round2(transaction.amount),
            "scene": transaction.scene,
            "merchant": transaction.merchant,
            "item": transaction.item,
            "platform": transaction.platform,
        }
        for transaction in sorted(excluded, key=lambda item: (-item.amount, item.timestamp))[:16]
    ]
    return rows


def build_report_payload(transactions: list[Transaction], alipay_path: Path, wechat_path: Path) -> dict[str, object]:
    annotate_transactions(transactions)
    start_date = min(transaction.timestamp.date() for transaction in transactions)
    end_date = max(transaction.timestamp.date() for transaction in transactions)
    span_days = (end_date - start_date).days + 1

    all_pool = transactions
    consumption_pool = [transaction for transaction in transactions if transaction.scene not in {"税费", "转账/社交往来"}]
    habit_pool = [
        transaction
        for transaction in consumption_pool
        if transaction.scene not in {"房租", "装修/家居", "旅行/滑雪"} and transaction.amount < 1000
    ]

    all_metrics = build_pool(all_pool, start_date, end_date)
    consumption_metrics = build_pool(consumption_pool, start_date, end_date)
    habit_metrics = build_pool(habit_pool, start_date, end_date)
    summary_cards = build_summary_cards(all_pool, consumption_pool, habit_pool, span_days)
    insights = build_insights(all_pool, consumption_pool, habit_pool, span_days)
    optimizations = build_optimizations(all_pool, consumption_pool, habit_pool, span_days)

    overall_top_transactions = [
        {
            "date": transaction.timestamp.strftime("%Y-%m-%d %H:%M"),
            "amount": round2(transaction.amount),
            "scene": transaction.scene,
            "merchant": transaction.merchant,
            "item": transaction.item,
            "platform": transaction.platform,
        }
        for transaction in sorted(all_pool, key=lambda item: (-item.amount, item.timestamp))[:18]
    ]

    source_breakdown = aggregate(all_pool, lambda transaction: transaction.platform)
    outlier_count = len([transaction for transaction in all_pool if transaction.amount >= 1000])
    small_count = len([transaction for transaction in habit_pool if transaction.amount <= 20])
    small_total = sum_amount([transaction for transaction in habit_pool if transaction.amount <= 20])
    digital_total = sum_amount([transaction for transaction in consumption_pool if transaction.scene in {"AI/云工具", "数字订阅"}])

    return {
        "title": "2026 年个人消费习惯分析报告",
        "subtitle": "基于支付宝 + 微信账单生成的本地自包含可视化页面",
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
            "days": span_days,
        },
        "sources": [str(alipay_path), str(wechat_path)],
        "summary_cards": summary_cards,
        "headline": {
            "all_total": sum_amount(all_pool),
            "consumption_total": sum_amount(consumption_pool),
            "habit_total": sum_amount(habit_pool),
            "outlier_count": outlier_count,
            "small_count": small_count,
            "small_total": small_total,
            "digital_total": digital_total,
            "platform_split": source_breakdown,
        },
        "methodology": [
            "仅统计支付宝与微信账单中的有效支出；已排除退款关闭单与非支出记录。",
            "消费型支出 = 全部支出 - 税费 - 纯转账/红包/小荷包/群收款等往来。",
            "习惯池 = 消费型支出 - 房租 - 装修/家居 - 旅行/滑雪 - 单笔 >= 1000 的一次性项目。",
            "习惯优化建议主要依据习惯池，不把税费、装修、房租误判为日常坏习惯。",
        ],
        "pools": {
            "all": {
                "name": "账户总流出",
                "description": "看现金流全貌，适合判断大项支出压在哪里。",
                **all_metrics,
            },
            "consumption": {
                "name": "消费型支出",
                "description": "剔除税费和纯转账后，更像“花出去的消费”。",
                **consumption_metrics,
            },
            "habit": {
                "name": "习惯池",
                "description": "剔除非日常大项后，更适合优化消费习惯。",
                **habit_metrics,
            },
        },
        "insights": insights,
        "optimizations": optimizations,
        "exclusion_table": build_exclusion_table(consumption_pool),
        "overall_top_transactions": overall_top_transactions,
    }


def html_template(payload_json: str) -> str:
    template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>个人消费习惯分析报告</title>
  <style>
    :root {{
      --bg: #0b1020;
      --panel: #121a2f;
      --panel-2: #18233f;
      --text: #eef4ff;
      --muted: #9fb0d0;
      --accent: #70e1ff;
      --accent-2: #7c89ff;
      --good: #59d98e;
      --warn: #ffbf5f;
      --bad: #ff8f8f;
      --border: rgba(255,255,255,0.09);
      --shadow: 0 18px 60px rgba(0,0,0,0.28);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Helvetica Neue", sans-serif;
      background:
        radial-gradient(circle at top right, rgba(124,137,255,0.18), transparent 30%),
        radial-gradient(circle at left top, rgba(112,225,255,0.14), transparent 28%),
        linear-gradient(180deg, #0b1020 0%, #11192d 100%);
      color: var(--text);
      line-height: 1.6;
    }}
    .container {{ max-width: 1440px; margin: 0 auto; padding: 32px 24px 64px; }}
    .hero {{ display: grid; grid-template-columns: 1.35fr 1fr; gap: 20px; margin-bottom: 20px; }}
    .panel {{
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
      border: 1px solid var(--border);
      border-radius: 20px;
      box-shadow: var(--shadow);
      padding: 22px;
      backdrop-filter: blur(14px);
    }}
    .hero h1 {{ font-size: 34px; margin: 0 0 10px; line-height: 1.2; }}
    .hero p {{ margin: 0; color: var(--muted); }}
    .hero-meta {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border);
      color: var(--text);
      font-size: 13px;
    }}
    .summary-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 20px 0; }}
    .summary-card h3 {{ margin: 0 0 8px; font-size: 16px; }}
    .summary-card .value {{ font-size: 34px; font-weight: 700; line-height: 1.1; margin-bottom: 8px; }}
    .summary-card p {{ margin: 0; color: var(--muted); font-size: 14px; }}
    .summary-card .share {{ color: var(--accent); margin-top: 10px; font-size: 13px; }}
    .method-list {{ margin: 0; padding-left: 18px; color: var(--muted); font-size: 14px; }}
    .method-list li + li {{ margin-top: 6px; }}
    .section-title {{ display: flex; justify-content: space-between; align-items: end; gap: 16px; margin: 30px 0 14px; }}
    .section-title h2 {{ margin: 0; font-size: 24px; }}
    .section-title p {{ margin: 0; color: var(--muted); }}
    .toggle-row {{ display: flex; gap: 10px; flex-wrap: wrap; }}
    .toggle-button {{
      appearance: none;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.03);
      color: var(--text);
      border-radius: 999px;
      padding: 10px 16px;
      cursor: pointer;
      transition: 0.2s ease;
      font-size: 14px;
    }}
    .toggle-button.active {{ background: linear-gradient(135deg, rgba(112,225,255,0.22), rgba(124,137,255,0.25)); border-color: rgba(112,225,255,0.35); }}
    .metric-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-bottom: 18px; }}
    .metric {{ padding: 16px; border-radius: 18px; background: var(--panel); border: 1px solid var(--border); }}
    .metric .label {{ color: var(--muted); font-size: 13px; margin-bottom: 8px; }}
    .metric .value {{ font-size: 24px; font-weight: 700; line-height: 1.15; }}
    .metric .sub {{ color: var(--muted); font-size: 12px; margin-top: 6px; }}
    .chart-grid {{ display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 16px; }}
    .chart-panel {{ background: var(--panel); border: 1px solid var(--border); border-radius: 20px; padding: 18px; min-height: 320px; }}
    .chart-panel h3 {{ margin: 0 0 4px; font-size: 18px; }}
    .chart-panel p {{ margin: 0 0 14px; color: var(--muted); font-size: 13px; }}
    .bar-list {{ display: grid; gap: 12px; }}
    .bar-item {{ display: grid; gap: 7px; }}
    .bar-meta {{ display: flex; justify-content: space-between; gap: 10px; font-size: 13px; }}
    .bar-track {{ height: 12px; border-radius: 999px; background: rgba(255,255,255,0.06); overflow: hidden; }}
    .bar-fill {{ height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); }}
    .mini-bars {{ display: flex; align-items: end; gap: 10px; min-height: 220px; padding-top: 18px; }}
    .mini-bar-wrap {{ flex: 1; display: grid; gap: 10px; justify-items: center; }}
    .mini-bar {{ width: 100%; max-width: 52px; border-radius: 14px 14px 4px 4px; background: linear-gradient(180deg, rgba(112,225,255,0.95), rgba(124,137,255,0.68)); }}
    .mini-label {{ font-size: 12px; color: var(--muted); text-align: center; }}
    .mini-value {{ font-size: 11px; color: var(--text); opacity: 0.85; }}
    .line-svg {{ width: 100%; height: 260px; display: block; }}
    .grid-two {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 16px; }}
    .insight-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }}
    .insight-card {{ background: var(--panel); border: 1px solid var(--border); border-radius: 18px; padding: 18px; }}
    .insight-card h3 {{ margin: 0 0 8px; font-size: 17px; }}
    .insight-card p {{ margin: 0; color: var(--muted); font-size: 14px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th, td {{ padding: 12px 10px; border-bottom: 1px solid rgba(255,255,255,0.08); vertical-align: top; text-align: left; }}
    th {{ color: var(--muted); font-weight: 600; }}
    td {{ color: var(--text); }}
    .table-panel {{ background: var(--panel); border: 1px solid var(--border); border-radius: 20px; padding: 10px 18px 18px; overflow: auto; }}
    .heatmap {{ display: grid; grid-template-columns: 84px repeat(7, 1fr); gap: 8px; align-items: center; }}
    .heat-label {{ color: var(--muted); font-size: 12px; text-align: center; }}
    .heat-cell {{ height: 44px; border-radius: 12px; display: grid; place-items: center; font-size: 11px; color: #fff; border: 1px solid rgba(255,255,255,0.05); }}
    .pill {{ display: inline-block; padding: 4px 8px; border-radius: 999px; background: rgba(112,225,255,0.12); color: var(--accent); font-size: 12px; }}
    .footer-note {{ margin-top: 18px; color: var(--muted); font-size: 12px; }}
    .wide {{ margin-top: 16px; }}
    @media (max-width: 1180px) {{
      .hero, .chart-grid, .grid-two, .insight-grid {{ grid-template-columns: 1fr; }}
      .summary-grid {{ grid-template-columns: 1fr; }}
      .metric-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    @media (max-width: 720px) {{
      .container {{ padding: 20px 14px 48px; }}
      .hero h1 {{ font-size: 28px; }}
      .metric-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <section class="hero">
      <div class="panel">
        <h1 id="title"></h1>
        <p id="subtitle"></p>
        <div class="hero-meta" id="heroMeta"></div>
      </div>
      <div class="panel">
        <div class="section-title" style="margin: 0 0 12px; align-items: start;">
          <div>
            <h2 style="font-size: 20px;">口径说明</h2>
            <p>报告里同时保留全貌、消费和习惯三个视角。</p>
          </div>
        </div>
        <ul class="method-list" id="methodList"></ul>
      </div>
    </section>

    <section class="summary-grid" id="summaryGrid"></section>

    <section>
      <div class="section-title">
        <div>
          <h2>主仪表盘</h2>
          <p id="poolDescription"></p>
        </div>
        <div class="toggle-row" id="poolToggle"></div>
      </div>

      <div class="metric-grid" id="metricGrid"></div>

      <div class="chart-grid">
        <div class="chart-panel">
          <h3>分类结构</h3>
          <p>按当前口径查看金额最大的消费场景。</p>
          <div id="categoryChart"></div>
        </div>
        <div class="chart-panel">
          <h3>月度走势</h3>
          <p>看 2026-01 到 2026-03 的金额重心怎么变化。</p>
          <div id="monthChart"></div>
        </div>
      </div>

      <div class="grid-two wide">
        <div class="chart-panel">
          <h3>每日支出曲线</h3>
          <p>横轴为日期，纵轴为当日总支出，用于识别尖峰日。</p>
          <svg class="line-svg" id="dailyLine"></svg>
        </div>
        <div class="chart-panel">
          <h3>支付方式</h3>
          <p>看你主要把钱从哪张卡、哪个钱包里花出去。</p>
          <div id="paymentChart"></div>
        </div>
      </div>

      <div class="grid-two wide">
        <div class="chart-panel">
          <h3>星期分布</h3>
          <p>看消费更偏工作日还是周末。</p>
          <div id="weekdayChart"></div>
        </div>
        <div class="chart-panel">
          <h3>时段分布</h3>
          <p>看支出更容易发生在深夜、午间还是晚上。</p>
          <div id="timeChart"></div>
        </div>
      </div>

      <div class="grid-two wide">
        <div class="chart-panel">
          <h3>商户集中度</h3>
          <p>看哪些商户最容易成为你的主要花钱入口。</p>
          <div id="merchantChart"></div>
        </div>
        <div class="chart-panel">
          <h3>星期 × 时段热力图</h3>
          <p>颜色越亮，代表该时段累计支出越高。</p>
          <div id="heatmap"></div>
        </div>
      </div>
    </section>

    <section>
      <div class="section-title">
        <div>
          <h2>习惯诊断</h2>
          <p>这部分回答“你的钱是怎么花的”，不是只列流水。</p>
        </div>
      </div>
      <div class="insight-grid" id="insightGrid"></div>
    </section>

    <section>
      <div class="section-title">
        <div>
          <h2>优化建议</h2>
          <p>尽量优先盯住真正能省下来的地方。</p>
        </div>
      </div>
      <div class="table-panel">
        <table>
          <thead>
            <tr>
              <th>动作</th>
              <th>为什么</th>
              <th>预期影响</th>
              <th>执行方式</th>
            </tr>
          </thead>
          <tbody id="optimizationTable"></tbody>
        </table>
      </div>
    </section>

    <section>
      <div class="section-title">
        <div>
          <h2>大额与重复项</h2>
          <p>一边看尖峰支出，一边看重复模式。</p>
        </div>
      </div>
      <div class="grid-two">
        <div class="table-panel">
          <h3>全部支出 Top 交易</h3>
          <table>
            <thead>
              <tr>
                <th>时间</th>
                <th>金额</th>
                <th>分类</th>
                <th>商户</th>
                <th>商品/说明</th>
              </tr>
            </thead>
            <tbody id="topTransactionTable"></tbody>
          </table>
        </div>
        <div class="table-panel">
          <h3>被排除出习惯池的代表项</h3>
          <table>
            <thead>
              <tr>
                <th>时间</th>
                <th>金额</th>
                <th>排除原因</th>
                <th>商户</th>
                <th>说明</th>
              </tr>
            </thead>
            <tbody id="exclusionTable"></tbody>
          </table>
        </div>
      </div>
      <div class="grid-two wide">
        <div class="table-panel">
          <h3>当前口径下的重复商户</h3>
          <table>
            <thead>
              <tr>
                <th>商户</th>
                <th>分类</th>
                <th>累计金额</th>
                <th>交易笔数</th>
                <th>活跃天数</th>
              </tr>
            </thead>
            <tbody id="recurringTable"></tbody>
          </table>
        </div>
        <div class="panel">
          <h3 style="margin-top: 0;">一句话结论</h3>
          <div id="headlineBadges" class="hero-meta"></div>
          <p class="footer-note">
            建议你以后至少按“固定居住 / 日常消费 / 工作工具 / 社交往来 / 一次性项目”五个桶记账。
            这样每月只看习惯池，优化会比盯所有流水更有效。
          </p>
        </div>
      </div>
    </section>
  </div>

  <script>
    const report = __PAYLOAD__;
    const poolKeys = ["all", "consumption", "habit"];
    let currentPool = "habit";

    const money = (value) => new Intl.NumberFormat("zh-CN", {{ style: "currency", currency: "CNY" }}).format(value);

    const setText = (selector, value) => {{
      const element = document.querySelector(selector);
      if (element) element.textContent = value;
    }};

    const html = (value) => value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");

    const renderHero = () => {{
      setText("#title", report.title);
      setText("#subtitle", report.subtitle);

      const heroMeta = document.querySelector("#heroMeta");
      heroMeta.innerHTML = `
        <span class="badge">周期：${{report.period.start}} 至 ${{report.period.end}}</span>
        <span class="badge">跨度：${{report.period.days}} 天</span>
        <span class="badge">总流出：${{money(report.headline.all_total)}}</span>
        <span class="badge">习惯池：${{money(report.headline.habit_total)}}</span>
      `;

      const methodList = document.querySelector("#methodList");
      methodList.innerHTML = report.methodology.map((item) => `<li>${{html(item)}}</li>`).join("");
    }};

    const renderSummaryCards = () => {{
      const summaryGrid = document.querySelector("#summaryGrid");
      summaryGrid.innerHTML = report.summary_cards.map((card) => `
        <div class="panel summary-card">
          <h3>${{html(card.label)}}</h3>
          <div class="value">${{money(card.value)}}</div>
          <p>${{html(card.description)}}</p>
          <div class="share">占总流出 ${{card.share}}%</div>
        </div>
      `).join("");
    }};

    const renderToggles = () => {{
      const poolToggle = document.querySelector("#poolToggle");
      poolToggle.innerHTML = poolKeys.map((poolKey) => {{
        const pool = report.pools[poolKey];
        const active = poolKey === currentPool ? "active" : "";
        return `<button class="toggle-button ${{active}}" data-pool="${{poolKey}}">${{html(pool.name)}}</button>`;
      }}).join("");
      poolToggle.querySelectorAll("button").forEach((button) => {{
        button.addEventListener("click", () => {{
          currentPool = button.dataset.pool;
          renderDashboard();
        }});
      }});
    }};

    const renderMetricGrid = (pool) => {{
      const metrics = [
        {{ label: "总金额", value: money(pool.total), sub: `${{pool.count}} 笔交易` }},
        {{ label: "客单价", value: money(pool.average_ticket), sub: "总金额 ÷ 笔数" }},
        {{ label: "活跃日均", value: money(pool.daily_mean), sub: `中位数 ${{money(pool.daily_median)}}` }},
        {{ label: "消费天数", value: `${{pool.spend_days}} 天`, sub: `覆盖率 ${{pool.spend_day_ratio}}%` }},
        {{ label: "工作日", value: money(pool.weekday_amount), sub: `占比 ${{pool.weekday_share}}%` }},
        {{ label: "周末", value: money(pool.weekend_amount), sub: `占比 ${{pool.weekend_share}}%` }},
      ];
      document.querySelector("#metricGrid").innerHTML = metrics.map((metric) => `
        <div class="metric">
          <div class="label">${{metric.label}}</div>
          <div class="value">${{metric.value}}</div>
          <div class="sub">${{metric.sub}}</div>
        </div>
      `).join("");
    }};

    const renderHorizontalBars = (selector, rows, valueKey = "amount", labelKey = "label") => {{
      const root = document.querySelector(selector);
      const maxValue = Math.max(...rows.map((row) => row[valueKey]), 1);
      root.innerHTML = `<div class="bar-list">${{rows.map((row) => `
        <div class="bar-item">
          <div class="bar-meta">
            <span>${{html(row[labelKey])}}</span>
            <span>${{money(row[valueKey])}} · ${{row.count}} 笔</span>
          </div>
          <div class="bar-track"><div class="bar-fill" style="width:${{Math.max(row[valueKey] / maxValue * 100, 2)}}%"></div></div>
        </div>
      `).join("")}</div>`;
    }};

    const renderVerticalBars = (selector, rows, valueKey = "amount") => {{
      const root = document.querySelector(selector);
      const maxValue = Math.max(...rows.map((row) => row[valueKey]), 1);
      root.innerHTML = `<div class="mini-bars">${{rows.map((row) => `
        <div class="mini-bar-wrap">
          <div class="mini-value">${{money(row[valueKey])}}</div>
          <div class="mini-bar" style="height:${{Math.max(row[valueKey] / maxValue * 180, 10)}}px"></div>
          <div class="mini-label">${{html(row.label)}}</div>
        </div>
      `).join("")}</div>`;
    }};

    const renderLine = (selector, rows) => {{
      const svg = document.querySelector(selector);
      const width = svg.clientWidth || 600;
      const height = svg.clientHeight || 260;
      const padding = {{ top: 16, right: 20, bottom: 28, left: 44 }};
      const innerWidth = width - padding.left - padding.right;
      const innerHeight = height - padding.top - padding.bottom;
      const maxValue = Math.max(...rows.map((row) => row.amount), 1);
      const x = (index) => padding.left + (rows.length <= 1 ? 0 : index / (rows.length - 1) * innerWidth);
      const y = (value) => padding.top + innerHeight - value / maxValue * innerHeight;
      const path = rows.map((row, index) => `${{index === 0 ? "M" : "L"}}${{x(index).toFixed(1)}},${{y(row.amount).toFixed(1)}}`).join(" ");
      const markers = rows.filter((row) => row.amount > 0).map((row, index) => `
        <circle cx="${{x(index)}}" cy="${{y(row.amount)}}" r="2.6" fill="#70e1ff" opacity="0.9"></circle>
      `).join("");
      const gridLines = [0, 0.25, 0.5, 0.75, 1].map((ratio) => {{
        const currentY = padding.top + innerHeight * ratio;
        const labelValue = maxValue * (1 - ratio);
        return `
          <line x1="${{padding.left}}" y1="${{currentY}}" x2="${{width - padding.right}}" y2="${{currentY}}" stroke="rgba(255,255,255,0.08)" />
          <text x="${{padding.left - 8}}" y="${{currentY + 4}}" fill="#9fb0d0" font-size="11" text-anchor="end">${{money(labelValue)}}</text>
        `;
      }}).join("");
      const startLabel = rows[0]?.date || "";
      const endLabel = rows[rows.length - 1]?.date || "";
      svg.setAttribute("viewBox", `0 0 ${{width}} ${{height}}`);
      svg.innerHTML = `
        <defs>
          <linearGradient id="lineGradient" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0%" stop-color="#70e1ff"></stop>
            <stop offset="100%" stop-color="#7c89ff"></stop>
          </linearGradient>
        </defs>
        ${{gridLines}}
        <path d="${{path}}" fill="none" stroke="url(#lineGradient)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"></path>
        ${{markers}}
        <text x="${{padding.left}}" y="${{height - 6}}" fill="#9fb0d0" font-size="11">${{startLabel}}</text>
        <text x="${{width - padding.right}}" y="${{height - 6}}" fill="#9fb0d0" font-size="11" text-anchor="end">${{endLabel}}</text>
      `;
    }};

    const renderHeatmap = (selector, matrix) => {{
      const root = document.querySelector(selector);
      const flat = matrix.flat();
      const maxValue = Math.max(...flat.map((item) => item.amount), 1);
      let htmlOutput = `<div class="heatmap">`;
      htmlOutput += `<div></div>`;
      matrix[0].forEach((cell) => {{ htmlOutput += `<div class="heat-label">${{cell.col}}</div>`; }});
      matrix.forEach((row) => {{
        htmlOutput += `<div class="heat-label">${{row[0].row}}</div>`;
        row.forEach((cell) => {{
          const alpha = 0.08 + cell.amount / maxValue * 0.82;
          const color = `rgba(112,225,255,${{alpha.toFixed(2)}})`;
          htmlOutput += `<div class="heat-cell" style="background:${{color}}" title="${{cell.row}} / ${{cell.col}}：${{money(cell.amount)}}，${{cell.count}} 笔">${{money(cell.amount)}}</div>`;
        }});
      }});
      htmlOutput += `</div>`;
      root.innerHTML = htmlOutput;
    }};

    const renderInsights = () => {{
      document.querySelector("#insightGrid").innerHTML = report.insights.map((item) => `
        <div class="insight-card">
          <h3>${{html(item.title)}}</h3>
          <p>${{html(item.body)}}</p>
        </div>
      `).join("");
    }};

    const renderOptimizations = () => {{
      document.querySelector("#optimizationTable").innerHTML = report.optimizations.map((item) => `
        <tr>
          <td>${{html(item.action)}}</td>
          <td>${{html(item.why)}}</td>
          <td><span class="pill">${{html(item.impact)}}</span></td>
          <td>${{html(item.how)}}</td>
        </tr>
      `).join("");
    }};

    const renderStaticTables = () => {{
      document.querySelector("#topTransactionTable").innerHTML = report.overall_top_transactions.map((item) => `
        <tr>
          <td>${{item.date}}</td>
          <td>${{money(item.amount)}}</td>
          <td>${{html(item.scene)}}</td>
          <td>${{html(item.merchant)}}</td>
          <td>${{html(item.item || "-")}}</td>
        </tr>
      `).join("");

      document.querySelector("#exclusionTable").innerHTML = report.exclusion_table.map((item) => `
        <tr>
          <td>${{item.date}}</td>
          <td>${{money(item.amount)}}</td>
          <td><span class="pill">${{html(item.reason)}}</span></td>
          <td>${{html(item.merchant)}}</td>
          <td>${{html(item.item || item.scene)}}</td>
        </tr>
      `).join("");

      const headlineBadges = document.querySelector("#headlineBadges");
      headlineBadges.innerHTML = `
        <span class="badge">全部支出 ${{money(report.headline.all_total)}}</span>
        <span class="badge">消费型支出 ${{money(report.headline.consumption_total)}}</span>
        <span class="badge">习惯池 ${{money(report.headline.habit_total)}}</span>
        <span class="badge">小额高频 ${{report.headline.small_count}} 笔 / ${{money(report.headline.small_total)}}</span>
        <span class="badge">数字工具与订阅 ${{money(report.headline.digital_total)}}</span>
      `;
    }};

    const renderRecurringTable = (pool) => {{
      const rows = pool.recurring_merchants;
      document.querySelector("#recurringTable").innerHTML = rows.length
        ? rows.map((row) => `
            <tr>
              <td>${{html(row.merchant)}}</td>
              <td>${{html(row.scene)}}</td>
              <td>${{money(row.amount)}}</td>
              <td>${{row.count}}</td>
              <td>${{row.days}}</td>
            </tr>
          `).join("")
        : `<tr><td colspan="5" style="color:#9fb0d0;">当前口径下没有足够明显的重复商户。</td></tr>`;
    }};

    const renderDashboard = () => {{
      renderToggles();
      const pool = report.pools[currentPool];
      setText("#poolDescription", pool.description);
      renderMetricGrid(pool);
      renderHorizontalBars("#categoryChart", pool.top_categories);
      renderVerticalBars("#monthChart", pool.monthly);
      renderLine("#dailyLine", pool.daily);
      renderHorizontalBars("#paymentChart", pool.payment_methods);
      renderVerticalBars("#weekdayChart", pool.weekday);
      renderVerticalBars("#timeChart", pool.time_bucket);
      renderHorizontalBars("#merchantChart", pool.top_merchants, "amount", "label");
      renderHeatmap("#heatmap", pool.heatmap);
      renderRecurringTable(pool);
    }};

    renderHero();
    renderSummaryCards();
    renderInsights();
    renderOptimizations();
    renderStaticTables();
    renderDashboard();
    window.addEventListener("resize", () => renderLine("#dailyLine", report.pools[currentPool].daily));
  </script>
</body>
</html>
"""
    normalized = template.replace("{{", "{").replace("}}", "}")
    return normalized.replace("__PAYLOAD__", payload_json)


def generate_report(alipay_path: Path, wechat_path: Path, output_path: Path) -> Path:
    transactions = [transaction for transaction in parse_alipay(alipay_path) + parse_wechat(wechat_path) if keep_spend(transaction)]
    report = build_report_payload(transactions, alipay_path, wechat_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_template(json.dumps(report, ensure_ascii=False)), encoding="utf-8")
    return output_path


def main() -> None:
    args = parse_args()
    alipay_path, wechat_path, output_path = resolve_inputs(args)
    output_path = generate_report(alipay_path, wechat_path, output_path)
    print(f"Alipay bill: {alipay_path}")
    print(f"WeChat bill: {wechat_path}")
    print(f"Report generated: {output_path}")

    if args.open:
        import subprocess

        subprocess.run(["open", str(output_path)], check=False)


if __name__ == "__main__":
    main()
