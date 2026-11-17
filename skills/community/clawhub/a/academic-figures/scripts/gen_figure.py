#!/usr/bin/env python3
"""
academic-figures v8.0.4: Publication-quality academic figure generator.

Generates charts from JSON/CSV data with:
- Publication-grade aesthetics (Nature/Science/Lancet style)
- Okabe-Ito colorblind-safe palette (Nature Methods gold standard)
- CJK (Chinese/Japanese/Korean) auto-detection, zero garbled text
- Bilingual labels (Chinese + English)
- Statistical annotations (error bars, significance markers)
- High-DPI output (600dpi default for line art, PDF/SVG/EPS/TIFF support)
- Enhanced forest plot (weights, heterogeneity I², events/total)

Usage:
  python gen_figure.py -t bar -d data.json -o figure.png
  python gen_figure.py -t heatmap -d data.json -o figure.png --cjk
  python gen_figure.py -t scatter -d data.csv -o figure.svg
  python gen_figure.py -t forest -d data.json -o figure.pdf --theme okabe-ito
  python gen_figure.py -t bar -d data.json -o figure.tiff --dpi 300

Data formats: JSON or CSV (first column = labels, rest = series)
"""
import argparse, json, csv, subprocess, sys, os, time, threading

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.transforms import BboxBase
import numpy as np

# v3.0.0 模块化：wizard 与异常诊断系统拆至独立模块（原名在此命名空间可用）
from af_wizard import _run_wizard
from af_resilience import spawn_retry as _spawn_retry, wd_scale as _wd_scale  # v6.2.0
from af_diagnostics import write_debug_report as _write_debug_report
_LAST_ARGS = None  # v6.4.0 --debug：main 局部 args 登记模块级，__main__ 异常层读
from af_diagnostics import (_EXIT_DATA_CLASSES, _EXIT_ENV_CLASSES,
                            _classify_exit_code, _diagnose_exception, _print_v3_error, _EXC_ZH_V3, _DIAG_PATTERNS,
                            _KNOWN_DATA_FIELDS)

try:
    import af_v23_stats as _afstats
    import af_v23_charts as _afcharts
except ImportError:  # v2.3 新图型/统计模块不在同目录时降级
    _afstats = None
    _afcharts = None

# ── v4.0.0 模块化第四刀：绘制层拆至 af_draw（生成器）/af_shared（叶工具）──
from af_shared import (has_cjk, HATCH_PATTERNS, _STYLE_NO_GRID, _SKETCH_MODE,
                        _ensure_ylabel_clear, CHART_NOTES, DEMO_DATA, list_flags_query, parse_inline_data, hero_panel_mode,
                        add_sig_bracket_arg, add_sig_auto_arg, load_cjk_font, advise_colorblind, parse_palette)
from af_draw import (GENERATORS, apply_base_style, _darken_color, _sig_stars, suggest_arena_note,
                     pairwise_vs_first, draw_bootstrap_brackets, annotate_bootstrap_stats, draw_stat_brackets,
                     annotate_auto_stats, annotate_multi_stats, gen_bar,
                     gen_heatmap, gen_scatter, gen_line, gen_box,
                     gen_forest, gen_violin, gen_km, gen_roc, gen_stacked_bar,
                     gen_dual_axis, gen_composite, gen_diagram, gen_flow, gen_prisma,
                     gen_slope, gen_volcano, gen_upset, gen_waterfall, waterfall_alt, validate_raincloud, raincloud_alt,
                     validate_waterfall, gen_swimmer, swimmer_alt, alt_text_core,
                     validate_swimmer,
                     gen_ridgeline, ridgeline_alt, validate_ridgeline,
                     write_audit_sidecar, gen_dumbbell, dumbbell_alt, validate_dumbbell,
                     write_repro_bundle,
                     gen_calibration, calibration_alt, validate_calibration,
                     gen_dca, dca_alt, validate_dca, format_suggest_line,
                     gen_nomogram, nomogram_alt, validate_nomogram, gen_rcs, rcs_alt, validate_rcs,
                     gen_subgroup_forest, subgroup_alt, validate_subgroup)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Style presets ──────────────────────────────────────────────────────
THEMES = {
    # v7.9.0 AF29：默认 glm-brand（品牌标识）。NOT colorblind-safe（字典如实标注；
    # 色盲安全场景用 okabe-ito，3+ 系列 stderr 提示）。语义色见各主题注释。
    # The old matplotlib-default palette is preserved as "classic".
    "classic": {
        "figsize": (10, 6),
        "dpi": 600,
        "font_size": 11,
        "colors": ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860",
                   "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"],
        "grid_alpha": 0.3,
        "spines": ["top", "right"],  # spines to hide
        "colorblind_safe": False,
    },
    # Okabe-Ito: Nature Methods recommended gold-standard colorblind-safe palette
    # Ref: Wong (2011) Nature Methods 8:441; Wilke "Fundamentals of Data Visualization"
    "okabe-ito": {
        "figsize": (8, 5.5),
        "dpi": 600,
        "font_size": 7,
        "colors": ["#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2",
                   "#D55E00", "#CC79A7", "#000000", "#999999", "#44AA99"],
        "grid_alpha": 0.2,
        "spines": ["top", "right"],
        "colorblind_safe": True,
    },
    "nature": {
        "figsize": (8, 5.5),
        "dpi": 600,
        "font_size": 7,
        "colors": ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F", "#8491B4",
                   "#91D1C2", "#DC0000", "#7E6148", "#B09C85"],
        "grid_alpha": 0.2,
        "spines": ["top", "right"],
        "colorblind_safe": False,
    },
    "lancet": {
        "figsize": (9, 6),
        "dpi": 600,
        "font_size": 7,
        "colors": ["#00468B", "#ED0000", "#42B540", "#0099B4", "#525252", "#7F6F00",
                   "#ED7D31", "#8B6914", "#4C0099", "#99CC00"],
        "grid_alpha": 0.25,
        "spines": ["top", "right"],
        "colorblind_safe": False,
    },
    # NEJM 官方风配色（ggsci nejm 色板，8 色）
    "nejm": {
        "figsize": (9, 6),
        "dpi": 600,
        "font_size": 8,
        "colors": ["#BC3C29", "#0072B5", "#E18727", "#20854E", "#7876B1", "#6F99AD",
                   "#FFDC91", "#EE4C97"],
        "grid_alpha": 0.25,
        "spines": ["top", "right"],
        "colorblind_safe": False,
    },
    # Science（AAAS）官方风配色（ggsci aaas 色板，10 色）
    "science": {
        "figsize": (8, 5.5),
        "dpi": 600,
        "font_size": 7,
        "colors": ["#3B4992", "#EE0000", "#008B45", "#631879", "#008280", "#BB0021",
                   "#5F559B", "#A20056", "#808180", "#1B1919"],
        "grid_alpha": 0.2,
        "spines": ["top", "right"],
        "colorblind_safe": False,
    },
    "conservative": {
        "figsize": (9, 5.5),
        "dpi": 600,
        "font_size": 8,
        "colors": ["#2E86C1", "#A0A0A0", "#E74C3C", "#27AE60", "#F39C12", "#8E44AD",
                   "#1ABC9C", "#E67E22", "#34495E", "#16A085"],
        "grid_alpha": 0.3,
        "spines": ["top", "right"],
        "colorblind_safe": False,
    },
    # GLM theme: elegant muted palette inspired by GLM-5.2 blog
    # Medium saturation — visible but not garish (素雅但不淡).
    # Darker than the raw blog pixels (#70A0D0 etc were too pale to read).
    # Verified: each color passes 4.5:1 contrast against white background.
    "glm": {
        "figsize": (10, 6),
        "dpi": 600,
        "font_size": 11,
        "colors": ["#5B8DBE",  # steel blue (比#70A0D0深一档，清晰可辨)
                   "#D79D55",  # warm yellow (GLM-5.2原图黄色像素均值，比#D09050亮一档)
                   "#6BA776",  # sage green
                   "#9B7BB8",  # dusty purple
                   "#C9694E",  # muted coral
                   "#5BA0A0",  # teal
                   "#B47A8E",  # mauve
                   "#7A7A7A",  # warm gray
                   "#C4A44A",  # mustard gold
                   "#7AAF42"],  # olive
        "grid_alpha": 0.15,
        "spines": ["top", "right"],
        "colorblind_safe": True,
    },
    "glm-brand": {
        "figsize": (10, 6),
        "dpi": 600,
        "font_size": 11,
        "colors": ["#2E5E8F",  # 深钢蓝（墨蓝方向一档，黑纹对比安全）
                   "#FFB627",  # 信号黄（品牌 token，蓝黄轴色盲安全）
                   "#6BA776",  # sage green
                   "#9B7BB8",  # dusty purple
                   "#C9694E",  # muted coral
                   "#5BA0A0",  # teal
                   "#B47A8E",  # mauve
                   "#7A7A7A",  # warm gray
                   "#C4A44A",  # mustard gold
                   "#8A9BA8"],  # blue gray
        "spines": ["top", "right"],
        "grid_alpha": 0.0,  # 品牌风格：无网格（Nature 版式语言）
        "hatch_edge": "auto",  # 斜纹色=填充同系深色（品牌精修）
        "colorblind_safe": False,  # v7.9.0 AF29：如实标注（黄蓝轴安全但 sage/coral 等非色盲全谱）
    },
    # Cool theme: elegant muted cool-toned palette (blues, teals, slate)
    # All colors in 190-260° hue range, low-medium saturation
    # Inspired by editorial design (FT/Economist) cool palettes
    "cool": {
        "figsize": (9, 5.5),
        "dpi": 600,
        "font_size": 8,
        "colors": ["#1B4965",  # deep navy
                   "#2E6F9E",  # ocean blue
                   "#4FA3C5",  # sky blue
                   "#3D8080",  # dark teal
                   "#62A0A8",  # medium teal
                   "#5B7BA0",  # steel blue-gray
                   "#7B9AB5",  # slate blue
                   "#9DB5CC"],  # pale steel
        "grid_alpha": 0.15,
        "spines": ["top", "right"],
        "colorblind_safe": True,
    },
}

THEME_ALIASES = {
    "okabe": "okabe-ito", "colorblind": "okabe-ito", "colorblind-safe": "okabe-ito",
    "okabeIto": "okabe-ito", "okabeito": "okabe-ito",
    "classic": "classic", "matplotlib": "classic", "default": "glm-brand",
    "glm": "glm", "glm-blog": "glm", "glmblog": "glm", "glm-brand": "glm-brand", "brand": "glm-brand", "glmb": "glm-brand",
    "cool": "cool", "cool-toned": "cool",
    "nature": "nature", "npg": "nature",
    "lancet": "lancet", "the-lancet": "lancet",
    "nejm": "nejm", "new-england": "nejm", "new-england-journal": "nejm",
    "science": "science", "aaas": "science",
    "conservative": "conservative", "conserv": "conservative",
}

THEME_SWATCH_DESCRIPTIONS = {
    "glm": "GLM 素雅莫兰迪风 · 色盲安全 · 钢蓝/暖黄/鼠尾草绿/灰紫/珊瑚",
    "glm-brand": "GLM 品牌视觉（默认）· 信号黄对比强化 · 无网格 · 同系深色斜纹",
    "classic": "经典 matplotlib 色板（v2.0 前的旧默认）",
    "okabe-ito": "Nature Methods 金标准 · 色盲安全 · 橙/天蓝/绿/黄/深蓝/红",
    "nature": "NPG 期刊风 · 红/蓝/绿/藏蓝",
    "lancet": "The Lancet 期刊风 · 深蓝/红/绿",
    "nejm": "NEJM 期刊风 · 砖红/钢蓝/橙/绿（8 色）",
    "science": "Science（AAAS）期刊风 · 藏蓝/红/绿/紫（10 色）",
    "conservative": "保守学术 · 蓝灰为主",
    "cool": "冷色调 · 深海军蓝→浅钢蓝 8 阶 · 色盲安全",
}

THEME_ORDER = ["glm-brand", "glm", "classic", "okabe-ito", "nature", "lancet", "nejm",
               "science", "conservative", "cool"]


def resolve_theme(name):
    """Resolve a --theme value to a canonical THEMES key (alias + lenient matching).
    Returns the canonical key, or None if no match."""
    if not name:
        return "glm-brand"  # v7.6 默认=品牌视觉（用户钦定黄蓝双斜线为默认输出）
    key = name.strip().lower()
    if key in THEMES:
        return key
    if key in THEME_ALIASES:
        return THEME_ALIASES[key]
    for canonical in THEMES:
        if canonical.startswith(key):
            return canonical
    return None




def cmd_list_themes():
    """Print all themes with ANSI color swatches."""
    for t in THEME_ORDER:
        desc = THEME_SWATCH_DESCRIPTIONS.get(t, "")
        colors = THEMES[t]["colors"]
        blocks = "".join(f"\x1b[48;2;{int(c[1:3],16)};{int(c[3:5],16)};{int(c[5:7],16)}m  \x1b[0m"
                         for c in colors)
        safe = "色盲安全" if THEMES[t].get("colorblind_safe") else ""
        print(f"  {t:<14} {blocks}  {desc} {safe}")
    print("\n用法: --theme <name>   别名: default/brand→glm-brand（引擎默认）, okabe→okabe-ito, classic→classic")


def cmd_theme_swatch(theme_key, out):
    """Render a swatch preview PNG for a theme."""
    t = THEMES[theme_key]
    colors = t["colors"]
    n = len(colors)
    import matplotlib.patches as mpatches
    fig, ax = plt.subplots(figsize=(max(6, n * 0.75), 2.2))
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for i, c in enumerate(colors):
        rect = mpatches.Rectangle((i + 0.1, 0.15), 0.8, 0.55, facecolor=c,
                                  edgecolor='black', linewidth=0.5)
        ax.add_patch(rect)
        ax.text(i + 0.5, 0.85, c, ha='center', va='bottom', fontsize=8)
    fig.suptitle(f"Theme: {theme_key}  ({n} colors)"
                 + ("  ·  colorblind-safe" if t.get("colorblind_safe") else ""),
                 fontsize=11, fontweight='bold')
    fig.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Swatch saved: {out}", file=sys.stderr)




def cmd_demo(args):
    """Interactive demo: menu of chart types, renders with sample data, prints the command used."""
    print("Academic Figures 交互演示 (v2.0+)\n选择图表类型:")
    types = [k for k in DEMO_DATA.keys() if k in GENERATORS]
    for i, t in enumerate(types, 1):
        print(f"  [{i}] {t}")
    sel = input(f"输入序号 (1-{len(types)}, 回车=1): ").strip() or "1"
    try:
        chart_type = types[int(sel) - 1]
    except (ValueError, IndexError):
        print("无效输入，使用 bar", file=sys.stderr)
        chart_type = "bar"
    import tempfile, json as _json
    tmpdir = tempfile.mkdtemp(prefix="af_demo_")
    data_path = os.path.join(tmpdir, "data.json")
    out_path = os.path.join(tmpdir, f"{chart_type}.png")
    with open(data_path, "w", encoding="utf-8") as f:
        _json.dump(DEMO_DATA[chart_type], f, ensure_ascii=False)
    cmd = (f"python3 scripts/gen_figure.py -t {chart_type} -d '{data_path}' -o '{out_path}' "
           f"--theme {args.theme or 'glm-brand'}")
    print(f"\n执行: {cmd}", file=sys.stderr)
    args.type, args.data, args.out = chart_type, data_path, out_path
    return True


def cmd_explain(chart_type):
    """Print usage notes for a chart type."""
    if chart_type not in GENERATORS:
        print(f"未知图表类型: {chart_type}", file=sys.stderr)
        print(f"可用: {', '.join(GENERATORS.keys())}", file=sys.stderr)
        sys.exit(1)
    print(f"[{chart_type}]")
    print(CHART_NOTES.get(chart_type, "参考文档相应章节。"))


# ── Chart-type suggestion (v2.1) ──────────────────────────────────────

def suggest_chart_type(data):
    """Heuristic chart-type recommendation from a loaded data dict.

    Returns [(score, chart_type, reason)] sorted best-first. Purely
    structural (no rendering) so it is safe to call on any input.
    """
    if not isinstance(data, dict):
        return []
    recs = []
    keys = set(data.keys())
    if "records_identified" in keys or "studies_included" in keys:
        recs.append((98, "prisma", "PRISMA flow fields (records_identified / studies_included)"))
    if isinstance(data.get("studies"), list) and data.get("studies") \
            and isinstance(data["studies"][0], dict) \
            and isinstance(data["studies"][0].get("judgements"), dict):
        recs.append((95, "rob", "studies[] with per-domain judgements (risk of bias traffic light)"))
    _s0 = (data.get("studies") or [None])[0]
    if isinstance(_s0, dict) and "events_t" in _s0: recs.append((95, "labbe", "studies[] with 2x2 events_t/n_t/events_c/n_c (L'Abbé plot; funnel needs effect/se instead)"))
    _sk = {str(k).strip().lower() for k in data.get("series", {}) or {}}
    if isinstance(data.get("time"), list) and isinstance(data.get("event"), list) \
            and isinstance(data.get("group"), list):
        recs.append((90, "subgroup", "long-format time/event/group lists → -t subgroup --stats cox (one-command fit)"))
    elif {"event", "status"} & _sk:
        # event/status 指示列=生存数据强信号（首列 time 常被 labels 吸收，故不要求 time 在 series）
        recs.append((90, "subgroup", "event indicator column → survival family; -t subgroup --stats cox = one-command fit"))
    if "blocks" in keys and "arrows" in keys:
        recs.append((96, "diagram", "blocks + arrows structure"))
    if "panels" in keys:
        recs.append((92, "composite", "multi-panel 'panels' definition"))
    curves = data.get("curves")
    if isinstance(curves, list) and curves and isinstance(curves[0], dict) \
            and {"fpr", "tpr"} <= set(curves[0]):
        recs.append((95, "roc", "curves[] with fpr/tpr arrays"))
    groups = data.get("groups")
    if isinstance(groups, dict) and groups:
        first = next(iter(groups.values()), None)
        if isinstance(first, list) and first and isinstance(first[0], (list, tuple)) \
                and len(first[0]) == 2:
            recs.append((94, "km", "groups mapped to [time, survival] step pairs"))
    _ev = data.get("event")
    if isinstance(data.get("time"), list) and isinstance(_ev, list) and \
            any((isinstance(v, (int, float)) and not isinstance(v, bool) and v >= 2)
                for v in _ev):
        recs.append((96, "cif", "time+event with competing-risk codes (≥2) — "
                     "cumulative incidence (Aalen-Johansen)"))
    if {"estimates", "ci_low", "ci_high"} <= keys:
        recs.append((93, "forest", "effect estimates with CI bounds"))
    if isinstance(data.get("matrix"), list):
        recs.append((88, "heatmap", "2D 'matrix'"))
    _sw_end = data.get("end")
    if isinstance(_sw_end, list) and _sw_end and \
            all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in _sw_end):
        recs.append((87, "swimmer", "per-subject 'end' durations — swimmer plot"))
    if {"left", "right"} <= keys:
        recs.append((86, "dual_axis", "left + right series for dual Y-axis"))
    if isinstance(data.get("datasets"), dict) and data["datasets"]:
        recs.append((72, "violin", "raw per-group 'datasets' — distribution view"))
        recs.append((70, "box", "raw per-group 'datasets' — boxplot view"))
        recs.append((71, "raincloud", "raw per-group 'datasets' — cloud+box+jitter trio"))
        recs.append((69, "ridgeline", "per-group 'datasets' — stacked-density ridgeline overview"))
    _db_f, _db_t = data.get("from"), data.get("to")
    if isinstance(_db_f, list) and isinstance(_db_t, list) and _db_f and \
            len(_db_f) == len(_db_t) and \
            all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in _db_f + _db_t):
        recs.append((85, "dumbbell", "per-row 'from'/'to' pairs — dumbbell gap chart"))
    x, y = data.get("x"), data.get("y")
    if isinstance(x, list) and isinstance(y, list) and x and len(x) == len(y):
        recs.append((80, "scatter", "paired x/y arrays"))
    # v4.5 R2-1：统计专用 schema 特征识别（此前 5 种形态全部误推荐为 bar）
    if {"log2fc", "pvalue"} <= keys:
        recs.append((91, "volcano", "log2fc + pvalue arrays — volcano plot"))
    studies = data.get("studies")
    if isinstance(studies, list) and studies and isinstance(studies[0], dict) \
            and "se" in studies[0]:
        recs.append((90, "funnel", "studies[] with se — funnel plot"))
        recs.append((85, "galbraith", "studies[] with se — Galbraith radial (heterogeneity/outliers)"))
    sets_ = data.get("sets")
    if isinstance(sets_, dict) and 2 <= len(sets_) <= 4 and \
            all(isinstance(v, list) for v in sets_.values()):
        recs.append((89, "venn", "sets{} element lists — venn/euler"))
    if isinstance(sets_, dict) and len(sets_) >= 5 and \
            all(isinstance(v, list) for v in sets_.values()):
        recs.append((92, "upset", "sets{} with ≥5 sets — UpSet intersection plot"))
    methods = data.get("methods")
    if isinstance(methods, dict) and len(methods) == 2 and \
            all(isinstance(v, list) for v in methods.values()):
        recs.append((88, "bland_altman", "two method arrays — bland-altman agreement"))
    if isinstance(data.get("fpr"), list) and isinstance(data.get("tpr"), list):
        recs.append((87, "roc", "flat fpr/tpr arrays — single-curve ROC"))
    if isinstance(data.get("models"), list) and data.get("thresholds"):
        recs.append((89, "dca", "thresholds + models[] net_benefit — decision curve"))
    if data.get("bins") or (data.get("predicted") and data.get("observed")):
        recs.append((88, "calibration", "predicted vs observed bins — calibration"))
    if data.get("variables") and data.get("outcome_scales"):
        recs.append((91, "nomogram", "variables + outcome_scales — nomogram"))
    if isinstance((_p0 := data.get("points")), list) and _p0 and isinstance(_p0[0], dict) and "est" in _p0[0]:
        recs.append((88, "rcs", "points[] est/ci grid — nonlinear dose-response"))
    if data.get("subgroups"):
        recs.append((93, "subgroup", "subgroups[] levels est/CI — subgroup forest"))
    series = data.get("series")
    if isinstance(series, dict) and series:
        lists = [v for v in series.values() if isinstance(v, list)]
        if lists and all(len(v) == 1 for v in lists):
            recs.append((68, "bar", "single-value series"))
        else:
            recs.append((76, "bar", "labels + named series"))
    seen = set()
    dedup = []
    for r in sorted(recs, key=lambda r: (-r[0], r[1])):
        if r[1] in seen:
            continue
        seen.add(r[1])
        dedup.append(r)
    return dedup


def cmd_suggest(data_path):
    """Analyze a data file and print recommended chart types + a ready-to-run command."""
    try:
        data = load_data(data_path)
    except Exception as e:
        print(f"ERROR: cannot load '{data_path}': {e}", file=sys.stderr)
        sys.exit(1)
    recs = suggest_chart_type(data)
    if not recs: print("No confident match — default to bar (labels + series). 无高匹配图型，默认柱状图；--explain <type> 可查字段说明。"); return
    print("Suggested chart types 推荐图型（按匹配度，best first）:")
    for i, (score, ctype, why) in enumerate(recs[:3], 1):
        print(format_suggest_line(i, score, ctype, why))
    best = recs[0][1]
    if _an := suggest_arena_note(best): print(_an)
    print(f"\nRun: python3 scripts/gen_figure.py -t {best} -d '{data_path}' -o out.pdf "
          f"--theme okabe-ito --verify  # --explain {best} 查字段说明")

# ── Journal presets (v2.0) ─────────────────────────────────────────────
# Column widths from Nature/Lancet author guidelines: single 89/85mm, double 183mm.
JOURNAL_PRESETS = {
    "nature": {"widths_mm": {"single": 89, "double": 183},
               "font_size": 7, "min_text_size": 5, "font_family": "Helvetica", "dpi": 600},
    "lancet": {"widths_mm": {"single": 85, "double": 183},
               "font_size": 8, "min_text_size": 6, "font_family": "Arial", "dpi": 600},
    # v2.2 international expansion — widths/min sizes follow each journal's
    # published author guidelines (commonly cited values); re-check the latest
    # guide before submission.
    "science": {"widths_mm": {"single": 55, "double": 120},
                "font_size": 7, "min_text_size": 5, "font_family": "Helvetica", "dpi": 600},
    "cell": {"widths_mm": {"single": 85, "double": 176},
             "font_size": 8, "min_text_size": 6, "font_family": "Arial", "dpi": 300},
    "nejm": {"widths_mm": {"single": 89, "double": 190},
             "font_size": 8, "min_text_size": 6, "font_family": "Helvetica", "dpi": 300},
    "jama": {"widths_mm": {"single": 89, "double": 183},
             "font_size": 8, "min_text_size": 6, "font_family": "Arial", "dpi": 600},
    "ieee": {"widths_mm": {"single": 89, "double": 181},
             "font_size": 8, "min_text_size": 6, "font_family": "Times New Roman", "dpi": 600},
    # Chinese presets — CJK font auto-enabled (cjk_default)
    "cma": {"widths_mm": {"single": 80, "double": 170},
            "font_size": 8, "min_text_size": 6, "font_family": "Arial", "dpi": 600,
            "cjk_default": True},
    "cn-core": {"widths_mm": {"single": 80, "double": 170},
                "font_size": 9, "min_text_size": 6, "font_family": "Arial", "dpi": 300,
                "cjk_default": True},
}

def _memory_hint(data, chart_type):
    """A3(v2.7)：渲染前对超大数据规模给中文提示（防内存型失败；只提醒不拦截）。"""
    try:
        n = 0
        if isinstance(data, dict):
            for v in data.values():
                if isinstance(v, list):
                    n += len(v)
                    n += sum(len(x) for x in v if isinstance(x, (list, tuple)))
                elif isinstance(v, dict):
                    for vv in v.values():
                        n += len(vv) if isinstance(vv, list) else 1
                elif isinstance(v, (int, float)):
                    n += 1
            if isinstance(data.get("matrix"), list):
                n = sum(len(r) for r in data["matrix"] if isinstance(r, list))
        if n > 1_000_000:
            print(f"提示：数据规模约 {n} 个数值点，内存占用较大。热图/聚类建议先按行聚合；"
                  "散点建议等距抽样到 1 万点内；也可降低 --dpi。", file=sys.stderr)
    except Exception:
        pass


def _load_journal_presets(base_dir=None):
    """A4(v2.7)：scripts/journal/*.json 为期刊预设唯一权威源（免费版=拍板基准）。
    目录缺失/单文件损坏时按刊回退内置值（离线与旧包永不受损）。"""
    import glob as _glob
    d = os.path.join(base_dir or os.path.dirname(os.path.abspath(__file__)), "journal")
    out = {}
    if os.path.isdir(d):
        for p in sorted(_glob.glob(os.path.join(d, "*.json"))):
            name = os.path.splitext(os.path.basename(p))[0]
            try:
                with open(p, encoding="utf-8") as fh:
                    spec = json.load(fh)
                for k in ("widths_mm", "font_size", "dpi"):
                    if k not in spec:
                        raise KeyError(f"缺少 {k}")
                out[name] = spec
            except Exception as exc:
                print(f"WARNING: 期刊预设 {os.path.basename(p)} 加载失败（{exc}），回退内置值",
                      file=sys.stderr)
    for k, v in _JOURNAL_BUILTIN.items():
        out.setdefault(k, v)
    return out


_JOURNAL_BUILTIN = {k: dict(v) for k, v in JOURNAL_PRESETS.items()}
JOURNAL_PRESETS = _load_journal_presets()

# v2.5：期刊预设 → 配色主题联动（用户显式给 --theme 时不覆盖）
JOURNAL_THEME = {"nature": "nature", "lancet": "lancet",
                 "nejm": "nejm", "science": "science"}

# Hatching patterns for bar charts (print-friendly + accessibility)
# ALL series get hatching when --hatch is enabled (including the first).
# Each series cycles through a different pattern so they're distinguishable
# even in black-and-white print. Hatch line color = black (edgecolor='black').
def generate_alt_text(chart_type, data, title=""):
    """One-paragraph accessibility description derived from the data dict.
    Written to <output>.alt.txt with --alt. EXTRA 图型（af_v23_charts）在此分流，
    核心分支=af_draw.alt_text_core（v4.10 移居，守 gen_figure <3400 行纪律）。"""
    if _afcharts is not None and chart_type in _afcharts.EXTRA_GENERATORS:
        return _afcharts.alt_extra(chart_type, data, title)
    return alt_text_core(chart_type, data, title)

# ── Font helpers ── load_cjk_font 已下沉 af_shared（v7.9.0 AF3 回退链），经顶部 import 引用。



def safe_text(ax, text, fontprop=None, **kwargs):
    """Set text with CJK font if needed."""
    if fontprop and has_cjk(str(text)):
        return ax.set_text(text) if hasattr(ax, 'set_text') else ax.text(text, fontproperties=fontprop, **kwargs)
    return ax.set_text(text) if hasattr(ax, 'set_text') else ax.text(text, **kwargs)


# ── Overlap prevention (mechanism-level) ───────────────────────────────

MIN_TICK_GAP = 6.0


def _boxes_overlap(b1, b2, ratio=0.04):
    """True if intersection area exceeds `ratio` of the smaller box."""
    inter = BboxBase.intersection(b1, b2)
    if inter is None or inter.width <= 0 or inter.height <= 0:
        return False
    inter_area = inter.width * inter.height
    return inter_area > ratio * min(b1.width * b1.height, b2.width * b2.height, 1)


def _adjacent_too_close(b1, b2, axis, min_gap=MIN_TICK_GAP):
    """True if two same-axis neighbor boxes touch or leave < min_gap px.

    Order-agnostic: tick-label order follows axis direction, which is
    inverted (top-to-bottom) on heatmap/forest/km axes. The gap is computed
    as the distance between the two boxes along the axis regardless of
    which one comes first in the list.
    """
    inter = BboxBase.intersection(b1, b2)
    if inter is not None and inter.width > 0 and inter.height > 0:
        return True
    if axis == 'x':
        gap = b2.x0 - b1.x1 if b2.x0 >= b1.x0 else b1.x0 - b2.x1
    else:
        gap = b1.y0 - b2.y1 if b1.y0 >= b2.y0 else b2.y0 - b1.y1
    return gap < min_gap


def _tick_boxes(ax, renderer):
    """Return (x_labels, y_labels, x_boxes, y_boxes) for visible tick labels.

    v5.4 机制修复：只统计视图区间内的刻度——区间外刻度渲染时不画，但其
    包围盒曾与轴角 y 标签假相交触发降级阶梯（DCA 着色首踩）。"""
    xl, yl, xb, yb = [], [], [], []
    x0v, x1v = sorted(ax.get_xlim())
    y0v, y1v = sorted(ax.get_ylim())
    for tv, lab in zip(ax.get_xticks(), ax.get_xticklabels()):
        if lab.get_text().strip() and lab.get_visible() and x0v <= tv <= x1v:
            xl.append(lab); xb.append(lab.get_window_extent(renderer))
    for tv, lab in zip(ax.get_yticks(), ax.get_yticklabels()):
        if lab.get_text().strip() and lab.get_visible() and y0v <= tv <= y1v:
            yl.append(lab); yb.append(lab.get_window_extent(renderer))
    return xl, yl, xb, yb



def _axis_has_overlap(xb, yb):
    """Check adjacent x-x, adjacent y-y (with min-gap), and x-y collisions."""
    for i in range(len(xb) - 1):
        if _boxes_overlap(xb[i], xb[i + 1]) or _adjacent_too_close(xb[i], xb[i + 1], 'x'):
            return True
    for i in range(len(yb) - 1):
        if _boxes_overlap(yb[i], yb[i + 1]) or _adjacent_too_close(yb[i], yb[i + 1], 'y'):
            return True
    for bx in xb:
        for by in yb:
            if _boxes_overlap(bx, by):
                return True
    return False


def _degrade_axis(ax, axis, level):
    """Apply one degradation step to tick labels. Returns True if applied.

    Ladder: 1 rotate 45° → 2 word-wrap → 3 shrink font → 4 rotate 90° →
    ≥5 stride-thinning. Labels are data: 90° rotation is always tried
    before any label is hidden, and every hidden label is reported by
    fix_tick_overlaps() so the data loss is never silent.
    """
    labels = ax.get_xticklabels() if axis == 'x' else ax.get_yticklabels()
    labels = [l for l in labels if l.get_text().strip()]
    if not labels:
        return False
    if level == 1 and axis == 'x':
        if _SKETCH_MODE[0] or all(l.get_rotation() == 45 for l in labels):
            return False  # sketch 手绘风：禁 45°（水平两行=wrap 产物，参考图口径）
        for l in labels:
            l.set_rotation(45)
            l.set_ha('right')
        return True
    if level == 2 and axis == 'x':
        wrapped = False
        for l in labels:
            if ' ' in l.get_text() and '\n' not in l.get_text():
                l.set_text('\n'.join(l.get_text().split(' ')))
                wrapped = True
        return wrapped
    if level == 3:
        sizes = {l.get_fontsize() for l in labels}
        if all(s <= 5 for s in sizes):
            return False
        for l in labels:
            l.set_fontsize(max(5, l.get_fontsize() - 1))
        return True
    if level == 4 and axis == 'x':
        if _SKETCH_MODE[0] or all(l.get_rotation() == 90 for l in labels):
            return False  # sketch 手绘风：禁 90°（宁可缩字不竖排）
        for l in labels:
            l.set_rotation(90)
            l.set_ha('center')
        return True
    if level >= 5 and _SKETCH_MODE[0]:
        return False  # v7.6.1 sketch 禁丢标签（模型名不可隐藏，宁可缩小字号）
    if level >= 5:
        stride = 2 ** (level - 4)
        hid = False
        for i, l in enumerate(labels):
            if i % stride != 0 and l.get_visible():
                l.set_visible(False)
                hid = True
        return hid
    return False


def fix_tick_overlaps(fig):
    """Post-render collision detection + auto-degradation ladder.

    Draws the figure, measures real tick-label bounding boxes, and applies
    rotation 45° → word-wrap → font-shrink → rotation 90° → stride-thinning
    until no axis (including composite panels) has overlapping labels.
    Stride-thinning hides labels (data loss) only after geometric fixes are
    exhausted, and prints a stderr warning whenever it fires.
    """
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for _pass in range(8):
        fixed_any = False
        for ax in fig.axes:
            if getattr(ax, "_af_category_axis", False):
                continue  # 热图家族：行列标签即数据，禁止降级抽稀（机制豁免）
            xl, yl, xb, yb = _tick_boxes(ax, renderer)
            if not _axis_has_overlap(xb, yb):
                continue
            for level in range(1, 11):
                if not _axis_has_overlap(xb, yb):
                    break
                if level in (1, 2, 4) and not xl:
                    continue
                applied = _degrade_axis(ax, 'x', level)
                if not applied and level >= 3:
                    applied = _degrade_axis(ax, 'y', level)
                if applied:
                    fixed_any = True
                    fig.canvas.draw()
                    renderer = fig.canvas.get_renderer()
                    xl, yl, xb, yb = _tick_boxes(ax, renderer)
        if not fixed_any:
            break

    hidden = sum(1 for ax in fig.axes
                 for l in ax.get_xticklabels() + ax.get_yticklabels()
                 if l.get_text().strip() and not l.get_visible())
    if hidden:
        print(f"academic-figures WARNING: hid {hidden} tick label(s) to resolve "
              f"overlap — hidden labels are lost data; increase --width/--height "
              f"or shorten labels", file=sys.stderr)


def place_annotation(ax, text, xy, fontsize=9.5, fontweight='bold', color='black', ha='center'):
    """Place an annotation, testing candidate offsets against existing text
    boxes (greedy collision avoidance). Returns the placed Text artist."""
    fig = ax.figure
    candidates = [(0, 14), (0, -24), (16, 0), (-16, 0), (0, 32), (0, -42),
                  (30, 14), (-30, 14), (30, -24), (-30, -24), (30, 32), (-30, -42)]
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    placed = [t.get_window_extent(renderer) for t in ax.texts if t.get_text().strip()]
    for dx, dy in candidates:
        t = ax.annotate(text, xy=xy, xytext=(dx, dy), textcoords='offset points',
                        ha=ha, va='center', fontsize=fontsize, fontweight=fontweight, color=color)
        fig.canvas.draw()
        bb = t.get_window_extent(renderer)
        if not any(_boxes_overlap(bb, pb) for pb in placed):
            return t
        t.remove()
    return ax.annotate(text, xy=xy, xytext=(0, 14), textcoords='offset points',
                       ha=ha, va='center', fontsize=fontsize, fontweight=fontweight, color=color)


# ── Data loading ───────────────────────────────────────────────────────

def _is_number(s):
    """Check if string represents a number."""
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def _classify_num_policy(vals):
    """v4.5 R2-7/R2-8 数值策略硬化：对数值数组分类
    返回 (bools, nonnum_strs, strnum_ok, infs) 计数——bool/inf=fatal，字符串数字=自动转换+警告。"""
    import math as _m
    bools = strnum = infs = 0
    for v in vals:
        if isinstance(v, bool):
            bools += 1
        elif isinstance(v, (int, float)):
            if isinstance(v, float) and not _m.isfinite(v):
                infs += 1
        elif isinstance(v, str):
            try:
                float(v)
                strnum += 1
            except ValueError:
                pass
    return bools, strnum, infs


def _read_excel(path, sheet=None):
    """Read an Excel sheet into (headers, rows-of-str) — the same shape the
    CSV branch of load_data() consumes. First non-empty row is the header."""
    try:
        import openpyxl
    except ImportError:
        raise ValueError(
            "xlsx requires openpyxl — install with: pip install openpyxl "
            "(or export the sheet to CSV)")
    try:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    except Exception as e:
        raise ValueError(
            f"cannot read {os.path.basename(path)} as Excel (.xlsx): {e} — "
            f"if the file is CSV/TSV, rename it to .csv")
    try:
        if sheet and sheet not in wb.sheetnames:
            raise ValueError(f"sheet '{sheet}' not found in {os.path.basename(path)} — "
                             f"available: {wb.sheetnames}")
        ws = wb[sheet] if sheet else wb.active
        rows_raw = list(ws.iter_rows(values_only=True))
    finally:
        wb.close()
    rows_raw = [r for r in rows_raw
                if any(v is not None and str(v).strip() != "" for v in r)]
    if not rows_raw:
        raise ValueError(f"sheet is empty: {os.path.basename(path)}")
    headers = ["" if v is None else str(v).strip() for v in rows_raw[0]]
    rows = [[("" if v is None else str(v).strip()) for v in r]
            for r in rows_raw[1:]]
    return headers, rows


def load_data(path, chart_type=None, sheet=None, csv_errors=True):
    """Load data from JSON, CSV or Excel (.xlsx/.xls). Returns dict with structure info.

    For CSV/Excel, chart_type is used to auto-convert long-format data:
    - scatter: first two numeric cols → {x, y}, third col → groups
    - box/violin: first col as groups, second numeric col as values → {series: {group: [values]}}
    - sheet: Excel only — sheet name (default: first/active sheet)
    """
    if (_inline := parse_inline_data(path)) is not None: return _inline  # v7.7.2 AF1：inline 简写（af_shared 真值，行预算纪律下沉）
    ext = os.path.splitext(path)[1].lower()
    if ext == '.json':
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except UnicodeDecodeError:
            raise ValueError("文件不是 UTF-8 编码（疑似 GBK/Excel 另存）——请用文本编辑器"
                             "另存为 UTF-8 后重试，或 iconv -f GBK -t UTF-8 转换")
    elif ext in ('.csv', '.tsv', '.xlsx', '.xls'):
        if ext in ('.csv', '.tsv'):
            delimiter = '\t' if ext == '.tsv' else ','
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=delimiter)
                headers = next(reader)
                rows = list(reader)
        else:
            headers, rows = _read_excel(path, sheet)
        # Build series, skipping non-numeric columns (C1 fix)
        # Identify numeric columns: >50% of values must be parseable as numbers
        numeric_col_indices = []
        for i, h in enumerate(headers):
            if i == 0:
                continue
            num_count = sum(1 for r in rows if i < len(r) and _is_number(r[i]))
            if num_count > len(rows) * 0.5:
                numeric_col_indices.append(i)

        # Collect all rows with non-numeric values across numeric columns (union)
        bad_rows = set()
        for i in numeric_col_indices:
            for ri, r in enumerate(rows):
                if ri < len(r) and not _is_number(r[i]):
                    bad_rows.add(ri)

        # Build series using only valid rows
        good_rows = [ri for ri in range(len(rows)) if ri not in bad_rows]
        series = {}
        for i in numeric_col_indices:
            vals = [float(rows[ri][i]) for ri in good_rows if ri < len(rows)]
            if vals:
                series[headers[i]] = vals

        # Sync labels with valid rows
        labels = [rows[ri][0] for ri in good_rows if ri < len(rows)]
        result = {"labels": labels, "series": series}

        # ── v6.0.0：CSV 误差列约定——X_se/X_sem/X_sd/X_err 配对主列 X（准确性审查
        # 与实现脱节的旧表述机制根治）。配对成功→不画成柱、转 errors 契约；
        # X_sd + X_n → SEM=sd/√n；孤儿列告警保留；--csv-no-errors 逃生门。
        if csv_errors and series:
            import re as _re
            _err_cols, _n_cols = {}, {}
            for k in list(series.keys()):
                m = _re.match(r"^(.*)_(sem|se|sd|err)$", str(k), _re.I)
                if m:
                    _err_cols[m.group(1)] = (k, m.group(2).lower())
                elif _re.match(r"^(.*)_n$", str(k), _re.I):
                    _n_cols[_re.match(r"^(.*)_n$", str(k), _re.I).group(1)] = k
            errors, notes = {}, []
            for base, (col, kind) in sorted(_err_cols.items()):
                if base not in series:
                    print(f"CSV 误差列告警：「{col}」找不到主列「{base}」——按普通数据列处理",
                          file=sys.stderr)
                    continue
                if len(series[col]) != len(series[base]):
                    print(f"CSV 误差列告警：「{col}」与主列「{base}」行数不一致——按普通数据列处理",
                          file=sys.stderr)
                    continue
                vals = series[col]
                if kind == "sd" and base in _n_cols:
                    nn = series[_n_cols[base]]
                    import math as _m
                    if len(nn) == len(vals) and all(v > 0 for v in nn):
                        vals = [v / _m.sqrt(n) for v, n in zip(vals, nn)]
                        notes.append(f"{_n_cols[base]}+{col} → {base}（SD+标本量→SEM=sd/√n）")
                        del series[_n_cols[base]]
                    else:
                        notes.append(f"{col} → {base}（±1SD；{_n_cols[base]} 行数不符/含非正值，未转 SEM）")
                else:
                    _lab = "SEM" if kind in ("sem", "se") else ("SD" if kind == "sd" else "误差值")
                    notes.append(f"{col} → {base}（±1{_lab}）")
                errors[base] = vals
                del series[col]
            if errors:
                result["errors"] = errors
                print("CSV 误差列识别：" + "；".join(notes)
                      + "（--csv-no-errors 可关闭，把误差列按普通数据画）", file=sys.stderr)

        # Long-format conversion for scatter (C1 real fix)
        if chart_type == 'scatter' and series:
            # Collect ALL numeric columns including index 0 if numeric header
            all_numeric = []
            for i, h in enumerate(headers):
                num_count = sum(1 for ri in good_rows if ri < len(rows) and _is_number(rows[ri][i]))
                if num_count > len(good_rows) * 0.5:
                    all_numeric.append((i, h))

            if len(all_numeric) >= 2:
                col_i, col_x_name = all_numeric[0]
                col_j, col_y_name = all_numeric[1]
                x_vals = [float(rows[ri][col_i]) for ri in good_rows if ri < len(rows) and col_i < len(rows[ri])]
                y_vals = [float(rows[ri][col_j]) for ri in good_rows if ri < len(rows) and col_j < len(rows[ri])]

                groups = None
                # Check remaining columns for groups (non-numeric with multiple unique values)
                if len(all_numeric) >= 3:
                    # Use third numeric column's position to find non-numeric columns
                    pass  # groups will be below
                # Try non-numeric columns for groups — prefer name hint, then fewest unique vals
                _group_hints = {'group', 'groups', 'category', 'categories', 'class', 'label', 'labels', 'type'}
                candidates = []
                for i, h in enumerate(headers):
                    if i in [idx for idx, _ in all_numeric]:
                        continue
                    vals = [rows[ri][i] for ri in good_rows if ri < len(rows)]
                    unique = set(vals)
                    if len(unique) > 1 and len(unique) <= 20:
                        score = (0, len(unique), i)  # (hint_match, unique_count, col_index)
                        if h.lower().strip() in _group_hints:
                            score = (-1, len(unique), i)
                        candidates.append((score, vals, h))
                if candidates:
                    candidates.sort()
                    groups = candidates[0][1]

                result = {"x": x_vals, "y": y_vals}
                if groups:
                    result["groups"] = groups
            elif len(all_numeric) == 1:
                # Only one numeric series from wide format, try using it as y with row index as x
                col_i, col_name = all_numeric[0]
                y_vals = [float(rows[ri][col_i]) for ri in good_rows if ri < len(rows) and col_i < len(rows[ri])]
                # Check if labels (first col) are numeric → use as x
                if labels and all(_is_number(l) for l in labels):
                    result = {"x": [float(l) for l in labels], "y": y_vals}
                else:
                    result = {"x": list(range(len(y_vals))), "y": y_vals, "groups": labels}

        # Long-format conversion for box/violin (C4 real fix)
        if chart_type in ('box', 'boxplot', 'violin') and series:
            first_col_vals = [rows[ri][0] for ri in good_rows if ri < len(rows)]
            unique_groups = list(dict.fromkeys(first_col_vals))  # preserve order
            # Check if first column looks like group labels (many repeats)
            if len(unique_groups) < len(first_col_vals) * 0.8 and len(unique_groups) >= 2:
                # Long format: group column + value column
                num_col_idx = numeric_col_indices[0] if numeric_col_indices else None
                if num_col_idx is not None:
                    grouped = {}
                    for g in unique_groups:
                        grouped[g] = []
                    for ri in good_rows:
                        if ri < len(rows) and num_col_idx < len(rows[ri]):
                            g = rows[ri][0]
                            v = rows[ri][num_col_idx]
                            if _is_number(v):
                                grouped[g].append(float(v))
                    # Only use if groups have multiple values
                    if any(len(v) >= 2 for v in grouped.values()):
                        result = {"labels": unique_groups, "series": grouped}

        return result
    else:
        raise ValueError(f"不支持的数据格式: {ext}。请改用 .json / .csv / .tsv / .xlsx")


# ── Data validation layer (v2.0) ───────────────────────────────────────

def _preflight_advisories(data, chart_type, downsample=None):
    """v2.9：渲染前预判式提示（纯函数，返回中文提示列表）。提前预判，不等硬限报错。"""
    msgs = []
    try:
        if (chart_type == "cluster_heatmap" and isinstance(data, dict)
                and not downsample):
            rows = len(data.get("matrix") or [])
            if rows > 1500:
                msgs.append(
                    f"cluster_heatmap 行数 {rows} 已超过建议值 1500（硬上限 3000）："
                    "聚类更慢、内存更高——建议加 --downsample 2000 等距采样；"
                    "如确需全量渲染可忽略本提示")
    except Exception:
        pass
    return msgs


def _field_nearmiss_warnings(data):
    """v2.9：dict 数据中出现"形似已知字段"的未知键时给中文纠错告警（非致命）。"""
    msgs = []
    try:
        if isinstance(data, dict):
            import difflib as _dif
            for k in data.keys():
                if (not isinstance(k, str) or k.startswith("_")
                        or k in _KNOWN_DATA_FIELDS):
                    continue
                near = _dif.get_close_matches(k, _KNOWN_DATA_FIELDS, n=1, cutoff=0.6)
                if near:
                    msgs.append(
                        f"字段名 '{k}' 不是有效字段——是否想用 '{near[0]}'？"
                        "（大小写与下划线必须完全一致；无法识别的字段会被忽略；"
                        "各图型字段见 --explain）")
    except Exception:
        pass
    return msgs


# ── v3.9：--order 类别顺序 / --normalize 归一化 / --doctor 体检 ──────────
_ORDER_CHARTS = ("bar", "grouped_bar", "hbar", "horizontal_bar", "stacked_bar",
                 "box", "violin", "line")
_NORM_CHARTS = ("bar", "grouped_bar", "hbar", "horizontal_bar", "stacked_bar", "line")


def apply_series_order(data, order, chart_type):
    """v3.9 --order：重排类别（bar 系/line 重排 labels 并同位列数组；
    box/violin 重排系列键）。显式列表须恰好覆盖全部标签；
    auto=按第一系列值降序（box/violin 按各组中位数降序）。
    significance 的 "系列:列索引" 键随重排改写。"""
    if chart_type in ("box", "violin"):
        series = data.get("series", data.get("datasets"))
        if not isinstance(series, dict) or not series:
            print("WARNING: --order 需要 {组名: 数值数组} 系列型数据，未找到——跳过",
                  file=sys.stderr)
            return
        names = list(series.keys())
        if order == "auto":
            new_names = sorted(
                names,
                key=lambda n: -float(np.median([float(v) for v in series[n]])))
        else:
            want = [w.strip() for w in order.split(",") if w.strip()]
            missing = [w for w in want if w not in names]
            if missing:
                raise ValueError(f"--order 标签未找到：{'、'.join(missing)}"
                                 f"（现有组：{'、'.join(names)}）")
            if sorted(want) != sorted(names):
                raise ValueError("--order 须恰好列出全部组名（不得多/少/重复）")
            new_names = want
        data["series"] = {n: series[n] for n in new_names}
        for k in ("labels", "x"):
            if isinstance(data.get(k), list) and len(data[k]) == len(names):
                data[k] = list(new_names)
        print(f"order: 类别顺序已重排 → {' → '.join(new_names)}", file=sys.stderr)
        return
    labels = data.get("labels", data.get("x"))
    series = data.get("series", data.get("datasets"))
    if not isinstance(labels, list) or not labels or not isinstance(series, dict):
        print("WARNING: --order 需要 labels+series 数据结构，未找到——跳过", file=sys.stderr)
        return
    labels = [str(l) for l in labels]
    if order == "auto":
        first = next(iter(series.values()))
        try:
            fv = [float(first[i]) for i in range(len(labels))]
        except Exception:
            print("WARNING: --order auto 无法读取第一系列数值——跳过", file=sys.stderr)
            return
        pairs = sorted(range(len(labels)), key=lambda i: -fv[i])
        new_labels = [labels[i] for i in pairs]
    else:
        want = [w.strip() for w in order.split(",") if w.strip()]
        missing = [w for w in want if w not in labels]
        if missing:
            raise ValueError(f"--order 标签未找到：{'、'.join(missing)}"
                             f"（现有：{'、'.join(labels)}）")
        if len(want) != len(labels) or len(set(want)) != len(labels):
            raise ValueError("--order 须恰好列出全部类别标签（不得重复/缺漏）")
        new_labels = want
    perm = [labels.index(l) for l in new_labels]

    def _perm(arr):
        if isinstance(arr, list) and len(arr) == len(labels):
            return [arr[i] for i in perm]
        return arr

    data["labels"] = new_labels
    if isinstance(data.get("x"), list):
        data["x"] = new_labels
    for sk, sv in series.items():
        if isinstance(sv, list):
            series[sk] = _perm(sv)
    if isinstance(data.get("errors"), dict):
        for ek, ev in data["errors"].items():
            if isinstance(ev, list):
                data["errors"][ek] = _perm(ev)
    sig = data.get("significance")
    if isinstance(sig, dict) and sig:
        inv = {old: new for new, old in enumerate(perm)}
        data["significance"] = {
            (f"{k.rpartition(':')[0]}:{inv[int(k.rpartition(':')[2])]}"
             if k.rpartition(":")[1] and k.rpartition(":")[2].isdigit()
             and int(k.rpartition(":")[2]) in inv else k): v
            for k, v in sig.items()}
    print(f"order: 类别顺序已重排 → {' → '.join(new_labels)}", file=sys.stderr)


def apply_normalize(data, mode, chart_type):
    """v3.9 --normalize：baseline=各系列÷第一系列均值（对照=1）；
    pct100=各系列÷自身首点×100（T0=100）。误差数组同步缩放。
    分布类（box/violin）不适用（flag 门 [ignored] 拦截）。"""
    series = data.get("series", data.get("datasets"))
    if not isinstance(series, dict) or not series:
        print("WARNING: --normalize 需要 series 数据，未找到——跳过", file=sys.stderr)
        return

    def _num(arr):
        try:
            return [float(v) for v in arr]
        except (TypeError, ValueError):
            return None

    names = list(series.keys())
    conv = {}
    if mode == "baseline":
        base_vals = _num(series[names[0]])
        if not base_vals:
            raise ValueError(f"--normalize baseline：第一系列「{names[0]}」非数值")
        base = float(np.mean(base_vals))
        if base == 0:
            raise ValueError("--normalize baseline：第一系列均值为 0，不能作基线（请检查数据）")
        for n in names:
            vals = _num(series[n])
            if vals is None:
                raise ValueError(f"--normalize：系列「{n}」含非数值")
            series[n] = [v / base for v in vals]
            conv[n] = 1.0 / base
        print(f"normalize baseline: 各系列已÷第一系列「{names[0]}」均值 {base:.4g}"
              f"（该系列现=1.00；误差棒同步缩放；原始数值请保留源数据）", file=sys.stderr)
    else:
        for n in names:
            vals = _num(series[n])
            if not vals:
                raise ValueError(f"--normalize：系列「{n}」非数值")
            if vals[0] == 0:
                raise ValueError(f"--normalize pct100：系列「{n}」首点为 0，"
                                 "不能作基期（请检查数据或改用 --normalize baseline）")
            f = 100.0 / vals[0]
            series[n] = [v * f for v in vals]
            conv[n] = f
        print("normalize pct100: 各系列已按自身首点=100 归一"
              "（误差棒同步缩放；原始数值请保留源数据）", file=sys.stderr)
    if isinstance(data.get("errors"), dict):
        for ek, ev in data["errors"].items():
            vals = _num(ev) if isinstance(ev, list) else None
            if vals and ek in conv:
                data["errors"][ek] = [v * conv[ek] for v in vals]


def _auto_summary(data, chart_type):
    """v4.1 --summary：从数据派生纯计数事实摘要（零推断）。派生不了的图型返回 None。"""
    def _num_list(v):
        return [float(x) for x in v if isinstance(x, (int, float))]

    if chart_type in ("km", "survival"):
        groups = data.get("groups") or {}
        if not isinstance(groups, dict) or not groups:
            return None
        n = ev = 0
        for pairs in groups.values():
            for p in pairs if isinstance(pairs, list) else []:
                if isinstance(p, (list, tuple)) and len(p) >= 2:
                    n += 1
                    if p[1] == 1:
                        ev += 1
        return f"n={n} 例 · 事件 {ev} 例 · {len(groups)} 组"
    series = data.get("series", data.get("datasets"))
    labels = data.get("labels", data.get("x", []))
    if not isinstance(series, dict) or not series:
        return None
    n = sum(len(_num_list(v)) for v in series.values())
    if n == 0:
        return None
    g_txt = f"{len(labels)} 组" if isinstance(labels, list) and labels else f"{len(series)} 系列"
    return f"n={n} · {g_txt}"


def _doctor_report(args, data):
    """v3.9 --doctor：渲染前参数/环境体检。返回需注意项数（0=全绿）。
    只报告不改退出码（带 -o 时继续渲染）；省略 -o 时 exit 1=有问题。"""
    import importlib
    issues = 0
    print("── doctor 参数/环境体检（v3.9）──", file=sys.stderr)
    import af_diagnostics as _afd
    issues += _afd.doctor_composite_shared_scale(data, lambda s: print(s, file=sys.stderr))
    combos = [
        (args.stats in ("auto", "multi", "bootstrap") and args.type not in ("box", "violin", "raincloud"),
         f"--stats {args.stats} 仅 box/violin/raincloud 生效"),
        (args.stats == "cox" and args.type not in ("forest", "subgroup"),
        "--stats cox 仅 forest/subgroup 生效"),
        (bool(args.compare) and args.type != "roc", "--compare 仅 roc 生效"),
        (bool(args.egger) and args.type != "funnel", "--egger 仅 funnel 生效"),
        (bool(args.hatch) and not getattr(args, "_hatch_implicit", False) and args.type not in ("bar", "grouped_bar", "hbar", "horizontal_bar", "stacked_bar"), "--hatch 仅 bar 系生效"),
        (bool(args.area) and args.type != "venn", "--area 仅 venn 生效"),
        (bool(args.sheet) and not str(args.data or "").lower().endswith((".xlsx", ".xls")),
         "--sheet 仅 .xlsx/.xls 生效"),
        (bool(getattr(args, "order", None)) and args.type not in _ORDER_CHARTS,
         "--order 仅 bar/box/violin/line 系生效"),
        (bool(getattr(args, "normalize", None)) and args.type not in _NORM_CHARTS,
         "--normalize 仅 bar 系/line 生效（分布数据不做均值归一）"),
        (bool(args.journal) and bool(args.width),
         "--journal 会锁定图宽，--width 将被覆盖（去掉 --width 或改用 --column）"),
    ]
    for bad, msg in combos:
        if bad:
            issues += 1
            print(f"  [!] {msg}", file=sys.stderr)
    try:
        fatal, warns = validate_data(data, args.type)
        if fatal:
            issues += len(fatal)
            for m in fatal:
                print(f"  [!] 数据致命: {m}", file=sys.stderr)
        else:
            print(f"  [ok] 数据结构校验通过（{args.type}）"
                  + (f"；{len(warns)} 条警告" if warns else ""), file=sys.stderr)
    except Exception as e:
        issues += 1
        print(f"  [!] 数据校验异常: {e}", file=sys.stderr)
    for mod, hint in (("numpy", "numpy"), ("matplotlib", "matplotlib"),
                      ("scipy", "scipy（仅 --stats 需要）")):
        try:
            importlib.import_module(mod)
        except Exception:
            print(f"  [!] 缺依赖 {hint}", file=sys.stderr)
            issues += 1
    if args.out:
        od = os.path.dirname(os.path.abspath(args.out))
        if not os.path.isdir(od):
            issues += 1
            print(f"  [!] 输出目录不存在: {od}", file=sys.stderr)
        elif not os.access(od, os.W_OK):
            issues += 1
            print(f"  [!] 输出目录不可写: {od}", file=sys.stderr)
        else:
            print(f"  [ok] 输出目录可写: {od}", file=sys.stderr)

    def _scan(o):
        if isinstance(o, str):
            return has_cjk(o)
        if isinstance(o, dict):
            return any(_scan(k) or _scan(v) for k, v in o.items())
        if isinstance(o, (list, tuple)):
            return any(_scan(v) for v in o)
        return False

    if any(has_cjk(t) for t in (args.title, args.xlabel, args.ylabel) if t) or _scan(data):
        print("  [i] 检测到中文文本——将自动加载 CJK 字体（--cjk 可显式指定）", file=sys.stderr)
    if str(args.out or "").lower().endswith((".pdf", ".tiff", ".tif", ".eps")) \
            and not getattr(args, "verify", False):
        print("  [i] 投稿格式输出建议加 --verify（重叠/元数据门禁；一键投稿包用 --pub-ready）",
              file=sys.stderr)
    print(f"── doctor 完成：{'✅ 未发现问题' if issues == 0 else f'⚠️ {issues} 项需注意'} ──",
          file=sys.stderr)
    return issues


def validate_data(data, chart_type):
    """Unified data validation: fatal errors + degradation warnings.

    Returns (fatal_msgs, warning_msgs).
    - fatal: figure CANNOT be drawn correctly -> caller must abort (exit code 1)
    - warning: figure can be drawn but data looks suspicious -> caller prints WARNING

    Covers per-type required fields, numeric types, length matching, and
    degenerate-data detection (all-equal series, non-finite values, ragged rows).
    """
    fatal, warns = [], []

    if not isinstance(data, dict):
        fatal.append("数据必须是非空 JSON 对象，或由 CSV 转换来的字典")
        return fatal, warns

    def _nonempty_list(v):
        return isinstance(v, (list, tuple)) and len(v) > 0

    def _len(v):
        return len(v) if isinstance(v, (list, tuple)) else 0

    def _warn_flat(name, vals):
        """Detect all-equal series -> flat chart, usually a data bug."""
        fvals = [float(v) for v in vals if _is_number(v)]
        if len(fvals) >= 2 and max(fvals) == min(fvals):
            warns.append(
                f"系列 '{name}' 的值全部相同（恒为 {fvals[0]:g}）— 图会是一条平线。"
                f"请确认这是数据本意，而不是取错了列")

    def _warn_non_numeric(name, vals):
        # v4.5 R2-7/R2-8/P2-5 数值策略硬化：
        #   bool / inf → fatal（语义错误/轴无意义）；字符串数字 → 自动转换+警告；
        #   None → 跳过（gen 层已实现，计数警告保持）
        n_bool = sum(1 for v in vals if isinstance(v, bool))
        if n_bool:
            fatal.append(f"系列 '{name}' 里有 {n_bool} 个布尔值（true/false 不是数值）— "
                         "请把布尔列转成 0/1 或删除")
        n_inf = sum(1 for v in vals
                    if isinstance(v, float) and (v == float("inf") or v == float("-inf")))
        if n_inf:
            fatal.append(f"系列 '{name}' 里有 {n_inf} 个 inf（通常由 1/0 或溢出产生）— "
                         "请清洗源数据后再画图")
        n_strnum = sum(1 for v in vals
                       if isinstance(v, str) and _is_number(v))
        if n_strnum:
            warns.append(f"系列 '{name}' 里有 {n_strnum} 个字符串数字已自动转换为数值"
                         "（建议源数据直接存数值）")
            for j, v in enumerate(vals):
                if isinstance(v, str) and _is_number(v):
                    try:
                        vals[j] = float(v) if "." in v or "e" in v.lower() else int(float(v))
                    except (ValueError, OverflowError):
                        pass
        n_bad = sum(1 for v in vals
                    if not isinstance(v, (int, float)) and not _is_number(v))
        if n_bad:
            warns.append(
                f"系列 '{name}' 里有 {n_bad} 个非数值项，画图时会跳过 — "
                f"请检查源数据里是否混入了 'NA'、'—' 或文字")

    def _check_series_dict(series, err_key, req_nonempty=True):
        """Validate a {name: [values]} dict. Returns fatal messages list."""
        msgs = []
        if not isinstance(series, dict):
            msgs.append(f"'{err_key}' 必须是 JSON 对象（形如 {{\"系列名\": [数值, ...]}}）— 当前类型不符")
            return msgs
        if req_nonempty and not series:
            msgs.append(f"'{err_key}' 是空的 — 至少要有一个系列（一组名称+数值数组）")
            return msgs
        empty_names = [n for n, v in series.items() if not _nonempty_list(v)]
        if empty_names:
            msgs.append(f"'{err_key}' 里这些系列没有数据: {empty_names[:3]}"
                        f"{'...' if len(empty_names) > 3 else ''} — 空系列无法画，请删掉或补数据")
        for n, v in series.items():
            if _nonempty_list(v):
                _warn_non_numeric(n, v)
                _warn_flat(n, v)
        return msgs

    # ── bar family: labels + series (+ errors / significance) ──
    if chart_type in ("bar", "grouped_bar", "hbar", "horizontal_bar", "line",
                      "stacked_bar", "box", "boxplot", "violin"):
        series = data.get("series", data.get("datasets", {}))
        fatal += _check_series_dict(series, "series")
        labels = data.get("labels", data.get("x", []))
        is_boxlike = chart_type in ("box", "boxplot", "violin")
        if _nonempty_list(labels) and series:
            if is_boxlike:
                # box/violin: labels are GROUP names — compare to series count,
                # not to values-per-series (each group holds its own array)
                n_labels, n_groups = _len(labels), len(series)
                if n_labels != n_groups:
                    fatal.append(
                        f"labels 有 {n_labels} 个组名但 series 有 {n_groups} 组 — "
                        f"每个箱线/小提琴图恰好对应一个组名，数量对不上多半是 labels 和数据错位了")
            else:
                n_labels, n_first = _len(labels), _len(next(iter(series.values())))
                if n_labels != n_first:
                    fatal.append(
                        f"labels 有 {n_labels} 项但系列值只有 {n_first} 个 — "
                        f"长度不齐会导致图内容被静默截断，请修正 CSV/JSON 对齐。")
        elif not is_boxlike and not _nonempty_list(labels):
            warns.append("未提供 labels：x 轴将使用序号 0..n-1")
        # errors must reference existing series (silent KeyError risk)
        errs = data.get("errors", {})
        if isinstance(errs, dict) and errs:
            unknown = [k for k in errs if k not in series]
            if unknown:
                warns.append(f"errors 引用了数据里不存在的系列: {unknown[:3]}")
            for n, v in errs.items():
                if n in series and _nonempty_list(v) and _len(v) != _len(series[n]):
                    warns.append(f"errors['{n}'] 有 {_len(v)} 个值但系列 '{n}' 有 {_len(series[n])} 个 — 数量应一一对应，误差棒可能错位")
        # significance keys must reference existing series
        sig = data.get("significance", {})
        if isinstance(sig, dict) and sig:
            # v4.5 P1-2：键格式为 "系列名:列索引"，须拆分后查系列名（整串比对必然误报）
            unknown = []
            for k in sig:
                head = k.rsplit(":", 1)[0] if ":" in str(k) else str(k)
                if head not in series:
                    unknown.append(k)
            if unknown:
                warns.append(f"significance 引用了数据里不存在的系列: {unknown[:3]}")

    # ── heatmap: matrix ──
    elif chart_type == "heatmap":
        matrix = data.get("matrix", data.get("data", data.get("values")))
        if matrix is None:
            fatal.append("heatmap 需要 'matrix'（二维数值数组）— 数据里没有这个字段")
        elif not isinstance(matrix, (list, tuple)) or len(matrix) == 0:
            fatal.append("heatmap: 'matrix' 为空 — 请提供二维数组")
        elif not all(isinstance(r, (list, tuple)) and _len(r) == _len(matrix[0]) for r in matrix):
            fatal.append("heatmap: 'matrix' 各行长度不一致（参差行）— 每行单元格数必须相同")
        else:
            flat = [float(x) for r in matrix for x in r if _is_number(x)]
            n_bad = sum(1 for r in matrix for x in r if not _is_number(x))
            if n_bad:
                warns.append(f"heatmap: {n_bad} 个非数值单元格将渲染为空白/NaN")
            if flat and max(flat) == min(flat):
                warns.append(f"heatmap: 全部 {len(flat)} 个单元格值相同（{flat[0]:g}）— 热图将是单一颜色，请核对数据")

    # ── scatter: x / y (+ groups) ──
    elif chart_type == "scatter":
        x = data.get("x", data.get("xs", []))
        y = data.get("y", data.get("ys", []))
        if not _nonempty_list(x):
            fatal.append("scatter 需要 'x'（数值数组）— 字段缺失或为空")
        if not _nonempty_list(y):
            fatal.append("scatter 需要 'y'（数值数组）— 字段缺失或为空")
        if not fatal:
            if _len(x) != _len(y):
                fatal.append(f"scatter: 'x' 有 {_len(x)} 个值但 'y' 有 {_len(y)} 个 — 每个点需要一对 x/y，长度必须一致")
            _warn_non_numeric("x", x)
            _warn_non_numeric("y", y)
            if len(x) >= 2 and _is_number(x[0]) and _is_number(x[-1]) and max(float(v) for v in x if _is_number(v)) == min(float(v) for v in x if _is_number(v)):
                warns.append("scatter: 所有 x 值相同 — 点将垂直堆叠，趋势线（若显示）无意义")
        groups = data.get("groups", data.get("colors"))
        if groups is not None and not _nonempty_list(groups):
            fatal.append("scatter: 'groups' 存在但为空")
        elif groups is not None and _len(groups) != _len(x) and _len(groups) > 0:
            warns.append(f"scatter: 'groups' 有 {_len(groups)} 项但共 {_len(x)} 个点 — 分组可能错位")

    # ── forest: estimates + ci_low + ci_high ──
    elif chart_type == "forest":
        estimates = data.get("estimates", data.get("values", []))
        ci_low = data.get("ci_low", data.get("lower", []))
        ci_high = data.get("ci_high", data.get("upper", []))
        if not _nonempty_list(estimates):
            fatal.append("forest 需要 'estimates'（各研究效应值）— 字段缺失或为空")
        if not _nonempty_list(ci_low):
            fatal.append("forest 需要 'ci_low'（各研究 CI 下限）— 字段缺失或为空")
        if not _nonempty_list(ci_high):
            fatal.append("forest 需要 'ci_high'（各研究 CI 上限）— 字段缺失或为空")
        if not fatal:
            if not (_len(estimates) == _len(ci_low) == _len(ci_high)):
                fatal.append(f"forest: estimates/ci_low/ci_high 长度不一致（{_len(estimates)}/{_len(ci_low)}/{_len(ci_high)}）— 每个研究都要三个值")
            _warn_non_numeric("estimates", estimates)
            for i in range(min(_len(estimates), _len(ci_low), _len(ci_high))):
                if _is_number(estimates[i]) and _is_number(ci_low[i]) and _is_number(ci_high[i]):
                    if not (float(ci_low[i]) <= float(estimates[i]) <= float(ci_high[i])):
                        warns.append(f"forest: 研究 {i} 的效应值 {estimates[i]:g} 落在 CI [{ci_low[i]:g}, {ci_high[i]:g}] 之外 — 请核对数据")
        labels = data.get("labels", data.get("studies", []))
        if _nonempty_list(labels) and _len(labels) != _len(estimates):
            warns.append(f"forest: {_len(labels)} 个研究标签但 {_len(estimates)} 个效应值 — 标签可能错位")
        weights = data.get("weights")
        if _nonempty_list(weights) and _len(weights) != _len(estimates):
            warns.append(f"forest: {_len(weights)} 个权重但 {_len(estimates)} 个效应值 — 气泡大小可能错配")
        events = data.get("events")
        if isinstance(events, list) and events and _len(events) != _len(estimates):
            warns.append(f"forest: {_len(events)} 行事件数据但 {_len(estimates)} 个效应值 — events/total 可能错位")

    # ── KM/RMST: groups (list of [t, s] pairs) OR time + survival ──
    elif chart_type in ("km", "survival", "rmst"):
        _pfx = "rmst" if chart_type == "rmst" else "km"
        groups = data.get("groups", data.get("series", {}))
        has_time = _nonempty_list(data.get("time", []))
        if isinstance(groups, dict) and groups and all(isinstance(v, (list, tuple)) and v and all(isinstance(p, (list, tuple)) and _len(p) >= 2 for p in v) for v in groups.values()):
            for gname, pairs in groups.items():
                times = [p[0] for p in pairs if _is_number(p[0])]
                if len(times) >= 2 and any(times[i] > times[i + 1] for i in range(len(times) - 1)):
                    warns.append(f"{_pfx}: 组 '{gname}' 时间点未升序 — 拟合前已自动排序，曲线不受影响")
        elif has_time and isinstance(data.get("survival"), dict):
            surv = data["survival"]
            fatal += _check_series_dict(surv, "survival", req_nonempty=False)
            for gname, s in surv.items():
                if _nonempty_list(s) and _len(s) != _len(data["time"]):
                    fatal.append(f"km: survival['{gname}'] 有 {_len(s)} 个值但 'time' 有 {_len(data['time'])} 个 — 长度必须一致")
        elif isinstance(groups, dict) and groups:
            # v2.6 A1: dict 有内容但值不是 [t, e] 成对列表。最常见是 CSV/Excel 长表
            # （time/event/group 各一列、一行一名患者）被通用转换装进 series——
            # 此前静默通过并渲染出无意义单曲线，必须拦截并给转换指引。
            _long_keys = {"time", "event", "status", "group", "groups"}
            _keys_l = {str(k).strip().lower() for k in groups}
            if _keys_l & _long_keys:
                fatal.append(
                    f"{_pfx}: 检测到长表结构（time/event/group 各占一列，一行记录一名患者）—"
                    "这种表无法直接画生存曲线。请转成 JSON："
                    '{"groups": {"组名": [[时间, 事件(1=事件/0=删失), ...]], ...}}，'
                    "每组一个数组；格式详见 references/data-formats.md")
            else:
                fatal.append(
                    f"{_pfx}: groups 的每个值必须是 [时间, 事件(1/0)] 成对列表，当前是普通数值数组 —"
                    '请改为 {"组名": [[12, 1], [24, 0], ...]}，或改用 time+survival 两个数组')
        elif not isinstance(groups, dict) or not groups:
            fatal.append("km 需要 'groups'（{组名: [[t, s], ...]}）或 'time'+'survival' 数组 — 都没找到")

    # ── ROC: curves OR fpr + tpr ──
    elif chart_type == "roc":
        curves = data.get("curves", [])
        fpr = data.get("fpr", data.get("x", []))
        tpr = data.get("tpr", data.get("y", []))
        if _nonempty_list(curves):
            has_scores_mode = data.get("labels") is not None and all(
                isinstance(c, dict) and _nonempty_list(c.get("scores")) for c in curves)
            for i, c in enumerate(curves):
                if not isinstance(c, dict) or not (_nonempty_list(c.get("fpr")) and _nonempty_list(c.get("tpr"))):
                    if has_scores_mode:
                        continue  # --compare 模式：原始分数曲线（labels+scores），无需 fpr/tpr
                    fatal.append(f"roc: curves[{i}] 必须有 'fpr' 和 'tpr' 数组（--compare 模式可用 labels+scores）")
                elif _len(c["fpr"]) != _len(c["tpr"]):
                    fatal.append(f"roc: curves[{i}] fpr/tpr 长度不一致（{_len(c['fpr'])}/{_len(c['tpr'])}）")
                else:
                    f = [float(v) for v in c["fpr"] if _is_number(v)]
                    if len(f) >= 2 and any(f[i] > f[i + 1] + 1e-9 for i in range(len(f) - 1)):
                        warns.append(f"roc: curves[{i}] fpr 非单调 — 请按阈值排序曲线")
                c_auc = c.get("auc")
                if isinstance(c_auc, (int, float)) and not (0.0 <= float(c_auc) <= 1.0):
                    warns.append(f"roc: curves[{i}] auc={c_auc:g} 超出 [0, 1] — 请核对该值")
        elif _nonempty_list(fpr) and _nonempty_list(tpr):
            if _len(fpr) != _len(tpr):
                fatal.append(f"roc: fpr 有 {_len(fpr)} 个但 tpr 有 {_len(tpr)} 个 — 长度必须一致")
            _warn_non_numeric("fpr", fpr)
            _warn_non_numeric("tpr", tpr)
        else:
            fatal.append("roc 需要 'curves'（{fpr,tpr} 列表）或 'fpr'+'tpr' 数组 — 都没找到")
        auc = data.get("auc")
        if isinstance(auc, (int, float)) and not (0.0 <= float(auc) <= 1.0):
            warns.append(f"roc: auc={auc:g} 超出 [0, 1] — 请核对该值")

    # ── dual_axis: labels + left + right ──
    elif chart_type == "dual_axis":
        labels = data.get("labels", data.get("x", []))
        left = data.get("left", data.get("y1", {}))
        right = data.get("right", data.get("y2", {}))
        fatal += _check_series_dict(left, "left/y1")
        fatal += _check_series_dict(right, "right/y2")
        if not fatal and _nonempty_list(labels) and left and right:
            n_first = _len(next(iter(left.values())))
            if _len(labels) != n_first:
                fatal.append(f"dual_axis: labels 有 {_len(labels)} 项但 left/right 系列有 {n_first} 个 — 长度必须一致")

    # ── slope: items 两时点 ──
    elif chart_type == "slope":
        items = data.get("items")
        if not isinstance(items, dict) or len(items) < 2:
            fatal.append("slope: 需要 'items'（至少 2 项，每项 [左值, 右值]）")
        else:
            for n, v in items.items():
                if not (isinstance(v, (list, tuple)) and len(v) == 2
                        and all(isinstance(x, (int, float)) and not isinstance(x, bool)
                                for x in v)):
                    fatal.append(f"slope: items['{n}'] 必须是恰好 2 个数值 [左值, 右值]")

    # ── volcano: 组学差异表达 ──
    elif chart_type == "volcano":
        l2 = data.get("log2fc")
        pv = data.get("pvalue")
        if not (isinstance(l2, list) and isinstance(pv, list)) or not l2 or len(l2) != len(pv):
            fatal.append("volcano: 需要 'log2fc' 与 'pvalue' 两个等长数值数组")
        else:
            if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in l2 + pv):
                fatal.append("volcano: log2fc/pvalue 必须全为数值")
            else:
                bad_p = [p for p in pv if not (0 < p <= 1)]
                if bad_p:
                    fatal.append(f"volcano: pvalue 必须在 (0, 1]（发现 {len(bad_p)} 个越界值，"
                                 "p=0 请用最小可表示值如 1e-300）")
        names = data.get("names")
        if names is not None and (not isinstance(names, list) or len(names) != len(l2 or [])):
            fatal.append("volcano: 'names' 长度必须与 log2fc 一致")

    # ── upset: 多集合交集（≥5 集合推荐；venn 2~4 的标准后继）──
    elif chart_type == "upset":
        s = data.get("sets")
        if not isinstance(s, dict) or len(s) < 2:
            fatal.append("upset: 需要 'sets'（≥2 个集合，值为元素列表；≥5 集合时最见长，"
                         "2~4 集合建议 venn）")
        else:
            if len(s) > 30:
                fatal.append(f"upset: 集合数 {len(s)} 超上限 30"
                             "（点阵行数过多不可读，请按意义分组或拆分）")
            for nm, els in s.items():
                if not isinstance(els, (list, tuple)) or not els:
                    fatal.append(f"upset: sets['{nm}'] 必须是非空元素列表")
                else:
                    bad = [e for e in els
                           if isinstance(e, bool) or not isinstance(e, (str, int, float))]
                    if bad:
                        fatal.append(f"upset: sets['{nm}'] 含不支持的元素类型 "
                                     f"（仅字符串/数值标量，发现 {len(bad)} 个）")
        tn = data.get("top_n")
        if tn is not None and (isinstance(tn, bool) or not isinstance(tn, int)
                               or not 1 <= tn <= 50):
            fatal.append("upset: top_n 取值 1~50")
        ms = data.get("min_size")
        if ms is not None and (isinstance(ms, bool) or not isinstance(ms, int) or ms < 1):
            fatal.append("upset: min_size ≥ 1")
        sm = data.get("sort")
        if sm is not None and str(sm).strip().lower() not in ("size", "degree"):
            fatal.append("upset: sort 只支持 'size' 或 'degree'")

    # ── waterfall: 肿瘤缓解瀑布（校验逻辑在 af_draw.validate_waterfall，v4.8）──
    elif chart_type == "waterfall":
        fatal.extend(validate_waterfall(data))

    # ── swimmer: 临床试验游泳图（校验逻辑在 af_draw.validate_swimmer，v4.10）──
    elif chart_type == "swimmer":
        fatal.extend(validate_swimmer(data))

    # ── ridgeline: 山脊图（校验逻辑在 af_draw.validate_ridgeline，v5.0）──
    elif chart_type == "ridgeline":
        fatal.extend(validate_ridgeline(data))

    # ── dumbbell: 哑铃图（校验逻辑在 af_draw.validate_dumbbell，v5.1）──
    elif chart_type == "dumbbell":
        fatal.extend(validate_dumbbell(data))

    # ── raincloud: 分布三合一（schema 同 violin；校验在 af_draw）──
    elif chart_type == "raincloud":
        fatal.extend(validate_raincloud(data))

    # ── calibration/dca: 临床预测模型线（校验逻辑在 af_draw，v5.2）──
    elif chart_type in ("calibration", "dca", "nomogram", "rcs", "subgroup"):
        fatal.extend({"calibration": validate_calibration, "dca": validate_dca,
                      "nomogram": validate_nomogram, "rcs": validate_rcs,
                      "subgroup": validate_subgroup}[chart_type](data))

    # ── composite: panels ──
    elif chart_type == "composite":
        panels = data.get("panels", [])
        if not isinstance(panels, list) or not panels:
            fatal.append("composite 需要 'panels'（非空面板对象列表）")
        else:
            bad = [i for i, p in enumerate(panels) if not isinstance(p, dict) or not p.get("type")]
            if bad:
                fatal.append(f"composite: 面板 {bad[:5]} 缺少 'type' 字段 — 每个面板都要有 type（如 'bar'）")
            # v4.3 span 跨行跨列：合法性 + 占位重叠检测（GridSpec 重叠静默，必须前置拦）
            _nr, _nc = (int(x) for x in data.get("layout", [1, 2]))
            _hero_valid = hero_panel_mode(data, panels)[0]  # v7.8.0：hero 接管布局，跳过 pos/span 占位检测
            occ = {}
            for i, p in enumerate(panels):
                if _hero_valid or not isinstance(p, dict):
                    continue
                # v4.5 R2-4：未知面板类型前置拒绝（原静默画 "Unknown type" 文本框）
                # v4.7：upset 为自管类型（内部 GridSpec 拆轴），不可作面板
                _pt = p.get("type")
                if _pt not in GENERATORS or _pt in ("composite", "diagram", "flow", "upset"):
                    fatal.append(f"composite: 面板 {i} type '{_pt}' 无效"
                                 "（可用：除 composite/diagram/upset 外的全部图型）")
                    continue
                if "pos" not in p:
                    continue  # v4.3 兼容：未显式写 pos 的面板保持旧宽容行为（不参与占位检查）
                pos = p.get("pos")
                if not (isinstance(pos, list) and len(pos) == 2
                        and all(isinstance(x, int) for x in pos)):
                    continue
                r0, c0 = pos
                if not (0 <= r0 < _nr and 0 <= c0 < _nc):
                    fatal.append(f"composite: 面板 {i} pos {pos} 超出 layout {[_nr, _nc]}")
                    continue
                sp = p.get("span", [1, 1]) or [1, 1]
                if not (isinstance(sp, list) and len(sp) == 2
                        and all(isinstance(x, int) and x >= 1 for x in sp)):
                    fatal.append(f"composite: 面板 {i} span 必须是 ≥1 的整数 [行, 列]")
                    continue
                rs = min(sp[0], _nr - r0)
                cs = min(sp[1], _nc - c0)
                for r in range(r0, r0 + rs):
                    for c in range(c0, c0 + cs):
                        if (r, c) in occ:
                            fatal.append(f"composite: 面板 {occ[(r, c)]} 与面板 {i} 在 "
                                         f"({r}, {c}) 占位重叠——span 布局不得交叠")
                            break
                        occ[(r, c)] = i
                    if (r, c) in occ and len(fatal) and "占位重叠" in fatal[-1]:
                        break

    # ── diagram: blocks ──
    elif chart_type == "diagram":
        blocks = data.get("blocks", [])
        if not isinstance(blocks, list) or not blocks:
            fatal.append("diagram 需要 'blocks'（非空块对象列表）")
    elif chart_type == "flow":
        nodes = data.get("nodes", [])
        if not isinstance(nodes, list) or len(nodes) < 2: fatal.append("flow 需要 'nodes'（≥2 个节点对象）")
        if data.get("layout") not in (None, "chain", "layered", "snake"): fatal.append("flow: layout 只支持 chain | layered | snake")
        _cols = data.get("columns")
        if _cols is not None and (not str(_cols).lstrip("-").isdigit() or not 2 <= int(_cols) <= 8): fatal.append(f"flow: columns 需为 [2, 8] 整数，收到 {_cols!r}")  # v8.0.4 validate-first [2,8]（渲染层同锁）

    # ── prisma: PRISMA 2020 flow, counts + arithmetic consistency gates ──
    elif chart_type == "prisma":
        req_ints = ["records_identified", "studies_included"]
        opt_ints = ["duplicates_removed", "records_screened", "records_excluded",
                    "reports_sought", "reports_not_retrieved", "reports_assessed"]
        vals = {}
        for k in req_ints + opt_ints:
            v = data.get(k)
            if v is None:
                continue
            if isinstance(v, bool) or not isinstance(v, int) or v < 0:
                fatal.append(f"prisma '{k}' 必须是非负整数（当前 {v!r}）")
            else:
                vals[k] = v
        for k in req_ints:
            if k not in vals:
                fatal.append(f"prisma 缺少 '{k}'（非负整数）")
        # Derive the pipeline the same way gen_prisma will, so gates hold
        # even for omitted intermediate fields (a review's numbers must ADD UP).
        ident = vals.get("records_identified")
        dup = vals.get("duplicates_removed", 0)
        screened = vals.get("records_screened")
        if screened is None and ident is not None:
            screened = ident - dup
        excluded = vals.get("records_excluded", 0)
        sought = vals.get("reports_sought")
        if sought is None and screened is not None:
            sought = screened - excluded
        not_ret = vals.get("reports_not_retrieved", 0)
        assessed = vals.get("reports_assessed")
        if assessed is None and sought is not None:
            assessed = sought - not_ret
        if ident is not None and vals.get("records_screened") is not None \
                and vals["records_screened"] != ident - dup:
            fatal.append(f"prisma 数字自洽校验失败: records_screened ({vals['records_screened']}) != "
                         f"records_identified - duplicates_removed ({ident - dup})")
        if vals.get("reports_sought") is not None and screened is not None \
                and vals["reports_sought"] != screened - excluded:
            fatal.append(f"prisma 数字自洽校验失败: reports_sought ({vals['reports_sought']}) != "
                         f"records_screened - records_excluded ({screened - excluded})")
        if vals.get("reports_assessed") is not None and sought is not None \
                and vals["reports_assessed"] != sought - not_ret:
            fatal.append(f"prisma 数字自洽校验失败: reports_assessed ({vals['reports_assessed']}) != "
                         f"reports_sought - reports_not_retrieved ({sought - not_ret})")
        _inc_only = vals.get("studies_included")  # v7.9.0 AF22：纳入≤评估守恒独立化（原嵌套分支曾放行 200>169）
        if _inc_only is not None and vals.get("reports_assessed") is not None and _inc_only > vals["reports_assessed"]:
            fatal.append(f"prisma 数字自洽校验失败: studies_included ({_inc_only}) > reports_assessed ({vals['reports_assessed']})——纳入研究数不可能超过全文评估的报告数，请复核流程数字")
        reasons = data.get("exclusion_reasons")
        if reasons is not None:
            if not isinstance(reasons, dict) or not reasons:
                fatal.append("prisma 'exclusion_reasons' 必须是非空对象 {原因: 数量}")
            else:
                bad = {r: n for r, n in reasons.items()
                       if isinstance(n, bool) or not isinstance(n, int) or n < 0}
                if bad:
                    fatal.append(f"prisma exclusion_reasons 的值必须是非负整数，"
                                 f"这些键有问题: {bad}")
                total = sum(n for n in reasons.values()
                            if isinstance(n, int) and not isinstance(n, bool))
                inc = vals.get("studies_included")
                if assessed is not None and inc is not None and total + inc != assessed:
                    fatal.append(f"prisma 数字自洽校验失败: exclusion_reasons 总数 ({total}) + "
                                 f"studies_included ({inc}) != reports_assessed ({assessed}) "
                                 f"— 排除人数+纳入数应等于评估全文数，请复核流程数字")
        lang = data.get("lang")
        if lang is not None and lang not in ("en", "zh"):
            fatal.append("prisma 'lang' 只能是 'en' 或 'zh'")

    if _afcharts is not None and chart_type in _afcharts.EXTRA_GENERATORS:
        f23, w23 = _afcharts.validate_extra(chart_type, data)
        fatal.extend(f23)
        warns.extend(w23)

    return fatal, warns


def legend_audit(ax, chart_type, no_legend, n_series):
    """Detect silently-empty legends: >= 2 series drawn, none labeled.

    n_series comes from the DATA (not artist count — matplotlib's
    get_legend_handles_labels only returns labeled artists, so an all-
    unlabeled multi-series figure reports 0 handles). Types that use
    x-axis labels (box/violin/forest), a colorbar (heatmap), or their
    own legend (dual_axis, composite, diagram) are exempt.
    """
    if no_legend or chart_type in ("box", "boxplot", "violin", "heatmap", "forest",
                                   "composite", "diagram", "dual_axis"):
        return None
    if n_series < 2:
        return None
    handles, labels = ax.get_legend_handles_labels()
    if not any(labels):
        return ("绘制了多个系列但没有一个带 label — 图例将为空；"
                "请在 JSON 里给系列加 name 键（或 CSV 用分组列）以便区分")
    return None


# ── Figure generators ──────────────────────────────────────────────────


if _afcharts is not None:
    GENERATORS.update(_afcharts.EXTRA_GENERATORS)
    DEMO_DATA.update(_afcharts.EXTRA_DEMO_DATA)

_EXC_ZH = {
    "KeyError": "缺少必需字段",
    "BadZipFile": "文件不是有效的压缩/xlsx 格式",
    "JSONDecodeError": "不是合法的 JSON 文本",
    "ValueError": "数值/格式不符合要求",
    "FileNotFoundError": "文件不存在或路径不对",
    "PermissionError": "文件被占用或没有写入权限",
    "UnicodeDecodeError": "文件编码不是 UTF-8/ASCII（请转存为 UTF-8）",
    "TypeError": "数据类型不匹配",
    "IndexError": "数据行/列数量不足",
    # v2.5 扩充：底层库常见异常中文化（评估 R 处方——英文异常名仍保留在括号内可搜索）
    "MemoryError": "数据规模超出可用内存（请减小数据量或分批处理）",
    "OverflowError": "数值溢出（数据量级过大或含极端值）",
    "ZeroDivisionError": "出现除零（数据退化：全为常数或完全相同）",
    "ParserError": "CSV/表格解析失败（行列数不齐或格式错乱）",
    "InvalidFileException": "不是有效的 xlsx 文件（或已损坏）",
    "AttributeError": "数据结构与该图型要求不符",
    "ModuleNotFoundError": "缺少依赖库（按提示 pip install 即可）",
    "IsADirectoryError": "给的是目录路径，需要的是文件",
    "StopIteration": "数据为空或已耗尽（检查文件内容是否为空）",
}


def _zh_exception(e: BaseException) -> str:
    """异常消息中文化：类名映射 + 底层消息保留（便于搜索）。"""
    name = type(e).__name__
    head = _EXC_ZH.get(name, f"{name}")
    return f"{head}（{name}: {e}）"


# ── 投稿精修（v2.5 --annotate / --legend-loc / --legend-outside）──────

_LEGEND_LOCS = {"best", "upper right", "upper left", "lower left", "lower right",
                "right", "center left", "center right", "lower center",
                "upper center", "center"}


def _parse_annotations(items):
    """解析 --annotate "x,y:文字" 列表 → [(x, y, 文字, 原串)]；语法错误即报 ValueError。"""
    out = []
    for raw in items or []:
        s = str(raw)
        if ":" not in s:
            raise ValueError(f'--annotate 语法为 "x,y:文字"（缺少冒号）：{raw}')
        coord, text = s.split(":", 1)
        parts = coord.split(",")
        if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
            raise ValueError(f'--annotate 坐标需为 "x,y"（数字或类别刻度标签）：{raw}')
        text = text.strip()
        if not text:
            raise ValueError(f"--annotate 注释文字不能为空：{raw}")
        out.append((parts[0].strip(), parts[1].strip(), text, s))
    return out


def _resolve_coord(axes, value, which):
    """注释坐标解析：数字直接用；非数字在类别轴刻度标签里查（返回刻度位置）。失败 None。"""
    s = str(value).strip()
    try:
        return float(s)
    except ValueError:
        pass
    if which == "x":
        labels, ticks = axes.get_xticklabels(), axes.get_xticks()
    else:
        labels, ticks = axes.get_yticklabels(), axes.get_yticks()
    for i, t in enumerate(labels):
        if t.get_text().strip() == s:
            try:
                return float(ticks[i])
            except (TypeError, ValueError, IndexError):
                return None
    return None


def _apply_annotations(fig, anns, theme, cjk_fp):
    """在主数据轴上放置箭头注释（审稿改稿刚需）。返回（可能新启用的）cjk_fp。

    - 目标轴选择：取"能解析全部注释坐标且坐标在轴范围内"的轴中数据元素最多者
      （km 双轴自动优先主图而非风险表；组合图自动选中对应面板）
    - 文字初始位：锚点黄金角环绕；复用 _declutter_texts 防重叠（引导线关闭，
      对应关系由 FancyArrowPatch 箭头承担，文字移动后箭头起点跟随重设）
    """
    if not anns:
        return cjk_fp
    import math as _m
    import matplotlib.patches as _mpatches

    def _try_axes(a):
        resolved = []
        # 排序后比较：兼容倒置轴（forest 的 y 轴自上而下，get_ylim() 返回 (大, 小)）
        xa, xb = sorted(a.get_xlim())
        ya, yb = sorted(a.get_ylim())
        for xs, ys, _t, _raw in anns:
            px = _resolve_coord(a, xs, "x")
            py = _resolve_coord(a, ys, "y")
            if px is None or py is None:
                return None
            if not (xa - 0.02 * (xb - xa) <= px <= xb + 0.02 * (xb - xa)):
                return None
            if not (ya - 0.02 * (yb - ya) <= py <= yb + 0.02 * (yb - ya)):
                return None
            resolved.append((px, py))
        return resolved

    def _data_score(a):
        # 曲线/散点/图像是主图特征；纯矩形（km 风险表条块）权重压低
        return (len(a.lines) * 10 + len(a.collections) * 10 + len(a.images) * 10
                + len(a.containers) * 5 + len(a.patches))

    target, resolved = None, None
    for a in sorted(fig.axes, key=_data_score, reverse=True):
        r = _try_axes(a)
        if r is not None:
            target, resolved = a, r
            break
    if target is None:
        a = fig.axes[0] if fig.axes else None
        detail = ""
        if a is not None:
            xl = [t.get_text() for t in a.get_xticklabels() if t.get_text()][:8]
            xa, xb = sorted(a.get_xlim())
            ya, yb = sorted(a.get_ylim())
            detail = (f"（x 轴范围 {xa:.4g}~{xb:.4g}"
                      + (f"，类别刻度: {','.join(xl)}" if xl else "")
                      + f"；y 轴范围 {ya:.4g}~{yb:.4g}）")
        print(f"ERROR: --annotate 无法定位坐标，请确认落在图表数据范围内{detail}",
              file=sys.stderr)
        sys.exit(1)

    # 注释含中文但 cjk_fp 未启用：提前补字体（declutter 中途 draw 不能出现度量失真）
    if cjk_fp is None and any(has_cjk(t) for _x, _y, t, _r in anns):
        try:
            cjk_fp, cjk_name = load_cjk_font(None)
            if cjk_fp:
                plt.rcParams['font.sans-serif'] = [cjk_name, 'DejaVu Sans'] \
                    + plt.rcParams['font.sans-serif']
                plt.rcParams['axes.unicode_minus'] = False
                print(f"自动补启用中文字体: {cjk_name}（--annotate 含中文）", file=sys.stderr)
        except Exception:
            pass

    x0, x1 = target.get_xlim()
    y0, y1 = target.get_ylim()
    span = min(abs(x1 - x0), abs(y1 - y0)) or 1.0
    fs = theme["font_size"]
    texts, arrows, anchors = [], [], []
    for k, ((px, py), (_xs, _ys, txt, _raw)) in enumerate(zip(resolved, anns)):
        ang = 2.399 * k
        ox, oy = span * 0.07 * _m.cos(ang), span * 0.07 * _m.sin(ang)
        t = target.text(px + ox, py + oy, txt, fontsize=fs, ha="center", va="center",
                        color="#333333", zorder=8,
                        fontproperties=cjk_fp if cjk_fp and has_cjk(txt) else None)
        arr = _mpatches.FancyArrowPatch((px + ox, py + oy), (px, py),
                                        arrowstyle="-|>", mutation_scale=fs * 0.9,
                                        color="#555555", linewidth=0.9,
                                        shrinkA=fs * 0.55, shrinkB=1.5, zorder=7)
        target.add_patch(arr)
        texts.append(t)
        arrows.append(arr)
        anchors.append((px, py))
    # 复用散点标签防重叠（引导线阈值放大→不画，箭头已承担对应关系）
    if _afcharts is not None and len(texts) >= 2:
        _afcharts._declutter_texts(target, texts, anchors, leader_min_frac=10.0)
    for arr, t, (ax_, ay_) in zip(arrows, texts, anchors):
        tx, ty = t.get_position()
        arr.set_positions((tx, ty), (ax_, ay_))
    return cjk_fp


def _apply_legend_control(fig, loc=None, outside=False, theme=None, cjk_fp=None):
    """--legend-loc / --legend-outside：重定位既有图例（原位重建，保留标题/列数）。

    - ≥2 个轴带图例 + outside：合并为全图共享图例（右侧，同名图例项去重）
    - 单图例：outside 移到轴右侧；否则按 loc 九宫格重摆
    """
    if not loc and not outside:
        return
    entries = []
    for a in fig.axes:
        hs, ls = a.get_legend_handles_labels()
        leg = a.get_legend()
        title = leg.get_title().get_text() if leg is not None else ""
        ncols = getattr(leg, "_ncols", None) or getattr(leg, "_ncol", None) or 1
        if leg is not None:
            leg.remove()
        if hs:
            entries.append((a, hs, ls, title, int(ncols)))
    if not entries:
        print("WARNING: 图中本无图例（--legend-loc/--legend-outside 未生效）",
              file=sys.stderr)
        return
    fs = (theme or {}).get("font_size", 10) - 1
    if outside and len(entries) >= 2:
        seen, hs_all, ls_all = set(), [], []
        for _a, hs, ls, _t, _n in entries:
            for h, l in zip(hs, ls):
                if l not in seen:
                    seen.add(l)
                    hs_all.append(h)
                    ls_all.append(l)
        fig.legend(hs_all, ls_all, loc="center left", bbox_to_anchor=(1.0, 0.5),
                   framealpha=0.9, fontsize=fs, prop=cjk_fp if cjk_fp else None)
        print(f"已合并 {len(entries)} 个面板的图例为全图共享图例（右侧）", file=sys.stderr)
        return
    for a, hs, ls, title, ncols in entries:
        kw = {}
        if title:
            kw["title"] = title
        if ncols > 1:
            kw["ncols"] = ncols
        if outside:
            a.legend(hs, ls, loc="center left", bbox_to_anchor=(1.02, 0.5),
                     framealpha=0.9, fontsize=fs, prop=cjk_fp if cjk_fp else None, **kw)
        else:
            a.legend(hs, ls, loc=loc, framealpha=0.9, fontsize=fs,
                     prop=cjk_fp if cjk_fp else None, **kw)


# ── Batch（v2.3 --batch）───────────────────────────────────────────────

def _run_batch_items(items, manifest_path):
    """逐项独立进程渲染批量/流水线条目，完成后写汇总报告（--batch 与 --pipeline 共用）。"""
    results = []
    for i, item in enumerate(items):
        if not isinstance(item, dict) or not all(k in item for k in ("type", "data", "out")):
            results.append({"index": i, "ok": False, "error": "缺少 type/data/out 字段"})
            print(f"[batch {i+1}/{len(items)}] FAIL: 缺少 type/data/out 字段", file=sys.stderr)
            continue
        argv = [sys.executable, os.path.abspath(__file__),
                "-t", str(item["type"]), "-d", str(item["data"]), "-o", str(item["out"])]
        for key, flag in (("title", "--title"), ("xlabel", "--xlabel"), ("ylabel", "--ylabel"),
                          ("theme", "--theme"), ("journal", "--journal"), ("column", "--column"),
                          ("stats", "--stats"), ("sheet", "--sheet"), ("risk_times", "--risk-times"),
                          ("legend_loc", "--legend-loc")):
            if item.get(key):
                argv.extend([flag, str(item[key])])
        for key, flag in (("alt", "--alt"), ("caption", "--caption"), ("egger", "--egger"),
                          ("compare", "--compare"), ("cjk", "--cjk"), ("hatch", "--hatch"),
                          ("show_values", "--show-values"), ("no_legend", "--no-legend"),
                          ("no_risk_table", "--no-risk-table"), ("area", "--area"),
                          ("legend_outside", "--legend-outside")):
            if item.get(key):
                argv.append(flag)
        for ann in (item.get("annotate") or []):
            argv.extend(["--annotate", str(ann)])
        for key, flag in (("dpi", "--dpi"), ("width", "--width"), ("height", "--height"),
                          ("timeout", "--timeout"), ("downsample", "--downsample")):
            if item.get(key):
                argv.extend([flag, str(item[key])])
        # v4.7 D-03：format/multi_format 接受列表（YAML 自然写法）——
        # 多元素列表→ --multi-format a,b；单元素列表/标量→ --format 单值
        _mf_raw = item.get("multi_format")
        _fv_raw = item.get("format")
        if isinstance(_mf_raw, (list, tuple)) or isinstance(_fv_raw, (list, tuple)):
            _lst = list(_mf_raw) if isinstance(_mf_raw, (list, tuple)) \
                else list(_fv_raw)
            _lst = [str(x).strip() for x in _lst if str(x).strip()]
            if len(_lst) > 1:
                argv.extend(["--multi-format", ",".join(_lst)])
            elif _lst:
                argv.extend(["--format", _lst[0]])
        else:
            if _mf_raw:
                argv.extend(["--multi-format", str(_mf_raw)])
            elif _fv_raw:
                argv.extend(["--format", str(_fv_raw)])
        try:
            proc = subprocess.run(argv, capture_output=True, text=True, timeout=300)
            out_path = str(item["out"])
            _cands = [out_path, out_path + "." + str(item.get("format", "png"))]
            for _f in str(item.get("multi_format") or "").replace("，", ",").split(","):
                _f = _f.strip().lower()
                if _f:
                    _cands.append(out_path + "." + _f)
            # v4.7 D-03：列表形式的多格式产物计入成功判定
            for _k in ("multi_format", "format"):
                _v = item.get(_k)
                if isinstance(_v, (list, tuple)):
                    _cands.extend(out_path + "." + str(x).strip().lower()
                                  for x in _v if str(x).strip())
            ok = proc.returncode == 0 and any(os.path.exists(c) for c in _cands)
            tail = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""
        except subprocess.TimeoutExpired:
            ok, tail = False, "超时（>300s）"
        results.append({"index": i, "out": str(item["out"]), "ok": ok, "stderr_tail": tail})
        print(f"[batch {i+1}/{len(items)}] {'OK' if ok else 'FAIL'}: {item['out']}",
              file=sys.stderr)
    n_ok = sum(1 for r in results if r["ok"])
    report = {"total": len(items), "ok": n_ok, "failed": len(items) - n_ok, "items": results}
    rpt_path = os.path.splitext(str(manifest_path))[0] + ".batch-report.json"
    try:
        with open(rpt_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"batch: {n_ok}/{len(items)} 成功，报告 {rpt_path}", file=sys.stderr)
    except OSError as e:
        print(f"WARNING: 批量报告写出失败：{e}", file=sys.stderr)
    if n_ok < len(items):
        sys.exit(2)


def cmd_pipeline(pipeline_path):
    """--pipeline：YAML/JSON 多图流水线（--batch 升级版，支持 defaults 全局默认）。

    结构（YAML 示例）：
        defaults:
          theme: glm
          dpi: 600
        figures:
          - type: km
            data: survival.json
            out: fig1_km
            title: 总生存曲线
    顶层直接写列表 = 无全局默认的精简写法。相对路径（data/out）相对
    流水线文件所在目录解析；条目键与 --batch 单项一致（另支持 multi_format）。
    """
    ext = os.path.splitext(str(pipeline_path))[1].lower()
    if ext in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            print("ERROR: YAML 流水线需要 PyYAML —— 先运行 pip install pyyaml；"
                  "或改用 JSON 流水线 / --batch（无额外依赖）", file=sys.stderr)
            sys.exit(1)
        try:
            with open(pipeline_path, encoding="utf-8") as f:
                spec = yaml.safe_load(f)
        except Exception as e:
            print(f"ERROR: 流水线 YAML 解析失败：{e}", file=sys.stderr)
            sys.exit(1)
    elif ext == ".json":
        try:
            with open(pipeline_path, encoding="utf-8") as f:
                spec = json.load(f)
        except Exception as e:
            print(f"ERROR: 流水线 JSON 读取失败：{e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("ERROR: 流水线文件需为 .yaml / .yml / .json", file=sys.stderr)
        sys.exit(1)
    if isinstance(spec, list):
        defaults, figures = {}, spec
    elif isinstance(spec, dict):
        figures = spec.get("figures")
        defaults = spec.get("defaults") or {}
    else:
        figures, defaults = None, {}
    if not isinstance(figures, list) or not figures:
        print("ERROR: 流水线需为非空列表，或含非空 'figures' 列表的对象"
              "（可选 'defaults' 全局默认）", file=sys.stderr)
        sys.exit(1)
    if not isinstance(defaults, dict):
        print("ERROR: 'defaults' 必须是对象（键值对形式的全局默认）", file=sys.stderr)
        sys.exit(1)
    base_dir = os.path.dirname(os.path.abspath(pipeline_path))
    items = []
    for fig in figures:
        if not isinstance(fig, dict):
            print(f"ERROR: figures 里的条目必须是对象，得到 {type(fig).__name__}",
                  file=sys.stderr)
            sys.exit(1)
        merged = dict(defaults)
        merged.update(fig)
        for k in ("data", "out"):
            v = merged.get(k)
            if isinstance(v, str) and v and not os.path.isabs(v):
                merged[k] = os.path.normpath(os.path.join(base_dir, v))
        items.append(merged)
    print(f"pipeline: {len(items)} 张图（defaults: "
          f"{', '.join(sorted(defaults.keys())) if defaults else '无'}）", file=sys.stderr)
    _run_batch_items(items, pipeline_path)


def cmd_batch(manifest_path):
    """--batch：JSON 清单批量出图（逐项独立进程，互不干扰），完成后写汇总报告。"""
    try:
        with open(manifest_path, encoding="utf-8") as f:
            items = json.load(f)
    except Exception as e:
        print(f"ERROR: 批量清单读取失败：{e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(items, list) or not items:
        print("ERROR: 批量清单需为非空 JSON 数组（每项含 type/data/out）", file=sys.stderr)
        sys.exit(1)
    _run_batch_items(items, manifest_path)


# ── Main ───────────────────────────────────────────────────────────────

def _run_cox_forest(args):
    """B1(v2.7)：--stats cox —— 原始逐例生存数据自动拟合多因素 Cox 比例风险模型，
    以 HR[95%CI] 森林图输出（无效线 1.0 自动）。数据格式：
    JSON: {"time":[...], "event":[...], 其余顶层键=协变量}，或
          {"time":[...], "event":[...], "covariates": {"名": [...]}}
    CSV : 表头含时间/事件列（--cox-time/--cox-event 改名），其余数值列=协变量；
          二分类文本列自动 0/1 编码（stderr 注明参照组）；>2 类目请先数值化。"""
    import csv as _csv

    path = args.data
    if not path or not os.path.exists(path):
        print(f"ERROR: 找不到数据文件：{path}", file=sys.stderr)
        sys.exit(1)
    ext = os.path.splitext(path)[1].lower()
    time_col = args.cox_time
    event_col = args.cox_event

    def _is_num_list(seq):
        try:
            return all(np.isfinite(float(v)) for v in seq)
        except (TypeError, ValueError):
            return False

    def _fatal(msg):
        print(f"ERROR: {msg}", file=sys.stderr)
        sys.exit(1)

    cov_raw = {}
    if ext == ".json":
        try:
            with open(path, encoding="utf-8-sig") as fh:
                d = json.load(fh)
        except Exception as exc:
            _fatal(f"JSON 解析失败：{exc}")
        if not isinstance(d, dict) or "time" not in d or "event" not in d:
            _fatal("Cox 数据 JSON 必须包含 time 与 event 两个数组（逐例一行）")
        if isinstance(d.get("covariates"), dict):
            cov_raw = {k: v for k, v in d["covariates"].items()}
        else:
            cov_raw = {k: v for k, v in d.items()
                       if k not in ("time", "event") and isinstance(v, list)}
    elif ext in (".csv", ".tsv", ".txt"):
        delim = "\t" if ext == ".tsv" else ","
        try:
            with open(path, encoding="utf-8-sig", newline="") as fh:
                rows = list(_csv.DictReader(fh, delimiter=delim))
        except Exception as exc:
            _fatal(f"CSV 解析失败：{exc}")
        if not rows:
            _fatal("CSV 为空")
        headers = list(rows[0].keys())
        for need in (time_col, event_col):
            if need not in headers:
                _fatal(f"CSV 缺少必需列「{need}」（现有列：{ '、'.join(headers) }）。"
                       f"可用 --cox-time/--cox-event 指定列名")
        def colvals(name):
            return [r[name] for r in rows]
        times_raw = colvals(time_col)
        events_raw = colvals(event_col)
        for name in headers:
            if name in (time_col, event_col):
                continue
            vals = [v for v in colvals(name) if str(v).strip() != ""]
            if _is_num_list(vals):
                cov_raw[name] = [float(v) for v in colvals(name)]
            else:
                uniq = sorted({str(v).strip() for v in vals})
                if len(uniq) == 2:
                    mapping = {uniq[0]: 0, uniq[1]: 1}
                    cov_raw[name] = [mapping.get(str(v).strip()) for v in colvals(name)]
                    if any(v is None for v in cov_raw[name]):
                        _fatal(f"列「{name}」存在无法识别的取值（允许：{'、'.join(uniq)}）")
                    print(f"Cox 编码：{name} → {uniq[0]}=0（参照）、{uniq[1]}=1"
                          f"（该变量 HR 为「{uniq[1]} 相对 {uniq[0]}」）", file=sys.stderr)
                elif len(uniq) > 2:
                    _fatal(f"列「{name}」有 {len(uniq)} 个类目（{ '、'.join(uniq[:4]) }…）——"
                           "多分类请先拆为哑变量（数值列）再提交")
    else:
        _fatal("--stats cox 支持 .json / .csv / .tsv 原始逐例数据；"
               "效应量森林图（已有 HR/OR 点估计）不要加 --stats cox")

    # 统一转数值
    if ext == ".json":
        if not _is_num_list(d["time"]) or not _is_num_list(d["event"]):
            _fatal("time/event 必须是数值数组（event 用 0/1）")
        times = [float(v) for v in d["time"]]
        events = [float(v) for v in d["event"]]
        for k, v in list(cov_raw.items()):
            if not _is_num_list(v):
                uniq = sorted({str(s) for s in v})
                if len(uniq) == 2:
                    cov_raw[k] = [1 if str(s) == uniq[1] else 0 for s in v]
                    print(f"Cox 编码：{k} → {uniq[0]}=0（参照）、{uniq[1]}=1", file=sys.stderr)
                else:
                    _fatal(f"协变量「{k}」不是数值数组（类目数 {len(uniq)}）——请先数值化")
        times = [float(v) for v in times]
        events = [float(v) for v in events]
        cov_raw = {k: [float(x) for x in v] for k, v in cov_raw.items()}
    else:
        try:
            times = [float(v) for v in times_raw]
            events = [float(v) for v in events_raw]
        except (TypeError, ValueError):
            _fatal("time/event 列存在非数值内容")

    if args.cox_cols:
        order = [c.strip() for c in str(args.cox_cols).split(",") if c.strip()]
        missing = [c for c in order if c not in cov_raw]
        if missing:
            _fatal(f"--cox-cols 指定了不存在的列：{'、'.join(missing)}")
        cov_raw = {c: cov_raw[c] for c in order}
    if not cov_raw:
        _fatal("没有可用的协变量列——Cox 多因素回归至少需要 1 个数值协变量")

    if _afstats is None:
        _fatal("统计模块 af_v23_stats 加载失败，无法执行 Cox 回归")
    names = list(cov_raw.keys())
    try:
        fit = _afstats.coxph_fit(times, events,
                                 np.column_stack([cov_raw[n] for n in names]),
                                 names=names)
    except ValueError as exc:
        _fatal(str(exc))
    ph = _afstats.cox_ph_test(fit)

    print(f"Cox 多因素回归（Efron 法）：n={fit['n']}，事件数={fit['n_events']}，"
          f"迭代 {fit['iterations']} 次{'收敛' if fit['converged'] else '未完全收敛'}，"
          f"loglik={fit['loglik']:.3f}", file=sys.stderr)
    print(f"{'协变量':<10}{'beta':>9}{'SE':>9}{'HR':>9}{'95%CI':>19}{'p':>10}{'PH-p':>9}",
          file=sys.stderr)
    for i, name in enumerate(names):
        ci = f"[{fit['hr_low'][i]:.3f},{fit['hr_high'][i]:.3f}]"
        print(f"{name:<10}{fit['beta'][i]:>9.4f}{fit['se'][i]:>9.4f}{fit['hr'][i]:>9.3f}"
              f"{ci:>19}{fit['p'][i]:>10.4f}{ph['p'][i]:>9.4f}", file=sys.stderr)
    low_ph = [n2 for n2, pv in zip(names, ph["p"]) if pv == pv and pv < 0.05]
    if low_ph:
        print(f"⚠ PH 提示：{'、'.join(low_ph)} 的比例风险假设近似检验 p<0.05——"
              "该变量效应可能随时间变化（可考虑分层/时变系数/分段 KM 核对）", file=sys.stderr)

    return {
        "labels": names,
        "estimates": [float(v) for v in fit["hr"]],
        "ci_low": [float(v) for v in fit["hr_low"]],
        "ci_high": [float(v) for v in fit["hr_high"]],
        "measure": "HR",
        "ref_line": 1.0,
        "title_note": f"Cox 多因素回归（n={fit['n']}, 事件={fit['n_events']}）",
    }



def _run_cox_subgroup(args):
    """v5.8：--stats cox × -t subgroup —— 原始逐例生存数据一键亚组分析。
    逐层 Cox HR(95%CI,p)（处理臂 vs 参照臂）+ 似然比 P 交互 + Overall 菱形；
    --cox-cols 可选调整协变量（进入全部模型）。数据格式同 --stats cox：
    JSON {"time":[...],"event":[...],其余=列} 或 CSV（--cox-time/--cox-event 改列名）。
    需 --subgroup-vars 名1,名2（类目列，或 --cut 名@阈值 二分数值列）。
    边界：引擎只做亚组拟合并可视化；亚组变量选择与层定义由研究者决定。"""
    import csv as _csv
    from collections import OrderedDict

    path = args.data
    if not path or not os.path.exists(path):
        print(f"ERROR: 找不到数据文件：{path}", file=sys.stderr)
        sys.exit(1)

    def _fatal(msg):
        print(f"ERROR: {msg}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(path)[1].lower()
    time_col, event_col = args.cox_time, args.cox_event
    cols = OrderedDict()
    if ext == ".json":
        try:
            with open(path, encoding="utf-8-sig") as fh:
                d = json.load(fh)
        except Exception as exc:
            _fatal(f"JSON 解析失败：{exc}")
        if not isinstance(d, dict) or "time" not in d or "event" not in d:
            _fatal("数据 JSON 必须包含 time 与 event 两个数组（逐例一行）")
        cols["time"] = d["time"]
        cols["event"] = d["event"]
        src_cols = d.get("covariates") if isinstance(d.get("covariates"), dict) else \
            {k: v for k, v in d.items() if k not in ("time", "event")}
        cols.update(src_cols or {})
    elif ext in (".csv", ".tsv", ".txt"):
        delim = "\t" if ext == ".tsv" else ","
        try:
            with open(path, encoding="utf-8-sig", newline="") as fh:
                rows = list(_csv.DictReader(fh, delimiter=delim))
        except Exception as exc:
            _fatal(f"CSV 解析失败：{exc}")
        if not rows:
            _fatal("CSV 为空")
        headers = list(rows[0].keys())
        for need in (time_col, event_col):
            if need not in headers:
                _fatal(f"CSV 缺少必需列「{need}」（现有列：{'、'.join(headers)}）。"
                       "可用 --cox-time/--cox-event 指定列名")
        for h in headers:
            cols[h] = [r[h] for r in rows]
    else:
        _fatal("--stats cox（subgroup）支持 .json / .csv / .tsv 原始逐例数据；"
               "已有 est/p 的亚组 JSON 不要加 --stats cox")

    def _as_float(seq):
        try:
            return [float(v) for v in seq]
        except (TypeError, ValueError):
            return None

    try:
        times = [float(v) for v in cols[time_col]]
        events = [float(v) for v in cols[event_col]]
    except (TypeError, ValueError):
        _fatal("time/event 列存在非数值内容")
    if _afstats is None:
        _fatal("统计模块 af_v23_stats 加载失败")
    n = len(times)

    # ── 处理臂：--treatment 或常见名自动探测 ──
    tname = args.treatment
    if not tname:
        for cand in ("trt", "treatment", "arm", "group", "exposure", "处理", "暴露"):
            if cand in cols:
                tname = cand
                print(f"处理臂自动探测：{cand}（可用 --treatment 指定）", file=sys.stderr)
                break
    if not tname:
        _fatal("未找到处理臂列——用 --treatment 列名指定（二分类：试验/对照）")
    if tname not in cols:
        _fatal(f"--treatment 列「{tname}」不存在（现有列：{'、'.join(list(cols)[:8])}…）")
    t_raw = cols[tname]
    t_num = _as_float(t_raw)
    if t_num is not None:
        uniq = sorted(set(t_num))
        if len(uniq) != 2:
            _fatal(f"处理臂「{tname}」须恰好两个取值（现有 {len(uniq)} 个）。"
                   "多臂请先二分（试验 vs 对照），或用类目文本列")
        ref_v, hi_v = uniq[0], uniq[-1]
        ref_s = str(int(ref_v)) if float(ref_v).is_integer() else str(ref_v)
        hi_s = str(int(hi_v)) if float(hi_v).is_integer() else str(hi_v)
        trt_bin = [1.0 if v == hi_v else 0.0 for v in t_num]
    else:
        seen, order = set(), []
        for v in t_raw:
            s = str(v).strip()
            if s not in seen:
                seen.add(s)
                order.append(s)
        if len(order) != 2:
            _fatal(f"处理臂「{tname}」须恰好两个取值（现有 {len(order)} 个）")
        ref_s, hi_s = order[0], order[1]
        trt_bin = [0.0 if str(v).strip() == ref_s else 1.0 for v in t_raw]
    print(f"处理臂：{hi_s}（编码 1）vs {ref_s}（参照 0）", file=sys.stderr)

    # ── 调整协变量 --cox-cols（可选，须数值列）──
    adjust = {}
    if args.cox_cols:
        for c in (x.strip() for x in str(args.cox_cols).split(",") if x.strip()):
            if c in (time_col, event_col, tname):
                continue
            if c not in cols:
                _fatal(f"--cox-cols 指定了不存在的列：{c}")
            fv = _as_float(cols[c])
            if fv is None:
                _fatal(f"调整协变量「{c}」含非数值——请先数值化")
            adjust[c] = fv

    # ── 亚组变量：--cut 名@阈值 二分 + --subgroup-vars 类目列 ──
    cuts = {}
    for spec in (args.cut or []):
        if "@" not in spec:
            _fatal(f"--cut 格式应为 名@阈值（收到：{spec}）")
        cname, thr_s = spec.split("@", 1)
        try:
            thr = float(thr_s)
        except ValueError:
            _fatal(f"--cut 阈值须为数字（收到：{spec}）")
        if cname not in cols:
            _fatal(f"--cut 列「{cname}」不存在")
        fv = _as_float(cols[cname])
        if fv is None:
            _fatal(f"--cut 列「{cname}」含非数值——只能二分数值列")
        lab_lo, lab_hi = (f"＜{thr_s}", f"≥{thr_s}")
        cuts[cname] = ([lab_lo if v < thr else lab_hi for v in fv], lab_lo, lab_hi)
        print(f"--cut：{cname} → {lab_lo}（<{thr_s}）/ {lab_hi}（≥{thr_s}）", file=sys.stderr)

    if not args.subgroup_vars:
        _fatal("一键亚组分析需要 --subgroup-vars 名1,名2（类目列名，逗号分隔；"
               "连续数值列先用 --cut 名@阈值 二分）。例：--subgroup-vars celltype,prior --cut age@60")
    groups_spec = []
    for gname in (x.strip() for x in str(args.subgroup_vars).split(",") if x.strip()):
        if gname in cuts:
            groups_spec.append((gname, cuts[gname][0]))
            continue
        if gname not in cols:
            _fatal(f"--subgroup-vars 列「{gname}」不存在（现有列：{'、'.join(list(cols)[:8])}…）")
        if gname == tname:
            _fatal("处理臂列不能同时作为亚组变量")
        raw = [str(v).strip() for v in cols[gname]]
        fv = _as_float(raw)
        if fv is not None and len(set(fv)) > 8:
            _fatal(f"亚组变量「{gname}」是连续数值（{len(set(fv))} 个不同值）——"
                   f"请先 --cut {gname}@阈值 二分")
        if fv is not None and all(float(v).is_integer() for v in set(fv)):
            raw = [str(int(float(v))) for v in cols[gname]]
        groups_spec.append((gname, raw))
    for cname, (vals, _lo, _hi) in cuts.items():   # --cut 声明即纳入（用户切了就是要用）
        if cname not in {g[0] for g in groups_spec}:
            groups_spec.append((cname, vals))

    try:
        res = _afstats.cox_subgroup_analysis(times, events, trt_bin, groups_spec,
                                             adjust=adjust or None)
    except ValueError as exc:
        _fatal(str(exc))

    def _r2(x):
        return round(float(x), 2)

    out = {
        "est_label": "HR",
        "x_label": f"HR（{hi_s} vs {ref_s}，95% CI）",
        "subgroups": [{"name": g["name"],
                       "p_interaction": round(float(g["p_interaction"]), 3),
                       "levels": [{"name": lv["name"], "n": int(lv["n"]),
                                   "est": _r2(lv["est"]), "ci_low": _r2(lv["ci_low"]),
                                   "ci_high": _r2(lv["ci_high"]),
                                   "p": round(float(lv["p"]), 4)} for lv in g["levels"]]}
                      for g in res["subgroups"]],
        "overall": {"est": _r2(res["overall"]["est"]), "ci_low": _r2(res["overall"]["ci_low"]),
                    "ci_high": _r2(res["overall"]["ci_high"]),
                    "p": round(float(res["overall"]["p"]), 4), "n": int(res["overall"]["n"])},
        "_method": (f"--stats cox 一键亚组拟合（v5.8）：{res['method']}。数据={os.path.basename(path)}，"
                    f"n={n}；引擎只做亚组拟合并可视化，亚组变量选择与层定义由研究者决定"),
    }
    print(f"亚组 Cox（Efron 核）n={n}：总体 HR={out['overall']['est']}"
          f"（{out['overall']['ci_low']}~{out['overall']['ci_high']}）p={out['overall']['p']}",
          file=sys.stderr)
    for g in out["subgroups"]:
        lv = "；".join(f"{l['name']}:{l['est']}({l['ci_low']}~{l['ci_high']},n={l['n']})"
                       for l in g["levels"])
        print(f"  {g['name']}（P 交互={g['p_interaction']}）{lv}", file=sys.stderr)
    print("提示：层定义/变量取舍由研究者决定；亚组结论以交互检验为准，不看层内 p 值。",
          file=sys.stderr)
    return out

def main():
    parser = argparse.ArgumentParser(
        description="academic-figures：一条命令生成投稿级学术图表",
        epilog="场景速查：基线表对比 -t bar --stats auto ｜ KM 生存 -t km（逐例数据自动风险表）"
               "｜ 竞争风险 -t cif（Aalen-Johansen+1−KM 高估对照）｜ RMST -t rmst（τ 截断平均生存+差值推断）"
               "｜ 诊断 ROC -t roc --compare ｜ 预测模型四件套 -t roc/calibration/dca/nomogram"
               "｜ Meta 森林+漏斗+径向 -t forest/funnel/galbraith ｜ 亚组森林 -t subgroup（原始数据一键拟合加 --stats cox）"
               "｜ 组学 -t volcano/-t cluster_heatmap ｜ 多面板 -t composite（share_y 统一尺度）"
               "｜ 偏倚风险 -t rob（robvis 同款交通灯）｜ 投稿包 --pub-ready ｜ 场景卡 references/scenario-cards.md ｜ 对智能体说 references/prompt-cards.md")
    parser.add_argument("--gate", default="basic", choices=["basic", "strict"], help="流程图/示意图渲染闸（v8.0.0）：strict=渲染后跑三层 bbox 断言（节点×边标签×箭头线段），任何非零交集 exit 2 拒绝交付")
    parser.add_argument("--type", "-t", choices=list(GENERATORS.keys()),
                        help="图型（如 bar/box/violin/km/roc/forest/prisma，--demo 可看菜单）")
    parser.add_argument("--data", "-d", help="输入数据文件（.json / .csv / .tsv / .xlsx）；支持 inline 简写 \"A=10,B=8,C=5\"（单系列，等价 labels+series value）")
    parser.add_argument("--sheet", default=None,
                        help="xlsx 的工作表名（默认取活动工作表）")
    parser.add_argument("--out", "-o", help="输出文件路径（.png / .svg / .pdf / .tiff / .eps）")
    parser.add_argument("--title", default="", help="图标题")
    parser.add_argument("--xlabel", default="", help="x 轴标签")
    parser.add_argument("--ylabel", default="", help="y 轴标签")
    parser.add_argument("--theme", default=None,
                        help="配色主题（默认 glm-brand；--list-themes 查看全部）")
    parser.add_argument("--style", default=None, choices=["glm-hatch", "nature-clean", "glm-brand", "sketch"],
                        help="快捷风格：'glm-hatch' = GLM 黄蓝斜线风（theme glm + --hatch）；"
                             "'nature-clean' = 顶刊版式（Okabe-Ito 配色+去顶右框线+无网格+无框图例，v3.3）；"
                             "'glm-brand' = 品牌视觉（信号黄对比强化+无网格+同系深色斜纹，v3.3.1）")
    parser.add_argument("--list-themes", action="store_true",
                        help="列出全部配色主题（含色卡预览）后退出")
    parser.add_argument("--list-flags", nargs="?", const="", default=None, metavar="TYPE", help="查询某图型旗标域（专属+域外[ignored] 预告）；无参数=全图型速览")
    parser.add_argument("--list-types", action="store_true",
                        help="列出全部图型（权威清单，每行一个）后退出")
    parser.add_argument("--theme-swatch", default=None, metavar="THEME",
                        help="渲染某主题的色卡预览图后退出")
    parser.add_argument("--demo", action="store_true",
                        help="交互演示：菜单选图型，用内置示例数据出图")
    parser.add_argument("--wizard", action="store_true",
                        help="选图向导：4 个问题生成完整命令；非交互环境打印决策树")
    parser.add_argument("--explain", default=None, metavar="CHART_TYPE",
                        help="打印某图型的用法说明与限制后退出")
    parser.add_argument("--suggest", action="store_true",
                        help="分析数据文件并推荐可用图型后退出")
    parser.add_argument("--quick", action="store_true",
                        help="一键出图：按数据自动选型并直接渲染（v3.1）")
    parser.add_argument("--cjk", action="store_true", help="启用中文字体（自动探测）")
    parser.add_argument("--cjk-font", default=None, help="指定中文字体文件路径")
    parser.add_argument("--width", type=float, default=None, help="图宽（英寸）")
    parser.add_argument("--height", type=float, default=None, help="图高（英寸）")
    parser.add_argument("--format", "-f", default=None, choices=["png", "svg", "pdf", "tiff", "eps"],
                        help="输出格式（默认按 --out 扩展名自动判断）")
    parser.add_argument("--pub-ready", action="store_true",
                        help="一键投稿包：自动加 --verify + --multi-format pdf,png + 色盲安全主题"
                             " + 复跑交付包（--pub-ready theme,NAME 可指定主题；v3.8，v5.2 合流复跑包）")
    parser.add_argument("--profile", default=None, metavar="FILE",
                        help="分层配置文件（v4.3）：JSON 预设呈现参数（theme/journal/"
                             "column/dpi/subtitle/source 等，白名单见文档），CLI 显式"
                             "参数优先——一次定义，处处复用")
    parser.add_argument("--peak-label", action="store_true",
                        help="自动峰值注记（v4.2）：最大值点标注\"峰值 X（类目）\"——"
                             "纯数据事实（bar/hbar/line 系）")
    parser.add_argument("--summary", action="store_true",
                        help="自动数据摘要副标题（v4.1）：纯计数事实（样本量/组数/"
                             "事件数等，零推断）；--subtitle 显式给出时以其为准")
    parser.add_argument("--subtitle", default=None, help="副标题（主标题下方第二行，小号灰色——标题层级 v4.0；兼容 --title \"主/副\" 斜杠写法）")
    parser.add_argument("--source", default=None, help="来源注（图底部右对齐小字，如\"数据来源：XX 数据库\"——v4.0）")
    parser.add_argument("--order", default=None, metavar="L1,L2,...|auto",
                        help="自定义类别顺序：逗号分隔标签，或 auto=按第一系列值降序"
                             "（box/violin 按各组中位数降序）（v3.9；仅 bar/box/violin/line 系）")
    parser.add_argument("--normalize", default=None, choices=["baseline", "pct100"],
                        help="归一化：baseline=各系列÷第一系列均值（对照=1）；"
                             "pct100=各系列÷自身首点×100（T0=100）（v3.9；仅 bar 系/line）")
    parser.add_argument("--doctor", action="store_true",
                        help="渲染前参数/环境体检报告（组合冲突/数据/依赖/输出目录），"
                             "只报告不改退出码；省略 -o 可只体检不渲染（v3.9）")
    parser.add_argument("--multi-format", default=None, metavar="F1,F2,...",
                        help="一次输出多种格式（逗号分隔 png/svg/pdf/tiff/eps，兼容全角逗号）："
                             "文件名取 --out 去扩展名后逐格式拼接，如 -o fig1 --multi-format tiff,png,pdf "
                             "→ fig1.tiff/fig1.png/fig1.pdf；与 --format 同时给出时以本参数为准")
    parser.add_argument("--dpi", type=int, default=None,
                        help="位图 DPI（默认：线条图 600，照片类 300）")
    parser.add_argument("--legend", action="store_true", default=True, help="显示图例")
    parser.add_argument("--no-legend", action="store_true", help="隐藏图例")
    parser.add_argument("--show-values", action="store_true", help="在图元上标注数值")
    parser.add_argument("--arena", nargs="?", const="auto", default=None, help="基准对比竞技场风格（v7.7 起单系列竖向 bar 默认启用）：per-bar 异质填充+冠军柱高亮+皇冠；负面指标（最高=最差，如错误率/不良事件）用 --arena off 关闭，--arena \"名称\" 按标签钉冠军")
    parser.add_argument("--trend", action="store_true", default=True, help="显示趋势线（散点图）")
    parser.add_argument("--no-trend", action="store_true", help="隐藏趋势线（散点图）")
    parser.add_argument("--cmap", default=None, help="热图配色映射（colormap）"); parser.add_argument("--vmin", type=float, default=None, help="热图色阶下限")
    parser.add_argument("--vmax", type=float, default=None, help="热图色阶上限")
    parser.add_argument("--annot", nargs="?", const="auto", default=None, metavar="on|auto|off", help="热图格内数值标注（v7.9.1：auto=超 30 行/列自动隐藏）；--cell-edge 格线描边（低对比色阶保结构）"); parser.add_argument("--cell-edge", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--discrete", action="store_true", help="热图离散色阶（有序离散标度：阶梯映射+离散色标，v7.9.1）"); parser.add_argument("--palette", default=None, metavar='"#hex,#hex,..."', help="外部配色注入（v7.9.1）：分类图按序替换主题系列色，热图按给定顺序构建连续色阶（浅端对齐低值）；flow 图取首色为主链基色、尾色为终点强调色，自动衍生同族明度阶梯（v8.0.4）")
    parser.add_argument("--horizontal", action="store_true", help="水平柱状图（即 hbar）"); parser.add_argument("--hatch", nargs="?", const="on", default=None, metavar="on|off", help="柱体加斜线填充（打印友好）；--hatch off 显式关闭（含品牌默认斜纹）")
    parser.add_argument("--alternate", action="store_true",
                        help="GLM 风格：单系列柱子交替前两种主题色")
    parser.add_argument("--show-ratio", action="store_true", help="分组柱上标注倍率（如 4.96x）")
    parser.add_argument("--ratio-base", type=int, default=0, help="倍率计算的基准系列序号（默认 0）")
    add_sig_bracket_arg(parser)
    add_sig_auto_arg(parser)
    parser.add_argument("--stats", default=None, choices=["auto", "multi", "cox", "bootstrap"],
                        help="box/violin 自动显著性标注：auto=各组 vs 第一组（Shapiro 定正态→Welch t / Mann-Whitney U）；multi=全两两（正态→ANOVA+Tukey，否则 KW+Dunn+Hochberg）；cox=仅 forest：原始逐例生存数据自动拟合多因素 Cox，输出 HR[95%%CI] 森林图+系数表+PH 检验。括号+星号自动绘制")
    parser.add_argument("--timeout", type=float, default=None,
                        help="渲染看门狗预算（秒）：超时强制中断并给中文建议（exit 5）；0=禁用自适应预算（保留硬保险）；默认自适应 30~1800s")
    parser.add_argument("--debug", action="store_true",
                        help="渲染失败时输出结构化诊断侧车 <output>.debug.json（输入指纹/字段映射/异常分类/修复建议，供程序化排障）；成功渲染不产出")
    parser.add_argument("--retries", type=int, default=1, metavar="N",
                        help="瞬时失败自动重试次数：看门狗超时/内存耗尽自动重跑（每代预算放宽 ×1.5）；确定性错误不重试；0=关闭；默认 1")
    parser.add_argument("--downsample", type=int, default=None, metavar="N",
                        help="cluster_heatmap 行数超过 N 时等距采样到 N 行（确定性采样）")
    parser.add_argument("--size", default=None,
                        choices=["16:9", "4:5", "3:2", "1:1", "5:4", "9:16"],
                        help="画幅比例预设（宽:高）：16:9 演示/PPT、4:5 与 3:2 通用、"
                             "9:16 手机/社交竖版、1:1 方版。宽度仍由期刊预设/主题决定，"
                             "仅按比例推算高度")
    parser.add_argument("--cox-time", default="time",
                        help="--stats cox 时生存时间列名（默认 time）")
    parser.add_argument("--cox-event", default="event",
                        help="--stats cox 时事件列名（默认 event；0=删失 1=事件）")
    parser.add_argument("--subgroup-vars", default=None,
                        help="--stats cox × -t subgroup：亚组变量列（逗号分隔，各 2~8 层；"
                             "连续数值列先用 --cut 二分）")
    parser.add_argument("--treatment", default=None,
                        help="--stats cox：处理臂列名（二分类；默认自动探测 trt/treatment/arm 等）")
    parser.add_argument("--cut", action="append", default=[],
                        help="--stats cox × -t subgroup：数值列二分，格式 名@阈值（可多次）"
                             "——自动按 <阈值/≥阈值 分层")
    parser.add_argument("--rmst-tau", default=None,
                        help="-t rmst：截断时间 τ（时间单位；缺省=最小最大随访之半并显著告知）")
    parser.add_argument("--csv-no-errors", action="store_true",
                        help="关闭 CSV 误差列自动识别（X_se/X_sem/X_sd/X_err 后缀列按普通数据列画）")
    parser.add_argument("--cox-cols", default=None,
                        help="--stats cox 时协变量列（逗号分隔，默认除时间/事件外全部数值列；"
                             "顺序即森林图行序）")
    parser.add_argument("--alt", action="store_true",
                        help="输出旁生成无障碍描述文件（<输出名>.alt.txt）")
    parser.add_argument("--caption", action="store_true",
                        help="输出旁生成中英双语期刊式图注文件（<输出名>.caption.txt）")
    parser.add_argument("--sensitivity", action="store_true",
                        help="forest：留一法敏感性分析（省略单研究后的合并效应画在同一图下方；"
                             "需 se_list 或对称 CI 反推）")
    parser.add_argument("--no-median", dest="no_median", action="store_true",
                        help="km：关闭自动中位生存计算与标注")
    parser.add_argument("--compare", action="store_true",
                        help="roc：配对 DeLong 检验比较 >=2 个模型 AUC（需 labels + 各曲线 scores 原始分数）")
    parser.add_argument("--egger", action="store_true",
                        help="funnel：绘制 Egger 回归线并报告漏斗不对称检验")
    parser.add_argument("--area", action="store_true",
                        help="venn：按区域计数比例绘制（Euler 图），替代默认等圆示意")
    parser.add_argument("--annotate", action="append", default=None, metavar='"X,Y:文字"',
                        help="在数据坐标处加箭头注释，可重复使用；类别轴可用刻度标签"
                             "定位（如 --annotate \"3.2,5.1:p=0.01\" 或 \"对照组:显著上调\"）")
    parser.add_argument("--direct-label", action="store_true",
                        help="线图直接标注系列名于线末端（替代图例框，Nature 风格；v3.4）")
    parser.add_argument("--no-direct-label", dest="direct_label", action="store_false",
                        help="关闭直接标注（glm-brand/nature-clean 主题下 line 默认开启）")
    parser.add_argument("--legend-loc", default=None, metavar="LOC",
                        help="图例位置：best/upper right/upper left/lower left/lower "
                             "right/right/center left/center right/center 等九宫格")
    parser.add_argument("--legend-outside", dest="legend_outside", action="store_true",
                        help="图例移到绘图区外侧；组合图自动合并为全图共享图例（右侧）")
    parser.add_argument("--no-risk-table", dest="no_risk_table", action="store_true",
                        help="km：关闭自动风险表（默认开启，位于主图下方）")
    def _risk_times_arg(v):
        try:
            out = [float(x) for x in str(v).replace("，", ",").split(",") if x.strip()]
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"风险表时间点 '{v}' 无法解析为数字（正确示例：2,6,10）")
        if not out:
            raise argparse.ArgumentTypeError("风险表时间点为空（正确示例：2,6,10）")
        return out
    parser.add_argument("--risk-times", default=None, type=_risk_times_arg,
                        metavar="T1,T2,...",
                        help="km：风险表显示时间点（逗号分隔数字；默认 0~最大随访等分 5 档）")
    parser.add_argument("--batch", default=None, metavar="FIGURES.json",
                        help="批量出图：JSON 清单（每项含 type/data/out，可带 title/theme/stats 等），"
                             "逐项渲染后写 .batch-report.json 汇总")
    parser.add_argument("--pipeline", default=None, metavar="ANALYSIS.yaml",
                        help="多图流水线（--batch 升级版）：YAML 或 JSON 描述一篇论文全部图表——"
                             "defaults 全局默认 + figures 逐图条目（type/data/out 必填，可覆盖默认），"
                             "一条命令批量渲染并写 .batch-report.json；相对路径相对流水线文件解析；"
                             "YAML 需先 pip install pyyaml（JSON 无额外依赖）")
    parser.add_argument("--repro", action="store_true",
                        help="渲染成功后写复跑交付包 <output>.repro/（命令+数据副本+成图副本+audit+README）")
    parser.add_argument("--audit", action="store_true",
                        help="渲染成功后写数字对账侧车 <output>.audit.json（描述统计独立重算，可逐项核对图上的数）")
    parser.add_argument("--verify", action="store_true",
                        help="对 PDF 输出做像素级文字重叠检查；发现重叠则退出码 2")
    parser.add_argument("--journal", default=None, choices=sorted(JOURNAL_PRESETS.keys()),
                        help="期刊预设（nature/lancet/science/cell/nejm/jama/ieee/cma/cn-core）："
                             "栏宽、字号、最小字号、字体；cma/cn-core 自动启用中文字体")
    parser.add_argument("--column", default="double", choices=["single", "double"],
                        help="--journal 的栏宽版式（默认 double 双栏）")

    args = parser.parse_args()

    # ── v4.3 --profile 分层配置文件（呈现参数预设；CLI 显式参数优先）──
    if getattr(args, "profile", None):
        _PALLOW = {"theme", "style", "journal", "column", "dpi", "width", "height",
                   "title", "subtitle", "source", "xlabel", "ylabel", "cjk", "verify",
                   "legend_loc", "legend_outside", "multi_format", "peak_label",
                   "summary", "alt", "caption", "format"}
        try:
            _prof = json.load(open(args.profile, encoding="utf-8"))
        except Exception as _e:
            print(f"ERROR: --profile 读取失败: {_e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(_prof, dict):
            print("ERROR: --profile 文件必须是 JSON 对象", file=sys.stderr)
            sys.exit(1)
        _applied = []
        for _k, _v in _prof.items():
            if _k not in _PALLOW:
                print(f"WARNING: --profile 忽略未知键 {_k}（白名单见文档）", file=sys.stderr)
                continue
            if getattr(args, _k, None) in (None, False):
                setattr(args, _k, _v)
                _applied.append(f"{_k}={_v}")
        if _applied:
            print("[profile] 已应用 " + str(len(_applied)) + " 项默认（"
                  + "；".join(_applied[:8]) + ("…" if len(_applied) > 8 else "")
                  + "）；CLI 显式参数优先", file=sys.stderr)

    if getattr(args, "multi_format", None):
        _req_fmts = []
        for _f in str(args.multi_format).replace("，", ",").split(","):
            _f = _f.strip().lower()
            if not _f:
                continue
            if _f not in ("png", "svg", "pdf", "tiff", "eps"):
                print(f"ERROR: --multi-format 不支持 '{_f}'。可用: png, svg, pdf, tiff, eps",
                      file=sys.stderr)
                sys.exit(1)
            if _f not in _req_fmts:
                _req_fmts.append(_f)
        if not _req_fmts:
            print("ERROR: --multi-format 为空。示例：--multi-format tiff,png,pdf", file=sys.stderr)
            sys.exit(1)
        args.multi_format = _req_fmts
        if args.format:
            print("WARNING: --format 与 --multi-format 同时给出，按 --multi-format 输出",
                  file=sys.stderr)

    if args.batch and args.pipeline:
        print("ERROR: --batch 与 --pipeline 只能二选一（--pipeline 是升级版，支持 YAML 与全局默认）",
              file=sys.stderr)
        sys.exit(1)
    if args.pipeline:
        cmd_pipeline(args.pipeline)
        sys.exit(0)
    if args.batch:
        cmd_batch(args.batch)
        sys.exit(0)

    if args.list_themes:
        cmd_list_themes()
        sys.exit(0)

    if args.list_types:
        # 权威图型清单出口（v5.7）：MCP/外部脚本动态消费，杜绝硬编码清单漂移
        print("\n".join(sorted(GENERATORS)))
        sys.exit(0)
    if args.list_flags is not None:
        try: print(list_flags_query(args.list_flags.strip() or None, sorted(GENERATORS)))
        except ValueError as e: print(f"ERROR: {e}", file=sys.stderr); sys.exit(1)
        sys.exit(0)

    if args.theme_swatch:
        resolved = resolve_theme(args.theme_swatch)
        if not resolved:
            print(f"ERROR: 未知主题 '{args.theme_swatch}'。可用: {', '.join(THEME_ORDER)}", file=sys.stderr)
            sys.exit(1)
        out = args.out or (f"theme_{resolved}_swatch.png")
        cmd_theme_swatch(resolved, out)
        sys.exit(0)

    if args.explain:
        cmd_explain(args.explain)
        sys.exit(0)

    if args.suggest:
        if not args.data:
            parser.error("--suggest 需要同时提供 -d/--data")
        cmd_suggest(args.data)
        sys.exit(0)

    if getattr(args, "wizard", False):
        _run_wizard()
        sys.exit(0)

    # ── v3.8：--pub-ready 一键投稿包（语义糖：展开为四件套显式参数）──
    if getattr(args, "pub_ready", False):
        args.verify = True
        if not args.multi_format:
            args.multi_format = ["pdf", "png"]  # 列表形式（与主解析块输出一致）
        if not args.theme:
            args.theme = "okabe-ito"
        args.pub_ready_applied = True
        print("[pub-ready] 已应用投稿包：--verify（PDF 重叠门禁）+ 色盲安全主题 "
              f"{args.theme} + 多格式导出 {args.multi_format} + 复跑交付包", file=sys.stderr)

    # ── v3.1：--quick 一键出图（自动选型 → 复用主渲染管线）──
    if getattr(args, "quick", False):
        if not args.data:
            parser.error("--quick 需要 -d/--data 指向数据文件（不确定图型可先跑 --suggest）")
        try:
            _qdata = load_data(args.data)
        except Exception as _e:
            print(f"ERROR: cannot load '{args.data}': {_e}", file=sys.stderr)
            sys.exit(1)
        _recs = suggest_chart_type(_qdata)
        _best = _recs[0][1] if _recs else "bar"
        _alt = ", ".join(r[1] for r in _recs[1:3]) if _recs else "—"
        args.type = _best
        if not args.out:
            args.out = "quick_" + _best + ".png"
        print(f"--quick: 已按数据自动选择图型 {_best}（其他候选：{_alt}；"
              "打分明细见 --suggest）", file=sys.stderr)

    if getattr(args, "doctor", False) and not args.out:
        # v3.9 --doctor 只体检模式：不渲染不出图
        if not args.type or not args.data:
            parser.error("--doctor（省略 -o）仍需 -t/--type 与 -d/--data")
        _d = load_data(args.data, chart_type=args.type, sheet=args.sheet)
        _n = _doctor_report(args, _d)
        sys.exit(1 if _n else 0)

    if args.demo:
        if not cmd_demo(args):
            sys.exit(1)
        if not args.type or not args.data or not args.out:
            print("ERROR: --demo 需要 --type/--data/--out", file=sys.stderr)
            sys.exit(1)
    else:
        if not args.type or not args.data or not args.out:
            parser.error("必须提供 -t/--type、-d/--data、-o/--out（或用 --demo 交互模式）")

    if isinstance(args.hatch, str):  # v7.8.1 AF9 on|off 归一化（裸旗标=on；off/false/0/no=显式关）
        args.hatch = args.hatch.strip().lower() not in ("off", "false", "0", "no")

    if args.style in ("glm-hatch", "glm-brand"):
        args.theme = "glm" if args.style == "glm-hatch" else "glm-brand"
        if args.hatch is None:
            args.hatch = True; args._hatch_implicit = True  # 隐式置位不冒充用户输入

    if args.style == "sketch": from af_draw import apply_sketch_style; apply_sketch_style()  # v7.6 手绘风
    if args.style in ("glm-brand", "nature-clean") and args.type == "line" \
            and not args.legend_loc:
        args.direct_label = True  # 设计语言第二刀：品牌/顶刊风格下 line 默认直接标注
    if args.style == "nature-clean":
        # ── v3.3：顶刊版式（设计语言包第一刀）——纯增量，默认行为零变化 ──
        args.theme = "okabe-ito"
        _STYLE_NO_GRID[0] = True
        plt.rcParams.update({
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 1.0,
            "legend.frameon": False,
            "grid.alpha": 0.0,
            "grid.linestyle": "-",
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
        })
        print("[style] nature-clean：Okabe-Ito 配色 + 去顶右框线 + 无网格 + 无框图例"
              "（Nature 系版式语言）", file=sys.stderr)

    if getattr(args, "area", False) and args.type != "venn":
        # v3.6：与其他静默忽略项统一口径——显式告知而非致命错（limits/faq 已同步）
        print("[ignored] --area 仅用于 venn；对", args.type,
              "不适用，已忽略（等圆模式为 venn 默认）", file=sys.stderr)
        args.area = False

    if getattr(args, "legend_loc", None):
        _loc = " ".join(args.legend_loc.strip().lower().replace("_", " ")
                        .replace("-", " ").split())
        if _loc not in _LEGEND_LOCS:
            print(f"ERROR: 未知图例位置 '{args.legend_loc}'。可用: best, upper right, "
                  "upper left, lower left, lower right, right, center left, "
                  "center right, lower center, upper center, center", file=sys.stderr)
            sys.exit(1)
        args.legend_loc = _loc
    try:
        annotations = _parse_annotations(args.annotate)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    theme_key = resolve_theme(args.theme)
    if theme_key == "glm-brand" and args.hatch is None:
        args.hatch = True; args._hatch_implicit = True  # v7.6 品牌斜纹默认开启（--hatch off 可关；隐式不打 [ignored]）
    _pal = parse_palette(args.palette) if getattr(args, "palette", None) else None  # v7.9.1 G1 注入
    if _pal:
        print(f"NOTICE: --palette 已注入 {len(_pal)} 色（主题系列色已替换；热图按给定顺序构建色阶）", file=sys.stderr)
    if not theme_key:
        print(f"ERROR: 未知主题 '{args.theme}'。运行 --list-themes 查看全部配色。", file=sys.stderr)
        sys.exit(1)
    if args.journal and args.theme is None and args.journal in JOURNAL_THEME:
        # v2.5 联动：--journal 期刊预设自动套同款配色（显式 --theme 优先）
        theme_key = JOURNAL_THEME[args.journal]
        print(f"配色已联动 {theme_key} 主题（显式 --theme 可覆盖）", file=sys.stderr)
    args.theme = theme_key
    theme = THEMES[theme_key]
    if _pal:  # v7.9.1 G1：palette 覆盖系列色（theme 定型后；热图色阶走 payload）
        theme = dict(theme); theme["colors"] = _pal
    if getattr(args, "theme", None) and args.type in ("heatmap", "cluster_heatmap"): print("NOTICE: 热图单元格配色由 --cmap/--vmin/--vmax 决定（--theme 只影响轴/文字），格色不变属预期", file=sys.stderr)  # v7.9.1 AF31

    # ── v3.2：自动行为透明化（[auto] 前缀显式告知）──
    if args.journal and getattr(args, "width", None):
        print("[auto] --journal 锁定图宽，--width "
              f"{args.width} 已被忽略（--height 仍生效）", file=sys.stderr)
    if (args.type in ("bar", "grouped_bar") and args.data
            and str(args.data).lower().endswith(".csv")):
        print("[hint] CSV 误差棒 v6.0 起支持后缀列写法（如 weight+weight_sd 自动配对；"
              "--csv-no-errors 关闭识别）", file=sys.stderr)
    if getattr(args, "verify", False):
        _fmt = os.path.splitext(str(args.out or ""))[1].lower()
        if _fmt and _fmt != ".pdf":
            print("[auto] --verify 仅对 PDF 输出生效；当前输出为 "
                  f"{_fmt or '无扩展名'}，本次不做像素级重叠检查", file=sys.stderr)
    if args.journal:
        preset = JOURNAL_PRESETS[args.journal]
        if preset.get("cjk_default"):
            args.cjk = True  # Chinese journals: CJK font on by default
        theme = dict(theme)
        w_in = preset["widths_mm"][args.column] / 25.4
        h_ratio = theme["figsize"][1] / theme["figsize"][0]
        theme["figsize"] = (w_in, w_in * h_ratio)
        theme["font_size"] = preset["font_size"]
        theme["dpi"] = preset["dpi"]
        if preset["font_family"] not in plt.rcParams['font.sans-serif']:
            plt.rcParams['font.sans-serif'].insert(0, preset["font_family"])
        print(f"期刊预设 {args.journal}（{args.column} 栏，宽 {w_in:.2f}in，"
              f"字体 {preset['font_family']} {preset['font_size']}pt，最小字号 {preset['min_text_size']}pt"
              f"— 可用 audit_pdf.py --min-size {preset['min_text_size']} 核查）", file=sys.stderr)
    if getattr(args, "size", None):
        rw, rh = (float(v) for v in args.size.split(":"))
        w_in, h_in = theme["figsize"]
        theme["figsize"] = (w_in, w_in * rh / rw)
        print(f"画幅预设 {args.size}：figsize {w_in:.2f}x{theme['figsize'][1]:.2f}in"
              f"（宽度不变，高度按比例）", file=sys.stderr)
    if args.stats == "cox":
        if args.type == "forest":
            data = _run_cox_forest(args)
        elif args.type == "subgroup":
            data = _run_cox_subgroup(args)
        else:
            # v4.5 R2-3：互斥策略统一——参数不适用=[ignored] 显式告知继续（与 auto/multi 同口径）
            print("[ignored] --stats cox（仅 forest/subgroup 生效）对 "
                  f"{args.type} 不适用，本次渲染已忽略", file=sys.stderr)
            args.stats = None
            data = load_data(args.data, chart_type=args.type, sheet=args.sheet,
                         csv_errors=not getattr(args, 'csv_no_errors', False))
    else:
        data = load_data(args.data, chart_type=args.type, sheet=args.sheet,
                         csv_errors=not getattr(args, 'csv_no_errors', False))

    # ── A4(v2.8)+v3.1：cluster_heatmap 降采样（确定性等距采样；校验前执行）──
    # v3.1：行数>3000 且未给 --downsample 时自动采样到 2000 行并显著告知
    #（此前为致命错退出；评测 errorHandling 指出"缺乏自动建议参数尝试"）。
    if (args.type == "cluster_heatmap" and isinstance(data, dict)
            and isinstance(data.get("matrix"), list)):
        _m = data["matrix"]
        _n = len(_m)
        _ds = getattr(args, "downsample", None)
        if _n > 3000 and not _ds:
            _ds = 2000
            print(f"AUTO-DOWNSAMPLE: cluster_heatmap 行数 {_n} 超过硬上限 3000——"
                  "已自动等距采样到 2000 行（确定性采样；需要其他行数用 --downsample N）",
                  file=sys.stderr)
        if _ds and _n > _ds:
            _step = -(-_n // max(int(_ds), 1))
            _idx = list(range(0, _n, _step))
            data["matrix"] = [_m[i] for i in _idx]
            for _k in ("row_labels", "rows", "y_labels"):
                if isinstance(data.get(_k), list) and len(data[_k]) == _n:
                    data[_k] = [data[_k][i] for i in _idx]
            print(f"downsample: cluster_heatmap 行数 {_n} → {len(data['matrix'])}"
                  f"（等距采样，步长 {_step}）", file=sys.stderr)

    # ── v2.9：cluster_heatmap 行数预判（半限 1500 即预警，不等 3000 硬限）──
    for _adv in _preflight_advisories(data, args.type,
                                      getattr(args, "downsample", None)):
        print(f"WARNING: {_adv}", file=sys.stderr)

    # ── v3.6：参数不适用显式告知（消除"静默忽略"——accuracy/usability 靶点）──
    _ignored = []
    if args.stats in ("auto", "multi", "bootstrap") and args.type not in ("box", "violin", "raincloud"):
        _ignored.append(f"--stats {args.stats}（仅 box/violin/raincloud 生效）")
    if args.compare and args.type != "roc":
        _ignored.append("--compare（仅 roc 生效）")
    if args.egger and args.type != "funnel":
        _ignored.append("--egger（仅 funnel 生效）")
    if args.hatch and not getattr(args, "_hatch_implicit", False) and args.type not in ("bar", "grouped_bar", "hbar", "horizontal_bar", "stacked_bar"):
        _ignored.append("--hatch（仅 bar 系生效）")  # v7.8.1 AF9：隐式置位不冒充用户输入
    if args.area and args.type != "venn":
        _ignored.append("--area（仅 venn 生效）")
    if args.sheet and not str(args.data or "").lower().endswith((".xlsx", ".xls")):
        _ignored.append("--sheet（仅 .xlsx 生效）")
    if getattr(args, "order", None) and args.type not in _ORDER_CHARTS:
        _ignored.append("--order（仅 bar/box/violin/line 系生效）")
        args.order = None
    if getattr(args, "normalize", None) and args.type not in _NORM_CHARTS:
        _ignored.append("--normalize（仅 bar 系/line 生效；分布数据不做均值归一）")
        args.normalize = None
    if getattr(args, "arena", None) not in (None, "off") and args.type != "bar": _ignored.append("--arena（仅 -t bar 单系列竖向生效；--arena off 显式关闭默认竞技场）")
    for _ig in _ignored:
        print(f"[ignored] {_ig} 对 {args.type} 不适用，本次渲染已忽略", file=sys.stderr)

    # ── v2.9：JSON 字段名近似匹配告警（拼写错误前置提醒，非致命）──
    for _w in _field_nearmiss_warnings(data):
        print(f"WARNING: {_w}", file=sys.stderr)

    _sv = next((v for v in (data.get("series"), data.get("datasets"),
               data.get("groups")) if isinstance(v, dict)), None)
    advise_colorblind(THEMES.get(theme_key, {}), len(_sv) if _sv else None)  # v7.9.0 AF29 色盲提示

    fatal_msgs, warn_msgs = validate_data(data, args.type)
    for w in warn_msgs:
        print(f"WARNING: {w}", file=sys.stderr)
    if fatal_msgs:
        for m in fatal_msgs:
            print(f"ERROR: {m}", file=sys.stderr)
        if any("CSV" in m or "csv" in m for m in fatal_msgs) or \
           any("error" in m.lower() and "bar" in m.lower() for m in fatal_msgs):
            print("HINT: CSV 误差棒用后缀列（v6.0 起，weight+weight_sd；见 --explain bar）；"
                  "JSON 则用 errors 字段", file=sys.stderr)
        sys.exit(1)
    _memory_hint(data, args.type)
    # ── v3.9：--order / --normalize（渲染前数据变换，stderr 透明告知）──
    if getattr(args, "order", None):
        try:
            apply_series_order(data, args.order, args.type)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
    if getattr(args, "normalize", None):
        try:
            apply_normalize(data, args.normalize, args.type)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
    if getattr(args, "doctor", False):
        _doctor_report(args, data)
    # ── A1(v2.8) 看门狗武装 ── v6.2.0：0=禁用自适应预算留硬保险；负数报错；重试上限全局登记
    global _LAST_ARGS; _LAST_ARGS = args
    os.environ["AF_RETRIES_MAX"] = str(max(0, int(getattr(args, "retries", 1))))
    if args.timeout is None or args.timeout > 0:
        _watchdog_arm(args.type, data,
                      budget=None if args.timeout is None else float(args.timeout))
    elif args.timeout == 0:
        print(f"WARNING: 自适应看门狗已禁用（--timeout 0）——保留 {_WD_HARD_CAP:.0f}s 硬保险防无限挂起（AF_NO_WATCHDOG=1 可完全关闭）", file=sys.stderr)
        _watchdog_arm(args.type, data, budget=_WD_HARD_CAP)
    else:
        print(f"ERROR: --timeout 不接受负数（{args.timeout:g}）；禁用自适应预算请用 --timeout 0（保留硬保险）", file=sys.stderr)
        sys.exit(1)
    if os.environ.get("AF_TEST_RENDER_DELAY") and os.environ.get("AF_RETRY_N", "0") == "0": time.sleep(float(os.environ["AF_TEST_RENDER_DELAY"]))  # 维护者钩子：仅首代延迟（确定性超时）——重试代恢复真实行为，防 savefig 中杀（6.7.0 逐字节锁逮）
    cjk_fp = None
    # Auto-detect: scan displayable text for CJK chars
    def _scan_cjk(obj):
        if isinstance(obj, str):
            return has_cjk(obj)
        if isinstance(obj, dict):
            return any(_scan_cjk(k) for k in obj.keys()) or any(_scan_cjk(v) for v in obj.values())
        if isinstance(obj, (list, tuple)):
            return any(_scan_cjk(v) for v in obj)
        return False

    def _text_has_cjk():
        for t in [args.title, args.xlabel, args.ylabel]:
            if t and has_cjk(t):
                return True
        # Recursive scan catches CJK nested in composite panels/diagram text
        return _scan_cjk(data) if data else False
    _auto_cjk = _text_has_cjk()
    if args.cjk or args.cjk_font or _auto_cjk:
        cjk_fp, cjk_name = load_cjk_font(args.cjk_font)
        if cjk_name:
            plt.rcParams['font.sans-serif'] = [cjk_name, 'DejaVu Sans'] + plt.rcParams['font.sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        if cjk_fp:
            print(f"已加载中文字体: {cjk_name}", file=sys.stderr)
        else:
            print("WARNING: 未找到中文字体，中文可能显示为方框", file=sys.stderr)

    # Create figure（km 默认带自动风险表：主图 + 下方独立表轴）
    width = args.width if args.width else theme["figsize"][0]
    height = args.height if args.height else theme["figsize"][1]
    km_risk = False
    risk_axes = None
    if args.type in ("km", "survival") and not getattr(args, "no_risk_table", False):
        _g = data.get("groups", data.get("series")) if isinstance(data, dict) else None
        if isinstance(_g, dict) and _g:
            def _is_raw_km(v):
                if not isinstance(v, (list, tuple)) or len(v) == 0:
                    return False
                if isinstance(v[0], (list, tuple)):
                    if not all(isinstance(p, (list, tuple)) and len(p) >= 2 for p in v[:8]):
                        return False
                    try:
                        seconds = [float(p[1]) for p in v[:8]]
                    except (TypeError, ValueError):
                        return False
                    return all(s in (0.0, 1.0) for s in seconds)
                return all(isinstance(x, (int, float)) for x in v[:5])
            try:
                km_risk = all(_is_raw_km(v) for v in _g.values())
            except Exception:
                km_risk = False
    if args.type == "cluster_heatmap" and isinstance(data, dict):
        _ch_rows = len(data.get("matrix", data.get("data", data.get("values"))) or [])
        height = max(height, min(_ch_rows * 0.16 + 1.0, 24.0))
    if args.type == "upset" and isinstance(data, dict):
        _us_n = len(data.get("sets") or {})
        if _us_n:
            height = max(height, min(_us_n * 0.42 + 2.8, 18.0))
            width = max(width, 9.0)
    if args.type == "pca" and isinstance(data, dict):
        _pca_n = len(data.get("matrix") or [])
        _has_groups = bool(data.get("groups"))
        if not _has_groups and 0 < _pca_n:
            width = max(width, 8.5)
            height = max(height, 6.0)
    def _make_fig():
        """fig/ax/risk_axes 创建（km 风险表时主图+表轴双行）；A2 降级重建复用。"""
        if km_risk:
            _n_rows = len(data.get("groups", data.get("series", {})) or {})
            _rt_h = min(0.9, 0.34 + 0.24 * max(_n_rows, 1))
            _f, _axes = plt.subplots(
                2, 1, figsize=(width, height + _rt_h),
                gridspec_kw={"height_ratios": [3.4, _rt_h]})
            return _f, _axes[0], _axes[1]
        _f, _a = plt.subplots(figsize=(width, height))
        return _f, _a, None

    fig, ax, risk_axes = _make_fig()

    # Generate
    gen_func = GENERATORS[args.type]
    kwargs = {
        "show_values": args.show_values, "arena": args.arena,
        "arena_default": args.arena is None and args.type == "bar" and not args.horizontal and not getattr(args, "pub_ready_applied", False),
        "trend": args.trend and not args.no_trend,
        "peak_label": getattr(args, "peak_label", False),
        "cmap": args.cmap,
        "vmin": args.vmin,
        "vmax": args.vmax,
        "annot": args.annot, "cell_edge": bool(getattr(args, "cell_edge", False)), "discrete": bool(getattr(args, "discrete", False)), "palette": _pal,
        "horizontal": args.horizontal or args.type in ("hbar", "horizontal_bar"),
        "hatch": args.hatch, "sig_bracket": getattr(args, "sig_bracket", False),
        "sig_auto": getattr(args, "sig_auto", False), "gate": getattr(args, "gate", "basic"),
        "direct_label": getattr(args, "direct_label", False),
        "alternate": args.alternate,
        "show_ratio": args.show_ratio,
        "ratio_base": args.ratio_base,
        "stats_auto": args.stats == "auto",
        "stats_bootstrap": args.stats == "bootstrap",
        "stats_multi": args.stats == "multi",
        "roc_compare": getattr(args, "compare", False),
        "sensitivity": getattr(args, "sensitivity", False),
        "median_auto": not getattr(args, "no_median", False),
        "egger": getattr(args, "egger", False),
        "area_mode": getattr(args, "area", False),
        "risk_table": km_risk,
        "rmst_tau": getattr(args, "rmst_tau", None),
        "risk_axes": risk_axes if km_risk else None,
        "risk_times": getattr(args, "risk_times", None),
        "auto_cjk_hdr": bool(args.cjk) and args.type in ("km", "survival"),
    }
    _a2_degraded = False
    for _a2_try in (1, 2):
        try:
            extra = gen_func(data, ax, theme, cjk_fp, **kwargs)
            break
        except MemoryError:
            plt.close(fig)
            if _a2_try == 2:
                raise
            width, height = width * 0.85, height * 0.85
            fig, ax, risk_axes = _make_fig()
            kwargs["risk_axes"] = risk_axes if km_risk else None
            _a2_degraded = True
            print("WARNING: 渲染内存不足——已自动降级重试（图幅 ×0.85，输出 DPI 减半）",
                  file=sys.stderr)

    # composite/diagram/upset manage their own axes and styling
    is_self_managed = extra in ("composite", "diagram", "flow", "upset")

    # v4.7 D-12：--title 对自管图型不生效——按 [ignored] 透明告知承诺显式提示
    if is_self_managed and getattr(args, "title", None):
        print(f"[ignored] --title 对 {args.type} 不生效（自管图型；标题放 JSON 的 "
              "title 字段）", file=sys.stderr)

    # Style (skip for self-managed types and dual_axis)
    if args.type not in ('dual_axis',) and not is_self_managed:
        apply_base_style(ax, theme)

    # Labels (skip for self-managed types like composite/diagram)
    if not is_self_managed:
        if args.title:
            title_text = args.title.replace('\\n', '\n')
            _t_pad = 22 if getattr(args, "subtitle", None) else 12
            ax.set_title(title_text, fontsize=theme["font_size"] + 1, fontweight='bold',
                         pad=_t_pad, loc=None if _SKETCH_MODE[0] else "center",
                         fontproperties=cjk_fp if cjk_fp and has_cjk(title_text) else None)
        if getattr(args, "summary", False) and not getattr(args, "subtitle", None):
            # v4.1 自动数据摘要副标题：只陈述计数事实（零推断，accuracy 优先）。
            # 单列观测计 wide 系列"系列名: 列表"的全部数值个数；km 统计例数与事件数。
            try:
                _sum_txt = _auto_summary(data, args.type)
            except Exception:
                _sum_txt = None
            if _sum_txt:
                print(f"summary: {_sum_txt}", file=sys.stderr)
            args.subtitle = _sum_txt
        if getattr(args, "subtitle", None):
            # v4.0 标题层级：副标题主标题正下方第二行（小号灰色，非加粗）
            _sub = str(args.subtitle).strip()[:200]
            ax.text(0.5, 1.012, _sub, transform=ax.transAxes, ha="center", va="bottom",
                    fontsize=theme["font_size"] - 1, color="#555555",
                    fontproperties=cjk_fp if cjk_fp and has_cjk(_sub) else None)
        if getattr(args, "source", None):
            # v4.0 来源注：整图底部小字（supxlabel 参与 tight_layout 自动让位，
            # 不与 x 刻度标签重叠；组合图/双轴均安全）
            _src = str(args.source).strip()[:200]
            try:
                fig.supxlabel(_src, x=0.995, ha="right",
                              fontsize=max(5.5, theme["font_size"] - 2), color="#777777",
                              fontproperties=cjk_fp if cjk_fp and has_cjk(_src) else None)
            except AttributeError:  # matplotlib<3.4 无 supxlabel：退化为 fig.text
                fig.text(0.995, 0.005, _src, ha="right", va="bottom",
                         fontsize=max(5.5, theme["font_size"] - 2), color="#777777",
                         fontproperties=cjk_fp if cjk_fp and has_cjk(_src) else None)
        if args.xlabel:
            ax.set_xlabel(args.xlabel, fontsize=theme["font_size"],
                          fontproperties=cjk_fp if cjk_fp and has_cjk(args.xlabel) else None)
        if args.ylabel:
            ax.set_ylabel(args.ylabel, fontsize=theme["font_size"],
                          fontproperties=cjk_fp if cjk_fp and has_cjk(args.ylabel) else None)
            _ensure_ylabel_clear(ax)

        # Colorbar (for heatmap only — extra must be a ScalarMappable)
        if extra is not None and hasattr(extra, 'get_cmap'):
            cbar = fig.colorbar(extra, ax=ax, shrink=0.8)
            cbar_label = data.get("cbar_label", args.ylabel)
            if cbar_label:
                cbar.set_label(cbar_label, fontsize=theme["font_size"] - 1,
                              fontproperties=cjk_fp if cjk_fp and has_cjk(cbar_label) else None)

        # Legend (skip if no labeled artists)
        _dl = getattr(args, "direct_label", False) and args.type == "line"
        # v3.4.1（55 线发现）：dual_axis 的组合图例（左+右轴）由 gen_dual_axis 内部构建，
        # 主流程无参 ax.legend() 会用主轴 handles 重建→右轴系列（如 CRP）从图例消失。
        if not _dl and args.type != "dual_axis" and not args.no_legend \
                and args.legend and ax.get_legend_handles_labels()[1]:
            ax.legend(fontsize=theme["font_size"] - 1, loc='best', framealpha=0.9,
                      prop=cjk_fp if cjk_fp else None)
        if args.type in ("bar", "grouped_bar", "hbar", "horizontal_bar", "line", "stacked_bar"):
            n_series = len(data.get("series", data.get("datasets", {})))
        elif args.type == "scatter":
            groups = data.get("groups")
            n_series = len(set(groups)) if isinstance(groups, (list, tuple)) and groups else 1
        else:
            n_series = 1
        audit_msg = legend_audit(ax, args.type, args.no_legend, n_series)
        if audit_msg:
            print(f"WARNING: {audit_msg}", file=sys.stderr)

    # ── v2.5 投稿精修：注释与图例控制（置于 CJK 兜底前，新文本一并被兜底覆盖；
    #    组合图/流程图等自管类型同样生效）──
    if annotations:
        cjk_fp = _apply_annotations(fig, annotations, theme, cjk_fp)
    if getattr(args, "legend_loc", None) or getattr(args, "legend_outside", False):
        _apply_legend_control(fig, loc=args.legend_loc, outside=args.legend_outside,
                              theme=theme, cjk_fp=cjk_fp)

    # ── 机制级兜底（必须在一切 draw 前：tight_layout/防重叠/savefig 都会渲染文本）──
    # 两层防护：①调用点忘传 fontproperties ②用户数据无中文但引擎自动生成中文标注
    # （如 KM 风险表/中位生存标注）导致 cjk_fp 未启用——此处发现 CJK 文本即自动找字体。
    import matplotlib.text as _mtext
    _cjk_texts = [t for t in fig.findobj(_mtext.Text)
                  if t.get_text() and has_cjk(t.get_text())
                  and not getattr(t, "_af_keep_fp", False)]
    if _cjk_texts:
        if cjk_fp is None:
            try:
                cjk_fp, cjk_name = load_cjk_font(None)
                if cjk_fp and not _SKETCH_MODE[0]:
                    plt.rcParams['font.sans-serif'] = [cjk_name, 'DejaVu Sans']
                    plt.rcParams['axes.unicode_minus'] = False
                    print(f"自动补启用中文字体: {cjk_name}（图内含自动生成的中文标注）",
                          file=sys.stderr)
            except Exception:
                pass
        if cjk_fp is not None:
            _fixed = 0
            for _t in _cjk_texts:
                try:
                    _t.set_fontproperties(cjk_fp)
                    _fixed += 1
                except Exception:
                    pass
            if _fixed:
                print(f"CJK 字体兜底：{_fixed} 处含中文文本已统一挂中文字体", file=sys.stderr)

    if not is_self_managed:
        plt.tight_layout()
        if getattr(args, "source", None): fig.subplots_adjust(bottom=0.18)  # v7.6.1 来源注与两行 x 标签防挤压

    # Mechanism-level anti-overlap: detect real collisions post-render and
    # degrade tick labels until no axis overlaps (works for composite panels)
    fix_tick_overlaps(fig)

    # Determine output format(s) and DPI（v2.6 C1：--multi-format 一次多格式）
    out_ext = os.path.splitext(args.out)[1].lower()
    fmt_map = {'.png': 'png', '.svg': 'svg', '.pdf': 'pdf', '.tiff': 'tiff', '.tif': 'tiff', '.eps': 'eps'}
    if getattr(args, "multi_format", None):
        _base = os.path.splitext(args.out)[0]
        save_targets = [(fmt, _base + "." + fmt) for fmt in args.multi_format]
    else:
        out_format = args.format if args.format else fmt_map.get(out_ext, 'png')
        _is_vec = out_format in ('svg', 'pdf', 'eps')
        final_out = args.out
        if not _is_vec and out_ext not in fmt_map:
            final_out = args.out + '.' + out_format
        save_targets = [(out_format, final_out)]

    # Smart DPI: raster formats use theme DPI (default 600 for line art),
    # vector formats ignore DPI (but we still set it for fallback)
    dpi = args.dpi if args.dpi else theme["dpi"]
    if _a2_degraded:
        dpi = max(150, int(dpi) // 2)

    saved_files = []
    for out_format, final_out in save_targets:
        is_vector = out_format in ('svg', 'pdf', 'eps')
        # For heatmaps or photo-heavy content, user can specify --dpi 300
        save_kwargs = {
            "dpi": dpi,
            "facecolor": 'white',
            "edgecolor": 'none',
        }
        # v4.5 R2-2：期刊预设激活时不用 tight 裁边——tight 会把实际图宽裁掉
        # 2.5-2.6mm（85→82.4），期刊按毫米核图有退稿风险；精确画布=宣称宽度。
        # 非 journal 保持 tight（吸收超界文本，日常美学不变）。
        if not getattr(args, "journal", None):
            save_kwargs["bbox_inches"] = 'tight'
        if out_format == 'pdf':
            # v4.5 R2-5：PDF 去 CreationDate → 同输入同字节（PNG 已成立）
            save_kwargs["metadata"] = {"CreationDate": None}
        if out_format == 'tiff':
            save_kwargs["pil_kwargs"] = {"compression": "tiff_lzw"}
        for _attempt in (1, 2):
            try:
                fig.savefig((_t := f"{final_out}.af_tmp{os.getpid()}"), format=out_format, **save_kwargs); os.replace(_t, final_out)  # v7.7.1 原子落盘：杀代竞态下僵尸渲染线程的滞后写只进孤儿 inode，不再截断成品（重试链逐字节锁复现实锤）
                break
            except OSError as e:
                if _attempt == 1:
                    print(f"WARNING: 文件写出失败（{e}），0.5 秒后自动重试一次…", file=sys.stderr)
                    time.sleep(0.5)
                else:
                    raise
            except MemoryError:
                if _attempt == 1:
                    save_kwargs["dpi"] = max(150, int(save_kwargs["dpi"]) // 2)
                    print("WARNING: 输出内存不足——DPI 已降为 "
                          f"{save_kwargs['dpi']} 自动重试一次…", file=sys.stderr)
                else:
                    raise
        saved_files.append((out_format, final_out, is_vector))
    plt.close()

    if args.alt:
        try:
            alt = generate_alt_text(args.type, data, args.title)
            alt_path = os.path.splitext(final_out)[0] + ".alt.txt"
            with open(alt_path, "w", encoding="utf-8") as f:
                f.write(alt + "\n")
            print(f"无障碍描述: {alt_path}", file=sys.stderr)
        except Exception as e:  # alt text must never break rendering
            print(f"WARNING: alt text generation failed: {e}", file=sys.stderr)

    if getattr(args, "caption", False):
        try:
            if _afcharts is not None:
                cap = _afcharts.make_caption(args.type, data, args.title)
            else:
                cap = args.title or args.type
            cap_path = os.path.splitext(final_out)[0] + ".caption.txt"
            with open(cap_path, "w", encoding="utf-8") as f:
                f.write(cap + "\n")
            print(f"图注: {cap_path}", file=sys.stderr)
        except Exception as e:  # caption 同样永不阻断渲染
            print(f"WARNING: caption generation failed: {e}", file=sys.stderr)

    cjk_info = " (colorblind-safe)" if theme.get("colorblind_safe") else ""
    if len(saved_files) == 1:
        out_format, final_out, is_vector = saved_files[0]
        sz = os.path.getsize(final_out)
        fmt_info = f"{out_format.upper()} @ {dpi}DPI" if not is_vector else f"{out_format.upper()} 矢量"
        print(f"已保存: {final_out}（{sz:,} 字节，{fmt_info}{cjk_info}）", file=sys.stderr)
    else:
        for _fmt, _path, _isvec in saved_files:
            sz = os.path.getsize(_path)
            fmt_info = f"{_fmt.upper()} @ {dpi}DPI" if not _isvec else f"{_fmt.upper()} 矢量"
            print(f"已保存: {_path}（{sz:,} 字节，{fmt_info}{cjk_info}）", file=sys.stderr)

    if getattr(args, "multi_format", None):
        _pdf_pick = [_p for _f, _p, _ in saved_files if _f == "pdf"]
        if _pdf_pick:
            out_format, final_out, is_vector = "pdf", _pdf_pick[0], True
        else:
            print("WARNING: --verify 只核查 PDF；--multi-format 中没有 PDF，跳过核查",
                  file=sys.stderr)
            args.verify = False
    if args.verify:
        if out_format != 'pdf':
            print("WARNING: --verify 仅核查 PDF 输出，本次跳过 / only applies to PDF", file=sys.stderr)
        else:
            try:
                sys.path.insert(0, SCRIPT_DIR)
                from verify_overlap_pixel import verify
            except ImportError:
                print("WARNING: --verify 需要 PyMuPDF(fitz)+scipy：pip install pymupdf scipy / requires PyMuPDF+scipy",
                      file=sys.stderr)
            else:
                real_overlaps, details = verify(final_out)
                if real_overlaps > 0:
                    print(f"VERIFY FAIL: 检出 {real_overlaps} 处真实文字重叠 / real overlaps in {final_out} — exit 2",
                          file=sys.stderr)
                    sys.exit(2)
                print(f"VERIFY OK: 无真实文字重叠 / no overlaps in {final_out}", file=sys.stderr)

    # ── v5.2 机制：audit/repro 移出单格式分支（multi-format 曾静默失效）；
    # 且置于 verify 门禁之后——verify FAIL 退出时不给坏图留复跑包。
    if getattr(args, "audit", False):
        write_audit_sidecar(data, args.type, args.out)
    if getattr(args, "repro", False) or getattr(args, "pub_ready_applied", False):
        write_repro_bundle(list(sys.argv), data, args.out,
                           extra_outputs=sorted({p for _f, p, _v in saved_files}))




# ── A1(v2.8)：渲染看门狗（v2.10：退出码分级与异常诊断拆至 af_diagnostics.py）──

_WD_BASE_BUDGET = {
    "cluster_heatmap": 240, "composite": 180, "pca": 120, "km": 120, "rmst": 120, "rob": 120,
    "forest": 90, "venn": 90, "prisma": 60,
}
_WD_DEFAULT_BUDGET = 90.0
_WD_MIN, _WD_MAX = 30.0, 1800.0
_WD_HARD_CAP = 7200.0  # --timeout 0（禁用自适应预算）时的硬保险，防无限挂起；不随重试放宽


def _wd_estimate_rows(data):
    """粗估数据规模（行数），供自适应预算；取不到返回 0。"""
    try:
        if not isinstance(data, dict):
            return 0
        m = data.get("matrix")
        if isinstance(m, list) and m:
            return len(m)
        g = data.get("groups")
        if isinstance(g, dict) and g:
            return max(len(v) for v in g.values())
        s = data.get("series")
        if isinstance(s, dict) and s:
            return max(len(v) for v in s.values())
        x = data.get("x")
        if isinstance(x, list):
            return len(x)
    except Exception:
        pass
    return 0


def _wd_scale(budget):
    """v6.2.0：重试代看门狗预算放宽（AF_WD_BUDGET_SCALE=1.5^N，由重试层写入）。"""
    try:
        s = float(os.environ.get("AF_WD_BUDGET_SCALE", "1") or 1)
    except ValueError:
        s = 1.0
    return budget * (s if s >= 1.0 else 1.0)


def _wd_budget_for(chart_type, data):
    rows = _wd_estimate_rows(data)
    base = _WD_BASE_BUDGET.get(chart_type, _WD_DEFAULT_BUDGET)
    factor = 1.0 + min(3.0, rows / 2000.0)
    return _wd_scale(max(_WD_MIN, min(_WD_MAX, base * factor)))


def _watchdog_arm(chart_type, data, budget=None):
    """A1(v2.8)：看门狗。监控线程发现主线程超过预算仍未结束 → 中文三段式诊断 +
    强制退出（exit 5）。跨平台（监控线程 + os._exit，不用 SIGALRM）；正常或异常
    结束时主线程消亡，守护线程自行退出，不会误伤。AF_NO_WATCHDOG=1 亦可禁用。"""
    if os.environ.get("AF_NO_WATCHDOG"):
        return None
    if budget is None:
        budget = _wd_budget_for(chart_type, data)
    elif budget != _WD_HARD_CAP:
        budget = _wd_scale(budget)  # v6.2.0：显式预算在重试代同样放宽；硬保险除外
    start = time.time()
    main_t = threading.main_thread()

    def _fire():
        el = time.time() - start
        print("ERROR: 渲染看门狗超时——图表未能按时完成，已强制中断（exit 5）",
              file=sys.stderr)
        print(f"└ 已用时 {el:.0f}s，超过预算 {budget:.0f}s"
              f"（图型={chart_type}，数据规模≈{_wd_estimate_rows(data)} 行）",
              file=sys.stderr)
        print("建议1: 数据过大先瘦身——cluster_heatmap 可加 --downsample 2000 等距采样",
              file=sys.stderr)
        print("建议2: 调大预算 --timeout 600；或本图禁用看门狗 --timeout 0",
              file=sys.stderr)
        print("建议3: composite 面板过多时拆成多图分别渲染", file=sys.stderr)
        rc = _spawn_retry(5)
        os._exit(5 if rc is None else rc)  # rc=重试进程最终退出码；None=未重试按 5

    def _monitor():
        warned = set()
        step = min(1.0, max(0.05, budget / 10.0))  # v6.2.0：预算<1s 时步长跟随，保证精度
        while True:
            time.sleep(step)
            if not main_t.is_alive():
                return
            el = time.time() - start
            if el >= budget:
                _fire()
                return
            for frac, tag in ((0.5, "50%"), (0.8, "80%")):
                if el >= budget * frac and tag not in warned:
                    warned.add(tag)
                    print(f"WARNING: 渲染已用时 {el:.0f}s（预算 {budget:.0f}s 的 {tag}）——"
                          f"超时将中断并给出建议", file=sys.stderr)

    t = threading.Thread(target=_monitor, name="af-watchdog", daemon=True)
    t.start()
    return t


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        sys.exit(130)
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        rc = _spawn_retry(code)
        if rc is not None:
            sys.exit(rc)
        raise
    except Exception as e:  # v3 中文诊断 + v6.4.0 --debug 结构化侧车（两分支行为本相同，去重）
        if os.environ.get("AF_DEBUG"):
            raise  # 维护者/反馈通道：完整 traceback
        _print_v3_error(e)
        if _LAST_ARGS is not None and getattr(_LAST_ARGS, "debug", False): _write_debug_report(_LAST_ARGS, e, getattr(_LAST_ARGS, "out", None))
        sys.exit(_classify_exit_code(e))
