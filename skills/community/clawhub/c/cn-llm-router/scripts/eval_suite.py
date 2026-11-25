"""本地质量评测集执行与评分（v2.9.0 新增）。

本地评分器：关键词命中 + 要点覆盖，纯规则、零 LLM 依赖（符合 #9）。
题库 references/eval_suite.json（50 题，四类）。
四维得分表 + 轻量雷达图（SVG 内联，不复制 gateway 六维全家桶）。

评测执行通过注入的 call_fn(prompt, category) -> str 完成模型调用，
本模块负责打分与聚合，保持 CLI 轻、可离线测试。
"""

import os
import sys
import json
import concurrent.futures as _cf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml_simple

HERE = os.path.dirname(os.path.abspath(__file__))
SUITE_JSON = os.path.normpath(os.path.join(HERE, "..", "references", "eval_suite.json"))
SCORE_TABLE = os.path.normpath(os.path.join(HERE, "..", "references", "score_table.yaml"))

DIMENSIONS = ("code", "reason", "translate", "summarize")
DIM_NAMES = {"code": "代码", "reason": "推理", "translate": "翻译", "summarize": "摘要"}


def load_suite(path=None):
    path = path or SUITE_JSON
    if not os.path.exists(path):
        raise ValueError("评测题库不存在: %s" % path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def score_case(case, response):
    """单题本地评分（0-10）。

    = 关键词命中率(50%) + 要点覆盖率(50%)，要点用弱匹配（关键词子集命中）。
    """
    rubric = case.get("rubric", {})
    keywords = rubric.get("keywords", [])
    points = rubric.get("points", [])
    text = str(response or "").lower()

    kw_hit = 0
    for kw in keywords:
        if str(kw).lower() in text:
            kw_hit += 1
    kw_ratio = kw_hit / len(keywords) if keywords else 1.0

    pt_hit = 0
    for pt in points:
        # 要点命中：整句或其关键词有 ≥1 命中即算部分覆盖
        tokens = [t for t in str(pt).lower().replace("，", " ").replace("、", " ").split() if len(t) >= 2]
        # 中文要点无空格 → 用 2-gram 近似
        if len(tokens) < 2:
            s = str(pt).lower()
            grams = [s[i:i + 2] for i in range(0, max(1, len(s) - 1))]
            hit = sum(1 for g in grams if g in text)
            ratio = hit / len(grams) if grams else 0.0
        else:
            hit = sum(1 for t in tokens if t in text)
            ratio = hit / len(tokens)
        if ratio >= 0.5:
            pt_hit += 1
    pt_ratio = pt_hit / len(points) if points else 1.0

    return round((kw_ratio * 0.5 + pt_ratio * 0.5) * 10, 2)


def run_suite(call_fn, suite=None, models=None, max_workers=4, progress_cb=None):
    """跑评测集。

    call_fn(model, prompt, category) -> str：模型调用（由 CLI 注入）
    models: [{"provider":..., "model":...}, ...]；None 时用价格档案里前 N 个（dry 场景）
    返回 {"by_model": {model_key: {...}}, "details": [...]}
    """
    suite = suite or load_suite()
    cases = suite.get("cases", [])
    models = models or []
    if not models:
        return {"by_model": {}, "details": [], "error": "无参评模型"}

    tasks = []
    for m in models:
        mkey = "%s/%s" % (m["provider"], m["model"])
        for case in cases:
            tasks.append((mkey, m, case))

    detail_lock = __import__("threading").Lock()
    details = []

    def work(mkey, model, case):
        try:
            resp = call_fn(model["provider"], model["model"], case["prompt"], case["category"])
            score = score_case(case, resp)
            err = None
        except Exception as e:
            resp, score, err = "", 0.0, str(e)
        rec = {
            "model": mkey, "case_id": case["id"], "category": case["category"],
            "score": score, "error": err,
        }
        with detail_lock:
            details.append(rec)
            if progress_cb:
                progress_cb(len(details), len(tasks))
        return rec

    workers = max(1, min(int(max_workers), len(tasks) or 1))
    with _cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(work, *t) for t in tasks]
        for fut in _cf.as_completed(futures):
            fut.result()

    # 聚合：每模型四维平均分 + 总分
    by_model = {}
    for m in models:
        mkey = "%s/%s" % (m["provider"], m["model"])
        per_cat = {d: [] for d in DIMENSIONS}
        for rec in details:
            if rec["model"] == mkey and rec["category"] in per_cat:
                per_cat[rec["category"]].append(rec["score"])
        avg = {d: round(sum(v) / len(v), 2) if v else 0.0 for d, v in per_cat.items()}
        by_model[mkey] = {
            "provider": m["provider"], "model": m["model"],
            "scores": avg,
            "total": round(sum(avg.values()) / len(avg), 2),
            "cases": sum(len(v) for v in per_cat.values()),
        }
    return {
        "by_model": by_model, "details": details,
        "suite": suite.get("suite", "unknown"), "total_cases": len(cases),
    }


def render_table(result):
    """四维得分表（文本）。"""
    lines = []
    lines.append("📊 本地质量评测（%s，共 %d 题）" % (result["suite"], result["total_cases"]))
    header = "  %-24s %6s %6s %6s %6s %7s" % ("模型", "代码", "推理", "翻译", "摘要", "总分")
    lines.append(header)
    lines.append("  " + "-" * 64)
    for mkey, d in sorted(result["by_model"].items(), key=lambda x: -x[1]["total"]):
        s = d["scores"]
        lines.append("  %-24s %6.2f %6.2f %6.2f %6.2f %7.2f" % (
            mkey[:24], s["code"], s["reason"], s["translate"], s["summarize"], d["total"]))
    return "\n".join(lines)


def render_radar_svg(result):
    """轻量雷达图（内联 SVG，自绘，无第三方库）。每个模型一个多边形。"""
    dims = DIMENSIONS
    n = len(dims)
    cx, cy, r = 150, 140, 100
    import math

    def pt(i, val):
        ang = -math.pi / 2 + i * 2 * math.pi / n
        rr = r * (val / 10.0)
        return cx + rr * math.cos(ang), cy + rr * math.sin(ang)

    colors = ["#185FA5", "#534AB7", "#0F6E56", "#BA7517", "#D4537E"]
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="300" height="290" viewBox="0 0 300 290">']
    parts.append('<rect width="300" height="290" fill="#FFFFFF"/>')
    # 网格
    for lvl in (2, 4, 6, 8, 10):
        pts = " ".join("%.1f,%.1f" % pt(i, lvl) for i in range(n))
        parts.append('<polygon points="%s" fill="none" stroke="#E0E0E0" stroke-width="0.5"/>' % pts)
    for i in range(n):
        x, y = pt(i, 10)
        parts.append('<line x1="%d" y1="%d" x2="%.1f" y2="%.1f" stroke="#E0E0E0" stroke-width="0.5"/>' % (cx, cy, x, y))
        lx, ly = pt(i, 12)
        parts.append('<text x="%.1f" y="%.1f" font-size="11" fill="#444" text-anchor="middle" dominant-baseline="central">%s</text>' %
                     (lx, ly, DIM_NAMES[dims[i]]))
    # 模型多边形
    for idx, (mkey, d) in enumerate(sorted(result["by_model"].items(), key=lambda x: -x[1]["total"])[:5]):
        color = colors[idx % len(colors)]
        pts = " ".join("%.1f,%.1f" % pt(i, d["scores"][dims[i]]) for i in range(n))
        parts.append('<polygon points="%s" fill="%s" fill-opacity="0.12" stroke="%s" stroke-width="1.5"/>' % (pts, color, color))
    # 图例
    for idx, (mkey, d) in enumerate(sorted(result["by_model"].items(), key=lambda x: -x[1]["total"])[:5]):
        color = colors[idx % len(colors)]
        y = 258 + (idx % 2) * 14
        x = 20 + (idx // 2) * 145
        parts.append('<rect x="%d" y="%d" width="9" height="9" fill="%s"/>' % (x, y, color))
        parts.append('<text x="%d" y="%d" font-size="10" fill="#444">%s</text>' % (x + 13, y + 8, mkey[:18]))
    parts.append("</svg>")
    return "\n".join(parts)


def save_radar_svg(result, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_radar_svg(result))
    return path


def load_score_table(path=None):
    path = path or SCORE_TABLE
    if not os.path.exists(path):
        return {"provider_scores": {}}
    data = yaml_simple.load_file(path)
    return data if isinstance(data, dict) else {"provider_scores": {}}


def save_score_table(result, path=None):
    """把评测结果写入个性化评分表（本地实测回填）。"""
    path = path or SCORE_TABLE
    table = load_score_table(path)
    scores = table.setdefault("provider_scores", {})
    from datetime import date
    today = date.today().isoformat()
    for mkey, d in result["by_model"].items():
        # mkey = provider/model，用完整名作 key 避免重名
        scores[mkey] = {
            "provider": d["provider"], "model": d["model"],
            **{dim: d["scores"][dim] for dim in DIMENSIONS},
            "total": d["total"], "eval_date": today, "cases": d["cases"],
        }
    yaml_simple.dump_file(path, table)
    return path


def compare_report(current, history):
    """生成历史对比：新模型/新版本值不值得换。

    current: run_suite 的 result；history: eval_store 的历史记录列表。
    返回文本对比报告。
    """
    lines = ["📈 评测历史对比报告"]
    if not history:
        lines.append("  暂无历史基线，本次结果已作为基线存档。")
        return "\n".join(lines)
    lines.append("  %-24s %8s %8s %8s" % ("模型", "本次总分", "历史最佳", "变化"))
    lines.append("  " + "-" * 52)
    for mkey, d in sorted(current["by_model"].items(), key=lambda x: -x[1]["total"]):
        past = [h for h in history if h.get("model") == mkey]
        best = max((h.get("total", 0) for h in past), default=None)
        if best is None:
            lines.append("  %-24s %8.2f %8s %8s" % (mkey[:24], d["total"], "-", "新"))
        else:
            delta = d["total"] - best
            tag = "↑+%.2f" % delta if delta > 0 else ("↓%.2f" % delta if delta < 0 else "持平")
            lines.append("  %-24s %8.2f %8.2f %8s" % (mkey[:24], d["total"], best, tag))
    return "\n".join(lines)
