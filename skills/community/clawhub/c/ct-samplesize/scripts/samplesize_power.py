#!/usr/bin/env python3
"""
Clinical Trial Sample Size & Power Calculator — v5.0.2

Architecture (v5):
- Default authoritative engine = remote coze R compute service (CozeBackend).
  Only trial-design params are sent (HTTP POST, no shell, no local R).
- v5 removed the local pure-Python fallback (LocalPythonBackend) and all
  third-party compute deps (statsmodels / numpy / scipy no longer required).
  select_backend() returns ONLY CozeBackend; coze unreachable → error, no fallback.
- Local R backend (LocalRBackend, in adapters/local-r/) is dev/transition only and is
  NOT shipped in the published package.
- Safe by default: --dry-run previews the exact coze request envelope; coze is
  a stateless compute service, so no local code is ever executed. The legacy
  --yes gate applies only to the optional local-R backend.
- Every user string that reaches server-side R is validated against a strict
  allowlist, so it can NEVER break out of an R string literal.
- Input args validated against strict allowlists regardless of backend.

Test types (65 total):
  Core: ttest_ind, ttest_paired, anova, proportion_one, proportion_two,
        non_inferiority, equivalence, be_tost, mixed_model, roc, poisson,
        bland_altman, cluster, vaccine_efficacy, multiple_endpoints,
        bayesian, dose_escalation
  New in v3.3: win_ratio, must_win, historical_controls, mams,
        conditional_power, ni_survival, superiority_margin, assurance,
        dunnett, mediation, group_sequential, adaptive, survival_exact
  New in v3.5 (PASS-survival): survival_equivalence, survival_superiority,
        cox_covariate, survival_one_sample, competing_risks,
        recurrent_events, survival_historical
  New in v3.6 (PASS Group-Sequential, rpact-backed): group_sequential
        (upgraded to rpact exact two-sample means), gsd_proportion,
        gsd_survival, gsd_hazard, gsd_poisson; real spending functions
        (OF/Pocock/WT/HSD-gamma/Kim-DeMets) + non-binding futility bounds
  New in v5.9.0 (Tier 1 PASS-coverage): correlation, variance_one,
        variance_two, cv_one, ci_mean, ci_prop, ci_or, ci_rr, ci_cor,
        ci_icc, regression_linear, meta_planning
  New in v5.10.0 (Tier 2 PASS-coverage): regression_logistic,
        regression_poisson, cluster_ext, rates_ext
"""
import argparse, sys, os, io, tempfile, re, json, time
from i18n import t, resolve_user_language
from compute_backend import select_backend, Result, Figure
from r_code_policy import r_code_unavailable, is_paid_env

# P1-C: local Monte-Carlo verification of an analytic sample-size solution
# (power ±2pp / TIE ±0.5pp). Independent implementation — does NOT reuse the
# analytic formulas, so a wrongly-derived n is caught, not rubber-stamped.
try:
    from verify import run_verify as _verify_run, format_report as _verify_fmt
except Exception:  # pragma: no cover — verify.py always ships alongside
    _verify_run = None
    _verify_fmt = None

# ── E1/E2: 本地确定性 NL 路由 + 参数别名解析（零 LLM；解析失败时由本地 agent 向用户追问，原始 NL 不入 coze）──
# 同目录 import（脚本可直接运行，也兼容从其他 cwd 经 subprocess 调用）
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
try:
    from classify_test import classify as _nl_classify
    from param_aliases import extract_parameters as _nl_extract
    _NL_AVAILABLE = True
except Exception:  # pragma: no cover — 缺模块时降级为「无 --nl 能力」
    _NL_AVAILABLE = False


# ═════════════════════════════════════════════════════════════════════════════
# 图形产物落盘与展示（coze 可能回传 SVG / HTML / PNG）
# ═════════════════════════════════════════════════════════════════════════════

# ── 输入白名单校验（编排层职责：无论送往 coze 还是本地 R，都先卡死危险字符）──
_SAFE_TOKEN_RE = re.compile(r'^[A-Za-z0-9_\-]+$')
_SAFE_PATH_RE = re.compile(r'^[A-Za-z0-9_.\- /\\:一-鿿]+$')


def _validate_token(name, value):
    """Reject categorical string args that could break out into generated code."""
    if value is None:
        return value
    if not _SAFE_TOKEN_RE.match(value):
        raise ValueError(
            "Invalid %s=%r: only [A-Za-z0-9_-] allowed "
            "(no quotes, semicolons or parentheses)." % (name, value)
        )
    return value


def _validate_path(path):
    """Reject output paths containing characters that could escape a string literal."""
    if path is None:
        return None
    if not _SAFE_PATH_RE.match(path):
        raise ValueError(
            "Unsafe output path %r: only letters, digits, spaces and ._-:/\\ "
            "are allowed (no quotes, semicolons or parentheses)." % path
        )
    return path


_FIG_EXT = {"svg": ".svg", "html": ".html", "png": ".png"}

# ── 渲染计时与超阈值提示（ct-base §19.10，全库统一）──
# 界面浏览器渲染无法在 agent 侧精确计时，用 SVG 体量作代理；超阈值生成 render_hint
RENDER_SVG_THRESHOLD = 30.0       # 本地渲染处理耗时上限（秒）
RENDER_SVG_KB_THRESHOLD = 200.0   # 单图/合计 SVG 体量上限（KB）


def _outputs_dir() -> str:
    """图形落盘目录：优先 CTSS_OUTPUT_DIR，其次当前工作目录下的 outputs/。"""
    d = os.environ.get("CTSS_OUTPUT_DIR") or os.path.join(os.getcwd(), "outputs")
    os.makedirs(d, exist_ok=True)
    return d


#: 契约缺失时的默认出图集合（与 v5.3.1 硬编码一致；契约就绪后由 _auto_curve_tests 取代）
_FALLBACK_AUTO_CURVE_TESTS = frozenset({
    "ttest_ind", "ttest_paired", "ttest_one",
    "proportion_one", "proportion_two",
})
_AUTO_CURVE_TESTS_CACHE = None


def _auto_curve_tests() -> frozenset:
    """从 tests/coze_cases/_contract_index.json 读取 default_curve=true 的 test 集合。

    单一真相源（v5.3.2）：每种检验方法「默认是否自动出曲线」由契约的
    default_curve 字段分别配置（改契约即改默认出图，无需改代码）；
    契约缺失 / 未登记字段时回退硬编码集合（与前版本行为一致）。
    """
    global _AUTO_CURVE_TESTS_CACHE
    if _AUTO_CURVE_TESTS_CACHE is not None:
        return _AUTO_CURVE_TESTS_CACHE
    try:
        idx_path = (Path(__file__).resolve().parent.parent
                    / "adapters" / "workbench" / "publish" / "tests" / "coze_cases"
                    / "_contract_index.json")
        data = json.loads(Path(idx_path).read_text(encoding="utf-8"))
        s = frozenset(
            t["test"] for t in data.get("tests", [])
            if t.get("default_curve") is True
        )
        _AUTO_CURVE_TESTS_CACHE = s or _FALLBACK_AUTO_CURVE_TESTS
    except Exception:  # noqa: BLE001 - 契约缺失时回退硬编码
        _AUTO_CURVE_TESTS_CACHE = _FALLBACK_AUTO_CURVE_TESTS
    return _AUTO_CURVE_TESTS_CACHE


def _resolve_figure_mode(explicit=None) -> str:
    """出图模式（ct-base §19.9）：svg_inline 默认；png_file 用 cairosvg 转位图。

    优先级：显式参数 > 环境变量 CTSS_FIGURE_MODE > 默认 svg_inline。
    """
    mode = (explicit or os.environ.get("CTSS_FIGURE_MODE") or "svg_inline").lower()
    return mode if mode in ("svg_inline", "png_file") else "svg_inline"


def _ratio_is_unequal(ratio):
    """用户是否显式要求组间不等比例分配（n2/n1 != 1）。

    判定口径：--ratio 缺失（None）或显式 =1.0 均视为等例，本地 HTML 渲染层
    据此隐藏 coze 默认返回的「分配比四图」；仅当 ratio 有效且 != 1 才展示。
    注意：hazard_ratio / rate_ratio / win_ratio_theta 等是**效应量**，绝不在此判定。
    """
    if ratio is None:
        return False
    try:
        return abs(float(ratio) - 1.0) > 1e-9
    except (TypeError, ValueError):
        return False


def _is_alloc_figure(fig):
    """识别 coze 返回的分配比四图：caption 含 'alloc' 字样（如 'ctss alloc ttest ind 1'）。"""
    cap = fig.get("caption") if isinstance(fig, dict) else getattr(fig, "caption", "")
    return "alloc" in (cap or "").lower()


def _filter_alloc(figs, show_alloc):
    """本地渲染层过滤：show_alloc=False 时剔除分配比图（coze 端仍返回全量）。"""
    if show_alloc:
        return figs
    return [f for f in figs if not _is_alloc_figure(f)]


# 跨 render_figures 调用单调递增的落盘文件序号：避免默认出图（批量折叠）时曲线
# 调用从 1 重新开始、覆盖主线首图 ctss_<test>_1.svg（pre-existing 磁盘归档层缺陷）。
# 每次 CLI 调用在 main() 入口重置为 0，保证序号确定性且跨调用唯一。
_FIG_FILE_SEQ = 0


def render_figures(figures, test: str, figure_mode=None, show_alloc=True):
    """把后端回传的图形写入磁盘，并打印标记供宿主渲染。
    落盘文件序号由模块级 _FIG_FILE_SEQ 跨调用单调递增（见下方循环），避免曲线覆盖主线首图。

    标记格式（宿主 agent 据此调用可视化 / 文件展示能力）：
        __FIGURE__ <format> <abs_path> caption="..."
        __SVG_WIDGET__ <html fragment>   # SVG 图：ct-base §19 内联渲染（宿主直接内嵌对话流）
        __RENDER_HINT__ <text>           # 超阈值提醒（ct-base §19.10），agent 必须在回复中体现

    出图模式（figure_mode，ct-base §19.9）：
        - svg_inline（默认）：__SVG_WIDGET__ 内联 + 落盘 .svg
        - png_file：cairosvg 转 PNG 落盘，emit __FIGURE__ png（不内联 SVG；需 cairosvg，
          未安装时优雅降级回 svg_inline 并提示）

    渲染计时与超阈值提示（ct-base §19.10）：
        - render_elapsed_seconds：本地渲染阶段耗时（拿到 SVG → widget/PNG 就绪）
        - render_svg_kb：所有 SVG 字节合计（KB），界面渲染无法精确计时，用此作代理
        - 任一超阈值（>30s / >200KB）生成 __RENDER_HINT__，建议切换 png_file
    """
    global _FIG_FILE_SEQ

    if not figures:
        return
    # 本地渲染层：未显式要求不等比例分配时，剔除 coze 默认返回的「分配比四图」
    figures = _filter_alloc(figures, show_alloc)
    if not figures:
        return
    outdir = _outputs_dir()
    mode = _resolve_figure_mode(figure_mode)
    svg_figs = []
    _svg_paths = []
    _svg_kb = 0.0
    _t0 = time.time()
    for fig in figures:
        _FIG_FILE_SEQ += 1
        i = _FIG_FILE_SEQ
        fmt = (fig.format or "svg").lower()
        ext = _FIG_EXT.get(fmt, ".txt")
        path = os.path.join(outdir, "ctss_%s_%d%s" % (test, i, ext))
        content = fig.content or ""
        if fmt == "png" and not content.lstrip().startswith("<"):
            import base64
            with open(path, "wb") as f:
                f.write(base64.b64decode(content))
        else:
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(content)
        if fmt == "svg":
            svg_figs.append({"svg": content, "type": fig.caption or "ct-samplesize 图"})
            _svg_paths.append(path)
            _svg_kb += len(content.encode("utf-8")) / 1024.0
        # 2026-08-28 设计修订（用户定）：对话流不展示单张图形，仅 HTML 报告全量展示。
        # __FIGURE__ svg/png（会触发宿主内联展示）默认关闭，仅保留落盘供归档/下载；
        # 宿主如需逐图内联展示，设 CTSS_INLINE_WIDGET=1 恢复。
        if os.environ.get("CTSS_INLINE_WIDGET") == "1":
            print('__FIGURE__ %s %s caption="%s"' % (fmt, path, (fig.caption or "").replace('"', "'")))
    # ct-base §19：SVG 内联渲染（复用统一 adapters/rendering.py 管线）
    if svg_figs:
        try:
            _skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            _adapters_dir = os.path.join(_skill_root, "adapters")
            for _p in (_skill_root, _adapters_dir):
                if _p not in sys.path:
                    sys.path.insert(0, _p)
            from rendering import build_figure_widget, svg_to_png  # type: ignore  # adapters/rendering.py

            if mode == "png_file":
                # 本地 cairosvg 转 PNG（同一处理链：strip clip → fix xml → bbox → viewBox → 光栅化）
                for f in svg_figs:
                    _FIG_FILE_SEQ += 1
                    try:
                        png_path = os.path.join(outdir, "ctss_%s_%d.png" % (test, _FIG_FILE_SEQ))
                        svg_to_png(f["svg"], png_path, scale=2.0)
                        if os.environ.get("CTSS_INLINE_WIDGET") == "1":
                            print('__FIGURE__ png %s caption="%s"' % (png_path, (f.get("type") or "").replace('"', "'")))
                    except Exception as e:  # noqa: BLE001 - cairosvg 缺失/失败 → 优雅降级
                        print("# png_file 转换失败，降级 svg_inline: %s" % e)
                        mode = "svg_inline"
                        break
            if mode == "svg_inline":
                # 2026-08-28 设计修订（用户定）：对话流不再内联 SVG 图形，
                # 图形展示完全交给 render_html_report 全量输出（HTML 报告）。
                # 这里只落盘 SVG 源文件 + __FIGURE__ svg 标记供下载/归档；
                # 若宿主仍需对话流内联，可设 CTSS_INLINE_WIDGET=1 恢复 __SVG_WIDGET__。
                if os.environ.get("CTSS_INLINE_WIDGET") == "1":
                    titles = [f.get("type") or "图 %d" % (j + 1) for j, f in enumerate(svg_figs)]
                    html = build_figure_widget(svg_figs, titles)
                    print("__SVG_WIDGET__ " + html)
                # SVG 源文件供下载（用户在对话流仅看到报告入口，文件在此持久化）
                if _svg_paths:
                    print("# SVG 图形已落盘（全量展示见 HTML 报告）: %s" % ", ".join(_svg_paths))
        except Exception as e:  # noqa: BLE001 - 渲染失败不阻断主流程
            print("# __SVG_WIDGET__ 生成失败: %s" % e)

    # ── 渲染计时与超阈值提示（ct-base §19.10）──
    _elapsed = round(time.time() - _t0, 3)
    _hint = None
    if mode == "svg_inline":
        reasons = []
        if _elapsed > RENDER_SVG_THRESHOLD:
            reasons.append("本地渲染处理耗时 %.0fs（> %.0fs 阈值）" % (_elapsed, RENDER_SVG_THRESHOLD))
        if _svg_kb > RENDER_SVG_KB_THRESHOLD:
            reasons.append("SVG 体量 %.0fKB（> %.0fKB，界面渲染/滚动可能明显变慢）" % (_svg_kb, RENDER_SVG_KB_THRESHOLD))
        if reasons:
            _hint = "；".join(reasons) + "。可切换图片文件模式（figure_mode='png_file' / 环境变量 CTSS_FIGURE_MODE=png_file）：本地 cairosvg 转 PNG，界面渲染更快、不占上下文（但变位图）。"
            print("__RENDER_HINT__ " + _hint)
    # 诊断信息（不参与提示，仅供排查）
    print("# render_elapsed_seconds=%.3f render_svg_kb=%.1f figure_mode=%s" % (_elapsed, _svg_kb, mode))


def _curve_svg_from_stats(stats: dict, test: str, target_power: float = None,
                          ref_n: float = None) -> str:
    """coze 端无图时（svglite/cairo 缺失），用曲线数值 stats{x,y,series} 纯 Python 生成 SVG。

    对齐 ct-base §19 内联渲染：700x500、网格线、多系列折线 + 图例、动态轴标签。
    仅标准库，无第三方依赖。
    ★ Power 参考线（2026-08-20）：当 y 轴语义为 Power 且传入 target_power 时，绘制
    红色虚线参考线（与 coze 权威版 svglite 一致），坐标用与数据点相同的 sy() 映射——
    保证参考线、刻度、数据点三者在同一坐标系统内，杜绝错位。
    """
    xs = stats.get("x") or []
    ys = stats.get("y") or []
    series = stats.get("series") or ["curve"]
    if not xs or not ys or len(xs) != len(ys):
        return ""
    xs = [float(v) for v in xs]
    ys = [float(v) for v in ys]
    # ★ 2026-08-30 用户定稿：样本量-把握度曲线统一为 X=样本量 N、Y=把握度 Power（习惯方向）。
    #   若 coze 端返回的是转置数据（x=power∈[0,1]、y=n>1），此处交换回标准方向。
    x_is_power = all(0.0 <= v <= 1.0 for v in xs) and max(ys) > 1.0
    if x_is_power:
        xs, ys = ys, xs
    xlab, ylab = "N", "Power"
    W, H, PAD_L, PAD_R, PAD_T, PAD_B = 700, 500, 70, 30, 30, 55
    PW, PH = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    if xmax == xmin:
        xmax = xmin + 1
    if ymax == ymin:
        ymax = ymin + 1
    ymin, ymax = ymin - (ymax - ymin) * 0.05, ymax + (ymax - ymin) * 0.05

    # ★ 参考线（2026-08-30 用户定稿；X=N、Y=Power 标准方向下）：
    #   正向求解（求 n）→ 在「给定 power」处画【水平线】Y=power，交点 X 即所需样本量；
    #   反向求解（求 power）→ 在「给定样本量」处画【竖线】X=n，交点 Y 即对应效能。
    #   与 run_task.R 对齐（forward: abline(h=power) / reverse: abline(v=nobs)）。
    #   forward 由 target_power 标识（传了 target_power 即求 n），reverse 由 ref_n 标识（求 power）。
    ref_power_val = None
    if target_power is not None and ref_n is None:
        rp = float(target_power)
        if ymin - 1e-9 <= rp <= ymax + 1e-9:
            ref_power_val = rp
    ref_n_val = None
    if ref_n is not None:
        rn = float(ref_n)
        if xmin - 1e-9 <= rn <= xmax + 1e-9:
            ref_n_val = rn

    def sx(v):
        return PAD_L + (v - xmin) / (xmax - xmin) * PW

    def sy(v):
        return PAD_T + (ymax - v) / (ymax - ymin) * PH

    colors = ["#c0392b", "#2980b9", "#27ae60", "#8e44ad", "#d35400", "#16a085"]
    # 系列分组（series 与点一一对应；若 series 为标量则整条单系列）
    groups = {}
    for i in range(len(xs)):
        s = str(series[i] if isinstance(series, list) and i < len(series) else (series if not isinstance(series, list) else "curve"))
        groups.setdefault(s, []).append(i)
    paths = []
    legend = []
    for j, (name, idxs) in enumerate(groups.items()):
        col = colors[j % len(colors)]
        pts = " ".join("%.1f,%.1f" % (sx(xs[i]), sy(ys[i])) for i in idxs)
        paths.append(
            '<polyline points="%s" fill="none" stroke="%s" stroke-width="2" '
            'stroke-linejoin="round" stroke-linecap="round"/>' % (pts, col))
        cx, cy = sx(xs[idxs[-1]]), sy(ys[idxs[-1]])
        legend.append(
            '<rect x="%.1f" y="%.1f" width="14" height="4" fill="%s"/>'
            '<text x="%.1f" y="%.1f" font-size="11" fill="#333">%s</text>'
            % (cx + 8, cy - 2, col, cx + 26, cy + 3, name))
    grid = []
    for g in range(5):
        gy = PAD_T + PH * g / 4
        grid.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#e0e0e0" stroke-width="1"/>'
                    % (PAD_L, gy, W - PAD_R, gy))
        grid.append('<text x="%d" y="%.1f" font-size="10" fill="#888" text-anchor="end">%.2f</text>'
                    % (PAD_L - 6, gy + 3, ymax - (ymax - ymin) * g / 4))
        gx = PAD_L + PW * g / 4
        grid.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#e0e0e0" stroke-width="1"/>'
                    % (gx, PAD_T, gx, H - PAD_B))
        grid.append('<text x="%.1f" y="%d" font-size="10" fill="#888" text-anchor="middle">%.2f</text>'
                    % (gx, H - PAD_B + 14, xmin + (xmax - xmin) * g / 4))
    ref = ""
    # 样本量竖直参考线（reverse 求 power）：x 轴为样本量时，在给定 n 处画蓝色虚线，
    # 直接读出该 n 对应的效能（与 run_task.R abline(v = nobs) 对齐）。
    refn = ""
    if ref_n_val is not None:
        rx = sx(ref_n_val)
        refn = (
            '<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#2980b9" '
            'stroke-width="1.2" stroke-dasharray="6,4"/>' % (rx, PAD_T, rx, H - PAD_B)
            + '<text x="%.1f" y="%d" font-size="10" fill="#2980b9" text-anchor="middle" '
              'font-weight="bold">n = %s</text>' % (rx, PAD_T - 4, format(ref_n_val, "g"))
        )
    # 目标把握度水平参考线（forward 求 n，X=N、Y=Power 标准方向）：在「给定 power」处画红色
    # 水平虚线 Y=power，交点 X 即达到该效能所需样本量（与 run_task.R abline(h = power) 对齐）。
    refp = ""
    if ref_power_val is not None:
        ry = sy(ref_power_val)
        refp = (
            '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#c0392b" '
            'stroke-width="1.2" stroke-dasharray="6,4"/>' % (PAD_L, ry, W - PAD_R, ry)
            + '<text x="%d" y="%.1f" font-size="10" fill="#c0392b" text-anchor="end" '
              'font-weight="bold">power = %s</text>' % (PAD_L - 6, ry - 4, format(ref_power_val, "g"))
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d">' % (W, H, W, H)
        + '<rect width="100%%" height="100%%" fill="#ffffff"/>'
        + "".join(grid)
        + ref
        + refp
        + refn
        + '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#999" stroke-width="1"/>'
          % (PAD_L, H - PAD_B, W - PAD_R, H - PAD_B)
        + '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#999" stroke-width="1"/>'
          % (PAD_L, PAD_T, PAD_L, H - PAD_B)
        + "".join(paths)
        + "".join(legend)
        + '<text x="%d" y="%d" font-size="13" fill="#333" font-weight="bold">Curve: %s</text>'
          % (PAD_L, PAD_T - 8, test)
        + '<text x="%d" y="%d" font-size="12" fill="#555" text-anchor="middle">%s</text>'
          % (PAD_L + PW / 2, H - 12, xlab)
        + '<text x="18" y="%d" font-size="12" fill="#555" text-anchor="middle" '
          'transform="rotate(-90 18 %d)">%s</text>'
          % (PAD_T + PH / 2, PAD_T + PH / 2, ylab)
        + "</svg>"
    )
    return svg


def render_curve_fallback(meta: dict, test: str, target_power: float = None,
                          ref_n: float = None):
    """coze 端无图但返回曲线数值时，本地生成 SVG 并输出内联标记（ct-base §19）。

    target_power：Power 参考线目标值（默认 None 不画；reverse 场景传 0.8 或用户 --power）。
    ref_n：样本量竖直参考线位置（reverse 求 power 场景传用户输入的 --nobs；None 不画）。
    """
    stats = (meta or {}).get("stats") if isinstance(meta, dict) else None
    if not isinstance(stats, dict):
        stats = meta if isinstance(meta, dict) and ("x" in meta or "series" in meta) else None
    if not stats:
        return
    xs = stats.get("x")
    ys = stats.get("y")
    if not xs or not ys:
        return
    svg = _curve_svg_from_stats(stats, test, target_power=target_power, ref_n=ref_n)
    if not svg:
        return
    outdir = _outputs_dir()
    path = os.path.join(outdir, "ctss_%s_curve.svg" % test)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    # 2026-08-28 设计修订（用户定）：对话流不内联图形，仅 HTML 报告全量展示。
    if os.environ.get("CTSS_INLINE_WIDGET") == "1":
        print('__FIGURE__ svg %s caption="Curve %s"' % (path, test))
    try:
        _skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        _adapters_dir = os.path.join(_skill_root, "adapters")
        for _p in (_skill_root, _adapters_dir):
            if _p not in sys.path:
                sys.path.insert(0, _p)
        from rendering import build_figure_widget  # type: ignore  # adapters/rendering.py
        html = build_figure_widget([{"svg": svg, "type": "Curve %s" % test}],
                                   ["Curve %s" % test])
        if os.environ.get("CTSS_INLINE_WIDGET") == "1":
            print("__SVG_WIDGET__ " + html)
        # 2026-08-28 设计修订：图形展示走 HTML 报告（render_html_report 全量），
        # 此处仅提示落盘 SVG 源文件供下载。
        print("# 图形 SVG 已落盘（全量展示见 HTML 报告）: %s" % path)
    except Exception as e:  # noqa: BLE001
        print("# __SVG_WIDGET__ 生成失败: %s" % e)


def build_parser():
    p = argparse.ArgumentParser(description="Clinical Trial Sample Size Calculator v4.0.1")
    p.add_argument("--test", required=False, default=None,
        choices=["ttest_ind","ttest_paired","ttest_one","anova","proportion_one","proportion_two",
                 "proportion_paired","odds_ratio","risk_ratio",
                 "non_inferiority","survival","mixed_model","roc","poisson",
                 "bland_altman","equivalence","be_tost","cluster",
                 "vaccine_efficacy","multiple_endpoints","bayesian","dose_escalation",
                 "win_ratio","must_win","historical_controls","mams",
                 "conditional_power","ni_survival","superiority_margin","assurance",
                 "dunnett","mediation","group_sequential","gsd_proportion","gsd_survival","gsd_hazard","gsd_poisson","gsd_survival_sim","gsd_hazard_sim","adaptive","survival_exact",
                 "survival_equivalence","survival_superiority","cox_covariate",
                 "survival_one_sample","competing_risks","recurrent_events",
                 "survival_historical",
                 "adaptive_simulate",
                 "correlation","variance_one","variance_two","cv_one",
                 "ci_mean","ci_prop","ci_or","ci_rr","ci_cor","ci_icc",
                 "regression_linear","meta_planning",
                 "regression_logistic","regression_poisson","cluster_ext","rates_ext",
                 # 非参数（NP1/NP2, v5.13.39）：Wilcoxon 秩和 / 符号秩（Noether 1987）
                 "wilcoxon","wilcoxon_signed_rank"])
    p.add_argument("--nl", default=None,
                   help="自然语言需求（零 LLM 本地确定性解析：自动识别 --test 并提取参数）。"
                        "例：'非劣效生存试验，NI界值1.25，期望HR=1.0，入组12月随访12月'。"
                        "本地仅做快速预路由；置信度低或参数不全时打印结构化提示，由本地 agent 向用户追问缺失 test/参数（≤2 轮→默认，ct-base §6.1），原始 NL 不入 coze。")
    p.add_argument("--language", dest="language", choices=["zh", "en"], default=None,
                   help="显式覆盖 coze 计算端报告/图表语言（备用提示）。不传时按 --nl 文本内容自动判定"
                        "（中文系统+英文输入→en，不被系统 locale 误判），再回退系统语言。等价于环境变量 CTSS_LOCALE。")
    p.add_argument("--yes", "-y", action="store_true",
                   help="显式确认执行 R 代码（默认 dry-run 安全预览，仅展示代码、不执行）")
    p.add_argument("--dry-run", action="store_true",
                   help="安全预览：仅生成并展示 R 代码、不执行（默认即此模式）")
    p.add_argument("--show-code", action="store_true", default=False,
                   help="执行并展示生成的 R 代码（默认不展示，仅按需提供）")
    # ── Common ──
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--power", type=float, default=0.8, help="目标检验效能 (与 --nobs 互斥)")
    p.add_argument("--nobs", type=int, default=None, help="给定样本量求效能 (与 --power 互斥)")
    p.add_argument("--show-assumptions", action="store_true", default=False,
                   help="打印本次计算的假设清单（显式输入 / 静默默认值 / 合理区间 / 解读风险 / 公开证据参考）后退出，不做求解")
    # ── 公开证据效应量参考（路线 A，2026-10-14）──
    p.add_argument("--effect-ref", dest="effect_ref", default=None,
                   help="公开证据效应量参考 JSON（来自公开已发表荟萃，schema 见 effect_size_benchmarks/）。"
                        "仅展示于假设清单；默认绝不代入。")
    p.add_argument("--adopt-ref", dest="adopt_ref", default=None,
                   help="显式采纳参考值代入计算：median|conservative|low|high|<来源序号>。"
                        "须与 --effect-ref 同用；采纳来源会打印并计入假设清单（可审计）。")
    p.add_argument("--ta", default=None, help="适应症（信息性，随假设清单输出）")
    p.add_argument("--endpoint", default=None, help="终点（信息性，随假设清单输出）")
    # upgrade I (2026-09-29): 规划层假设质量审计（四分级 + 设计逻辑族 + fallback）
    p.add_argument("--audit", action="store_true", default=False,
                   help="假设质量审计（规划层）：known/weak/unknown/missing 四分级 + "
                        "设计逻辑族自洽核查 + fallback 场景规划，打印后退出，不做求解。"
                        "与 --show-assumptions（计算层参数清单）互补。")
    p.add_argument("--evidence-source", default="",
                   help="--audit 用：已附历史证据来源的参数名清单（逗号分隔，如 "
                        "effect,sd），命中者假设升为 known。")
    p.add_argument("--batch-file", default=None,
                   help="批量计算：JSON 文件路径（数组）。每个元素 "
                        '{"test": 终点类型, "args": {覆盖字段}, "ctx": {覆盖字段}}；'
                        "逐项继承命令行默认参数并覆盖指定字段。对应 coze v5.7 batch 模式，"
                        "一次请求完成网格/敏感性扫描，本地逐项渲染并合并输出。")
    # ── t-test / ANOVA ──
    p.add_argument("--effect", type=float)
    p.add_argument("--k_groups", type=int, default=2)
    p.add_argument("--side", choices=["one", "two"], default="two",
                   help="检验方向: one=单侧, two=双侧(默认)")
    p.add_argument("--sd", type=float, default=None,
                   help="标准差。提供时 --effect 视为原始均差(Δ), 自动折算 Cohen's d = effect/sd; 否则 --effect 直接作为 d")
    # upgrade J1 (2026-09-29): MCID 语义入口——原始单位的最小重要差值，折算 d=MCID/sd
    p.add_argument("--mcid", type=float, default=None,
                   help="最小重要差值 MCID（原始单位，需配合 --sd；等效于 --effect 传原始差值）。"
                        "建议同时用 --mcid-source 声明依据（anchor/distribution/expert+出处），"
                        "满足 CONSORT-SPIRIT Item14 / CDE 样本量指导原则『目标差值依据』要求。")
    p.add_argument("--mcid-source", default=None,
                   help="MCID 依据声明（如 'anchor: PASS 2015 cut-point' / 'distribution: 0.5*SD "
                        "(norman2003)' / 'expert: Delphi 共识 XX'）。输出与假设审计将引用该来源。")
    p.add_argument("--justify", action="store_true", default=False,
                   help="计算完成后追加输出 IRB/SAP-ready 论证段落（中英双语，J2，"
                        "结构对齐 CONSORT-SPIRIT Item14 + CDE《样本量估计指导原则(试行)》）。"
                        "规划层独立预览可配 --test 直接运行 scripts/justify_text.py。")
    p.add_argument("--ratio", type=float, default=None,
                   help="两组不等例分配比 n2/n1（仅 ttest_ind 用；缺省=1 等例）。提供时 --nobs 视为第一组 n1，n2=nobs*ratio")
    # ── Proportion ──
    p.add_argument("--p1", type=float, default=0.7,
                   help="gsd_proportion 治疗组比例 (difference 模式必填, 默认 0.7)")
    p.add_argument("--p2", type=float, default=0.5,
                   help="gsd_proportion 对照组比例 (difference 模式必填, 默认 0.5)")
    # ── 非参数 Wilcoxon（NP1/NP2, v5.13.39）──
    # 效应输入两路径：superiority 直给优先；否则 median_diff + sd（+ shape）按位移分布折算。
    # 偏态结局（生存时间、不良事件计数、中位数与均数差异显著）不满足正态近似时使用。
    # 命名说明：不叫 --phi 是为避开 regression_poisson/rates_ext 的过离散参数 φ。
    p.add_argument("--superiority", type=float, default=None,
                   help="随机优势 φ（治疗组受试者结局优于对照组受试者的概率，0.5=无差异，"
                        "典型 0.6 小 / 0.65 中 / 0.7 中大≈d=0.5）。直给时优先于 median_diff 路径")
    p.add_argument("--median_diff", type=float, default=None,
                   help="组间（或配对差）中位数差 Δ。需配合 --sd 折算 φ："
                        "normal → φ=Φ(Δ/(σ√2))（两样本）/ Φ(Δ/σ)（配对）；"
                        "logistic → φ=plogis(Δ/(s·k))，s=σ√3/π。仅给 Δ 不给 sd 将报错（不静默默认）")
    p.add_argument("--shape", choices=["normal", "logistic"], default="normal",
                   help="median_diff 折算 φ 时的位移分布形状假设：normal（默认）或 logistic。"
                        "logistic 厚尾、同等 Δ 下所需样本量更小")
    # ── Non-inferiority / Equivalence ──
    p.add_argument("--margin", type=float)
    # ── Survival ──
    p.add_argument("--hazard_ratio", "--hr", type=float)
    # ── Mixed model ──
    p.add_argument("--effect_name", type=str)
    p.add_argument("--varcorr", type=float, default=0.5)
    p.add_argument("--sigma", type=float, default=1.0)
    p.add_argument("--nsim", type=int, default=500)
    # ── ROC ──
    p.add_argument("--auc0", type=float, default=0.5)
    p.add_argument("--auc1", type=float)
    # ── Poisson ──
    p.add_argument("--lambda1", type=float)
    p.add_argument("--lambda2", type=float)
    p.add_argument("--t1", type=float, default=1.0)
    p.add_argument("--t2", type=float, default=1.0)
    # ── Cluster ──
    p.add_argument("--icc", type=float)
    p.add_argument("--m", type=float)
    p.add_argument("--n_indiv", type=float)
    # ── Bland-Altman ──
    p.add_argument("--sd_diff", type=float)
    p.add_argument("--w", type=float)
    # ── Bioequivalence ──
    p.add_argument("--theta0", type=float, default=0.95)
    p.add_argument("--theta1", type=float, default=None,
                   help="BE 等效下界（默认 0.8；与 --theta2 同给；或单给 --margin 自动 1/margin）")
    p.add_argument("--theta2", type=float, default=None,
                   help="BE 等效上界（默认 1.25；与 --theta1 同给；或单给 --margin 自动 margin）")
    p.add_argument("--cv", type=float, default=0.25)
    p.add_argument("--design", type=str, default="2x2")
    # ── Vaccine, Bayesian, multiple endpoints, dose escalation ──
    p.add_argument("--ve_control", type=float, default=0.02)
    p.add_argument("--ve_treatment", type=float, default=0.005)
    p.add_argument("--prior_a0", type=float, default=0.5)
    p.add_argument("--prob_control", type=float, default=0.3)
    p.add_argument("--prob_treatment", type=float, default=0.15)
    p.add_argument("--correlation", type=float, default=0.5)
    p.add_argument("--n_doses", type=int, default=5)
    p.add_argument("--target_dlt", type=float, default=0.33)
    # ── Tier 1 新增（2026-10-12）：CI 精度 / 方差 / 回归 / Meta 规划 ──
    p.add_argument("--half_width", type=float, default=None,
                   help="置信区间半宽（ci_mean/ci_prop/ci_or/ci_rr/ci_cor/ci_icc：给定→求 n；配 --nobs→求达成半宽）")
    p.add_argument("--rel_error", type=float, default=None,
                   help="相对误差（cv_one：CV 估计 CI 的相对半宽目标）")
    p.add_argument("--p0", type=float, default=None,
                   help="基线比例（ci_or/ci_rr 对照组事件率；meta_planning or/rr 用）")
    p.add_argument("--f2", type=float, default=None,
                   help="Cohen's f²（regression_linear：R²/(1-R²)）")
    p.add_argument("--u_pred", type=int, default=None,
                   help="预测变量数 u（regression_linear）")
    p.add_argument("--effect_type", type=str, default=None,
                   choices=["smd","paired","or","rr","cor","cluster"],
                   help="Meta 效应类型（meta_planning）")
    p.add_argument("--n_per_study", type=float, default=None,
                   help="每研究样本量（meta_planning，用于算研究内方差 vw）")
    p.add_argument("--i2", type=float, default=None,
                   help="异质性 I²（meta_planning；与 R=I²/(1-I²) 互为双参数）")
    p.add_argument("--R", dest="R", type=float, default=None,
                   help="异质性比 R=组间/组内（meta_planning；直输优先于 I² 映射，R=0 即固定效应）")
    p.add_argument("--effect0", type=float, default=None,
                   help="H0 效应量（meta_planning：效应量原尺度；缺省 or/rr=1、其余=0）")
    p.add_argument("--cluster_cv", type=float, default=None,
                   help="簇大小变异系数 COV（meta_planning cluster：DE=1+((COV²+1)M-1)ρ；缺省 0=等簇大小）")
    p.add_argument("--k_studies", type=int, default=None,
                   help="研究数 K（meta_planning：给定→求效能；缺省→求所需 K）")
    # ── 可变每研究样本量（2026-10-21 前端打通）：n_cv 走契约 optional 通道 ──
    p.add_argument("--n_cv", type=float, default=None,
                   help="研究间样本量变异系数 CV（meta_planning：>0 启用保守档 V_eff=V·(1+CV²)；再配 --n_sim 启用 MC 精确档输出功效带）")

    # ── Tier 2 新增（2026-10-12）：回归 / 整群扩展 / 率扩展 ──
    p.add_argument("--x_type", type=str, default=None,
                   choices=["continuous", "binary"],
                   help="逻辑回归协变量类型（regression_logistic：continuous 连续 / binary 二分类）")
    p.add_argument("--q", type=float, default=None,
                   help="P(X=1)（regression_logistic 二分类协变量患病比例）")
    p.add_argument("--r2", type=float, default=None,
                   help="协变量与其它变量的复相关平方 R²（regression_logistic / regression_poisson）")
    p.add_argument("--mu_x", type=float, default=None,
                   help="协变量均值 μ_X（regression_poisson 正态 X）")
    p.add_argument("--phi", type=float, default=None,
                   help="过离散参数 φ（regression_poisson / rates_ext；>1 为负二项型过离散）")
    p.add_argument("--cv_cluster", type=float, default=None,
                   help="簇大小变异系数 CV（cluster_ext 不等群设计效应）")
    p.add_argument("--rate_mode", type=str, default=None,
                   choices=["ratio", "single_ci", "ratio_ci"],
                   help="率模式（rates_ext：ratio 率比检验 / single_ci 单率 CI / ratio_ci 率比 CI）")

    # ═══ NEW v3.3 arguments ═══
    # Win-Ratio
    p.add_argument("--win_ratio_theta", type=float, default=1.5)
    p.add_argument("--n_sim_initial", type=int, default=100)
    p.add_argument("--se_approx", type=float, default=0.0625)
    p.add_argument("--n_sim", type=int, default=None,
                   help="MC 模拟次数（meta_planning：配 --n_cv 启用 MC 精确档 ss_meta_planning_mc，建议 ≥2000；缺省 None=不启用 MC）")
    # Must-Win / Co-Primary
    p.add_argument("--n_endpoints_must", type=int, default=2)
    p.add_argument("--effect_must", type=float, default=0.3)
    p.add_argument("--correlation_must", type=float, default=0.5)
    # Historical Controls
    p.add_argument("--p_control_current", type=float, default=0.3)
    p.add_argument("--historical_response", type=int, default=15)
    p.add_argument("--historical_n", type=int, default=100)
    p.add_argument("--a0_borrowing", type=float, default=0.5)
    # MAMS
    p.add_argument("--n_arms_mams", type=int, default=3)
    p.add_argument("--n_stages_mams", type=int, default=2)
    p.add_argument("--delta_effect", type=float, default=0.3)
    # Conditional Power / SSR
    p.add_argument("--timing", type=float, default=0.5)
    p.add_argument("--observed_effect", type=float, default=0.2)
    p.add_argument("--planned_effect", type=float, default=0.3)
    p.add_argument("--n_completed", type=int, default=100)
    p.add_argument("--n_planned", type=int, default=200)
    # NI Survival
    p.add_argument("--ni_margin_surv", type=float, default=1.25)
    p.add_argument("--hr_expected", type=float, default=1.0)
    p.add_argument("--accrual_time", type=float, default=12)
    p.add_argument("--followup_time", type=float, default=12)
    p.add_argument("--dropout_rate", type=float, default=0.05)
    p.add_argument("--event_rate", type=float, default=0)
    # Superiority Margin
    p.add_argument("--sup_margin", type=float, default=0.05)
    p.add_argument("--sigma_ratio", type=float, default=1.0)
    p.add_argument("--p_control_sup", type=float, default=0.3)
    p.add_argument("--delta_sup", type=float, default=0.15)
    # Assurance
    p.add_argument("--n_sim_assurance", type=int, default=5000)
    # 2026-08-20 统一为先验 Beta(2,2)：默认 None 不发送，R 端 %||% 2 生效（原 CLI 3/7 覆盖了 R 端默认）
    p.add_argument("--shape1_trt", type=float, default=None)
    p.add_argument("--shape2_trt", type=float, default=None)
    p.add_argument("--shape1_ctrl", type=float, default=None)
    p.add_argument("--shape2_ctrl", type=float, default=None)
    p.add_argument("--n_assurance", type=int, default=100)
    # 2026-08-20 修复：默认 0.0 会被 build_params 发送并覆盖 R 端 %||% 0.05 → margin=0 计算错误；
    # 改为 None 不发送，R 端回落 0.05（另有 <=0 防御）
    p.add_argument("--margin_assurance", type=float, default=None)
    # Dunnett
    p.add_argument("--n_groups_dunnett", type=int, default=3)
    p.add_argument("--n_control_dunnett", type=int, default=50)
    p.add_argument("--effect_dunnett", type=float, default=0.4)
    # Mediation
    p.add_argument("--a_path", type=float, default=0.3)
    p.add_argument("--b_path", type=float, default=0.3)
    p.add_argument("--sigma2_m", type=float, default=1.0)
    p.add_argument("--sigma2_y", type=float, default=1.0)
    p.add_argument("--cprime", type=float, default=0.0)
    p.add_argument("--n_sim_mediation", type=int, default=1000)
    # Group Sequential
    p.add_argument("--n_interim", type=int, default=1,
                   help="中期分析次数 (k-1)；总分析次数 kMax = n_interim + 1")
    p.add_argument("--effect_gs", type=float, default=0.4,
                   help="group_sequential 的标准化效应量 (Cohen's d)")
    p.add_argument("--spending_func", type=str, default="OF",
                   choices=["OF", "Pocock", "WT", "HSD", "KimDeMets"],
                   help="alpha 消耗函数: OF=O'Brien-Fleming, Pocock, WT=Wang-Tsiatis, "
                        "HSD=Hwang-Shih-DeCani(gamma, 经 --rho), KimDeMets(asOF)")
    # Adaptive
    p.add_argument("--n_stages_adapt", type=int, default=2)
    p.add_argument("--effect_adaptive", type=float, default=0.4)
    p.add_argument("--adaptive_type", type=str, default="SSR")
    # Survival Exact
    p.add_argument("--alpha_exact", type=float, default=0.05)
    p.add_argument("--power_exact", type=float, default=0.8)
    p.add_argument("--hr_exact", type=float, default=0.75)
    p.add_argument("--accrual_exact", type=float, default=12)
    p.add_argument("--followup_exact", type=float, default=12)
    p.add_argument("--dropout_exact", type=float, default=0.05)
    p.add_argument("--event_rate_exact", type=float, default=0.3)
    p.add_argument("--n_stages_exact", type=int, default=1)
    # ═══ NEW v3.5: PASS-survival extensions (7) ═══
    # Survival Equivalence (TOST on HR)
    p.add_argument("--eq_margin_surv", type=float, default=1.25)
    # Survival Superiority by a margin (HR)
    p.add_argument("--sup_margin_surv", type=float, default=0.8)
    p.add_argument("--sup_hr", type=float, default=0.67)
    # Cox covariate power (Vittinghoff)
    p.add_argument("--cox_hr", type=float, default=2.0)
    p.add_argument("--cox_r2", type=float, default=0.3)
    p.add_argument("--cox_prev", type=float, default=0.5)
    p.add_argument("--cox_event_prop", type=float, default=0.3)
    # One-sample exponential
    p.add_argument("--median0", type=float, default=12.0)
    p.add_argument("--median1", type=float, default=18.0)
    # Competing risks (cumulative incidence)
    p.add_argument("--ci_control", type=float, default=0.2)
    p.add_argument("--ci_treatment", type=float, default=0.1)
    # Recurrent events (Andersen-Gill)
    p.add_argument("--rate_control", type=float, default=1.0)
    p.add_argument("--rate_ratio", type=float, default=0.6)
    p.add_argument("--recur_followup", type=float, default=2.0)
    # Historical control log-rank
    p.add_argument("--new_median", type=float, default=18.0)
    p.add_argument("--hist_n", type=float, default=100.0)
    # ═══ NEW v3.6: PASS Group-Sequential extensions (rpact-backed) ═══
    # Two proportions (difference / ratio / odds-ratio)
    p.add_argument("--gs_proportion_metric", type=str, default="difference",
                   choices=["difference", "ratio", "or"],
                   help="gsd_proportion 的效应度量: difference(默认)/ratio/or")
    p.add_argument("--gs_ratio", type=float, default=0.8,
                   help="gsd_proportion ratio 模式: 治疗组比例 = 对照组 × ratio")
    p.add_argument("--gs_or", type=float, default=0.5,
                   help="gsd_proportion OR 模式: 治疗组比值比")
    # Two survival / hazard-rate (control median -> lambda2)
    p.add_argument("--gs_median_control", type=float, default=12.0,
                   help="gsd_survival/gsd_hazard 对照中位生存(月), 推导 lambda2")
    # Two Poisson rates
    p.add_argument("--gs_rate1", type=float, default=0.6,
                   help="gsd_poisson 治疗组发生率 (lambda1, /人年)")
    p.add_argument("--gs_rate2", type=float, default=1.0,
                   help="gsd_poisson 对照组发生率 (lambda2, /人年)")
    p.add_argument("--gs_poisson_time", type=float, default=2.0,
                   help="gsd_poisson 每人随访时间(年)")
    # ── Adaptive Monte-Carlo simulator (test=adaptive_simulate) ──
    # 纯 Python 蒙特卡洛自适应/成组序贯仿真器 (无 R, 无 shell, 直接运行)
    p.add_argument("--sim_design", type=str, default="group_sequential",
                   choices=["group_sequential", "adaptive_reestimate", "drop_the_loser"],
                   help="仿真设计类型 / simulation design")
    p.add_argument("--n_simulations", type=int, default=10000,
                   help="蒙特卡洛重复次数 / Monte-Carlo replications")
    p.add_argument("--sim_n", type=int, default=100,
                   help="每组样本量 (仿真用) / per-arm sample size for simulation")
    p.add_argument("--effect_size", type=float, default=0.3,
                   help="Cohen's d (仿真效应量)")
    p.add_argument("--effect_sizes", type=str, default=None,
                   help="drop_the_loser 各臂 d 逗号列表, 如 '0.2,0.35,0.5'")
    p.add_argument("--interim_looks", type=int, default=2,
                   help="分析次数 (含最终) / number of looks incl. final")
    p.add_argument("--spending_function", type=str, default="obrien_fleming",
                   choices=["obrien_fleming", "pocock", "power_family"],
                   help="alpha 消耗函数 / alpha spending function")
    p.add_argument("--rho", type=float, default=3.0,
                   help="HSD / Kim-DeMets 消耗函数的 gammaA (Hwang-Shih-DeCani γ, 默认 3.0)")
    p.add_argument("--wt_delta", type=float, default=0.25,
                   help="Wang-Tsiatis 参数 Δ (仅 --spending_func WT 生效, 默认 0.25)")
    p.add_argument("--futility", action="store_true", help="加入非绑定 futility 边界")
    p.add_argument("--beta", type=float, default=0.2, help="futility beta-spending")
    p.add_argument("--reestimate_method", type=str, default="promising_zone",
                   choices=["promising_zone"], help="样本量再估计方法")
    p.add_argument("--interim_fraction", type=float, default=0.5,
                   help="SSR/选臂 interim 信息比例")
    p.add_argument("--target_cp", type=float, default=0.9, help="SSR 目标条件功效")
    p.add_argument("--max_inflation", type=float, default=2.0, help="SSR 二阶段样本量上限倍数")
    p.add_argument("--n_arms", type=int, default=3, help="drop_the_loser 处理臂数")
    p.add_argument("--selection_fraction", type=float, default=0.5, help="选臂 interim 比例")
    p.add_argument("--correction", type=str, default="dunnett",
                   choices=["dunnett", "bonferroni"], help="多臂多重性校正")
    p.add_argument("--optimize", action="store_true",
                   help="网格搜索达到 --power 的最小每组样本量")
    p.add_argument("--n_min", type=int, default=10, help="--optimize 样本量下界")
    p.add_argument("--n_max", type=int, default=1000, help="--optimize 样本量上界")
    p.add_argument("--visualize", action="store_true", help="生成仿真结果 PNG")
    p.add_argument("--sim_output", type=str, default=None, help="仿真结果 JSON 输出路径")
    p.add_argument("--sim_seed", type=int, default=None, help="随机种子")
    # ── Curve mode (power / sample-size curves) ──
    p.add_argument("--n_seq", type=str, default=None,
                   help="样本量序列: 显式 '20,40,200' 或自动 '20:20:200'(起:步:止) → 绘制 power 曲线")
    p.add_argument("--power_seq", type=str, default=None,
                   help="效能序列: 显式 '0.6,0.7,0.95' 或自动 '0.6:0.05:0.95' → 绘制样本量曲线")
    p.add_argument("--plot_effects", type=str, default=None,
                   help="多效应量叠加(可选): '0.3,0.5,0.8' 画多条曲线做敏感性分析")
    p.add_argument("--effect_seq", type=str, default=None,
                   help="效应量连续序列: 显式 '0.1,0.2,0.9' 或自动 '0.1:0.05:0.9'(起:步:止) → "
                        "绘制效应量轴曲线(x=效应量; 配 --n_seq 时 y=效能, 配 --power_seq 时 y=所需样本量)")
    p.add_argument("--dist_plot", action="store_true", default=False,
                   help="① H0/H1 分布重叠图：标准化效应空间画两条正态密度并着色 α/β 区"
                        "(支持 ttest*/proportion*/survival)")
    p.add_argument("--power_time_seq", type=str, default=None,
                   help="③ 生存随访-效能曲线(仅 survival)：随访时长序列(单位与 event_rate 一致，如年 '1:0.5:4')"
                        "→ x=时长 y=效能；需配合 --event_rate / --accrual_time")
    p.add_argument("--heatmap", action="store_true", default=False,
                   help="④ 效能热力图：需 --n_seq(样本量) + --effect_seq(效应量) 两序列，"
                        "绘制效能填充热力图(支持 9 个曲线 test)")
    p.add_argument("--out", type=str, default=None,
                   help="曲线 PNG 输出路径 (默认系统临时目录)")

    # ── P1-C: 本地模拟验证闭环（verify.py 桥接，默认关闭）──
    # 把解析解（来自 pwr/coze 的 n 及组序贯边界）回代 Monte-Carlo，独立验证其
    # 真实 power / TIE。默认不触发；--verify 显式开启。模块纯本地、零联网。
    pv = p.add_argument_group("P1-C verification (本地模拟验证闭环)")
    pv.add_argument("--verify", action="store_true",
                    help="P1-C: 开启本地 Monte-Carlo 验证闭环（对 --verify-design 指定的设计，"
                         "用 --verify-n 回代模拟，校验 power ±2pp / TIE ±0.5pp）")
    pv.add_argument("--verify-design", default=None,
                    choices=["ttest_ind", "ttest_one", "ttest_paired",
                             "proportion_two", "survival", "group_sequential",
                             "adaptive_reestimate"],
                    help="P1-C 验证对象设计类型（默认按所计算的检验自动映射；"
                         "此处仅用于显式覆盖）")
    pv.add_argument("--verify-n", type=int, default=None,
                    help="P1-C 回代的样本量 n（解析解给出的 n；必填，否则验证无意义）")
    pv.add_argument("--verify-power", type=float, default=0.8,
                    help="P1-C 名义功效目标（待验证）")
    pv.add_argument("--verify-nsim", type=int, default=20000,
                    help="P1-C Monte-Carlo 重复次数（上限 500000）")
    pv.add_argument("--verify-side", choices=["one", "two"], default="two")
    pv.add_argument("--verify-effect-size", type=float, default=None,
                    help="P1-C 连续端点 Cohen's d（ttest_*/group_sequential/adaptive）")
    pv.add_argument("--verify-p1", type=float, default=None, help="P1-C 治疗组比例")
    pv.add_argument("--verify-p2", type=float, default=None, help="P1-C 对照组比例")
    pv.add_argument("--verify-hr", type=float, default=None, help="P1-C 风险比 HR")
    pv.add_argument("--verify-median-control", type=float, default=None,
                    help="P1-C 对照中位生存（与 HR 同单位）")
    pv.add_argument("--verify-accrual", type=float, default=None, help="P1-C 入组期")
    pv.add_argument("--verify-followup", type=float, default=None, help="P1-C 末例随访期")
    pv.add_argument("--verify-boundaries", type=str, default=None,
                    help="P1-C 组序贯 z 边界（rpact/gsDesign 输出，逗号分隔）。"
                         "强烈建议提供——这才是独立验证；不提供则用内置 Lan-DeMets 自算（仅 sanity）")
    pv.add_argument("--verify-looks", type=int, default=2)
    pv.add_argument("--verify-spending", default="obrien_fleming",
                    choices=["obrien_fleming", "pocock"])
    pv.add_argument("--verify-expected-events", type=float, default=None,
                    help="P1-C 生存设计解析期望事件数（校验容差 ±5%%）")
    pv.add_argument("--verify-interim-fraction", type=float, default=None,
                    help="P1-C 适应性 SSR interim 信息比例")
    pv.add_argument("--verify-target-cp", type=float, default=None,
                    help="P1-C 适应性 SSR 目标条件功效")
    pv.add_argument("--verify-max-inflation", type=float, default=None,
                    help="P1-C 适应性 SSR 二阶段样本量上限倍数")
    pv.add_argument("--verify-json", default=None, help="P1-C 验证报告 JSON 输出路径")
    pv.add_argument("--verify-no-tie", action="store_true",
                    help="P1-C 跳过 H0 TIE 检验")

    # ── 出图模式（ct-base §19.9）──
    p.add_argument("--figure-mode", dest="figure_mode", choices=["svg_inline", "png_file"],
                   default=None,
                   help="图形呈现模式: svg_inline(默认,内联对话流) / png_file(本地 cairosvg 转 PNG)。"
                        "也可经环境变量 CTSS_FIGURE_MODE 设置。")

    return p


# ─────────────────────────────────────────────────────────────────────────────
# 单条 / 批量结果渲染（v5.7：抽为共享函数，单请求与批量路径复用）
# ─────────────────────────────────────────────────────────────────────────────
def _render_single_result(res, test, figure_mode=None, out_dir=None, idx=None,
                          show_alloc=True):
    """渲染单条 Result（文本 + 图形 + HTML 报告 + 曲线兜底 + R 代码），与历史单请求渲染一致。

    idx 非空时先打印分隔标题（批量路径逐项使用）；单请求路径 idx=None 不打印分隔。
    coze 后端无需 --yes 确认（gated=False），故 R 代码 / R 数值始终展示（与历史行为一致）。
    show_alloc=False 时本地 HTML 渲染层隐藏「分配比四图」（coze 端仍返回全量，仅此处过滤）。
    """
    if idx is not None:
        print("\n" + "-" * 60)
        print("▌ %d) test=%s" % (idx, test))
        print("-" * 60)
    if res.text:
        print(res.text)

    # ── 图形产物（coze 返回 SVG/HTML；本地 R 直接写 PNG）──
    render_figures(res.figures, test, figure_mode=figure_mode, show_alloc=show_alloc)
    # v5.3.2：聚合 HTML 报告（stats + 内联 SVG + R 复现脚本，单文件浏览器直接打开）
    try:
        from rendering import render_html_report  # type: ignore  # adapters/rendering.py

        _report_env = {
            "status": "ok",
            "stats": res.r_result or res.meta,
            "narrative": res.text,
            "figures": [
                {"format": f.format, "content": f.content, "caption": f.caption}
                for f in _filter_alloc(res.figures, show_alloc)
            ],
            # 高级方法（B 类名单）不把 R 代码写进 HTML 报告（2026-10-13 产品策略；
            # 付费用户 is_paid_env() 放行——与 coze 端 node 出口判定一致）
            "repro": ({"r": res.r_code}
                      if (res.r_code
                          and not r_code_unavailable(test, paid=is_paid_env()))
                      else None),
            "warnings": [],
            # 契约漂移标记（ct-base §20.9）：透传自 compute 的 meta，供渲染横幅消费
            "_needs_upgrade": bool((res.meta or {}).get("_needs_upgrade", False)),
            "_contract_drift": (res.meta or {}).get("_contract_drift", []) or [],
        }
        _rp = render_html_report(_report_env, out_dir=out_dir or _outputs_dir(),
                                 test=test, backend=res.backend or "coze",
                                 show_alloc=show_alloc)
        if _rp:
            print('__FIGURE__ html %s caption="ct-samplesize 结果报告"' % _rp)
    except Exception as _e:  # noqa: BLE001 - HTML 报告生成失败不阻断主流程
        print("# HTML 报告生成跳过: %s" % _e)
    # coze 端无图（svglite/cairo 缺失）但返回曲线数值 → 本地生成 SVG 兜底（ct-base §19）。
    # 仅在 coze 未返回任何图形时才兜底——否则同一曲线会被处理两遍（coze SVG + 本地
    # fallback 两份输出），且持久化文件可能被无参考线的 fallback 版覆盖（2026-08-20 修复）。
    if not res.figures:
        render_curve_fallback(res.meta, test,
                              target_power=0.8, ref_n=None)
    # coze 返回未填充 meta 时（无 __CTSS_RESULT__ 标记）res.meta 可为 None，防御性取空字典
    _png = (res.meta or {}).get("png_path")
    if _png:
        print(t("info.png_saved", path=_png))

    # ── R 源码 / R 数值（默认回传并展示，对齐 meta-analysis；2026-08-29 修订）──
    # 旧逻辑仅在 --show-code / CTSS_RETURN_R_CODE 时展示；现默认展示（coze 始终回传 repro.r）。
    # 2026-10-13：B 类高级方法（r_code_policy.R_CODE_UNAVAILABLE_TESTS）对免费用户
    # 不提供 R 代码，改提示联系作者；付费用户（CTSS_ACCOUNT_ID / CTSS_BILLING_TOKEN）
    # 放行。coze 端 node 出口已按同标记判定；此处为展示层兜底（含 mock/本地路径）。
    # R 数值结果（r_result）不受影响，照常展示。
    if r_code_unavailable(test, paid=is_paid_env()):
        print("=" * 60)
        print(t("info.r_code_unavailable"))
        print("=" * 60)
    elif res.r_code:
        print("=" * 60)
        print(t("header.r_code"))
        print("=" * 60)
        print(res.r_code)
    if res.r_result:
        print("-" * 60)
        print(json.dumps(res.r_result, ensure_ascii=False, indent=2))
    print("=" * 60)


def render_batch(br, specs, figure_mode=None):
    """渲染批量聚合结果（coze v5.7 batch）：先打印汇总，再逐项渲染（复用 _render_single_result）。"""
    print("=" * 60)
    print("批量计算结果 / Batch Results")
    print("=" * 60)
    print("总数 %d · 成功 %d · 失败 %d · tests=%s · modes=%s · 状态=%s"
          % (br.count, br.ok, br.errors, br.tests, br.modes, br.status))
    print("=" * 60)
    for it, spec in zip(br.items, specs):
        if it.result is not None:
            # 逐项判定是否显式要求不等比例分配（spec[1] 为该条目的 args Namespace）
            show_alloc = _ratio_is_unequal(getattr(spec[1], "ratio", None))
            _render_single_result(it.result, it.test, figure_mode=figure_mode,
                                  idx=it.index, show_alloc=show_alloc)
        else:
            print("\n" + "-" * 60)
            print("▌ %d) test=%s [失败]" % (it.index, it.test))
            print("-" * 60)
            print("# 错误: %s" % (it.error or it.status))
            print("=" * 60)


def _run_batch(backend, args, base_ctx):
    """批量路径入口：读取 --batch-file，构造 specs，调用后端 compute_batch，渲染聚合结果。

    batch-file 格式：JSON 数组，元素 {"test": 终点类型, "args": {覆盖字段},
    "ctx": {覆盖字段}}。逐项克隆命令行 args 为完整 Namespace 并覆盖指定字段（继承默认值），
    故只需在文件里写差异字段。dry-run / --show-code 时仅打印批量请求信封预览。
    """
    from adapters.coze_client import build_batch  # 延迟导入，避免循环

    try:
        with open(args.batch_file, "r", encoding="utf-8") as fh:
            entries = json.load(fh)
    except Exception as _e:  # noqa: BLE001
        print("# [batch] 读取批量文件失败: %s" % _e)
        sys.exit(1)
    if not isinstance(entries, list):
        print("# [batch] 批量文件根必须是 JSON 数组")
        sys.exit(1)

    specs = []
    for entry in entries:
        if not isinstance(entry, dict) or not entry.get("test"):
            print("# [batch] 跳过非法条目（缺 test）: %r" % entry)
            continue
        a = argparse.Namespace(**vars(args))        # 克隆命令行默认参数
        a.test = entry["test"]
        for k, v in (entry.get("args") or {}).items():
            setattr(a, k, v)
        ctx_i = dict(base_ctx)
        ctx_i.update(entry.get("ctx") or {})
        specs.append((entry["test"], a, ctx_i))

    if not specs:
        print("# [batch] 无有效条目，退出")
        sys.exit(1)

    # dry-run / --show-code：仅预览批量请求信封（不发送）
    if args.dry_run or args.show_code:
        env = build_batch(specs)
        print("=" * 60)
        print("批量请求信封预览（coze v5.7 batch）")
        print("=" * 60)
        print(json.dumps(env, ensure_ascii=False, indent=2, default=str))
        print("=" * 60)
        return

    try:
        br = backend.compute_batch(specs)
    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)
    render_batch(br, specs, figure_mode=args.figure_mode)


def main():
    """CLI 入口：整条命令包一层 request_scope。

    2026-11-15：一次用户需求（一条 CLI 命令 / 一次工作台操作）常被拆成多个
    Coze 子请求（n→power 验算、曲线、批量格点、验证器），以前每个 POST 各写
    一行飞书。这里统一分配 request_id，服务端 feishu_save 按它合并成一行。
    coze_client 不可导入（纯本地 R 路径）时零影响。
    """
    try:
        from adapters.coze_client import request_scope
    except Exception:  # noqa: BLE001 — 纯本地路径 / 循环导入均无副作用
        return _main_impl()
    with request_scope():
        return _main_impl()


def _main_impl():
    global _FIG_FILE_SEQ
    _FIG_FILE_SEQ = 0  # 重置落盘文件序号，保证每次 CLI 调用从 1 起、序号确定
    p = build_parser()
    args = p.parse_args()

    # ── Security: validate every user string that reaches generated R code ──
    # These are interpolated into R string literals; enforce strict allowlists so
    # they can never inject arbitrary R code. Fail fast with a clear message.
    try:
        _validate_token("--adaptive_type", args.adaptive_type)
        _validate_token("--design", args.design)
        _validate_token("--spending_func", args.spending_func)
        _validate_token("--effect_name", args.effect_name)
        if args.test == "adaptive_simulate":
            _validate_token("--sim_design", args.sim_design)
            _validate_token("--spending_function", args.spending_function)
            _validate_token("--reestimate_method", args.reestimate_method)
            _validate_token("--correction", args.correction)
            if args.effect_sizes is not None:
                if not re.match(r'^[0-9.,\- ]+$', args.effect_sizes):
                    raise ValueError(
                        t("error.effect_sizes_invalid", value=args.effect_sizes))
            if args.sim_output is not None:
                _validate_path(args.sim_output)
        if args.out is not None:
            _validate_path(args.out)  # raises ValueError if unsafe
    except ValueError as e:
        p.error(str(e))

    # ═══ E1/E2: 自然语言确定性预路由（零 LLM，仅本地快速预解析）═══
    # 若提供 --nl，先用确定性规则识别 test + 提取参数，结果 write-thru 到 args 作为强信号；
    # 置信度低 / 参数不全时打印结构化提示（不静默错参、不阻断），由本地 agent 向用户追问缺失项；原始 NL 永不进入 coze 信封。
    if args.nl:
        if not _NL_AVAILABLE:
            print("# [NL-route] 本地 NL 解析模块不可用，跳过 --nl 预路由；请向用户追问 test/参数，原始 NL 不入 coze")
        else:
            _nl = args.nl
            _cls = _nl_classify(_nl)
            if _cls.get("test"):
                args.test = _cls["test"]
                print("# [NL-route] test=%s (confidence=%s, matched=%s)"
                      % (args.test, _cls["confidence"], ",".join(_cls.get("matched", [])) or "-"))
                if _cls.get("needs_llm_fallback"):
                    print("# [NL-route] 终点类型置信度低，建议向用户追问终点类型（≤2 轮→默认，ct-base §6.1）")
                for _m in _cls.get("missing", []):
                    print("# [NL-route] 缺关键信息: %s" % _m)
            else:
                print("# [NL-route] 未能从自然语言识别 test，请向用户追问终点类型；原始 NL 不入 coze")
            # 参数提取：仅把 NL 中明确给出的参数 write-thru 到 args（不推断、不补默认）
            _pe = _nl_extract(_nl, test=args.test)
            for _k, _v in _pe.get("params", {}).items():
                if hasattr(args, _k):
                    setattr(args, _k, _v)
            if _pe.get("needs_llm_fallback"):
                _note = "; ".join(_pe.get("notes", [])) or "参数识别不全"
                print("# [NL-params] 部分参数需向用户追问补全: " + _note)

    # SECURITY: dry-run is the SAFE DEFAULT. Execution requires an explicit
    # opt-in (--yes / -y) so generated R code is never run silently.
    confirmed = args.yes and not args.dry_run

    # ── Solve direction: --nobs given → solve for power; else solve for n ──
    if args.nobs is not None and args.nobs > 0:
        solve_for_power = True
    else:
        solve_for_power = False
        args.nobs = None

    # ── Numeric range validation ──
    _RANGE_RULES = {
        "alpha": (0, 0.5), "power": (0, 1),
        "auc0": (0, 1), "auc1": (0, 1),
        "correlation": (-1, 1), "icc": (0, 1),
        "margin": (0, None), "hazard_ratio": (0, None),
        "ni_margin_surv": (0, None), "sup_margin": (0, None),
        "delta_sup": (0, None),
        "ve_control": (0, 1), "ve_treatment": (0, 1),
        "prob_control": (0, 1), "prob_treatment": (0, 1),
        "p_control_sup": (0, 1), "p_control_current": (0, 1),
        "event_rate_exact": (0, 1), "dropout_exact": (0, 1),
        "p1": (0, 1), "p2": (0, 1),
        "eq_margin_surv": (0, None), "sup_margin_surv": (0, None), "sup_hr": (0, None),
        "cox_hr": (0, None), "cox_r2": (0, 1), "cox_prev": (0, 1),
        "cox_event_prop": (0, 1), "median0": (0, None), "median1": (0, None),
        "ci_control": (0, 1), "ci_treatment": (0, 1),
        "rate_control": (0, None), "rate_ratio": (0, None),
        "recur_followup": (0, None), "new_median": (0, None), "hist_n": (0, None),
        "gs_ratio": (0, 1), "gs_or": (0, None), "gs_median_control": (0, None),
        "gs_rate1": (0, None), "gs_rate2": (0, None), "gs_poisson_time": (0, None),
        "nobs": (0, None),
    }
    _range_errors = []
    for label, (lo, hi) in _RANGE_RULES.items():
        val = getattr(args, label, None)
        if val is None:
            continue
        if lo is not None and val <= lo:
            _range_errors.append(t("validation.range_error_gt", label=label, bound=lo, val=val))
        if hi is not None and val >= hi:
            _range_errors.append(t("validation.range_error_lt", label=label, bound=hi, val=val))
    if _range_errors:
        print(t("validation.failed"))
        for e in _range_errors:
            print(f"  ✗ {e}")
        sys.exit(1)

    # ── 公开证据参考采纳（路线 A，2026-10-14）──
    # 插在数值范围校验之后、d_val 折算之前：--adopt-ref 显式指定才代入，
    # 代入值覆盖对应 args 参数，来源打印到 stdout 并进入假设清单（可审计）。
    # 尺度/终点不符（effect_ref.compatible）硬拒绝；文件校验失败即退出，不静默跳过。
    if getattr(args, "adopt_ref", None) and not getattr(args, "effect_ref", None):
        p.error("--adopt-ref 须与 --effect-ref 同用（采纳目标参考文件缺失）")
    if getattr(args, "effect_ref", None) and getattr(args, "adopt_ref", None):
        try:
            import effect_ref as _er
        except ImportError:
            import scripts.effect_ref as _er
        _ref_data, _err = _er.load_ref(args.effect_ref)
        if _err:
            print("[effect-ref] " + _err, file=sys.stderr)
            sys.exit(1)
        _refs, _errors, _warnings = _er.validate(_ref_data)
        if _errors:
            for _e in _errors:
                print("[effect-ref] ✗ " + _e, file=sys.stderr)
            sys.exit(1)
        _adopted, _perr = _er.pick(_refs, args.adopt_ref)
        if _perr:
            print("[effect-ref] " + _perr, file=sys.stderr)
            sys.exit(1)
        _ok, _reason = _er.compatible(_adopted, args.test, args)
        if not _ok:
            print("[effect-ref] " + _reason, file=sys.stderr)
            sys.exit(1)
        # OR/RR 参考经 --effect 落地（ci_or/ci_rr/regression_*/rates_ext 引擎读 p$effect）；
        # effect/hazard_ratio 同名落地。映射表见 effect_ref.TARGET_ARG。
        _target_arg = _er.TARGET_ARG.get(_adopted["param"], _adopted["param"])
        setattr(args, _target_arg, _adopted["value"])
        print("[effect-ref] 已采纳公开参考：%s=%s（%s）→ 落地参数 --%s；来源: %s"
              % (_adopted["param"], _adopted["value"], _adopted["basis"],
                 _target_arg, _adopted["source"]))
        print("[effect-ref] 声明: " + _er.DISCLAIMER)
        args._effect_ref_ctx = {"ta": args.ta or _ref_data.get("ta"),
                                "endpoint": args.endpoint or _ref_data.get("endpoint"),
                                "summary": _er.summarize(_refs),
                                "adopted": _adopted,
                                "disclaimer": _er.DISCLAIMER}
    elif getattr(args, "effect_ref", None):
        # 仅展示不采纳：数据照样校验（错误即退出），但不改任何参数
        try:
            import effect_ref as _er
        except ImportError:
            import scripts.effect_ref as _er
        _ref_data, _err = _er.load_ref(args.effect_ref)
        if _err:
            print("[effect-ref] " + _err, file=sys.stderr)
            sys.exit(1)
        _refs, _errors, _warnings = _er.validate(_ref_data)
        if _errors:
            for _e in _errors:
                print("[effect-ref] ✗ " + _e, file=sys.stderr)
            sys.exit(1)
        args._effect_ref_ctx = {"ta": args.ta or _ref_data.get("ta"),
                                "endpoint": args.endpoint or _ref_data.get("endpoint"),
                                "summary": _er.summarize(_refs),
                                "adopted": None,
                                "disclaimer": _er.DISCLAIMER}

    # ── 效应量 / 检验方向统一处理 (--side / --sd) ──
    # alt: one-sided -> "greater" (预期处理组更优); two-sided -> "two.sided"
    alt = "greater" if args.side == "one" else "two.sided"
    # d_val: 提供 --sd 时 --effect 视为原始均差 Δ, 自动折算 d = Δ/sd; 否则 --effect 直接为 d
    # upgrade J1: --mcid 是 --effect(原始单位) 的语义别名——MCID 必须以原始单位 + sd
    # 折算（d = MCID/sd），单独给出即声明"目标差值来自临床锚定"而非拍脑袋效应量。
    _mcid_mode = args.mcid is not None
    if _mcid_mode:
        if args.sd is None or args.sd <= 0:
            p.error("--mcid 需配合 --sd（MCID 以原始终点单位表示，折算 d = MCID / SD）")
        if args.effect is not None:
            p.error("--mcid 与 --effect 互斥：MCID 即目标差值（原始单位），请二选一")
        args.effect = args.mcid   # 折算通道复用：effect(Δ)/sd
    if args.sd is not None and args.sd > 0:
        d_val = (args.effect if args.effect is not None else 0.5) / args.sd
    else:
        d_val = args.effect if args.effect is not None else 0.5

    if not args.test and not args.batch_file:
        if args.nl:
            p.error(t("error.test_required")
                    + "（自然语言路由未能识别终点类型：请用 --test 显式指定，或换种表述后重试）")
        else:
            p.error(t("error.test_required"))

    # ── upgrade J1：MCID 折算回显（计算模式；规划审计另见 --audit 分支）──
    if _mcid_mode:
        print("[MCID] 目标差值 = MCID %s（原始单位）｜ SD = %s ｜ 折算效应量 d = %.4f"
              % (args.mcid, args.sd, d_val))
        print("[MCID] 依据: %s" % (args.mcid_source
              or "（未声明——SPIRIT Item14/CDE 要求『目标差值须有临床依据』，建议 --mcid-source 标注 "
              "anchor-/distribution-/expert- 来源与出处）"))

    # ── 假设清单显式化（ct-update 建议 ct-samplesize::E）──
    # 独立于后端（coze/R），仅做可审计性清单输出，不触碰数值真相源。
    if args.show_assumptions:
        try:
            import assumption_block as _ab
        except ImportError:
            import scripts.assumption_block as _ab  # 作为脚本子模块时
        _ectx = getattr(args, "_effect_ref_ctx", None)
        block = _ab.build_assumption_block(args, args.test, p, effect_ref=_ectx)
        print("=" * 60)
        print("假设清单 / Assumption Block")
        print("=" * 60)
        print(_ab.json.dumps(block, ensure_ascii=False, indent=2))
        if _ectx:
            try:
                import effect_ref as _er
            except ImportError:
                import scripts.effect_ref as _er
            print(_er.render({"ta": _ectx.get("ta"), "endpoint": _ectx.get("endpoint")},
                             _ectx["summary"], _ectx["adopted"], []))
        sys.exit(0)

    # ── 假设质量审计（ct-update 建议 ct-samplesize::I，规划层）──
    # 四分级证据审计 + 设计逻辑族自洽 + fallback 规划；同样独立于后端。
    if args.audit:
        try:
            import hypothesis_audit as _ha
        except ImportError:
            import scripts.hypothesis_audit as _ha
        _ov = {}
        for _k in (args.evidence_source or "").split(","):
            if _k.strip():
                _ov[_k.strip()] = "known"
        if _mcid_mode:
            # J1 联动：MCID 有临床来源声明 → 效应量假设升 known（无来源时仍按
            # 启发式判定，distribution 拍值不豁免）
            _ov["effect"] = "known" if args.mcid_source else "weak"
        _rep = _ha.audit_hypotheses(args, args.test, p, grades_override=_ov)
        if _mcid_mode:
            print("[MCID] d = MCID(%s) / SD(%s) = %.3f | 依据: %s"
                  % (args.mcid, args.sd, d_val, args.mcid_source or "（未声明——建议 --mcid-source 标注 anchor/distribution/expert 来源）"))
        print(_ha.render_text(_rep))
        sys.exit(0)

    # ═════════════════════════════════════════════════════════════════════════
    # 统一后端调度（coze 权威 / 本地 Python 兜底 / 本地 R 开发后端）
    # ═════════════════════════════════════════════════════════════════════════
    ctx = {
        "confirmed": confirmed,
        "solve_for_power": solve_for_power,
        "alt": alt,
        "d_val": d_val,
        "curve": bool(args.n_seq or args.power_seq or args.effect_seq
                     or args.dist_plot or args.power_time_seq or args.heatmap),
        "show_code": bool(args.show_code),
        "dry_run": bool(args.dry_run),
        # R 真相源开关：默认回传完整 R 源码 + R 数值（repro.r），对齐 meta-analysis 的
        # "每个分析默认回传可复现 R 代码" 行为（用户规则 2026-08-29：默认分析回传 R 代码）。
        # 旧逻辑仅在 --show-code / CTSS_RETURN_R_CODE 时开启，导致 coze 默认根本不被要求
        # 返回 R 代码、HTML 报告与对话都拿不到（即用户报的"默认不回传 R 代码"）。
        "return_r_code": True,
        # coze 计算端语言备用入参（ct-base language_policy.md §"user_language 备用入参"）：
        # 由 i18n.resolve_user_language 按三级优先级统一解析——① 显式 override
        # (--language / CTSS_LOCALE) ② 否则按 --nl 输入文本内容级检测 ③ 回退系统 locale。
        # 仅作为"调用方提示"注入请求，coze 端可忽略；不影响本地 UI 提示语言（仍走系统 locale）。
        "user_language": resolve_user_language(
            query=args.nl,
            override=args.language or os.environ.get("CTSS_LOCALE") or os.environ.get("CTSS_LANG"),
        ),
    }

    try:
        backend = select_backend(args.test)  # v5: 唯一后端 = coze（无本地回退）
    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)

    # ── 批量模式（coze v5.7 batch）：一次请求完成网格/敏感性扫描，本地逐项渲染 ──
    if args.batch_file:
        _run_batch(backend, args, ctx)
        return

    # ── 待执行载荷预览（local-r → R 源码；coze → 请求信封；python → 无）──
    gated = backend.requires_confirmation          # 本地 R 需 --yes；coze / Python 不需要
    payload = backend.preview(args.test, args, ctx)
    if payload is not None and (args.show_code or args.dry_run or (gated and not confirmed)):
        _hdr = t("header.r_code") if gated else t("header.coze_request")
        print("=" * 60)
        print(_hdr)
        print("=" * 60)
        print(payload)
        print("=" * 60)

    if gated and not confirmed:
        print(t("safe_preview.not_executed_curve") if ctx["curve"]
              else t("safe_preview.not_executed"))
        return
    if args.dry_run:
        return

    if gated:
        print(t("exec.running"))
        sys.stdout.flush()

    # ── 自动附带曲线（v5.3.2 起契约 default_curve 配置）── 折叠改造 2026-10-07 ──
    # 不发起第二次 coze POST（原 res2 块）；改为把 [主求解, 曲线] 组装为批量信封，
    # 经 compute_batch 一次性发出（1 次 POST / 1 行 searchlog），coze 内部逐 spec 独立
    # 求解——主 n 求解与曲线互不影响（coze 收到 curve_* 会切换为「仅曲线」模式，不能并入
    # 主 POST，否则主求解被吞）。用户显式 --power_seq/--n_seq 时 ctx["curve"]=True，走用户
    # 自己的曲线，不触发本块。coze 端点契约未变 ⇒ 旧版本地客户端（仍发 res2）不受影响。
    auto_curve = (not ctx["curve"] and args.test in _auto_curve_tests()
                  and not args.dry_run and not gated)

    def _make_curve_spec():
        a2 = argparse.Namespace(**vars(args))
        a2.n_seq = None
        a2.power_seq = None
        a2.plot_effects = None
        c2 = dict(ctx)
        c2["curve"] = True
        if solve_for_power and args.nobs:
            _n = args.nobs
            _n_min = max(5, int(_n * 0.5))
            _n_max = max(_n_min + 8, int(_n * 1.5))
            _step = max(1, round((_n_max - _n_min) / 8))
            a2.n_seq = "%d:%d:%d" % (_n_min, _step, _n_max)
        else:
            a2.power_seq = "0.6:0.05:0.95"
        return a2, c2

    try:
        if auto_curve:
            a2, c2 = _make_curve_spec()
            _batch = backend.compute_batch(
                [(args.test, args, ctx), (args.test, a2, c2)])
            res = _batch.items[0].result
            _curve_res = _batch.items[1].result
            if res is None:
                raise RuntimeError(
                    "批量计算主求解项失败: %s"
                    % (_batch.items[0].error or "未知错误"))
        else:
            res = backend.compute(args.test, args, ctx)
            _curve_res = None
    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)

    _render_single_result(res, args.test, figure_mode=args.figure_mode,
                          show_alloc=_ratio_is_unequal(args.ratio))

    # ── 自动附带曲线渲染（折叠后曲线来自批量信封第二项；按用户口径不打印"已自动附带"提示）──
    if _curve_res is not None:
        if getattr(_curve_res, "figures", None):
            render_figures(_curve_res.figures, args.test, figure_mode=args.figure_mode,
                           show_alloc=_ratio_is_unequal(args.ratio))
        else:
            render_curve_fallback(getattr(_curve_res, "meta", None), args.test,
                                  target_power=getattr(args, "power", None) or 0.8,
                                  ref_n=getattr(args, "nobs", None))

    # ── upgrade J2：IRB/SAP-ready 论证段落（中英双语，计算完成后追加）──
    # 默认隐藏（用户口径 2026-09-29）：不带 --justify 不直接生成段落，仅在单次
    # 计算成功后给一行"可生成文档段落"提示，由用户/agent 决定是否补跑。
    if getattr(args, "justify", False):
        try:
            import justify_text as _jt
        except ImportError:
            import scripts.justify_text as _jt
        _n_res, _n_key = None, ""
        for _src in (res.meta, res.r_result):
            if isinstance(_src, dict):
                for _k in ("n", "n_total", "total_n", "N", "required_n",
                           "n_per_group", "nPerGroup", "n1"):
                    if _src.get(_k) is not None:
                        _n_res, _n_key = _src[_k], _k
                        break
            if _n_res is not None:
                break
        _n_note = "每组" if _n_key in ("n_per_group", "nPerGroup", "n1") else "总"
        print(_jt.render(args.test, args, d_val, n_total=_n_res,
                         mcid_mode=_mcid_mode, n_note=_n_note, meta=res.meta))
    elif not ctx["curve"]:
        try:
            print("\n" + t("offer.justification"))
        except Exception:  # noqa: BLE001 - 提示缺失不影响主结果输出
            pass

    # ── 默认图形层（v5.6 起全部上 coze）────────────────────────────────────
    # 架构：coze 端 R（coze_figure_layer.R）为主出图；若其失败，coze 内部回退到
    #   figure_kit.py（随包上传到 coze 的 Python 兜底，位于 adapters/coze/scripts/）。
    #   本地是「瘦客户端」：只承接 coze 回传的 `figures` 数组，交由 _render_single_result
    #   统一落盘 / 内联 / 聚合进 HTML 报告，本地绝不再渲染（详见 SKILL.md v5.6 说明）。
    #   （历史上此处有一段本地透出循环，与 render_figures 重复，已在 v5.6 删除。）

    # ── P1-C: 本地模拟验证闭环（独立 Monte-Carlo，默认关闭）──
    if args.verify:
        if _verify_run is None:
            print("# [verify] 模块 verify.py 不可用，跳过验证。")
        elif not args.verify_n:
            print("# [verify] 未提供 --verify-n（解析解给出的样本量）；无 n 则验证无意义，跳过。")
        else:
            try:
                bnds = None
                if args.verify_boundaries:
                    bnds = [float(x) for x in
                            args.verify_boundaries.replace(" ", "").split(",") if x]
                vparams = {k: v for k, v in {
                    "effect_size": args.verify_effect_size, "p1": args.verify_p1,
                    "p2": args.verify_p2, "hazard_ratio": args.verify_hr,
                    "median_control": args.verify_median_control,
                    "accrual": args.verify_accrual, "followup": args.verify_followup,
                    "interim_fraction": args.verify_interim_fraction,
                    "target_cp": args.verify_target_cp,
                    "max_inflation": args.verify_max_inflation,
                }.items() if v is not None}
                vrep = _verify_run(
                    args.verify_design or "ttest_ind", args.verify_n, alpha=args.alpha,
                    power=args.verify_power, side=args.verify_side,
                    nsim=args.verify_nsim, params=vparams, boundaries=bnds,
                    looks=(len(bnds) if bnds else args.verify_looks),
                    spending=args.verify_spending,
                    expected_events=args.verify_expected_events,
                    check_tie=not args.verify_no_tie)
                print(vrep if isinstance(vrep, str) else _verify_fmt(vrep))
                if args.verify_json:
                    with open(args.verify_json, "w", encoding="utf-8") as _vf:
                        json.dump(vrep, _vf, ensure_ascii=False, indent=2)
                    print("\n[verify] JSON -> %s" % args.verify_json)
            except SystemExit as _se:
                print("# [verify] 中止: %s" % _se)
            except Exception as _e:  # noqa: BLE001 - 验证失败不阻断主样本量结果
                print("# [verify] 验证失败（不影响主结果）: %s" % _e)


if __name__ == "__main__":
    main()
