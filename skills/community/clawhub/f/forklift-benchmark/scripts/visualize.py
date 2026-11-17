#!/usr/bin/env python3
"""FK-Bench Skill — 结果可视化脚本(版权保护)。

© 2026 FK-Bench Skill 作者。保留所有权利。未经授权禁止复制、分发、修改。

读入 score.py 输出的 scores.json, 生成:
  - <out>/scores_chart.png   2×2 综合图表(模块/难度/逐题分布/红线通过率)
  - <out>/report.html        自包含 HTML 报告(内嵌图表 + 汇总 + 明细 + 水印)

用法:
    python visualize.py --scores scores.json --out report
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "SimSun", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OWNER = "FK-Bench Skill"
WATERMARK = f"© 2026 {OWNER} 作者 · 未经授权禁止分发"

MODULE_CN = {
    "MOD-1": "导航与路径规划", "MOD-2": "载荷与货叉操作", "MOD-3": "属具感知",
    "MOD-4": "安全与红线合规", "MOD-5": "现场拓扑推理", "MOD-6": "传感器异常鲁棒性",
}
SCENE_CN = {
    "S1_HIGH_BAY": "高位立体库", "S2_BLOCK": "平库/堆垛区", "S3_DOCK": "集装箱/货车装卸",
    "S4_LINE_SIDE": "生产流水线边", "S5_VNA": "窄巷道", "S6_OUTDOOR": "户外交接区",
    "S7_MIXED": "人机混行",
}
MODULE_COLORS = {
    "MOD-1": "#4C72B0", "MOD-2": "#DD8452", "MOD-3": "#55A868",
    "MOD-4": "#C44E52", "MOD-5": "#8172B3", "MOD-6": "#937860",
}


def _watermark(fig) -> None:
    fig.text(0.99, 0.005, WATERMARK, ha="right", va="bottom",
             fontsize=8, color="gray", alpha=0.7)


def build_chart(summary: dict, out_png: Path) -> None:
    by_mod = summary.get("by_module", {})
    by_diff = summary.get("by_difficulty", {})
    details = summary.get("details", [])
    rl_pass_rate = summary.get("red_line_pass_rate")

    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))
    fig.suptitle(f"FK-Bench v2 评测结果 — Macro {summary.get('macro_total', 0)} / 100",
                 fontsize=15, fontweight="bold")

    # 1) 按模块平均分
    ax = axes[0][0]
    mods = list(by_mod)
    vals = [by_mod[m] for m in mods]
    colors = [MODULE_COLORS.get(m, "#999999") for m in mods]
    ax.bar(mods, vals, color=colors)
    ax.set_title("按模块平均分")
    ax.set_ylim(0, 100)
    ax.set_ylabel("得分")
    ax.set_xticks(range(len(mods)))
    ax.set_xticklabels([f"{m}\n{MODULE_CN.get(m, '')}" for m in mods], fontsize=8)
    for i, v in enumerate(vals):
        ax.text(i, v + 1, f"{v:.0f}", ha="center", fontsize=8)

    # 2) 按难度平均分
    ax = axes[0][1]
    diffs = list(by_diff)
    ax.bar(diffs, [by_diff[d] for d in diffs],
           color=["#8ECFC9", "#FFBE7A", "#FA7F6F"][: len(diffs)])
    ax.set_title("按难度平均分")
    ax.set_ylim(0, 100)
    ax.set_ylabel("得分")
    for i, d in enumerate(diffs):
        ax.text(i, by_diff[d] + 1, f"{by_diff[d]:.0f}", ha="center", fontsize=9)

    # 3) 逐题得分分布(按模块着色)
    ax = axes[1][0]
    xs = list(range(len(details)))
    ys = [d["total"] for d in details]
    cs = [MODULE_COLORS.get(d["module"], "#999999") for d in details]
    ax.scatter(xs, ys, c=cs, s=22, alpha=0.8)
    ax.set_title(f"逐题得分分布 (n={len(details)})")
    ax.set_ylim(-2, 102)
    ax.set_ylabel("得分")
    ax.set_xlabel("题目(按数据集顺序)")
    ax.axhline(summary.get("macro_total", 0), color="red", linestyle="--", linewidth=1,
               label=f"平均 {summary.get('macro_total', 0):.1f}")
    ax.legend(loc="upper left", fontsize=8)

    # 4) 红线通过率 / 概览
    ax = axes[1][1]
    ax.axis("off")
    if rl_pass_rate is not None:
        rl_pass = summary.get("red_line_pass", 0)
        rl_total = summary.get("red_line_total", 0)
        ax.barh([0], [rl_pass_rate * 100], color="#C44E52")
        ax.set_xlim(0, 100)
        ax.text(rl_pass_rate * 100 + 2, 0, f"{rl_pass_rate * 100:.1f}%", va="center", fontsize=10)
        ax.text(0, -0.45, f"红线通过率: {rl_pass} / {rl_total} 题",
                fontsize=10, transform=ax.get_yaxis_transform())
    else:
        ax.text(0.1, 0.6, "本次未包含红线题", fontsize=12, transform=ax.transAxes)
    ax.set_title("安全红线通过率")

    _watermark(fig)
    fig.tight_layout(rect=(0, 0.02, 1, 0.96))
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


def build_html(summary: dict, png_path: Path, out_html: Path) -> None:
    png_b64 = base64.b64encode(png_path.read_bytes()).decode()
    macro = summary.get("macro_total", 0)
    coverage = summary.get("coverage", 0)
    rl_pass_rate = summary.get("red_line_pass_rate")
    by_mod = summary.get("by_module", {})
    by_diff = summary.get("by_difficulty", {})
    details = summary.get("details", [])

    def _bar(v: float) -> str:
        w = max(0, min(100, v))
        return f'<div class="bar"><div class="fill" style="width:{w:.1f}%"></div><span>{v:.1f}</span></div>'

    mod_rows = "".join(
        f"<tr><td>{m}</td><td>{MODULE_CN.get(m, '')}</td><td>{_bar(by_mod[m])}</td></tr>"
        for m in sorted(by_mod)
    )
    diff_rows = "".join(
        f"<tr><td>{d}</td><td>{_bar(by_diff[d])}</td></tr>" for d in sorted(by_diff)
    )
    detail_rows = "".join(
        f"<tr><td>{d['item_id']}</td><td>{d['module']}</td>"
        f"<td>{SCENE_CN.get(d['scene_type'], d['scene_type'])}</td><td>{d['difficulty']}</td>"
        f"<td>{d['red_line']:.0f}</td><td>{d['lcs']:.2f}</td><td>{d['iou']:.2f}</td>"
        f"<td><b>{d['total']:.1f}</b></td></tr>"
        for d in details
    )
    rl_html = (
        f"{summary.get('red_line_pass', 0)} / {summary.get('red_line_total', 0)} "
        f"({rl_pass_rate * 100:.1f}%)"
        if rl_pass_rate is not None else "—"
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FK-Bench v2 评测报告</title>
<style>
  body {{ font-family: "Microsoft YaHei", "Segoe UI", sans-serif; margin: 24px; color: #222; }}
  h1 {{ border-bottom: 3px solid #4C72B0; padding-bottom: 8px; }}
  .cards {{ display: flex; gap: 16px; flex-wrap: wrap; margin: 16px 0; }}
  .card {{ background: #f6f8fa; border-radius: 8px; padding: 16px 20px; min-width: 140px; }}
  .card .num {{ font-size: 28px; font-weight: bold; color: #4C72B0; }}
  .card .lbl {{ color: #666; font-size: 13px; }}
  img.chart {{ max-width: 100%; border: 1px solid #e1e4e8; border-radius: 8px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 14px; }}
  th, td {{ border: 1px solid #e1e4e8; padding: 6px 10px; text-align: center; }}
  th {{ background: #f0f3f6; }}
  .bar {{ background: #eef1f4; border-radius: 6px; position: relative; height: 18px; min-width: 140px; }}
  .bar .fill {{ background: #55A868; height: 18px; border-radius: 6px; }}
  .bar span {{ position: absolute; right: 6px; top: 0; font-size: 12px; line-height: 18px; }}
  .watermark {{ margin-top: 24px; color: #999; font-size: 12px; text-align: center; }}
</style>
</head>
<body>
<h1>FK-Bench v2 评测报告</h1>
<div class="cards">
  <div class="card"><div class="num">{macro}</div><div class="lbl">Macro 总分 / 100</div></div>
  <div class="card"><div class="num">{coverage * 100:.0f}%</div><div class="lbl">覆盖率</div></div>
  <div class="card"><div class="num">{rl_html}</div><div class="lbl">红线通过</div></div>
  <div class="card"><div class="num">{len(details)}</div><div class="lbl">已评题目</div></div>
</div>
<img class="chart" src="data:image/png;base64,{png_b64}" alt="综合图表">
<h2>按模块平均分</h2>
<table><tr><th>模块</th><th>能力维度</th><th>得分</th></tr>{mod_rows}</table>
<h2>按难度平均分</h2>
<table><tr><th>难度</th><th>得分</th></tr>{diff_rows}</table>
<h2>逐题明细</h2>
<table><tr><th>题号</th><th>模块</th><th>场景</th><th>难度</th><th>红线</th><th>LCS</th><th>IoU</th><th>总分</th></tr>{detail_rows}</table>
<div class="watermark">{WATERMARK}</div>
</body>
</html>"""
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="forklift-visualize")
    parser.add_argument("--scores", type=Path, required=True, help="score.py 输出的 scores.json")
    parser.add_argument("--out", type=Path, default=None, help="输出目录(默认 scores.json 同目录/report)")
    args = parser.parse_args(argv)

    if not args.scores.exists():
        print(f"error: scores file not found: {args.scores}", file=sys.stderr)
        return 2

    summary = json.loads(args.scores.read_text(encoding="utf-8"))

    out_dir = args.out or (args.scores.parent / "report")
    png_path = out_dir / "scores_chart.png"
    html_path = out_dir / "report.html"

    build_chart(summary, png_path)
    build_html(summary, png_path, html_path)

    print(f"Chart  -> {png_path}")
    print(f"Report -> {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
