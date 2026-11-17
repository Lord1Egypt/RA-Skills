#!/usr/bin/env python3
"""Validate Chinese CSV/JSON exports and aggregate evidence; never write prose.

Copyright 2026 aimeGeo contributors. SPDX-License-Identifier: MIT-0
"""

import argparse
import csv
import json
import math
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit


class DataError(ValueError):
    pass


TABLES = ("文章", "发布", "AI回答", "经营")
KEYS = {"文章": "文章ID", "发布": "发布ID", "AI回答": "记录ID", "经营": "记录ID"}
GROUPS = {}
LABELS = {}


def register(group, **labels):
    for key, label in labels.items():
        GROUPS[key] = group
        LABELS[key] = label


register("文章", articles="新增文章数")
register("发布", publications="发布记录数", published_articles="涉及文章数",
         submitted="已投稿", submission_failed="投稿失败", not_submitted="未投稿",
         submission_unknown="投稿未知", approved="审核通过", reviewing="审核中",
         rejected="审核拒绝", review_unknown="审核未知", public="公开已验证",
         not_public="未公开", public_pending="公开待核验", public_unknown="公开未知",
         indexed="收录已验证", not_found="收录未检出", index_unrun="收录未查询",
         index_failed="收录查询失败", index_unknown="收录未知")
register("AI回答", ai_completed="实际完成回答", ai_failed="AI查询失败",
         ai_unrun="AI未运行", ai_simulated="AI模拟回答", ai_mentions="实际品牌提及回答",
         ai_cited="实际原生引用回答", ai_mention_rate="实际品牌提及率",
         ai_citation_rate="实际原生引用率", sim_cited="模拟原生引用回答",
         sim_citation_rate="模拟原生引用率")
register("经营", sessions="会话数", conversions="转化会话数", revenue="归因收入",
         cost="成本", cvr="会话转化率", roi="ROI")


def require(condition, message):
    if not condition:
        raise DataError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def text_field(row, key):
    value = row.get(key)
    require(nonempty(value), f"{key} 必须为非空字符串")
    row[key] = value.strip()
    return row[key]


def day(value):
    require(isinstance(value, str), "日期必须为 YYYY-MM-DD 字符串")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise DataError(f"无效日期: {value}") from exc
    require(parsed.isoformat() == value, f"日期必须为 YYYY-MM-DD: {value}")
    return parsed


def number(value, key):
    if value is None or value == "":
        return None
    require(not isinstance(value, bool), f"{key} 不能为布尔值")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise DataError(f"{key} 必须为非负有限数值") from exc
    require(math.isfinite(result) and result >= 0, f"{key} 必须为非负有限数值")
    if key in ("会话", "转化会话"):
        require(result.is_integer(), f"{key} 必须为整数")
        return int(result)
    return result


def enum(row, key, choices):
    value = text_field(row, key)
    require(value in choices, f"{key} 无效: {value}；允许 {', '.join(choices)}")
    return value


def evidence(row, key):
    text_field(row, key)


def validate_row(table, row, nature):
    text_field(row, KEYS[table])
    if table == "文章":
        text_field(row, "标题")
    elif table == "发布":
        text_field(row, "文章ID")
        text_field(row, "账号")
        text_field(row, "平台")
        submitted = enum(row, "投稿", ("已提交", "失败", "未提交", "未知"))
        enum(row, "审核", ("通过", "审核中", "拒绝", "未知"))
        public = enum(row, "公开", ("已验证", "未公开", "待核验", "未知"))
        indexed = enum(row, "收录", ("已验证", "未检出", "未查询", "查询失败", "未知"))
        if submitted == "已提交":
            evidence(row, "投稿证据")
        if public == "已验证":
            evidence(row, "公开证据")
        if indexed in ("已验证", "未检出"):
            evidence(row, "收录证据")
    elif table == "AI回答":
        text_field(row, "平台")
        text_field(row, "问题ID")
        state = enum(row, "运行状态", ("已完成", "未运行", "查询失败", "模拟"))
        require(nature != "模拟" or state != "已完成", "模拟数据的完成回答须显式标为 模拟")
        if state in ("已完成", "模拟"):
            text_field(row, "回答")
            enum(row, "品牌提及", ("是", "否"))
            evidence(row, "证据")
            refs = row.get("原生引用")
            if isinstance(refs, str):
                try:
                    refs = json.loads(refs)
                except ValueError as exc:
                    raise DataError("原生引用必须为 JSON 数组；确认无引用时填 []") from exc
            require(isinstance(refs, list), "原生引用必须为数组；空白不等于零引用")
            for ref in refs:
                require(isinstance(ref, dict), "每条原生引用必须为对象")
                url = ref.get("url", "")
                require(isinstance(url, str), "引用 url 必须为字符串")
                try:
                    parsed = urlsplit(url)
                    valid = parsed.scheme in ("http", "https") and bool(parsed.hostname)
                except ValueError:
                    valid = False
                require(valid, "原生引用需要有效的 http(s) URL")
                enum(ref, "归属", ("本项目", "其他"))
            row["原生引用"] = refs
        else:
            require(row.get("品牌提及") in (None, ""), "未运行/失败不能填写品牌提及结论")
            require(row.get("原生引用") in (None, "", "[]", []), "未运行/失败不能填写引用结果")
            if state == "查询失败":
                text_field(row, "错误")
    else:
        text_field(row, "账号")
        for key in ("会话", "转化会话", "归因收入", "成本"):
            row[key] = number(row.get(key), key)
        if row["会话"] is not None and row["转化会话"] is not None:
            require(row["转化会话"] <= row["会话"], "转化会话不能大于会话")
        if row["归因收入"] is not None or row["成本"] is not None:
            text_field(row, "币种")


def load_table(base, table, spec, start, end, project, accounts, nature):
    require(isinstance(spec, dict), f"{table} 数据源应为对象")
    path_text = text_field(spec, "路径")
    relative = Path(path_text)
    require(not relative.is_absolute() and ".." not in relative.parts,
            f"{table} 路径须位于配置目录内")
    path = (base / relative).resolve()
    require(path.is_relative_to(base), f"{table} 路径不能通过符号链接越出配置目录")
    freshness = day(spec.get("数据截至"))
    require(freshness >= end, f"{table} 数据截至早于周期结束；请缩短周期")
    coverage = enum(spec, "覆盖", ("完整", "部分"))
    text_field(spec, "说明")
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames or []
            require(len(fields) == len(set(fields)), f"{table} CSV 列名重复")
            required = {"项目", "日期", KEYS[table]}
            require(required <= set(fields), f"{table} CSV 缺少基础列 {sorted(required)}")
            rows = list(reader)
    elif path.suffix.lower() == ".json":
        rows = json.loads(path.read_text(encoding="utf-8-sig"))
        require(isinstance(rows, list), f"{table} JSON 须为对象数组")
    else:
        raise DataError(f"{table} 只支持 .csv 或 .json")
    chosen, seen = [], set()
    for i, raw in enumerate(rows, 1):
        try:
            require(isinstance(raw, dict), "记录必须为对象")
            row = dict(raw)
            require(None not in row, "CSV 存在超出表头的字段")
            row_project = text_field(row, "项目")
            row_day = day(row.get("日期"))
            if row_project != project or not start <= row_day <= end:
                continue
            if table in ("发布", "经营"):
                account = text_field(row, "账号")
                if accounts and account not in accounts:
                    continue
            validate_row(table, row, nature)
            key = text_field(row, KEYS[table])
            require(key not in seen, f"{KEYS[table]} 重复: {key}；先核对去重")
            seen.add(key)
            chosen.append(row)
        except DataError as exc:
            raise DataError(f"{table} 第 {i} 条: {exc}") from exc
    return chosen, {**spec, "选中行数": len(chosen), "排除行数": len(rows) - len(chosen),
                    "覆盖": coverage}


def aggregate_period(base, config, period):
    require(isinstance(period, dict), "周期应为对象")
    start, end = day(period.get("开始")), day(period.get("结束"))
    require(start <= end, "周期开始不能晚于结束")
    specs = period.get("数据", {})
    require(isinstance(specs, dict), "周期数据须为对象")
    require(not set(specs) - set(TABLES), "存在未知数据表")
    tables, sources = {}, {}
    for table, spec in specs.items():
        tables[table], sources[table] = load_table(
            base, table, spec, start, end, config["项目"], config.get("账号", []), config["数据性质"])
    metrics = {}

    def put(key, value, unit="条", numerator=None, denominator=None, reason=""):
        require(value is None or math.isfinite(value), f"{LABELS[key]} 汇总溢出")
        source = sources.get(GROUPS[key])
        status = "已统计"
        if value is None:
            status = "N/A"
        elif config["数据性质"] == "模拟" or key.startswith("sim_"):
            status = "模拟"
        elif source and source["覆盖"] == "部分":
            status = "部分样本"
        metrics[key] = {"value": value, "unit": unit, "numerator": numerator,
                        "denominator": denominator, "status": status, "reason": reason}

    for key in LABELS:
        unit = "%" if key.endswith("_rate") or key in ("cvr", "roi") else "条"
        if key in ("articles", "published_articles"):
            unit = "篇"
        elif key in ("revenue", "cost"):
            unit = "货币单位未提供"
        put(key, None, unit, reason=f"未提供{GROUPS[key]}数据")
    if "文章" in tables:
        put("articles", len(tables["文章"]), "篇", reason="按项目内文章ID去重；日期为创建日")
    if "发布" in tables:
        rows = tables["发布"]
        put("publications", len(rows), reason="周期内创建的发布记录；非文章数")
        put("published_articles", len({r["文章ID"] for r in rows}), "篇")
        states = {
            "投稿": {"已提交": "submitted", "失败": "submission_failed", "未提交": "not_submitted", "未知": "submission_unknown"},
            "审核": {"通过": "approved", "审核中": "reviewing", "拒绝": "rejected", "未知": "review_unknown"},
            "公开": {"已验证": "public", "未公开": "not_public", "待核验": "public_pending", "未知": "public_unknown"},
            "收录": {"已验证": "indexed", "未检出": "not_found", "未查询": "index_unrun", "查询失败": "index_failed", "未知": "index_unknown"},
        }
        for field, mapping in states.items():
            counts = Counter(r[field] for r in rows)
            for state, key in mapping.items():
                put(key, counts[state], denominator=len(rows), reason=f"独立读取{field}字段；不从其他阶段推导")
    if "AI回答" in tables:
        rows = tables["AI回答"]
        actual = [r for r in rows if r["运行状态"] == "已完成"]
        simulated = [r for r in rows if r["运行状态"] == "模拟"]
        for state, key in (("已完成", "ai_completed"), ("查询失败", "ai_failed"),
                           ("未运行", "ai_unrun"), ("模拟", "ai_simulated")):
            put(key, sum(r["运行状态"] == state for r in rows), reason="按运行状态分别计数")
        mentions = sum(r["品牌提及"] == "是" for r in actual)
        cited = lambda subset: sum(any(ref["归属"] == "本项目" for ref in r["原生引用"]) for r in subset)
        for subset, count, rate in ((actual, "ai_cited", "ai_citation_rate"),
                                    (simulated, "sim_cited", "sim_citation_rate")):
            n, d = cited(subset), len(subset)
            note = "分子为包含本项目原生引用的回答数；每次完整回答算一个样本"
            put(count, n if d else None, numerator=n if d else None, denominator=d,
                reason=note if d else "零有效回答样本；未运行/失败/模拟不计入实际分母")
            put(rate, 100 * n / d if d else None, "%", n if d else None, d,
                note if d else "零有效回答样本，引用率 N/A")
        put("ai_mentions", mentions if actual else None, numerator=mentions if actual else None,
            denominator=len(actual), reason="仅实际完成回答" if actual else "零实际完成回答样本")
        put("ai_mention_rate", 100 * mentions / len(actual) if actual else None, "%",
            mentions if actual else None, len(actual), "仅实际完成回答" if actual else "零实际完成回答样本")
    if "经营" in tables:
        rows = tables["经营"]
        currencies = {r["币种"] for r in rows if r["归因收入"] is not None or r["成本"] is not None}
        require(len(currencies) <= 1, "经营数据币种混用；请分币种运行，不自动换汇")
        currency = next(iter(currencies), "货币单位未提供")
        values = {}
        for field, key in (("会话", "sessions"), ("转化会话", "conversions"),
                           ("归因收入", "revenue"), ("成本", "cost")):
            value = sum(r[field] for r in rows) if rows and all(r[field] is not None for r in rows) else None
            values[key] = value
            put(key, value, currency if key in ("revenue", "cost") else "次",
                reason="已选中行的合计" if value is not None else f"{field}为空或无经营样本，不将缺失补零")
        sessions, conversions = values["sessions"], values["conversions"]
        put("cvr", 100 * conversions / sessions if sessions and conversions is not None else None,
            "%", conversions, sessions, "转化会话/会话；会话缺失或为0时 N/A")
        revenue, cost = values["revenue"], values["cost"]
        measured = nonempty(sources["经营"].get("统计口径"))
        valid = bool(sessions and cost and revenue is not None and measured)
        put("roi", 100 * (revenue - cost) / cost if valid else None, "%",
            revenue - cost if valid else None, cost,
            "(归因收入-成本)/成本；按导出归因口径" if valid else "缺正数会话、正数成本、归因收入或统计口径，ROI N/A")
    return {"开始": start.isoformat(), "结束": end.isoformat(), "天数": (end - start).days + 1,
            "来源": sources, "指标": metrics, "_tables": tables}


def comparison(key, current, previous):
    if previous is None:
        return {"delta": None, "percent": None, "reason": "未提供上期"}
    a, b = current["指标"][key], previous["指标"][key]
    group = GROUPS[key]
    reason = ""
    if a["value"] is None or b["value"] is None:
        reason = "本期或上期指标 N/A"
    elif current["天数"] != previous["天数"]:
        reason = "周期天数不同；不直接比较总量"
    elif a["unit"] != b["unit"]:
        reason = "单位/币种不同"
    else:
        sa, sb = current["来源"][group], previous["来源"][group]
        if sa["覆盖"] != "完整" or sb["覆盖"] != "完整":
            reason = "存在部分数据，先核对覆盖范围"
        elif group == "发布" and (day(sa["数据截至"]) - day(current["结束"])) != (day(sb["数据截至"]) - day(previous["结束"])):
            reason = "发布状态快照的观察延迟不同"
        elif sa.get("统计口径", "") != sb.get("统计口径", ""):
            reason = "统计口径改变"
        elif group in ("AI回答", "经营") and not nonempty(sa.get("统计口径")):
            reason = "未提供可比较的统计口径"
        elif group == "AI回答":
            def panel(p, states=None):
                return Counter((r["平台"], r["问题ID"], r["运行状态"] == "模拟")
                               for r in p["_tables"][group]
                               if states is None or r["运行状态"] in states)
            if panel(current) != panel(previous):
                reason = "AI平台/问题/运行次数/模拟构成改变"
            elif key in ("ai_mentions", "ai_cited", "ai_mention_rate", "ai_citation_rate") and panel(current, {"已完成"}) != panel(previous, {"已完成"}):
                reason = "实际有效回答的平台/问题/运行次数构成改变；不将失败或未运行造成的样本变化算作效果增长"
            elif key in ("sim_cited", "sim_citation_rate") and panel(current, {"模拟"}) != panel(previous, {"模拟"}):
                reason = "模拟有效回答的平台/问题/运行次数构成改变"
    if reason:
        return {"delta": None, "percent": None, "reason": reason}
    delta = a["value"] - b["value"]
    return {"delta": delta, "percent": 100 * delta / b["value"] if b["value"] else None,
            "reason": "上期为0，变化率 N/A" if b["value"] == 0 else ""}


def build(config, base):
    require(isinstance(config, dict), "配置须为 JSON 对象")
    text_field(config, "项目")
    enum(config, "数据性质", ("实际", "模拟"))
    accounts = config.get("账号", [])
    require(isinstance(accounts, list) and all(nonempty(a) for a in accounts), "账号须为非空字符串数组")
    accounts = [account.strip() for account in accounts]
    require(len(accounts) == len(set(accounts)), "账号筛选重复")
    config["账号"] = accounts
    current = aggregate_period(base, config, config.get("本期"))
    previous = aggregate_period(base, config, config["上期"]) if config.get("上期") is not None else None
    if previous:
        require(previous["结束"] < current["开始"], "上期与本期重叠或顺序颠倒")
    comparisons = {k: comparison(k, current, previous) for k in LABELS}
    for p in (current, previous):
        if p:
            p.pop("_tables")
    return {"项目": config["项目"], "数据性质": config["数据性质"], "账号筛选": accounts,
            "范围说明": "文章与AI按项目统计；账号筛选只影响发布和经营；发布为周期内创建记录的状态快照",
            "本期": current, "上期": previous, "比较": comparisons,
            "指标名称": LABELS}


def display(value):
    if value is None:
        return "N/A"
    return round(value, 6) if isinstance(value, float) else value


def csv_safe(value):
    value = display(value)
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def write_outputs(result, output):
    output.mkdir(parents=True, exist_ok=False)
    (output / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    fields = ("项目", "账号范围", "数据性质", "指标", "单位", "本期单位", "上期单位", "本期", "上期", "本期分子", "本期分母",
              "上期分子", "上期分母", "变化量", "变化单位", "变化率(%)", "本期状态", "上期状态", "比较说明", "本期说明", "上期说明")
    with (output / "指标明细.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(fields)
        for key, label in LABELS.items():
            scope = ("项目级（账号筛选不适用）" if GROUPS[key] in ("文章", "AI回答")
                     else "、".join(result["账号筛选"]) or "全部导出账号")
            a = result["本期"]["指标"][key]
            b = result["上期"]["指标"][key] if result["上期"] else {}
            c = result["比较"][key]
            common_unit = a["unit"] if not b or a["unit"] == b["unit"] else "本期/上期不同"
            delta_unit = ("百分点" if a["unit"] == "%" else a["unit"]) if c["delta"] is not None else None
            values = (result["项目"], scope, result["数据性质"], label,
                      common_unit, a["unit"], b.get("unit"), a["value"], b.get("value"), a["numerator"], a["denominator"],
                      b.get("numerator"), b.get("denominator"), c["delta"], delta_unit,
                      c["percent"], a["status"], b.get("status", "N/A"), c["reason"], a["reason"], b.get("reason", "未提供上期"))
            writer.writerow([csv_safe(v) for v in values])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="配置 JSON；数据路径相对于此文件")
    parser.add_argument("--output", required=True, type=Path, help="新建输出目录，已存在则拒绝覆盖")
    args = parser.parse_args(argv)
    try:
        config = json.loads(args.input.read_text(encoding="utf-8-sig"))
        result = build(config, args.input.resolve().parent)
        write_outputs(result, args.output)
    except (DataError, OSError, ValueError, TypeError) as exc:
        print(f"输入错误: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"summary": str(args.output / "summary.json"), "metrics": str(args.output / "指标明细.csv"),
                      "数据性质": result["数据性质"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
