#!/usr/bin/env python3
"""宝宝每日护理记录工具 - 纯 Python，无外部依赖"""

import sys
import json
import argparse
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def get_data_dir(custom_dir=None):
    d = Path(custom_dir) if custom_dir else DEFAULT_DATA_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def file_for_date(data_dir, dt):
    return data_dir / f"{dt}.json"


def load_day(data_dir, dt):
    f = file_for_date(data_dir, dt)
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    return None


def save_day(data_dir, dt, data):
    data["date"] = dt
    f = file_for_date(data_dir, dt)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def deep_merge(base, override):
    """递归合并：override 中非 None 的值覆盖 base"""
    result = dict(base)
    for k, v in override.items():
        if v is None:
            continue
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def empty_template():
    return {
        "date": None,
        "temperature": {"morning": None, "afternoon": None},
        "jaundice": {
            "morning": {"forehead": None, "face": None, "chest": None},
            "evening": {"forehead": None, "face": None, "chest": None},
        },
        "bath": None,
        "weight": None,
        "sleep": {"quality": None, "hours": None},
        "feeding": {
            "formula": {"ml": None, "times": None},
            "breastMilk": {"ml": None, "times": None},
        },
        "diaper": {"poop": None, "pee": None},
        "symptoms": [],
        "note": None,
    }


# ── Commands ──────────────────────────────────────────────


def cmd_save(args):
    """保存/合并单日数据"""
    data_dir = get_data_dir(args.dir)
    dt = args.date or str(date.today())
    new_data = json.loads(args.data)

    existing = load_day(data_dir, dt)
    if existing:
        # 特殊处理 symptoms：合并去重
        if "symptoms" in new_data and "symptoms" in existing:
            merged_symptoms = list(set((existing.get("symptoms") or []) + (new_data.get("symptoms") or [])))
            existing_copy = dict(existing)
            new_copy = dict(new_data)
            existing_copy.pop("symptoms", None)
            new_copy.pop("symptoms", None)
            merged = deep_merge(existing_copy, new_copy)
            merged["symptoms"] = merged_symptoms
        else:
            merged = deep_merge(existing, new_data)
    else:
        template = empty_template()
        merged = deep_merge(template, new_data)

    save_day(data_dir, dt, merged)
    print(json.dumps({"status": "ok", "date": dt, "data": merged}, ensure_ascii=False, indent=2))


def cmd_get(args):
    """获取单日数据"""
    data_dir = get_data_dir(args.dir)
    dt = args.date or str(date.today())
    data = load_day(data_dir, dt)
    if data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": f"无 {dt} 的记录"}, ensure_ascii=False))
        sys.exit(1)


def cmd_list(args):
    """列出最近 N 天有记录的日期"""
    data_dir = get_data_dir(args.dir)
    n = args.last or 7
    files = sorted(data_dir.glob("*.json"), reverse=True)
    result = []
    for f in files[:n]:
        data = json.loads(f.read_text(encoding="utf-8"))
        summary_line = _day_summary(data)
        result.append({"date": f.stem, "summary": summary_line})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_query(args):
    """日期范围查询"""
    data_dir = get_data_dir(args.dir)
    files = sorted(data_dir.glob("*.json"))
    result = []
    for f in files:
        dt = f.stem
        if args.start and dt < args.start:
            continue
        if args.end and dt > args.end:
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        result.append(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_summary(args):
    """汇总最近 N 天趋势"""
    data_dir = get_data_dir(args.dir)
    n = args.last or 7
    files = sorted(data_dir.glob("*.json"), reverse=True)[:n]
    files.reverse()

    if not files:
        print(json.dumps({"error": "暂无数据"}, ensure_ascii=False))
        sys.exit(1)

    days = [json.loads(f.read_text(encoding="utf-8")) for f in files]

    # 体温趋势
    temps = []
    for d in days:
        t = d.get("temperature") or {}
        am = t.get("morning")
        pm = t.get("afternoon")
        if am is not None or pm is not None:
            temps.append({"date": d["date"], "morning": am, "afternoon": pm})

    # 体重趋势
    weights = [{"date": d["date"], "kg": d.get("weight")} for d in days if d.get("weight") is not None]

    # 喂养趋势
    feedings = []
    for d in days:
        f = d.get("feeding") or {}
        fm = f.get("formula") or {}
        bm = f.get("breastMilk") or {}
        total_ml = (fm.get("ml") or 0) + (bm.get("ml") or 0)
        total_times = (fm.get("times") or 0) + (bm.get("times") or 0)
        if total_ml > 0 or total_times > 0:
            feedings.append({
                "date": d["date"],
                "formulaMl": fm.get("ml"),
                "formulaTimes": fm.get("times"),
                "breastMilkMl": bm.get("ml"),
                "breastMilkTimes": bm.get("times"),
                "totalMl": total_ml,
                "totalTimes": total_times,
            })

    # 排泄趋势
    diapers = []
    for d in days:
        dp = d.get("diaper") or {}
        if dp.get("poop") is not None or dp.get("pee") is not None:
            diapers.append({"date": d["date"], "poop": dp.get("poop"), "pee": dp.get("pee")})

    # 黄疸趋势
    jaundice_list = []
    for d in days:
        j = d.get("jaundice") or {}
        am = j.get("morning") or {}
        pm = j.get("evening") or {}
        if any(v is not None for v in [*am.values(), *pm.values()]):
            jaundice_list.append({"date": d["date"], "morning": am, "evening": pm})

    summary = {
        "period": f"{days[0]['date']} ~ {days[-1]['date']}",
        "totalDays": len(days),
        "temperature": temps,
        "weight": weights,
        "feeding": feedings,
        "diaper": diapers,
        "jaundice": jaundice_list,
    }

    # 计算均值
    if feedings:
        avg_ml = sum(f["totalMl"] for f in feedings) / len(feedings)
        summary["avgDailyMl"] = round(avg_ml, 0)
    if diapers:
        avg_poop = sum((d["poop"] or 0) for d in diapers) / len(diapers)
        avg_pee = sum((d["pee"] or 0) for d in diapers) / len(diapers)
        summary["avgDailyPoop"] = round(avg_poop, 1)
        summary["avgDailyPee"] = round(avg_pee, 1)

    print(json.dumps(summary, ensure_ascii=False, indent=2))


def cmd_delete(args):
    """删除单日记录"""
    data_dir = get_data_dir(args.dir)
    dt = args.date
    f = file_for_date(data_dir, dt)
    if f.exists():
        f.unlink()
        print(json.dumps({"status": "ok", "deleted": dt}, ensure_ascii=False))
    else:
        print(json.dumps({"error": f"无 {dt} 的记录"}, ensure_ascii=False))
        sys.exit(1)


# ── Helpers ───────────────────────────────────────────────


def _day_summary(data):
    """生成单日摘要文本"""
    parts = []
    t = data.get("temperature") or {}
    if t.get("morning") is not None or t.get("afternoon") is not None:
        temps = "/".join(str(v) for v in [t.get("morning"), t.get("afternoon")] if v is not None)
        parts.append(f"体温{temps}°C")

    f = data.get("feeding") or {}
    fm = f.get("formula") or {}
    bm = f.get("breastMilk") or {}
    total = (fm.get("ml") or 0) + (bm.get("ml") or 0)
    if total:
        parts.append(f"奶量{total}ml")

    dp = data.get("diaper") or {}
    if dp.get("poop") is not None:
        parts.append(f"便{dp['poop']}次")
    if dp.get("pee") is not None:
        parts.append(f"尿{dp['pee']}次")

    w = data.get("weight")
    if w is not None:
        parts.append(f"体重{w}kg")

    return " | ".join(parts) if parts else "（部分数据）"


# ── Main ──────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="宝宝每日护理记录工具")
    parser.add_argument("--dir", help="数据目录路径（默认 skill 内 data/）")
    sub = parser.add_subparsers(dest="cmd")

    p_save = sub.add_parser("save", help="保存/合并单日数据")
    p_save.add_argument("--date", help="日期 YYYY-MM-DD（默认今天）")
    p_save.add_argument("--data", required=True, help="JSON 数据字符串")

    p_get = sub.add_parser("get", help="获取单日数据")
    p_get.add_argument("--date", help="日期 YYYY-MM-DD（默认今天）")

    p_list = sub.add_parser("list", help="列出最近 N 天记录")
    p_list.add_argument("--last", type=int, default=7, help="天数（默认 7）")

    p_query = sub.add_parser("query", help="日期范围查询")
    p_query.add_argument("--start", help="开始日期")
    p_query.add_argument("--end", help="结束日期")

    p_summary = sub.add_parser("summary", help="趋势汇总")
    p_summary.add_argument("--last", type=int, default=7, help="天数（默认 7）")

    p_delete = sub.add_parser("delete", help="删除单日记录")
    p_delete.add_argument("--date", required=True, help="日期 YYYY-MM-DD")

    args = parser.parse_args()
    cmds = {
        "save": cmd_save,
        "get": cmd_get,
        "list": cmd_list,
        "query": cmd_query,
        "summary": cmd_summary,
        "delete": cmd_delete,
    }

    if args.cmd in cmds:
        cmds[args.cmd](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
