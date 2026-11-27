# -*- coding: utf-8 -*-
"""af_draw — 核心图型生成器+统计标注助手（v4.0.0 模块化第四刀，自 gen_figure 拆出）。

拆分后 gen_figure 主文件保留：参数解析/校验/统计推断/流水线/文档；
本模块只做绘制。公开名经 gen_figure 再导出，`import gen_figure` 用法不变。
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle
import numpy as np

try:
    import af_v23_stats as _afstats
except ImportError:  # 统计模块不在同目录时降级（标注函数自行判 None 提示）
    _afstats = None
from af_shared import (has_cjk, HATCH_PATTERNS, _STYLE_NO_GRID, _ensure_ylabel_clear,
                       _SKETCH_MODE, hero_panel_mode, fmt_ratio_ci, cell_text_color)

# v7.9.1 AF40：定性色阶名单（承载有序/数值标度时 colorbar 语义易误读）
_QUALITATIVE_CMAPS = {"Set1", "Set2", "Set3", "Pastel1", "Pastel2", "Accent",
                      "Dark2", "Paired", "tab10", "tab20", "tab20b", "tab20c"}


def _darken_color(color, factor=0.55):
    """Return a darker shade of the given color. (Legacy; hatch now uses black.)"""
    import matplotlib.colors as mcolors
    try:
        rgb = mcolors.to_rgb(color)
        return tuple(c * factor for c in rgb)
    except Exception:
        return (0.2, 0.2, 0.2)


# ── Auto significance annotations (v2.2) ──────────────────────────────

def _sig_stars(p):
    return "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "NS"


def pairwise_vs_first(series):
    """Compare each series against the first one: Shapiro normality test,
    then Welch t-test (both normal) or Mann-Whitney U (otherwise).
    Returns [(name, p_or_None, stars, method)]. Requires scipy."""
    from scipy import stats as _st
    names = list(series.keys())
    if len(names) < 2:
        return []
    ref_all = np.asarray(series[names[0]], dtype=float)
    ref_all = ref_all[np.isfinite(ref_all)]
    out = []
    for name in names[1:]:
        vals = np.asarray(series[name], dtype=float)
        vals = vals[np.isfinite(vals)]
        if len(vals) < 3 or len(ref_all) < 3:
            out.append((name, None, "n.s.", "n<3"))
            continue
        normal = True
        for arr in (ref_all, vals):
            if 3 <= len(arr) <= 5000:
                _, sp = _st.shapiro(arr)
                if sp <= 0.05:
                    normal = False
                    break
        if normal:
            _, p = _st.ttest_ind(ref_all, vals, equal_var=False)
            method = "Welch t"
        else:
            _, p = _st.mannwhitneyu(ref_all, vals, alternative="two-sided")
            method = "Mann-Whitney U"
        out.append((name, float(p), _sig_stars(float(p)), method))
    return out


def draw_bootstrap_brackets(ax, positions, results, data_top, font_size=8):
    """v3.5：bootstrap 均值差 95%CI 括号（文本=Δ 与 CI 区间，非 p 星号）。"""
    span = max(abs(data_top) * 0.08, 1e-9)
    for j, (name, diff, lo, hi) in enumerate(results):
        if diff is None:
            continue
        yi = data_top + span * (0.55 + 1.05 * j)
        x0, x1 = positions[0], positions[j + 1]
        ax.plot([x0, x0, x1, x1],
                [yi - span * 0.22, yi, yi, yi - span * 0.22],
                color="#333333", lw=1.2, zorder=6)
        sig = "" if (lo > 0 or hi < 0) else "（CI 含 0）"
        ax.text((x0 + x1) / 2, yi + span * 0.10,
                f"Δ={diff:.3g}, 95%CI[{lo:.3g},{hi:.3g}]{sig}",
                ha="center", va="bottom", fontsize=font_size, color="#333333", zorder=6)
    return data_top + span * (0.55 + 1.05 * max(0, len(results) - 1)) + span * 0.6


def annotate_bootstrap_stats(ax, series, positions, theme, chart_type):
    """--stats bootstrap 入口（box/violin）：每组均值 bootstrap CI 误差棒
    + 组间均值差 CI 括号 + stderr 报告（确定性：固定种子）。"""
    names = list(series.keys())
    if len(names) < 2:
        print(f"WARNING: --stats bootstrap needs >= 2 series ({chart_type}); skipped",
              file=sys.stderr)
        return
    import os as _os
    seed = int(_os.environ.get("AF_BOOTSTRAP_SEED", "20260925"))
    try:
        from af_v23_stats import bootstrap_ci, bootstrap_vs_first, bootstrap_median_ci
        per_group = [(n,) + bootstrap_ci(v, seed=seed) for n, v in series.items()]
        med_ci = [(n,) + bootstrap_median_ci(v, seed=seed) for n, v in series.items()]
        diffs = bootstrap_vs_first(series, seed=seed)
    except ImportError:
        print("WARNING: --stats bootstrap requires numpy（环境侧，退出码 4）", file=sys.stderr)
        return
    except ValueError as e:
        print(f"WARNING: --stats bootstrap: {e}", file=sys.stderr)
        return
    # 每组均值 ± bootstrap CI 误差棒（画在组位置上）
    for (name, stat, lo, hi), x_pos in zip(per_group, positions):
        err_lo, err_hi = stat - lo, hi - stat
        ax.errorbar(x_pos, stat, yerr=[[max(err_lo, 0)], [max(err_hi, 0)]],
                    fmt="D", markersize=4, color="#333333", ecolor="#333333",
                    elinewidth=1.4, capsize=4, capthick=1.4, zorder=7)
    data_top = max(max([float(v) for v in vals]) for vals in series.values() if len(vals))
    top = draw_bootstrap_brackets(ax, positions, diffs, data_top,
                                  font_size=max(6, theme["font_size"]))
    lo_ax, hi_ax = ax.get_ylim()
    if top > hi_ax:
        ax.set_ylim(lo_ax, top)
    print(f"stats bootstrap（percentile 法，{5000} 次重采样，种子 {seed}）：", file=sys.stderr)
    for name, stat, lo, hi in per_group:
        print(f"  {name}: 均值={stat:.4g}, 95%CI[{lo:.4g},{hi:.4g}]", file=sys.stderr)
    for (name, med, mlo, mhi), (_, stat, lo, hi) in zip(med_ci, per_group):
        print(f"  {name}: 中位数={med:.4g}, 95%CI[{mlo:.4g},{mhi:.4g}]"
              f"（偏态数据建议引用中位数 CI 而非均值 CI）", file=sys.stderr)
    g0 = names[0]
    for name, diff, lo, hi in diffs:
        if diff is None:
            continue
        verdict = "稳健差异" if (lo > 0 or hi < 0) else "CI 含 0（不能断言差异）"
        print(f"  {g0} vs {name}: 均值差 Δ={diff:.4g}, 95%CI[{lo:.4g},{hi:.4g}] —— {verdict}",
              file=sys.stderr)


def draw_stat_brackets(ax, positions, results, data_top, font_size=8):
    """Draw one comparison bracket per result (each group vs group 0), stacked
    above the tallest data point. Returns the new suggested ylim top."""
    span = max(abs(data_top) * 0.08, 1e-9)
    for j, (name, p, stars, method) in enumerate(results):
        if p is None:
            continue
        yi = data_top + span * (0.55 + 1.05 * j)
        x0, x1 = positions[0], positions[j + 1]
        ax.plot([x0, x0, x1, x1],
                [yi - span * 0.22, yi, yi, yi - span * 0.22],
                color="#333333", lw=1.2, zorder=6)
        ax.text((x0 + x1) / 2, yi + span * 0.10, stars, ha="center",
                va="bottom", fontsize=font_size, color="#333333", zorder=6)
    return data_top + span * (0.55 + 1.05 * max(0, len(results) - 1)) + span * 0.6


def annotate_auto_stats(ax, series, positions, theme, chart_type):
    """--stats auto entry point for box/violin: compute + draw + report."""
    names = list(series.keys())
    if len(names) < 2:
        print(f"WARNING: --stats auto needs >= 2 series ({chart_type}); skipped",
              file=sys.stderr)
        return
    try:
        results = pairwise_vs_first(series)
    except ImportError:
        print("WARNING: --stats auto requires scipy — install with: pip install scipy",
              file=sys.stderr)
        return
    data_top = max(max([float(v) for v in vals]) for vals in series.values() if len(vals))
    top = draw_stat_brackets(ax, positions, results, data_top,
                             font_size=max(6, theme["font_size"]))
    lo, hi = ax.get_ylim()
    if top > hi:
        ax.set_ylim(lo, top)
    g0 = names[0]
    for name, p, stars, method in results:
        p_txt = "NA" if p is None else f"{p:.4g}"
        print(f"  stats ({chart_type}): {g0} vs {name}: {method}, p={p_txt} -> {stars}",
              file=sys.stderr)


def annotate_multi_stats(ax, series, positions, theme, chart_type):
    """--stats multi 入口：全两两比较（正态→Tukey；否则 Kruskal-Wallis+Dunn+Hochberg）。"""
    if _afstats is None:
        print("WARNING: --stats multi 需要 af_v23_stats.py 与 gen_figure.py 同目录",
              file=sys.stderr)
        return
    names = list(series.keys())
    if len(names) < 3:
        print("WARNING: --stats multi 需要 >=3 组（两组比较请用 --stats auto）",
              file=sys.stderr)
        return
    clean = {}
    for n, v in series.items():
        arr = np.asarray(v, dtype=float)
        clean[n] = arr[np.isfinite(arr)]
    try:
        pairs = _afstats.multi_pairwise(clean)
    except ValueError as e:
        print(f"WARNING: --stats multi 无法计算：{e}", file=sys.stderr)
        return
    data_top = max(max([float(x) for x in v]) for v in clean.values() if len(v))
    span = max(abs(data_top) * 0.08, 1e-9)
    sig = [t for t in pairs if t[2] is not None]
    if len(sig) > 8:
        print(f"WARNING: 显著对比 {len(sig)} 对，仅绘制前 8 对括号（完整结果见 stderr 报告）",
              file=sys.stderr)
    top_needed = data_top
    for idx, (a_name, b_name, p, stars, method) in enumerate(sig[:8]):
        yi = data_top + span * (0.55 + 1.05 * idx)
        x0 = positions[names.index(a_name)]
        x1 = positions[names.index(b_name)]
        ax.plot([x0, x0, x1, x1],
                [yi - span * 0.22, yi, yi, yi - span * 0.22],
                color="#333333", lw=1.2, zorder=6)
        ax.text((x0 + x1) / 2, yi + span * 0.10, stars, ha="center",
                va="bottom", fontsize=max(6, theme["font_size"]), color="#333333", zorder=6)
        top_needed = yi + span * 0.6
    lo, hi = ax.get_ylim()
    if top_needed > hi:
        ax.set_ylim(lo, top_needed)
    for a_name, b_name, p, stars, method in pairs:
        print(f"  stats ({chart_type}): {a_name} vs {b_name}: {method}, p={p:.4g} -> {stars}",
              file=sys.stderr)


# ── Alt text generation (v2.2, accessibility) ─────────────────────────


def _fmt_series_value(v, series_values):
    """v6.8.0：show-values 数值标签精度自适应（随系列数据小数位，cap 3；整数仍整数）。
    历史：bar 固定 .1f 曾把 5.032 显示成 5.0（视觉门二轮机械断言抓获）。"""
    v = float(v)
    if v.is_integer():
        return f"{int(v)}"

    def _dec(x):
        s = f"{float(x):.6f}".rstrip("0")
        return len(s.split(".")[1]) if "." in s else 0

    nd = min(3, max((_dec(x) for x in series_values), default=1))
    return f"{v:.{nd}f}"


def _hatch_edgecolor(theme, fill_color):
    """斜纹描边色：主题声明 hatch_edge=auto 时用填充同系深色，否则黑色（历史行为）。"""
    if not isinstance(theme, dict) or theme.get("hatch_edge") != "auto":
        return "black"
    fills = fill_color if isinstance(fill_color, list) else [fill_color]
    return [_darken_color(c, 0.55) for c in fills] if isinstance(fill_color, list) \
        else _darken_color(fill_color, 0.55)


def apply_base_style(ax, theme):
    """Apply common styling to axes."""
    for spine in theme["spines"]:
        ax.spines[spine].set_visible(False)
    if _STYLE_NO_GRID[0]:
        ax.grid(False)
        ax.tick_params(labelsize=theme["font_size"] - 1, length=3, width=1.0)
        return
    ax.yaxis.grid(True, alpha=theme["grid_alpha"], linestyle='--')
    ax.tick_params(labelsize=theme["font_size"] - 1)


def apply_sketch_style():
    """v7.6 --style sketch：手绘风（参考图精髓复刻）。xkcd path effects（线条抖动+
    手写体 fallback 链）+淡虚线网格+粗白纹；配合立体皇冠与黑粗数值标签。"""
    plt.xkcd()
    plt.rcParams["font.family"] = ["Balsamiq Sans", "Comic Neue", "Patrick Hand",
                                   "Humor Sans", "xkcd", "Comic Sans MS",
                                   "DejaVu Sans"]  # v7.6.1 粗圆马克笔手写链（Balsamiq=参考图同气质且高辨识）
    plt.rcParams["axes.grid.axis"] = "y"  # 参考图=仅水平网格
    plt.rcParams["axes.titlelocation"] = "left"
    plt.rcParams["axes.titlecolor"] = "#1F4E79"
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["hatch.linewidth"] = 2.2
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.linestyle"] = "--"
    plt.rcParams["grid.alpha"] = 0.35
    plt.rcParams["grid.linewidth"] = 0.7
    plt.rcParams["axes.axisbelow"] = True  # 网格在柱体下层（参考图口径）
    _SKETCH_MODE[0] = True
    os.environ["AF_SKETCH"] = "1"  # detect_cjk_font 子进程感知手绘模式（中文手写字形）
    print("[style] sketch 手绘模式（xkcd 手绘线+淡虚线网格+粗白纹+黑粗数值+立体皇冠）",
          file=sys.stderr)


_ARENA_FILL = ("#E8A33D", "#5B8DB8", "#9B72C7")   # v7.6.2 数据柱全彩循环（橙斜/蓝点/紫斜）
_ARENA_HATCH = ("///", "..", "///")               # 白粗纹两种（斜/点）×三彩
_ARENA_BASE = "#A9B7C6"                            # 参照系柱（人类/基线/随机）=浅蓝灰实心，不占彩循环位
_ARENA_BASELINE_KW = ("基线", "人类", "随机", "baseline", "human", "random")
_ARENA_CHAMP = "#0F8A6D"


def _labels_short(lb):
    """v7.6.2 arena stderr 用：标签首行截断。"""
    return str(lb).split("\n")[0][:12]


def _draw_crown(ax, bar, vmax, yspan=None):
    """v7.6 --arena 立体皇冠（参考图 emoji 皇冠复刻）：五尖冠体+三尖顶圆球
    +分离底座+双层金+深棕描边。抬升按轴跨度计（低值面板数值不被压）。"""
    cx = bar.get_x() + bar.get_width() / 2.0
    _span = yspan if yspan else vmax
    y0 = bar.get_y() + bar.get_height() + _span * 0.12
    w = bar.get_width() * 0.52
    h = _span * 0.075
    xL, xR = cx - w, cx + w
    yb = y0 + h * 0.16
    pts = [(xL, yb), (xL, yb + h * 0.62), (cx - w * 0.5, yb + h * 0.30),
           (cx, yb + h * 0.95), (cx + w * 0.5, yb + h * 0.30), (xR, yb + h * 0.62),
           (xR, yb)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="#F6B72E",
                         edgecolor="#8A5A16", linewidth=1.6, zorder=7))
    for fx, fy in ((xL, yb + h * 0.62), (cx, yb + h * 0.95), (xR, yb + h * 0.62)):
        ax.add_patch(Circle((fx, fy), w * 0.12, facecolor="#FFD34D",
                            edgecolor="#8A5A16", linewidth=1.2, zorder=8))
    ax.add_patch(FancyBboxPatch(
        (xL - w * 0.10, y0), 2 * (w + w * 0.10), h * 0.15,
        boxstyle="round,pad=0,rounding_size=" + str(w * 0.08),
        facecolor="#E09E1F", edgecolor="#8A5A16", linewidth=1.4, zorder=9))


def gen_bar(data, ax, theme, cjk_fp, **kwargs):
    """Grouped bar chart with horizontal mode, hatching, error bars, significance, and ratio annotations."""
    labels = data.get("labels", data.get("x", []))
    series = data.get("series", data.get("datasets", {}))

    n_groups = len(labels)
    n_series = len(series)
    x = np.arange(n_groups)
    w = 0.8 / max(n_series, 1)
    colors = theme["colors"]
    horizontal = kwargs.get("horizontal", False)
    use_hatch = kwargs.get("hatch", False)
    show_ratio = kwargs.get("show_ratio", False)
    ratio_base = kwargs.get("ratio_base", 0)  # index of base series for ratio

    error_data = data.get("errors", {})
    significance = data.get("significance", {})

    bar_func = ax.barh if horizontal else ax.bar
    all_bars = []  # store for ratio calculation

    for i, (name, values) in enumerate(series.items()):
        offset = (i - (n_series - 1) / 2) * w
        errs = None
        if name in error_data and error_data[name]:
            errs = error_data[name]
            if isinstance(errs, list) and all(isinstance(e, (int, float)) for e in errs):
                pass  # per-bar error
            elif isinstance(errs, (int, float)):
                errs = [errs] * n_groups

        hatch_val = HATCH_PATTERNS[i % len(HATCH_PATTERNS)] if use_hatch else None
        # v7.5 --arena 基准对比竞技场风格（单系列竖向 bar）：per-bar 异质填充循环
        # （灰实心/橙白斜线/蓝白点纹）+冠军柱实心深青绿+金色皇冠+数值高亮。
        arena = kwargs.get("arena")
        if isinstance(arena, str) and arena.strip().lower() == "off":
            arena = None  # v7.7 --arena off 显式逃生门（负面指标最高=最差，自动皇冠失义）
        _auto_arena = False
        if arena is None and kwargs.get("arena_default") and n_series == 1 \
                and len(values) >= 2 and not kwargs.get("alternate") \
                and not kwargs.get("horizontal"):
            arena = "auto"; _auto_arena = True  # v7.7 默认竞技场（默认输出=最佳输出第二期）
        _aci = None
        if arena and n_series == 1:
            if horizontal:
                print("[ignored] --arena 仅支持竖向 bar（横向模式本次忽略）", file=sys.stderr)
                arena = None
            else:
                _vals_f = [float(v) for v in values]
                if str(arena) == "auto":
                    _aci = max(range(len(_vals_f)), key=lambda k: _vals_f[k])
                else:
                    _aci = next((k for k, lb in enumerate(labels)
                                 if " ".join(str(lb).split()) == " ".join(str(arena).split())), None)
                    if _aci is None:
                        print(f"[ignored] --arena {arena} 未匹配类别标签，自动选最高柱",
                              file=sys.stderr)
                        _aci = max(range(len(_vals_f)), key=lambda k: _vals_f[k])
                def _is_base(k):
                    return any(w in str(labels[k]).lower() for w in _ARENA_BASELINE_KW)
                _ci = [k for k in range(len(_vals_f)) if k != _aci and not _is_base(k)]
                bar_colors = []
                for k in range(len(_vals_f)):
                    if k == _aci:
                        bar_colors.append(_ARENA_CHAMP)
                    elif _is_base(k):
                        bar_colors.append(_ARENA_BASE)
                    else:
                        bar_colors.append(_ARENA_FILL[_ci.index(k) % 3])
                print(f"[arena] 冠军={_labels_short(labels[_aci])}"
                      f"（{'默认竞技场风格；负面指标请 --arena off' if _auto_arena else '--arena'}）",
                      file=sys.stderr)
                if str(arena) == "auto" and _is_base(_aci):
                    print(f"[arena] 冠军为基线项 {_labels_short(labels[_aci])}"
                          "——若非预期请 --arena \"名称\" 指定冠军或 --arena off",
                          file=sys.stderr)
        elif arena:
            print("[ignored] --arena 仅单系列 bar 生效（多系列已忽略）", file=sys.stderr)
        # v3.10 单系列视觉增强（真金链路反馈"默认出图朴素"）：
        # ①Top-N 强调层级——最大条(含并列)主题主色，其余同色淡化（focus+context）
        # ②斜纹豁免——斜纹是"系列区分"工具，单系列铺满=噪声
        # ③图例抑制——单系列图例=系列名复读（label 不设，图例自然消失）
        _single_enh = (n_series == 1 and len(values) >= 3
                       and not kwargs.get("alternate", False))
        if arena and n_series == 1:
            pass  # --arena：bar_colors 已在上方 arena 块赋值（per-bar 循环+冠军）
        elif kwargs.get("alternate", False) and n_series == 1:
            # GLM-5.2 blog style: alternate first two theme colors per bar
            bar_colors = [colors[j % 2] for j in range(len(values))]
        elif _single_enh:
            from matplotlib.colors import to_rgba
            _vals = [float(v) for v in values]
            _vmax = max(_vals)
            _accent = colors[i % len(colors)]
            _muted = to_rgba(_accent, 0.42)
            bar_colors = [_accent if abs(v - _vmax) < 1e-12 else _muted for v in _vals]
            _is_brand = isinstance(theme, dict) and theme.get("hatch_edge") == "auto"
            if use_hatch and not _is_brand:
                hatch_val = None  # 单系列斜纹豁免（v3.10：斜纹=系列区分工具；glm-brand 不豁免）
                print("[ignored] --hatch 单系列已豁免斜纹（系列区分工具；"
                      "--style glm-brand 不豁免）", file=sys.stderr)
        else:
            bar_colors = colors[i % len(colors)]
        if arena and n_series == 1 and _aci is not None:
            bars = bar_func(x + offset, values, w * 0.78, yerr=errs, color=bar_colors,
                            edgecolor="white",
                            linewidth=[0.5 if (k == _aci or any(w in str(labels[k]).lower() for w in _ARENA_BASELINE_KW)) else 1.4 for k in range(len(values))],
                            hatch=[None if (k == _aci or any(w in str(labels[k]).lower() for w in _ARENA_BASELINE_KW))
                                   else _ARENA_HATCH[_ci.index(k) % 3]
                                   for k in range(len(values))],
                            capsize=3, error_kw={'linewidth': 1})
            _ys = ax.get_ylim()[1] - ax.get_ylim()[0]
            _draw_crown(ax, bars[_aci], max(float(v) for v in values), yspan=_ys)
            _top = ax.get_ylim()[1]
            ax.set_ylim(top=_top + _ys * 0.22)  # 皇冠全域（冠顶=y0+0.178span，0.22 留裕量）
        elif use_hatch and not (n_series == 1 and hatch_val is None):
            # GLM-5.2 blog style: ALL bars get hatching. glm-brand: 同系深色纹+边
            #（视觉精修）；其他主题保持黑色纹（历史行为）。
            bars = bar_func(x + offset, values, w, yerr=errs,
                            color=bar_colors,
                            edgecolor=_hatch_edgecolor(theme, bar_colors), linewidth=0.6,
                            hatch=hatch_val, capsize=3,
                            error_kw={'linewidth': 1},
                            label=name if n_series > 1 else None)
        else:
            bars = bar_func(x + offset, values, w, yerr=errs,
                            color=bar_colors, edgecolor='white', linewidth=0.5,
                            capsize=3, error_kw={'linewidth': 1},
                            label=name if n_series > 1 else None)
        if _SKETCH_MODE[0]:
            # v7.7.1 缺陷修复：xkcd 路径抖动会把柱体白色描边随机位移切入自身/邻柱
            # 填充（视觉门实锤白楔缺口，且抖动无种子=随机逃逸）——sketch 模式柱体
            # 补丁一律禁用路径抖动走直边（手绘感保留在轴线/网格/字体/皇冠）。
            for _p in getattr(bars, "patches", []):
                _p.set_sketch_params(None)
        all_bars.append((name, values, bars, offset))

        # v4.2 --peak-label：最大值点自动注记（数据事实，单/多系列均取全局峰）
        if kwargs.get("peak_label", False) and i == n_series - 1:
            _gl = next(iter(series))  # 全局峰所在系列
            _best, _bv = None, None
            for _n, _vals in series.items():
                for _j, _v in enumerate(_vals):
                    if _bv is None or float(_v) > _bv:
                        _best, _bv = (_n, _j), float(_v)
            if _best is not None:
                _annotate_peak(ax, list(range(len(labels))), labels, series[_best[0]],
                               horizontal, theme, cjk_fp,
                               series_name=_best[0] if n_series > 1 else None)

        # Value labels on bars
        if kwargs.get("show_values", False):
            for j, v in enumerate(values):
                err = errs[j] if errs and j < len(errs) else 0
                _fv = _fmt_series_value(v, values)
                _champ = bool(arena and n_series == 1 and j == _aci)
                if _champ:
                    _vc, _fw = _ARENA_CHAMP, 'bold'
                elif _SKETCH_MODE[0]:
                    _vc, _fw = "#222222", 'bold'  # sketch 手绘风：数值黑粗（参考图口径）
                else:
                    _vc, _fw = colors[i % len(colors)], 'bold' if _champ else 'normal'
                _fs = 10 if _SKETCH_MODE[0] else 7
                if horizontal:
                    ax.text(v + err + max(values) * 0.01, x[j] + offset,
                            _fv, ha='left', va='center', fontsize=_fs,
                            color=_vc, fontweight=_fw)
                else:
                    ax.text(x[j] + offset, v + err + max(values) * 0.01,
                            _fv, ha='center', va='bottom', fontsize=_fs,
                            color=_vc, fontweight=_fw)

    # Ratio annotations (e.g., "4.96x" above second series bars)
    if show_ratio and n_series >= 2:
        base_name = list(series.keys())[ratio_base]
        base_values = list(series.values())[ratio_base]
        for i, (name, values, bars, offset) in enumerate(all_bars):
            if i == ratio_base:
                continue
            for j, v in enumerate(values):
                bv = base_values[j] if j < len(base_values) else 0
                if bv != 0:
                    ratio = v / bv
                    ratio_str = f'{ratio:.2f}x' if ratio >= 1 else f'{ratio:.2f}x'
                    ratio_color = '#D55E00'
                    if horizontal:
                        ax.text(v + max(values) * 0.02, x[j] + offset,
                                ratio_str, ha='left', va='center', fontsize=8,
                                fontweight='bold', color=ratio_color)
                    else:
                        ax.text(x[j] + offset, v + max(values) * 0.02,
                                ratio_str, ha='center', va='bottom', fontsize=8,
                                fontweight='bold', color=ratio_color)

    # Significance brackets
    if significance:
        for key, label in significance.items():
            parts = key.split(":")
            if len(parts) == 2:
                grp_idx = int(parts[1])
            else:
                grp_idx = int(parts[0])
            if horizontal:
                x_top = ax.get_xlim()[1] * 0.95
                y_pos = x[grp_idx]
                fc = '#C0392B' if label not in ('NS', 'ns') else 'gray'
                fw = 'bold' if label not in ('NS', 'ns') else 'normal'
                ax.annotate(label, (x_top, y_pos), ha='left', va='center',
                            fontsize=8, fontweight=fw, color=fc)
            else:
                y_top = ax.get_ylim()[1] * 0.95
                fc = '#C0392B' if label not in ('NS', 'ns') else 'gray'
                fw = 'bold' if label not in ('NS', 'ns') else 'normal'
                ax.annotate(label, (x[grp_idx], y_top), ha='center', va='bottom',
                            fontsize=8, fontweight=fw, color=fc)

    if horizontal:
        y_fs = theme["font_size"] - 1
        if len(labels) > 12:
            y_fs -= 1
        ax.set_yticks(x)
        ax.set_yticklabels(labels, fontsize=y_fs,
                           fontproperties=cjk_fp if cjk_fp and any(has_cjk(l) for l in labels) else None)
        ax.invert_yaxis()
    else:
        max_lbl_len = max((len(str(l)) for l in labels), default=0)
        rotation = 0 if _SKETCH_MODE[0] else (45 if (len(labels) > 8 or max_lbl_len > 12) else 0)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=theme["font_size"] - 1,
                           rotation=rotation, ha='right' if rotation else 'center',
                           fontproperties=cjk_fp if cjk_fp and any(has_cjk(l) for l in labels) else None)


def gen_heatmap(data, ax, theme, cjk_fp, **kwargs):
    """Heatmap with text annotations."""
    matrix = data.get("matrix", data.get("data", data.get("values", None)))
    if matrix is None:
        # Fallback: build matrix from series (C2 fix — CSV heatmap support)
        series = data.get("series", {})
        if series:
            matrix = np.array(list(series.values()))
        else:
            matrix = np.array([])
    else:
        matrix = np.array(matrix)
    row_labels = data.get("row_labels", data.get("y_labels", data.get("rows", data.get("labels", []))))
    col_labels = data.get("col_labels", data.get("x_labels", data.get("cols", list(data.get("series", {}).keys()))))
    cmap = kwargs.get("cmap") or "RdBu_r"
    vmin = kwargs.get("vmin", None)
    vmax = kwargs.get("vmax", None)
    annot_fmt = kwargs.get("annot_format", "{:+.1f}")

    if matrix.size == 0:
        raise ValueError("heatmap: matrix is empty — provide 'matrix' (2D list) or 'series'")
    ax._af_category_axis = True  # 行列标签是数据：豁免 fix_tick_overlaps 降级

    has_neg = bool((matrix < 0).any())
    # Data-driven default: all-positive data uses a warm sequential colormap
    # (YlOrRd) — RdBu_r's white midpoint makes low positive values look like
    # a "broken band" (断层). Diverging colormaps are only sensible when the
    # data actually spans negative values.
    if cmap == "RdBu_r" and not has_neg and kwargs.get("cmap") is None:
        cmap = "YlOrRd"

    if vmin is None or vmax is None:
        if has_neg:
            abs_max = max(abs(matrix.min()), abs(matrix.max()))
            vmin = vmin if vmin is not None else -abs_max
            vmax = vmax if vmax is not None else abs_max
        else:
            vmin = vmin if vmin is not None else float(matrix.min())
            vmax = vmax if vmax is not None else float(matrix.max())

    # v7.9.1 AF40：定性色阶承载数值标度 → 提示（--discrete 才是正解）
    _cmap_name = str(kwargs.get("cmap") or ("RdBu_r" if has_neg else "YlOrRd"))
    if _cmap_name.split("_r")[0] in _QUALITATIVE_CMAPS and not kwargs.get("discrete"):
        print(f"NOTICE: 定性色阶 {_cmap_name} 用于数值标度——colorbar 语义易误读；"
              f"有序离散数据请加 --discrete（阶梯映射+离散色标）", file=sys.stderr)

    # v7.9.1 AF43：--discrete 离散映射（ListedColormap 采样+BoundaryNorm，colorbar 同步离散）
    _norm = None
    if kwargs.get("discrete"):
        from matplotlib.colors import BoundaryNorm
        _nd = min(max(int(np.ptp(matrix)) + 1, 2), 9)
        _bounds = np.linspace(float(vmin), float(vmax), _nd + 1)
        cmap = plt.get_cmap(cmap, _nd)
        _norm = BoundaryNorm(_bounds, cmap.N)
        im = ax.imshow(matrix, cmap=cmap, norm=_norm, aspect='auto')
    else:
        im = ax.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')

    # v7.9.1 AF44：--cell-edge 格线描边（低对比色阶下保结构；edge 色随底色明暗自动取反；
    # imshow 不支持 edgecolors——以半整数边界 axvline/axhline 画格线）
    if kwargs.get("cell_edge"):
        _cm_probe = im.cmap
        _ec = "#ffffff" if cell_text_color(_cm_probe(0.55)) == "#ffffff" else "#777777"
        for _x in np.arange(0.5, matrix.shape[1] - 0.5, 1.0):
            ax.axvline(_x, color=_ec, lw=0.6, zorder=3)
        for _y in np.arange(0.5, matrix.shape[0] - 0.5, 1.0):
            ax.axhline(_y, color=_ec, lw=0.6, zorder=3)

    # v7.9.1 AF6+AF32/AF6b：格内数值=密度门控+按格底色亮度反色
    # （原=无条件逐格绘制+9pt 死硬+按数值阈值判黑白——大矩阵必然压字、暗底黑字隐形）
    _nr, _nc = matrix.shape[0], matrix.shape[1]
    annot_mode = str(kwargs.get("annot") or "auto").strip().lower()
    if annot_mode not in ("on", "off", "auto"):
        annot_mode = "auto"
    if annot_mode == "auto" and (_nr > 30 or _nc > 30):
        annot_mode = "off"
        print(f"NOTICE: 矩阵 {_nr}x{_nc} 过密——格内数值已自动隐藏"
              f"（--annot on 可强制；或 cluster_heatmap --downsample 改数据）", file=sys.stderr)
    if annot_mode != "off":
        _afs = 9 if max(_nr, _nc) <= 15 else (7 if max(_nr, _nc) <= 30 else 6)
        for i in range(_nr):
            for j in range(_nc):
                v = matrix[i, j]
                _face = im.cmap(im.norm(v))
                ax.text(j, i, annot_fmt.format(v), ha='center', va='center',
                        fontsize=_afs, fontweight='bold',
                        color=cell_text_color(_face))

    ax.set_xticks(range(len(col_labels)))
    use_cjk_cols = cjk_fp and any(has_cjk(l) for l in col_labels)
    max_col_len = max((len(str(l)) for l in col_labels), default=0)
    rot = 45 if (len(col_labels) > 6 or max_col_len > 14) else 0
    ax.set_xticklabels(col_labels, fontsize=theme["font_size"] - 2,
                       rotation=rot, ha='right' if rot else 'center',
                       fontproperties=cjk_fp if use_cjk_cols else None)
    ax.set_yticks(range(len(row_labels)))
    use_cjk_rows = cjk_fp and any(has_cjk(l) for l in row_labels)
    ax.set_yticklabels(row_labels, fontsize=theme["font_size"],
                       fontproperties=cjk_fp if use_cjk_rows else None)

    return im  # for colorbar


def gen_scatter(data, ax, theme, cjk_fp, **kwargs):
    """Scatter plot with optional trend line and grouping."""
    x_data = np.array(data.get("x", data.get("xs", [])))
    y_data = np.array(data.get("y", data.get("ys", [])))
    groups = data.get("groups", data.get("colors", None))

    _raster = len(x_data) > 50000  # v7.8.0 A10：>50K 点数据层栅格化（轴/文字保矢量）
    if _raster:
        print("[rasterized] 数据点 >50K——散点数据层已栅格化（坐标轴/文字保持矢量，"
              "控制 PDF/SVG 体积；与 cluster_heatmap --downsample 互补：一个改渲染层一个改数据）",
              file=sys.stderr)
    if groups is None:
        ax.scatter(x_data, y_data, s=60 if not _raster else 12,
                   rasterized=_raster, color=theme["colors"][0],
                   edgecolors='white', linewidth=0.5, alpha=0.7, zorder=3)
    else:
        # Validate groups length matches x/y data length
        n = min(len(x_data), len(y_data))
        if len(groups) > n:
            groups = groups[:n]
        unique_groups = list(dict.fromkeys(groups))  # preserve order
        for i, g in enumerate(unique_groups):
            mask = [j for j in range(len(groups)) if groups[j] == g]
            c = theme["colors"][i % len(theme["colors"])]
            ax.scatter(x_data[mask], y_data[mask], s=60 if not _raster else 12,
                       rasterized=_raster, c=c,
                       edgecolors='white', linewidth=0.5, alpha=0.7,
                       label=g, zorder=3)

    # Point labels (data["labels"] — one per (x, y) point)
    point_labels = data.get("labels", [])
    if point_labels and len(point_labels) == len(x_data):
        use_cjk = cjk_fp and any(has_cjk(str(l)) for l in point_labels)
        n_pts = len(x_data)
        for i, (xi, yi, lab) in enumerate(zip(x_data, y_data, point_labels)):
            # Alternate above/below to keep neighbors readable; offset grows
            # with index so clustered points (e.g. years 1950/1953/1955) don't collide.
            row = i // 2  # every other point flips side
            dy = 10 + 3 * row if i % 2 == 0 else -13 - 3 * row
            ax.annotate(str(lab), xy=(xi, yi), xytext=(0, dy),
                        textcoords='offset points', fontsize=6.5,
                        ha='center', va='center', zorder=5,
                        fontproperties=cjk_fp if use_cjk else None,
                        color='#444444', alpha=0.9)

    # Trend line
    if kwargs.get("trend", True) and len(x_data) >= 3:
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        x_line = np.linspace(x_data.min(), x_data.max(), 100)
        ax.plot(x_line, p(x_line), '--', color='gray', alpha=0.6, linewidth=1.2,
                zorder=2, label='Linear trend')
        r = np.corrcoef(x_data, y_data)[0, 1]
        ax.text(0.95, 0.05, f'r = {r:.3f}', transform=ax.transAxes,
                ha='right', va='bottom', fontsize=9, fontstyle='italic', color='gray',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='lightgray'))

    # Mean points
    if groups and kwargs.get("show_mean", False):
        unique_groups = list(dict.fromkeys(groups))
        for i, g in enumerate(unique_groups):
            mask = [j for j in range(len(groups)) if groups[j] == g]
            mx, my = np.mean(x_data[mask]), np.mean(y_data[mask])
            c = theme["colors"][i % len(theme["colors"])]
            ax.scatter(mx, my, s=150, c=c, edgecolors='black', linewidth=1.2,
                       marker='o', zorder=4)

    ax.xaxis.grid(True, alpha=theme["grid_alpha"], linestyle='--')


def gen_line(data, ax, theme, cjk_fp, **kwargs):
    """Line chart with optional error bands."""
    labels = data.get("labels", data.get("x", []))
    series = data.get("series", data.get("datasets", {}))
    error_data = data.get("errors", {})
    markers = ['o', 's', 'D', '^', 'v', 'p', '*', 'h', '+', 'x']

    x = np.arange(len(labels)) if not any(isinstance(l, (int, float)) for l in labels) else np.array(labels)

    _line_ends = []  # v3.4 直接标注收集器
    for i, (name, values) in enumerate(series.items()):
        c = theme["colors"][i % len(theme["colors"])]
        mk = markers[i % len(markers)]
        lw = kwargs.get("linewidth", 2)
        ax.plot(x, values, c=c, marker=mk, markersize=6, linewidth=lw, label=name, zorder=3)

        # Error band/fill
        if name in error_data and error_data[name]:
            errs = error_data[name]
            if isinstance(errs, list) and len(errs) == len(values):
                lower = [v - e for v, e in zip(values, errs)]
                upper = [v + e for v, e in zip(values, errs)]
                ax.fill_between(x, lower, upper, color=c, alpha=0.15, zorder=2)
        if kwargs.get("direct_label"):
            _line_ends.append((str(name), values[-1], c))

    # ── v3.4：直接标注（线末端系列名，自动上下避让，替代图例框）──
    if kwargs.get("direct_label") and _line_ends:
        _span = (max(v for _, v, _ in _line_ends) - min(v for _, v, _ in _line_ends)) or 1.0
        _gap = _span * 0.08
        _order = sorted(range(len(_line_ends)), key=lambda i: _line_ends[i][1])
        _adj = {i: _line_ends[i][1] for i in _order}
        for _a, _b in zip(_order, _order[1:]):
            if _adj[_b] - _adj[_a] < _gap:
                _adj[_b] = _adj[_a] + _gap
        _x_span = (max(x) - min(x)) or 1.0
        ax.set_xlim(right=max(x) + _x_span * 0.22)
        _any_cjk = cjk_fp and any(has_cjk(n) for n, _, _ in _line_ends)
        for _i, (_name, _v, _c) in enumerate(_line_ends):
            ax.annotate(_name, xy=(max(x) + _x_span * 0.03, _adj[_i]),
                        textcoords="data", color=_c, fontweight="bold",
                        fontsize=theme["font_size"] - 1, va="center", ha="left",
                        fontproperties=cjk_fp if _any_cjk else None,
                        annotation_clip=False)

    # ── v4.2 --peak-label：全局最大值点注记（数据事实）──
    if kwargs.get("peak_label") and series:
        _best_n, _best_i = None, None
        for _n, _vals in series.items():
            for _j, _v in enumerate(_vals):
                if _best_i is None or float(_v) > float(_best_v):
                    _best_n, _best_i, _best_v = _n, _j, _v
        _annotate_peak(ax, list(x), labels, series[_best_n], False, theme, cjk_fp,
                       series_name=_best_n if len(series) > 1 else None)

    ax.set_xticks(x if not any(isinstance(l, (int, float)) for l in labels) else range(len(labels)))
    if not any(isinstance(l, (int, float)) for l in labels):
        use_cjk = cjk_fp and any(has_cjk(l) for l in labels)
        rot = 45 if len(labels) > 10 else 0
        ax.set_xticklabels(labels, fontsize=theme["font_size"] - 1,
                           rotation=rot, ha='right' if rot else 'center',
                           fontproperties=cjk_fp if use_cjk else None)


def gen_box(data, ax, theme, cjk_fp, **kwargs):
    """Box plot with optional jitter points."""
    labels = data.get("labels", data.get("x", []))
    series = data.get("series", data.get("datasets", {}))

    positions = list(range(len(series)))
    # v4.5 P2-5/R2-9：null/None 跳过并计数（兑现"非数值项画图时会跳过"的警告承诺）
    _clean = {}
    _dropped = 0
    for _n, _vals in series.items():
        _c = [v for v in _vals if v is not None]
        if len(_c) != len(_vals):
            _dropped += len(_vals) - len(_c)
            print(f"WARNING: box: 系列 '{_n}' 跳过 {len(_vals) - len(_c)} 个 null 值",
                  file=sys.stderr)
        _clean[_n] = _c
    series = _clean
    bp = ax.boxplot(list(series.values()), positions=positions, widths=0.5,
                    patch_artist=True, showfliers=False)

    for i, (patch, name) in enumerate(zip(bp['boxes'], series.keys())):
        patch.set_facecolor(theme["colors"][i % len(theme["colors"])])
        patch.set_alpha(0.6)

    # Jitter points
    rng = np.random.default_rng(42)
    for i, (name, values) in enumerate(series.items()):
        vals = np.array(values, dtype=float)
        jitter_x = positions[i] + rng.normal(0, 0.06, len(vals))
        c = theme["colors"][i % len(theme["colors"])]
        ax.scatter(jitter_x, vals, s=18, c=c, alpha=0.5, zorder=3, edgecolors='none')

    ax.set_xticks(positions)
    use_cjk = cjk_fp and any(has_cjk(l) for l in series.keys())
    ax.set_xticklabels(list(series.keys()), fontsize=theme["font_size"] - 1,
                       fontproperties=cjk_fp if use_cjk else None)

    if kwargs.get("stats_multi"):
        annotate_multi_stats(ax, series, positions, theme, "box")
    elif kwargs.get("stats_auto"):
        annotate_auto_stats(ax, series, positions, theme, "box")
    elif kwargs.get("stats_bootstrap"):
        annotate_bootstrap_stats(ax, series, positions, theme, "box")


def gen_forest(data, ax, theme, cjk_fp, **kwargs):
    """Forest plot for meta-analysis with weights, heterogeneity, and events."""
    ax._af_category_axis = True  # 研究名 y 轴是数据：豁免防重叠抽稀（与热图同机制）
    labels = data.get("labels", data.get("studies", []))
    estimates = data.get("estimates", data.get("values", []))
    ci_low = data.get("ci_low", data.get("lower", []))
    ci_high = data.get("ci_high", data.get("upper", []))
    weights = data.get("weights", None)  # Study weights for bubble size
    overall = data.get("overall", None)
    measure = data.get("measure", "OR")  # Effect measure label: OR, RR, HR, MD, SMD
    # v2.6.0 审核修复：缺省无效线按效应尺度自动取值——比率尺度（OR/RR/HR）无效线
    # 是 1.0，差值尺度（MD/SMD）是 0.0；旧默认恒取 0 会把自然尺度 OR/HR 的
    # "CI 是否跨过 1"画错位置，误导显著性判读。显式 ref_line 永远优先。
    ref_line = data.get("ref_line", None)
    if ref_line is None:
        ref_line = 0.0 if str(measure).upper() in ("MD", "SMD") else 1.0
        print(f"forest: 未指定 ref_line，按效应尺度 {measure} 自动取无效线 {ref_line:g}"
              f"（log 尺度数据请显式传 ref_line=0）", file=sys.stderr)
    heterogeneity = data.get("heterogeneity", None)  # {"Q": float, "df": int, "I2": float, "p": float}
    events = data.get("events", None)  # [{"events": int, "total": int}, ...] per study
    use_hatch = kwargs.get("hatch", False)

    # ── v2.4.0：留一法敏感性分析（--sensitivity）──
    if kwargs.get("sensitivity") and _afstats is not None:
        se_per_study = data.get("se_list", data.get("ses", None))
        if se_per_study is None and len(ci_low) == len(ci_high) == len(estimates) and len(estimates) >= 4:
            se_per_study = [(float(h) - float(l)) / 3.92
                            for l, h in zip(ci_low, ci_high)]
            print("WARNING: forest: --sensitivity 由 95%CI 反推 se（近似 (hi-lo)/3.92）；"
                  "有精确 se 请在数据提供 se_list", file=sys.stderr)
        loo = None
        if se_per_study is None or len(se_per_study) != len(estimates):
            print("WARNING: forest: --sensitivity 需要 se_list 或可反推的对称 CI，已跳过",
                  file=sys.stderr)
        else:
            try:
                loo = _afstats.leave_one_out(estimates, se_per_study)
            except ValueError as e:
                print(f"WARNING: forest: 留一法无法计算：{e}", file=sys.stderr)
        if loo:
            for gi, (omi, pooled, plo, phi) in enumerate(loo):
                y = -(gi + 2)
                ax.plot([plo, phi], [y, y], color="#888888", lw=1.4, zorder=3)
                ax.scatter([pooled], [y], s=46, marker="D",
                           color=theme["colors"][1 % len(theme["colors"])],
                           edgecolor="#5B6770", linewidth=0.8, zorder=4)
                _lbl = (labels[omi] if isinstance(labels, list) and omi < len(labels)
                        else f"Study {omi+1}")
                ax.text(-0.02, y, f"省略{_lbl}", transform=ax.get_yaxis_transform(),
                        ha="right", va="center",
                        fontsize=max(6, theme["font_size"] - 1),
                        fontproperties=cjk_fp if cjk_fp and has_cjk(str(_lbl)) else None,
                        color="#555555")
            ax.axhline(-1.2, color="#CCCCCC", lw=0.8, linestyle="--")
            ax.text(-0.02, -1.55, "留一法敏感性分析（省略单研究后的随机效应合并）",
                    transform=ax.get_yaxis_transform(), ha="right", va="center",
                    fontsize=max(6.5, theme["font_size"] - 1),
                    fontproperties=cjk_fp if cjk_fp and has_cjk("留一") else None,
                    color="#8a6414")
            ax.set_ylim(-(len(loo) + 3.2), None)
            print(f"forest: 留一法敏感性分析 {len(loo)} 组已绘制（可见性依赖各研究效应单位一致）",
                  file=sys.stderr)

    n_studies = len(labels)
    y_pos = list(range(n_studies))

    # Calculate weight-based bubble sizes if weights provided
    if weights and len(weights) == n_studies:
        w_arr = np.array(weights, dtype=float)
        w_min, w_max = w_arr.min(), w_arr.max()
        if w_max > w_min:
            bubble_sizes = 40 + (w_arr - w_min) / (w_max - w_min) * 160  # 40-200 range
        else:
            bubble_sizes = np.full(n_studies, 80.0)
    else:
        bubble_sizes = np.full(n_studies, 80.0)

    # Column layout: leave space for events column on left
    plot_x_start = 0.0
    events_col_x = None
    if events and len(events) == n_studies:
        events_col_x = -0.3  # Relative position in axes coords, handled via text

    for i, (est, lo, hi) in enumerate(zip(estimates, ci_low, ci_high)):
        # CI whisker line
        ax.plot([lo, hi], [i, i], '-', color=theme["colors"][0], linewidth=1.5, zorder=2)
        # Weighted point estimate (bubble)
        ax.scatter(est, i, c=theme["colors"][0], s=bubble_sizes[i], zorder=3,
                   edgecolors='black', linewidth=0.5)
        # Effect estimate annotation on right（v7.8.1 AF11：CI 自适应小数位防 1.00 误读）
        _re_s, _rl_s, _rh_s, _ = fmt_ratio_ci(est, lo, hi, str(measure))
        ax.text(hi + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.02, i,
                f'{_re_s} [{_rl_s}, {_rh_s}]', va='center', fontsize=8)
        # Events/Total on left (if provided)
        if events and i < len(events):
            ev = events[i]
            ev_str = f"{ev.get('events', '?')}/{ev.get('total', '?')}" if isinstance(ev, dict) else str(ev)
            ax.annotate(ev_str, xy=(0, 0), xytext=(-0.15, i),
                        textcoords=('axes fraction', 'data'),
                        ha='right', va='center', fontsize=7, color='#555555')

    # Reference line
    ax.axvline(x=ref_line, color='gray', linestyle='--', linewidth=1, alpha=0.6)

    # Separator line before overall
    if overall:
        ax.axhline(y=n_studies - 0.5, color='#333333', linewidth=0.8, alpha=0.5)

    # Overall diamond
    if overall:
        oy = n_studies
        est_o = overall["estimate"]
        lo_o = overall["ci_low"]
        hi_o = overall["ci_high"]
        diamond_x = [lo_o, est_o, hi_o, est_o, lo_o]
        diamond_y = [oy, oy - 0.2, oy, oy + 0.2, oy]
        ax.fill(diamond_x, diamond_y, color=theme["colors"][1], alpha=0.7, zorder=4,
                hatch=HATCH_PATTERNS[1] if use_hatch else None)
        _oe, _ol, _oh, _osig = fmt_ratio_ci(est_o, lo_o, hi_o, str(measure))
        _onull = '1' if str(measure).upper() in ('RR', 'OR', 'HR') else '0'
        _osfx = f'（不含 {_onull}）' if _osig else ''
        ax.text(hi_o + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.02, oy,
                f'Overall: {_oe} [{_ol}, {_oh}]{_osfx}', va='center',
                fontsize=9, fontweight='bold')

    # Heterogeneity annotation
    if heterogeneity:
        i2 = heterogeneity.get("I2", None)
        q_val = heterogeneity.get("Q", None)
        df_val = heterogeneity.get("df", None)
        p_val = heterogeneity.get("p", None)
        parts = []
        if i2 is not None:
            parts.append(f"I² = {i2:.1f}%")
        if q_val is not None and df_val is not None:
            parts.append(f"Q = {q_val:.2f}, df = {df_val}")
        if p_val is not None:
            parts.append(f"p = {p_val:.3f}" if p_val >= 0.001 else f"p < 0.001")
        if parts:
            het_text = "Heterogeneity: " + "; ".join(parts)
            ax.text(0.5, -0.12, het_text, transform=ax.transAxes,
                    ha='center', va='top', fontsize=7, fontstyle='italic', color='#555555')

    # X-axis label with measure type
    ax.set_xlabel(measure, fontsize=theme["font_size"])

    # Column header for events
    if events and len(events) > 0:
        ax.annotate("Events/Total", xy=(0, 0), xytext=(-0.15, -0.8),
                    textcoords=('axes fraction', 'data'),
                    ha='right', va='center', fontsize=7, fontweight='bold', color='#333333')

    all_labels = list(labels) + (["Overall"] if overall else [])
    ax.set_yticks(list(y_pos) + ([n_studies] if overall else []))
    use_cjk = cjk_fp and any(has_cjk(l) for l in all_labels)
    ax.set_yticklabels(all_labels, fontsize=theme["font_size"],
                       fontproperties=cjk_fp if use_cjk else None)
    ax.invert_yaxis()


def gen_violin(data, ax, theme, cjk_fp, **kwargs):
    """Violin plot with optional inner box and jitter points."""
    labels = data.get("labels", data.get("x", []))
    series = data.get("series", data.get("datasets", {}))

    positions = list(range(len(series)))
    values_list = list(series.values())

    vp = ax.violinplot(values_list, positions=positions, widths=0.6,
                       showmeans=kwargs.get("show_means", True),
                       showmedians=kwargs.get("show_medians", True),
                       showextrema=kwargs.get("show_extrema", True))

    # Color the violin bodies
    for i, body in enumerate(vp['bodies']):
        body.set_facecolor(theme["colors"][i % len(theme["colors"])])
        body.set_alpha(0.6)
        body.set_edgecolor(theme["colors"][i % len(theme["colors"])])
        body.set_linewidth(1)

    # Style internal lines
    for part in ['cmeans', 'cmedians', 'cmins', 'cmaxes', 'cbars']:
        if part in vp:
            vp[part].set_color('#333333')
            vp[part].set_linewidth(1)

    ax.set_xticks(positions)
    use_cjk = cjk_fp and any(has_cjk(l) for l in series.keys())
    ax.set_xticklabels(list(series.keys()), fontsize=theme["font_size"] - 1,
                       fontproperties=cjk_fp if use_cjk else None)

    if kwargs.get("stats_multi"):
        annotate_multi_stats(ax, series, positions, theme, "violin")
    elif kwargs.get("stats_auto"):
        annotate_auto_stats(ax, series, positions, theme, "violin")
    elif kwargs.get("stats_bootstrap"):
        annotate_bootstrap_stats(ax, series, positions, theme, "violin")


def _km_note_box(ax, text, cjk_fp=None):
    """KM 右上角注释框（log-rank/中位生存）：实测宽度自适应字号，
    保证不越出坐标区、不压 y 轴刻度；不透明底+高 zorder 防曲线横穿文字。"""
    fs = 8.0
    t = None
    for _ in range(7):
        if t is not None:
            t.remove()
        t = ax.text(0.97, 0.96, text, transform=ax.transAxes, ha="right", va="top",
                    fontsize=fs, fontstyle="italic", color="#333333", zorder=6,
                    fontproperties=cjk_fp if (cjk_fp and has_cjk(text)) else None,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=1.0,
                              edgecolor="lightgray"))
        fig = ax.figure
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        bb = t.get_window_extent(renderer=renderer)
        ax_bb = ax.get_window_extent(renderer=renderer)
        if bb.x0 >= ax_bb.x0 or fs <= 6.0:
            break
        fs -= 0.5
    return t


def gen_km(data, ax, theme, cjk_fp, **kwargs):
    """Kaplan-Meier 生存曲线（v2.3：自动风险表 + 自动 log-rank）。

    原始数据格式（每样本 [时间, 事件]）>=2 组时自动做 Mantel-Haenszel
    log-rank 检验并在图内标注；主图下方以独立坐标轴渲染"Number at risk"
    风险表（主流程经 --no-risk-table 可关闭，--risk-times 自定义显示时间点）。
    仍兼容：用户直接提供 risk_table/log_rank（优先采用，不重复计算）、
    预计算 survival 曲线格式（无原始数据时跳过自动统计并提示）。
    """
    groups = data.get("groups", data.get("series", {}))
    risk_table = data.get("risk_table", None)      # 兼容 v2.2 用户供表
    log_rank = data.get("log_rank", None)
    median_survival = data.get("median_survival", None)
    risk_axes = kwargs.get("risk_axes", None)
    want_risk = kwargs.get("risk_table", True)
    risk_times_arg = kwargs.get("risk_times", None)

    if isinstance(groups, dict):
        group_names = list(groups.keys())
    elif isinstance(groups, list):
        group_names = data.get("labels", [f"Group {i+1}" for i in range(len(groups))])
        groups = dict(zip(group_names, groups))
        bad = [g for g in groups.values()
               if not (isinstance(g, (list, tuple)) and
                       all(isinstance(p, (list, tuple)) and len(p) >= 2 and
                           all(isinstance(n, (int, float)) for n in p) for p in g) or
                       all(isinstance(n, (int, float)) for n in g))]
        if bad:
            raise ValueError(
                "km: unsupported 'groups' format. Expected {\"Group\": [[t, s], ...]} "
                "or [t1, t2, ...] per group — got object list like "
                "[{\"label\": ..., \"time\": ..., \"events\": ...}]. "
                "Convert to {\"组名\": [[t, s], ...]}.")
    else:
        group_names = []
        groups = {}

    raw_groups = {}     # 组名 -> (times, events)
    precomputed = False
    if not groups and "time" in data and "survival" in data:
        precomputed = True
        surv_data = data["survival"]
        cens_data = data.get("censored", {})
        group_names = list(surv_data.keys())
        for gname in group_names:
            t_arr = np.asarray(data["time"], dtype=float)
            s_arr = np.asarray(surv_data[gname], dtype=float)
            c_arr = np.asarray(cens_data.get(gname, [0] * len(s_arr)), dtype=float)
            c = theme["colors"][group_names.index(gname) % len(theme["colors"])]
            ax.step(t_arr, s_arr, where='post', color=c, linewidth=2, label=gname, zorder=3)
            _cm = (c_arr[:len(t_arr)] == 1)
            if _cm.any():
                ax.scatter(t_arr[:len(t_arr)][_cm], s_arr[:len(t_arr)][_cm],
                           marker='+', color=c, s=30, linewidth=1.5, zorder=4)
        if risk_axes is None or not want_risk:
            print("WARNING: km: 预计算 survival 格式无原始数据，无法自动计算风险表/"
                  "log-rank——请提供 {组: [[时间,事件], ...]} 原始格式", file=sys.stderr)
    else:
        for gname in group_names:
            raw = groups.get(gname, None)
            if not isinstance(raw, (list, tuple)) or len(raw) == 0:
                continue
            if isinstance(raw[0], (list, tuple)):
                times = np.array([p[0] for p in raw], dtype=float)
                second = np.array([p[1] for p in raw], dtype=float)
                # v3.7：竞争风险编码（整数且含 ≥2）优先于预计算判定——
                # 此前含 2 的原始数据被误当预计算生存概率静默绘制
                _is_int_code = np.all(second == np.floor(second)) and np.any(second >= 2)
                if np.all(np.isin(second, (0.0, 1.0))):
                    raw_groups[gname] = (times, second)   # [时间, 事件0/1]
                elif _is_int_code:
                    raw_groups[gname] = (times, second)   # [时间, 事件0/1/2+竞争风险]
                else:
                    # [时间, 预计算生存概率]：直接阶梯绘制（v2.2 曾误当事件数，
                    # 曲线数学错误；v2.3 起正确识别），不计入自动统计
                    c = theme["colors"][group_names.index(gname) % len(theme["colors"])]
                    ax.step(times, second, where='post', color=c, linewidth=2,
                            label=gname, zorder=3)
                    print(f"WARNING: km: '{gname}' 第二列为连续值，按预计算生存概率绘制"
                          "（无原始数据，跳过自动风险表/log-rank）", file=sys.stderr)
                continue
            times = np.array(raw, dtype=float)
            raw_groups[gname] = (times, np.ones(len(times)))

        # ── v3.7：竞争风险检测（任一组 events 含 ≥2 编码 → Aalen-Johansen CIF 模式）──
        _competing = any(
            np.any(np.asarray(ev) >= 2)
            for (_t, ev) in raw_groups.values() if len(ev) == len(_t))
        if _competing and _afstats is not None:
            _cn_src = data.get("cause_names") if isinstance(data, dict) else None
            _cause_names = _cn_src if isinstance(_cn_src, dict) else {}
            print("[auto] km: 检测到竞争风险事件编码（≥2）——切换 Aalen-Johansen "
                  "累计发生率曲线（每因一条）；单队列建议改用专用图型 -t cif"
                  "（含 1−KM 高估对照虚线与统计报告）", file=sys.stderr)
            for i, gname in enumerate(group_names):
                if gname not in raw_groups:
                    continue
                c = theme["colors"][i % len(theme["colors"])]
                times, events = raw_groups[gname]
                _aj = _afstats.aalen_johansen(times, events)
                for j, state in enumerate(sorted(_aj["cif"].keys())):
                    _cl = _cause_names.get(state) if isinstance(_cause_names, dict) else None
                    label = _cl or (f"{gname}·原因{state}" if state >= 2 else f"{gname}·目标事件")
                    ax.step(_aj["times"], _aj["cif"][state], where="post",
                            color=theme["colors"][(i * 3 + j) % len(theme["colors"])],
                            linewidth=2, label=label, zorder=3)
                _ttl = (kwargs.get("competing_title")
                        or f"{gname}: 累计发生率（Aalen-Johansen，竞争风险）")
                if i == 0:
                    ax.set_title(_ttl, fontsize=theme["font_size"],
                                 fontproperties=cjk_fp if cjk_fp and has_cjk(_ttl) else None)
            ax.set_ylabel("累计发生率 Cumulative Incidence",
                          fontsize=theme["font_size"] - 1,
                          fontproperties=cjk_fp if cjk_fp else None)
            return  # AJ 模式独立渲染，不走 KM 主循环

        for i, gname in enumerate(group_names):
            if gname not in raw_groups:
                continue
            c = theme["colors"][i % len(theme["colors"])]
            times, events = raw_groups[gname]
            if _afstats is not None:
                t_seq, s_seq, censor_pts = _afstats.km_estimate(times, events)
            else:
                order = np.argsort(times, kind="stable")
                ts, es = times[order], events[order]
                surv, t_seq, s_seq, censor_pts = 1.0, [0.0], [1.0], []
                n_risk = len(ts)
                for ut in np.unique(ts):
                    m = ts == ut
                    d = float(es[m].sum())
                    n_c = int(m.sum() - d)
                    if n_risk > 0 and d > 0:
                        surv *= 1 - d / n_risk
                    if n_c:
                        censor_pts.append((float(ut), surv))
                    t_seq.append(float(ut)); s_seq.append(surv)
                    n_risk -= int(m.sum())
            ax.step(t_seq, s_seq, where='post', color=c, linewidth=2, label=gname, zorder=3)
            if censor_pts:
                _cts, _css = zip(*censor_pts)
                ax.scatter(_cts, _css, marker='+', color=c, s=30, linewidth=1.5, zorder=4)
            if median_survival and gname in median_survival and median_survival[gname] is not None:
                ax.axvline(x=float(median_survival[gname]), color=c, linestyle=':',
                           alpha=0.4, linewidth=1)

    # 参考线（中位生存 0.5）
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)

    # ── 自动 log-rank（原始数据 >=2 组且用户未提供时）──
    if log_rank is None and len(raw_groups) >= 2 and _afstats is not None:
        try:
            chi2_v, p_lr, df_lr = _afstats.logrank_test(raw_groups)
            log_rank = {"p": p_lr, "method": "log-rank"}
            print(f"km: log-rank 检验：chi2={chi2_v:.3g}, df={df_lr}, p={p_lr:.4g}",
                  file=sys.stderr)
        except Exception as e:
            print(f"WARNING: km: log-rank 自动计算失败（{e}），跳过标注", file=sys.stderr)

    # ── 自动中位生存（原始数据组；用户传 median_survival 仍画竖线，互不冲突）──
    median_notes = []
    _med_ci = [0, 0]  # v6.4.0：[带CI组数, 显示数值组数]——CI 缺失时标签须降级
    if kwargs.get("median_auto", True) and raw_groups and _afstats is not None:
        for gname in group_names:
            if gname not in raw_groups or (median_survival and gname in median_survival):
                continue
            t_g, e_g = raw_groups[gname]
            try:
                med, clo, chi_ = _afstats.km_median_survival(t_g, e_g)
            except Exception:
                med = None
            if med is None:
                median_notes.append(f"{gname}: 未到达")
            elif len(t_g) < 2:
                # v4.5 R2-6：单例组不存在 95%CI（n=1 时 KM 中位=唯一时间），只报中位
                median_notes.append(f"{gname}: {med:g}（n=1，无CI）")
            else:
                if clo is not None and chi_ is not None:
                    median_notes.append(f"{gname}: {med:g}（{clo:g}~{chi_:g}）")
                    _med_ci[0] += 1
                else:
                    median_notes.append(f"{gname}: {med:g}")
                _med_ci[1] += 1
                if median_survival is None:
                    median_survival = {}
                median_survival.setdefault(gname, med)
        if median_notes:
            _ml = "中位生存（95%CI）" if _med_ci[1] > 0 and _med_ci[0] == _med_ci[1] else "中位生存"
            print("km: 自动" + _ml + "：" + "；".join(median_notes), file=sys.stderr)
        if log_rank is not None:
            method = log_rank.get("method", "log-rank")
            p_val = log_rank.get("p")
            try:
                p_val = float(p_val)
            except (ValueError, TypeError):
                p_val = 1.0
            p_str = f"p = {p_val:.3f}" if p_val >= 0.001 else "p < 0.001"
            sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else "NS"
            _box_lines = [f"{method} {p_str} {sig}" if sig else f"{method} {p_str}"]
            if median_notes:
                _ml = "中位生存（95%CI）" if _med_ci[1] > 0 and _med_ci[0] == _med_ci[1] else "中位生存"
                _box_lines.append(_ml)
                _box_lines += median_notes[:4]
            _km_note_box(ax, "\n".join(_box_lines), cjk_fp)
            median_notes = []
        if median_notes:
            _ml = "中位生存（95%CI）" if _med_ci[1] > 0 and _med_ci[0] == _med_ci[1] else "中位生存"
            _km_note_box(ax, _ml + "\n" + "\n".join(median_notes[:4]), cjk_fp)

    # ── 风险表（自动计算；独立坐标轴与主图共享 x 轴）──
    rendered = False
    if want_risk and raw_groups and risk_axes is not None and _afstats is not None:
        try:
            if risk_times_arg:
                if isinstance(risk_times_arg, str):
                    disp_times = [float(x) for x in risk_times_arg.split(",") if x.strip()]
                else:
                    disp_times = [float(x) for x in risk_times_arg]
            else:
                all_t = np.concatenate([t for t, _ in raw_groups.values()])
                disp_times = _afstats.default_risk_times(all_t, k=5)
            ax.set_xlim(left=0)
            x_max = ax.get_xlim()[1]
            rows = []
            for gname in group_names:
                if gname not in raw_groups:
                    continue
                t_g, e_g = raw_groups[gname]
                col = theme["colors"][group_names.index(gname) % len(theme["colors"])]
                rows.append((gname, _afstats.km_at_risk(t_g, e_g, disp_times), col))
            ra = risk_axes
            ra.set_xlim(0, x_max)
            ra.set_ylim(0, max(len(rows), 1))
            ra.invert_yaxis()
            for sp in ra.spines.values():
                sp.set_visible(False)
            ra.set_yticks([])
            ra.tick_params(axis="x", labelbottom=False, length=0)
            ra.grid(False)
            _hdr_txt = ("Number at risk（处于风险人数）"
                        if any(has_cjk(str(g)) for g, _, _ in rows) or bool(cjk_fp)
                        else "Number at risk")
            _fp_hdr = cjk_fp if cjk_fp and has_cjk(_hdr_txt) else None
            ra.text(0.0, -0.66, _hdr_txt,
                    fontsize=max(7, theme["font_size"] - 1), fontweight="bold",
                    color="#333333", ha="left", va="center", fontproperties=_fp_hdr,
                    clip_on=False)
            # 组名实测定位（修复组名与首列数字黏连）：右缘 = 首列数字左缘 - 间距
            ra.figure.canvas.draw()
            _renderer = ra.figure.canvas.get_renderer()
            _inv_data = ra.transData.inverted()
            _num_fs = max(6.5, theme["font_size"] - 1.5)
            _t0 = min(disp_times)
            _first_w = 0.0
            for _g, _counts, _c in rows:
                _p = ra.text(_t0, 0.5, str(_counts[0]), fontsize=_num_fs,
                             ha="center", va="center")
                _bb = _p.get_window_extent(renderer=_renderer).transformed(_inv_data)
                _first_w = max(_first_w, _bb.width)
                _p.remove()
            _name_right = _t0 - _first_w / 2 - x_max * 0.02
            for ri, (gname, counts, col) in enumerate(rows):
                y = ri + 0.5
                _fp_g = cjk_fp if cjk_fp and has_cjk(str(gname)) else None
                ra.text(_name_right, y, str(gname), fontsize=max(6.5, theme["font_size"] - 1.5),
                        color=col, ha="right", va="center", fontweight="bold",
                        fontproperties=_fp_g, clip_on=False)
                for t_v, cnt in zip(disp_times, counts):
                    if t_v <= x_max:
                        ra.text(t_v, y, str(cnt),
                                fontsize=max(6.5, theme["font_size"] - 1.5),
                                color="#333333", ha="center", va="center")
            rendered = True
        except Exception as e:
            print(f"WARNING: km: 自动风险表渲染失败（{e}）", file=sys.stderr)

    # ── 兼容 v2.2：用户直接提供 risk_table 且无自动表时的文本模式 ──
    if not rendered and risk_table and isinstance(risk_table, dict):
        rt_times = risk_table.get("times", [])
        ax.text(0.02, -0.08, "Number at risk", transform=ax.transAxes,
                fontsize=7, fontweight='bold', color='#333333')
        for i, gname in enumerate(group_names):
            c = theme["colors"][i % len(theme["colors"])]
            n_at = risk_table.get(gname, [])
            rt_str = "  ".join(str(n) for n in n_at)
            ax.text(0.02, -0.08 - (i + 1) * 0.04, f"{gname}: {rt_str}",
                    transform=ax.transAxes, fontsize=6, color=c)

    ax.set_ylim(-0.02, 1.02)
    ax.set_xlim(left=0)
    ax.xaxis.grid(True, alpha=theme["grid_alpha"], linestyle='--')


def gen_roc(data, ax, theme, cjk_fp, **kwargs):
    """ROC curve with AUC value, confidence interval, and optimal cutoff."""
    curves = data.get("curves", None)  # list of curve objects
    single_fpr = data.get("fpr", data.get("x", None))
    single_tpr = data.get("tpr", data.get("y", None))
    single_auc = data.get("auc", None)
    ci = data.get("ci", None)  # {"low": 0.82, "high": 0.94}
    cutoff = data.get("cutoff", None)  # {"fpr": 0.15, "tpr": 0.88, "threshold": 2.35}
    diagonal = data.get("diagonal", True)  # show diagonal reference line

    # Support single curve (fpr/tpr arrays) or multiple curves
    if curves is None and single_fpr is not None and single_tpr is not None:
        fpr_arr = np.array(single_fpr, dtype=float)
        tpr_arr = np.array(single_tpr, dtype=float)
        auc_val = single_auc

        # Compute AUC if not provided
        if auc_val is None:
            auc_val = np.trapezoid(tpr_arr, fpr_arr) if hasattr(np, 'trapezoid') else np.trapz(tpr_arr, fpr_arr)

        ax.plot(fpr_arr, tpr_arr, color=theme["colors"][0], linewidth=2.5, zorder=3,
                label=f'AUC = {auc_val:.3f}')

        # CI annotation
        if ci:
            ci_low = ci.get("low", ci.get("ci_low", None))
            ci_high = ci.get("high", ci.get("ci_high", None))
            if ci_low is not None and ci_high is not None:
                ax.text(0.95, 0.05, f'95% CI: [{ci_low:.3f}, {ci_high:.3f}]',
                        transform=ax.transAxes, ha='right', va='bottom',
                        fontsize=8, color='#555555',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor='lightgray'))

        # Optimal cutoff point
        if cutoff:
            co_fpr = cutoff.get("fpr", None)
            co_tpr = cutoff.get("tpr", None)
            co_thr = cutoff.get("threshold", None)
            if co_fpr is not None and co_tpr is not None:
                ax.scatter(co_fpr, co_tpr, color=theme["colors"][0], s=80, zorder=5,
                           edgecolors='black', linewidth=1, marker='o')
                label_parts = [f'Optimal cutoff']
                if co_thr is not None:
                    label_parts.append(f'threshold = {co_thr}')
                ax.annotate('\n'.join(label_parts), (co_fpr, co_tpr),
                            textcoords='offset points', xytext=(10, -15),
                            fontsize=7, color='#555555',
                            arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))

    elif curves:
        # Multiple ROC curves
        _seen_labels = set()
        for i, curve in enumerate(curves):
            fpr_c = np.array(curve.get("fpr", curve.get("x", [])), dtype=float)
            tpr_c = np.array(curve.get("tpr", curve.get("y", [])), dtype=float)
            auc_c = curve.get("auc", None)
            name = curve.get("name", f'Model {i+1}')

            if auc_c is None:
                auc_c = np.trapezoid(tpr_c, fpr_c) if hasattr(np, 'trapezoid') else np.trapz(tpr_c, fpr_c)

            c = theme["colors"][i % len(theme["colors"])]
            label = f'{name} (AUC={auc_c:.3f})'
            # B3(v2.7)：两条曲线 AUC 相同（或同名）时图例标签会完全重复——
            # 自动加序号消歧并 stderr 告知，避免图例两条一模一样无法区分
            if label in _seen_labels:
                uniq = f'{label} #{i + 1}'
                k = 2
                while uniq in _seen_labels:
                    uniq = f'{label} #{k + 1}'
                    k += 1
                print(f"WARNING: ROC 曲线「{name}」图例标签重复（AUC 相同或同名），"
                      f"已自动消歧为「{uniq}」", file=sys.stderr)
                label = uniq
            _seen_labels.add(label)
            ax.plot(fpr_c, tpr_c, color=c, linewidth=2, zorder=3, label=label)

    # ── v2.3：配对 DeLong 多模型 AUC 比较（--compare，需原始分数）──
    if kwargs.get("roc_compare") and _afstats is not None:
        labels_raw = data.get("labels", None)
        curves_cmp = data.get("curves", None)
        scores_ok = (labels_raw is not None and isinstance(curves_cmp, list)
                     and all("scores" in c for c in curves_cmp)
                     and len(curves_cmp) >= 2)
        if scores_ok:
            try:
                scores_by_model = {str(c.get("name", f"模型{i+1}")): c["scores"]
                                   for i, c in enumerate(curves_cmp)}
                aucs_d, pairs_d = _afstats.delong_paired(labels_raw, scores_by_model)
                lines = ["DeLong 配对检验"]
                for a_n, b_n, p_d, z_d in pairs_d:
                    lines.append(f"{a_n} vs {b_n}: p={p_d:.3g}")
                    print(f"  roc compare: {a_n} vs {b_n}: AUC "
                          f"{aucs_d[a_n]:.3f} vs {aucs_d[b_n]:.3f}, "
                          f"DeLong p={p_d:.4g} (z={z_d:.2g})", file=sys.stderr)
                ax.text(0.97, 0.32, "\n".join(lines), transform=ax.transAxes,
                        ha="right", va="top", fontsize=7, color="#333333",
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                  alpha=0.92, edgecolor='lightgray'))
            except Exception as e:
                print(f"WARNING: roc: DeLong 计算失败（{e}）", file=sys.stderr)
        else:
            print("WARNING: roc: --compare 需要 labels（0/1 数组）+ 每条曲线含原始 "
                  "scores 数组（同一样本多模型）——只有 fpr/tpr 曲线时无法做 DeLong",
                  file=sys.stderr)

    # Diagonal reference line
    if diagonal:
        ax.plot([0, 1], [0, 1], '--', color='gray', alpha=0.5, linewidth=1, zorder=1)

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect('equal')

    # v4.6：默认语义轴标题（期刊级；用户显式 --xlabel/--ylabel 时主流程会再覆盖）
    _roc_xl = "False Positive Rate"
    _roc_yl = "True Positive Rate"
    ax.set_xlabel(_roc_xl, fontsize=theme["font_size"],
                  fontproperties=cjk_fp if cjk_fp and has_cjk(_roc_xl) else None)
    ax.set_ylabel(_roc_yl, fontsize=theme["font_size"],
                  fontproperties=cjk_fp if cjk_fp and has_cjk(_roc_yl) else None)
    ax.xaxis.grid(True, alpha=theme["grid_alpha"], linestyle='--')


def gen_stacked_bar(data, ax, theme, cjk_fp, **kwargs):
    """Stacked bar chart for compositional data (e.g., subgroup proportions)."""
    labels = data.get("labels", data.get("x", []))
    series = data.get("series", data.get("datasets", {}))
    percentage = data.get("percentage", False)  # normalize to 100%
    show_total = data.get("show_total", False)  # show total on top of each bar
    errors = data.get("errors", None)  # optional error bars for totals
    use_hatch = kwargs.get("hatch", False)

    n_groups = len(labels)
    x = np.arange(n_groups)
    colors = theme["colors"]
    bottoms = np.zeros(n_groups)

    for i, (name, values) in enumerate(series.items()):
        vals = np.array(values, dtype=float)
        c = colors[i % len(colors)]
        hatch_val = HATCH_PATTERNS[i % len(HATCH_PATTERNS)] if use_hatch else None
        bars = ax.bar(x, vals, 0.65, bottom=bottoms, color=c,
                      edgecolor=_hatch_edgecolor(theme, colors[i % len(colors)]) if use_hatch else 'white',
                      linewidth=0.6 if use_hatch else 0.5,
                      hatch=hatch_val, label=name, zorder=2)

        # Value labels inside bars (only for segments > 5% of total)
        totals = sum(np.array(s, dtype=float) for s in series.values())
        for j, (v, total) in enumerate(zip(vals, totals)):
            if total > 0 and v / total > 0.05:  # only label segments > 5%
                ax.text(x[j], bottoms[j] + v / 2, f'{v:.1f}' if not percentage else f'{v/total*100:.1f}%',
                        ha='center', va='center', fontsize=7, color='white', fontweight='bold',
                        zorder=3)

        bottoms += vals

    # Total labels on top
    if show_total:
        for j in range(n_groups):
            total = bottoms[j]
            ax.text(x[j], total + 0.5, f'N={total:.0f}', ha='center', va='bottom',
                    fontsize=7, color='#333333', fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=theme["font_size"] - 1,
                       fontproperties=cjk_fp if cjk_fp and any(has_cjk(l) for l in labels) else None)

    if percentage:
        ax.set_ylim(0, max(bottoms) * 1.1)


def _fmt_num(v):
    return f'{int(v)}' if float(v).is_integer() else f'{v:.1f}'


def _annotate_peak(ax, xs, labels, values, horizontal, theme, cjk_fp, series_name=None):
    """v4.2 --peak-label：最大值点自动注记（纯数据事实：峰值+所在类目）。"""
    vals = [float(v) for v in values]
    if len(vals) < 2:
        return
    im = int(max(range(len(vals)), key=lambda k: vals[k]))
    head = f"峰值 {_fmt_num(vals[im])}"
    lab = str(labels[im]) if im < len(labels) else ""
    txt = head + (f"（{lab}）" if lab else "") + (f" · {series_name}" if series_name else "")
    _px = xs[im] if isinstance(xs, (list, tuple)) and im < len(xs) else im
    ax.annotate(txt, xy=(_px, vals[im]) if not horizontal else (vals[im], im),
                xytext=(0, 14) if not horizontal else (14, 0),
                textcoords="offset points", ha="center" if not horizontal else "left",
                fontsize=max(6, theme["font_size"] - 0.5), color="#B3541E",
                fontproperties=cjk_fp if cjk_fp and has_cjk(txt) else None,
                arrowprops=dict(arrowstyle="-", color="#B3541E", lw=0.8), zorder=6)
    print(f"peak: {txt}", file=sys.stderr)


def gen_slope(data, ax, theme, cjk_fp, **kwargs):
    """Slope chart（v4.2，第 23 号图型）：两时点比较——每项一条左→右连线，
    两端直接标注"名称+数值"，最大上升项主题色强调、最大下降项暖橙。
    期刊 pre/post 标准形态（如治疗前后、基线→随访）。

    JSON: {"left_label": "基线", "right_label": "12 周",
           "items": {"药物A": [72, 85], "药物B": [65, 61]}}  # 每项恰好 2 个数值
    """
    items = data.get("items")
    if not isinstance(items, dict) or len(items) < 2:
        raise ValueError("slope: 需要 'items'（至少 2 项，每项 [左值, 右值]）")
    for n, v in items.items():
        if not (isinstance(v, (list, tuple)) and len(v) == 2
                and all(isinstance(x, (int, float)) for x in v)):
            raise ValueError(f"slope: items['{n}'] 必须是恰好 2 个数值 [左值, 右值]")
    names = list(items.keys())
    lv = [float(items[n][0]) for n in names]
    rv = [float(items[n][1]) for n in names]
    deltas = [r - l for l, r in zip(lv, rv)]
    i_rise = int(max(range(len(names)), key=lambda k: deltas[k]))
    i_fall = int(min(range(len(names)), key=lambda k: deltas[k]))

    from matplotlib.colors import to_rgba
    accent = theme["colors"][0]
    x0, x1 = 0.0, 1.0
    for i, n in enumerate(names):
        if i == i_rise and deltas[i_rise] > 0:
            c, lw, z = accent, 2.6, 3
        elif i == i_fall and deltas[i_fall] < 0:
            c, lw, z = "#D55E00", 2.2, 3
        else:
            c, lw, z = to_rgba(accent, 0.45), 1.5, 2  # v7.9.1 AF42：0.32 在白底过淡（细元素可见性下限）
        ax.plot([x0, x1], [lv[i], rv[i]], color=c, lw=lw, zorder=z,
                marker="o", markersize=4, markerfacecolor=c)

    def _spread(vals):
        order = sorted(range(len(vals)), key=lambda k: vals[k])
        out = [0.0] * len(vals)
        lo, hi = min(vals), max(vals)
        gap = max((hi - lo) * 0.07, 1e-9)
        for a in range(1, len(order)):
            p, q = order[a - 1], order[a]
            out[q] = max(out[p] + gap, vals[q]) if vals[q] >= vals[p] else vals[q]
        # 自下而上推开后，若顶到底顺序错位再自上而下收一遍
        for a in range(len(order) - 2, -1, -1):
            p, q = order[a], order[a + 1]
            if out[q] - out[p] < gap:
                out[p] = out[q] - gap
        return out

    ly, ry = _spread(lv), _spread(rv)
    # v7.9.1 AF37：把 _spread 溢出的标签纳入 ylim（左端全同值时 spread 会把最下项
    # 推到 ylim 外=标签掉出图框；扩框优于钳制——钳制会把多个标签挤到同一点互叠）
    _all = list(lv) + list(rv) + list(ly) + list(ry)
    _lo, _hi = min(_all), max(_all)
    _m = ((_hi - _lo) * 0.06) or 1.0
    ax.set_ylim(_lo - _m, _hi + _m)
    _fp = cjk_fp
    for i, n in enumerate(names):
        fp = _fp if _fp and has_cjk(n) else None
        ax.plot([x0], [lv[i]], "o", color=accent if i == i_rise else "#888888",
                markersize=4, zorder=3)
        ax.text(x0 - 0.04, ly[i], f"{n}  {_fmt_num(lv[i])}", ha="right", va="center",
                fontsize=theme["font_size"] - 0.5, color="#333333", fontproperties=fp)
        ax.text(x1 + 0.04, ry[i], f"{_fmt_num(rv[i])}  {n}", ha="left", va="center",
                fontsize=theme["font_size"] - 0.5, color="#333333", fontproperties=fp)

    ll = str(data.get("left_label", "") or "")
    rl = str(data.get("right_label", "") or "")
    ax.set_xlim(-0.6, 1.6)
    ax.set_xticks([x0, x1])
    ax.set_xticklabels([ll or "Before", rl or "After"],
                       fontsize=theme["font_size"], fontweight="bold",
                       fontproperties=_fp if _fp and (has_cjk(ll) or has_cjk(rl)) else None)
    _top = _fp if _fp and (has_cjk(ll) or has_cjk(rl)) else None
    if ll:
        ax.text(0, 1.03, ll, transform=ax.get_xaxis_transform(), ha="center",
                fontsize=theme["font_size"], fontweight="bold", color="#555555",
                fontproperties=_top)
    if rl:
        ax.text(1, 1.03, rl, transform=ax.get_xaxis_transform(), ha="center",
                fontsize=theme["font_size"], fontweight="bold", color="#555555",
                fontproperties=_top)
    apply_base_style(ax, theme)
    ax.grid(False)
    ax.set_yticks([])


def gen_volcano(data, ax, theme, cjk_fp, **kwargs):
    """Volcano plot（v4.4，第 24 号图型）：组学差异表达标准形态——
    x=log2(倍数变化)，y=-log10(p 值)；上调暖橙/下调蓝/非显著灰；
    阈值虚线（|log2FC| 与 p）+ 显著性 Top-N 自动名称标注（确定性偏移避让）。

    JSON: {"log2fc": [2.1, -1.3, ...], "pvalue": [1e-6, 0.03, ...],
           "names": ["GeneA", ...](可选), "fc_cut": 1.0, "p_cut": 0.05, "top": 10}
    """
    import math
    l2 = data.get("log2fc")
    pv = data.get("pvalue")
    if not (isinstance(l2, list) and isinstance(pv, list)) or not l2 or len(l2) != len(pv):
        raise ValueError("volcano: 需要 'log2fc' 与 'pvalue' 两个等长数值数组")
    names = data.get("names")
    if names is not None and (not isinstance(names, list) or len(names) != len(l2)):
        raise ValueError("volcano: 'names' 长度必须与 log2fc 一致")
    try:
        l2v = [float(v) for v in l2]
        pvv = [float(v) for v in pv]
    except (TypeError, ValueError):
        raise ValueError("volcano: log2fc/pvalue 必须全为数值")
    if any(p <= 0 or p > 1 for p in pvv):
        raise ValueError("volcano: pvalue 必须在 (0, 1] 区间（p=0 无法取对数，请用最小可表示值如 1e-300）")
    fc_cut = float(data.get("fc_cut", 1.0))
    p_cut = float(data.get("p_cut", 0.05))
    top_n = int(data.get("top", 10))
    # v7.9.0 AF35：约束违例点名违例字段与实值（原合并一句话不指认哪个参数）
    _viol = []
    if fc_cut <= 0:
        _viol.append(f"fc_cut={data.get('fc_cut', 1.0)} 不满足 fc_cut>0")
    if not (0 < p_cut < 1):
        _viol.append(f"p_cut={data.get('p_cut', 0.05)} 不满足 0<p_cut<1")
    if top_n < 0:
        _viol.append(f"top={data.get('top', 10)} 不满足 top≥0")
    if _viol:
        raise ValueError("volcano: " + "；".join(_viol))

    yv = [-math.log10(p) for p in pvv]
    sig_cut = -math.log10(p_cut)
    cls = []
    for x, y in zip(l2v, yv):
        if x >= fc_cut and y >= sig_cut:
            cls.append("up")
        elif x <= -fc_cut and y >= sig_cut:
            cls.append("down")
        else:
            cls.append("ns")
    colors = {"up": "#D55E00", "down": "#0072B2", "ns": "#B8B8B8"}
    sizes = {"up": 16, "down": 16, "ns": 9}
    for c in ("ns", "down", "up"):  # 显著点后画（置顶）
        xs = [x for x, k in zip(l2v, cls) if k == c]
        ys = [y for y, k in zip(yv, cls) if k == c]
        ax.scatter(xs, ys, s=sizes[c], c=colors[c], alpha=0.85 if c != "ns" else 0.7,
                   linewidths=0, zorder=3 if c != "ns" else 2)

    # 阈值参考线
    ax.axvline(fc_cut, color="#999999", ls="--", lw=0.9, zorder=1)
    ax.axvline(-fc_cut, color="#999999", ls="--", lw=0.9, zorder=1)
    ax.axhline(sig_cut, color="#999999", ls="--", lw=0.9, zorder=1)

    # 显著性 Top-N 名称标注（按 p 升序 = y 降序，确定性交错偏移）
    import matplotlib.pyplot as plt  # noqa: F401
    idx_sig = [i for i, k in enumerate(cls) if k in ("up", "down")]
    idx_sig.sort(key=lambda i: yv[i], reverse=True)
    n_up = sum(1 for k in cls if k == "up")
    n_down = sum(1 for k in cls if k == "down")
    for rank, i in enumerate(idx_sig[:top_n]):
        if names is None:
            break
        dx = 5 if l2v[i] >= 0 else -5
        ax.annotate(str(names[i]), xy=(l2v[i], yv[i]),
                    xytext=(dx, 4 + (rank % 3) * 5), textcoords="offset points",
                    ha="left" if dx > 0 else "right",
                    fontsize=max(5.5, theme["font_size"] - 1),
                    color=colors[cls[i]],
                    fontproperties=cjk_fp if cjk_fp and has_cjk(str(names[i])) else None)

    # 计数事实框（纯计数，零推断）
    ax.text(0.02, 0.98, f"↑{n_up}  ↓{n_down}  ns {len(cls) - n_up - n_down}",
            transform=ax.transAxes, va="top", ha="left",
            fontsize=theme["font_size"], color="#555555",
            fontproperties=cjk_fp if cjk_fp and has_cjk("上调") else None)

    # 坐标轴语义（类型专属默认；CLI --xlabel/--ylabel 可覆盖）
    xl = str(data.get("x_label", "") or "log2 fold change")
    yl = str(data.get("y_label", "") or "-log10(p-value)")
    ax.set_xlabel(xl, fontsize=theme["font_size"],
                  fontproperties=cjk_fp if cjk_fp and has_cjk(xl) else None)
    ax.set_ylabel(yl, fontsize=theme["font_size"],
                  fontproperties=cjk_fp if cjk_fp and has_cjk(yl) else None)
    ax.set_xlim(min(l2v) - 0.3, max(l2v) + 0.3)
    apply_base_style(ax, theme)


def _upset_name_band(names, theme, fig):
    """v4.7 D-07：按最长集合名动态求 (左边距, wspace)——名字带=左边距+面板间隙，
    固定值时长名会压进 set-size 条。est_in 为名字显示宽度的保守估计（CJK≈1em/字）。"""
    fs = theme.get("font_size", 9)
    try:
        max_chars = max(len(str(nm)) for nm in names)
    except ValueError:
        max_chars = 8
    est_in = max_chars * fs * 0.016
    left = min(0.45, max(0.24, 0.03 + est_in / max(fig.get_figwidth(), 1e-6)))
    usable_w = (0.97 - left) * max(fig.get_figwidth(), 1e-6)
    needed_in = est_in + 0.15
    wspace = min(0.9, 2.0 * needed_in / max(usable_w - needed_in, 0.5))
    return left, wspace




def raincloud_alt(data, t=""):
    """v4.9：raincloud 的 --alt 文本。"""
    series = data.get("series") or data.get("datasets") or {}
    meds = []
    for n, v in series.items():
        try:
            import numpy as _np
            meds.append(f"{n} 中位数 {_np.median([float(x) for x in v]):g}")
        except Exception:
            pass
    seg = "；".join(meds[:6]) + ("等" if len(meds) > 6 else "")
    n_pts = sum(len(v) for v in series.values())
    return (f"雨云图（分布三合一：密度云+箱线+原始点），共 {len(series)} 组 {n_pts} 个数据点"
            + (f"；{seg}" if seg else "") + f"。{t}")


def validate_raincloud(data):
    """v4.9：raincloud 数据校验（返回 fatal 列表；放本模块守 gen_figure 行数纪律）。"""
    fatal = []
    series = data.get("series", data.get("datasets"))
    labels = data.get("labels", data.get("x", []))
    if not isinstance(series, dict) or not series:
        fatal.append("raincloud: 需要 'datasets'（{组名: [数值数组]}），schema 同 violin")
        return fatal
    if labels and len(labels) != len(series):
        fatal.append(f"raincloud: labels 有 {len(labels)} 项但 datasets 有 {len(series)} 组——须一一对应")
    for n, vals in series.items():
        if not isinstance(vals, (list, tuple)) or not vals:
            fatal.append(f"raincloud: datasets['{n}'] 必须是非空数值数组")
            continue
        bad = [v for v in vals if isinstance(v, bool) or not isinstance(v, (int, float))]
        if bad:
            fatal.append(f"raincloud: datasets['{n}'] 含 {len(bad)} 个非数值项")
            continue
        import math as _m
        if not all(_m.isfinite(float(v)) for v in vals):
            fatal.append(f"raincloud: datasets['{n}'] 含非有限数值（NaN/±Infinity）——请清洗源数据")
    j = data.get("jitter")
    if j is not None and (isinstance(j, bool) or not isinstance(j, (int, float)) or not 0 <= j <= 0.3):
        fatal.append("raincloud: jitter 取值 0~0.3")
    cs = data.get("cloud_scale")
    if cs is not None and (isinstance(cs, bool) or not isinstance(cs, (int, float)) or not 0 <= cs <= 2.0):
        fatal.append("raincloud: cloud_scale 取值 0~2.0")
    return fatal




def gen_raincloud(data, ax, theme, cjk_fp, **kwargs):
    """Raincloud plot（v4.9，第 27 号图型）：半小提琴（KDE 密度云）+ 箱线（五数概括）
    + 抖动原始点（雨滴）三合一——分布可视化现代标准形态（Allen et al. 2021），
    box 只给摘要、violin 藏样本、raincloud 全部给出且互不遮挡。

    左云右雨：半小提琴在组位左侧、窄箱居中、确定性抖动雨滴在右侧。
    JSON 与 violin 同 schema：{"labels": [...], "datasets": {"组名": [值...]}}
    可选 "jitter": 0.08（雨滴横向抖动幅度）、"cloud_scale": 1.0（云宽缩放）。
    """
    import random as _random
    labels = data.get("labels", data.get("x", []))
    series = data.get("series", data.get("datasets", {}))
    if not isinstance(series, dict) or not series:
        raise ValueError("raincloud: 需要 'datasets'（{{组名: [数值数组]}}），schema 同 violin")
    names = list(series.keys())
    if labels and len(labels) != len(names):
        raise ValueError(f"raincloud: labels 有 {len(labels)} 项但 datasets 有 {len(names)} 组——须一一对应")
    for n, vals in series.items():
        if not isinstance(vals, (list, tuple)) or not vals:
            raise ValueError(f"raincloud: datasets['{n}'] 必须是非空数值数组")
        bad = [v for v in vals if isinstance(v, bool) or not isinstance(v, (int, float))
               or not np.isfinite(float(v))]
        if bad:
            raise ValueError(f"raincloud: datasets['{n}'] 含 {len(bad)} 个非有限数值（NaN/±Infinity/非数值）")
    jitter_w = float(data.get("jitter", 0.08))
    cloud_scale = float(data.get("cloud_scale", 1.0))
    if not (0 <= jitter_w <= 0.3) or cloud_scale < 0 or cloud_scale > 2.0:
        raise ValueError("raincloud: jitter 取值 0~0.3、cloud_scale 取值 0~2.0（0=藏云；>2.0 会跨组叠压，已按代数界收紧）")

    from scipy.stats import gaussian_kde
    positions = list(range(len(names)))
    rng = _random.Random(4900)  # 确定性雨滴（同数据同图）
    fs = theme["font_size"]

    for i, (name, vals) in enumerate(series.items()):
        v = np.asarray([float(x) for x in vals], dtype=float)
        color = theme["colors"][i % len(theme["colors"])]
        # ── 云（半小提琴，KDE）──
        if cloud_scale > 0:
            try:
                kde = gaussian_kde(v)
                grid = np.linspace(v.min() - 0.5 * v.std() - 1e-9, v.max() + 0.5 * v.std() + 1e-9, 80)
                dens = kde(grid)
                # v7.9.1 AF27：KDE 尾部裁剪到数据范围（时间/计数类数据密度云
                # 曾越过 0 下界伸入无意义负值区——边界外密度=核平滑伪影）
                if v.min() >= 0:
                    _inside = grid >= 0
                    grid, dens = grid[_inside], dens[_inside]
                dens = dens / dens.max() * 0.28 * cloud_scale  # cs≤2.0：半宽≤0.56，与箱/邻组雨带不叠
                ax.fill_betweenx(grid, i - dens, i, facecolor=color, alpha=0.45,
                                 edgecolor=color, linewidth=1.0, zorder=2)
            except (np.linalg.LinAlgError, ValueError):  # 全同值/单点组：KDE 退化 → 竖线示意（n=1 抛 ValueError）
                ax.plot([i, i], [v.min(), v.max()], color=color, lw=2, alpha=0.5, zorder=2)
                ax.plot(i, float(v.mean()), "o", color=color, ms=5, zorder=3)
                print(f"raincloud: 组「{name}」方差为 0 或单点，云退化为标记线", file=sys.stderr)
        else:
            print("raincloud: cloud_scale=0，云已隐藏（仅箱+雨）", file=sys.stderr)

        # ── 箱（窄箱线：五数概括）──
        q1, med, q3 = np.percentile(v, [25, 50, 75])
        iqr = q3 - q1
        whisker_lo = max(v.min(), q1 - 1.5 * iqr)
        whisker_hi = min(v.max(), q3 + 1.5 * iqr)
        bw = 0.055
        ax.plot([i - bw, i + bw], [med, med], color="#2D3746", lw=2.2, zorder=4)
        ax.add_patch(plt.Rectangle((i - bw, q1), 2 * bw, q3 - q1, fill=True,
                                   facecolor="white", edgecolor="#2D3746", lw=1.2, zorder=3))
        ax.plot([i, i], [whisker_lo, q1], color="#2D3746", lw=1.1, zorder=3)
        ax.plot([i, i], [q3, whisker_hi], color="#2D3746", lw=1.1, zorder=3)
        ax.plot([i - bw * 0.7, i + bw * 0.7], [whisker_lo, whisker_lo], color="#2D3746", lw=1.1, zorder=3)
        ax.plot([i - bw * 0.7, i + bw * 0.7], [whisker_hi, whisker_hi], color="#2D3746", lw=1.1, zorder=3)
        # ── 雨（确定性抖动原始点）──
        xs = [i + 0.10 + rng.uniform(0, jitter_w) for _ in v]
        ax.scatter(xs, v, s=11, color=color, alpha=0.65, linewidths=0, zorder=3)

    if kwargs.get("stats_multi"):
        annotate_multi_stats(ax, series, positions, theme, "raincloud")
    elif kwargs.get("stats_auto"):
        annotate_auto_stats(ax, series, positions, theme, "raincloud")
    elif kwargs.get("stats_bootstrap"):
        annotate_bootstrap_stats(ax, series, positions, theme, "raincloud")

    ax.set_xticks(positions)
    show_labels = labels if labels else names
    ax.set_xticklabels(list(show_labels), fontsize=fs - 1,
                       fontproperties=cjk_fp if cjk_fp and has_cjk("".join(map(str, show_labels))) else None)
    ax._af_category_axis = True  # 组名是数据：豁免刻度抽稀（同 waterfall）
    ax.set_xlim(-0.7, len(names) - 0.3 + 0.1 + jitter_w)
    apply_base_style(ax, theme)
    print(f"raincloud: {len(names)} 组 / 共 {sum(len(v) for v in series.values())} 个原始点"
          f"（云=KDE 密度，箱=五数概括，雨=原始点）", file=sys.stderr)


def gen_upset(data, ax, theme, cjk_fp, **kwargs):
    """UpSet 交集图（v4.7，第 25 号图型）：多集合交集可视化——韦恩图（2~4 集合）
    的标准后继；≥5 集合场景（组学多基因集/多标签共现/多中心入排标准重叠）远优于 venn。

    经典三区布局：顶部=交集大小柱（降序，计数直标）；中部=点阵（行=集合、
    列=交集，实心点+竖连线标隶属关系）；左下=集合总大小横条（与点阵共 y 轴、
    自右向左生长）。排序确定性三键 tie-break（大小→度数→名称序），同数据同图；
    未展示交集只计入 stderr 事实行，不出图（零猜测）。

    JSON: {"sets": {"集合名": [元素...], ...}, "title": "..."(可选),
           "top_n": 12, "min_size": 1, "sort": "size"|"degree"}
    """
    from matplotlib import gridspec as _gridspec
    from matplotlib.ticker import MaxNLocator

    sets_raw = data.get("sets")
    if not isinstance(sets_raw, dict) or len(sets_raw) < 2:
        raise ValueError("upset: 需要 'sets'（≥2 个集合，值为元素列表；≥5 集合时最见长，"
                         "2~4 集合建议 venn）")
    if len(sets_raw) > 30:
        raise ValueError(f"upset: 集合数 {len(sets_raw)} 超上限 30"
                         "（点阵行数过多不可读，请按意义分组或拆分）")
    names = [str(k) for k in sets_raw.keys()]
    if len(set(names)) != len(names):
        raise ValueError("upset: 集合名转字符串后重复，请改名")
    member = {}
    for k, els in sets_raw.items():
        nm = str(k)
        if not isinstance(els, (list, tuple)) or not els:
            raise ValueError(f"upset: sets['{nm}'] 必须是非空元素列表")
        seen = set()
        for e in els:
            if isinstance(e, bool) or not isinstance(e, (str, int, float)):
                raise ValueError(f"upset: sets['{nm}'] 含不支持的元素类型 "
                                 f"{type(e).__name__}（仅字符串/数值标量）")
            seen.add(e)
        member[nm] = seen
    top_n = data.get("top_n", 12)
    min_size = data.get("min_size", 1)
    sort_mode = str(data.get("sort", "size")).strip().lower()
    # v4.7 D-11：与 validate 同口径的严格整数校验（Python API 直调不再静默截断 12.5→12）
    for _nm, _v in (("top_n", top_n), ("min_size", min_size)):
        if isinstance(_v, bool) or not isinstance(_v, int):
            raise ValueError(f"upset: {_nm} 必须是整数")
    if not 1 <= top_n <= 50:
        raise ValueError("upset: top_n 取值 1~50")
    if min_size < 1:
        raise ValueError("upset: min_size ≥ 1")
    if sort_mode not in ("size", "degree"):
        raise ValueError("upset: sort 只支持 'size' 或 'degree'")

    # 交集模式计数：元素 → 隶属集合 pattern → 计数
    elem_pat = {}
    for nm, s in member.items():
        for e in s:
            elem_pat.setdefault(e, set()).add(nm)
    pat_count = {}
    for pats in elem_pat.values():
        fk = frozenset(pats)
        pat_count[fk] = pat_count.get(fk, 0) + 1

    pats = [(p, c) for p, c in pat_count.items() if c >= min_size]
    if not pats:
        raise ValueError(f"upset: min_size={min_size} 过滤后无交集可展示"
                         f"（当前最大交集为 {max(pat_count.values())}）")
    if sort_mode == "size":
        pats.sort(key=lambda pc: (-pc[1], -len(pc[0]), sorted(pc[0])))
    else:
        pats.sort(key=lambda pc: (-len(pc[0]), -pc[1], sorted(pc[0])))
    shown = pats[:top_n]
    n_hidden = len(pats) - len(shown)
    hidden_elems = sum(c for _, c in pats[top_n:])

    n = len(names)
    row_of = {nm: n - 1 - i for i, nm in enumerate(names)}  # 首个集合=顶行
    fig = ax.figure
    ax.remove()
    # v4.7 D-04：交集柱必须与点阵同列（gs[0,1]），否则柱与隶属点阵错位 1/4 图宽，
    # 破坏 UpSet 的定义性读图关系（经典 UpSet 左上留空：suptitle 居中覆盖）。
    _lft, _wsp = _upset_name_band(names, theme, fig)
    gs = _gridspec.GridSpec(2, 2, figure=fig, height_ratios=[2.7, 1.5],
                            width_ratios=[0.95, 3.05], hspace=0.06,
                            wspace=_wsp, left=_lft,
                            right=0.97, top=0.88, bottom=0.07)
    ax_isz = fig.add_subplot(gs[0, 1])
    ax_mat = fig.add_subplot(gs[1, 1])
    ax_set = fig.add_subplot(gs[1, 0])  # 不 sharey（共享组会让 tick_params 相互传播）
    c0 = theme["colors"][0]
    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    _cjk_all = cjk_fp if cjk_fp and has_cjk("".join(names) + "交集集合") else None

    # 顶部：交集大小柱（计数直标；整数刻度）
    counts = [c for _, c in shown]
    xs = np.arange(len(shown))
    ax_isz.bar(xs, counts, width=0.62, color=c0, edgecolor="none", zorder=3)
    for x, c in zip(xs, counts):
        ax_isz.text(x, c + max(counts) * 0.02, str(c), ha="center", va="bottom",
                    fontsize=fs_s, color="#333333")
    ax_isz.set_xlim(-0.7, len(shown) - 0.3)
    ax_isz.set_ylim(0, max(counts) * 1.18)
    ax_isz.set_xticks([])
    ax_isz.set_ylabel("Intersection size", fontsize=fs)
    ax_isz.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
    ax_isz.spines["top"].set_visible(False)
    ax_isz.spines["right"].set_visible(False)
    if n_hidden:
        _hid = (f"另有 {n_hidden} 个交集（共 {hidden_elems} 个元素）未展示"
                if _cjk_all else
                f"+{n_hidden} more intersections ({hidden_elems} elements) not shown")
        ax_isz.text(0.995, 0.97, _hid, transform=ax_isz.transAxes, ha="right",
                    va="top", fontsize=fs_s, color="#777777",
                    fontproperties=_cjk_all)

    # 中部：点阵（实心点+竖连线）
    for j, (pat, _c) in enumerate(shown):
        rows = sorted(row_of[s] for s in pat)
        if len(rows) > 1:
            ax_mat.plot([j, j], [rows[0], rows[-1]], color="#4A4A4A", lw=1.0,
                        zorder=2, solid_capstyle="butt")
        for r in rows:
            ax_mat.plot(j, r, "o", ms=5.2, color="#2E2E2E", zorder=3,
                        markeredgecolor="none")
    ax_mat.set_xlim(-0.7, len(shown) - 0.3)
    ax_mat.set_ylim(-0.7, n - 0.3)
    ax_mat.set_yticks(range(n))
    ax_mat.set_yticklabels(list(reversed(names)), fontsize=fs_s,
                           fontproperties=_cjk_all)
    ax_mat._af_category_axis = True  # 集合名是数据：豁免 fix_tick_overlaps 静默抽稀（D-06）
    ax_mat.set_xticks([])
    for sp in ("top", "right", "bottom", "left"):
        ax_mat.spines[sp].set_visible(False)
    ax_mat.tick_params(left=False, bottom=False)

    # 左下：集合总大小横条（自右向左生长，与点阵同 y 界；数值白字居柱内右端）
    set_sizes = [len(member[nm]) for nm in names]
    ys = [row_of[nm] for nm in names]
    _smax = max(set_sizes)
    ax_set.barh(ys, set_sizes, height=0.52, color=c0, alpha=0.55,
                edgecolor="none", zorder=3)
    for y, v in zip(ys, set_sizes):
        if v >= _smax * 0.12:
            # 数值白字居柱内右端（柱足够长时）
            ax_set.text(_smax * 0.04, y, str(v), va="center", ha="right",
                        fontsize=fs_s, color="#FFFFFF", zorder=4)
        else:
            # D-05：短柱时白字会落到柱外白底上不可见——改深色置于柱尖外侧
            ax_set.text(v + _smax * 0.05, y, str(v), va="center", ha="right",
                        fontsize=fs_s, color="#333333", zorder=4)
    ax_set.set_xlim(_smax * 1.45, 0)
    ax_set.set_ylim(-0.7, n - 0.3)
    ax_set.set_yticks([])
    ax_set.set_xticks([])
    for sp in ("top", "right", "bottom", "left"):
        ax_set.spines[sp].set_visible(False)
    ax_set.tick_params(labelleft=False, left=False, bottom=False)
    ax_set.set_ylabel("Set size", fontsize=fs)

    ttl = data.get("title")
    if ttl:
        fig.suptitle(str(ttl), fontsize=fs + 1, fontweight="bold",
                     fontproperties=cjk_fp if cjk_fp and has_cjk(str(ttl)) else None)

    print(f"upset: {n} 集合 / {len(pat_count)} 个非空交集模式 / 展示 top {len(shown)}"
          f"（sort={sort_mode}，min_size={min_size}）"
          + (f"；另有 {n_hidden} 个交集（{hidden_elems} 元素）未展示" if n_hidden else ""),
          file=sys.stderr)
    return "upset"  # main() 据此跳过 tight_layout/基础样式（自管类型，同 composite）


def waterfall_alt(data, t=""):
    """v4.8：waterfall 的 --alt 文本（放本模块守 gen_figure <3400 行纪律）。"""
    from collections import Counter as _C
    chg = data.get("change") or []
    grp = data.get("group")
    if isinstance(grp, list) and grp:
        cnt = _C(str(g).upper() for g in grp)
        fact = "  ".join(f"{k} {v}" for k, v in cnt.most_common())
    else:
        pr = float(data.get("pr_cut", -30.0))
        pd = float(data.get("pd_cut", 20.0))
        try:
            vals = [float(v) for v in chg]
            n_r = sum(1 for v in vals if v <= pr)
            n_p = sum(1 for v in vals if v >= pd)
            fact = f"缓解 {n_r}、稳定 {len(vals) - n_r - n_p}、进展 {n_p}"
        except (TypeError, ValueError):
            fact = ""
    return (f"肿瘤缓解瀑布图，共 {len(chg)} 例（每例自基线最佳变化%，降序）"
            + (f"；{fact}" if fact else "") + f"。{t}")


def validate_waterfall(data):
    """v4.8：waterfall 数据校验（返回 fatal 列表）；逻辑与 gen_waterfall 内部
    校验同口径。放本模块使 gen_figure 行数守住模块化纪律（<3400）。"""
    fatal = []
    chg = data.get("change")
    if not (isinstance(chg, list) and chg):
        fatal.append("waterfall: 需要 'change'（非空数值数组，单位 %；肿瘤缩小为负）")
        return fatal
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in chg):
        fatal.append("waterfall: change 必须全为数值")
        return fatal
    import math as _m
    if not all(_m.isfinite(x) for x in chg):
        fatal.append("waterfall: change 含非有限值（NaN/±Infinity）——请清洗源数据")
        return fatal
    nchg = len(chg)
    names = data.get("names")
    if names is not None and (not isinstance(names, list) or len(names) != nchg):
        fatal.append("waterfall: 'names' 长度必须与 change 一致")
    grp = data.get("group")
    if grp is not None:
        if not isinstance(grp, list) or len(grp) != nchg:
            fatal.append("waterfall: 'group' 长度必须与 change 一致")
        elif not all(isinstance(g, (str, int, float)) and not isinstance(g, bool)
                     for g in grp):
            fatal.append("waterfall: 'group' 必须全为字符串或数值标量")
    pc = data.get("pr_cut")
    dc = data.get("pd_cut")
    if pc is not None and (isinstance(pc, bool) or not isinstance(pc, (int, float))
                           or pc >= 0):
        fatal.append("waterfall: pr_cut 必须为负数（如 -30）")
    if dc is not None and (isinstance(dc, bool) or not isinstance(dc, (int, float))
                           or dc <= 0):
        fatal.append("waterfall: pd_cut 必须为正数（如 20）")
    sm = data.get("sort")
    if sm is not None and str(sm).strip().lower() not in ("desc", "input"):
        fatal.append("waterfall: sort 只支持 'desc' 或 'input'")
    return fatal


def gen_waterfall(data, ax, theme, cjk_fp, **kwargs):
    """Waterfall plot（v4.8，第 26 号图型）：肿瘤学最佳缓解瀑布图——每例患者
    自基线最佳肿瘤直径变化百分比，按变化降序（经典形态）排列；
    阈值虚线（PR/PD）+ 类别着色 + 计数事实框（纯计数，零推断）。

    着色语义：给 group（如 RECIST CR/PR/SD/PD）时按类别着色（主题色按首现顺序）；
    未给 group 时按阈值分桶：≤pr_cut 缓解蓝 / ≥pd_cut 进展橙 / 中间稳定灰
    （与 volcano 同款色盲安全语义色）。

    JSON: {"change": [-45.2, ...], "names": ["P001", ...](可选),
           "group": ["PR", ...](可选), "pr_cut": -30.0, "pd_cut": 20.0,
           "sort": "desc"(默认)|"input", "y_label": "..."(可选)}
    """
    chg = data.get("change")
    if not (isinstance(chg, list) and chg):
        raise ValueError("waterfall: 需要 'change'（非空数值数组，单位 %；"
                         "肿瘤缩小为负、增大为正）")
    try:
        vals = [float(v) for v in chg]
    except (TypeError, ValueError):
        raise ValueError("waterfall: change 必须全为数值")
    import math as _m
    if not all(_m.isfinite(v) for v in vals):
        raise ValueError("waterfall: change 含非有限值（NaN/±Infinity）——"
                         "请清洗源数据（v4.5 数值政策：非有限值一律拒绝，不静默跳过）")
    n = len(vals)
    names = data.get("names")
    if names is not None and (not isinstance(names, list) or len(names) != n):
        raise ValueError("waterfall: 'names' 长度必须与 change 一致")
    group = data.get("group")
    if group is not None:
        if not isinstance(group, list) or len(group) != n:
            raise ValueError("waterfall: 'group' 长度必须与 change 一致")
        if not all(isinstance(g, (str, int, float)) and not isinstance(g, bool)
                   for g in group):
            raise ValueError("waterfall: 'group' 必须全为字符串或数值标量")
    pr_cut = float(data.get("pr_cut", -30.0))
    pd_cut = float(data.get("pd_cut", 20.0))
    sort_mode = str(data.get("sort", "desc")).strip().lower()
    if pr_cut >= 0 or pd_cut <= 0:
        raise ValueError("waterfall: pr_cut 必须为负数（如 -30）、pd_cut 必须为正数（如 20）")
    if sort_mode not in ("desc", "input"):
        raise ValueError("waterfall: sort 只支持 'desc' 或 'input'")

    order = sorted(range(n), key=lambda i: (-vals[i], i)) if sort_mode == "desc" \
        else list(range(n))
    svals = [vals[i] for i in order]
    snames = [str(names[i]) if names else f"P{i+1:02d}" for i in order]
    sgroup = [str(group[i]) if group else None for i in order]

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    x = np.arange(n)
    if sgroup and group is not None:
        # 类别着色：全为 RECIST 标准类别时用规范语义色（CR/PR 蓝系、SD 灰、PD 橙，
        # 与阈值分桶模式同语义），否则主题色按首现顺序（确定性）
        _recist = {"CR": "#2C5F8A", "PR": "#5FA4D0", "SD": "#B8B8B8", "PD": "#D55E00"}
        cats, cmap = [], {}
        _upper = [str(g).upper() for g in sgroup]
        if set(_upper) <= set(_recist):
            # v4.8 审查 P3-3：大小写不敏感归一到规范大写形（PR/pr 不再拆成两条图例）
            sgroup = _upper
            for gu in _upper:
                if gu not in cmap:
                    cmap[gu] = _recist[gu]
                    cats.append(gu)
        else:
            for g in sgroup:
                if g not in cmap:
                    cmap[g] = theme["colors"][len(cmap) % len(theme["colors"])]
                    cats.append(g)
        bar_colors = [cmap[g] for g in sgroup]
        handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[c]) for c in cats]
        ax.legend(handles, cats, loc="upper right", frameon=False,
                  fontsize=fs_s, prop=cjk_fp if cjk_fp and has_cjk("".join(cats)) else None)
        cnt = {c: sgroup.count(c) for c in cats}
        fact = "  ".join(f"{c} {cnt[c]}" for c in cats)
    else:
        # 阈值分桶（与 volcano 同语义色）
        r_col, s_col, p_col = "#0072B2", "#B8B8B8", "#D55E00"
        bar_colors = [r_col if v <= pr_cut else (p_col if v >= pd_cut else s_col)
                      for v in svals]
        handles = [plt.Rectangle((0, 0), 1, 1, color=c)
                   for c in (r_col, s_col, p_col)]
        n_r = sum(1 for v in svals if v <= pr_cut)
        n_p = sum(1 for v in svals if v >= pd_cut)
        labels = ["缓解" if cjk_fp else "Response",
                  "稳定" if cjk_fp else "Stable",
                  "进展" if cjk_fp else "Progression"]
        ax.legend(handles, labels, loc="upper right", frameon=False, fontsize=fs_s,
                  prop=cjk_fp if cjk_fp else None)
        fact = (f"≤{pr_cut:g}: {n_r}   ({pr_cut:g}, {pd_cut:g}): {n - n_r - n_p}   "
                f"≥{pd_cut:g}: {n_p}")

    ax.bar(x, svals, width=0.72, color=bar_colors, edgecolor="none", zorder=3)
    if kwargs.get("show_values"):
        for xi, v in zip(x, svals):
            ax.text(xi, v + (1.2 if v >= 0 else -1.2), f"{v:g}",
                    ha="center", va="bottom" if v >= 0 else "top",
                    fontsize=fs_s, color="#333333")

    # 零基线 + PR/PD 阈值虚线（右端小标注）
    ax.axhline(0, color="#4A4A4A", lw=1.0, zorder=2)
    for cut, txt in ((pr_cut, f"{pr_cut:g}%"), (pd_cut, f"{pd_cut:g}%")):
        ax.axhline(cut, color="#999999", ls="--", lw=0.9, zorder=1)
        ax.text(n - 0.35, cut, txt, ha="left", va="center", fontsize=fs_s,
                color="#777777")

    ax.set_xticks(x)
    # 标签自适应：>14 例竖排（发表惯例）；>60 例按 stride 抽稀+字号收缩
    #（竖排 100 例会糊死——审查 P2-2；抽稀写入 stderr，数据完整性靠 --show-values/
    # 完整表格承担，图面保可读）
    _rot = 90 if n > 14 else 0
    _fs_x = max(4.5, fs_s * (14.0 / n if n > 14 else 1.0))
    _stride = max(1, -(-n // 50))
    _show_names = snames if _stride == 1 else         [nm if i % _stride == 0 else "" for i, nm in enumerate(snames)]
    ax.set_xticklabels(_show_names, fontsize=_fs_x, rotation=_rot, ha="center",
                       fontproperties=cjk_fp if cjk_fp and has_cjk("".join(snames)) else None)
    ax._af_category_axis = True  # 患者标识是数据：豁免刻度抽稀（同热图/forest）
    yl = str(data.get("y_label", "") or
             ("自基线最佳变化（%）" if cjk_fp else "Best change from baseline (%)"))
    ax.set_ylabel(yl, fontsize=fs,
                  fontproperties=cjk_fp if cjk_fp and has_cjk(yl) else None)
    ax.set_xlim(-0.7, n + (1.6 if n else 0))  # 右侧留阈值标注位
    # 计数事实框左下 + 白底托底（v4.8 审查 P2-1：n=1/sort=input 下柱体会穿字，
    # 全正数据时 -30% 虚线也会划过——白底 alpha 0.85 保证任何数据形态下可读）
    ax.text(0.02, 0.02, fact, transform=ax.transAxes, va="bottom", ha="left",
            fontsize=fs_s, color="#555555",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85,
                      boxstyle="round,pad=0.25"),
            zorder=5,
            fontproperties=cjk_fp if cjk_fp and has_cjk("缓解") else None)
    print(f"waterfall: {n} 例（sort={sort_mode}，缓解≤{pr_cut:g}%，进展≥{pd_cut:g}%）"
          + (f"；x 标签每 {_stride} 例显示 1 个" if _stride > 1 else "")
          + f"；{fact}", file=sys.stderr)
    apply_base_style(ax, theme)


# v4.10：RECIST 规范语义色（与 gen_waterfall 阈值分桶/类别着色同族， swimmer 复用）
_RECIST_SEMANTIC = {"CR": "#2C5F8A", "PR": "#5FA4D0", "SD": "#B8B8B8", "PD": "#D55E00"}


def reserve_bottom_band(ax, n_rows, top_pad=0.4, band=0.8):
    """v5.2 机制统一：行型横向图（y=0..n-1 倒轴）的底部浮动元素预留带——
    图例/事实框等浮动元素专属空带，防与数据行碰撞（pitfalls 类级铁律
    「浮动元素预留带」的共享实现；swimmer 事实框/dumbbell 图例两次教训沉淀）。
    倒轴语义：底部空带 = y ∈ (-band, 0)；返回该区间供调用者放置浮动元素。"""
    ax.set_ylim(n_rows + top_pad, -band)
    return (-band, 0.0)


def gen_swimmer(data, ax, theme, cjk_fp, **kwargs):
    """Swimmer plot（v4.10，第 28 号图型）：临床试验游泳图——每例受试者一条横条，
    条长=治疗/随访持续时长，按持续时长降序（经典形态，PharmaSUG/IASLC 惯例）；
    端部箭头=数据截止时仍在治疗/缓解（ongoing），条上空心圆点=里程碑事件时间
    （如首次应答）；类别着色与瀑布图同族（RECIST 规范语义色），地标参考线=竖直
    虚线。里程碑允许晚于条端（停药后应答持续的经典形态）。

    JSON: {"end": [12.3, ...](必填，>0，单位自定), "start": [0, ...](可选，默认 0，
           须 <end), "names": [...](可选), "group": [...](可选，RECIST/类别着色),
           "milestones": [[6.1], ...](可选，每例里程碑时间点列表，可为 null),
           "ongoing": [true, ...](可选，端部箭头), "ref_lines": [12, 24](可选，地标),
           "sort": "duration"(默认)|"input", "x_label": "..."(可选)}
    """
    import math as _m
    end_raw = data.get("end")
    if not (isinstance(end_raw, list) and end_raw):
        raise ValueError("swimmer: 需要 'end'（非空数值数组：每例治疗/随访持续时长，单位自定）")
    try:
        end = [float(v) for v in end_raw]
    except (TypeError, ValueError):
        raise ValueError("swimmer: end 必须全为数值")
    if not all(_m.isfinite(v) for v in end):
        raise ValueError("swimmer: end 含非有限值（NaN/±Infinity）——请清洗源数据"
                         "（数值政策：非有限值一律拒绝，不静默跳过）")
    if any(v <= 0 for v in end):
        raise ValueError("swimmer: end 必须全为正数（时长 ≤0 无意义）")
    n = len(end)
    start_raw = data.get("start")
    if start_raw is not None:
        if not isinstance(start_raw, list) or len(start_raw) != n:
            raise ValueError("swimmer: 'start' 长度必须与 end 一致")
        try:
            start = [float(v) for v in start_raw]
        except (TypeError, ValueError):
            raise ValueError("swimmer: start 必须全为数值")
        if not all(_m.isfinite(v) for v in start):
            raise ValueError("swimmer: start 含非有限值")
        bad = [i + 1 for i in range(n) if start[i] >= end[i]]
        if bad:
            raise ValueError("swimmer: start 必须小于 end（第 "
                             + ", ".join(str(b) for b in bad[:5]) + " 例违反）")
    else:
        start = [0.0] * n
    names = data.get("names")
    if names is not None and (not isinstance(names, list) or len(names) != n):
        raise ValueError("swimmer: 'names' 长度必须与 end 一致")
    group = data.get("group")
    if group is not None:
        if not isinstance(group, list) or len(group) != n:
            raise ValueError("swimmer: 'group' 长度必须与 end 一致")
        if not all(isinstance(g, (str, int, float)) and not isinstance(g, bool)
                   for g in group):
            raise ValueError("swimmer: 'group' 必须全为字符串或数值标量")
    ms_raw = data.get("milestones")
    if ms_raw is not None:
        if not isinstance(ms_raw, list) or len(ms_raw) != n:
            raise ValueError("swimmer: 'milestones' 长度必须与 end 一致（每例一个时间点数组）")
        ms = []
        for i, row in enumerate(ms_raw):
            if row is None:
                ms.append([])
                continue
            if not isinstance(row, list):
                raise ValueError(f"swimmer: milestones[{i}] 必须是时间点数组（或 null）")
            try:
                row_f = [float(v) for v in row]
            except (TypeError, ValueError):
                raise ValueError(f"swimmer: milestones[{i}] 必须全为数值")
            if not all(_m.isfinite(v) for v in row_f):
                raise ValueError(f"swimmer: milestones[{i}] 含非有限值")
            if any(v < start[i] for v in row_f):
                raise ValueError(f"swimmer: milestones[{i}] 早于该例 start（里程碑不能早于起条）")
            ms.append(row_f)
    else:
        ms = [[] for _ in range(n)]
    on_raw = data.get("ongoing")
    if on_raw is not None:
        if not isinstance(on_raw, list) or len(on_raw) != n or \
                not all(isinstance(v, bool) for v in on_raw):
            raise ValueError("swimmer: 'ongoing' 必须是与 end 等长的布尔数组"
                             "（true=数据截止时仍在治疗/缓解）")
        on = on_raw
    else:
        on = [False] * n
    ref = data.get("ref_lines")
    if ref is not None:
        if not isinstance(ref, list) or \
                not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in ref):
            raise ValueError("swimmer: 'ref_lines' 必须是数值数组（地标时间，如 [12, 24]）")
        ref = [float(v) for v in ref]
    else:
        ref = []
    sort_mode = str(data.get("sort", "duration")).strip().lower()
    if sort_mode not in ("duration", "input"):
        raise ValueError("swimmer: sort 只支持 'duration' 或 'input'")

    order = sorted(range(n), key=lambda i: (-(end[i] - start[i]), i)) \
        if sort_mode == "duration" else list(range(n))
    s_end = [end[i] for i in order]
    s_start = [start[i] for i in order]
    s_ms = [ms[i] for i in order]
    s_on = [on[i] for i in order]
    snames = [str(names[i]) if names else f"P{i+1:03d}" for i in order]
    sgroup = [str(group[i]) if group is not None else None for i in order]

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    y = np.arange(n)

    legend_handles, legend_labels = [], []
    if sgroup and group is not None:
        # 类别着色：全为 RECIST 标准类别时用规范语义色（大小写归一，同 waterfall），
        # 否则主题色按首现顺序（确定性）
        cats, cmap = [], {}
        _upper = [str(g).upper() for g in sgroup]
        if set(_upper) <= set(_RECIST_SEMANTIC):
            sgroup = _upper
            for gu in _upper:
                if gu not in cmap:
                    cmap[gu] = _RECIST_SEMANTIC[gu]
                    cats.append(gu)
        else:
            for g in sgroup:
                if g not in cmap:
                    cmap[g] = theme["colors"][len(cmap) % len(theme["colors"])]
                    cats.append(g)
        bar_colors = [cmap[g] for g in sgroup]
        legend_handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[c]) for c in cats]
        legend_labels = cats
        fact = "  ".join(f"{c} {sgroup.count(c)}" for c in cats)
    else:
        bar_colors = [theme["colors"][0]] * n
        fact = f"n={n}"
    if any(s_ms):
        legend_handles.append(plt.Line2D([], [], marker="o", ls="none", mfc="white",
                                         mec="#4A4A4A", mew=1.1, ms=4.6))
        legend_labels.append("里程碑" if cjk_fp else "Milestone")
    if any(s_on):
        legend_handles.append(plt.Line2D([], [], marker=">", ls="none",
                                         color="#4A4A4A", ms=5))
        legend_labels.append("持续中" if cjk_fp else "Ongoing")
    if legend_handles:
        # 白衬底（framealpha 0.95）：ref_lines 地标虚线可能从图例下穿过，
        # 衬底保证任何数据形态下图例内部不被切割（验收 P1 修复）
        ax.legend(legend_handles, legend_labels, loc="lower right",
                  frameon=True, framealpha=0.95, edgecolor="none",
                  fontsize=fs_s,
                  prop=cjk_fp if cjk_fp and has_cjk("".join(legend_labels)) else None)

    ax.barh(y, [e - s for e, s in zip(s_end, s_start)], left=s_start, height=0.62,
            color=bar_colors, edgecolor="none", zorder=3)
    n_ms = 0
    for i in range(n):
        for v in s_ms[i]:
            ax.plot(v, y[i], "o", mfc="white", mec="#4A4A4A", mew=1.1, ms=4.6, zorder=4)
            n_ms += 1
    n_on = sum(1 for v in s_on if v)
    for i in range(n):
        if s_on[i]:
            ax.plot(s_end[i], y[i], ">", color="#4A4A4A", ms=5, zorder=4, clip_on=False)
    for v in ref:
        ax.axvline(v, color="#999999", ls="--", lw=0.9, zorder=1)
        ax.text(v, -0.55, f"{v:g}", ha="center", va="bottom", fontsize=fs_s,
                color="#777777")

    ax.set_yticks(y)
    # 标签自适应：>24 例字号收缩（游泳图逐例条形不可抽稀——每条=一名受试者）
    _fs_y = max(4.5, fs_s * (24.0 / n if n > 24 else 1.0))
    ax.set_yticklabels(snames, fontsize=_fs_y,
                       fontproperties=cjk_fp if cjk_fp and has_cjk("".join(snames)) else None)
    ax._af_category_axis = True  # 受试者编号是数据：豁免刻度抽稀（同 waterfall）
    xl = str(data.get("x_label", "") or
             ("自基线时间（周）" if cjk_fp else "Time from baseline (weeks)"))
    ax.set_xlabel(xl, fontsize=fs,
                  fontproperties=cjk_fp if cjk_fp and has_cjk(xl) else None)
    reserve_bottom_band(ax, n, top_pad=1.1)  # 首例（最长条）在顶部；上边留 ref_lines 标注位，
    # 底部预留 ~1.6 行空带给左下事实框（sorted-desc 时底部条最短，箱体不再咬条——验收 P1）
    _x_max = max(s_end + [v for row in s_ms for v in row])
    ax.set_xlim(0, _x_max * 1.07)  # 右侧留端部箭头位
    ax.text(0.02, 0.05, fact, transform=ax.transAxes, va="bottom", ha="left",
            fontsize=fs_s, color="#555555",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85,
                      boxstyle="round,pad=0.25"), zorder=5,
            fontproperties=cjk_fp if cjk_fp and has_cjk(fact) else None)
    print(f"swimmer: {n} 例（sort={sort_mode}，持续中 {n_on} 例，里程碑 {n_ms} 个）"
          + (f"；{fact}" if sgroup and group is not None else ""), file=sys.stderr)
    apply_base_style(ax, theme)


def swimmer_alt(data, t=""):
    """v4.10：swimmer 的 --alt 文本（放本模块守 gen_figure <3400 行纪律）。"""
    end = data.get("end") or []
    n = len(end)
    start = data.get("start") or [0.0] * n
    durs = [float(e) - float(s) for e, s in zip(end, start)]
    on = data.get("ongoing") or []
    n_on = sum(1 for v in on if v)
    ms = data.get("milestones") or []
    n_ms = sum(len(r) for r in ms if isinstance(r, list))
    group = data.get("group")
    if isinstance(group, list) and group:
        import collections as _c
        cnt = _c.Counter(str(g).upper() for g in group)
        gs = "，".join(f"{k} {v}例" for k, v in cnt.items())
    else:
        gs = "未分组"
    rng = f"{min(durs):g}–{max(durs):g}" if durs else "0"
    return (f"游泳图（临床试验逐例时长），共 {n} 例，时长 {rng}（单位自定），"
            f"持续中 {n_on} 例，里程碑 {n_ms} 个，{gs}。{t}")


def validate_swimmer(data):
    """v4.10：swimmer 数据校验（返回 fatal 列表）；与 gen_swimmer 内部校验同口径，
    供 --doctor 与渲染前统一走（同 validate_waterfall 模式）。"""
    fatal = []
    end = data.get("end")
    if not (isinstance(end, list) and end):
        fatal.append("swimmer: 需要 'end'（非空数值数组：每例治疗/随访持续时长，单位自定）")
        return fatal
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in end):
        fatal.append("swimmer: end 必须全为数值")
        return fatal
    import math as _m
    if not all(_m.isfinite(float(v)) for v in end):
        fatal.append("swimmer: end 含非有限值（NaN/±Infinity）——请清洗源数据")
    elif any(float(v) <= 0 for v in end):
        fatal.append("swimmer: end 必须全为正数（时长 ≤0 无意义）")
    n = len(end)
    start = data.get("start")
    if start is not None:
        if not isinstance(start, list) or len(start) != n or \
                not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in start):
            fatal.append("swimmer: 'start' 必须是与 end 等长的数值数组")
        elif any(float(s) >= float(e) for s, e in zip(start, end)):
            fatal.append("swimmer: start 必须小于 end")
    names = data.get("names")
    if names is not None and (not isinstance(names, list) or len(names) != n):
        fatal.append("swimmer: 'names' 长度必须与 end 一致")
    group = data.get("group")
    if group is not None and (not isinstance(group, list) or len(group) != n):
        fatal.append("swimmer: 'group' 长度必须与 end 一致")
    ms = data.get("milestones")
    if ms is not None:
        if not isinstance(ms, list) or len(ms) != n:
            fatal.append("swimmer: 'milestones' 长度必须与 end 一致（每例一个时间点数组）")
        else:
            for i, row in enumerate(ms):
                if row is None:
                    continue
                if not isinstance(row, list) or \
                        not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in row):
                    fatal.append(f"swimmer: milestones[{i}] 必须是数值数组（或 null）")
                elif isinstance(start, list) and any(float(v) < float(start[i]) for v in row):
                    fatal.append(f"swimmer: milestones[{i}] 早于该例 start")
    on = data.get("ongoing")
    if on is not None and (not isinstance(on, list) or len(on) != n or
                           not all(isinstance(v, bool) for v in on)):
        fatal.append("swimmer: 'ongoing' 必须是与 end 等长的布尔数组")
    ref = data.get("ref_lines")
    if ref is not None and (not isinstance(ref, list) or
                            not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in ref)):
        fatal.append("swimmer: 'ref_lines' 必须是数值数组")
    sm = data.get("sort")
    if sm is not None and str(sm).strip().lower() not in ("duration", "input"):
        fatal.append("swimmer: sort 只支持 'duration' 或 'input'")
    return fatal


def gen_dual_axis(data, ax, theme, cjk_fp, **kwargs):
    """Dual Y-axis chart, canonical 左柱右线 form (v3.10): left-axis series draw
    as BARS, right-axis series as dashed LINES — override per side with data keys
    left_type/right_type ("bar"|"line"). The merged legend covers BOTH axes and is
    drawn frameless inside a reserved top band so it never occludes peaks (v3.10
    A2/A4 修复); --legend-loc / --legend-outside still honored."""
    labels = data.get("labels", data.get("x", []))
    left_series = data.get("left", data.get("y1", {}))  # {"CRP (mg/L)": [5, 8, 12, ...]}
    right_series = data.get("right", data.get("y2", {}))  # {"DAS28": [3.2, 4.1, 5.6, ...]}
    left_errors = data.get("left_errors", data.get("y1_errors", {}))
    right_errors = data.get("right_errors", data.get("y2_errors", {}))
    left_ylabel = data.get("left_ylabel", "")
    right_ylabel = data.get("right_ylabel", "")
    left_type = str(data.get("left_type", "bar")).strip().lower()
    right_type = str(data.get("right_type", "line")).strip().lower()
    if left_type not in ("bar", "line"):
        left_type = "bar"
    if right_type not in ("bar", "line"):
        right_type = "line"

    def _check_series_dict(sd, which):
        if not isinstance(sd, dict):
            raise ValueError(f"dual_axis: {which} must be a dict of {{series_name: [values]}}")
        for k, v in sd.items():
            if not isinstance(v, (list, tuple)) or not all(isinstance(x, (int, float)) for x in v):
                raise ValueError(
                    f"dual_axis: {which}['{k}'] must be a numeric list. "
                    f"Wrong format? Use {{\"{which}\": {{\"系列名\": [值, ...]}}}} — not "
                    f"{{\"name\": ..., \"values\": ...}}.")
    _check_series_dict(left_series, "left")
    _check_series_dict(right_series, "right")

    markers = ['o', 's', 'D', '^', 'v', 'p', '*', 'h']
    x = np.arange(len(labels)) if not any(isinstance(l, (int, float)) for l in labels) else np.array(labels, dtype=float)

    # Create second axis
    ax2 = ax.twinx()

    # Plot left axis series（v3.10：默认柱状——经典左柱右线形态）
    n_left = len(left_series)
    n_right = len(right_series)
    _label_all = (n_left + n_right) > 1  # 唯一系列不设 label（图例抑制）
    if left_type == "bar":
        w_left = 0.72 / max(n_left, 1)
        for i, (name, values) in enumerate(left_series.items()):
            c = theme["colors"][i % len(theme["colors"])]
            offs = (i - (n_left - 1) / 2) * w_left
            errs = left_errors.get(name) or None
            if errs is not None and not all(isinstance(e, (int, float)) for e in errs):
                errs = None
            ax.bar(x + offs, values, w_left * 0.9, yerr=errs,
                   color=c, edgecolor='white', linewidth=0.5, capsize=3,
                   error_kw={'linewidth': 1},
                   label=name if _label_all else None, zorder=2.5)
    else:
        for i, (name, values) in enumerate(left_series.items()):
            c = theme["colors"][i % len(theme["colors"])]
            mk = markers[i % len(markers)]
            ax.plot(x, values, color=c, marker=mk, markersize=6, linewidth=2,
                    label=name if _label_all else None, zorder=3)
            if name in left_errors and left_errors[name]:
                errs = left_errors[name]
                lower = [v - e for v, e in zip(values, errs)]
                upper = [v + e for v, e in zip(values, errs)]
                ax.fill_between(x, lower, upper, color=c, alpha=0.15, zorder=2)

    # Plot right axis series
    right_colors = ['#D55E00', '#CC79A7', '#0072B2', '#009E73', '#F0E442']  # distinct from left
    if theme.get("colorblind_safe"):
        # Use different Okabe-Ito colors for right axis
        offset = len(left_series)
        right_colors = [theme["colors"][(offset + j) % len(theme["colors"])] for j in range(5)]

    if right_type == "bar":
        w_right = 0.72 / max(n_right, 1)
        for i, (name, values) in enumerate(right_series.items()):
            c = right_colors[i % len(right_colors)]
            offs = (i - (n_right - 1) / 2) * w_right
            errs = right_errors.get(name) or None
            if errs is not None and not all(isinstance(e, (int, float)) for e in errs):
                errs = None
            ax2.bar(x + offs, values, w_right * 0.9, yerr=errs,
                    color=c, edgecolor='white', linewidth=0.5, capsize=3,
                    error_kw={'linewidth': 1},
                    label=name if _label_all else None, zorder=2.5)
    else:
        for i, (name, values) in enumerate(right_series.items()):
            c = right_colors[i % len(right_colors)]
            mk = markers[(n_left + i) % len(markers)]
            ax2.plot(x, values, color=c, marker=mk, markersize=6, linewidth=2,
                     linestyle='--', label=name if _label_all else None, zorder=3)
            if name in right_errors and right_errors[name]:
                errs = right_errors[name]
                lower = [v - e for v, e in zip(values, errs)]
                upper = [v + e for v, e in zip(values, errs)]
                ax2.fill_between(x, lower, upper, color=c, alpha=0.15, zorder=2)

    # Style right axis
    ax2.spines['right'].set_visible(True)
    ax2.tick_params(axis='y', labelsize=theme["font_size"] - 1)
    ax2.grid(False)  # no grid on right axis

    # Set x-axis labels
    if not any(isinstance(l, (int, float)) for l in labels):
        ax.set_xticks(x)
        use_cjk = cjk_fp and any(has_cjk(l) for l in labels)
        ax.set_xticklabels(labels, fontsize=theme["font_size"] - 1,
                           fontproperties=cjk_fp if use_cjk else None)

    # Axis labels
    if left_ylabel:
        ax.set_ylabel(left_ylabel, fontsize=theme["font_size"],
                      fontproperties=cjk_fp if cjk_fp and has_cjk(left_ylabel) else None)
        _ensure_ylabel_clear(ax)
    if right_ylabel:
        ax2.set_ylabel(right_ylabel, fontsize=theme["font_size"],
                       fontproperties=cjk_fp if cjk_fp and has_cjk(right_ylabel) else None)
        _ensure_ylabel_clear(ax2)

    # Combine legends from both axes（v3.10 A2/A4：显式合并+不遮挡）
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    handles, lbls = lines1 + lines2, labels1 + labels2
    # v3.10：可选轴下限覆盖（如 right_floor=35 让百分比右轴整数起算——投稿规范；默认保持 5% 边距）
    for _key, _ax in (("left_floor", ax), ("right_floor", ax2)):
        _fl = data.get(_key)
        if isinstance(_fl, (int, float)) and not isinstance(_fl, bool):
            _lo, _hi = _ax.get_ylim()
            if _fl < _hi:
                _ax.set_ylim(float(_fl), _hi)
            else:
                print(f"WARNING: dual_axis {_key}={_fl} 不小于当前上限 {_hi:.4g}，已忽略",
                      file=sys.stderr)
    if handles:
        if kwargs.get("legend_outside"):
            ax.legend(handles, lbls, fontsize=theme["font_size"] - 1,
                      loc='lower center', bbox_to_anchor=(0.5, 1.02),
                      ncol=min(len(lbls), 4), frameon=False,
                      prop=cjk_fp if cjk_fp else None)
        elif kwargs.get("legend_loc"):
            ax.legend(handles, lbls, fontsize=theme["font_size"] - 1,
                      loc=kwargs["legend_loc"], framealpha=0.9,
                      prop=cjk_fp if cjk_fp else None)
        else:
            # 默认：左右轴各留顶部预留带，图例嵌入预留区（无边框，物理不遮数据）
            for _a in (ax, ax2):
                _lo, _hi = _a.get_ylim()
                if _hi > _lo:
                    _a.set_ylim(_lo, _hi + (_hi - _lo) * (0.18 if len(lbls) <= 4 else 0.28))
            ax.legend(handles, lbls, fontsize=theme["font_size"] - 1,
                      loc='upper center', ncol=min(len(lbls), 4), frameon=False,
                      prop=cjk_fp if cjk_fp else None)

    # Store ax2 reference for downstream use
    return ax2


def gen_composite(data, ax, theme, cjk_fp, **kwargs):
    """Multi-panel composite figure (e.g., Panel A + B + C for journal figures).

    JSON format:
    {
      "layout": [rows, cols],  // e.g. [1, 3] or [2, 2]
      "panels": [
        {
          "title": "Panel A: ...",
          "type": "bar",        // any chart type from GENERATORS
          "data": { ... },      // data for that chart type
          "xlabel": "...", "ylabel": "...",
          "pos": [row, col]     // grid position (0-indexed)
        },
        ...
      ]
    }
    """
    import matplotlib.gridspec as gridspec

    layout = data.get("layout", [1, 2])
    n_rows, n_cols = layout[0], layout[1]
    panels = data.get("panels", [])

    if not panels:
        return None

    fig = ax.figure
    # Clear the default axis created by plt.subplots
    ax.remove()

    # v7.8.0 hero_panel：主面板跨全行+1.35:1 双列（B1 规格——跨工具调研沉淀，
    # 实现自有）。hero 优先级高于 pos/span：合法时布局由本块接管，两者忽略。
    # 仅 3-6 面板支持；>6 或索引非法打 WARNING 回退均等网格（不静默）。
    _hero_ok, _hp = hero_panel_mode(data, panels)
    if _hp is not None and not _hero_ok:
        _why = ("仅 3-6 面板支持" if not (3 <= len(panels) <= 6)
                else "须为 0 起始的整数面板序号且在范围内")
        print(f"WARNING: hero_panel={_hp!r} 未启用（{_why}）——回退均等网格", file=sys.stderr)
    if _hero_ok:
        _n_aux = len(panels) - 1
        gs = gridspec.GridSpec(_n_aux, 2, figure=fig, width_ratios=[1.35, 1.0],
                               hspace=0.6, wspace=0.3,
                               left=0.08, right=0.95,
                               top=0.72 if data.get("suptitle") else 0.92,
                               bottom=0.13 if data.get("source_note") else 0.08)
        print(f"[hero] hero_panel={_hp}（{len(panels)} 面板：主面板跨全行 "
              f"width_ratios=[1.35, 1.0]，辅面板右列纵排）", file=sys.stderr)
    else:
        gs = gridspec.GridSpec(n_rows, n_cols, figure=fig,
                               hspace=0.35, wspace=0.3,
                               left=0.08, right=0.95,
                               top=0.72 if data.get("suptitle") else 0.92,
                               bottom=0.13 if data.get("source_note") else 0.08)

    # v4.1 自动面板标签（期刊 A/B/C 规范自动化）："panel_labels": true → 按
    # pos 行序自动加粗 A/B/C…；传数组（如 ["I","II"]）自定义序列；缺省 false
    # （兼容既有图，避免与手写 "Panel A:" 类标题重复标注）。
    panel_labels = data.get("panel_labels", False)
    _pl_seq = panel_labels if isinstance(panel_labels, list) else None
    _pl_on = bool(panel_labels)
    if _hero_ok:
        # 标签序=阅读序：hero（左列跨全行）先，辅面板右列自上而下按数组序
        _pos_order = [_hp] + [i for i in range(len(panels)) if i != _hp]
    else:
        _pos_order = sorted(range(len(panels)),
                            key=lambda i: (panels[i].get("pos", [9, 9])[0],
                                           panels[i].get("pos", [9, 9])[1]))
    _pl_of = {idx: k for k, idx in enumerate(_pos_order)}
    _aux_slot = 0  # hero 模式右列下一空槽
    _panel_axes = []  # (ax, ylabel) 采集——share_y 统一用（v5.6）

    for _pi, panel in enumerate(panels):
        pos = panel.get("pos", [0, 0])
        panel_type = panel.get("type", "bar")
        panel_data = panel.get("data", {})

        if _hero_ok:
            # hero 优先级高于 span/pos：主面板左列跨全行，辅面板右列逐行占位
            if _pi == _hp:
                sub_ax = fig.add_subplot(gs[:, 0])
            else:
                sub_ax = fig.add_subplot(gs[_aux_slot, 1])
                _aux_slot += 1
        else:
            _rs, _cs = panel.get("span", [1, 1]) or [1, 1]
            try:
                _rs, _cs = int(_rs), int(_cs)
            except (TypeError, ValueError):
                _rs = _cs = 1
            _rs = max(1, min(_rs, n_rows - pos[0]))
            _cs = max(1, min(_cs, n_cols - pos[1]))
            sub_ax = fig.add_subplot(gs[pos[0]:pos[0] + _rs, pos[1]:pos[1] + _cs])

        # Get the generator function
        gen_func = GENERATORS.get(panel_type)
        if gen_func is None:
            sub_ax.text(0.5, 0.5, f"Unknown type: {panel_type}",
                        ha='center', va='center', transform=sub_ax.transAxes)
            continue
        # v4.7：自管类型不可作面板（validate 已前置拦截；此处兜底 Python API 直调路径）
        if panel_type in ("composite", "diagram", "upset"):
            sub_ax.text(0.5, 0.5, f"'{panel_type}' 不能作为面板（自管图型）",
                        ha='center', va='center', transform=sub_ax.transAxes,
                        fontproperties=cjk_fp if cjk_fp else None)
            continue

        # Pass through relevant kwargs
        panel_kwargs = {
            "show_values": panel.get("show_values", kwargs.get("show_values", False)),
            "trend": panel.get("trend", kwargs.get("trend", True)),
            # B3(v2.7)：hbar/horizontal_bar 面板自动横排（与主入口同规则；实战坑：composite
            # 内 hbar 被当竖 bar 渲染，用户被迫改用 bar+horizontal 绕行）
            "horizontal": panel.get("horizontal", False)
                          or panel_type in ("hbar", "horizontal_bar"),
            "hatch": panel.get("hatch", False),
            "alternate": panel.get("alternate", False),
            "arena": panel.get("arena", kwargs.get("arena")),  # v7.5 面板级竞技场风格
            "show_ratio": panel.get("show_ratio", False),
            "cmap": panel.get("cmap", kwargs.get("cmap")),
            "vmin": panel.get("vmin", kwargs.get("vmin")),
            # v3.4.1（55 线发现+82 等效移植）：KM 面板 median_auto 面板级透传——
            # 此前白名单缺失，composite 里 median_auto:false 被静默忽略（单位错标复发）
            "median_auto": panel.get("median_auto", kwargs.get("median_auto", True)),
            "stats_bootstrap": panel.get("stats_bootstrap", kwargs.get("stats_bootstrap", False)),
            "direct_label": panel.get("direct_label", kwargs.get("direct_label", False)),
            "vmax": panel.get("vmax", kwargs.get("vmax")),
        }

        extra = gen_func(panel_data, sub_ax, theme, cjk_fp, **panel_kwargs)
        apply_base_style(sub_ax, theme)

        # v4.1 自动面板标签：左上角加粗 A/B/C…（轴外，永不压数据）
        if _pl_on:
            _lab = (_pl_seq[_pl_of[_pi]] if _pl_seq
                    else chr(65 + _pl_of[_pi]))
            sub_ax.text(-0.08, 1.05, str(_lab), transform=sub_ax.transAxes,
                        fontsize=theme["font_size"] + 3, fontweight="bold",
                        ha="right", va="bottom",
                        fontproperties=cjk_fp if cjk_fp and has_cjk(str(_lab)) else None)

        # Panel-specific labels
        ptitle = panel.get("title", "")
        psub = panel.get("subtitle", "")
        if ptitle:
            sub_ax.set_title(ptitle, fontsize=theme["font_size"], fontweight='bold',
                             pad=34 if psub else 8,
                             fontproperties=cjk_fp if cjk_fp and has_cjk(ptitle) else None)
        if psub:
            sub_ax.text(0.5, 1.02, psub, transform=sub_ax.transAxes, ha='center',
                        va='bottom', fontsize=theme["font_size"] - 2, color="#9A9A9A",
                        fontproperties=cjk_fp if cjk_fp and has_cjk(psub) else None)
        if panel.get("xlabel"):
            sub_ax.set_xlabel(panel["xlabel"], fontsize=theme["font_size"] - 1,
                              fontproperties=cjk_fp if cjk_fp and has_cjk(panel["xlabel"]) else None)
        if panel.get("ylabel"):
            sub_ax.set_ylabel(panel["ylabel"], fontsize=theme["font_size"] - 1,
                              fontproperties=cjk_fp if cjk_fp and has_cjk(panel["ylabel"]) else None)
            _ensure_ylabel_clear(sub_ax)
        _panel_axes.append((sub_ax, (sub_ax.get_ylabel() or "").strip()))

        # Legend for panel
        show_legend = panel.get("legend", True)
        if show_legend and sub_ax.get_legend_handles_labels()[1]:
            sub_ax.legend(fontsize=theme["font_size"] - 2, loc='best', framealpha=0.9,
                          prop=cjk_fp if cjk_fp else None)

        # Colorbar for heatmap panels
        if extra is not None and hasattr(extra, 'get_cmap'):
            cbar = fig.colorbar(extra, ax=sub_ax, shrink=0.8)

    # v5.6 composite 共享尺度自动统一：share_y=true 时，同 ylabel（同变量语义）
    # 的面板 y 轴统一到全体范围（doctor 预检「范围差>5 倍」提示的机制出口）。
    if bool(data.get("share_y", False)):
        _groups = {}
        for _a, _yl in _panel_axes:
            if _yl:
                _groups.setdefault(_yl, []).append(_a)
        for _yl, _axs in _groups.items():
            if len(_axs) < 2:
                continue
            _log = any(a.get_yscale() == "log" for a in _axs)
            if _log:
                for a in _axs:
                    a.set_yscale("log")
                _lo = min(max(a.get_ylim()[0], 1e-12) for a in _axs)
                _hi = max(a.get_ylim()[1] for a in _axs)
            else:
                _lo = min(a.get_ylim()[0] for a in _axs)
                _hi = max(a.get_ylim()[1] for a in _axs)
            if not (_hi > _lo):
                continue
            for a in _axs:
                a.set_ylim(_lo, _hi)
            print(f"composite: share_y 已统一「{_yl}」×{len(_axs)} 面板 y 轴"
                  f"（{'log ' if _log else ''}{_lo:.4g}~{_hi:.4g}）", file=sys.stderr)

    # v7.6 手绘参考图形态件：单行多面板间虚线分隔 + json suptitle 总标题（左上粗体）
    if data.get("suptitle"):
        _st = str(data["suptitle"])
        fig.text(0.02, 0.995, _st, fontsize=theme["font_size"] + 6,
                 fontweight="bold", color="#1F4E79", ha="left", va="top",
                 fontproperties=cjk_fp if cjk_fp and has_cjk(_st) else None)
        fig.subplots_adjust(top=0.72)  # 面板标题层整体让出总标题层（参考图两级标题）
    if data.get("source_note"):
        _sn = str(data["source_note"])
        fig.text(0.02, 0.012, _sn, fontsize=theme["font_size"] - 2,
                 color="#9A9A9A", ha="left", va="bottom",
                 fontproperties=cjk_fp if cjk_fp and has_cjk(_sn) else None)
    _n_panels = len(data.get("panels", []))
    # v7.8.0：分隔虚线假设 [1, N] 横排布局（k/N 处竖线）——hero 模式为双列纵向
    # 布局，旧坐标会把虚线横穿主面板与来源行（视觉门 FAIL 实锤），跳过。
    if _n_panels > 1 and not _hero_ok:
        for _k in range(1, _n_panels):
            fig.add_artist(plt.Line2D([_k / _n_panels, _k / _n_panels],
                                      [0.02, 0.96], transform=fig.transFigure,
                                      ls="--", color="#B8B8B8", lw=1.2, zorder=0))

    return "composite"  # signal to main() that figure is already built


def gen_diagram(data, ax, theme, cjk_fp, **kwargs):
    """Architecture/flow diagram（v8.0.0 起布局/路由委托 af_flow 引擎——
    磁吸逐段箭头+lane 回边+标签避让+文本自适应+画布裁剪+三层 bbox 闸）。

    JSON（坐标可选——不给 x/y/w/h 时按语义自动布局）：
      {"background": "light",
       "blocks": [{"id":"A","label":"Input","sublabel":"...","x":0,"y":0,"w":2,"h":1,
                   "color":"#56B4E9","shape":"round|rect"}, ...],
       "arrows": [{"from":"A","to":"B","label":"flow","style":"->","dashed":true,
                   "color":"..."}, ...],
       "groups": [{"blocks":["A","B"],"label":"Phase 1","color":"#009E73","style":"dashed"}],
       "annotations": [{"text":"...","x":1,"y":-1,"fontsize":9,"color":"..."}]}
    kwargs: gate="basic"|"strict"（strict=三层 bbox 断言，违规 exit 2）、
            orthogonal=True（曼哈顿折线）、autolayout=True（无坐标块自动横链布局）。"""
    import af_flow
    blocks = data.get("blocks", [])
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("diagram: 需要 'blocks'（非空块对象列表）")
    for b in blocks:
        for k in ("id",):
            if k not in b:
                raise ValueError(f"diagram: blocks 每项须含 '{k}'")
        if not all(k in b for k in ("x", "y", "w", "h")):
            if kwargs.get("autolayout") or not any(
                    "x" in bb for bb in blocks):
                blocks = af_flow.layout_semantic(
                    [{"id": bb.get("id"), "label": bb.get("label", bb.get("id")),
                      "sublabel": bb.get("sublabel"), "color": bb.get("color"),
                      "shape": bb.get("shape", "round")} for bb in blocks],
                    data.get("arrows", []), layout="chain",
                    ax=ax, fs=theme.get("font_size", 11), cjk_fp=cjk_fp)
                break
            else:
                raise ValueError("diagram: blocks 缺 x/y/w/h 坐标（或整组省略以启用自动布局）")
    violations, ratio = af_flow.render(
        ax, ax.figure, blocks, data.get("arrows", []),
        groups=data.get("groups", []), annotations=data.get("annotations", []),
        theme=theme, cjk_fp=cjk_fp, gate=kwargs.get("gate", "basic"),
        orthogonal=bool(kwargs.get("orthogonal")),
        hops=bool(kwargs.get("flow_hops")))
    if kwargs.get("gate") == "strict" and violations:
        print("GATE STRICT FAIL（三层 bbox 闸违规清单）:", file=sys.stderr)
        for v in violations:
            print(f"  ✗ {v}", file=sys.stderr)
        raise ValueError(f"diagram: strict 闸 {len(violations)} 项违规——拒绝交付")
    print(f"flow: {len(blocks)} 节点 {len(data.get('arrows', []))} 边"
          f"（内容占比 {ratio:.0%}）", file=sys.stderr)
    return "diagram"


def gen_flow(data, ax, theme, cjk_fp, **kwargs):
    """flow（v8.0.0，第 42 号图型）：语义 JSON 流程图——用户只给节点/边语义，
    引擎自动布局（横链/分层）+磁吸逐段箭头+lane 回边+标签避让+文本自适应+裁剪。

    JSON: {"layout": "chain"|"layered", "direction": "TB"|"LR",
           "nodes": [{"id":"A","label":"...","sublabel":"...","color":"#...",
                      "shape":"round|rect"}, ...],
           "edges": [{"from":"A","to":"B","label":"...","dashed":true,"color":"..."}],
           "groups": [...], "annotations": [...], "title": "..."}"""
    import af_flow
    nodes = data.get("nodes")
    edges = data.get("edges", [])
    if not isinstance(nodes, list) or len(nodes) < 2:
        raise ValueError("flow: 需要 'nodes'（≥2 个节点对象）")
    for n in nodes:
        if not n.get("id"):
            raise ValueError("flow: nodes 每项须含 'id'")
    if kwargs.get("palette") and all(n.get("color") for n in nodes):
        # [ignored] 透明告知承诺：显式 color 优先于 --palette（合法优先级），
        # 但全量覆盖时 palette 实际未参与——必须显式告知，禁止静默无效。
        print("[ignored] --palette 未生效：所有节点已带显式 color（显式优先）。"
              "如需注入配色，移除节点 color 字段即可", file=sys.stderr)
    # v8.0.4 flow 专属默认系列（Teal Coral 顶刊精修，源自降饱和派生）：
    # [0]=主链基色（引擎同族明度阶梯）[-1]=终点强调色，中间=分支浅填充。
    # --palette 时 [0]/[-1] 同规则生效——任意注入板自动获得角色化雅致分配。
    _FLOW_SERIES = ["#336672", "#A7C4C6", "#BF8078"]
    theme = dict(theme)
    theme["colors"] = kwargs.get("palette") or _FLOW_SERIES
    layout = str(data.get("layout", "chain")).strip().lower()
    if layout not in ("chain", "layered", "snake", "swimlane"):
        raise ValueError("flow: layout 只支持 'chain' | 'layered' | 'snake' | 'swimlane'")
    if layout == "swimlane" and not data.get("lanes"):
        raise ValueError("flow: layout=swimlane 需要 'lanes'（名称列表）")
    _cols = data.get("columns")
    if _cols is not None:
        try:
            _cols = int(_cols)
        except (TypeError, ValueError):
            raise ValueError(f"flow: columns 需为整数，收到 {_cols!r}")
        if not (2 <= _cols <= 8):
            raise ValueError(f"flow: columns 超出许可区间 [2, 8]，收到 {_cols}")
    direction = str(data.get("direction", "TB")).strip().upper()
    if direction not in ("TB", "LR"):
        raise ValueError("flow: direction 只支持 'TB' | 'LR'")
    # 数据级字号（v8.0.4）：语义 JSON 可携 font_size——论文图按目标排版宽度
    # 反推作者字号（如 12in 宽链图投 6.5in 版心 → font_size 16 落版后 ≈8pt）
    _fs = data.get("font_size") or theme.get("font_size", 11)
    try:
        _fs = float(_fs)
    except (TypeError, ValueError):
        raise ValueError(f"flow: font_size 需为数值，收到 {_fs!r}")
    if not (6 <= _fs <= 40):
        raise ValueError(f"flow: font_size 超出许可区间 [6, 40]，收到 {_fs}")
    theme["font_size"] = _fs   # render() 内部同样从 theme 读 fs，保持同源
    blocks = af_flow.layout_semantic(nodes, edges, layout=layout, direction=direction,
                                     columns=_cols, lanes=data.get("lanes"),
                                     ax=ax, fs=_fs, cjk_fp=cjk_fp)
    arrows = [{"from": e["from"], "to": e["to"], **{k: v for k, v in e.items()
               if k in ("label", "dashed", "color", "label_color", "thick",
                        "bidirectional", "open")}}
              for e in edges]
    violations, ratio = af_flow.render(
        ax, ax.figure, blocks, arrows,
        groups=data.get("groups", []), annotations=data.get("annotations", []),
        theme=theme, cjk_fp=cjk_fp, gate=kwargs.get("gate", "basic"),
        orthogonal=bool(kwargs.get("orthogonal")),
        legend_flag=data.get("legend"), hops=bool(kwargs.get("flow_hops")))
    if kwargs.get("gate") == "strict" and violations:
        print("GATE STRICT FAIL（三层 bbox 闸违规清单）:", file=sys.stderr)
        for v in violations:
            print(f"  ✗ {v}", file=sys.stderr)
        raise ValueError(f"flow: strict 闸 {len(violations)} 项违规——拒绝交付")
    n_back = sum(1 for e in edges if e.get("dashed"))
    print(f"flow: {len(nodes)} 节点 {len(edges)} 边（layout={layout}，虚线回边 {n_back}，"
          f"内容占比 {ratio:.0%}）", file=sys.stderr)
    return "diagram"


# ── PRISMA 2020 flow diagram (v2.1) ───────────────────────────────────

PRISMA_LABELS = {
    "en": {
        "identification": "Identification", "screening": "Screening", "included": "Included",
        "identified": "Records identified from\ndatabases",
        "duplicates": "Records removed before\nscreening (duplicates)",
        "screened": "Records screened",
        "excluded": "Records excluded",
        "sought": "Reports sought for\nretrieval",
        "not_retrieved": "Reports not retrieved",
        "assessed": "Reports assessed for\neligibility",
        "reasons": "Reports excluded:",
        "included_box": "Studies included in\nreview",
    },
    "zh": {
        "identification": "识别", "screening": "筛选", "included": "纳入",
        "identified": "数据库检索获得的\n记录",
        "duplicates": "初筛前剔除的记录\n（重复文献）",
        "screened": "初筛的记录",
        "excluded": "初筛排除",
        "sought": "寻求获取的报告",
        "not_retrieved": "未能获取的报告",
        "assessed": "进行合格性评估\n的报告",
        "reasons": "排除的报告：",
        "included_box": "纳入综述的研究",
    },
}


def gen_prisma(data, ax, theme, cjk_fp, **kwargs):
    """PRISMA 2020 systematic-review flow diagram.

    JSON format (counts must add up; validate_data() gates arithmetic):
    {
      "records_identified": 128,       // required
      "duplicates_removed": 23,
      "records_screened": 105,         // default: identified - duplicates
      "records_excluded": 61,
      "reports_sought": 44,            // default: screened - excluded
      "reports_not_retrieved": 3,
      "reports_assessed": 41,          // default: sought - not_retrieved
      "exclusion_reasons": {"Wrong population": 5, "Wrong intervention": 7},
      "studies_included": 25,          // required
      "lang": "en"                     // or "zh" (standard Chinese wording)
    }
    Layout: PRISMA 2020 three-phase spine (Identification / Screening /
    Included) with exclusion boxes to the right, per the official template.
    """
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

    lang = data.get("lang", "en")
    L = PRISMA_LABELS.get(lang, PRISMA_LABELS["en"])

    def _n(key):
        v = data.get(key)
        return v if isinstance(v, int) and not isinstance(v, bool) else 0

    identified = _n("records_identified")
    dup = _n("duplicates_removed")
    screened = data.get("records_screened")
    screened = (identified - dup) if not isinstance(screened, int) else screened
    excluded = _n("records_excluded")
    sought = data.get("reports_sought")
    sought = (screened - excluded) if not isinstance(sought, int) else sought
    not_ret = _n("reports_not_retrieved")
    assessed = data.get("reports_assessed")
    assessed = (sought - not_ret) if not isinstance(assessed, int) else assessed
    reasons = data.get("exclusion_reasons") or {}
    included = _n("studies_included")

    spine_color = theme["colors"][0]
    final_color = theme["colors"][1] if len(theme["colors"]) > 1 else spine_color
    side_face, side_edge, text_color = "#F2F2F2", "#8A8A8A", "#1a1a1a"
    arrow_color = "#555555"
    fs = theme["font_size"]

    def _fp(*texts):
        return cjk_fp if cjk_fp and any(has_cjk(t) for t in texts) else None

    # ── geometry (data units; aspect equal) ──
    SW, BW = 4.6, 4.4                 # spine / side box widths
    SX, XX = 0.0, 7.4                 # x origins
    GAP = 0.78                        # vertical gap
    n_reasons = max(1, len(reasons))
    # 内容感知盒高：双行中文标签+计数行在固定盒高下会溢出框体——
    # 盒高 = 标签行数×行高 + 计数行 + 内边距，行高随字号缩放
    _lh = 0.62 * max(0.8, fs / 8.0)
    def _box_h(label):
        return max(1.15, (label.count(chr(10)) + 1) * _lh + 0.85)
    BH_BY = {n: _box_h(L["included_box"] if n == "included" else L[n])
             for n in ("identified", "screened", "sought", "assessed", "included")}
    BH = max(BH_BY.values())
    RH = max(BH, 0.95 + 0.42 * n_reasons * max(0.8, fs / 8.0))

    order = ["identified", "screened", "sought", "assessed", "included"]
    ys = {}
    top = 10.0
    y = top
    for name in order:
        ys[name] = y - BH_BY[name]
        y -= (BH_BY[name] + GAP)

    def _cy(name):
        return ys[name] + BH / 2

    side = {
        "duplicates": (ys["identified"] + ys["screened"]) / 2 + BH / 2 - BH,
        "excluded": (ys["screened"] + ys["sought"]) / 2 + BH / 2 - BH,
        "not_retrieved": (ys["sought"] + ys["assessed"]) / 2 + BH / 2 - BH,
    }
    show_dup = not (dup == 0 and "duplicates_removed" not in data)
    show_notret = not (not_ret == 0 and "reports_not_retrieved" not in data)
    # reasons box: top-anchored to the assessed row's midline, growing
    # downward — this leaves the sought/assessed slot free for the
    # not-retrieved side box (official PRISMA 2020 arrangement)
    y_reasons = ys["assessed"] + BH_BY["assessed"] * 0.5 - RH
    implied_excluded = max(assessed - included, 0)

    # ── limits (set early so side-box text can be measured in data units) ──
    xmin, ymin = SX - 2.3, min(ys["included"], y_reasons) - 1.1
    ymax = top + 0.75
    ax.set_xlim(xmin, XX + BW + 0.5)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.axis("off")
    fig = ax.get_figure()
    # 主框文字实测自愈：盒高系数是估算可能低估——以最终几何实测文字高度，
    # 超出盒体就放大该盒并整体重排，迭代到全部装下（同侧框 auto-fit 思路）
    if fig is not None:
        for _round in range(4):
            fig.canvas.draw()
            _rend = fig.canvas.get_renderer()
            _inv = ax.transData.inverted()
            grew = False
            for _name in order:
                _label = L["included_box"] if _name == "included" else L[_name]
                _t = ax.text(0.5, 0.5, _label + "\n" + "n = 000",
                             fontsize=fs - 1, fontweight="bold",
                             fontproperties=_fp(_label))
                _need = _t.get_window_extent(renderer=_rend).transformed(_inv).height + 0.30
                _t.remove()
                if _need > BH_BY[_name] * 1.02:
                    BH_BY[_name] = _need
                    grew = True
            if not grew:
                break
            BH = max(BH_BY.values())
            RH = max(RH, BH)
            _y = top
            for _name in order:
                ys[_name] = _y - BH_BY[_name]
                _y -= (BH_BY[_name] + GAP)
            y_reasons = ys["assessed"] + BH_BY["assessed"] * 0.5 - RH
            ymin = min(ys["included"], y_reasons) - 1.1
            ax.set_ylim(ymin, ymax)


    # ── side-box auto-fit: measure the real rendered width of every side-box
    # line, widen the boxes to fit, and wrap reason lines only as a last
    # resort (growing the box height to match). The old fixed-width box let
    # long exclusion reasons spill outside the frame.
    BW_MAX = 7.2
    reason_items = [(str(r), n) for r, n in reasons.items()]
    item_display = {r: [f"· {r} (n = {n})"] for r, n in reason_items}
    specs = []
    if show_dup:
        specs.append((L["duplicates"], fs - 1, _fp(L["duplicates"])))
    specs.append((L["excluded"], fs - 1, _fp(L["excluded"])))
    if show_notret:
        specs.append((L["not_retrieved"], fs - 1, _fp(L["not_retrieved"])))
    specs.append((L["reasons"], fs - 1, _fp(L["reasons"])))
    for r, n in reason_items:
        specs.append((item_display[r][0], fs - 1.5, _fp(r, str(n))))

    if specs and fig is not None:
        # Iterate to a fixed point: set the final geometry FIRST, then
        # measure, because data-unit widths depend on xlim. Widening BW
        # changes the span, which changes the measurement — so each pass
        # measures under the span it proposes, until the width stops moving.
        widths = {}
        need = BW
        for _pass in range(3):
            ax.set_xlim(xmin, XX + BW + 0.5)
            ax.set_ylim(ymin, ymax)
            meas = [ax.text(XX + BW / 2, (ymin + ymax) / 2, txt, fontsize=fsize,
                            fontproperties=fp, alpha=0, zorder=-10)
                    for txt, fsize, fp in specs]
            fig.canvas.draw()
            ren = fig.canvas.get_renderer()
            inv = ax.transData.inverted()
            widths = {}
            for t, (txt, _f, _p) in zip(meas, specs):
                bb = t.get_window_extent(ren)
                widths[txt] = abs(inv.transform((bb.x1, bb.y1))[0]
                                  - inv.transform((bb.x0, bb.y0))[0])
                t.remove()
            need = max(widths.values()) + 0.7 if widths else BW
            BW_new = min(max(BW, need), BW_MAX)
            if BW_new == BW:
                break
            BW = BW_new
        if need > BW_MAX:
            import textwrap

            def _block_w(block, fsize, fp):
                t = ax.text(XX + BW / 2, (ymin + ymax) / 2, block, fontsize=fsize,
                            fontproperties=fp, alpha=0, zorder=-10)
                fig.canvas.draw()
                bb = t.get_window_extent(fig.canvas.get_renderer())
                t.remove()
                return abs(inv.transform((bb.x1, bb.y1))[0]
                           - inv.transform((bb.x0, bb.y0))[0])

            for r, n in reason_items:
                line = item_display[r][0]
                if widths.get(line, 0) + 0.7 > BW_MAX:
                    per = max(8, int(len(line) * (BW_MAX - 0.7) / max(widths[line], 1e-6)))
                    for _attempt in range(4):
                        wrapped = textwrap.wrap(line, per) or [line]
                        display = [wrapped[0]] + ["   " + s for s in wrapped[1:]]
                        if _block_w("\n".join(display), fs - 1.5,
                                    _fp(r, str(n))) + 0.7 <= BW_MAX:
                            break
                        per = max(6, int(per * 0.8))
                    item_display[r] = display
            extra = sum(len(v) - 1 for v in item_display.values())
            RH += 0.30 * extra
            y_reasons = ys["assessed"] + BH_BY["assessed"] * 0.5 - RH
        ymin = min(ys["included"], y_reasons) - 1.1
        ax.set_xlim(xmin, XX + BW + 0.5)
        ax.set_ylim(ymin, ymax)

    # grow two-line side boxes vertically if label + count overflow BH
    # (a wider canvas squeezes data-unit heights). Boxes grow symmetrically
    # around their center, so the arrow anchors (_scy) stay aligned.
    side_two = []
    if show_dup:
        side_two.append(("duplicates", L["duplicates"]))
    side_two.append(("excluded", L["excluded"]))
    if show_notret:
        side_two.append(("not_retrieved", L["not_retrieved"]))
    side_h = {k: BH for k, _ in side_two}
    if fig is not None:
        fig.canvas.draw()
        _ren = fig.canvas.get_renderer()
        _inv = ax.transData.inverted()

        def _text_h(text, fsize, fp):
            t = ax.text(XX + BW / 2, (ymin + ymax) / 2, text, fontsize=fsize,
                        fontproperties=fp, alpha=0, zorder=-10)
            fig.canvas.draw()
            bb = t.get_window_extent(fig.canvas.get_renderer())
            t.remove()
            return abs(_inv.transform((0, bb.y1))[1] - _inv.transform((0, bb.y0))[1])

        for key, lab in side_two:
            need = (_text_h(lab, fs - 1, _fp(lab))
                    + _text_h("n = 0", fs - 1.5, _fp("0")) + 0.52)
            side_h[key] = max(BH, need)

    # phase bands + rotated phase labels (canonical three-phase template,
    # left-rail style: zero collision with the vertical flow)
    phases = [("identification", ["identified"]),
              ("screening", ["screened", "sought", "assessed"]),
              ("included", ["included"])]
    for label, rows in phases:
        y0 = min(ys[r] for r in rows) - 0.42
        y1 = max(ys[r] + BH for r in rows) + 0.42
        ax.add_patch(FancyBboxPatch((SX - 0.45, y0), SW + 0.9, y1 - y0,
                                    boxstyle="round,pad=0.05", facecolor=spine_color,
                                    edgecolor="none", alpha=0.06, zorder=0))
        ax.text(SX - 0.95, (y0 + y1) / 2, L[label], ha="center", va="center",
                rotation=90, fontsize=fs, color="#555555", fontweight="bold",
                fontproperties=_fp(L[label]))

    def _main_box(name, label, count, color=None):
        c = color or spine_color
        _bh = BH_BY[name]
        ax.add_patch(FancyBboxPatch((SX, ys[name]), SW, _bh, boxstyle="round,pad=0.08",
                                    facecolor=c, edgecolor="white", linewidth=1.2,
                                    alpha=0.95, zorder=3))
        ax.text(SX + SW / 2, ys[name] + _bh * 0.68, label, ha="center", va="center",
                fontsize=fs - 1, color="white", fontweight="bold",
                fontproperties=_fp(label))
        ax.text(SX + SW / 2, ys[name] + _bh * 0.22, f"n = {count}", ha="center",
                va="center", fontsize=fs - 1.5, color="white",
                fontproperties=_fp(str(count)))

    def _side_box(y0, h, lines, counts=None):
        ax.add_patch(FancyBboxPatch((XX, y0), BW, h, boxstyle="round,pad=0.08",
                                    facecolor=side_face, edgecolor=side_edge,
                                    linewidth=1.0, zorder=3))
        if counts is None:
            label, count = lines
            ax.text(XX + BW / 2, y0 + h * 0.63, label, ha="center", va="center",
                    fontsize=fs - 1, color=text_color, fontproperties=_fp(label))
            ax.text(XX + BW / 2, y0 + h * 0.26, f"n = {count}", ha="center", va="center",
                    fontsize=fs - 1.5, color=text_color, fontproperties=_fp(str(count)))
        else:
            title, items = lines, counts
            ax.text(XX + BW / 2, y0 + h - 0.34, title, ha="center", va="center",
                    fontsize=fs - 1, color=text_color, fontweight="bold",
                    fontproperties=_fp(title))
            n_rows = sum(txt.count("\n") + 1 for txt, _ in items)
            step = (h - 0.62) / max(1, n_rows)
            yy = y0 + h - 0.34 - step
            for txt, n in items:
                ax.text(XX + BW / 2, yy, txt, ha="center", va="center",
                        fontsize=fs - 1.5, color=text_color,
                        fontproperties=_fp(str(n)))
                yy -= step * (txt.count("\n") + 1)

    def _arrow(x0, y0, x1, y1, lw=1.6):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="->",
                                     color=arrow_color, linewidth=lw,
                                     mutation_scale=14, zorder=2))

    # spine boxes + arrows
    _main_box("identified", L["identified"], identified)
    _main_box("screened", L["screened"], screened)
    _main_box("sought", L["sought"], sought)
    _main_box("assessed", L["assessed"], assessed)
    _main_box("included", L["included_box"], included, color=final_color)
    for a, b in zip(order, order[1:]):
        # v7.9.1 AF24：箭头终点用该框实际高度 BH_BY[b]（原全局 BH——中文长标签使
        # 各框不对称长高时终点过冲钻进下一框底下=框间连接头被覆盖半截）
        _arrow(SX + SW / 2, ys[a], SX + SW / 2, ys[b] + BH_BY[b])

    # side boxes + arrows
    def _scy(key):
        return side[key] + BH / 2

    if show_dup:
        h = side_h["duplicates"]
        _side_box(side["duplicates"] + BH / 2 - h / 2, h, (L["duplicates"], dup))
        _arrow(SX + SW, _scy("duplicates"), XX, _scy("duplicates"), lw=1.4)
    h = side_h["excluded"]
    _side_box(side["excluded"] + BH / 2 - h / 2, h, (L["excluded"], excluded))
    _arrow(SX + SW, _scy("excluded"), XX, _scy("excluded"), lw=1.4)
    if show_notret:
        h = side_h["not_retrieved"]
        _side_box(side["not_retrieved"] + BH / 2 - h / 2, h, (L["not_retrieved"], not_ret))
        _arrow(SX + SW, _scy("not_retrieved"), XX, _scy("not_retrieved"), lw=1.4)
    if reasons:
        items = [("\n".join(item_display[r]), n) for r, n in reason_items]
        _side_box(y_reasons, RH, L["reasons"], items)
    else:
        _side_box(y_reasons, BH, (L["reasons"], implied_excluded))
    _arrow(SX + SW, ys["assessed"] + BH_BY["assessed"] * 0.35, XX, ys["assessed"] + BH_BY["assessed"] * 0.35, lw=1.4)

    # content-aware figure proportions (limits were set pre-draw for the
    # side-box auto-fit; BW/y_reasons carry the auto-fitted values)
    xmax = XX + BW + 0.5
    ymin = min(ys["included"], y_reasons) - 1.1
    if fig is not None:
        span_h, span_w = ymax - ymin, xmax - xmin
        fig_w = fig.get_size_inches()[0]
        fig.set_size_inches(fig_w, max(4.0, fig_w * (span_h / span_w) * 0.92))

    return "diagram"




# ── v4.10.0：--alt 无障碍文本核心（自 gen_figure 移居，模块化纪律 <3400 行）──
# EXTRA 图型（af_v23_charts）仍由 gen_figure.generate_alt_text 先行分流到此
def _alt_num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def alt_text_core(chart_type, data, title=""):
    """One-paragraph accessibility description derived from the data dict.
    Written to <output>.alt.txt with --alt."""
    t = f"{title}。" if title else ""

    def _max_txt(vals):
        fv = [_alt_num(v) for v in vals if isinstance(vals, list)]
        fv = [v for v in fv if v is not None]
        return f"{max(fv):g}" if fv else "?"

    if chart_type in ("bar", "grouped_bar", "hbar", "horizontal_bar"):
        series = data.get("series", {})
        labels = data.get("labels", [])
        parts = []
        for name, vals in series.items():
            fv = [v for v in (_alt_num(x) for x in vals) if v is not None]
            if fv:
                parts.append(f"{name} 最大值 {max(fv):g}")
        return (f"柱状图。{t}共 {len(labels)} 组：{'、'.join(map(str, labels))}。"
                f"{'；'.join(parts)}。")
    if chart_type in ("box", "boxplot", "violin"):
        series = data.get("series", {})
        segs = []
        for name, vals in series.items():
            fv = sorted(v for v in (_alt_num(x) for x in vals) if v is not None)
            if fv:
                segs.append(f"{name}：中位数 {fv[len(fv)//2]:g}（n={len(fv)}）")
        kind = "箱线图" if chart_type in ("box", "boxplot") else "小提琴图"
        return f"{kind}。{t}{'；'.join(segs)}。"
    if chart_type in ("km", "survival"):
        groups = data.get("groups", {})
        lr = data.get("log_rank") or {}
        tail = f"Log-rank p = {lr.get('p')}。" if lr.get("p") is not None else ""
        return (f"Kaplan-Meier 生存曲线。{t}分组：{'、'.join(groups.keys())}。{tail}")
    if chart_type == "roc":
        curves = data.get("curves", [])
        names = "；".join(f"{c.get('name', 'curve')} AUC {c.get('auc', '?')}"
                          for c in curves)
        return f"ROC 曲线。{t}{names}。"
    if chart_type == "forest":
        o = data.get("overall") or {}
        o_txt = (f"合并效应 {o.get('estimate')}（95%CI {o.get('ci_low')}–{o.get('ci_high')}）。"
                 if o else "")
        return f"森林图，{len(data.get('labels', []))} 项研究。{t}{o_txt}"
    if chart_type == "heatmap":
        m = data.get("matrix", [])
        cols = len(m[0]) if m else 0
        return f"热图，{len(m)} 行 × {cols} 列。{t}"
    if chart_type == "prisma":
        return (f"PRISMA 2020 系统综述流程图：最初识别 "
                f"{data.get('records_identified')} 条记录，最终纳入 "
                f"{data.get('studies_included')} 项研究。{t}")
    if chart_type == "composite":
        panels = data.get("panels", [])
        names = "、".join(str(p.get("title", "")) for p in panels)
        return f"多面板组合图，{len(panels)} 个面板：{names}。{t}"
    if chart_type == "line":
        series = data.get("series", {})
        n_pts = len(next(iter(series.values()), []))
        return f"折线图，{len(series)} 条系列 × {n_pts} 个数据点。{t}"
    if chart_type == "scatter":
        return f"散点图，共 {len(data.get('x', []))} 个数据点。{t}"
    if chart_type == "dual_axis":
        return f"双 Y 轴折线图。{t}"
    if chart_type == "diagram":
        return f"流程图。{t}"
    if chart_type == "volcano":
        l2 = data.get("log2fc") or []
        n_up = n_dn = 0
        try:
            fc_cut = float(data.get("fc_cut", 1.0))
            p_cut = float(data.get("p_cut", 0.05))
            import math as _m
            sig = -_m.log10(p_cut)
            for x, p in zip(l2, data.get("pvalue") or []):
                if -_m.log10(p) >= sig and x >= fc_cut:
                    n_up += 1
                elif -_m.log10(p) >= sig and x <= -fc_cut:
                    n_dn += 1
        except Exception:
            pass
        return (f"火山图（组学差异表达），共 {len(l2)} 个特征，"
                f"阈值内上调 {n_up} 个、下调 {n_dn} 个。{t}")
    if chart_type == "slope":
        items = data.get("items") or {}
        return f"斜率图（两时点比较），共 {len(items)} 条线。{t}"
    if chart_type == "waterfall":
        return waterfall_alt(data, t)  # v4.8：实现在 af_draw（模块化纪律 <3400 行）
    if chart_type == "swimmer":
        return swimmer_alt(data, t)  # v4.10：实现在 af_draw（模块化纪律 <3400 行）
    if chart_type == "ridgeline":
        return ridgeline_alt(data, t)  # v5.0：同上
    if chart_type == "dumbbell":
        return dumbbell_alt(data, t)  # v5.1：同上
    if chart_type == "raincloud":
        return raincloud_alt(data, t)
    if chart_type == "calibration":
        return calibration_alt(data, t)  # v5.2：临床预测模型线
    if chart_type == "dca":
        return dca_alt(data, t)  # v5.2：临床预测模型线
    if chart_type == "nomogram":
        return nomogram_alt(data, t)  # v5.3：预测模型线（列线图）
    if chart_type == "rcs":
        return rcs_alt(data, t)  # v5.4：临床回归线（限制性立方样条）
    if chart_type == "subgroup":
        return subgroup_alt(data, t)  # v5.5：亚组分析森林图
    if chart_type == "upset":
        s = data.get("sets") or {}
        top_n = data.get("top_n", 12)
        return (f"UpSet 集合交集图，共 {len(s)} 个集合"
                f"（{'、'.join(list(map(str, s.keys()))[:6])}{'等' if len(s) > 6 else ''}），"
                f"展示元素数最多的前 {top_n} 个交集；行=集合，柱=交集大小。{t}")
    return f"{chart_type} 图。{t}"



def gen_ridgeline(data, ax, theme, cjk_fp, **kwargs):
    """Ridgeline plot（v5.0，第 29 号图型）：山脊图/joyplot——多组 KDE 密度沿纵向
    堆叠、部分重叠，一屏展示"分布如何逐组移动/变形"（时间进程/剂量梯度/分场景
    比较的全景形态；Wehrle & Johnson 经典形态）。画序自底向上（画家算法），
    上排山脊线完整覆盖下排填充。

    JSON: {"labels": [...组名（自上而下）], "datasets": {组名: [数值...]}}
    可选 "overlap": 0.55（0~0.95 山脊纵向重叠比例）、"sort": "input"(默认)|"median"、
    "x_label": "..."。退化：某组仅 1 个不同值 → 该组退化为基线标记线并 stderr 告知。
    """
    from scipy.stats import gaussian_kde
    labels = data.get("labels", data.get("x", []))
    series = data.get("series", data.get("datasets", {}))
    if not isinstance(series, dict) or not series:
        raise ValueError("ridgeline: 需要 'datasets'（{{组名: [数值数组]}}），schema 同 violin")
    names = list(series.keys())
    if labels and len(labels) != len(names):
        raise ValueError(f"ridgeline: labels 有 {len(labels)} 项但 datasets 有 {len(names)} 组——须一一对应")
    for n, vals in series.items():
        if not isinstance(vals, (list, tuple)) or not vals:
            raise ValueError(f"ridgeline: datasets['{n}'] 必须是非空数值数组")
        bad = [v for v in vals if isinstance(v, bool) or not isinstance(v, (int, float))
               or not np.isfinite(float(v))]
        if bad:
            raise ValueError(f"ridgeline: datasets['{n}'] 含 {len(bad)} 个非有限数值（NaN/±Infinity/非数值）")
    overlap = float(data.get("overlap", 0.55))
    if not (0 <= overlap <= 0.95):
        raise ValueError("ridgeline: overlap 取值 0~0.95（>0.95 山脊相互吞没）")
    sort_mode = str(data.get("sort", "input")).strip().lower()
    if sort_mode not in ("input", "median"):
        raise ValueError("ridgeline: sort 只支持 'input' 或 'median'")
    if sort_mode == "median":
        names = sorted(names, key=lambda k: -float(np.median(series[k])))

    allv = np.concatenate([np.asarray([float(x) for x in series[k]], dtype=float) for k in names])
    gmin, gmax = float(allv.min()), float(allv.max())
    pad = 0.15 * (gmax - gmin if gmax > gmin else max(1.0, abs(gmin)))
    grid = np.linspace(gmin - 1.5 * pad, gmax + 1.5 * pad, 260)
    dens = {}
    for k in names:
        v = np.asarray([float(x) for x in series[k]], dtype=float)
        if len(np.unique(v)) < 2:
            dens[k] = None  # 退化：单值组
            continue
        kde = gaussian_kde(v)
        dens[k] = kde(grid)
    hmax = max((d.max() for d in dens.values() if d is not None), default=1.0)
    if hmax <= 0:
        hmax = 1.0

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    n = len(names)
    step = 1.0 - overlap
    bases = {k: (n - 1 - i) * step for i, k in enumerate(names)}  # i=0 在顶
    degenerate = []
    # 画家算法：自底向上画，且每条山脊 fill/outline 同层 zorder 按位次递增——
    # 上排山脊整体（含轮廓）覆盖下排重叠区（验收 P1：分层 zorder 会让下排轮廓
    # 骑压上排填充，视觉上"下排覆盖上排"）
    for k in reversed(names):
        color = theme["colors"][names.index(k) % len(theme["colors"])]
        base = bases[k]
        z = 2.0 + (n - 1 - names.index(k))  # names 自上而下：顶排 z 最大，整层覆盖下排
        if dens[k] is None:
            v0 = float(np.asarray([float(x) for x in series[k]], dtype=float)[0])
            ax.plot([v0, v0], [base, base + 0.45], color=color, lw=3.5,
                    solid_capstyle="butt", alpha=0.85, zorder=z)
            degenerate.append(k)
            continue
        d = dens[k] / hmax
        ax.fill_between(grid, base, base + d, facecolor=color, alpha=0.85,
                        edgecolor="none", zorder=z)
        ax.plot(grid, base + d, color=color, lw=1.3, zorder=z + 0.01)
        ax.plot([grid[0], grid[-1]], [base, base], color="#4A4A4A", lw=0.7,
                alpha=0.65, zorder=z + 0.01)
    ax.set_yticks([bases[k] for k in names])
    ax.set_yticklabels(names, fontsize=fs_s,
                       fontproperties=cjk_fp if cjk_fp and has_cjk("".join(names)) else None)
    ax._af_category_axis = True  # 组名是数据：豁免刻度抽稀（同 raincloud）
    top_base = bases[names[0]]
    ax.set_xlim(grid[0], grid[-1])
    ax.set_ylim(-0.18, top_base + 1.22)
    xl = str(data.get("x_label", "") or ("数值" if cjk_fp else "Value"))
    ax.set_xlabel(xl, fontsize=fs,
                  fontproperties=cjk_fp if cjk_fp and has_cjk(xl) else None)
    print(f"ridgeline: {n} 组（overlap={overlap:g}，sort={sort_mode}）"
          + (f"；单值退化 {len(degenerate)} 组: {'、'.join(degenerate)}" if degenerate else ""),
          file=sys.stderr)
    apply_base_style(ax, theme)


def ridgeline_alt(data, t=""):
    """v5.0：ridgeline 的 --alt 文本（放本模块守 gen_figure <3400 行纪律）。"""
    series = data.get("series", data.get("datasets", {}))
    names = list(series.keys()) if isinstance(series, dict) else []
    ns = {k: len(v) for k, v in series.items() if isinstance(v, list)} if isinstance(series, dict) else {}
    overlap = data.get("overlap", 0.55)
    med = []
    for k in names:
        v = [float(x) for x in series[k] if isinstance(x, (int, float)) and not isinstance(x, bool)]
        if v:
            v.sort()
            m = v[len(v)//2] if len(v) % 2 else (v[len(v)//2 - 1] + v[len(v)//2]) / 2
            med.append(f"{k} 中位 {m:g}")
    return (f"山脊图（{len(names)} 组堆叠密度，overlap {overlap}），自上而下："
            f"{'、'.join(names)}。各组的样本量：{'、'.join(f'{k} {ns[k]}' for k in names if k in ns)}。"
            + ("；".join(med) + "。" if med else "") + t)


def validate_ridgeline(data):
    """v5.0：ridgeline 数据校验（返回 fatal 列表）；与 gen_ridgeline 同口径。"""
    fatal = []
    series = data.get("series", data.get("datasets", {}))
    if not isinstance(series, dict) or not series:
        fatal.append("ridgeline: 需要 'datasets'（{组名: [数值数组]}），schema 同 violin")
        return fatal
    labels = data.get("labels", data.get("x"))
    if labels is not None and (not isinstance(labels, list) or len(labels) != len(series)):
        fatal.append("ridgeline: labels 项数须与 datasets 组数一一对应")
    for n, vals in series.items():
        if not isinstance(vals, (list, tuple)) or not vals:
            fatal.append(f"ridgeline: datasets['{n}'] 必须是非空数值数组")
        elif any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in vals):
            fatal.append(f"ridgeline: datasets['{n}'] 含非数值项")
    ov = data.get("overlap")
    if ov is not None and (not isinstance(ov, (int, float)) or isinstance(ov, bool)
                           or not (0 <= float(ov) <= 0.95)):
        fatal.append("ridgeline: overlap 取值 0~0.95")
    sm = data.get("sort")
    if sm is not None and str(sm).strip().lower() not in ("input", "median"):
        fatal.append("ridgeline: sort 只支持 'input' 或 'median'")
    return fatal




def write_audit_sidecar(data, chart_type, out_path):
    """v5.0 --audit：数字对账侧车 <output>.audit.json——从输入数据独立重算描述
    统计（纯计数零推断），评审/用户可逐项核对"图上的数与数据是否对得上"。
    同输入同字节（无时间戳；含输入 sha256 前 12 位做指纹）。"""
    import hashlib
    import json as _json
    import os as _os

    def _stats(vals):
        xs = sorted(float(v) for v in vals
                    if isinstance(v, (int, float)) and not isinstance(v, bool)
                    and np.isfinite(float(v)))
        n = len(xs)
        if not n:
            return {"n": 0}
        mean = sum(xs) / n
        var = sum((x - mean) ** 2 for x in xs) / (n - 1) if n > 1 else 0.0
        med = xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2
        return {"n": n, "mean": round(mean, 6), "sd": round(var ** 0.5, 6),
                "median": round(med, 6), "min": round(xs[0], 6), "max": round(xs[-1], 6)}

    audit = {"chart_type": chart_type, "generated_by": "academic-figures --audit",
             "note": "描述统计由输入数据独立重算（纯计数零推断）；均值/中位数/SD 供逐项对账",
             "stats": {}}
    raw = _json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
    audit["input_sha256_12"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]
    for container in ("datasets", "series", "groups"):
        obj = data.get(container)
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, list):
                    audit["stats"][f"{container}.{k}"] = _stats(v)
    labels = data.get("labels") or data.get("x")
    if isinstance(labels, list):
        audit["stats"]["labels"] = _stats(labels) if all(
            isinstance(v, (int, float)) and not isinstance(v, bool) for v in labels) else {
            "n": len(labels), "type": "categorical"}
    dst = str(out_path) + ".audit.json"
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(_json.dumps(audit, ensure_ascii=False, indent=1, sort_keys=True))
    print(f"audit: 数字对账侧车已写 {dst}（{len(audit['stats'])} 项）", file=sys.stderr)
    return dst




def gen_dumbbell(data, ax, theme, cjk_fp, **kwargs):
    """Dumbbell plot（v5.1，第 30 号图型）：哑铃图——每行两点（from→to）+连接线，
    横向形态（发表惯例），强调"逐条目的差距大小"（两时点/两组对照：基线 vs
    随访、男 vs 女、实验 vs 对照；Pew/Lancet 系常用形态）。严格限两时点：
    >2 时点请用 slope/line，配对检验请用 paired。

    JSON: {"labels": [...], "from": [...], "to": [...],
           "from_label": "起点"(可选图例名), "to_label": "终点",
           "sort": "gap"(默认，|to-from| 降序)|"input"|"to"(按 to 降序),
           "show_values": false(点端数值), "show_gap": false(连接线中点 Δ 标注),
           "x_label": "..."}
    """
    import math as _m
    labels = data.get("labels")
    frm, to = data.get("from"), data.get("to")
    if not (isinstance(frm, list) and frm and isinstance(to, list) and to):
        raise ValueError("dumbbell: 需要 'from' 与 'to'（非空数值数组）")
    if len(frm) != len(to):
        raise ValueError("dumbbell: from 与 to 长度必须一致")
    n = len(to)
    try:
        fv = [float(v) for v in frm]
        tv = [float(v) for v in to]
    except (TypeError, ValueError):
        raise ValueError("dumbbell: from/to 必须全为数值")
    if not (all(_m.isfinite(v) for v in fv) and all(_m.isfinite(v) for v in tv)):
        raise ValueError("dumbbell: from/to 含非有限值（NaN/±Infinity）——请清洗源数据")
    if labels is not None and (not isinstance(labels, list) or len(labels) != n):
        raise ValueError("dumbbell: 'labels' 长度必须与 from/to 一致")
    for key in ("from_label", "to_label"):
        v = data.get(key)
        if v is not None and not isinstance(v, str):
            raise ValueError(f"dumbbell: '{key}' 须为字符串（图例名）")
    sort_mode = str(data.get("sort", "gap")).strip().lower()
    if sort_mode not in ("gap", "input", "to"):
        raise ValueError("dumbbell: sort 只支持 'gap' | 'input' | 'to'")
    order = list(range(n))
    if sort_mode == "gap":
        order = sorted(range(n), key=lambda i: (-abs(tv[i] - fv[i]), i))
    elif sort_mode == "to":
        order = sorted(range(n), key=lambda i: (-tv[i], i))

    c_from = theme["colors"][0]
    c_to = theme["colors"][1 % len(theme["colors"])]
    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    show_values = bool(data.get("show_values", False) or kwargs.get("show_values", False))
    show_gap = bool(data.get("show_gap", False))

    y = list(range(n))
    snames = [str(labels[i]) if labels else f"P{i+1:02d}" for i in order]
    for row, i in enumerate(order):
        lo, hi = min(fv[i], tv[i]), max(fv[i], tv[i])
        ax.plot([lo, hi], [row, row], color="#999999", lw=2.8,  # v7.9.0 AF36 衍生：#BBBBBB 偏浅（细元素应更实）
                solid_capstyle="round", zorder=2)
        ax.plot([fv[i]], [row], marker="o", mfc="white", mec=c_from, mew=1.7,
                ms=8, ls="none", zorder=3)
        ax.plot([tv[i]], [row], marker="o", mfc=c_to, mec=c_to, ms=8,
                ls="none", zorder=4)
        if show_values:
            ax.text(fv[i], row + 0.22, f"{fv[i]:g}", ha="center", va="bottom",
                    fontsize=fs_s, color=c_from)
            ax.text(tv[i], row + 0.22, f"{tv[i]:g}", ha="center", va="bottom",
                    fontsize=fs_s, color=c_to)
        if show_gap and hi - lo > 0:
            # 倒轴语义：数据 y 越大越靠下，row+0.26 = 连接线视觉下方
            ax.text((lo + hi) / 2, row + 0.26, f"Δ{abs(tv[i] - fv[i]):g}",
                    ha="center", va="top", fontsize=fs_s, color="#555555")

    ax.set_yticks(y)
    ax.set_yticklabels(snames[:n], fontsize=fs_s,
                       fontproperties=cjk_fp if cjk_fp and has_cjk("".join(snames)) else None)
    ax._af_category_axis = True  # 条目名是数据：豁免刻度抽稀（同 swimmer）
    # 底部预留 1 行空带给右下图例（gap 排序末行连接线可能顶到右缘，防碰撞）
    reserve_bottom_band(ax, n, top_pad=0.4)
    ax.set_yticks([y[i] for i in range(n)])
    allv = fv + tv
    # 机制（类级铁律，见 pitfalls「端点标记必留 pad」）：显式 set_xlim 禁用
    # matplotlib 边距，数据极值处的标记（本图 from/to 圆点）必被裁半——自留 4% pad
    lo_all, hi_all = min(allv), max(allv)
    _pad = (hi_all - lo_all) * 0.04 or (max(1.0, abs(hi_all) * 0.02))
    ax.set_xlim(lo_all - _pad, hi_all + _pad)
    fl = str(data.get("from_label", "") or ("起点" if cjk_fp else "From"))
    tl = str(data.get("to_label", "") or ("终点" if cjk_fp else "To"))
    handles = [plt.Line2D([], [], marker="o", mfc="white", mec=c_from, mew=1.7,
                          ms=8, ls="none"),
               plt.Line2D([], [], marker="o", mfc=c_to, mec=c_to, ms=8, ls="none")]
    ax.legend(handles, [fl, tl], loc="lower right", frameon=False, fontsize=fs_s,
              prop=cjk_fp if cjk_fp and has_cjk(fl + tl) else None)
    xl = str(data.get("x_label", "") or ("数值" if cjk_fp else "Value"))
    ax.set_xlabel(xl, fontsize=fs,
                  fontproperties=cjk_fp if cjk_fp and has_cjk(xl) else None)
    _gaps = [abs(tv[i] - fv[i]) for i in range(n)]
    print(f"dumbbell: {n} 行（sort={sort_mode}，差距 {min(_gaps):g}~{max(_gaps):g}）"
          f"；起点均值 {sum(fv)/n:.2f} → 终点均值 {sum(tv)/n:.2f}", file=sys.stderr)
    apply_base_style(ax, theme)


def dumbbell_alt(data, t=""):
    """v5.1：dumbbell 的 --alt 文本（放本模块守 gen_figure <3400 行纪律）。"""
    frm, to = data.get("from") or [], data.get("to") or []
    n = min(len(frm), len(to))
    labels = data.get("labels") or [f"P{i+1}" for i in range(n)]
    pairs = []
    for i in range(n):
        try:
            f0, t0 = float(frm[i]), float(to[i])
            pairs.append(f"{labels[i]} {f0:g}→{t0:g}（差 {t0 - f0:+g}）")
        except (TypeError, ValueError):
            continue
    return (f"哑铃图（每行两点比较，共 {n} 行）：{'；'.join(pairs)}。{t}")


def validate_dumbbell(data):
    """v5.1：dumbbell 数据校验（返回 fatal 列表）；与 gen_dumbbell 同口径。"""
    fatal = []
    frm, to = data.get("from"), data.get("to")
    if not (isinstance(frm, list) and frm and isinstance(to, list) and to):
        fatal.append("dumbbell: 需要 'from' 与 'to'（非空数值数组）")
        return fatal
    if len(frm) != len(to):
        fatal.append("dumbbell: from 与 to 长度必须一致")
        return fatal
    for name, arr in (("from", frm), ("to", to)):
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in arr):
            fatal.append(f"dumbbell: {name} 必须全为数值")
    import math as _m
    if not any("必须全为数值" in f for f in fatal):
        if not (all(_m.isfinite(float(v)) for v in frm)
                and all(_m.isfinite(float(v)) for v in to)):
            fatal.append("dumbbell: from/to 含非有限值——请清洗源数据")
    labels = data.get("labels")
    if labels is not None and (not isinstance(labels, list) or len(labels) != len(to)):
        fatal.append("dumbbell: 'labels' 长度必须与 from/to 一致")
    for key in ("from_label", "to_label"):
        v = data.get(key)
        if v is not None and not isinstance(v, str):
            fatal.append(f"dumbbell: '{key}' 须为字符串")
    sm = data.get("sort")
    if sm is not None and str(sm).strip().lower() not in ("gap", "input", "to"):
        fatal.append("dumbbell: sort 只支持 'gap' | 'input' | 'to'")
    return fatal




# ═══ v5.2：calibration 校准曲线 + dca 决策曲线（临床预测模型线，第 31/32 图型）═══

def _cal_bins(data):
    """calibration 两种给法归一：bins[] 对象数组 或 predicted/observed 平行数组。
    返回 (pred, obs, lo, hi, ns)；给法非法或非数值时抛 ValueError。"""
    bins = data.get("bins")
    if isinstance(bins, list) and bins:
        pred, obs, lo, hi, ns = [], [], [], [], []
        for i, b in enumerate(bins):
            if not isinstance(b, dict) or "predicted" not in b or "observed" not in b:
                raise ValueError(f"calibration: bins[{i}] 须为含 predicted/observed 的对象")
            try:
                pred.append(float(b["predicted"]))
                obs.append(float(b["observed"]))
                lo.append(float(b["ci_lo"]) if b.get("ci_lo") is not None else None)
                hi.append(float(b["ci_hi"]) if b.get("ci_hi") is not None else None)
                ns.append(int(b["n"]) if b.get("n") is not None else None)
            except (TypeError, ValueError):
                raise ValueError(f"calibration: bins[{i}] 的 predicted/observed/ci/n 须为数值")
        return pred, obs, lo, hi, ns
    pred, obs = data.get("predicted"), data.get("observed")
    if not (isinstance(pred, list) and pred and isinstance(obs, list) and obs):
        raise ValueError("calibration: 需要 bins[] 或 predicted/observed 平行数组")
    if len(pred) != len(obs):
        raise ValueError("calibration: predicted 与 observed 长度必须一致")
    lo, hi, ns = data.get("ci_lo"), data.get("ci_hi"), data.get("n")
    for nm, a in (("ci_lo", lo), ("ci_hi", hi), ("n", ns)):
        if a is not None and (not isinstance(a, list) or len(a) != len(pred)):
            raise ValueError(f"calibration: {nm} 长度必须与 predicted 一致")
    try:
        fv = lambda a: [float(v) if v is not None else None for v in (a or [])]
        return ([float(v) for v in pred], [float(v) for v in obs],
                fv(lo), fv(hi), [int(v) if v is not None else None for v in (ns or [])])
    except (TypeError, ValueError):
        raise ValueError("calibration: predicted/observed/ci/n 必须全为数值")


def gen_calibration(data, ax, theme, cjk_fp, **kwargs):
    """calibration 校准曲线（v5.2，第 31 号图型）：临床预测模型三件套之一
    （与 ROC/DCA 同生态）——分箱预测概率 vs 实际观测率 + 理想对角线（虚线），
    等比坐标。JSON: bins=[{predicted,observed,n?,ci_lo?,ci_hi?}] 或
    predicted/observed 平行数组（ci_lo/ci_hi/n 可选平行数组，长度同 predicted）；
    hl_p 可选（Hosmer-Lemeshow p，左上角标注）；smooth=true 画各箱线性插值
    参考线（默认关，稀疏分箱慎用）。"""
    pred, obs, lo, hi, ns = _cal_bins(data)
    n = len(pred)
    for i, (p, o) in enumerate(zip(pred, obs)):
        if not (0.0 <= p <= 1.0 and 0.0 <= o <= 1.0):
            raise ValueError(f"calibration: 第 {i+1} 箱 predicted/observed 须在 [0,1]")
    for arr, nm in ((lo, "ci_lo"), (hi, "ci_hi")):
        if any(v is not None and not (0.0 <= v <= 1.0) for v in arr):
            raise ValueError(f"calibration: {nm} 超出 [0,1]")
    hl_p = data.get("hl_p")
    if hl_p is not None:
        hl_p = float(hl_p)
        if not (0.0 <= hl_p <= 1.0):
            raise ValueError("calibration: hl_p 须在 [0,1]")
    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    c_main = theme["colors"][0]
    ax.plot([-0.02, 1.02], [-0.02, 1.02], ls=(0, (5, 4)), lw=1.1,
            color="#999999", zorder=1)
    yerr = None
    if any(v is not None for v in lo) and any(v is not None for v in hi):
        yerr = [[max(0.0, o - (l if l is not None else o)) for o, l in zip(obs, lo)],
                [max(0.0, (h if h is not None else o) - o) for o, h in zip(obs, hi)]]
    ax.errorbar(pred, obs, yerr=yerr, fmt="o", ms=5.5, mfc=c_main, mec=c_main,
                ecolor=c_main, elinewidth=1.0, capsize=2.2, ls="none", zorder=3)
    if bool(data.get("smooth")) and n >= 4:
        sp = sorted(range(n), key=lambda i: pred[i])
        ax.plot([pred[i] for i in sp], [obs[i] for i in sp], lw=1.0,
                color=c_main, alpha=0.45, zorder=2)
    # 端点标记必留 pad（类级铁律）：预测/观测可取 0/1，显式 xlim 禁用边距
    _pad = 0.045
    ax.set_xlim(-_pad, 1.0 + _pad)
    ax.set_ylim(-_pad, 1.0 + _pad)
    ax.set_aspect("equal", adjustable="box")  # 校准曲线正方形坐标为发表惯例
    xl = str(data.get("x_label") or ("预测概率（分箱）" if cjk_fp else "Predicted probability"))
    yl = str(data.get("y_label") or ("实际观测率" if cjk_fp else "Observed rate"))
    ax.set_xlabel(xl, fontsize=fs, fontproperties=cjk_fp if cjk_fp and has_cjk(xl) else None)
    ax.set_ylabel(yl, fontsize=fs, fontproperties=cjk_fp if cjk_fp and has_cjk(yl) else None)
    handles = [plt.Line2D([], [], ls=(0, (5, 4)), lw=1.1, color="#999999"),
               plt.Line2D([], [], marker="o", mfc=c_main, mec=c_main,
                          ls="none", ms=5.5)]
    lbls = [("理想校准" if cjk_fp else "Ideal"),
            ("各箱（95%CI）" if (cjk_fp and yerr) else ("各箱" if cjk_fp else "Bins"))]
    ax.legend(handles, lbls, loc="lower right", frameon=False, fontsize=fs_s,
              prop=cjk_fp if cjk_fp else None)
    if hl_p is not None:
        ax.text(0.03, 0.97, f"Hosmer–Lemeshow p = {hl_p:g}", transform=ax.transAxes,
                ha="left", va="top", fontsize=fs_s, color="#555555",
                fontproperties=cjk_fp if cjk_fp else None)
    devs = [o - p for p, o in zip(pred, obs)]
    _n_all = sum(v for v in ns if v)
    print(f"calibration: {n} 箱" + (f"，总 n={_n_all}" if _n_all else "")
          + f"；平均偏差(观察-预测) {sum(devs)/n:+.3f}，最大 |偏差| {max(abs(d) for d in devs):.3f}",
          file=sys.stderr)
    apply_base_style(ax, theme)


def calibration_alt(data, t=""):
    """v5.2：calibration 的 --alt 文本（本模块实现守 gen_figure <3400 行纪律）。"""
    try:
        pred, obs, _lo, _hi, ns = _cal_bins(data)
    except ValueError:
        return f"校准曲线（分箱预测概率 vs 实际观测率）。{t}"
    devs = [o - p for p, o in zip(pred, obs)]
    _n_all = sum(v for v in ns if v)
    return (f"校准曲线（{len(pred)} 箱" + (f"，总样本 {_n_all}" if _n_all else "")
            + f"）：平均偏差(观察-预测) {sum(devs)/len(devs):+.3f}，"
            f"最大 |偏差| {max(abs(d) for d in devs):.3f}；理想对角线为完美校准参照。{t}")


def validate_calibration(data):
    """v5.2：calibration 数据校验（返回 fatal 列表）；与 gen_calibration 同口径。"""
    fatal = []
    try:
        pred, obs, lo, hi, _ns = _cal_bins(data)
    except ValueError as e:
        return [str(e)]
    for i, (p, o) in enumerate(zip(pred, obs)):
        if not (0.0 <= p <= 1.0 and 0.0 <= o <= 1.0):
            fatal.append(f"calibration: 第 {i+1} 箱 predicted/observed 须在 [0,1]")
    for nm, arr in (("ci_lo", lo), ("ci_hi", hi)):
        if any(v is not None and not (0.0 <= v <= 1.0) for v in arr):
            fatal.append(f"calibration: {nm} 超出 [0,1]")
    hp = data.get("hl_p")
    if hp is not None:
        try:
            if not (0.0 <= float(hp) <= 1.0):
                fatal.append("calibration: hl_p 须在 [0,1]")
        except (TypeError, ValueError):
            fatal.append("calibration: hl_p 须为数值")
    return fatal


def gen_dca(data, ax, theme, cjk_fp, **kwargs):
    """dca 决策曲线分析（v5.2，第 32 号图型）：临床预测模型三件套之一——
    净收益 vs 阈值概率，各模型与两条参照策略（全部干预/不干预）比较，
    净收益定义 Vickers（每 100 人净真阳性数）。
    JSON: thresholds 严格升序 (0,1) 开区间；models=[{name, net_benefit}] 1~6 个；
    prevalence (0,1) 可选（画理论 treat-all）或 treat_all 显式数组（优先）；
    show_none 默认 true（treat-none=0 水平虚线）。"""
    thr, models = data.get("thresholds"), data.get("models")
    if not (isinstance(thr, list) and thr):
        raise ValueError("dca: 需要 'thresholds'（升序阈值数组）")
    try:
        tv = [float(v) for v in thr]
    except (TypeError, ValueError):
        raise ValueError("dca: thresholds 必须全为数值")
    if any(not (0.0 < v < 1.0) for v in tv) or any(
            tv[i] >= tv[i + 1] for i in range(len(tv) - 1)):
        raise ValueError("dca: thresholds 须严格升序且在 (0,1) 开区间（t=0/1 净收益无定义）")
    if not (isinstance(models, list) and 1 <= len(models) <= 6):
        raise ValueError("dca: 需要 'models'（1~6 个 {name, net_benefit} 对象）")
    n = len(tv)
    names, nbs = [], []
    for i, m in enumerate(models):
        if not isinstance(m, dict) or not isinstance(m.get("net_benefit"), list):
            raise ValueError(f"dca: models[{i}] 须为含 name/net_benefit 的对象")
        if len(m["net_benefit"]) != n:
            raise ValueError(f"dca: models[{i}].net_benefit 长度必须与 thresholds 一致（{n}）")
        try:
            nbs.append([float(v) for v in m["net_benefit"]])
        except (TypeError, ValueError):
            raise ValueError(f"dca: models[{i}].net_benefit 必须全为数值")
        names.append(str(m.get("name") or f"Model {i+1}"))
    prev = data.get("prevalence")
    if prev is not None:
        prev = float(prev)
        if not (0.0 < prev < 1.0):
            raise ValueError("dca: prevalence 须在 (0,1)")
    ta = data.get("treat_all")
    if ta is not None:
        if not (isinstance(ta, list) and len(ta) == n):
            raise ValueError("dca: treat_all 长度必须与 thresholds 一致")
        ta = [float(v) for v in ta]
    show_none = data.get("show_none", True)

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    handles, hlbls = [], []
    if ta is not None:
        ax.plot(tv, ta, color="#888888", lw=1.6, zorder=2)
        handles.append(plt.Line2D([], [], color="#888888", lw=1.6))
        hlbls.append("全部干预" if cjk_fp else "Treat all")
    elif prev is not None:
        ax.plot(tv, [prev - (1.0 - prev) * t / (1.0 - t) for t in tv],
                color="#888888", lw=1.6, zorder=2)
        handles.append(plt.Line2D([], [], color="#888888", lw=1.6))
        hlbls.append(f"全部干预（患病率 {prev:g}）" if cjk_fp
                     else f"Treat all (prev {prev:g})")
    if show_none:
        ax.axhline(0.0, color="#AAAAAA", lw=1.2, ls=(0, (4, 3)), zorder=1)
        handles.append(plt.Line2D([], [], color="#AAAAAA", lw=1.2, ls=(0, (4, 3))))
        hlbls.append("不干预" if cjk_fp else "Treat none")
    markers = ("o", "s", "^", "D", "v", "<")
    all_nb = [v for row in nbs for v in row] + list(ta or [])
    # 获益区间着色（v5.4）：模型净收益 > max(treat-all, treat-none=0) 的连续
    # 区段淡色填充（临床含义：该阈值区间内按模型决策有净获益）。受益于参照
    # 线存在；无任何参照时跳过。benefit_shade=false 关闭。
    _shade_on = bool(data.get("benefit_shade", True))
    _ta_arr = ta if ta is not None else (
        [prev - (1.0 - prev) * t / (1.0 - t) for t in tv] if prev is not None else None)
    _shade_msg = []
    if _shade_on:
        for i, (nm, nb) in enumerate(zip(names, nbs)):
            c = theme["colors"][i % len(theme["colors"])]
            if _ta_arr is not None:
                cond = [(n > a and n > 0) for n, a in zip(nb, _ta_arr)]
            else:
                cond = [n > 0 for n in nb]
            if any(cond):
                ax.fill_between(tv, 0, nb, where=cond, color=c, alpha=0.12,
                                lw=0, zorder=1)
                _runs = []
                _s = None
                for k, f in enumerate(cond + [False]):
                    if f and _s is None:
                        _s = k
                    elif not f and _s is not None:
                        _runs.append((tv[_s], tv[k - 1]))
                        _s = None
                _shade_msg.append(f"{nm} 获益区 " + "、".join(
                    f"{a:g}~{b:g}" for a, b in _runs))
    for i, (nm, nb) in enumerate(zip(names, nbs)):
        c = theme["colors"][i % len(theme["colors"])]
        ax.plot(tv, nb, color=c, lw=1.8, marker=markers[i % len(markers)],
                ms=3.6, zorder=3)
        handles.append(plt.Line2D([], [], color=c, lw=1.8,
                                  marker=markers[i % len(markers)], ms=3.6))
        hlbls.append(nm)
    _pad = (max(tv) - min(tv)) * 0.04 or 0.01
    ax.set_xlim(min(tv) - _pad, max(tv) + _pad)  # 端点标记必留 pad（类级铁律）
    lo_y, hi_y = min(0.0, min(all_nb)), max(all_nb)
    _py = (hi_y - lo_y) * 0.06 or 0.05
    ax.set_ylim(lo_y - _py, hi_y + _py * 1.6)  # 顶部多留图例位
    xl = str(data.get("x_label") or ("阈值概率" if cjk_fp else "Threshold probability"))
    yl = str(data.get("y_label") or ("净收益" if cjk_fp else "Net benefit"))
    ax.set_xlabel(xl, fontsize=fs, fontproperties=cjk_fp if cjk_fp and has_cjk(xl) else None)
    ax.set_ylabel(yl, fontsize=fs, fontproperties=cjk_fp if cjk_fp and has_cjk(yl) else None)
    ax.legend(handles, hlbls, loc="upper right", frameon=False, fontsize=fs_s,
              prop=cjk_fp if cjk_fp and has_cjk("".join(names) + "".join(hlbls)) else None)
    _pk = [max(nb) for nb in nbs]
    _pf = _dca_peak_fmt(_pk)  # v7.9.0 AF28：0.185/0.180 同显 +0.18 掩盖差异→折叠时升位
    peaks = [f"{nm} 峰值 {_pf[k]}@{tv[nbs[k].index(_pk[k])]:g}"
             for k, nm in enumerate(names)]
    print(f"dca: 阈值 {min(tv):g}~{max(tv):g}（{n} 点），{len(names)} 个模型"
          + (f"，患病率 {prev:g}" if prev is not None else "")
          + "；" + "；".join(peaks)
          + (("；" + "；".join(_shade_msg)) if _shade_msg else ""), file=sys.stderr)
    apply_base_style(ax, theme)


def _dca_peak_fmt(vals):
    """v7.9.0 AF28：峰值显示精度自适应——2 位小数若把不同真值折叠成同串
    （0.185/0.180 同显 +0.18，读者误判两模型等价）则逐级升位直到可区分。"""
    try:
        for _nd in (2, 3, 4):
            _ss = [f"{v:+.{_nd}f}" for v in vals]
            if len(set(_ss)) == len(_ss):
                return _ss
        return [f"{v:+g}" for v in vals]
    except Exception:
        return [f"{v:+.2f}" for v in vals]


def dca_alt(data, t=""):
    """v5.2：dca 的 --alt 文本。"""
    thr = data.get("thresholds") or []
    models = data.get("models") or []
    segs = []
    _pkv, _meta = [], []
    for m in models:
        if isinstance(m, dict) and isinstance(m.get("net_benefit"), list):
            nb = [float(v) for v in m["net_benefit"]
                  if isinstance(v, (int, float)) and not isinstance(v, bool)]
            if nb:
                _pkv.append(max(nb))
                _meta.append((m.get('name', '模型'), nb.index(max(nb))))
    _pf = _dca_peak_fmt(_pkv) if _pkv else []
    for k, (nm, i) in enumerate(_meta):
        segs.append(f"{nm} 峰值净收益 {_pf[k]}"
                    f"（阈值 {thr[i] if i < len(thr) else '?'}）")
    return (f"决策曲线分析（{len(models)} 个模型，{len(thr)} 个阈值点"
            + ("；参照策略：全部干预/不干预" if data.get("show_none", True) else "")
            + f"）：{'；'.join(segs)}。{t}")


def validate_dca(data):
    """v5.2：dca 数据校验（返回 fatal 列表）；与 gen_dca 同口径。"""
    fatal = []
    thr, models = data.get("thresholds"), data.get("models")
    if not (isinstance(thr, list) and thr):
        return ["dca: 需要 'thresholds'（升序阈值数组）"]
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in thr):
        return ["dca: thresholds 必须全为数值"]
    if any(not (0.0 < v < 1.0) for v in thr) or any(
            thr[i] >= thr[i + 1] for i in range(len(thr) - 1)):
        fatal.append("dca: thresholds 须严格升序且在 (0,1) 开区间")
    if not (isinstance(models, list) and 1 <= len(models) <= 6):
        fatal.append("dca: 需要 'models'（1~6 个 {name, net_benefit} 对象）")
        return fatal
    n = len(thr)
    for i, m in enumerate(models):
        if not isinstance(m, dict) or not isinstance(m.get("net_benefit"), list):
            fatal.append(f"dca: models[{i}] 须为含 name/net_benefit 的对象")
            continue
        if len(m["net_benefit"]) != n:
            fatal.append(f"dca: models[{i}].net_benefit 长度必须与 thresholds 一致（{n}）")
        elif any(isinstance(v, bool) or not isinstance(v, (int, float))
                 for v in m["net_benefit"]):
            fatal.append(f"dca: models[{i}].net_benefit 必须全为数值")
    prev = data.get("prevalence")
    if prev is not None and (isinstance(prev, bool)
                             or not isinstance(prev, (int, float))
                             or not (0.0 < prev < 1.0)):
        fatal.append("dca: prevalence 须为 (0,1) 内数值")
    ta = data.get("treat_all")
    if ta is not None and (not isinstance(ta, list) or len(ta) != n
                           or any(isinstance(v, bool) or not isinstance(v, (int, float))
                                  for v in ta)):
        fatal.append("dca: treat_all 长度必须与 thresholds 一致且全为数值")
    return fatal


# ═══ v5.3：nomogram 列线图（临床预测模型线，第 33 图型）═══

def _nom_fmt(v):
    """nomogram 刻度值格式化：整数值去小数尾，其余 %g。"""
    if isinstance(v, (int, float)) and not isinstance(v, bool) \
            and float(v).is_integer():
        return str(int(v))
    return f"{v:g}"


def _nom_ticks(var, pts_hi=100.0, name_key="name"):
    """nomogram 尺归一：返回 (tick_labels, points_at)。ticks 数值→格式化；
    points_at 缺省=线性 0..100。变量尺 pts_hi=100；结局尺传总积分上限
    （None=只查非负）。name_key 取 name/label 进报错。给法非法抛 ValueError。"""
    disp = str(var.get(name_key) or "?")
    ticks = var.get("ticks")
    if not (isinstance(ticks, list) and 2 <= len(ticks) <= 12):
        raise ValueError(f"nomogram: 尺「{disp}」需要 ticks（2~12 个刻度）")
    labels = var.get("labels")
    if labels is not None and (not isinstance(labels, list) or len(labels) != len(ticks)):
        raise ValueError(f"nomogram: 「{disp}」labels 长度必须与 ticks 一致")
    fmt = _nom_fmt
    out = [str(labels[i]) if labels else (str(t) if isinstance(t, str) else fmt(t))
           for i, t in enumerate(ticks)]
    pa = var.get("points_at")
    if pa is None:
        n = len(ticks)
        pa = [k * 100.0 / (n - 1) for k in range(n)]
    else:
        if not (isinstance(pa, list) and len(pa) == len(ticks)):
            raise ValueError(f"nomogram: 「{disp}」points_at 长度必须与 ticks 一致")
        try:
            pa = [float(v) for v in pa]
        except (TypeError, ValueError):
            raise ValueError(f"nomogram: 「{disp}」points_at 必须全为数值")
        if any(v < 0.0 for v in pa) or (pts_hi is not None
                                        and any(v > pts_hi for v in pa)):
            hi = f"[0,{pts_hi:g}]" if pts_hi is not None else "非负"
            raise ValueError(f"nomogram: 「{disp}」points_at 须 {hi}")
    return out, pa


def gen_nomogram(data, ax, theme, cjk_fp, **kwargs):
    """nomogram 列线图（v5.3，第 33 号图型）：临床预测模型第四件——把多变量
    回归模型的贡献转成"查表尺"：各变量刻度→Points(0~100)→Total Points→
    结局概率。引擎只做可视化不拟合：points/points_at 请来自你已拟合的模型
    （R rms::nomogram / Python 统计包输出），方法学口径写入统计方法段。
    JSON: variables=[{name, ticks[2~12], labels?, points_at?}]
          outcome_scales=[{label, ticks, points_at}]（1~3 个，points 为总分口径）
          total_points_max 可选（默认=结局尺最大 points 或 100×变量数）。
    返回 "diagram" 哨兵（自管版面：无轴框/无网格）。"""
    variables = data.get("variables")
    if not (isinstance(variables, list) and 1 <= len(variables) <= 12):
        raise ValueError("nomogram: 需要 variables（1~12 个 {name, ticks, ...} 对象）")
    vlabels, vpoints, vnames = [], [], []
    for v in variables:
        if not isinstance(v, dict) or not v.get("name") or "ticks" not in v:
            raise ValueError("nomogram: variables 每项须为含 name/ticks 的对象")
        lab, pts = _nom_ticks(v, pts_hi=100.0, name_key="name")
        vnames.append(str(v["name"]))
        vlabels.append(lab)
        vpoints.append(pts)
    outcomes = data.get("outcome_scales") or []
    if not (isinstance(outcomes, list) and 1 <= len(outcomes) <= 3):
        raise ValueError("nomogram: 需要 outcome_scales（1~3 个 {label, ticks, points_at}）")
    olab, olabels, opoints = [], [], []
    for o in outcomes:
        if not isinstance(o, dict) or not o.get("label") or "ticks" not in o:
            raise ValueError("nomogram: outcome_scales 每项须为含 label/ticks 的对象")
        if o.get("points_at") is None:  # v7.9.0 AF26 新伤：静默线性默认会出错误尺
            print(f"WARNING: nomogram 结局尺「{o.get('label')}」未给 points_at——"
                  f"已按线性 0~100 默认映射到总积分轴，若模型总分上限非 100 概率刻度位置即错，"
                  f"请显式提供 points_at（该概率刻度对应的中介总分）", file=sys.stderr)
        lab, pts = _nom_ticks(o, pts_hi=None, name_key="label")
        olab.append(str(o["label"]))
        olabels.append(lab)
        opoints.append(pts)
    tmax = data.get("total_points_max")
    if tmax is not None:
        tmax = float(tmax)
        if not (tmax > 0):
            raise ValueError("nomogram: total_points_max 须为正数")
    else:
        pool = [p for row in opoints for p in row] or [100.0 * len(variables)]
        tmax = max(pool + [100.0])

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    cjk = cjk_fp
    fp = cjk  # 行名/刻度可能含中文，统一挂字体（无中文时 has_cjk 判空）
    x0, x1 = 0.055, 0.955
    W = x1 - x0

    def px(p, span):
        return x0 + (p / span) * W if span else x0

    rows = [("Points", ["0", "25", "50", "75", "100"],
             [0, 25, 50, 75, 100], 100.0, True)]
    for nm, labs, pts in zip(vnames, vlabels, vpoints):
        rows.append((nm, labs, pts, 100.0, False))
    # 自适应好台阶：在 4/5/8/10 等分中选步长最"整"（尾数最短）的方案
    tp_ticks = min(((k, len(str(round(tmax / k, 4)).split(".")[-1].rstrip("0")))
                    for k in (4, 5, 8, 10)), key=lambda x: x[1])[0]
    rows.append(("Total Points 总积分" if cjk else "Total Points",
                 [_nom_fmt(tmax * k / tp_ticks) for k in range(tp_ticks + 1)],
                 [tmax * k / tp_ticks for k in range(tp_ticks + 1)], tmax, True))
    for lb, labs, pts in zip(olab, olabels, opoints):
        rows.append((lb, labs, pts, tmax, False))

    n = len(rows)
    c_line, c_txt = "#333333", "#111111"
    for i, (nm, labs, pts, span, is_ruler) in enumerate(rows):
        y = -i * 1.0
        xs = [px(p, span) for p in pts]
        lw = 1.6 if is_ruler else 1.2
        ax.plot([min(xs), max(xs)], [y, y], color=c_line, lw=lw,
                solid_capstyle="butt", zorder=2)
        for k, x in enumerate(xs):
            ax.plot([x, x], [y, y - 0.14], color=c_line, lw=1.0, zorder=2)
            ax.text(x, y - 0.24, labs[k], ha="center", va="top", fontsize=fs_s,
                    color=c_txt, zorder=3,
                    fontproperties=fp if fp and has_cjk(labs[k]) else None)
        nm_disp = ("Points" if nm == "Points" and not cjk
                   else "Points 点数" if nm == "Points" else nm)
        ax.text(x0, y + 0.16, nm_disp, ha="left", va="bottom", fontsize=fs_s,
                color=c_txt, zorder=3,
                fontproperties=fp if fp and has_cjk(nm_disp) else None)
    ax.set_xlim(0, 1)
    ax.set_ylim(-(n - 1) * 1.0 - 0.75, 0.62)
    ax.axis("off")
    # 自管版面：行多则增高图幅（≥0.6in/行），根治多变量行距压缩
    _w = ax.figure.get_size_inches()[0]
    _h = min(13.0, max(ax.figure.get_size_inches()[1], 1.9 + 0.62 * n))
    ax.figure.set_size_inches(_w, _h)
    _pv = ["%s（%s）" % (vnames[i], "，".join(vlabels[i][:4])
                        + ("…" if len(vlabels[i]) > 4 else ""))
           for i in range(len(vnames))]
    print(f"nomogram: {len(vnames)} 个变量 + {len(olab)} 个结局尺"
          f"（Total Points 0~{tmax:g}）；变量：" + "；".join(_pv), file=sys.stderr)
    return "diagram"


def nomogram_alt(data, t=""):
    """v5.3：nomogram 的 --alt 文本。"""
    variables = data.get("variables") or []
    outcomes = data.get("outcome_scales") or []
    segs = []
    for v in variables:
        if isinstance(v, dict) and v.get("name"):
            ticks = v.get("ticks") or []
            segs.append(f"{v['name']}（{'，'.join(map(str, ticks[:5]))}"
                        f"{'…' if len(ticks) > 5 else ''}）")
    outs = []
    for o in outcomes:
        if isinstance(o, dict):
            pa = o.get("points_at") or []
            if pa:
                outs.append(f"{o.get('label', '结局')}（总分 {pa[0]}~{pa[-1]}）")
    return (f"列线图（{len(variables)} 个预测变量"
            + (f"，结局尺：{'、'.join(outs)}" if outs else "")
            + f"）：变量自上而下为 {'；'.join(segs)}；"
              "顶部 Points 尺逐变量计分，合计后查 Total Points 对应结局概率。"
              f"{t}")


def validate_nomogram(data):
    """v5.3：nomogram 数据校验（返回 fatal 列表）；与 gen_nomogram 同口径。"""
    fatal = []
    variables = data.get("variables")
    if not (isinstance(variables, list) and 1 <= len(variables) <= 12):
        return ["nomogram: 需要 variables（1~12 个 {name, ticks, ...} 对象）"]
    seen = set()
    for v in variables:
        if not isinstance(v, dict) or not v.get("name") or "ticks" not in v:
            fatal.append("nomogram: variables 每项须为含 name/ticks 的对象")
            continue
        try:
            _nom_ticks(v)
        except ValueError as e:
            fatal.append(str(e))
        nm = str(v["name"])
        if nm in seen:
            fatal.append(f"nomogram: 变量名重复「{nm}」")
        seen.add(nm)
    outcomes = data.get("outcome_scales") or []
    if not (isinstance(outcomes, list) and 1 <= len(outcomes) <= 3):
        fatal.append("nomogram: 需要 outcome_scales（1~3 个 {label, ticks, points_at}）")
        return fatal
    for o in outcomes:
        if not isinstance(o, dict) or not o.get("label") or "ticks" not in o:
            fatal.append("nomogram: outcome_scales 每项须为含 label/ticks 的对象")
            continue
        try:
            _nom_ticks(o, pts_hi=None, name_key="label")
        except ValueError as e:
            fatal.append(str(e))
    tmax = data.get("total_points_max")
    if tmax is not None:
        try:
            if not (float(tmax) > 0):
                fatal.append("nomogram: total_points_max 须为正数")
        except (TypeError, ValueError):
            fatal.append("nomogram: total_points_max 须为数值")
    return fatal


# ═══ v5.4：rcs 限制性立方样条曲线（临床回归线，第 34 图型）+ DCA 获益区着色 ═══

def gen_rcs(data, ax, theme, cjk_fp, **kwargs):
    """rcs 限制性立方样条/非线性剂量反应曲线（v5.4，第 34 号图型）：把已拟合
    样条模型的网格结果画成 带置信带的效应曲线（HR/OR 惯例对数轴 + 参照线）。
    JSON: points=[{value, est, ci_lo, ci_hi}]（≥5 点，来自你拟合的 RCS/Cox/
    Logistic 样条输出——引擎只可视化不拟合，方法学口径写入统计方法段）；
    ref 参照值（竖虚线，惯例=中位数）；log_y 默认 true（比值尺度；差值尺度
    传 false，此时参照水平线默认 y=0，可用 hline_at 覆盖）；hist=true 底部
    暴露变量 rug。"""
    import math as _m
    pts = data.get("points")
    if not (isinstance(pts, list) and len(pts) >= 5):
        raise ValueError("rcs: 需要 points（≥5 个 {value, est, ci_lo, ci_hi}，来自已拟合样条模型）")
    vals, ests, los, his = [], [], [], []
    for i, p in enumerate(pts):
        if not isinstance(p, dict) or not all(k in p for k in ("value", "est", "ci_lo", "ci_hi")):
            raise ValueError(f"rcs: points[{i}] 须为含 value/est/ci_lo/ci_hi 的对象")
        try:
            v, e, lo, hi = (float(p["value"]), float(p["est"]),
                            float(p["ci_lo"]), float(p["ci_hi"]))
        except (TypeError, ValueError):
            raise ValueError(f"rcs: points[{i}] 四个字段必须全为数值")
        if not all(_m.isfinite(x) for x in (v, e, lo, hi)):
            raise ValueError(f"rcs: points[{i}] 含非有限值——请清洗源数据")
        vals.append(v); ests.append(e); los.append(lo); his.append(hi)
    log_y = bool(data.get("log_y", True))
    if log_y and (min(ests) <= 0 or min(los) <= 0):
        raise ValueError("rcs: log_y=true 时 est/ci 必须 >0（比值尺度）；差值尺度请传 log_y=false")
    for i, (e, lo, hi) in enumerate(zip(ests, los, his)):
        if not (lo <= e <= hi):
            raise ValueError(f"rcs: points[{i}] 须 ci_lo ≤ est ≤ ci_hi")
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    sv = [vals[i] for i in order]
    for a, b in zip(sv, sv[1:]):
        if a == b:
            raise ValueError("rcs: points 的 value 有重复——样条网格须单调")
    hline_at = data.get("hline_at", 1.0 if log_y else 0.0)
    hline_at = float(hline_at)
    ref = data.get("ref")
    if ref is not None:
        ref = float(ref)
        if not (min(vals) <= ref <= max(vals)):
            raise ValueError("rcs: ref 须落在 points 的 value 范围内")

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    c_main = theme["colors"][0]
    xs = sv
    lo_s = [los[i] for i in order]
    hi_s = [his[i] for i in order]
    e_s = [ests[i] for i in order]
    # 置信带 + 效应线（端点必留 pad，类级铁律）
    ax.fill_between(xs, lo_s, hi_s, color=c_main, alpha=0.18, zorder=1)
    ax.plot(xs, e_s, color=c_main, lw=1.8, zorder=3)
    _xr = (max(xs) - min(xs)) * 0.04 or 0.5
    ax.set_xlim(min(xs) - _xr, max(xs) + _xr)
    lo_all, hi_all = min(lo_s + [hline_at]), max(hi_s + [hline_at])
    _yr = (hi_all - lo_all) * 0.06 or 0.1
    ax.set_ylim(lo_all - _yr, hi_all + _yr * 1.4)
    if log_y:
        ax.set_yscale("log")
        # 对数轴平实刻度（共享 helper，v5.5 起 subgroup 同用）
        from matplotlib.ticker import ScalarFormatter, NullFormatter
        _plain_log_ticks_x(ax)
        ax.yaxis.set_minor_formatter(NullFormatter())
    # 参照线：水平（无效应）+ 竖直（参照值）
    ax.axhline(hline_at, color="#999999", lw=1.1, ls=(0, (5, 4)), zorder=2)
    handles = [plt.Line2D([], [], color=c_main, lw=1.8),
               plt.Line2D([], [], color="#999999", lw=1.1, ls=(0, (5, 4)))]
    lbls = [(est_label := ("OR" if "OR" in str(data.get("y_label", "") or "") else "HR")) + ("（95%CI 带）" if cjk_fp else " (95%CI band)"),
            ("无效应" if cjk_fp else "No effect")]
    if ref is not None:
        ax.axvline(ref, color="#BBBBBB", lw=1.0, ls=(0, (3, 3)), zorder=2)
        ax.text(ref, hi_all + _yr * 0.9, f"ref={ref:g}", ha="center", va="bottom",
                fontsize=fs_s, color="#777777")
        handles.append(plt.Line2D([], [], color="#BBBBBB", lw=1.0, ls=(0, (3, 3))))
        lbls.append("参照值" if cjk_fp else "Reference")
    if bool(data.get("hist", True)):
        for v in xs:
            ax.plot([v, v], [lo_all - _yr * 0.75, lo_all - _yr * 0.35],
                    color="#AAAAAA", lw=0.9, zorder=2)
    xl = str(data.get("x_label") or ("" if not cjk_fp else ""))
    yl = str(data.get("y_label") or ("比值（对数轴）" if cjk_fp and log_y else ""))
    if xl:
        ax.set_xlabel(xl, fontsize=fs, fontproperties=cjk_fp if cjk_fp and has_cjk(xl) else None)
    if yl:
        ax.set_ylabel(yl, fontsize=fs, fontproperties=cjk_fp if cjk_fp and has_cjk(yl) else None)
    ax.legend(handles, lbls, loc="upper right", frameon=False, fontsize=fs_s,
              prop=cjk_fp if cjk_fp and has_cjk("".join(lbls)) else None)
    print(f"rcs: {len(vals)} 个网格点，value {min(xs):g}~{max(xs):g}"
          + (f"，ref={ref:g}" if ref is not None else "")
          + f"；est {min(e_s):g}~{max(e_s):g}（{'对数轴' if log_y else '线性轴'}）",
          file=sys.stderr)
    apply_base_style(ax, theme)


def rcs_alt(data, t=""):
    """v5.4：rcs 的 --alt 文本。"""
    pts = data.get("points") or []
    es = [float(p.get("est")) for p in pts
          if isinstance(p, dict) and isinstance(p.get("est"), (int, float))
          and not isinstance(p.get("est"), bool)]
    if es:
        seg = (f"效应在网格内介于 {min(es):g}~{max(es):g}"
               f"（{'对数轴' if data.get('log_y', True) else '线性轴'}）")
    else:
        seg = "带 95%CI 置信带的非线性效应曲线"
    return (f"限制性立方样条曲线（{len(pts)} 个网格点；{seg}）："
            "曲线偏离参照水平=存在非线性关联；置信带与参照水平相交处为无统计学差异区。"
            f"{t}")


def validate_rcs(data):
    """v5.4：rcs 数据校验（返回 fatal 列表）；与 gen_rcs 同口径。"""
    fatal = []
    pts = data.get("points")
    if not (isinstance(pts, list) and len(pts) >= 5):
        return ["rcs: 需要 points（≥5 个 {value, est, ci_lo, ci_hi}）"]
    for i, p in enumerate(pts):
        if not isinstance(p, dict) or not all(k in p for k in ("value", "est", "ci_lo", "ci_hi")):
            fatal.append(f"rcs: points[{i}] 须为含 value/est/ci_lo/ci_hi 的对象")
            continue
        try:
            v, e, lo, hi = (float(p["value"]), float(p["est"]),
                            float(p["ci_lo"]), float(p["ci_hi"]))
        except (TypeError, ValueError):
            fatal.append(f"rcs: points[{i}] 四个字段必须全为数值")
            continue
        if lo > e or e > hi:
            fatal.append(f"rcs: points[{i}] 须 ci_lo ≤ est ≤ ci_hi")
    if data.get("log_y", True):
        for i, p in enumerate(pts):
            if isinstance(p, dict):
                try:
                    if float(p["est"]) <= 0 or float(p["ci_lo"]) <= 0:
                        fatal.append("rcs: log_y=true 时 est/ci 必须 >0（差值尺度请传 log_y=false）")
                        break
                except (TypeError, ValueError, KeyError):
                    pass
    ref = data.get("ref")
    if ref is not None:
        try:
            vs = [float(p["value"]) for p in pts if isinstance(p, dict)]
            if not (min(vs) <= float(ref) <= max(vs)):
                fatal.append("rcs: ref 须落在 points 的 value 范围内")
        except (TypeError, ValueError, KeyError):
            pass
    return fatal


# ═══ v5.5：subgroup 亚组分析森林图（临床回归线，第 35 图型）═══

def _plain_log_ticks_x(ax):
    """_plain_log_ticks 的 y 轴变体（rcs 用）。"""
    from matplotlib.ticker import LogLocator
    _plain_log_ticks(ax)
    ax.yaxis.set_major_locator(LogLocator(base=10.0,
                                          subs=(1.0, 1.5, 2.0, 3.0, 5.0, 7.0),
                                          numticks=100))


def _bold_fontprops(cjk_fp, fs):
    """CJK 真粗体（v5.5 验收三轮意见的机制实现）：set_weight 对无 Bold face
    的 CJK 字体会静默回退 regular——此处优先找系统 Bold CJK 字面文件（如
    NotoSerifCJK-Bold.ttc）直接实例化；找不到则退化为描边路径效果（必然增粗）。
    返回 (fontprops|None, stroke_path_effect|None)。"""
    try:
        import matplotlib.font_manager as _fm
        _keys = ("Noto Sans CJK", "Noto Serif CJK", "Source Han", "WenQuanYi",
                 "Microsoft YaHei", "PingFang", "SimHei")
        _cands = [f.fname for f in _fm.fontManager.ttflist
                  if "bold" in f.fname.lower()
                  and any(k in (f.name or "") for k in _keys)]
        if _cands:
            fp = (cjk_fp.copy() if cjk_fp is not None else _fm.FontProperties())
            fp.set_file(_cands[0])
            return fp, None
    except Exception:
        pass
    try:
        import matplotlib.patheffects as _pe
        return None, _pe.withStroke(linewidth=max(0.8, fs * 0.05), foreground="#222222")
    except Exception:
        return None, None


def _plain_log_ticks(ax):
    """对数轴平实刻度（v5.4 验收 P1 的共享实现）：主刻度 1/1.5/2/3/5/7 子集
    + 标量格式化，禁 10⁰ 式科学计数法/偏移记法。所有对数轴图型统一走此 helper。"""
    from matplotlib.ticker import LogLocator, ScalarFormatter, NullFormatter
    ax.xaxis.set_major_locator(LogLocator(base=10.0,
                                          subs=(1.0, 1.5, 2.0, 3.0, 5.0, 7.0),
                                          numticks=100))
    _sf = ScalarFormatter()
    _sf.set_powerlimits((-3, 4))
    ax.xaxis.set_major_formatter(_sf)
    ax.xaxis.set_minor_formatter(NullFormatter())


def gen_subgroup_forest(data, ax, theme, cjk_fp, **kwargs):
    """subgroup 亚组分析森林图（v5.5，第 35 号图型）：亚组效应 + 交互检验
    一图呈现（NEJM/Lancet 风格：左侧亚组行、中间 CI 森林、右侧 est/p 列，
    亚组标题行报 P interaction，底部总效应菱形）。
    JSON: subgroups=[{name, p_interaction?, levels=[{name, est, ci_low, ci_high,
    n?, p?}]}]（1~12 组，每组 2~8 层）；overall={est, ci_low, ci_high, p?, n?}
    可选；est_label 决定无效线（比率 HR/OR/RR=1，差值 MD/SMD=0）；log_x 默认
    true（比率尺度惯例）。引擎只可视化不拟合：est/p 请来自你的亚组模型。"""
    import math as _m
    subgroups = data.get("subgroups")
    if not (isinstance(subgroups, list) and 1 <= len(subgroups) <= 12):
        raise ValueError("subgroup: 需要 subgroups（1~12 个 {name, levels} 对象）")
    parsed = []
    for sg in subgroups:
        if not isinstance(sg, dict) or not sg.get("name") or not isinstance(sg.get("levels"), list):
            raise ValueError("subgroup: subgroups 每项须为含 name/levels 的对象")
        if not (2 <= len(sg["levels"]) <= 8):
            raise ValueError(f"subgroup: 「{sg['name']}」levels 须 2~8 层")
        levels = []
        for lv in sg["levels"]:
            if not isinstance(lv, dict) or not lv.get("name"):
                raise ValueError(f"subgroup: 「{sg['name']}」levels 每项须含 name")
            try:
                e, lo, hi = float(lv["est"]), float(lv["ci_low"]), float(lv["ci_high"])
            except (KeyError, TypeError, ValueError):
                raise ValueError(f"subgroup: 「{sg['name']}」/{lv.get('name')} 须有数值 est/ci_low/ci_high")
            if not all(_m.isfinite(x) for x in (e, lo, hi)):
                raise ValueError(f"subgroup: 「{sg['name']}」/{lv['name']} 含非有限值")
            if not (lo <= e <= hi):
                raise ValueError(f"subgroup: 「{sg['name']}」/{lv['name']} 须 ci_low ≤ est ≤ ci_high")
            p = lv.get("p")
            if p is not None:
                p = float(p)
                if not (0.0 <= p <= 1.0):
                    raise ValueError(f"subgroup: 「{sg['name']}」/{lv['name']} p 须在 [0,1]")
            levels.append({"name": str(lv["name"]), "est": e, "lo": lo, "hi": hi,
                           "n": lv.get("n"), "p": p})
        pi = sg.get("p_interaction")
        if pi is not None:
            pi = float(pi)
            if not (0.0 <= pi <= 1.0):
                raise ValueError(f"subgroup: 「{sg['name']}」p_interaction 须在 [0,1]")
        parsed.append({"name": str(sg["name"]), "levels": levels, "pi": pi})
    overall = data.get("overall")
    if overall is not None:
        if not isinstance(overall, dict):
            raise ValueError("subgroup: overall 须为对象")
        try:
            overall = {**overall, "est": float(overall["est"]),
                       "lo": float(overall["ci_low"]), "hi": float(overall["ci_high"])}
        except (KeyError, TypeError, ValueError):
            raise ValueError("subgroup: overall 须有数值 est/ci_low/ci_high")
        if not (overall["lo"] <= overall["est"] <= overall["hi"]):
            raise ValueError("subgroup: overall 须 ci_low ≤ est ≤ ci_high")
    est_label = str(data.get("est_label") or "HR")
    log_x = bool(data.get("log_x", est_label.upper() in ("HR", "OR", "RR")))
    ref = 0.0 if est_label.upper() in ("MD", "SMD") else 1.0

    fs = theme["font_size"]
    fs_s = max(5.0, fs - 1.5)
    c_main = theme["colors"][0]
    c_alt = theme["colors"][1 % len(theme["colors"])]
    fp_bold, hdr_stroke = _bold_fontprops(cjk_fp, fs_s)

    # 行布局（自上而下）：组标题行+层行；底部 overall
    rows = []  # (kind, payload, y)
    y = 0.0
    all_ests = [lv["est"] for sg in parsed for lv in sg["levels"]]
    all_los = [lv["lo"] for sg in parsed for lv in sg["levels"]]
    all_his = [lv["hi"] for sg in parsed for lv in sg["levels"]]
    if overall:
        all_ests.append(overall["est"]); all_los.append(overall["lo"]); all_his.append(overall["hi"])
    for sg in parsed:
        rows.append(("header", sg, y))
        y -= 1.0
        for lv in sg["levels"]:
            rows.append(("level", lv, y))
            y -= 1.0
        y -= 0.45
    if overall:
        y -= 0.25
        rows.append(("overall", overall, y))
    n_rows = len(rows)

    # 绘制
    fp_hdr = cjk_fp
    for kind, payload, yy in rows:
        if kind == "header":
            _ht = ax.text(-0.145, yy, payload["name"], transform=ax.get_yaxis_transform(),
                          ha="left", va="center", fontsize=fs_s,
                          color="#222222",
                          fontproperties=fp_bold if fp_bold else (cjk_fp if cjk_fp and has_cjk(payload["name"]) else None))
            if hdr_stroke is not None:
                _ht.set_path_effects([hdr_stroke])
            _ht._af_keep_fp = True  # 兜底不得覆盖本对象的粗体字面（机制标记）
            if payload["pi"] is not None:
                _show_pi(payload["pi"], yy, fs_s, cjk_fp, ax)
        elif kind == "level":
            # 层名左对齐固定列（标题 x=-0.145，层名 x=-0.113）：缩进恒定、
            # 恒在绘图区外不压脊线（-0.113 为最长层名 TPS≥50% 留 >8px 余量，
            # 验收四轮实测值；禁右对齐锚点进 axes 内部）
            ax.text(-0.113, yy, payload["name"],
                    transform=ax.get_yaxis_transform(), ha="left", va="center",
                    fontsize=fs_s, color="#333333",
                    fontproperties=cjk_fp if cjk_fp and has_cjk(payload["name"]) else None)
            ax.plot([payload["lo"], payload["hi"]], [yy, yy], color="#555555",
                    lw=1.4, solid_capstyle="butt", zorder=3)
            ax.plot([payload["lo"], payload["lo"]], [yy - 0.14, yy + 0.14],
                    color="#555555", lw=1.2, zorder=3)
            ax.plot([payload["hi"], payload["hi"]], [yy - 0.14, yy + 0.14],
                    color="#555555", lw=1.2, zorder=3)
            sig = payload["p"] is not None and payload["p"] < 0.05
            ax.scatter([payload["est"]], [yy],
                       s=52 if sig else 40, marker="s",
                       c=c_main if sig else "white",
                       edgecolors=c_main, linewidths=1.2, zorder=4)
            _lv_txt = f"{payload['est']:.2f} ({payload['lo']:.2f}, {payload['hi']:.2f})"
            ax.text(1.03, yy, _lv_txt, transform=ax.get_yaxis_transform(),
                    ha="left", va="center", fontsize=fs_s, family="monospace",
                    color="#222222")
            if payload["p"] is not None:
                ax.text(1.30, yy, _fmt_p(payload["p"]), transform=ax.get_yaxis_transform(),
                        ha="left", va="center", fontsize=fs_s,
                        color="#8a1f1f" if sig else "#222222")
        else:  # overall
            ax.plot([payload["lo"], payload["hi"]], [yy, yy], color="#444444",
                    lw=1.6, zorder=3)
            ax.scatter([payload["est"]], [yy], s=110, marker="D", c=c_alt,
                       edgecolors="#333333", linewidths=0.9, zorder=4)
            ax.text(-0.02, yy, "Overall 总效应" if cjk_fp else "Overall",
                    transform=ax.get_yaxis_transform(), ha="right", va="center",
                    fontsize=fs_s, fontweight="bold",
                    fontproperties=fp_hdr if fp_hdr else None)
            ax.text(1.03, yy, f"{payload['est']:.2f} ({payload['lo']:.2f}, {payload['hi']:.2f})",
                    transform=ax.get_yaxis_transform(), ha="left", va="center",
                    fontsize=fs_s, family="monospace", fontweight="bold")
            if payload.get("p") is not None:
                ax.text(1.30, yy, _fmt_p(float(payload["p"])), transform=ax.get_yaxis_transform(),
                        ha="left", va="center", fontsize=fs_s, fontweight="bold")

    # 轴：est 尺度 + 无效线 + 平实对数刻度
    lo_all, hi_all = min(all_los), max(all_his)
    if log_x:
        lo_all, hi_all = max(lo_all, 1e-3), hi_all
        _pad_lo, _pad_hi = lo_all / 1.25, hi_all * 1.25
        ax.set_xlim(_pad_lo, _pad_hi)
        ax.set_xscale("log")
        _plain_log_ticks(ax)
        ax.axvline(ref, color="#999999", lw=1.0, ls=(0, (5, 4)), zorder=1)
    else:
        _pad = (hi_all - lo_all) * 0.08 or 0.1
        ax.set_xlim(lo_all - _pad, hi_all + _pad)
        ax.axvline(ref, color="#999999", lw=1.0, ls=(0, (5, 4)), zorder=1)
    ax.set_ylim(y - 0.9, 1.35)
    ax.set_yticks([])
    xl = str(data.get("x_label") or est_label)
    ax.set_xlabel(xl, fontsize=fs, fontproperties=cjk_fp if cjk_fp and has_cjk(xl) else None)
    # 列头
    ax.text(1.03, 1.02, est_label + (" (95% CI)" if "CI" not in est_label else ""),
            transform=ax.get_yaxis_transform(), ha="left", va="bottom", fontsize=fs_s)
    if any(lv["p"] is not None for sg in parsed for lv in sg["levels"]) \
            or (overall and overall.get("p") is not None):
        ax.text(1.30, 1.02, "P", transform=ax.get_yaxis_transform(),
                ha="left", va="bottom", fontsize=fs_s)
    ax._af_category_axis = True  # 行名是数据：豁免防重叠抽稀
    _n_lv = sum(len(sg["levels"]) for sg in parsed)
    _sig_int = sum(1 for sg in parsed if sg["pi"] is not None and sg["pi"] < 0.05)
    print(f"subgroup: {len(parsed)} 个亚组变量 / {_n_lv} 层"
          + (f"+overall" if overall else "")
          + f"；交互显著（P<0.05）{_sig_int} 个", file=sys.stderr)
    apply_base_style(ax, theme)


def _show_pi(pi, y, fs, cjk_fp, ax):
    ax.text(1.30, y, _fmt_p(pi), transform=ax.get_yaxis_transform(),
            ha="left", va="center", fontsize=fs, fontweight="bold",
            color="#8a1f1f" if pi < 0.05 else "#555555")


def _fmt_p(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def subgroup_alt(data, t=""):
    subgroups = data.get("subgroups") or []
    segs = []
    for sg in subgroups:
        if isinstance(sg, dict) and sg.get("name"):
            lv = sg.get("levels") or []
            names = "、".join(str(l.get("name", "?")) for l in lv[:4] if isinstance(l, dict))
            pi = sg.get("p_interaction")
            segs.append(f"{sg['name']}（{names}{'…' if len(lv) > 4 else ''}"
                        f"{f'；P 交互={pi}' if pi is not None else ''}）")
    return (f"亚组分析森林图（{len(subgroups)} 个亚组变量）：{'；'.join(segs)}。"
            "方块=各层效应估计，横线=95%CI，菱形=总效应；P 交互<0.05 提示效应"
            f"存在亚组异质性。{t}")


def validate_subgroup(data):
    """v5.5：subgroup 数据校验（返回 fatal 列表）；与 gen_subgroup_forest 同口径。"""
    fatal = []
    subgroups = data.get("subgroups")
    if not (isinstance(subgroups, list) and 1 <= len(subgroups) <= 12):
        return ["subgroup: 需要 subgroups（1~12 个 {name, levels} 对象）"]
    for sg in subgroups:
        if not isinstance(sg, dict) or not sg.get("name") or not isinstance(sg.get("levels"), list):
            fatal.append("subgroup: subgroups 每项须为含 name/levels 的对象")
            continue
        if not (2 <= len(sg["levels"]) <= 8):
            fatal.append(f"subgroup: 「{sg['name']}」levels 须 2~8 层")
        for lv in sg["levels"]:
            if not isinstance(lv, dict) or not lv.get("name"):
                fatal.append(f"subgroup: 「{sg['name']}」levels 每项须含 name")
                continue
            try:
                if not (float(lv["ci_low"]) <= float(lv["est"]) <= float(lv["ci_high"])):
                    fatal.append(f"subgroup: 「{sg['name']}」/{lv['name']} 须 ci_low ≤ est ≤ ci_high")
            except (KeyError, TypeError, ValueError):
                fatal.append(f"subgroup: 「{sg['name']}」/{lv.get('name')} 须有数值 est/ci_low/ci_high")
            p = lv.get("p")
            if p is not None and not (0.0 <= float(p) <= 1.0):
                fatal.append(f"subgroup: 「{sg['name']}」/{lv['name']} p 须在 [0,1]")
        pi = sg.get("p_interaction")
        if pi is not None and not (0.0 <= float(pi) <= 1.0):
            fatal.append(f"subgroup: 「{sg['name']}」p_interaction 须在 [0,1]")
    return fatal


def write_repro_bundle(argv, data, out_path, extra_outputs=None):
    """v5.1 --repro：复跑交付包 <output>.repro/——数据副本+精确命令+README+
    audit.json+成图副本，任何人拿到包即可逐字节复现该图（确定性引擎：
    同输入同命令=同输出）。幂等：重跑整目录重建。"""
    import hashlib
    import json as _json
    import os as _os
    import shutil as _sh

    d = str(out_path) + ".repro"
    if _os.path.isdir(d):
        _sh.rmtree(d)
    _os.makedirs(d)
    with open(_os.path.join(d, "command.txt"), "w", encoding="utf-8") as fh:
        fh.write(" ".join(argv) + "\n")
    # 数据副本（argv 里的 -d/--data 文件原样拷贝）
    try:
        di = argv.index("-d") if "-d" in argv else argv.index("--data")
        src = argv[di + 1]
        if _os.path.isfile(src):
            _sh.copy2(src, _os.path.join(d, _os.path.basename(src)))
    except (ValueError, IndexError):
        pass
    # 成图副本（主输出 + v5.2 起多格式交付的全部导出文件）
    copied = set()
    for p in [str(out_path)] + [str(x) for x in (extra_outputs or [])]:
        if p and _os.path.isfile(p) and _os.path.basename(p) not in copied:
            _sh.copy2(p, _os.path.join(d, _os.path.basename(p)))
            copied.add(_os.path.basename(p))
    # audit（与 --audit 同一套独立重算）
    audit = {}
    def _stats(vals):
        xs = sorted(float(v) for v in vals
                    if isinstance(v, (int, float)) and not isinstance(v, bool)
                    and np.isfinite(float(v)))
        n = len(xs)
        if not n:
            return {"n": 0}
        mean = sum(xs) / n
        var = sum((x - mean) ** 2 for x in xs) / (n - 1) if n > 1 else 0.0
        med = xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2
        return {"n": n, "mean": round(mean, 6), "sd": round(var ** 0.5, 6),
                "median": round(med, 6), "min": round(xs[0], 6), "max": round(xs[-1], 6)}
    stats = {}
    for container in ("datasets", "series", "groups"):
        obj = data.get(container)
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, list):
                    stats[f"{container}.{k}"] = _stats(v)
    raw = _json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
    audit = {"chart_type": data.get("_chart_type", ""),
             "generated_by": "academic-figures --repro",
             "input_sha256_12": hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12],
             "stats": stats}
    with open(_os.path.join(d, "audit.json"), "w", encoding="utf-8") as fh:
        fh.write(_json.dumps(audit, ensure_ascii=False, indent=1, sort_keys=True))
    readme = (
        "# 复跑说明 / REPRODUCE\n\n"
        "- 命令（逐字复跑）：见 `command.txt`\n"
        "- 输入数据：本目录内的数据文件副本（与原始输入逐字节一致）\n"
        f"- 成图副本：本目录内与交付物逐字节一致"
        + (f"（含 {len(copied)} 个导出格式文件）" if len(copied) > 1 else "") + "\n"
        "- audit.json：描述统计由输入独立重算（纯计数零推断），可逐项核对图上的数\n"
        "- 确定性保证：同输入+同命令 → 同字节输出（引擎无随机源/无时间戳）\n"
        "- 依赖：matplotlib + numpy（+scipy 仅 --stats/KDE 类图型）；中文字体：系统 CJK 字体或 --cjk-font 指定\n"
    )
    with open(_os.path.join(d, "README_REPRODUCE.md"), "w", encoding="utf-8") as fh:
        fh.write(readme)
    print(f"repro: 复跑交付包已写 {d}{_os.sep}（命令/数据副本/成图副本/audit/README）",
          file=sys.stderr)
    return d


# v5.2：--suggest 输出双语化（domestic 反馈：辅助输出此前以英文为主）
# ── v6.9.0 sig-bracket 组间显著性括号 ─────────────────────────────────
def pairwise_all(series):
    """v7.0.0 --sig-auto：全部两两比较（itertools.combinations）。
    Shapiro 常态判定（双组均 p>0.05 → Welch t；否则 Mann-Whitney U）——
    与 pairwise_vs_first 同构检验家族。返回 [(a, b, p_or_None), ...]。"""
    from scipy import stats as _st
    import itertools as _it
    out = []
    for a, b in _it.combinations(list(series.keys()), 2):
        xa = [float(v) for v in series[a] if v is not None]
        xb = [float(v) for v in series[b] if v is not None]
        if len(xa) < 2 or len(xb) < 2:
            out.append((a, b, None))
            continue
        try:
            norm = (_st.shapiro(xa).pvalue > 0.05
                    and _st.shapiro(xb).pvalue > 0.05)
        except Exception:
            norm = False
        try:
            if norm:
                p = float(_st.ttest_ind(xa, xb, equal_var=False).pvalue)
            else:
                p = float(_st.mannwhitneyu(xa, xb).pvalue)
        except Exception:
            p = None
        out.append((a, b, p))
    return out


def compute_bracket_layers(pairs):
    """comparisons 分层布局纯函数：pairs=[(i, j), ...]（组索引对，i<j 自动归一）。
    经典区间重叠最低层分配（span 长的先放矮层）→ 返回与输入同序的 layer 列表。
    同层两条 bracket 的 [i,j] 闭区间重叠即视为冲突（共享端点=竖线相撞，也算）。"""
    idx = sorted(range(len(pairs)), key=lambda k: -(max(pairs[k]) - min(pairs[k])))
    placed, out = [], [0] * len(pairs)
    for k in idx:
        i, j = min(pairs[k]), max(pairs[k])
        layer = 0
        while any(pl == layer and not (pj < i or pi > j) for (pi, pj, pl) in placed):
            layer += 1
        out[k] = layer
        placed.append((i, j, layer))
    return out


def _maybe_draw_brackets(data, ax, kwargs, chart_name=None):
    """GENERATORS wrapper 钩子：--sig-bracket + JSON comparisons → 组间显著性括号。
    组名经 ax tick 标签映射（bar/box/violin 三族 tick 均为组名）；horizontal 模式
    暂不支持（[ignored] 告知）；未知组名 raise ValueError（中文诊断）。"""
    if not (kwargs.get("sig_bracket") or kwargs.get("sig_auto")):
        return
    if chart_name is not None and chart_name not in (
            "bar", "grouped_bar", "box", "violin"):
        print("[ignored] --sig-bracket 对 " + chart_name + " 不适用（仅 bar/grouped_bar/box/violin）", file=sys.stderr)
        return
    comps = data.get("comparisons")
    if (not comps or not isinstance(comps, list)) and kwargs.get("sig_auto"):
        _auto_domains = ("box", "violin", "raincloud")
        if chart_name not in _auto_domains:
            print("[ignored] --sig-auto 仅对 box/violin/raincloud 的原始分布数据自动检验；"
                  "聚合图请改用 comparisons 字段 + --sig-bracket", file=sys.stderr)
            return
        _ser = data.get("series") or data.get("groups") or {}
        if not isinstance(_ser, dict) or len(_ser) < 2:
            print("[ignored] --sig-auto 需要 ≥2 组原始数据（series/groups）", file=sys.stderr)
            return
        try:
            _pairs = pairwise_all(_ser)
        except ImportError:
            print("WARNING: --sig-auto 需要 scipy（pip install scipy）", file=sys.stderr)
            return
        comps = [{"a": a, "b": b, "p": p} for (a, b, p) in _pairs if p is not None]
        _n_ns = sum(1 for (_a, _b, p) in _pairs if p is None)
        if _n_ns:
            print(f"WARNING: --sig-auto {_n_ns} 组样本量 <2 无法检验，已跳过", file=sys.stderr)
        print(f"[sig-auto] 两两检验 {_pairs and len(_pairs)} 对（Shapiro 判常态："
              "双常态组 Welch t / 否则 Mann-Whitney U）", file=sys.stderr)
        print("[sig-auto] 检验假设（样本独立性/随机抽样）请自行确认；"
              "论文引用时请报告所用检验方法与各组 n", file=sys.stderr)
    if not comps or not isinstance(comps, list):
        print("[ignored] --sig-bracket 需要数据携带 comparisons 字段"
              "（示例: [{a:组A, b:组B, p:0.03}, ...]）", file=sys.stderr)
        return
    if kwargs.get("horizontal"):
        print("[ignored] --sig-bracket 暂不支持 horizontal 模式", file=sys.stderr)
        return
    ticks = [t.get_text() for t in ax.get_xticklabels()]
    pos_map = {name: k for k, name in enumerate(ticks) if name}
    if len(pos_map) < 2:
        print("[ignored] --sig-bracket 未识别到组名 tick（需 ≥2 组）", file=sys.stderr)
        return
    pairs, stars = [], []
    for c in comps:
        a, b = c.get("a"), c.get("b")
        if a not in pos_map or b not in pos_map:
            raise ValueError(
                f"comparisons 引用未知组名 {a!r}/{b!r}；有效组名: {sorted(pos_map)}")
        if a == b:
            raise ValueError(f"comparisons 的 a/b 不可为同组（{a!r}）")
        p = c.get("p")
        if p is None:
            label = str(c.get("label") or _sig_stars(float(c.get("p", 1.0))))
        else:
            label = _sig_stars(float(p))
        pairs.append((pos_map[a], pos_map[b]))
        stars.append(label)
    layers = compute_bracket_layers(pairs)
    n_layer = max(layers) + 1
    y0, y1 = ax.get_ylim()
    span = (y1 - y0) or 1.0
    step = span * 0.09
    pad = span * 0.02
    base = y1 + pad
    ax.set_ylim(top=base + step * n_layer + pad)
    width = (max(pos_map.values()) - min(pos_map.values())) / max(len(pos_map) - 1, 1) * 0.12
    for (i, j), layer, s in zip(pairs, layers, stars):
        yb = base + step * layer
        ax.plot([i, i, j, j], [yb, yb + step * 0.32, yb + step * 0.32, yb],
                color="#333333", linewidth=1.1, clip_on=False, zorder=5)
        ax.text((i + j) / 2, yb + step * 0.42, s, ha="center", va="bottom",
                fontsize=9, color="#333333", zorder=5)
    print(f"[sig-bracket] {len(pairs)} 组间比较 → {n_layer} 层"
          f"（星号阈值 <0.05/<0.01/<0.001；NS=不显著）", file=sys.stderr)


def _wrap_brackets(fn, chart_name=None):
    def _w(data, ax, theme, cjk_fp, **kwargs):
        extra = fn(data, ax, theme, cjk_fp, **kwargs)
        _maybe_draw_brackets(data, ax, kwargs, chart_name)
        return extra
    _w.__name__ = fn.__name__
    _w.__doc__ = fn.__doc__
    return _w



_SUGGEST_TYPE_ZH = {
    "bar": "柱状图", "grouped_bar": "分组柱状图", "hbar": "横向条形图",
    "stacked_bar": "堆叠柱状图", "heatmap": "热图", "scatter": "散点图",
    "line": "折线图", "dual_axis": "双轴图", "box": "箱线图",
    "forest": "森林图", "km": "生存曲线", "roc": "ROC 曲线",
    "violin": "小提琴图", "composite": "组合图", "diagram": "流程示意图", "flow": "流程图",
    "prisma": "PRISMA 流程图", "funnel": "Meta 漏斗图",
    "bland_altman": "Bland-Altman 一致性", "pca": "PCA 降维",
    "paired": "配对图", "venn": "韦恩图", "cluster_heatmap": "聚类热图",
    "upset": "UpSet 交集图", "raincloud": "雨云图", "slope": "斜率图",
    "volcano": "火山图", "swimmer": "游泳图", "waterfall": "瀑布图",
    "ridgeline": "山脊图", "dumbbell": "哑铃图",
    "calibration": "校准曲线", "dca": "决策曲线", "rmst": "RMST 限制平均生存时间", "rob": "偏倚风险交通灯图",
}


def format_suggest_line(idx, score, ctype, why):
    """--suggest 单行双语：英文理由后追加图型中文名（未知类型静默回退英文）。"""
    zh = _SUGGEST_TYPE_ZH.get(ctype)
    return f"  [{idx}] {ctype:<12} score {score:<3} — {why}" + (f"（{zh}）" if zh else "")


def suggest_arena_note(best):
    """v7.7 --suggest 附属提示（返回 str，空串=不打印）：bar 默认竞技场+sketch 榜单配方。"""
    if best in ("bar", "hbar"):
        return ("[arena] bar 单系列默认竞技场风格（冠军=最高柱；负面指标请 --arena off）；"
                "基准榜单场景推荐加 --style sketch 手绘风。")
    return ""


_RAW_GENERATORS = {
    "bar": gen_bar,
    "grouped_bar": gen_bar,
    "hbar": gen_bar,
    "horizontal_bar": gen_bar,
    "stacked_bar": gen_stacked_bar,
    "heatmap": gen_heatmap,
    "scatter": gen_scatter,
    "line": gen_line,
    "dual_axis": gen_dual_axis,

    "box": gen_box,
    "boxplot": gen_box,
    "forest": gen_forest,
    "km": gen_km,
    "survival": gen_km,
    "roc": gen_roc,
    "violin": gen_violin,
    "composite": gen_composite,
    "diagram": gen_diagram,
    "flow": gen_flow,
    "prisma": gen_prisma,
    "slope": gen_slope,
    "volcano": gen_volcano,
    "upset": gen_upset,
    "waterfall": gen_waterfall,
    "swimmer": gen_swimmer,
    "ridgeline": gen_ridgeline,
    "dumbbell": gen_dumbbell,
    "raincloud": gen_raincloud,
    "calibration": gen_calibration,
    "dca": gen_dca,
    "nomogram": gen_nomogram,
    "rcs": gen_rcs,
    "subgroup": gen_subgroup_forest,
}
GENERATORS = {k: _wrap_brackets(v, k) for k, v in _RAW_GENERATORS.items()}
