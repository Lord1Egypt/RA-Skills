#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成一日「涨停板龙虎榜深度研判」报告（两种排版样式）。

工作流：
    1. 载入候选数据 JSON
    2. 跑四层漏斗（L1→L2→L2.5→L3）+ 评分管道 → 产信号行
    3. 渲染数据驱动的 HTML
    4. 把 HTML 渲成 PDF
    5. （仅样式 A）复用 templates/make_pptx.py 产出 PPTX（v1.1 仍含硬编码示例数据，
       全数据驱动重写列入 v2.0 roadmap —— 见 docs/wealth-password-strategy.md）

两种排版样式（`--style`）：
    classic（样式 A，默认）—— MS 色系（#002B5C / #C5A572）+ A4 纵向，Playwright 导 PDF。
        产物：涨停板龙虎榜深度研判报告-YYYYMMDD.html / .pdf / .pptx
    bii（样式 B）—— BlackRock 投资研究院「左文字栏 + 右图表」双栏范式，A4 横向 + Chart.js
        内联，CDP 导 PDF。产物：涨停板龙虎榜深度研判报告-BII双栏-YYYYMMDD.html / .pdf
        详见 SKILL.md §12。
    both —— 两套都出。

用法：
    python3 scripts/generate_daily.py
    python3 scripts/generate_daily.py --data strategy/sample_data.json --date 2026-09-16
    python3 scripts/generate_daily.py --style bii
    python3 scripts/generate_daily.py --style both --out out/20260916
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from strategy import calibers as C          # noqa: E402
from strategy import formulas as F          # noqa: E402
from strategy import funnel as FN           # noqa: E402
from strategy import knowledge as KN        # noqa: E402
from strategy import pipeline as PL         # noqa: E402
from strategy import playbook as PB         # noqa: E402

REPO = pathlib.Path(__file__).resolve().parent.parent
TEMPLATES = REPO / "templates"
ASSETS = REPO / "assets"
ECHARTS_PATH = ASSETS / "echarts.min.js"


def load_data(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        sys.exit(f"[!] 数据文件不存在：{path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"[!] JSON 解析失败 {path}: {e}")


def render_html(data: dict, date: str, out_path: pathlib.Path) -> None:
    """生成数据驱动的 HTML（含 funnel + signal 表）。"""
    inds, stocks = _build_inputs(data)

    fr = FN.run_funnel(inds, stocks)
    funnel_pass = [s.merged for s in fr.l3_pass] or data.get("candidates", [])
    ctx = data.get("context", {}) or {}

    def _num(key, default=None):
        """容错取值：显式 null / 缺失 / 非数值 一律回退默认值（v2.3 契约允许写 null）。"""
        v = ctx.get(key, default)
        if v is None:
            return default
        try:
            return float(v)
        except (TypeError, ValueError):
            return default

    equity = _num("equity", 1_000_000)
    stage = (ctx.get("stage", "II") or "II").upper()
    ice = F.is_ice_point(int(_num("limit_up_count", 60)), _num("broken_rate", 0.2),
                         _num("index_pct", 0)) if ctx else False
    result = PL.run_pipeline(funnel_pass, equity=equity, stage=stage, ice_point=ice)

    # v2.3 知识蒸馏层：情绪周期 5 阶段状态机 + 索罗斯反身性标签（缺项自动降级）
    _lu = int(_num("limit_up_count", 60)) if ctx else None
    _br = _num("broken_rate", 0.2) if ctx else None
    sent = KN.sentiment_cycle(
        _lu, _br,
        lianban_height=(int(_num("lianban_height")) if _num("lianban_height") is not None else None),
        lianban_rate=_num("lianban_rate"),
        prev_premium=_num("prev_premium"),
        prev_stage=ctx.get("prev_sentiment_stage"),
    )
    refl = KN.reflexivity(
        ladder_height_today=(int(_num("lianban_height")) if _num("lianban_height") is not None else None),
        ladder_height_prev=(int(_num("lianban_height_prev")) if _num("lianban_height_prev") is not None else None),
        vr_slope_up=ctx.get("vr_slope_up"),
        margin_net3d=_num("margin_net3d"),
        prev_premium=_num("prev_premium"),
    )

    def _render_sentiment_dashboard() -> str:
        cap = f"{sent.pos_cap:.0%}"
        reasons = "；".join(sent.reasons) if sent.reasons else "—"
        refl_r = "；".join(refl.reasons) if refl.reasons else "—"
        ban = "允许打板" if sent.allow_da_ban else "禁止打板（低吸/半路为主）"
        return (
            "<table>"
            f"<tr><th>维度</th><th>判定</th><th>依据</th><th>操作指令</th></tr>"
            f"<tr><td>情绪周期（5 阶段）</td><td class=\"{'ok' if sent.stage in ('启动', '发酵', '高潮') else 'no'}\">"
            f"{sent.stage} · {sent.mode} · 仓位上限 {cap}</td><td>{reasons}</td>"
            f"<td>{ban}{('　' + sent.note) if sent.note else ''}</td></tr>"
            f"<tr><td>反身性（索罗斯）</td><td class=\"{'ok' if refl.stage == '强化' else ('no' if refl.stage == '毁灭' else '')}\">"
            f"{refl.stage}</td><td>{refl_r}</td><td>强化期持有待涨，毁灭期逢高兑现、只做首板</td></tr>"
            "</table>"
        )

    sentiment_html = _render_sentiment_dashboard()

    rows_html = _render_signal_rows(result["rows"])
    funnel_html = _render_funnel_section(fr, inds)
    caliber_html = (
        "<pre>" + C.describe().replace("<", "&lt;").replace(">", "&gt;") + "</pre>"
    )

    body = f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="UTF-8">
<title>涨停板龙虎榜深度研判报告-{date}</title>
<style>
/* @page 必须显式声明：没有它时 preferCSSPageSize 无从遵循，Chrome 会按 locale
   回退到 Letter(612×792)，导出的 PDF 比 A4 短一截、每页内容都错位。 */
@page{{size:A4 portrait;margin:14mm 12mm;}}
body{{font-family:"PingFang SC","Microsoft YaHei",sans-serif;max-width:980px;margin:24px auto;color:#12181F;line-height:1.65}}
h1{{color:#002B5C;border-bottom:3px solid #C5A572;padding-bottom:8px}}
h2{{color:#002B5C;margin-top:32px;border-left:4px solid #C5A572;padding-left:10px}}
pre{{background:#F6F8FA;padding:12px;border-left:3px solid #C5A572;overflow:auto}}
table{{border-collapse:collapse;width:100%;margin:12px 0;font-size:13px}}
th,td{{border:1px solid #DDE3EA;padding:6px 10px;text-align:left}}
th{{background:#0A3D6E;color:#fff;font-weight:600}}
tr:nth-child(even){{background:#F6F8FA}}
.ok{{color:#1E8449;font-weight:600}}
.no{{color:#C1272D;font-weight:600}}
.callout{{background:#FDF3F3;border-left:4px solid #C1272D;padding:10px 14px;margin:12px 0}}
.muted{{color:#6B7785;font-size:12px}}
@media print{{
  body{{max-width:none;margin:0;}}
  *{{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
  h2{{break-after:avoid;page-break-after:avoid;}}
  table,pre,.callout{{break-inside:avoid;page-break-inside:avoid;}}
  thead{{display:table-header-group;}}
}}
</style>
</head><body>
<h1>涨停板龙虎榜深度研判报告 · {date}</h1>
<p class="muted">口径版本 <b>{C.CALIBER_VERSION}</b> · 框架：L1→L2→L2.5→L3 四层漏斗 + 财富密码选股策略</p>

<h2>0. 本报告口径（v2 永久生效）</h2>
{caliber_html}

<h2>1. 市场情绪仪表盘（v2.3 知识蒸馏）</h2>
{sentiment_html}

<h2>2. 四层漏斗执行结果</h2>
{funnel_html}

<h2>3. 评分管道 · 风控信号表</h2>
{rows_html}

<h2>4. α 账本</h2>
<p class="muted">阶段 <b>{result['ledger']['stage']}</b> · α_max <b>{result['ledger']['alpha_budget']:.1%}</b> ·
已用 <b>{result['ledger']['used_pct']:.2%}</b> · 剩余 <b>{result['ledger']['remaining']:,.0f}</b> 元 ·
持仓 <b>{result['ledger']['positions']}</b> 笔</p>

<h2>5. 盘前 6 项检查</h2>
{PB.render_checklist_md().replace("<table>", '<table><thead>').replace("</table>", "</thead></table>").replace("<tr>", "<tr><th>#</th><th>检查项</th><th>做法</th><th>产出</th></tr>", 1).replace("<th>", "<th>")}

<h2>6. 免责声明</h2>
<p class="callout">{PB.playbook()['disclaimer']}</p>

<p class="muted">由 <code>scripts/generate_daily.py</code> 自动生成 · {dt.datetime.now().isoformat(timespec='seconds')}</p>
</body></html>"""

    # 注入 echarts（即使本报告未用图，也保留占位以兼容模板样式）
    body = body.replace("/*__ECHARTS__*/", "")  # 本数据驱动版未含图表
    out_path.write_text(body, encoding="utf-8")
    print(f"[1] HTML 已写出: {out_path} ({out_path.stat().st_size/1024:.1f} KB)")


def _build_inputs(data: dict) -> tuple[list, list]:
    inds = [FN.Industry(i["code"], i["name"], float(i["rank"]), float(i["vr"]),
                        float(i.get("dispersion", 0.0)), i.get("note", ""))
            for i in data.get("industries", [])]
    stocks = []
    for c in data.get("candidates", []):
        raw = {k: v for k, v in c.items()
               if k not in ("code", "name", "sector", "rank", "vr", "note")}
        stocks.append(FN.Stock(c["code"], c["name"], c.get("sector", ""),
                               float(c["rank"]) if c.get("rank") is not None else None,
                               float(c["vr"]) if c.get("vr") is not None else None,
                               raw))
    return inds, stocks


def _render_funnel_section(fr: Any, inds: list) -> str:
    parts = ["<table><tr><th>层</th><th>标的/行业</th><th>分位</th><th>额比</th><th>结果</th></tr>"]
    for ind in inds:
        passed = (ind.rank <= C.RANK_LOW_THRESHOLD)
        parts.append(
            f"<tr><td>L1 行业</td><td>{ind.name}</td><td>{ind.rank:.1f}%</td><td>{ind.vr:.2f}×</td>"
            f"<td class='{'ok' if passed else 'no'}'>{'入池' if passed else '未入池'}</td></tr>"
        )
    for s in fr.l2_pass:
        parts.append(
            f"<tr><td>L2 个股</td><td>{s.name}</td><td>{s.rank:.1f}%</td><td>{s.vr:.2f}×</td>"
            f"<td class='ok'>入池</td></tr>"
        )
    for g in fr.l2_5_removed:
        parts.append(
            f"<tr><td>L2.5 可交易</td><td>{g.name}</td><td>—</td><td>—</td>"
            f"<td class='no'>{g.reasons[0]}</td></tr>"
        )
    for g in fr.l3_vetoed:
        parts.append(
            f"<tr><td>L3 基本面</td><td>{g.name}</td><td>—</td><td>—</td>"
            f"<td class='no'>{g.reasons[0]}</td></tr>"
        )
    for s in fr.l3_pass:
        parts.append(
            f"<tr><td><b>最终</b></td><td><b>{s.name}</b></td><td>—</td><td>—</td>"
            f"<td class='ok'><b>通过</b></td></tr>"
        )
    parts.append("</table>")
    sens = fr.sensitivity
    parts.append(
        f"<p class='callout'>敏感度：50% 相对线（默认）→ <b>{sens['rule_50pct_relative']}</b> 只过会；"
        f"任何减速即排除 → <b>{sens['rule_any_deceleration']}</b> 只过会；"
        f"±{abs(sens['rule_50pct_relative']-sens['rule_any_deceleration'])} 只</p>"
    )
    return "\n".join(parts)


def _render_signal_rows(rows) -> str:
    parts = [
        "<table><tr><th>代码</th><th>名称</th><th>综合分</th><th>动作</th><th>股数</th><th>名义</th><th>说明</th></tr>"
    ]
    for r in rows:
        note = r.blocked_by or ("；".join(r.notes)[:140] if r.notes else "—")
        parts.append(
            f"<tr><td>{r.code}</td><td>{r.name}</td><td>{r.score:.1f}</td>"
            f"<td>{r.action}</td><td>{r.shares or '—'}</td><td>{r.notional or '—'}</td>"
            f"<td>{note}</td></tr>"
        )
    parts.append("</table>")
    return "\n".join(parts)


def render_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
    """样式 A 的 HTML → PDF。

    首选 Playwright；Playwright 不可用（未装、或浏览器二进制没下载）时自动回退到
    系统 Chrome + CDP（templates/bii/cdp_render.sh）。

    为什么要这条回退：Playwright 的 Chromium 要单独 `playwright install` 才有，
    新环境里极常见"脚本能跑但 PDF 出不来"。而系统 Chrome 几乎总是装着的，
    CDP 这条路的产物与 Playwright 完全一致（都走 printToPDF、都以 CSS @page 为准）。
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sync_playwright = None

    if sync_playwright is not None:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(args=["--allow-file-access-from-files"])
                page = browser.new_page(viewport={"width": 980, "height": 1400})
                page.emulate_media(media="print")
                page.goto(html_path.as_uri(), wait_until="load", timeout=120_000)
                page.wait_for_timeout(1200)
                page.pdf(
                    path=str(pdf_path), format="A4",
                    print_background=True, prefer_css_page_size=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                )
                browser.close()
            print(f"[2] PDF  已写出: {pdf_path} ({pdf_path.stat().st_size/1024:.1f} KB)")
            return
        except Exception as e:      # 浏览器二进制缺失 / 启动超时等
            print(f"[i] Playwright 导 PDF 失败（{type(e).__name__}: {str(e).splitlines()[0][:90]}），改用系统 Chrome + CDP")

    render_pdf_cdp(html_path, pdf_path)


def render_pdf_cdp(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
    """用系统 Chrome + CDP 导 PDF（方向由模板的 @page 决定）。"""
    import subprocess
    script = TEMPLATES / "bii" / "cdp_render.sh"
    if not script.exists():
        sys.exit(f"[!] 找不到 {script}，且 Playwright 不可用 —— 无法导出 PDF")
    res = subprocess.run(
        ["bash", str(script), str(html_path), str(pdf_path), "2400", "css"],
        cwd=str(REPO),
    )
    if res.returncode != 0 or not pdf_path.exists():
        sys.exit(f"[!] CDP 导 PDF 失败（退出码 {res.returncode}）")
    print(f"[2] PDF  已写出: {pdf_path} ({pdf_path.stat().st_size/1024:.1f} KB)")


def render_pptx(html_dir: pathlib.Path, date: str) -> pathlib.Path:
    """复用 templates/make_pptx.py（通过环境变量切换输出路径）。

    v1.1 限制：PPTX 内容仍使用 make_pptx.py 内硬编码的 2026-09-11 数据。
    v2.0 roadmap：将 make_pptx.py 重构为接受 data dict 的函数式 API。
    """
    import subprocess
    base = f"涨停板龙虎榜深度研判报告-{date}"
    out_html = html_dir / f"{base}.html"
    pptx_path = html_dir / f"{base}.pptx"
    env = os.environ.copy()
    env["POUT"] = str(html_dir)
    env["PFILE"] = f"{base}.pptx"
    # make_pptx 期望从 templates/ 目录运行
    cmd = [sys.executable, str(TEMPLATES / "make_pptx.py")]
    # 把 HTML 临时放到 templates/ 下（make_pptx 不读 HTML，但需要目录存在以导入样式）
    print(f"[3] 调用 make_pptx.py 生成 PPTX（v1.1 仍含 2026-09-11 硬编码示例）...")
    res = subprocess.run(cmd, cwd=str(TEMPLATES), env=env, capture_output=True, text=True)
    if res.returncode != 0:
        # v2.3：PPTX 为可选项，失败降级为警告，不得阻断 HTML/PDF 主产物
        print(f"[!] make_pptx 失败（已跳过，不影响 HTML/PDF）:\n{res.stderr}", file=sys.stderr)
        return pptx_path
    # 默认输出到 templates/，移到目标目录
    default_pptx = TEMPLATES / "涨停板龙虎榜深度研判报告-20260911.pptx"
    if default_pptx.exists():
        default_pptx.rename(pptx_path)
    print(f"[3] PPTX 已写出: {pptx_path} ({pptx_path.stat().st_size/1024:.1f} KB)")
    return pptx_path


def render_bii(data_path: pathlib.Path, date: str, out_dir: pathlib.Path,
               predict_file: pathlib.Path | None = None) -> list[pathlib.Path]:
    """样式 B：调用 templates/bii/render.sh 出 BII 双栏 HTML + PDF。

    为什么不在这里重写一遍导 PDF：BII 的流程里有三步是"必须按顺序做对"的
    （全新 profile 起 Chrome → 钉 1123px 视口校验图表与溢出 → CDP 流式导 PDF），
    拆开写极易漏步。render.sh 已把这三步和页数一致性校验串成一条命令，直接复用。

    `predict_file` 指向「次日 5 条可证伪预判」JSON（第 14 页，契约见 SKILL.md §12.9）。
    不传时由生成器自动探测 <data 同级>/predictions.json 与 <out>/predictions.json；
    都没有则渲染「示例占位页」（页内明确标注），不会静默出错。

    返回产出文件列表（可能因失败为空）。
    """
    import subprocess
    script = TEMPLATES / "bii" / "render.sh"
    if not script.exists():
        print(f"[!] 找不到 {script}，跳过样式 B", file=sys.stderr)
        return []
    print("[B] 生成 BII 双栏范式报告（含图表/溢出/页数三重校验）...")
    cmd = ["bash", str(script), "--data", str(data_path), "--date", date, "--out", str(out_dir)]
    if predict_file is not None:
        cmd += ["--predict-file", str(predict_file)]
    res = subprocess.run(cmd, cwd=str(REPO))
    if res.returncode != 0:
        print(f"[!] 样式 B 生成失败（退出码 {res.returncode}）", file=sys.stderr)
        return []
    dc = date.replace("-", "")
    return [
        out_dir / f"涨停板龙虎榜深度研判报告-BII双栏-{dc}.html",
        out_dir / f"涨停板龙虎榜深度研判报告-BII双栏-{dc}.pdf",
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="生成一日龙虎榜报告（样式 A / B / 双样式）")
    ap.add_argument("--data", default=str(REPO / "strategy" / "sample_data.json"))
    ap.add_argument("--date", default=dt.date.today().strftime("%Y-%m-%d"))
    ap.add_argument("--out", default=None, help="输出目录（默认 out/dragon-tiger-YYYYMMDD）")
    ap.add_argument("--style", choices=["classic", "bii", "both"], default="classic",
                    help="classic=MS 色系 A4 纵向（默认）；bii=BII 双栏 A4 横向；both=两套都出")
    ap.add_argument("--predict-file", default=None,
                    help="次日 5 条可证伪预判 JSON（仅样式 B 用；缺省自动探测 predictions.json）")
    args = ap.parse_args()

    date_compact = args.date.replace("-", "")
    out_dir = pathlib.Path(args.out) if args.out else REPO / "out" / f"dragon-tiger-{date_compact}"
    out_dir = out_dir.expanduser().resolve()   # 必须转绝对路径：subprocess 用 cwd=TEMPLATES
    out_dir.mkdir(parents=True, exist_ok=True)
    base = f"涨停板龙虎榜深度研判报告-{date_compact}"
    # ⚠️ data / predict 都必须转绝对路径：render_bii() 用 cwd=REPO 起子进程，
    #    相对路径会相对 REPO 解析（而不是调用方的 cwd），于是找不到文件。
    data_path = pathlib.Path(args.data).expanduser().resolve()

    print("=" * 60)
    print(f" A股龙虎榜深度研判 · {args.date} · 口径 {C.CALIBER_VERSION} · 样式 {args.style}")
    print("=" * 60)

    produced: list[pathlib.Path] = []

    if args.style in ("classic", "both"):
        data = load_data(data_path)
        html_path = out_dir / f"{base}.html"
        pdf_path = out_dir / f"{base}.pdf"
        # 先做 PPTX（避免 HTML 触发 Playwright 期间 UI 阻塞）
        pptx_path = render_pptx(out_dir, date_compact)
        render_html(data, args.date, html_path)
        render_pdf(html_path, pdf_path)
        produced += [html_path, pdf_path, pptx_path]

    if args.style in ("bii", "both"):
        pf = pathlib.Path(args.predict_file).expanduser().resolve() if args.predict_file else None
        if pf is not None and not pf.exists():
            sys.exit(f"[!] 预判文件不存在：{pf}")
        produced += render_bii(data_path, args.date, out_dir, pf)

    print("\n" + "=" * 60)
    print(f" 已生成于: {out_dir}")
    for f in produced:
        if f.exists():
            print(f"  · {f.name} ({f.stat().st_size/1024:.1f} KB)")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())