from __future__ import annotations

import base64
import html
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# reportlab TTFont 注册名（内置 CID 兜底时为 STSong-Light）
PDF_CJK_FONT_NAME = "SourceHanSansCN"


def _workspace_root() -> Path:
    raw = os.environ.get("OPENCLAW_WORKSPACE") or os.environ.get("FILE_DOWNLOAD_BASE")
    if not raw:
        raw = os.path.expanduser("~/.openclaw/workspace")
    return Path(raw).resolve()


def _load_config(skill_root: Path) -> Dict[str, Any]:
    cfg_path = skill_root / "config" / "config.yaml"
    if not cfg_path.exists():
        return {}
    try:
        import yaml

        with cfg_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _slugify(value: str, default: str = "bi_report") -> str:
    text = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._-]+", "_", (value or "").strip())
    text = text.strip("._-")
    return text or default


def _report_root_dir(skill_root: Path, context: Dict[str, Any]) -> Path:
    options = context.get("options") or {}
    cfg = _load_config(skill_root)
    out_dir = options.get("output_dir") or cfg.get("output_reports_dir") or ""
    if out_dir:
        out_path = Path(out_dir)
        if not out_path.is_absolute():
            out_path = _workspace_root() / out_path
        return out_path.resolve()
    return (_workspace_root() / "databird" / "output").resolve()


def _report_run_name(context: Dict[str, Any]) -> str:
    options = context.get("options") or {}
    job_id = str(options.get("job_id") or "").strip()
    if job_id:
        return _slugify(job_id, "bi_job")
    query = str(context.get("query") or "").strip()[:40]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{stamp}_{_slugify(query or 'bi_report')}"


def _report_title(context: Dict[str, Any]) -> str:
    options = context.get("options") or {}
    title = str(options.get("report_title") or "").strip()
    if title:
        return title
    query = str(context.get("query") or "").strip()
    return query or "Data Bird 分析报告"


def _html_page(
    title: str,
    body: str,
    extra_head: str = "",
    extra_after_styles: str = "",
) -> str:
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  {extra_head}
  <style>
    body {{
      font-family: "SourceHanSansCN", -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
      margin: 0;
      color: #1f2937;
      background: #f8fafc;
    }}
    .page {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 24px;
    }}
    .hero {{
      background: linear-gradient(135deg, #0f172a, #1d4ed8);
      color: #fff;
      border-radius: 16px;
      padding: 28px;
      margin-bottom: 24px;
    }}
    .hero h1 {{
      margin: 0 0 10px;
      font-size: 30px;
    }}
    .meta {{
      opacity: 0.9;
      font-size: 14px;
    }}
    .section {{
      background: #fff;
      border-radius: 16px;
      padding: 20px 22px;
      margin-bottom: 20px;
      box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }}
    .section h2 {{
      margin: 0 0 14px;
      font-size: 20px;
    }}
    .section h3 {{
      margin: 0 0 12px;
      font-size: 16px;
    }}
    .chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 10px;
    }}
    .chip {{
      background: #eff6ff;
      color: #1d4ed8;
      border: 1px solid #bfdbfe;
      border-radius: 999px;
      padding: 6px 12px;
      font-size: 13px;
    }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
    }}
    .summary-card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 14px;
    }}
    .summary-card .label {{
      color: #64748b;
      font-size: 13px;
      margin-bottom: 6px;
    }}
    .summary-card .value {{
      font-size: 22px;
      font-weight: 700;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      font-size: 14px;
    }}
    th, td {{
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid #e5e7eb;
      vertical-align: top;
    }}
    th {{
      color: #475569;
      background: #f8fafc;
    }}
    ul {{
      margin: 0;
      padding-left: 20px;
    }}
    li + li {{
      margin-top: 8px;
    }}
    .chart-card {{
      margin-bottom: 20px;
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      padding: 14px;
      background: #fff;
    }}
    .chart-box {{
      width: 100%;
      height: 420px;
    }}
    .chart-links {{
      margin-top: 12px;
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      font-size: 14px;
    }}
    .chart-links a {{
      color: #2563eb;
      text-decoration: none;
    }}
    .footer-note {{
      color: #64748b;
      font-size: 13px;
      margin-top: 18px;
    }}
    .pdf-chart img {{
      width: 720px;
      border: 1px solid #dbe2ea;
      border-radius: 8px;
    }}
  </style>
  {extra_after_styles}
</head>
<body>
  {body}
</body>
</html>"""


def _summary_cards(summary: Dict[str, Any]) -> str:
    row_count = summary.get("rowCount") or summary.get("row_count") or 0
    col_count = len(summary.get("columns") or [])
    time_col = summary.get("detectedTimeColumn") or "-"
    scenario = summary.get("scenario_label") or summary.get("scenario") or "-"
    chart_count = summary.get("chartCount") or 0
    return f"""
    <div class="summary-grid">
      <div class="summary-card"><div class="label">数据行数</div><div class="value">{row_count}</div></div>
      <div class="summary-card"><div class="label">字段数</div><div class="value">{col_count}</div></div>
      <div class="summary-card"><div class="label">时间列</div><div class="value" style="font-size:18px">{html.escape(str(time_col))}</div></div>
      <div class="summary-card"><div class="label">数据场景</div><div class="value" style="font-size:18px">{html.escape(str(scenario))}</div></div>
      <div class="summary-card"><div class="label">图表数量</div><div class="value">{chart_count}</div></div>
    </div>
    """


def _columns_table(summary: Dict[str, Any]) -> str:
    columns = summary.get("columns") or []
    if not columns:
        return "<p>无字段摘要。</p>"
    rows = []
    for col in columns:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(col.get('name', '')))}</td>"
            f"<td>{html.escape(str(col.get('dtype', '')))}</td>"
            f"<td>{html.escape(str(col.get('semanticType', '')))}</td>"
            f"<td>{html.escape(str(col.get('role', '')))}</td>"
            "</tr>"
        )
    return (
        "<table><thead><tr><th>字段</th><th>类型</th><th>语义</th><th>角色</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def _bullet_section(title: str, items: List[str]) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{html.escape(str(item))}</li>" for item in items if str(item).strip())
    if not lis:
        return ""
    return f'<div class="section"><h2>{html.escape(title)}</h2><ul>{lis}</ul></div>'


def _paragraph_section(title: str, items: List[str]) -> str:
    rows = "".join(
        f'<p style="margin:0 0 10px; line-height:1.8;">{html.escape(str(item))}</p>'
        for item in items
        if str(item).strip()
    )
    if not rows:
        return ""
    return f'<div class="section"><h2>{html.escape(title)}</h2>{rows}</div>'


def _write_chart_html(chart: Dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    title = chart.get("title") or "图表"
    option = json.dumps(chart.get("option") or {}, ensure_ascii=False)
    out_path.write_text(
        _html_page(
            title,
            f"""
            <div class="page">
              <div class="section">
                <h2>{html.escape(title)}</h2>
                <div id="chart" class="chart-box"></div>
              </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
            <script>
              const chart = echarts.init(document.getElementById('chart'));
              chart.setOption({option});
              window.addEventListener('resize', () => chart.resize());
            </script>
            """,
        ),
        encoding="utf-8",
    )


def _bundled_font_paths(skill_root: Path) -> List[str]:
    """Skill 内置 fonts/ 目录下的中文字体（思源黑体等），优先固定文件名。"""
    d = skill_root / "fonts"
    if not d.is_dir():
        return []
    preferred = [
        d / "SourceHanSansSC-Regular.otf",
        d / "SourceHanSansSC-Medium.otf",
        d / "NotoSansSC-Regular.otf",
    ]
    seen = set()
    out: List[str] = []
    for p in preferred:
        if p.is_file():
            s = str(p.resolve())
            if s not in seen:
                seen.add(s)
                out.append(s)
    for pat in ("*.otf", "*.ttf", "*.ttc"):
        for p in sorted(d.glob(pat)):
            s = str(p.resolve())
            if s not in seen:
                seen.add(s)
                out.append(s)
    return out


def _setup_matplotlib(skill_root: Optional[Path] = None):
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import font_manager as fm
    from matplotlib import pyplot as plt

    fallback = [
        "PingFang SC",
        "Microsoft YaHei",
        "Noto Sans CJK SC",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    if skill_root:
        for fpath in _bundled_font_paths(skill_root):
            try:
                fm.fontManager.addfont(fpath)
                fam = fm.FontProperties(fname=fpath).get_name()
                plt.rcParams["font.sans-serif"] = [fam] + fallback
                break
            except Exception:
                continue
        else:
            plt.rcParams["font.sans-serif"] = fallback
    else:
        plt.rcParams["font.sans-serif"] = fallback
    plt.rcParams["axes.unicode_minus"] = False
    return plt


def _axis_data(axis: Any) -> List[Any]:
    if isinstance(axis, list):
        axis = axis[0] if axis else {}
    return list((axis or {}).get("data") or [])


def _save_chart_png(chart: Dict[str, Any], out_path: Path, skill_root: Path) -> None:
    plt = _setup_matplotlib(skill_root)
    option = chart.get("option") or {}
    ctype = chart.get("type") or "line"
    title = chart.get("title") or "图表"
    series = option.get("series") or []
    x_data = _axis_data(option.get("xAxis"))

    fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=150)
    try:
        if ctype == "pie" and series:
            data = series[0].get("data") or []
            labels = [str(item.get("name", "")) for item in data]
            values = [float(item.get("value", 0) or 0) for item in data]
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
        elif ctype in {"bar", "histogram"} and series:
            x_index = list(range(len(x_data)))
            width = 0.8 / max(len(series), 1)
            for idx, item in enumerate(series):
                values = item.get("data") or []
                offset = [x + (idx - (len(series) - 1) / 2) * width for x in x_index]
                ax.bar(offset, values, width=width, label=str(item.get("name", f"系列{idx + 1}")))
            ax.set_xticks(x_index)
            ax.set_xticklabels([str(x) for x in x_data], rotation=30, ha="right")
            if len(series) > 1:
                ax.legend()
        elif ctype == "scatter" and series:
            points = series[0].get("data") or []
            xs = [p[0] for p in points if isinstance(p, (list, tuple)) and len(p) >= 2]
            ys = [p[1] for p in points if isinstance(p, (list, tuple)) and len(p) >= 2]
            ax.scatter(xs, ys, s=28, alpha=0.75)
        else:
            for idx, item in enumerate(series):
                values = item.get("data") or []
                label = str(item.get("name", f"系列{idx + 1}"))
                if x_data:
                    ax.plot([str(x) for x in x_data], values, marker="o", linewidth=2, label=label)
                else:
                    ax.plot(values, marker="o", linewidth=2, label=label)
            if len(series) > 1:
                ax.legend()

        ax.set_title(title)
        y_axis = option.get("yAxis")
        x_axis = option.get("xAxis")
        if isinstance(x_axis, dict) and x_axis.get("name"):
            ax.set_xlabel(str(x_axis.get("name")))
        if isinstance(y_axis, dict) and y_axis.get("name"):
            ax.set_ylabel(str(y_axis.get("name")))
        ax.grid(True, linestyle="--", alpha=0.25)
        fig.tight_layout()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, bbox_inches="tight")
    finally:
        plt.close(fig)


def _image_to_data_uri(path: str) -> str:
    try:
        raw = Path(path).read_bytes()
    except OSError:
        return ""
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _build_report_html(
    title: str,
    report_md: str,
    summary: Dict[str, Any],
    insight: Dict[str, Any],
    charts: List[Dict[str, Any]],
    chart_html_paths: List[Path],
) -> str:
    cards = _summary_cards(summary)
    cols = _columns_table(summary)
    executive = list(insight.get("executiveSummary") or [])
    findings = list(insight.get("keyFindings") or insight.get("conclusions") or [])
    drivers = list(insight.get("driverAnalysis") or [])
    risks = list(insight.get("risks") or insight.get("anomalies") or [])
    opportunities = list(insight.get("opportunities") or [])
    actions = list(insight.get("actionPlan") or insight.get("suggestions") or [])
    chips = "".join(
        f'<span class="chip">{html.escape(str(name))}</span>'
        for name in [c.get("name", "") for c in (summary.get("columns") or [])[:12]]
        if str(name).strip()
    )
    chart_blocks = []
    for idx, chart in enumerate(charts):
        chart_id = f"report_chart_{idx + 1}"
        chart_link = chart_html_paths[idx].name if idx < len(chart_html_paths) else ""
        link_html = f'<a href="charts/{html.escape(chart_link)}" target="_blank">单图 HTML</a>' if chart_link else ""
        takeaway_html = ""
        if chart.get("takeaway"):
            takeaway_html = f'<p style="margin:12px 0 0; color:#475569;"><strong>Key takeaway:</strong> {html.escape(str(chart.get("takeaway")))}</p>'
        chart_blocks.append(
            f"""
            <div class="chart-card">
              <h3>{html.escape(str(chart.get("title") or f"图表 {idx + 1}"))}</h3>
              <div id="{chart_id}" class="chart-box"></div>
              {takeaway_html}
              <div class="chart-links">{link_html}</div>
            </div>
            """
        )
    body = f"""
    <div class="page">
      <div class="hero">
        <h1>{html.escape(title)}</h1>
        <div class="meta">生成时间：{html.escape(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}</div>
        <div class="chips">{chips}</div>
      </div>
      <div class="section">
        <h2>报告摘要</h2>
        {cards}
      </div>
      <div class="section">
        <h2>字段概览</h2>
        {cols}
      </div>
      {_bullet_section("执行摘要", executive)}
      {_bullet_section("关键发现", findings)}
      {_paragraph_section("驱动分析", drivers)}
      {_bullet_section("风险提示", risks)}
      {_bullet_section("机会判断", opportunities)}
      {_bullet_section("行动建议", actions)}
      <div class="section">
        <h2>图表分析</h2>
        {''.join(chart_blocks) or '<p>无图表。</p>'}
      </div>
      <div class="section">
        <h2>Markdown 原文</h2>
        <pre style="white-space:pre-wrap; margin:0;">{html.escape(report_md)}</pre>
      </div>
      <div class="footer-note">HTML 版本支持交互式 ECharts；PDF 版本会嵌入静态图像。</div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script>
      const charts = {json.dumps([c.get("option") or {} for c in charts], ensure_ascii=False)};
      charts.forEach((option, idx) => {{
        const el = document.getElementById(`report_chart_${{idx + 1}}`);
        if (!el) return;
        const chart = echarts.init(el);
        chart.setOption(option);
        window.addEventListener('resize', () => chart.resize());
      }});
    </script>
    """
    return _html_page(title, body)


def _resolve_path(p_str: str, skill_root: Path) -> Optional[Path]:
    if not p_str:
        return None
    p = Path(p_str).expanduser()
    if not p.is_absolute():
        p = (skill_root / p).resolve()
    else:
        p = p.resolve()
    return p if p.is_file() else None


def _pdf_cjk_font_setup(skill_root: Path, context: Dict[str, Any]) -> Tuple[str, str]:
    """
    为 reportlab 注册中文字体，返回 (font_name, err_msg)。

    优先顺序（TTF/TTC 优先，CFF OTF 不被 reportlab 原生支持）：
    1. CLAW_BI_PDF_FONT / DATA_BIRD_PDF_FONT 环境变量（明确指定时若不存在则报错）
    2. options.pdf_chinese_font / options.pdf_font
    3. config.yaml pdf_chinese_font
    4. fonts/ 目录下 .ttf / .ttc（跳过 .otf，reportlab 不支持 CFF 字形）
    5. 系统 TTF/TTC（macOS STHeiti、Linux Noto）
    6. reportlab 内置 UnicodeCIDFont 'STSong-Light'（万能兜底，无需任何额外文件）
    """
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    except Exception as exc:
        return "", f"reportlab 不可用: {exc}"

    # 若已注册直接返回
    try:
        if PDF_CJK_FONT_NAME in pdfmetrics.getRegisteredFontNames():
            return PDF_CJK_FONT_NAME, ""
    except Exception:
        pass

    # --- 显式环境变量路径 ---
    env = (os.environ.get("DATA_BIRD_PDF_FONT") or os.environ.get("CLAW_BI_PDF_FONT") or "").strip()
    if env:
        p = _resolve_path(env, skill_root)
        if p is None:
            return "", f"CLAW_BI_PDF_FONT/DATA_BIRD_PDF_FONT 指向的文件不存在: {env}"
        try:
            pdfmetrics.registerFont(TTFont(PDF_CJK_FONT_NAME, str(p)))
            return PDF_CJK_FONT_NAME, ""
        except Exception as exc:
            return "", f"CLAW_BI_PDF_FONT/DATA_BIRD_PDF_FONT 字体加载失败: {exc}"

    # --- 收集候选 TTF/TTC（reportlab 仅支持 TrueType 字形，不支持 CFF OTF）---
    candidates: List[str] = []
    seen: set = set()

    def _add(s: str) -> None:
        if s and s not in seen:
            seen.add(s)
            candidates.append(s)

    opts = context.get("options") or {}
    for key in ("pdf_chinese_font", "pdf_font"):
        raw = str(opts.get(key) or "").strip()
        p = _resolve_path(raw, skill_root)
        if p:
            _add(str(p))

    cfg = _load_config(skill_root)
    for key in ("pdf_chinese_font", "pdf_font"):
        raw = str(cfg.get(key) or "").strip()
        p = _resolve_path(raw, skill_root)
        if p:
            _add(str(p))

    fonts_dir = skill_root / "fonts"
    if fonts_dir.is_dir():
        for ext in ("*.ttf", "*.ttc"):
            for fp in sorted(fonts_dir.glob(ext)):
                _add(str(fp.resolve()))

    for sys_p in (
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
    ):
        if Path(sys_p).is_file():
            _add(sys_p)

    for fpath in candidates:
        try:
            pdfmetrics.registerFont(TTFont(PDF_CJK_FONT_NAME, fpath))
            return PDF_CJK_FONT_NAME, ""
        except Exception:
            continue

    # --- 万能兜底：reportlab 内置 UnicodeCIDFont（STSong-Light，无需字体文件）---
    CID_FONT = "STSong-Light"
    try:
        pdfmetrics.registerFont(UnicodeCIDFont(CID_FONT))
        return CID_FONT, ""
    except Exception as exc:
        return "", f"所有字体均注册失败，最后错误: {exc}"


def _write_pdf(
    report_dir: Path,
    pdf_path: Path,
    title: str,
    summary: Dict[str, Any],
    insight: Dict[str, Any],
    chart_image_paths: List[str],
    charts: List[Dict[str, Any]],
    skill_root: Path,
    context: Dict[str, Any],
) -> str:
    """
    使用 reportlab platypus 生成 PDF，彻底避免 xhtml2pdf 的 CJK 乱码问题。
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            HRFlowable,
            Image as RLImage,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except Exception as exc:
        return f"reportlab 不可用: {exc}"

    font_name, font_err = _pdf_cjk_font_setup(skill_root, context)
    if not font_name:
        return font_err

    # --- 样式定义 ---
    CLR_BLUE = colors.HexColor("#1d4ed8")
    CLR_DARK = colors.HexColor("#0f172a")
    CLR_TEXT = colors.HexColor("#1f2937")
    CLR_MUTE = colors.HexColor("#64748b")
    CLR_CARD = colors.HexColor("#f8fafc")
    CLR_BORDER = colors.HexColor("#e2e8f0")

    def ps(name: str, size: int = 11, leading: int = 18, color: Any = CLR_TEXT, bold: bool = False, **kw: Any) -> ParagraphStyle:
        return ParagraphStyle(name, fontName=font_name, fontSize=size, leading=leading, textColor=color, **kw)

    st_title  = ps("ptitle",  size=20, leading=28, color=colors.white, spaceAfter=4)
    st_meta   = ps("pmeta",   size=10, leading=14, color=colors.HexColor("#cbd5e1"), spaceAfter=0)
    st_h2     = ps("ph2",     size=14, leading=20, color=CLR_DARK, spaceBefore=10, spaceAfter=6)
    st_body   = ps("pbody",   size=11, leading=18, color=CLR_TEXT, spaceAfter=3)
    st_bullet = ps("pbullet", size=11, leading=18, color=CLR_TEXT, leftIndent=10, spaceAfter=3)
    st_label  = ps("plabel",  size=9,  leading=14, color=CLR_MUTE, spaceAfter=2)
    st_val    = ps("pval",    size=16, leading=22, color=CLR_DARK, spaceAfter=0)
    st_th     = ps("pth",     size=10, leading=14, color=CLR_MUTE, spaceAfter=0)
    st_td     = ps("ptd",     size=10, leading=14, color=CLR_TEXT, spaceAfter=0)
    st_note   = ps("pnote",   size=10, leading=16, color=CLR_MUTE, spaceAfter=6)

    W = A4[0] - 30 * mm

    def section_header(text: str) -> List[Any]:
        return [
            Paragraph(text, st_h2),
            HRFlowable(width=W, thickness=1, color=CLR_BORDER, spaceAfter=6),
        ]

    def bullet_list(items: List[str]) -> List[Any]:
        return [Paragraph(f"• {item}", st_bullet) for item in items if str(item).strip()]

    story: List[Any] = []

    # --- 标题块（深蓝背景 Table） ---
    gen_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header_table = Table(
        [[Paragraph(title, st_title)], [Paragraph(f"生成时间：{gen_time}", st_meta)]],
        colWidths=[W],
    )
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CLR_DARK),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [CLR_DARK, colors.HexColor("#1e3a5f")]),
        ("BOX", (0, 0), (-1, -1), 1, CLR_BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6 * mm))

    # --- 数据摘要卡片 ---
    row_count = summary.get("rowCount") or summary.get("row_count") or 0
    col_count = len(summary.get("columns") or [])
    time_col = str(summary.get("detectedTimeColumn") or "-")
    scenario = str(summary.get("scenario_label") or summary.get("scenario") or "-")
    chart_count = str(summary.get("chartCount") or len(charts) or 0)
    card_data = [
        [
            Paragraph("数据行数", st_label),
            Paragraph("字段数", st_label),
            Paragraph("时间列", st_label),
            Paragraph("数据场景", st_label),
            Paragraph("图表数量", st_label),
        ],
        [
            Paragraph(str(row_count), st_val),
            Paragraph(str(col_count), st_val),
            Paragraph(time_col, st_val),
            Paragraph(scenario, st_val),
            Paragraph(chart_count, st_val),
        ],
    ]
    card_w = W / 5
    summary_table = Table(card_data, colWidths=[card_w, card_w, card_w, card_w, card_w])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CLR_CARD),
        ("BOX", (0, 0), (-1, -1), 1, CLR_BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, CLR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.extend(section_header("报告摘要"))
    story.append(summary_table)
    story.append(Spacer(1, 5 * mm))

    # --- 字段列表 ---
    columns = summary.get("columns") or []
    if columns:
        story.extend(section_header("字段概览"))
        col_rows = [[Paragraph(h, st_th) for h in ["字段名", "类型", "语义", "角色"]]]
        for col in columns:
            col_rows.append([
                Paragraph(str(col.get("name", "")), st_td),
                Paragraph(str(col.get("dtype", "")), st_td),
                Paragraph(str(col.get("semanticType", "")), st_td),
                Paragraph(str(col.get("role", "")), st_td),
            ])
        cw = W / 4
        col_table = Table(col_rows, colWidths=[cw * 1.4, cw * 0.8, cw * 0.8, cw])
        col_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), CLR_CARD),
            ("BOX", (0, 0), (-1, -1), 1, CLR_BORDER),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, CLR_BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(col_table)
        story.append(Spacer(1, 5 * mm))

    # --- 咨询式短报告正文 ---
    for sec_title, key in [
        ("执行摘要", "executiveSummary"),
        ("关键发现", "keyFindings"),
        ("驱动分析", "driverAnalysis"),
        ("风险提示", "risks"),
        ("机会判断", "opportunities"),
        ("行动建议", "actionPlan"),
    ]:
        items = insight.get(key) or []
        if items:
            story.extend(section_header(sec_title))
            story.extend(bullet_list([str(i) for i in items]))
            story.append(Spacer(1, 4 * mm))

    # --- 图表图片 ---
    if chart_image_paths:
        story.extend(section_header("图表分析"))
        img_w = W
        img_max_h = 100 * mm
        for img_path, chart in zip(chart_image_paths, charts):
            p = Path(img_path)
            if not p.is_file():
                continue
            chart_title = str(chart.get("title") or "图表")
            story.append(Paragraph(chart_title, st_h2))
            try:
                img = RLImage(str(p), width=img_w)
                ratio = img.imageHeight / img.imageWidth if img.imageWidth else 0.5
                h = img_w * ratio
                if h > img_max_h:
                    img = RLImage(str(p), width=img_max_h / ratio, height=img_max_h)
                else:
                    img = RLImage(str(p), width=img_w, height=h)
                story.append(img)
            except Exception:
                story.append(Paragraph(f"（图片加载失败：{img_path}）", st_body))
            takeaway = str(chart.get("takeaway") or "").strip()
            if takeaway:
                story.append(Paragraph(f"Key takeaway: {takeaway}", st_note))
            story.append(Spacer(1, 4 * mm))

    # --- 构建文档 ---
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            leftMargin=15 * mm,
            rightMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
            title=title,
        )
        doc.build(story)
    except Exception as exc:
        return f"reportlab PDF 构建失败: {exc}"
    return ""


def generate_report_artifacts(skill_root: Path, context: Dict[str, Any]) -> Dict[str, Any]:
    report_dir = _report_root_dir(skill_root, context) / _report_run_name(context)
    charts_dir = report_dir / "charts"
    images_dir = report_dir / "images"
    report_dir.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    report_title = _report_title(context)
    report_md = str(context.get("report_md") or "").strip() or "# 分析报告\n\n无内容"
    charts = list(context.get("charts") or [])
    summary = dict(context.get("summary") or context.get("schema") or {})
    insight = dict(context.get("insight") or {})

    report_md_path = report_dir / "report.md"
    report_html_path = report_dir / "report.html"
    report_pdf_path = report_dir / "report.pdf"

    chart_html_paths: List[Path] = []
    chart_image_paths: List[Path] = []
    chart_errors: List[str] = []

    for idx, chart in enumerate(charts):
        base_name = _slugify(str(chart.get("id") or f"chart_{idx + 1}"), f"chart_{idx + 1}")
        chart_html_path = charts_dir / f"{base_name}.html"
        chart_png_path = images_dir / f"{base_name}.png"
        try:
            _write_chart_html(chart, chart_html_path)
            chart_html_paths.append(chart_html_path)
        except Exception as exc:
            chart_errors.append(f"{base_name}.html: {exc}")
        try:
            _save_chart_png(chart, chart_png_path, skill_root)
            chart_image_paths.append(chart_png_path)
        except Exception as exc:
            chart_errors.append(f"{base_name}.png: {exc}")

    report_md_path.write_text(report_md, encoding="utf-8")
    report_html_path.write_text(
        _build_report_html(report_title, report_md, summary, insight, charts, chart_html_paths),
        encoding="utf-8",
    )

    opts = context.get("options") if isinstance(context.get("options"), dict) else {}
    pdf_mode = str(opts.get("pdf_generation_mode") or "local").strip().lower()
    pdf_error = ""
    if pdf_mode == "server":
        pdf_error = "PDF 由服务器侧生成"
    else:
        pdf_error = _write_pdf(
            report_dir=report_dir,
            pdf_path=report_pdf_path,
            title=report_title,
            summary=summary,
            insight=insight,
            chart_image_paths=[str(p) for p in chart_image_paths],
            charts=charts,
            skill_root=skill_root,
            context=context,
        )
        if pdf_error and report_pdf_path.exists():
            try:
                report_pdf_path.unlink()
            except OSError:
                pass

    return {
        "report_dir": str(report_dir),
        "report_md_path": str(report_md_path),
        "report_html_path": str(report_html_path),
        "report_pdf_path": str(report_pdf_path) if report_pdf_path.exists() else "",
        "chart_paths": [str(p) for p in chart_html_paths],
        "chart_image_paths": [str(p) for p in chart_image_paths],
        "chart_errors": chart_errors,
        "report_pdf_error": pdf_error,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
