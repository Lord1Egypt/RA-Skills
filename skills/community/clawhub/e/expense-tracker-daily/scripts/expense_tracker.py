#!/usr/bin/env python3
"""
expense_tracker.py — 智能记账数据引擎
用法:
  python expense_tracker.py add --amount 35 --category 餐饮 --desc "午饭" [--date 2026-04-09]
  python expense_tracker.py list [--limit 20] [--category 餐饮] [--from 2026-04-01] [--to 2026-04-30]
  python expense_tracker.py delete --id <id>
  python expense_tracker.py stats [--period month|week|day] [--date 2026-04-09]
  python expense_tracker.py categories
  python expense_tracker.py summary [--top 5]
"""

import argparse
import io
import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Fix Windows stdout encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

DATA_DIR = Path.home() / ".qclaw" / "workspace" / "expense-tracker-data"
DATA_FILE = DATA_DIR / "expenses.json"
CONFIG_FILE = DATA_DIR / "config.json"

# ── 分类关键词映射 ──────────────────────────────────────────
CATEGORY_KEYWORDS = {
    "餐饮": [
        "午饭", "晚饭", "早饭", "早餐", "午餐", "晚餐", "宵夜", "外卖",
        "吃饭", "餐厅", "食堂", "饭", "面", "粉", "火锅", "烧烤", "烤肉",
        "奶茶", "咖啡", "饮品", "饮料", "零食", "小吃", "水果", "蛋糕",
        "甜品", "冰激凌", "聚餐", "请客", "宴", "酒", "啤酒", "菜",
        "便当", "盒饭", "麻辣烫", "冒菜", "饺子", "包子", "馒头",
        "煎饼", "粥", "拉面", "寿司", "披萨", "汉堡", "炸鸡", "麻辣香锅",
    ],
    "交通": [
        "打车", "滴滴", "出租", "地铁", "公交", "高铁", "火车", "飞机",
        "机票", "车票", "油费", "加油", "停车", "过路费", "高速", "骑手",
        "顺风车", "摩的", "单车", "共享", "地铁卡", "一卡通",
    ],
    "购物": [
        "超市", "淘宝", "京东", "拼多多", "网购", "购物", "买", "商城",
        "衣服", "裤子", "鞋", "包", "化妆品", "护肤品", "日用品",
        "家电", "数码", "手机", "电脑", "平板", "耳机", "充电器",
        "家具", "家居", "厨具", "文具", "书籍",
    ],
    "娱乐": [
        "电影", "游戏", "KTV", "唱歌", "酒吧", "演出", "演唱会", "音乐节",
        "门票", "景点", "旅游", "旅行", "门票", "会员", "视频", "音乐",
        "网费", "话费", "充值", "VIP", "直播", "打赏",
    ],
    "住房": [
        "房租", "租金", "水电", "电费", "水费", "燃气", "物业", "网费",
        "宽带", "维修", "装修", "家具", "家电安装",
    ],
    "医疗": [
        "看病", "医院", "药", "挂号", "体检", "牙", "眼科", "保险",
        "门诊", "住院", "手术", "保健",
    ],
    "教育": [
        "学费", "课程", "培训", "书", "教材", "考试", "报名费",
        "网课", "知识付费", "订阅",
    ],
    "人情": [
        "红包", "礼物", "份子", "随礼", "生日", "结婚", "满月",
        "过节", "春节", "中秋", "月饼",
    ],
}

# ── 数据操作 ────────────────────────────────────────────────

def _ensure_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def _load_data():
    _ensure_dir()
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text("utf-8"))
        except (json.JSONDecodeError, IOError):
            return []
    return []

def _save_data(expenses):
    _ensure_dir()
    DATA_FILE.write_text(json.dumps(expenses, ensure_ascii=False, indent=2), "utf-8")

def _next_id():
    expenses = _load_data()
    if not expenses:
        return 1
    return max(e.get("id", 0) for e in expenses) + 1

# ── 命令实现 ────────────────────────────────────────────────

def cmd_add(args):
    expense = {
        "id": _next_id(),
        "amount": round(float(args.amount), 2),
        "category": args.category or "其他",
        "description": args.desc or "",
        "date": args.date or datetime.now().strftime("%Y-%m-%d"),
        "timestamp": int(datetime.now().timestamp() * 1000),
    }
    expenses = _load_data()
    expenses.append(expense)
    _save_data(expenses)
    _out({
        "status": "ok",
        "expense": expense,
        "message": f"已记录: {expense['category']} ¥{expense['amount']} — {expense['description'] or '无备注'} ({expense['date']})"
    })

def cmd_list(args):
    expenses = _load_data()
    # 过滤
    if args.category:
        expenses = [e for e in expenses if e.get("category") == args.category]
    if args.from_date:
        expenses = [e for e in expenses if e.get("date", "") >= args.from_date]
    if args.to_date:
        expenses = [e for e in expenses if e.get("date", "") <= args.to_date]
    # 按日期倒序
    expenses.sort(key=lambda e: (e.get("date", ""), e.get("id", 0)), reverse=True)
    # 限制
    limit = args.limit or len(expenses)
    shown = expenses[:limit]
    _out({
        "status": "ok",
        "total": len(expenses),
        "shown": len(shown),
        "expenses": shown
    })

def cmd_delete(args):
    expenses = _load_data()
    target_id = int(args.id)
    before = len(expenses)
    expenses = [e for e in expenses if e.get("id") != target_id]
    after = len(expenses)
    if before == after:
        _out({"status": "error", "message": f"未找到 id={target_id} 的记录"})
    else:
        _save_data(expenses)
        _out({"status": "ok", "message": f"已删除 id={target_id} 的记录"})

def cmd_stats(args):
    expenses = _load_data()
    period = args.period or "month"
    ref_date = args.date or datetime.now().strftime("%Y-%m-%d")
    ref = datetime.strptime(ref_date, "%Y-%m-%d")

    # 时间范围
    if period == "day":
        start = ref
        end = ref
    elif period == "week":
        start = ref - timedelta(days=ref.weekday())
        end = start + timedelta(days=6)
    else:  # month
        start = ref.replace(day=1)
        next_month = ref.replace(day=28) + timedelta(days=4)
        end = next_month.replace(day=1) - timedelta(days=1)

    start_str = start.strftime("%Y-%m-%d")
    end_str = end.strftime("%Y-%m-%d")
    filtered = [e for e in expenses if start_str <= e.get("date", "") <= end_str]

    total = sum(e.get("amount", 0) for e in filtered)
    by_category = {}
    daily = {}
    for e in filtered:
        cat = e.get("category", "其他")
        by_category[cat] = by_category.get(cat, 0) + e.get("amount", 0)
        d = e.get("date", "")
        daily[d] = daily.get(d, 0) + e.get("amount", 0)

    # 排序
    by_category = dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True))

    _out({
        "status": "ok",
        "period": period,
        "period_label": {"day": "日", "week": "周", "month": "月"}[period],
        "date": ref_date,
        "range": {"start": start_str, "end": end_str},
        "total": round(total, 2),
        "count": len(filtered),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
        "daily": {k: round(v, 2) for k, v in sorted(daily.items())},
    })

def cmd_categories(_args):
    _out({
        "status": "ok",
        "categories": list(CATEGORY_KEYWORDS.keys()) + ["其他"],
        "keywords_map": {k: v[:10] for k, v in CATEGORY_KEYWORDS.items()},  # 只返回前10个关键词做预览
    })

def cmd_summary(args):
    expenses = _load_data()
    top = args.top or 5
    # 总计
    total = sum(e.get("amount", 0) for e in expenses)
    count = len(expenses)
    # 按类别
    by_category = {}
    for e in expenses:
        cat = e.get("category", "其他")
        by_category[cat] = by_category.get(cat, 0) + e.get("amount", 0)
    by_category = dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True)[:top])
    # 最近5笔
    recent = sorted(expenses, key=lambda e: e.get("timestamp", 0), reverse=True)[:5]

    _out({
        "status": "ok",
        "total_expenses": round(total, 2),
        "total_records": count,
        "top_categories": {k: round(v, 2) for k, v in by_category.items()},
        "recent": recent,
    })

# ── 工具 ────────────────────────────────────────────────────

def _out(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))

# ── CLI ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="expense-tracker CLI")
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="添加记录")
    p_add.add_argument("--amount", "-a", required=True, help="金额")
    p_add.add_argument("--category", "-c", help="分类")
    p_add.add_argument("--desc", "-d", default="", help="描述")
    p_add.add_argument("--date", help="日期 YYYY-MM-DD")

    # list
    p_list = sub.add_parser("list", help="列出记录")
    p_list.add_argument("--limit", "-n", type=int, help="数量限制")
    p_list.add_argument("--category", "-c", help="按分类过滤")
    p_list.add_argument("--from", dest="from_date", help="起始日期")
    p_list.add_argument("--to", dest="to_date", help="结束日期")

    # delete
    p_del = sub.add_parser("delete", help="删除记录")
    p_del.add_argument("--id", required=True, help="记录ID")

    # stats
    p_stats = sub.add_parser("stats", help="统计分析")
    p_stats.add_argument("--period", "-p", choices=["day", "week", "month"], default="month")
    p_stats.add_argument("--date", help="参考日期 YYYY-MM-DD")

    # categories
    sub.add_parser("categories", help="查看分类")

    # summary
    p_sum = sub.add_parser("summary", help="总览")
    p_sum.add_argument("--top", "-t", type=int, default=5, help="Top N 分类")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "add": cmd_add,
        "list": cmd_list,
        "delete": cmd_delete,
        "stats": cmd_stats,
        "categories": cmd_categories,
        "summary": cmd_summary,
    }
    cmds[args.command](args)

if __name__ == "__main__":
    main()
