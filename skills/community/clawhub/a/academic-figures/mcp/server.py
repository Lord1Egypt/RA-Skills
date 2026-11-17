#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""academic-figures MCP server — 41 种学术图型（随引擎注册表）经 FastMCP 暴露。

运行（分发形态）:
    uvx --from "git+https://github.com/docsor1212/academic-figures#subdirectory=mcp" academic-figures-mcp
    # 或本地: python mcp/server.py            # stdio（默认）
    #        python mcp/server.py --http 8765 # streamable-http

设计原则:
- 核心实现 render_chart_impl / suggest_chart_impl / doctor_impl 不依赖 fastmcp
  （纯 subprocess 调引擎），无 fastmcp 环境下本模块仍可 import 与测试。
- 引擎定位: 优先包内嵌入式副本 af_engine/（uvx/git 分发形态，由 mcp/sync_engine.sh
  从 trunk scripts/ 同步并做 sha 门禁）；回退 trunk 布局 ../scripts/（开发形态）。
- 边界（G5）: 单次调用单图；data ≤ 2MB；dpi 72–600；预览 dpi ≤ 150；
  stdout/stderr 截断 4KB；渲染超时 900s（引擎内另有自适应看门狗）。
- 红线: 零密钥、零遥测、纯本地渲染；Pro 云渲染与计费不在本 Server 范围。
- 确定性: 同输入同字节（引擎保证），MCP 层不做任何缓存改写。
"""
import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))

# 引擎定位: 包内嵌入式副本（分发形态）→ trunk scripts/（开发形态）
_ENGINE_DIR = None
for _cand in (os.path.join(_HERE, "af_engine"),
              os.path.join(os.path.dirname(_HERE), "scripts")):
    if os.path.isfile(os.path.join(_cand, "gen_figure.py")):
        _ENGINE_DIR = _cand
        if _cand not in sys.path:
            sys.path.insert(0, _cand)
        break
if _ENGINE_DIR is None:
    raise FileNotFoundError("gen_figure.py 未找到（af_engine/ 嵌入副本或 ../scripts/）")
GEN = os.path.join(_ENGINE_DIR, "gen_figure.py")

try:
    from fastmcp import FastMCP
    try:
        from fastmcp.utilities.types import Image  # fastmcp 4.x：Image 不在顶层
    except ImportError:
        from fastmcp import Image  # 兼容旧版
    _MCP_OK = True
except ImportError:  # pragma: no cover - 无 fastmcp 时仅暴露 impl（可测试）
    _MCP_OK = False

CHARTS = [
    "bar", "bland_altman", "box", "boxplot", "calibration",
    "cif", "cluster_heatmap", "composite", "dca", "diagram",
    "dual_axis", "dumbbell", "forest", "funnel", "galbraith",
    "flow", "grouped_bar", "hbar", "heatmap", "horizontal_bar", "km",
    "labbe", "line", "nomogram", "paired", "pca",
    "prisma", "raincloud", "rcs", "ridgeline", "rmst",
    "rob", "roc", "scatter", "slope", "stacked_bar",
    "subgroup", "survival", "swimmer", "upset", "venn",
    "violin", "volcano", "waterfall"]
MAX_DATA_BYTES = 2_000_000     # G5: 数据上限（与 Pro 对齐）
MAX_DPI, MIN_DPI = 600, 72
PREVIEW_DPI_MAX = 150          # 回传预览上限（600dpi 成品只落盘不回传）
RENDER_TIMEOUT = 900           # 秒（引擎内看门狗先于本超时触发）
_CLIP = 4000                   # G5: 文本字段截断
_OPT_STR = {"title", "subtitle", "source", "xlabel", "ylabel", "theme", "style",
            "journal", "column", "legend_loc"}
_OPT_FLAG = {"verify", "cjk", "peak_label", "summary", "legend_outside"}


def _clip(obj, limit=_CLIP):
    """递归截断长字符串（防超大输出撑爆 MCP 消息；结构保持）。"""
    if isinstance(obj, str):
        return obj if len(obj) <= limit else obj[:limit] + f"…[+{len(obj) - limit} chars]"
    if isinstance(obj, list):
        return [_clip(x, limit) for x in obj]
    if isinstance(obj, dict):
        return {k: _clip(v, limit) for k, v in obj.items()}
    return obj


def _validate(chart, data, dpi):
    if chart not in CHARTS:
        raise ValueError(f"chart 必须是以下之一: {', '.join(CHARTS)}")
    if not isinstance(data, str) or not data.strip():
        raise ValueError("data 必须是非空字符串（JSON 对象/数组或 CSV 文本）")
    if len(data.encode("utf-8")) > MAX_DATA_BYTES:
        raise ValueError(f"data 超过 {MAX_DATA_BYTES // 1000000}MB 上限")
    try:
        dpi = int(dpi)
    except (TypeError, ValueError):
        raise ValueError("dpi 必须是整数")
    if not (MIN_DPI <= dpi <= MAX_DPI):
        raise ValueError(f"dpi 必须在 {MIN_DPI}–{MAX_DPI}")
    return dpi


def _build_cmd(chart, inp, out, dpi, options, fmt):
    cmd = [sys.executable, GEN, "-t", chart, "-d", inp, "-o", out, "--dpi", str(dpi)]
    options = options or {}
    for k, v in options.items():
        k = str(k)
        flag = "--" + k.replace("_", "-")  # dest 下划线 → CLI 连字符（legend_outside→--legend-outside）
        if k in _OPT_STR and v not in (None, ""):
            cmd += [flag, str(v)[:200]]
        elif k in _OPT_FLAG and v:
            cmd.append(flag)
        elif k == "multi_format" and v:
            cmd += [flag, str(v)]
        elif k not in (_OPT_STR | _OPT_FLAG | {"multi_format"}):
            pass  # 未知键静默跳过（服务端宽容；引擎侧另有校验）
    if fmt != "png":
        cmd += ["-f", fmt]
    return cmd


def _run_engine(cmd, timeout=None):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=timeout or RENDER_TIMEOUT, encoding="utf-8",
                           errors="replace")
        return p.returncode, (p.stdout or ""), (p.stderr or "")
    except subprocess.TimeoutExpired:
        return 5, "", f"ERROR: 渲染超时（{RENDER_TIMEOUT}s 上限，引擎看门狗未及触发）"


def _refresh_charts_from_engine():
    """v5.7 机制化：以引擎 `--list-types` 注册表为准刷新 CHARTS（杜绝清单漂移——
    此前硬编码清单已落后引擎十余个图型）。引擎不可达/输出异常时保留内置清单。"""
    global CHARTS
    try:
        # 独立短超时（审计 P2）：引擎 import 挂死时不得拖住服务启动
        code, so, _se = _run_engine([sys.executable, GEN, "--list-types"],
                                    timeout=30)
        if code == 0:
            ts = sorted({x.strip() for x in (so or "").splitlines() if x.strip()})
            if len(ts) >= 10:
                CHARTS = ts
    except Exception:
        pass  # 回退内置清单（上面 CHARTS 初值，与 v5.7 注册表逐字对齐）


_refresh_charts_from_engine()


def query_capability_impl(chart: str = "") -> dict:
    """v6.8.0：图型能力查询（动态真值=引擎注册表，防清单/文档漂移）。
    chart 留空=全图型清单+旗标域速览；指定图型名=该图型专属/域外旗标详情。"""
    def _q(extra):
        return _run_engine([sys.executable, GEN] + extra, timeout=60)
    c1, types_out, e1 = _q(["--list-types"])
    if c1 != 0 or not types_out.strip():
        return {"ok": False, "error": f"引擎 --list-types 不可达: {(e1 or '')[:200]}"}
    charts = sorted({x.strip() for x in types_out.splitlines() if x.strip()})
    if not chart:
        c3, fl_all, _e3 = _q(["--list-flags"])
        return {"ok": True, "chart_count": len(charts), "charts": charts,
                "flags_overview": fl_all.strip() if c3 == 0 else "(--list-flags 不可达)",
                "usage": "chart 留空=全图型+旗标域速览；chart=图型名（如 km/labbe）看单图型旗标详情"}
    if chart not in charts:
        return {"ok": False, "error": f"未知图型 {chart}", "charts": charts}
    c2, fl_out, _e2 = _q(["--list-flags", chart])
    return {"ok": True, "chart": chart, "chart_count": len(charts),
            "flags": fl_out.strip() if c2 == 0 else "(--list-flags 不可达)"}


def render_chart_impl(chart: str, data: str, options: dict = None,
                      dpi: int = 150, fmt: str = "png",
                      return_preview: bool = True) -> dict:
    """渲染一张学术图表（纯实现，无 MCP 依赖）。

    返回 dict:
      status: ok | overlap_detected | fatal | timeout
      files: [{format, path}]
      preview_base64_png: 预览图 base64（fmt=png 且尺寸 ≤1.5MB 时）
      exit_code / stderr_tail: 引擎诊断（中文）
    """
    dpi = _validate(chart, data, dpi)
    fmt = str(fmt or "png").lower()
    if fmt not in ("png", "pdf", "svg", "eps", "tiff"):
        raise ValueError("fmt 必须是 png/pdf/svg/eps/tiff")
    options = options if isinstance(options, dict) else {}

    with tempfile.TemporaryDirectory(prefix="afmcp_") as work:
        ext = "json" if data.lstrip()[:1] in ("{", "[") else "csv"
        inp = os.path.join(work, "input." + ext)
        with open(inp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(data)
        out = os.path.join(work, "figure." + fmt)
        code, so, se = _run_engine(_build_cmd(chart, inp, out, dpi, options, fmt))
        status = {0: "ok", 2: "overlap_detected"}.get(code, "fatal" if code != 5 else "timeout")
        # 成品落持久目录（work 临时目录随 impl 返回即清理；路径必须对客户端长期有效）
        files = []
        if os.path.exists(out):
            persist = os.path.join(tempfile.gettempdir(), "af_mcp_out")
            os.makedirs(persist, exist_ok=True)
            final = os.path.join(persist, f"{chart}_{dpi}dpi.{fmt}")
            shutil.copy2(out, final)
            files = [{"format": fmt, "path": final}]
        result = {"status": status, "exit_code": code, "files": _clip(files),
                  "stderr_tail": _clip(se[-2000:]), "chart": chart, "dpi": dpi}
        preview = os.path.join(work, "figure.png")
        if (return_preview and fmt == "png" and os.path.exists(preview)
                and os.path.getsize(preview) <= 1_500_000):
            result["preview_base64_png"] = base64.b64encode(open(preview, "rb").read()).decode()
        return result


def suggest_chart_impl(data: str) -> dict:
    """数据驱动图型推荐（--suggest 同源）。"""
    if not isinstance(data, str) or not data.strip():
        raise ValueError("data 必须是非空字符串")
    if len(data.encode("utf-8")) > MAX_DATA_BYTES:
        raise ValueError(f"data 超过 {MAX_DATA_BYTES // 1000000}MB 上限")
    with tempfile.TemporaryDirectory(prefix="afmcp_") as work:
        ext = "json" if data.lstrip()[:1] in ("{", "[") else "csv"
        inp = os.path.join(work, "input." + ext)
        with open(inp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(data)
        code, so, se = _run_engine([sys.executable, GEN, "--suggest", "-d", inp])
        return {"status": "ok" if code == 0 else "error",
                "recommendation": _clip(so), "stderr_tail": _clip(se[-1000:])}


def doctor_impl(chart: str, data: str, options: dict = None) -> dict:
    """渲染前参数/环境体检（--doctor 同源，只体检不渲染）。"""
    dpi = _validate(chart, data, 150)
    options = options if isinstance(options, dict) else {}
    with tempfile.TemporaryDirectory(prefix="afmcp_") as work:
        ext = "json" if data.lstrip()[:1] in ("{", "[") else "csv"
        inp = os.path.join(work, "input." + ext)
        with open(inp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(data)
        cmd = [sys.executable, GEN, "-t", chart, "-d", inp, "--doctor"]
        for k, v in options.items():
            k = str(k)
            if k in _OPT_STR and v not in (None, ""):
                cmd += [f"--{k}", str(v)[:200]]
            elif k in _OPT_FLAG and v:
                cmd.append(f"--{k}")
        code, so, se = _run_engine(cmd)
        return {"exit_code": code, "report": _clip(se)}


def capability_matrix_impl() -> dict:
    """全图型注册表 × 期刊预设 × 关键边界（读引擎注册表，非手抄）。"""
    script = (
        "import json, glob, sys, os;"
        f"sys.path.insert(0, {str(_ENGINE_DIR)!r});"
        "os.chdir(sys.path[0]);"
        "import gen_figure as g;"
        "charts = sorted(set(k for k, v in g.GENERATORS.items()));"
        "journals = sorted(os.path.basename(p)[:-5] for p in glob.glob(os.path.join(sys.path[0], 'journal', '*.json')));"
        "print(json.dumps({'charts': charts, 'journals': journals,"
        "                  'count': len([c for c in charts if c not in ('horizontal_bar','boxplot','survival')])}, ensure_ascii=False))")
    code, so, se = _run_engine([sys.executable, "-c", script])
    try:
        return json.loads(so.strip().splitlines()[-1])
    except Exception:
        return {"error": se[-500:] or so[-500:]}


def changelog_impl(lines: int = 120) -> dict:
    cl = os.path.join(_ENGINE_DIR, "changelog.md")
    if not os.path.isfile(cl):
        cl2 = os.path.join(os.path.dirname(_ENGINE_DIR), "references", "changelog.md")
        cl = cl2 if os.path.isfile(cl2) else cl
    if not os.path.isfile(cl):
        return {"content": "(changelog.md 未随包分发)"}
    out = []
    for i, l in enumerate(open(cl, encoding="utf-8", errors="replace")):
        if i >= max(10, min(int(lines), 400)):
            break
        out.append(l.rstrip("\n"))
    return {"content": "\n".join(out)}


# ── FastMCP 三原语 ──────────────────────────────────────────────
if _MCP_OK:
    mcp = FastMCP("academic-figures")

    @mcp.tool
    def render_chart(chart: str, data: str, options: dict = None,
                     dpi: int = 150, fmt: str = "png") -> dict:
        """渲染一张投稿级学术图表。41 种图型（bar/line/km/forest/roc/slope/composite/prisma…，
        见 capability_matrix 资源）。data=JSON 对象字符串或 CSV 文本；options 可传
        title/subtitle/source/xlabel/ylabel/theme/journal/column/verify/peak_label/summary 等；
        返回 150dpi 内预览 base64 + 成品文件路径（默认 png，fmt=pdf 走矢量+重叠门禁）。"""
        result = render_chart_impl(chart, data, options, dpi, fmt)
        preview = os.path.join(tempfile.gettempdir(), "afmcp_last_preview.png")
        if fmt == "png" and result.get("preview_base64_png"):
            open(preview, "wb").write(base64.b64decode(result["preview_base64_png"]))
        return result

    @mcp.tool
    def suggest_chart(data: str) -> dict:
        """不确定用什么图？传入数据（JSON/CSV），返回数据驱动的图型推荐与理由。"""
        return suggest_chart_impl(data)

    @mcp.tool
    def doctor(chart: str, data: str, options: dict = None) -> dict:
        """渲染前参数/环境体检：组合冲突、数据 schema、依赖、输出目录一次说清（exit 1=有发现）。"""
        return doctor_impl(chart, data, options)

    @mcp.tool
    def query_capability(chart: str = "") -> dict:
        """查图型能力面：chart 留空=全注册表清单+每旗标域适用图型速览；
        指定 chart（如 "km"/"labbe"）=该图型专属旗标+域外旗标（[ignored] 预告）。
        动态真值=引擎 --list-types / --list-flags。"""
        return query_capability_impl(chart)

    @mcp.resource("capability://matrix")
    def capability_matrix() -> dict:
        """全图型注册表 × 期刊预设（引擎注册表实读）。"""
        return capability_matrix_impl()

    @mcp.resource("capability://changelog")
    def changelog() -> dict:
        """版本历史（头部）。"""
        return changelog_impl()

    @mcp.prompt
    def chart_picker(context: str = "") -> str:
        """选图助手：把用户场景引导到正确图型。"""
        return (
            "为用户的科研数据选图。步骤：\n"
            "1. 先用 suggest_chart 传入数据拿推荐；\n"
            "2. 两时点前后比较用 slope；多时点趋势用 line；\n"
            "3. time-to-event 用 km（竞争风险 events≥2 自动切 Aalen-Johansen）；\n"
            "4. 诊断试验用 roc（多模型加 options 不可行时改用 --compare 说明）；\n"
            "5. 多面板组图用 composite（panel_labels:true 自动 A/B/C，span 跨行跨列）。\n"
            + (f"用户上下文：{context}\n" if context else "")
            + "渲染统一走 render_chart。投稿 PDF 记得 options 里 verify:true。")


def main():
    ap = argparse.ArgumentParser(description="academic-figures MCP server")
    ap.add_argument("--http", action="store_true", help="streamable-http 模式（默认 stdio）")
    ap.add_argument("--port", type=int, default=8529)
    args = ap.parse_args()
    if not _MCP_OK:
        print("ERROR: 需要 fastmcp（pip install fastmcp）", file=sys.stderr)
        sys.exit(4)
    if args.http:
        mcp.run(transport="http", host="127.0.0.1", port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
