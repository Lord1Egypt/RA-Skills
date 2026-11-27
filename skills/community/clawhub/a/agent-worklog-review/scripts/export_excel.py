#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 token_usage.jsonl + tasks_classified.jsonl 导出为多 sheet XLSX。

借鉴 token-stats 的 XLSX 交付与缓存率口径：
  缓存率 = cache_tokens / total_tokens × 100%
  非缓存 token 沿用本项目 fresh_tokens（汇报建议口径）

费用列可选：config/local/pricing.local.json
  {"模型名": {"input": 0.000001, "output": 0.000002, "cache": 0.0000001}}
  单价单位由使用者自定（通常 USD/token）；不配置则不出现费用列，不臆造价格。

依赖 openpyxl；缺失时只提示不中断主链路。
输出：$OUTPUT_DIR/agent_worklog.xlsx
"""
import os, sys, json, collections, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import out_dir, month_of
from stat_tokens import project_of

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

OUT = out_dir()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEAD_FILL = PatternFill("solid", fgColor="1F4E78") if HAS_OPENPYXL else None
HEAD_FONT = Font(color="FFFFFF", bold=True) if HAS_OPENPYXL else None
TITLE_FONT = Font(bold=True, size=13, color="1F4E78") if HAS_OPENPYXL else None
THIN = Side(style="thin", color="D9D9D9") if HAS_OPENPYXL else None


def load_jsonl(name):
    p = os.path.join(OUT, name)
    rows = []
    if not os.path.isfile(p):
        return rows
    for line in open(p, encoding="utf-8"):
        try:
            rows.append(json.loads(line))
        except Exception:
            continue
    return rows


def load_pricing():
    p = os.path.join(ROOT, "config", "local", "pricing.local.json")
    if not os.path.isfile(p):
        return {}
    try:
        return json.load(open(p, encoding="utf-8")) or {}
    except Exception:
        return {}


def sheet(wb, name, headers, rows, widths=None, number_cols=()):
    ws = wb.create_sheet(name)
    ws.append(headers)
    for c in ws[1]:
        c.fill, c.font = HEAD_FILL, HEAD_FONT
        c.alignment = Alignment(horizontal="center", vertical="center")
    for r in rows:
        ws.append(list(r))
    ws.freeze_panes = "A2"
    for i, h in enumerate(headers, 1):
        letter = get_column_letter(i)
        if widths and i <= len(widths):
            ws.column_dimensions[letter].width = widths[i - 1]
        else:
            longest = max([len(str(h))] + [len(str(r[i - 1])) for r in rows[:200]]) if rows else len(str(h))
            ws.column_dimensions[letter].width = min(max(longest + 2, 10), 42)
    for row in ws.iter_rows(min_row=2):
        for c in row:
            if c.column in number_cols and isinstance(c.value, (int, float)):
                c.number_format = "#,##0"
    return ws


def agg_table(rows, key, pricing=None):
    """按维度聚合 token，返回 (headers, rows)。"""
    d = collections.defaultdict(lambda: [0, 0, 0, 0, 0, 0, 0])
    for r in rows:
        k = r.get(key) or "未知"
        x = d[k]
        x[0] += 1
        x[1] += r.get("input_tokens", 0)
        x[2] += r.get("output_tokens", 0)
        x[3] += r.get("cache_tokens", 0)
        x[4] += r.get("total_tokens", 0)
        x[5] += r.get("fresh_tokens", r.get("total_tokens", 0))
        if pricing:
            p = pricing.get(r.get("model", ""), {})
            x[6] += (r.get("input_tokens", 0) * p.get("input", 0)
                     + r.get("output_tokens", 0) * p.get("output", 0)
                     + r.get("cache_tokens", 0) * p.get("cache", 0))
    headers = ["类别", "会话数", "输入 token", "输出 token", "缓存 token",
               "合计 token", "非缓存 token", "缓存率"]
    if pricing:
        headers.append("估算费用")
    out = []
    for k, v in sorted(d.items(), key=lambda x: -x[1][4]):
        rate = (v[3] / v[4] * 100) if v[4] else 0
        line = [k, v[0], v[1], v[2], v[3], v[4], v[5], round(rate, 1)]
        if pricing:
            line.append(round(v[6], 4))
        out.append(line)
    return headers, out


def main():
    if not HAS_OPENPYXL:
        print("跳过 Excel 导出：未安装 openpyxl（pip install openpyxl 后重跑）")
        return 0

    tokens = load_jsonl("token_usage.jsonl")
    tasks = load_jsonl("tasks_classified.jsonl")
    pricing = load_pricing()
    for r in tokens:
        r["project"] = project_of(r.get("cwd", ""), r.get("title", ""))
        r["month"] = month_of(r.get("timestamp"))

    wb = Workbook()
    wb.remove(wb.active)

    # 1) 总览
    ws = wb.create_sheet("总览")
    total = sum(r.get("total_tokens", 0) for r in tokens)
    fresh = sum(r.get("fresh_tokens", r.get("total_tokens", 0)) for r in tokens)
    cache = sum(r.get("cache_tokens", 0) for r in tokens)
    ws["A1"] = "本机 AI Agent 工作复盘 — 数据总览"
    ws["A1"].font = TITLE_FONT
    ws.append([])
    summary = [
        ("统计时间", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("Token 会话数", len(tokens)),
        ("任务记录数", len(tasks)),
        ("合计 token", total),
        ("非缓存 token（汇报建议口径）", fresh),
        ("缓存 token", cache),
        ("缓存率", f"{cache / total * 100:.1f}%" if total else "0%"),
        ("覆盖 Agent 数", len({r.get("agent") for r in tokens})),
        ("费用列", "已按 config/local/pricing.local.json 估算" if pricing else "未配置定价表，不臆造费用"),
    ]
    for k, v in summary:
        ws.append([k, v])
    ws.append([])
    ws.append(["口径提示", "缓存命中 token 是上下文复用，不等于真实消耗；汇报用量建议用非缓存 token。"])
    ws.append(["统计范围", "仅本机实际产生会话数据的 Agent；未安装/未使用的 Agent 不列入。"])
    ws.append(["数据来源", "本机会话文件只读解析，不联网、无遥测。"])
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 62

    # 2-4) 三个 token 维度
    for name, key in [("按 Agent", "agent"), ("按项目", "project"), ("按月份", "month")]:
        h, rows = agg_table(tokens, key, pricing)
        sheet(wb, name, h, rows, number_cols=tuple(range(2, len(h))))

    # 5) 按模型
    md = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
    for r in tokens:
        if not r.get("model"):
            continue
        x = md[r["model"]]
        x[0] += 1
        x[1] += r.get("input_tokens", 0)
        x[2] += r.get("output_tokens", 0)
        x[3] += r.get("cache_tokens", 0)
        x[4] += r.get("total_tokens", 0)
    sheet(wb, "按模型",
          ["模型", "会话数", "输入 token", "输出 token", "缓存 token", "合计 token"],
          [[k] + v for k, v in sorted(md.items(), key=lambda x: -x[1][4])[:30]],
          number_cols=(2, 3, 4, 5, 6))

    # 6) Top 会话
    top = [[r.get("agent", ""), r.get("project", ""), str(r.get("timestamp", ""))[:19],
            r.get("model", ""), r.get("total_tokens", 0),
            r.get("fresh_tokens", 0), (r.get("title") or "")[:80]]
           for r in sorted(tokens, key=lambda x: -x.get("total_tokens", 0))[:50]]
    sheet(wb, "Top会话", ["Agent", "项目", "时间", "模型", "合计 token", "非缓存 token", "任务标题"],
          top, widths=(18, 22, 21, 26, 16, 16, 60), number_cols=(5, 6))

    # 7) 任务分类
    for dim, label in [("work_type", "工作类型"), ("project", "项目"), ("month", "月份"), ("agent", "Agent")]:
        c = collections.Counter(r.get(dim) or "未知" for r in tasks)
        sheet(wb, f"任务-{label}", [label, "任务数"],
              [[k, v] for k, v in c.most_common()], number_cols=(2,))

    # 8) 明细（便于筛选核对）
    if tasks:
        keys = ["agent", "title", "month", "project", "work_type", "ai_tags", "timestamp", "cwd"]
        rows = [[", ".join(str(x) for x in (r.get(k) or [])) if isinstance(r.get(k), list)
                 else str(r.get(k) or "")[:120] for k in keys] for r in tasks[:5000]]
        sheet(wb, "任务明细", keys, rows)

    path = os.path.join(OUT, "agent_worklog.xlsx")
    wb.save(path)
    print(f"Excel 已导出: {path}  ({os.path.getsize(path)//1024} KB, {len(wb.sheetnames)} sheets)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
