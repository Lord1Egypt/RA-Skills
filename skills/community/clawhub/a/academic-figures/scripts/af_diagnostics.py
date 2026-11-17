# -*- coding: utf-8 -*-
"""异常兜底诊断系统（v3.0.0 自 gen_figure.py 拆出；行为完全一致）。
分级退出码（3 数据/4 环境/6 内存）、中文三段式诊断、字段名近似匹配纠错。"""
import os
import sys

# ── 分级退出码（v2.8 定义，v2.10 拆出）──────────────────────────────────
# 退出码：0 成功；1 参数/校验致命错；2 --verify 重叠与批量部分失败（历史语义不变）；
# 3 数据或格式错误；4 环境或依赖错误；5 看门狗超时；6 内存护栏拒绝（降级重试仍败）。
_EXIT_DATA_CLASSES = {
    "ValueError", "KeyError", "IndexError", "TypeError", "AttributeError",
    "ZeroDivisionError", "OverflowError", "ArithmeticError",
    "FileNotFoundError", "IsADirectoryError", "JSONDecodeError",
    "UnicodeDecodeError", "UnicodeError", "BadZipFile", "LinAlgError",
}
_EXIT_ENV_CLASSES = {
    "ImportError", "ModuleNotFoundError", "OSError", "PermissionError",
    "NotADirectoryError", "SubprocessError", "TimeoutExpired",
    "RuntimeError", "NotImplementedError",
}


def _classify_exit_code(e):
    """v3 兜底路径的退出码分类：数据侧=3、环境侧=4、内存=6、其余=2（历史语义）。"""
    try:
        cls = type(e).__name__
        if cls == "MemoryError":
            return 6
        cands = {cls}
        mod = type(e).__module__
        if mod and mod != "builtins":
            cands.add(f"{mod}.{cls}")
        if cands & _EXIT_ENV_CLASSES:
            return 4
        if cands & _EXIT_DATA_CLASSES:
            return 3
    except Exception:
        pass
    return 2



# ── A2(v2.7)：异常兜底 v3 —— 任何未知异常都输出「中文诊断 + 原文 + 针对性建议」──
_EXC_ZH_V3 = {
    "MemoryError": ("内存不足", "数据量超出可用内存：减少行数/列数（热图先聚合行、散点抽样），"
                    "或关闭其他占内存的程序后重试"),
    "KeyError": ("缺少所需的数据字段", "对照 --explain <图型> 核对数据字段名；"
                 "字段名大小写和下划线必须完全一致"),
    "IndexError": ("索引越界", "数据某行/列长度与其他行不一致（常见于手工编辑的表格），"
                   "逐行检查列数是否一致"),
    "ValueError": ("数值或格式不符合要求", "检查数据中是否有非数字内容、空值或格式错误"),
    "TypeError": ("数据类型不匹配", "检查是否把文本传给了需要数值的参数，或数组成员类型混用"),
    "AttributeError": ("对象缺少所需属性", "多为数据结构与图型要求不符：对照 --explain <图型> 核对"),
    "ZeroDivisionError": ("除零错误", "数据中存在全为相同值/全 0 的列或组，导致统计量无法计算"),
    "LinAlgError": ("矩阵奇异/不可解", "协变量或特征列之间存在完全线性相关，移除冗余列后重试"),
    "FileNotFoundError": ("文件不存在", "核对 --data 路径拼写；相对路径以当前工作目录为基准"),
    "PermissionError": ("文件权限不足", "输出目录可能只读或文件被占用：换一个可写目录，"
                        "或关闭正在查看该文件的程序"),
    "IsADirectoryError": ("给的是目录不是文件", "--data 需要指向具体文件"),
    "JSONDecodeError": ("JSON 语法错误", "检查引号/逗号/括号是否成对；可用任意 JSON 校验器先验证"),
    "UnicodeDecodeError": ("文件编码不是 UTF-8", "用编辑器把文件另存为 UTF-8（勿用 GBK/ANSI）"),
    "Error": ("CSV 格式错误", "常见原因：字段内含未转义引号、行内逗号数不一致"),
    "BadZipFile": ("文件不是有效的压缩/xlsx 格式", "xlsx 可能实为改名的 html/csv，"
                   "请用 Excel 另存为标准 xlsx"),
    "TimeoutError": ("操作超时", "渲染超时：数据过大先瘦身，或用 --timeout 600 调大预算"
                    "（--timeout 0 禁用看门狗）"),
    "ImportError": ("缺少依赖库（环境侧，退出码 4）", "按报错里的库名 pip install 即可；"
                   "核心图型仅需 matplotlib/numpy/scipy/pillow"),
    "ModuleNotFoundError": ("缺少依赖库（环境侧，退出码 4）", "按报错里的库名 pip install；"
                           "注意装到与运行时相同的 Python 环境"),
    "OSError": ("系统输入/输出错误（环境侧，退出码 4）", "常见于磁盘满、文件被占用、"
               "路径不可写：换目录或关闭占用程序后重试"),
    "TimeoutExpired": ("子进程超时", "外部命令（如字体探测）未按时返回；重跑一次通常可恢复"),
    "NotImplementedError": ("该场景暂不支持", "多为图型不支持的参数组合：对照 --explain <图型>"
                           " 核对用法"),
    "RuntimeError": ("运行时错误", "多为渲染内核的边界情况：换数据重试可定位是否数据触发"),
    "OverflowError": ("数值溢出", "数据中存在极端值（如 1e300 或 -log10(0)=inf），先清理极端值"),
}

_DIAG_PATTERNS = [
    (r"could not convert string to float", "数据列混入了非数字文本（如单位、百分号、全角数字）",
     "去掉单位与说明文字，数字一律半角；「3.5±0.2」请拆成均值与误差两列"),
    (r"nan|missing|NaN", "数据中存在缺失值（NaN）",
     "先删除含缺失值的行/列，或填入合理数值后再提交"),
    (r"inhomogeneous|ragged", "嵌套数组的各行长度不一致（锯齿数据）",
     "逐行核对元素个数，短的行需补齐或删除"),
    (r"shape mismatch|broadcast", "各列/各组的长度不一致",
     "同一图内各组数据点数必须与标签数对齐，逐列核对长度"),
    (r"Expecting value|Expecting .* delimiter|Invalid control character", "JSON 语法错误",
     "检查最近一次编辑处的引号/逗号/括号；字符串必须用双引号"),
    (r"out of bounds|out of range|index .* is out of", "引用了不存在的位置",
     "通常是 pos 超出 layout 网格，或 risk-times 超出随访时间范围"),
    (r"Font family|findfont|font", "字体不可用",
     "中文字体缺失时运行 setup_env.py 自动检测；或改用 --no-cjk"),
    (r"Permission denied", "权限不足", "换可写目录或关闭占用文件的程序"),
    (r"No such file", "文件/路径不存在", "核对路径拼写与工作目录"),
    (r"Singular matrix|LinAlg", "矩阵奇异", "存在完全线性相关的列，移除冗余列"),
    (r"invalid literal for int", "把非整数文本当整数解析", "该列改为数值（如 1/2/3），勿留文字"),
    (r"exactly one of|required positional", "命令行参数缺失或冲突", "用 --help 查看该子命令必填项"),
    (r"No module named", "缺少依赖库（Python 找不到该模块，退出码 4）",
     "按报错里的模块名 pip install 安装后重试；确认装进运行时同一 Python 环境"),
    (r"exec format error|cannot execute", "外部命令无法执行", "检查依赖程序是否安装、架构是否匹配"),
]


_KNOWN_DATA_FIELDS = [
    "labels", "series", "errors", "significance", "groups", "matrix",
    "comparisons",
    "row_labels", "col_labels", "rows", "cols", "x_labels", "y_labels",
    "time", "event", "group", "fpr", "tpr", "scores", "name",
    "sets", "counts", "areas", "studies", "effect", "se", "lower", "upper",
    "panels", "layout", "values", "data", "x", "y", "category", "value",
  "log2fc", "pvalue", "names", "fc_cut", "p_cut", "top", "items", "left", "right", "left_ylabel", "right_ylabel", "left_errors", "right_errors", "left_type", "right_type", "left_label", "right_label", "x_label", "y_label", "sets", "methods", "before", "after", "curves", "groups", "matrix", "ref_line", "median_survival", "overall", "studies_included", "duplicates_removed", "records_screened", "reports_sought", "reports_not_retrieved", "reports_assessed", "exclusion_reasons", "arrows",
  "title", "top_n", "min_size", "sort", "panel_labels", "span", "pos", "hero_panel", "xlabel", "ylabel", "type",
  "change", "pr_cut", "pd_cut",
  "datasets", "jitter", "cloud_scale",
  "start", "end", "milestones", "ongoing", "ref_lines",
  "from", "to", "from_label", "to_label", "show_values", "show_gap",
  "predicted", "observed", "bins", "ci_lo", "ci_hi", "hl_p", "smooth",
  "thresholds", "models", "net_benefit", "prevalence", "treat_all", "show_none",
  "variables", "outcome_scales", "total_points_max", "ticks", "points_at",
  "points", "est", "ci_lo", "ci_hi", "ref", "log_y", "hline_at", "hist", "benefit_shade",
  "subgroups", "levels", "p_interaction", "p", "overall", "est_label", "log_x",
  "arcs", "share_y",
  "cause_labels", "compare_km", "percent", "time_unit", "y_max",
  "domains", "judgements",
  # v7.9.0 AF21/AF4：补注册被假警告误伤的合法键（prisma 校验器必收键+lang、km log_rank/risk_table、labbe events_t——
  # 原 "title" 与 "events_t" 间缺逗号致相邻字面量拼接成 "titleevents_t"，events_t 实际未注册）
  "records_identified", "records_excluded", "reports_excluded", "lang",
  "log_rank", "risk_table",
  "events_t", "n_t", "events_c", "n_c", "est_measure", "show_labels",
]


def _is_validation_error(e):
    """v7.9.0 AF10：校验类错误判定——ValueError 且消息符合引擎「<图型>: 」前缀约定。
    校验类错误的原因已在消息里精确到字段/数值（如 volcano: fc_cut=0 不满足 fc_cut>0），
    错误包装首行应直用精确原因，不再叠加瞬态重试/AF_DEBUG 等无关建议。"""
    import re as _re
    _m = str(e) or ""
    return (type(e).__name__ == "ValueError"
            and (bool(_re.match(r"^[a-z_]{2,24}: ", _m)) or "校验失败" in _m))


def _diagnose_exception(e):
    """v3 兜底诊断：返回 (中文诊断, 原文, [建议1, 建议2, 建议3])。本函数自身永不抛异常。"""
    try:
        cls = type(e).__name__
        qual = f"{type(e).__module__}.{cls}"
        zh, why = "未知类型的错误", ""
        for key, (z2, w2) in _EXC_ZH_V3.items():
            if cls == key or qual == key or qual.endswith("." + key):
                zh, why = z2, w2
                break
        tips = []
        # v2.9：KeyError 字段名近似匹配（JSON 字段拼写错误给中文纠错提示）
        if cls == "KeyError" and getattr(e, "args", None) \
                and isinstance(e.args[0], str) and e.args[0]:
            import difflib as _dif
            _near = _dif.get_close_matches(e.args[0], _KNOWN_DATA_FIELDS, n=2, cutoff=0.6)
            if _near:
                tips.append(f"字段名 {e.args[0]} 未识别——最接近的合法字段：{_near}"
                            "（大小写与下划线必须完全一致）")
        for pat, diag, tip in _DIAG_PATTERNS:
            import re as _re
            if _re.search(pat, str(e) or "", _re.I):
                tips.append(f"{diag}——{tip}")
                if len(tips) >= 2:
                    break
        if why:
            tips.append(why)
        # v7.9.0 AF10：校验类错误首行=精确原因（消息自带字段/实值），不再叠加
        # 模式匹配/瞬态重试等建议（精确消息本身就是最短修复路径）
        if _is_validation_error(e):
            return str(e).strip(), f"{qual}: {e}", []
        tips.append("瞬态失败（超时/内存）会自动重试（--retries）；"
                      "反复失败请核对数据与参数")
        return zh, f"{qual}: {e}", tips[:3]
    except Exception:
        return "未知错误", repr(e), ["重试一次", "核对数据格式", "见文档 FAQ"]


def _print_v3_error(e):
    zh, orig, tips = _diagnose_exception(e)
    print(f"ERROR: 渲染失败——{zh}", file=sys.stderr)
    print(f"└ 原始错误（保留可搜索）：{orig}", file=sys.stderr)
    for i, t in enumerate(tips, 1):
        print(f"建议{i}: {t}", file=sys.stderr)
    if not _is_validation_error(e):  # v7.9.0 AF10：校验类错误不引导 AF_DEBUG（原因已精确）
        print("仍失败：AF_DEBUG=1 重跑可输出完整技术细节（反馈问题时请附上）", file=sys.stderr)




def doctor_composite_shared_scale(data, print_fn=None):
    """v5.4 --doctor 规则：组合图「同变量跨面板」尺度一致性预检——
    ≥2 个面板 y 轴标签相同（同变量语义）而数值范围差异 >5 倍时提示：
    审稿人会视为两回事/或应共享尺度（pitfalls 配色跨面板一致性规则的孪生）。
    返回提示数（0=通过）。print_fn 注入 stderr 打印。"""
    out = print_fn or (lambda s: None)
    n = 0
    panels = data.get("panels") if isinstance(data, dict) else None
    if not (isinstance(panels, list) and len(panels) >= 2):
        return 0
    by_ylabel = {}
    for p in panels:
        if not isinstance(p, dict):
            continue
        d = p.get("data") if isinstance(p.get("data"), dict) else p
        # v5.6 修复：ylabel 在 composite schema 里是面板级字段（data-formats.md），
        # 旧实现只读 panel.data.ylabel——标准数据上预检从未生效；两级都查。
        yl = str(p.get("y_label") or p.get("ylabel")
                 or d.get("y_label") or d.get("ylabel") or "")
        if not yl:
            continue
        rng = None
        for key in ("series", "datasets", "groups"):
            obj = d.get(key)
            if isinstance(obj, dict) and obj:
                vals = [v for row in obj.values() if isinstance(row, list)
                        for v in row
                        if isinstance(v, (int, float)) and not isinstance(v, bool)]
                if len(vals) >= 2:
                    lo, hi = min(vals), max(vals)
                    rng = (abs(lo) + abs(hi)) / 2 or abs(hi) or 1.0
                    span = (hi - lo) or 1.0
                    rng = max(abs(span), abs(hi))
                break
        if rng is not None:
            by_ylabel.setdefault(yl, []).append(rng)
    for yl, rngs in by_ylabel.items():
        if len(rngs) >= 2 and max(rngs) / max(min(rngs), 1e-12) > 5:
            out(f"[doctor] 面板间「{yl}」数值范围相差 "
                f"{max(rngs) / max(min(rngs), 1e-12):.0f} 倍——同变量跨面板请共享"
                f"同一 y 尺度（composite 数据加 \"share_y\": true 可自动统一；"
                f"或改用不同轴标签区分不同变量）")
            n += 1
    return n


def write_debug_report(args, exc, out_path):
    """--debug：渲染失败时的结构化诊断侧车（<output>.debug.json，v6.4.0）。

    供调用方（agent/脚本）程序化排障：输入指纹/字段映射（含未知字段名单）/
    异常分类与修复建议/重试代数。成功渲染不产出；失败但未加 --debug 也不产出。
    """
    import hashlib
    import json as _json
    rep = {"schema": "af-debug/1", "chart_type": getattr(args, "type", None),
           "output": getattr(args, "out", None)}
    data_path = getattr(args, "data", None)
    if data_path and os.path.exists(data_path):
        raw = open(data_path, "rb").read()
        rep["input"] = {"path": data_path, "size_bytes": len(raw),
                        "sha256_12": hashlib.sha256(raw).hexdigest()[:12]}
        try:
            parsed = _json.loads(raw)
            if isinstance(parsed, dict):
                keys = list(parsed.keys())
                rep["fields_seen"] = keys
                rep["fields_unknown"] = [k for k in keys if k not in _KNOWN_DATA_FIELDS]
        except Exception:
            rep["input"]["format"] = "non-JSON (CSV/Excel passed through)"
    rep["exception"] = {"type": type(exc).__name__, "message": str(exc)[:300]}
    try:
        zh, _orig, tips = _diagnose_exception(exc)
        rep["diagnosis"] = {"summary": zh, "suggestions": tips}
    except Exception:
        pass
    rep["retries_attempted"] = int(os.environ.get("AF_RETRY_N", "0") or 0)
    target = (out_path or "figure") + ".debug.json"
    with open(target, "w", encoding="utf-8") as f:
        _json.dump(rep, f, ensure_ascii=False, indent=1)
    print(f"DEBUG: 诊断侧车已写 {target}", file=sys.stderr)
    return target
