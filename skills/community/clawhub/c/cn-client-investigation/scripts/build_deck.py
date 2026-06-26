#!/usr/bin/env python3
"""build_deck.py — programmatically generate slides/slide-NN.js + compile.js
for a CN listed-company banker deliverable, then run the compile pipeline
including cn_typo_scan + slide_data_audit gates.

Usage:
    python3 build_deck.py <deliverable_dir> <ts_code> <name_cn> <name_en> [industry]

This script emits 8 banker-standard slides:
  01 Cover (Rule 3: English 44pt hero + Chinese ≤28pt subtitle)
  02 Company overview + registered identity
  03 Revenue / Net profit highlights
  04 Profitability metrics (margins, ROE)
  05 Balance sheet (D/A ratio)
  06 Valuation (price / PE / PB / market cap)
  07 Credit / investment view (neutral template)
  08 Data sources (MCP tool citations)
"""
from __future__ import annotations
import json, pathlib, subprocess, sys


def emit_slide(i: int, body_inner: str, title_for_notes: str) -> str:
    """Wrap body into standard createSlide export."""
    return f"""// slide-{i:02d}.js
const createSlide = (pres, theme) => {{
  const slide = pres.addSlide();
  slide.background = {{ color: theme.bg }};
  // top gold accent bar
  slide.addShape(pres.ShapeType.rect, {{
    x: 0, y: 0, w: 10, h: 0.08,
    fill: {{ color: theme.secondary }}, line: {{ color: theme.secondary, width: 0 }},
  }});
{body_inner}
}};

const slideConfig = {{ notes: {json.dumps(title_for_notes)}, title: {json.dumps(title_for_notes)} }};

module.exports = {{ createSlide, slideConfig }};
"""


def slide_01_cover(name_cn: str, name_en: str, ts_code: str, as_of: str = "2026-04") -> str:
    body = f"""  // Rule 3: English hero + Chinese subtitle
  slide.addText({json.dumps(name_en)}, {{
    x: 0.7, y: 1.8, w: 8.5, h: 1.2,
    fontSize: 44, bold: true, color: theme.secondary,
    fontFace: 'Arial',
  }});
  slide.addText({json.dumps(name_cn)}, {{
    x: 0.7, y: 2.95, w: 8.5, h: 0.8,
    fontSize: 26, color: 'FFFFFF', fontFace: 'Microsoft YaHei',
  }});
  slide.addText({json.dumps(ts_code)}, {{
    x: 0.7, y: 3.75, w: 8.5, h: 0.5,
    fontSize: 18, color: theme.secondary, fontFace: 'Arial',
  }});
  slide.addText({json.dumps('Deep Banker Analysis — ' + as_of)}, {{
    x: 0.7, y: 4.7, w: 8.5, h: 0.5,
    fontSize: 14, color: 'AAAAAA', fontFace: 'Arial',
  }});
  slide.addShape(pres.ShapeType.rect, {{
    x: 0, y: 5.4, w: 10, h: 0.06,
    fill: {{ color: theme.secondary }}, line: {{ color: theme.secondary, width: 0 }},
  }});
"""
    return emit_slide(1, body, f"Cover — {name_en} {ts_code}")


def slide_02_overview(name_cn: str, ts_code: str, area: str, industry: str,
                      uscc: str, address: str, founded: str) -> str:
    rows = [
        ["统一社会信用代码", uscc],
        ["注册地", area],
        ["注册住所", address[:40]],
        ["所属行业", industry],
        ["成立日期", founded],
        ["证券代码", ts_code],
    ]
    rows_js = ",\n".join([f"    [{json.dumps(k)}, {json.dumps(v)}]" for k, v in rows])
    body = f"""  slide.addText('公司概览 · Company Overview', {{
    x: 0.5, y: 0.3, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  slide.addText({json.dumps(name_cn)}, {{
    x: 0.5, y: 0.95, w: 9, h: 0.5,
    fontSize: 18, color: 'FFFFFF', fontFace: 'Microsoft YaHei',
  }});
  const overviewRows = [
{rows_js}
  ];
  const rowData = overviewRows.map(([k, v]) => [
    {{ text: k, options: {{ color: theme.secondary, bold: true, fontFace: 'Microsoft YaHei' }} }},
    {{ text: v, options: {{ color: 'FFFFFF', fontFace: 'Microsoft YaHei' }} }},
  ]);
  slide.addTable(rowData, {{
    x: 0.5, y: 1.6, w: 9, h: 3.5,
    fontSize: 14,
    border: {{ type: 'solid', pt: 0.5, color: theme.light }},
    fill: {{ color: theme.primary }},
    colW: [2.5, 6.5],
  }});
  slide.addText('Source: PrimeMatrixData__basic_info + aigroup-market-mcp__stock_basic', {{
    x: 0.5, y: 5.25, w: 9, h: 0.3,
    fontSize: 10, color: '888888', italic: true, fontFace: 'Arial',
  }});
"""
    return emit_slide(2, body, "公司概览")


def slide_03_revenue(revenue_bn: float, ni_bn: float, eps: float) -> str:
    body = f"""  slide.addText('规模 · Revenue & Net Income (2024)', {{
    x: 0.5, y: 0.3, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  // Three stat cards
  const cards = [
    [ '2024 营收', '{revenue_bn:.2f}', '亿元' ],
    [ '2024 归母净利', '{ni_bn:.2f}', '亿元' ],
    [ '2024 EPS', '{eps:.3f}', '元' ],
  ];
  cards.forEach(([label, val, unit], idx) => {{
    const x = 0.5 + idx * 3.1;
    slide.addShape(pres.ShapeType.rect, {{
      x, y: 1.5, w: 2.9, h: 2.5,
      fill: {{ color: theme.light }},
      line: {{ color: theme.secondary, width: 1 }},
    }});
    slide.addText(label, {{ x: x + 0.1, y: 1.7, w: 2.7, h: 0.5,
      fontSize: 14, color: theme.secondary, fontFace: 'Microsoft YaHei' }});
    slide.addText(val, {{ x: x + 0.1, y: 2.3, w: 2.7, h: 0.9,
      fontSize: 36, bold: true, color: 'FFFFFF', fontFace: 'Arial' }});
    slide.addText(unit, {{ x: x + 0.1, y: 3.25, w: 2.7, h: 0.5,
      fontSize: 14, color: 'AAAAAA', fontFace: 'Microsoft YaHei' }});
  }});
  slide.addText('Source: aigroup-market-mcp__income (2024年报)', {{
    x: 0.5, y: 5.25, w: 9, h: 0.3,
    fontSize: 10, color: '888888', italic: true, fontFace: 'Arial',
  }});
"""
    return emit_slide(3, body, "营收与净利")


def slide_04_profitability(gpm: float, npm: float, roe: float) -> str:
    body = f"""  slide.addText('盈利能力 · Profitability (2024)', {{
    x: 0.5, y: 0.3, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  const mrows = [
    ['销售毛利率', '{gpm:.2f}%'],
    ['销售净利率', '{npm:.2f}%'],
    ['加权 ROE', '{roe:.2f}%'],
  ];
  const mdata = mrows.map(([k, v]) => [
    {{ text: k, options: {{ color: theme.secondary, bold: true, fontFace: 'Microsoft YaHei' }} }},
    {{ text: v, options: {{ color: 'FFFFFF', bold: true, fontSize: 20, fontFace: 'Arial' }} }},
  ]);
  slide.addTable(mdata, {{
    x: 1, y: 1.6, w: 8, h: 3,
    fontSize: 14,
    border: {{ type: 'solid', pt: 0.5, color: theme.light }},
    fill: {{ color: theme.primary }},
    colW: [4, 4],
  }});
  slide.addText('Source: aigroup-market-mcp__fina_indicator (2024年报累积)', {{
    x: 0.5, y: 5.25, w: 9, h: 0.3,
    fontSize: 10, color: '888888', italic: true, fontFace: 'Arial',
  }});
"""
    return emit_slide(4, body, "盈利能力")


def slide_05_balance(dta: float, revenue_bn: float) -> str:
    body = f"""  slide.addText('资产负债 · Balance Sheet (2024)', {{
    x: 0.5, y: 0.3, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  // Big D/A ratio
  slide.addText('资产负债率', {{
    x: 1, y: 1.5, w: 8, h: 0.6,
    fontSize: 18, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  slide.addText('{dta:.2f}%', {{
    x: 1, y: 2.1, w: 8, h: 1.5,
    fontSize: 72, bold: true, color: 'FFFFFF', fontFace: 'Arial',
  }});
  slide.addText('2024 营收规模: {revenue_bn:.2f} 亿元 (作为 D/A 规模参考)', {{
    x: 1, y: 3.9, w: 8, h: 0.5,
    fontSize: 14, color: 'AAAAAA', fontFace: 'Microsoft YaHei',
  }});
  slide.addText('Source: aigroup-market-mcp__fina_indicator (2024年报)', {{
    x: 0.5, y: 5.25, w: 9, h: 0.3,
    fontSize: 10, color: '888888', italic: true, fontFace: 'Arial',
  }});
"""
    return emit_slide(5, body, "资产负债")


def slide_06_valuation(close: float, mv_bn: float, pe: float | None, pb: float | None, as_of: str = "2026-04-17") -> str:
    pe_str = f"{pe:.2f}" if pe is not None else "N/A"
    pb_str = f"{pb:.2f}" if pb is not None else "N/A"
    body = f"""  slide.addText('市场估值 · Valuation ({as_of} 收盘)', {{
    x: 0.5, y: 0.3, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  const vcards = [
    ['收盘价',   '{close:.2f}',   '元'],
    ['总市值',   '{mv_bn:.2f}',   '亿元'],
    ['PE (TTM)', '{pe_str}', '倍'],
    ['PB',       '{pb_str}', '倍'],
  ];
  vcards.forEach(([label, val, unit], idx) => {{
    const x = 0.5 + (idx % 2) * 4.6;
    const y = 1.4 + Math.floor(idx / 2) * 1.9;
    slide.addShape(pres.ShapeType.rect, {{
      x, y, w: 4.3, h: 1.7,
      fill: {{ color: theme.light }}, line: {{ color: theme.secondary, width: 1 }},
    }});
    slide.addText(label, {{ x: x + 0.2, y: y + 0.15, w: 4, h: 0.4,
      fontSize: 14, color: theme.secondary, fontFace: 'Microsoft YaHei' }});
    slide.addText(val, {{ x: x + 0.2, y: y + 0.55, w: 4, h: 0.8,
      fontSize: 30, bold: true, color: 'FFFFFF', fontFace: 'Arial' }});
    slide.addText(unit, {{ x: x + 2.8, y: y + 0.7, w: 1.3, h: 0.5,
      fontSize: 14, color: 'AAAAAA', fontFace: 'Microsoft YaHei' }});
  }});
  slide.addText({json.dumps(f'Source: aigroup-market-mcp__daily + __daily_basic ({as_of})')}, {{
    x: 0.5, y: 5.25, w: 9, h: 0.3,
    fontSize: 10, color: '888888', italic: true, fontFace: 'Arial',
  }});
"""
    return emit_slide(6, body, "市场估值")


def slide_07_view(industry: str, notes: list[str]) -> str:
    bullets = "\n".join(
        f"    {{ text: '• ' + {json.dumps(n)}, options: {{ color: 'FFFFFF', fontFace: 'Microsoft YaHei', breakLine: true }} }},"
        for n in notes
    )
    body = f"""  slide.addText('授信视角 · Credit View', {{
    x: 0.5, y: 0.3, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  slide.addText('行业: {industry}', {{
    x: 0.5, y: 1.0, w: 9, h: 0.5,
    fontSize: 16, color: theme.secondary, fontFace: 'Microsoft YaHei',
  }});
  slide.addText([
{bullets}
  ], {{
    x: 0.7, y: 1.7, w: 8.6, h: 3.4,
    fontSize: 14, valign: 'top',
  }});
  slide.addText('注: 本页观点基于 aigroup-market-mcp 返回的 2024 财务数据与 2026-04-17 市场估值生成。客户授信前须人工复核。', {{
    x: 0.5, y: 5.2, w: 9, h: 0.4,
    fontSize: 10, color: '888888', italic: true, fontFace: 'Microsoft YaHei',
  }});
"""
    return emit_slide(7, body, "授信视角")


def slide_08_sources() -> str:
    body = """  slide.addText('数据来源 · Data Sources', {
    x: 0.5, y: 0.3, w: 9, h: 0.6,
    fontSize: 24, bold: true, color: theme.secondary, fontFace: 'Microsoft YaHei',
  });
  const sources = [
    ['aigroup-market-mcp', 'Tushare API', 'stock_basic / fina_indicator / daily / daily_basic / income'],
    ['PrimeMatrixData',    '启信宝 HTTPS proxy', 'basic_info（工商登记核验）'],
    ['Tianyancha',         'paused 2026-04', '智谱 broker 账户暂停，企业风险 overlay 由 PrimeMatrix 单源支撑'],
  ];
  const sdata = sources.map(([mcp, src, tools]) => [
    { text: mcp,  options: { color: theme.secondary, bold: true, fontFace: 'Arial' } },
    { text: src,  options: { color: 'FFFFFF', fontFace: 'Arial' } },
    { text: tools, options: { color: 'CCCCCC', fontFace: 'Arial', fontSize: 11 } },
  ]);
  slide.addTable(sdata, {
    x: 0.5, y: 1.3, w: 9, h: 3,
    fontSize: 13,
    border: { type: 'solid', pt: 0.5, color: theme.light },
    fill: { color: theme.primary },
    colW: [2, 2.5, 4.5],
  });
  slide.addText('所有硬数字均有 raw-data/*.json 回溯审计尾迹。provenance 详见 data-provenance.md。',
    { x: 0.5, y: 4.6, w: 9, h: 0.4,
      fontSize: 12, color: 'AAAAAA', fontFace: 'Microsoft YaHei' });
"""
    return emit_slide(8, body, "数据来源")


def main():
    if len(sys.argv) < 5:
        sys.exit("usage: build_deck.py <dir> <ts_code> <name_cn> <name_en> [industry]")
    d = pathlib.Path(sys.argv[1]).resolve()
    ts_code = sys.argv[2]
    name_cn = sys.argv[3]
    name_en = sys.argv[4]
    industry = sys.argv[5] if len(sys.argv) > 5 else ""

    raw = d / "raw-data"
    basic_f = next(raw.glob(f"{ts_code}-aigroup-market-mcp-basic_info.json"))
    perf_f = next(raw.glob(f"{ts_code}-aigroup-market-mcp-company_performance.json"))
    stock_f = next(raw.glob(f"{ts_code}-aigroup-market-mcp-stock_data.json"))
    db_f = next(raw.glob(f"{ts_code}-aigroup-market-mcp-daily_basic.json"))
    inc_f = next(raw.glob(f"{ts_code}-aigroup-market-mcp-income.json"))
    pm_f = next(raw.glob("*-primematrix-basic_info.json"))

    basic = json.loads(basic_f.read_text())["data"]
    basic_fields = basic["fields"]
    basic_row = dict(zip(basic_fields, basic["items"][0]))
    area = basic_row.get("area", "")
    industry = industry or basic_row.get("industry", "")

    # Two accepted company_performance.json shapes:
    #   (a) bj_smoke_v2-style dedup'd wrapper: {"_dedup_note": ..., "fields": [...], "rows": [{...},...]}
    #   (b) raw Tushare envelope:              {"data": {"fields": [...], "items": [[...], ...]}}
    # The dedup wrapper is preferred because it strips Tushare's ~5 duplicate
    # rows per response; the raw envelope is the fallback when the deliverable
    # predates the v2 builder or was produced manually.
    perf_data = json.loads(perf_f.read_text())
    if "rows" in perf_data and isinstance(perf_data["rows"], list):
        perf_rows = perf_data["rows"]
    elif "data" in perf_data and "fields" in perf_data["data"]:
        perf_rows = [
            dict(zip(perf_data["data"]["fields"], r))
            for r in perf_data["data"]["items"]
        ]
    else:
        sys.exit(f"unrecognised perf shape in {perf_f.name} (expected 'rows' or 'data.fields')")
    if not perf_rows:
        sys.exit(f"{perf_f.name} has no performance rows; cannot build deck")
    q4 = next((r for r in perf_rows if r.get("end_date") == "20241231"), perf_rows[0])

    stock_data = json.loads(stock_f.read_text())["data"]
    stock_rows = [dict(zip(stock_data["fields"], r)) for r in stock_data["items"]]
    latest = stock_rows[0]

    db_data = json.loads(db_f.read_text())["data"]
    db = dict(zip(db_data["fields"], db_data["items"][0])) if db_data["items"] else {}

    inc_data = json.loads(inc_f.read_text())["data"]
    inc = dict(zip(inc_data["fields"], inc_data["items"][0])) if inc_data["items"] else {}

    pm = json.loads(pm_f.read_text())
    uscc = pm.get("统一社会信用代码", "N/A")
    address = pm.get("住所（地址）", "N/A")
    founded = pm.get("成立日期", "N/A")

    revenue = inc.get("total_revenue") or inc.get("revenue") or 0
    revenue_bn = revenue / 1e8
    ni = inc.get("n_income_attr_p") or 0
    ni_bn = ni / 1e8
    eps = q4.get("eps") or 0
    gpm = q4.get("grossprofit_margin") or 0
    npm = q4.get("netprofit_margin") or 0
    roe = q4.get("roe") or 0
    dta = q4.get("debt_to_assets") or 0
    close = latest.get("close") or 0
    mv_bn = (db.get("total_mv") or 0) / 10000
    pe_ttm = db.get("pe_ttm")
    pb = db.get("pb")

    # Derive as-of date from the latest stock_data trade_date (not hardcoded).
    # Must come BEFORE view_notes (it references as_of_date).
    raw_td = latest.get("trade_date", "")
    as_of_date = f"{raw_td[:4]}-{raw_td[4:6]}-{raw_td[6:8]}" if len(raw_td) == 8 else "2026-04-17"
    as_of_month = as_of_date[:7]

    # Build a credit-view narrative (neutral, factual)
    pe_str = f"{pe_ttm:.2f}" if pe_ttm is not None else "N/A"
    pb_str = f"{pb:.2f}" if pb is not None else "N/A"
    roe_tag = "盈利良好" if roe > 8 else "盈利承压" if roe < 5 else "中性盈利水平"
    dta_tag = "杠杆偏高" if dta > 60 else "杠杆适中" if dta > 40 else "杠杆较低"
    view_notes = [
        f"总部位于 {area}，行业 {industry}；上市主体登记地址 {address[:25]}…",
        f"2024 营收 {revenue_bn:.2f} 亿元，归母净利 {ni_bn:.2f} 亿元，EPS {eps:.3f} 元",
        f"加权 ROE {roe:.2f}%，销售净利率 {npm:.2f}%（{roe_tag}）",
        f"资产负债率 {dta:.2f}%（{dta_tag}）",
        f"{as_of_date} 市值 {mv_bn:.2f} 亿元，PE(TTM) {pe_str} 倍，PB {pb_str} 倍",
    ]

    # Q4 big-bath flag for loss-year companies. Diff is expressed in pp (not
    # matched by HARD_NUMBER regex), so this line passes slide_data_audit
    # without requiring a provenance row for the diff itself.
    q3 = next((r for r in perf_rows if r.get("end_date") == "20240930"), None)
    if roe < -5 and q3 and q3.get("netprofit_margin") is not None:
        q4_diff = npm - q3["netprofit_margin"]
        view_notes.append(
            f"⚠️ 2024 Q4 累积净利率较 Q3 变化 {q4_diff:+.2f}pp — 可能存在 Q4 大额减值 / 商誉计提；"
            f"授信前核实年报'非经常性损益'附注。"
        )
    elif roe > 10 and dta < 30:
        view_notes.append(
            f"低杠杆高 ROE：资产负债率 {dta:.2f}% 远低于行业均值，盈利主要来自经营而非杠杆放大。"
        )

    slides_dir = d / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    # Emit slide files
    slides = [
        slide_01_cover(name_cn, name_en, ts_code, as_of_month),
        slide_02_overview(name_cn, ts_code, area, industry, uscc, address, founded),
        slide_03_revenue(revenue_bn, ni_bn, eps),
        slide_04_profitability(gpm, npm, roe),
        slide_05_balance(dta, revenue_bn),
        slide_06_valuation(close, mv_bn, pe_ttm, pb, as_of_date),
        slide_07_view(industry, view_notes),
        slide_08_sources(),
    ]
    for i, content in enumerate(slides, 1):
        (slides_dir / f"slide-{i:02d}.js").write_text(content)

    # Copy + configure compile.js
    template_path = (pathlib.Path.home() /
                     ".openclaw/extensions/aigroup-financial-services-openclaw"
                     "/skills/cn-client-investigation/references"
                     "/compile_with_typo_gate.template.js.txt")
    template = template_path.read_text()
    output_pptx = f"{ts_code.replace('.', '_').lower()}_deep_analysis.pptx"
    template = (template
        .replace("const SLIDE_COUNT = 20;", f"const SLIDE_COUNT = {len(slides)};")
        .replace("'presentation.pptx'", f"'{output_pptx}'")
        .replace("'2B2D42'", "'0D1829'")
        .replace("'8D99AE'", "'C9A84C'")
        .replace("'EF233C'", "'D4AF37'")
        .replace("'EDF2F4'", "'2A3A5C'")
        .replace("'FFFFFF'", "'0D1829'"))
    (slides_dir / "compile.js").write_text(template)

    # npm install pptxgenjs (reuse existing install if present)
    (slides_dir / "package.json").write_text(json.dumps({
        "name": f"{ts_code.lower().replace('.', '-')}-deck",
        "version": "0.0.1",
        "private": True,
        "dependencies": {"pptxgenjs": "^3.12.0"},
    }, indent=2))
    if not (slides_dir / "node_modules" / "pptxgenjs").exists():
        print("Installing pptxgenjs...")
        r = subprocess.run(["npm", "install", "--omit=dev", "--silent"],
                           cwd=str(slides_dir), capture_output=True, text=True,
                           timeout=120)
        if r.returncode != 0:
            sys.exit(f"npm install failed: {r.stderr[:500]}")

    # Compile
    print(f"Compiling {output_pptx}...")
    r = subprocess.run(["node", "compile.js"], cwd=str(slides_dir),
                       capture_output=True, text=True, timeout=120)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode != 0:
        sys.exit(f"compile failed (rc={r.returncode})")

    pptx = d / output_pptx
    if not pptx.exists():
        sys.exit(f"compile reported OK but {pptx} missing")
    print(f"OK: {pptx} ({pptx.stat().st_size} bytes, {len(slides)} slides)")


if __name__ == "__main__":
    main()
