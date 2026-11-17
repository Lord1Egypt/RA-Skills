#!/usr/bin/env python3
"""从 asr-completed 接口 JSON 生成十维拓客洞察 HTML。用法见 SKILL.md。"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_DIMENSIONS: list[dict[str, Any]] = [
    {"name": "拓客场景", "keywords": ["陌拜", "上门", "网点", "电话营销", "进社区", "路演", "扫楼"]},
    {"name": "触达人群", "keywords": ["老板", "客户", "王总", "李总", "朱总", "经理", "主任", "厂长"]},
    {"name": "开口获客话术", "keywords": ["您好", "你好", "打扰", "请问", "方便", "拜访"]},
    {"name": "客户需求", "keywords": ["额度", "利率", "期限", "还款", "资金", "周转", "采购"]},
    {"name": "客户拒绝原因", "keywords": ["不需要", "考虑一下", "没兴趣", "太忙", "再说", "不行"]},
    {"name": "有效意向分类", "keywords": ["有意向", "高意向", "再联系", "签约", "办手续", "尽快"]},
    {"name": "产品匹配", "keywords": ["产品", "贷款", "信贷", "快贷", "杭信贷", "经营贷"]},
    {"name": "成交阻碍痛点", "keywords": ["材料", "抵押", "担保", "审批", "流程", "麻烦", "慢"]},
    {"name": "跟进动作", "keywords": ["回访", "再约", "发资料", "加微信", "明天", "下周"]},
    {"name": "拓客成效数据", "keywords": ["放款", "到账", "批复", "审批通过", "额度批复"]},
]

TRANSCRIPT_KEYS = ("transcript", "asrText", "asr_text", "text", "content", "dialogue", "asrContent")
DATE_KEYS = ("recordTime", "createdAt", "startTime", "recordingTime", "date", "recordDate")


CHART_JS_CDN_PRIMARY = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"
CHART_JS_CDN_FALLBACK = "https://cdn.bootcdn.net/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"
TEMPLATE_NAME = "asr_insight_template.html"

MOBILE_UTF8_HEAD_MARKERS = (
    '<meta charset="utf-8"',
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"',
)


def ensure_mobile_utf8_head(html: str) -> str:
    """手机内嵌浏览器在对象 Content-Type 非 text/html 时依赖 BOM + http-equiv。"""
    if all(m in html for m in MOBILE_UTF8_HEAD_MARKERS):
        return html
    if '<meta charset="utf-8"' in html and "http-equiv" not in html[:2048].lower():
        return html.replace(
            '<meta charset="utf-8" />',
            '<meta charset="utf-8" />\n  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
            1,
        )
    return html


def template_path() -> Path:
    return Path(__file__).resolve().parent.parent / TEMPLATE_NAME


def load_chart_tail(charts_json: str) -> str:
    """从模板提取 Chart.js 与绘图脚本；部署时缺模板会导致图表区空白。"""
    path = template_path()
    if path.is_file():
        base = path.read_text(encoding="utf-8")
        idx = base.find(f'<script src="{CHART_JS_CDN_PRIMARY}"')
        if idx < 0:
            idx = base.find("<script>\n(function ()")
        if idx >= 0:
            tail = base[idx:]
            tail, n = re.subn(
                r"var charts = \[.*?\];",
                f"var charts = {charts_json};",
                tail,
                count=1,
                flags=re.DOTALL,
            )
            if n == 0:
                tail = tail.replace(
                    "(function () {",
                    f"(function () {{\n  var charts = {charts_json};",
                    1,
                )
            if CHART_JS_CDN_FALLBACK not in tail:
                tail = tail.replace(
                    'crossorigin="anonymous"></script>',
                    f"crossorigin=\"anonymous\" onerror=\"this.onerror=null;this.src='{CHART_JS_CDN_FALLBACK}'\"></script>",
                    1,
                )
            return tail
    return (
        f'  <script src="{CHART_JS_CDN_PRIMARY}" crossorigin="anonymous" '
        f"onerror=\"this.onerror=null;this.src='{CHART_JS_CDN_FALLBACK}'\"></script>\n"
        f"  <p class=\"chart-note\">图表脚本未找到（缺少 {TEMPLATE_NAME}），请查看上方统计表。</p>\n"
        "</body></html>"
    )


def read_input_text(input_path: str | None) -> str:
    """接口 JSON 固定按 UTF-8 读取；stdin 也用 UTF-8，避免 Windows 默认 GBK 导致中文乱码。"""
    if input_path:
        return Path(input_path).read_text(encoding="utf-8-sig")
    return sys.stdin.buffer.read().decode("utf-8")


def load_api_payload(raw: str) -> dict[str, Any]:
    data = json.loads(raw)
    if "data" in data and isinstance(data["data"], dict):
        return data
    if "records" in data:
        return {"code": 0, "msg": "success", "data": data}
    raise ValueError("无法识别的 JSON：需要完整接口响应或含 records 的 data 对象")


def get_transcript(rec: dict[str, Any]) -> str:
    for k in TRANSCRIPT_KEYS:
        v = rec.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return ""


def get_record_day(rec: dict[str, Any]) -> str | None:
    for k in DATE_KEYS:
        v = rec.get(k)
        if not v:
            continue
        s = str(v)
        m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
        if m:
            return m.group(1)
    return None


def get_file_alias(rec: dict[str, Any]) -> str:
    """获取录音名称，优先使用 fileAlias，为空时返回空字符串。"""
    v = rec.get("fileAlias")
    if v is not None and str(v).strip():
        return str(v).strip()
    return ""


def first_keyword_hit(text: str, keywords: list[str]) -> str | None:
    for kw in keywords:
        if kw and kw in text:
            return kw
    return None


def excerpt_snippet(text: str, keyword: str, max_len: int = 120) -> str:
    idx = text.find(keyword)
    if idx < 0:
        return text[:max_len] + ("…" if len(text) > max_len else "")
    start = max(0, idx - 40)
    end = min(len(text), idx + len(keyword) + 80)
    snippet = text[start:end]
    if start > 0:
        snippet = "…" + snippet
    if end < len(text):
        snippet += "…"
    return snippet


def analyze(records: list[dict[str, Any]], dimensions: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(records)
    dim_stats: list[dict[str, Any]] = []
    daily_counts: dict[str, int] = defaultdict(int)
    undated = 0

    for rec in records:
        day = get_record_day(rec)
        if day:
            daily_counts[day] += 1
        else:
            undated += 1

    sorted_days = sorted(daily_counts.keys())
    daily_dim_hits: dict[str, dict[str, int]] = {d: defaultdict(int) for d in sorted_days}

    for dim in dimensions:
        name = dim["name"]
        keywords = dim.get("keywords") or []
        hit_indices: list[int] = []
        excerpts: list[tuple[str, str]] = []

        for i, rec in enumerate(records):
            text = get_transcript(rec)
            if not text:
                continue
            kw = first_keyword_hit(text, keywords)
            if kw:
                hit_indices.append(i)
                file_alias = get_file_alias(rec)
                excerpts.append((kw, excerpt_snippet(text, kw), file_alias))
                day = get_record_day(rec)
                if day and day in daily_dim_hits:
                    daily_dim_hits[day][name] += 1

        hit_count = len(hit_indices)
        coverage = round(100.0 * hit_count / n, 1) if n else 0.0
        dim_stats.append(
            {
                "name": name,
                "keywords": keywords,
                "hit_count": hit_count,
                "coverage": coverage,
                "excerpts": excerpts[:5],
            }
        )

    covered_dims = sum(1 for d in dim_stats if d["hit_count"] > 0)
    top_dims = sorted(dim_stats, key=lambda x: x["hit_count"], reverse=True)[:5]
    series = []
    for d in top_dims:
        if d["hit_count"] == 0:
            continue
        data = [daily_dim_hits[day].get(d["name"], 0) for day in sorted_days]
        series.append({"name": d["name"], "data": data})

    volume_values = [daily_counts[d] for d in sorted_days]
    coverage_values = [d["coverage"] for d in dim_stats]
    dim_names = [d["name"] for d in dim_stats]

    charts = [
        {
            "id": "volume-trend",
            "type": "line",
            "title": "录音样本量按日变化",
            "labels": sorted_days,
            "values": volume_values,
            "meta": {"undatedRecords": undated, "aggregated": None},
        },
        {
            "id": "dimension-radar",
            "type": "radar",
            "title": "各维度覆盖率全景",
            "labels": dim_names,
            "values": coverage_values,
            "meta": {},
        },
        {
            "id": "dimension-coverage",
            "type": "bar",
            "title": "各维度关键词覆盖率",
            "labels": dim_names,
            "values": coverage_values,
            "meta": {"preferHorizontalOnMobile": True},
        },
    ]
    if series and sorted_days:
        charts.append(
            {
                "id": "dimension-hits-trend",
                "type": "line",
                "title": "各维度命中数变化趋势（Top 维度）",
                "labels": sorted_days,
                "series": series,
                "meta": {"undatedRecords": undated, "aggregated": None},
            }
        )

    return {
        "total": n,
        "covered_dims": covered_dims,
        "dim_count": len(dimensions),
        "dim_stats": dim_stats,
        "charts": charts,
        "sorted_days": sorted_days,
        "undated": undated,
    }


def render_dimension_card(stat: dict[str, Any], total: int) -> str:
    name = html.escape(stat["name"])
    hit = stat["hit_count"]
    cov = stat["coverage"]
    if hit == 0:
        findings = f"在 {total} 条转写中未识别到与本维度强相关的关键词，建议结合上下文人工复核。"
        excerpts_html = '<p class="muted">暂无典型摘录。</p>'
        suggest = "可补充针对性话术或场景演练。"
    else:
        findings = (
            f"在 {hit}/{total} 条录音（覆盖率 {cov:.1f}%）中出现与「{name}」相关的表述。"
        )
        items = []
        for tag, snippet, file_alias in stat["excerpts"]:
            alias_display = html.escape(file_alias) if file_alias else ""
            alias_html = f'<span class="record-name">[{alias_display}]</span> ' if alias_display else ""
            items.append(
                f'<li>{alias_html}<span class="tag">{html.escape(tag)}</span>'
                f"{html.escape(snippet)}</li>"
            )
        excerpts_html = f'<ul class="excerpts">{"".join(items)}</ul>' if items else '<p class="muted">暂无典型摘录。</p>'
        suggest = "建议沉淀高频表述为可复用话术，并在复盘会中对照录音强化。"

    return f"""<section class="card">
  <h2>{name}</h2>
  <p class="findings">{html.escape(findings)}</p>
  <p class="metrics"><strong>命中录音</strong> {hit} · <strong>覆盖率</strong> {cov:.1f}%</p>
  {excerpts_html}
  <p class="suggest"><strong>建议</strong> {html.escape(suggest)}</p>
</section>"""


def build_html(
    analysis: dict[str, Any],
    *,
    window_label: str,
    user_id: str,
    generated_at: str,
) -> str:
    total = analysis["total"]
    dim_stats = analysis["dim_stats"]
    covered = analysis["covered_dims"]
    dim_count = analysis["dim_count"]

    table_rows = "".join(
        f'<tr><td>{html.escape(d["name"])}</td>'
        f'<td class="num">{d["coverage"]:.1f}%</td>'
        f'<td class="num">{d["hit_count"]}</td></tr>'
        for d in dim_stats
    )
    cards = "".join(render_dimension_card(d, total) for d in dim_stats)

    chart_cards = []
    for ch in analysis["charts"]:
        cid = ch["id"]
        chart_cards.append(
            f"""    <div class="chart-card{" chart-card-wide" if "dimension" in cid else ""}">
      <h3>{html.escape(ch["title"])}</h3>
      <div class="chart-canvas-wrap" data-chart-id="{html.escape(cid)}">
        <canvas id="chart-{html.escape(cid)}" role="img" aria-label="{html.escape(ch["title"])}"></canvas>
      </div>
    </div>"""
        )

    framework = "十维拓客框架" if dim_count == 10 else f"选定的 {dim_count} 个分析维度"
    summary = (
        f"基于 {total} 条 ASR 转写，按{framework}完成统计；"
        f"{covered}/{dim_count} 个维度在样本中出现相关表述。"
    )
    title = report_title(dim_count)
    meta_line = (
        f"统计窗口：{html.escape(window_label)} · 样本 {total} 条录音转写 · "
        f"分析维度 {dim_count} 项 · 维度覆盖 {covered}/{dim_count}"
    )
    charts_json = json.dumps(analysis["charts"], ensure_ascii=False)

    tpl = template_path()
    head_part = ""
    if tpl.is_file():
        base = tpl.read_text(encoding="utf-8")
        head_end = base.find("</head>")
        if head_end > 0:
            head_part = base[: head_end + len("</head>")]

    if not head_part:
        head_part = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <title>十维拓客 · 录音转写洞察报告</title>
  <style>body{font-family:system-ui,sans-serif;margin:0;padding:16px;}</style>
</head>"""

    body = f"""<body>
  <div class="wrap">
    <header>
      <h1>{html.escape(title)}</h1>
      <div class="meta">{meta_line}</div>
    </header>
    <div class="summary">
      <h2>执行摘要</h2>
      <p>{html.escape(summary)}</p>
    </div>
    <section class="dim-table-panel card">
  <h2>各维度统计一览</h2>
  <p class="charts-intro">下表与图表数据一致，便于手机端快速浏览；详细摘录见下方分维度说明。</p>
  <div class="table-scroll" role="region" aria-label="各维度统计表" tabindex="0">
    <table class="dim-table">
      <thead><tr><th>维度</th><th>覆盖率</th><th>命中条数</th></tr></thead>
      <tbody>{table_rows}</tbody>
    </table>
  </div>
</section>
    <section class="charts-panel">
  <h2>各维度数据图表</h2>
  <p class="charts-intro">基于 ASR 转写按维度关键词与录音时间统计；页面已适配电脑与手机浏览器，可横屏查看趋势图。</p>
  <div class="chart-grid">
{chr(10).join(chart_cards)}
</div>
</section>
    {cards}
    <footer>本报告依据 ASR 转写自动生成；图表为各维度关键词命中与录音日分布统计，已适配电脑与手机浏览。结论请结合下方摘录复核。生成时间 {html.escape(generated_at)}</footer>
  </div>
"""

    chart_tail = load_chart_tail(charts_json)
    return ensure_mobile_utf8_head(head_part + "\n" + body + "\n  " + chart_tail.lstrip())


def select_dimensions_by_names(names: list[str]) -> list[dict[str, Any]]:
    """从默认十维中按名称筛选子集，保留 DIMENSIONS 表中的顺序。"""
    if not names:
        return list(DEFAULT_DIMENSIONS)
    wanted = {n.strip() for n in names if n.strip()}
    if not wanted:
        return list(DEFAULT_DIMENSIONS)
    catalog = {d["name"]: d for d in DEFAULT_DIMENSIONS}
    missing = sorted(wanted - set(catalog.keys()))
    if missing:
        available = "、".join(d["name"] for d in DEFAULT_DIMENSIONS)
        raise ValueError(f"未知维度：{'、'.join(missing)}。可选：{available}")
    return [catalog[n] for n in (d["name"] for d in DEFAULT_DIMENSIONS) if n in wanted]


def report_title(dim_count: int) -> str:
    if dim_count == 10:
        return "十维拓客 · 录音转写洞察报告"
    return f"{dim_count}维分析 · 录音转写洞察报告"


def _fmt_window_part(value: str) -> str:
    """将接口返回日期（ISO 或 YYYY-MM-DD 或 YYYYMMDD）规范为 YYYY-MM-DD 展示。"""
    s = str(value).strip()
    if len(s) == 8 and s.isdigit():
        return f"{s[:4]}-{s[4:6]}-{s[6:8]}"
    if len(s) >= 10 and s[4] == "-":
        return s[:10]
    return s


def format_window(data: dict[str, Any]) -> str:
    st = data.get("startTime") or ""
    et = data.get("endTime") or ""
    if st and et:
        return f"{_fmt_window_part(st)} 至 {_fmt_window_part(et)}"
    return "接口默认窗口"


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 ASR 十维拓客洞察 HTML")
    parser.add_argument(
        "-i",
        "--input",
        help="接口 JSON 文件路径；省略则从 stdin 读取",
    )
    parser.add_argument("-o", "--output", required=True, help="输出 HTML 路径")
    parser.add_argument(
        "--dimensions",
        help="自定义维度 JSON 文件（数组，元素含 name、keywords）；与 --only 二选一",
    )
    parser.add_argument(
        "--only",
        action="append",
        metavar="NAME",
        help="仅分析指定维度（可重复或逗号分隔），名称须与默认十维一致，如：客户需求 跟进动作",
    )
    parser.add_argument(
        "--write-meta",
        metavar="PATH",
        help="写出交付元数据 JSON（供 publish_asr_report.py --meta 使用）",
    )
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                pass

    raw = read_input_text(args.input)
    payload = load_api_payload(raw)
    if payload.get("code") not in (0, "0", None) and payload.get("code") != 0:
        print(f"业务失败: code={payload.get('code')} msg={payload.get('msg')}", file=sys.stderr)
        return 2

    data = payload.get("data") or {}
    records = data.get("records") or []
    if not isinstance(records, list):
        print("data.records 不是数组", file=sys.stderr)
        return 2

    if len(records) == 0:
        print(
            "录音条数为 0，不生成 HTML。请直接向用户说明无样本并建议核对 agentid 或调整时间范围。",
            file=sys.stderr,
        )
        return 3

    if args.dimensions and args.only:
        print("请只使用 --dimensions 或 --only 之一", file=sys.stderr)
        return 2

    if args.dimensions:
        dimensions = json.loads(Path(args.dimensions).read_text(encoding="utf-8"))
    elif args.only:
        names: list[str] = []
        for chunk in args.only:
            names.extend(p.strip() for p in chunk.replace("，", ",").split(",") if p.strip())
        try:
            dimensions = select_dimensions_by_names(names)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            return 2
    else:
        dimensions = list(DEFAULT_DIMENSIONS)

    analysis = analyze(records, dimensions)
    html_out = build_html(
        analysis,
        window_label=format_window(data),
        user_id=str(data.get("userId") or ""),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    out_path = Path(args.output)
    # build_html 已含 ensure_mobile_utf8_head；此处仅写 BOM 供手机浏览器识别 UTF-8
    out_path.write_text(html_out, encoding="utf-8-sig")
    dim_count = analysis["dim_count"]
    covered = analysis["covered_dims"]
    total = analysis["total"]
    framework = "十维拓客框架" if dim_count == 10 else f"选定的 {dim_count} 个分析维度"
    executive_summary = (
        f"基于 {total} 条 ASR 转写，按{framework}完成统计；"
        f"{covered}/{dim_count} 个维度在样本中出现相关表述。"
    )
    if args.write_meta:
        meta_path = Path(args.write_meta)
        meta_path.write_text(
            json.dumps(
                {
                    "title": report_title(dim_count),
                    "executiveSummary": executive_summary,
                    "recordCount": total,
                    "covered_dims": covered,
                    "dim_count": dim_count,
                    "window_label": format_window(data),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    print(
        f"Wrote {out_path} ({len(records)} records, {covered}/{dim_count} dims covered)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
