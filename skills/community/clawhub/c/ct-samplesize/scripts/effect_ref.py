#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
effect_ref.py — ct-samplesize 公开证据效应量参考基线（路线 A MVP）

思路来源：CODEX「按适应症 benchmark 效应量 → 标定样本量假设」的设计期前馈。
实现红线（2026-10-14 与用户确认）：
  - 数据仅来自公开已发表荟萃（用户自带 --effect-ref 或策展库），绝不连接商业策展数据库；
  - 默认只展示、绝不静默代入；采纳必须 --adopt-ref 显式指定，且来源写入输出（可审计）；
  - 纯标准库，不触碰数值真相源（coze R）；采纳仅改写本地 args，正式计算仍走既有链路；
  - 效应量尺度不符（参考是 HR、当前是连续终点等）拒绝采纳，只允许展示。

参考文件 schema（与 meta-analysis 技能 benchmark_reference 四元组互认，并扩展 param/scale）：
{
  "ta": "NSCLC",                  // 适应症（信息性）
  "endpoint": "ORR",              // 终点（信息性）
  "as_of": "2026-10-14",          // 策展日期（>3 年提示复查）
  "references": [
    {"param": "effect",           // 可采纳的目标参数：effect / hazard_ratio / odds_ratio / risk_ratio
     "scale": "d",                // 效应量尺度：d | MD | SMD（effect）；HR；OR；RR
     "estimate": 0.35, "ci_low": 0.22, "ci_high": 0.48,
     "n": 3204,                   // 参考 MA 总样本量（可选）
     "source": "Cochrane 2021, Smith et al.",   // 必填
     "pmid": "12345678"}          // 可选
  ]
}

与 ma_extractor.py（路线 C）的互认：抽取器产出的 HR/OR/RR/SMD/MD 候选
（param=hazard_ratio/odds_ratio/risk_ratio/effect）经人工 --confirm 入库后，
本模块 validate 全盘接受；OR/RR 为比值型（零假设=1，估计与 CI 须为正），
SMD 与 d 数值等价（同一尺度两种写法）。
"""

import json
import sys
from datetime import date

# 可采纳的目标参数 → （零假设值, 说明）
# effect 服务 ttest/ANOVA/meta_planning 连续终点；hazard_ratio 服务生存终点；
# odds_ratio / risk_ratio 服务比值型检验（ci_or/ci_rr/regression_*/rates_ext，
# 其比值经 CLI --effect 传入，引擎读 params$effect —— 见 TARGET_ARG）。
# p1/p2、margin 等涉及试验特异性设定（基线率、临床判定界值），不开放基准采纳。
ADOPTABLE_PARAMS = {
    "effect": {"null": 0.0, "desc": "效应量（Cohen's d / SMD / 原始均差）"},
    "hazard_ratio": {"null": 1.0, "desc": "风险比 HR"},
    "odds_ratio": {"null": 1.0, "desc": "比值比 OR"},
    "risk_ratio": {"null": 1.0, "desc": "风险比 RR"},
}

# 比值型参数：估计与 CI 须严格为正；CI 排除零假设（1）方可作设计假设
RATIO_PARAMS = ("hazard_ratio", "odds_ratio", "risk_ratio")

# param → 允许的 scale（SMD 与 d 数值等价；ma_extractor 的 SMD 候选据此入库）
PARAM_SCALES = {
    "effect": ("d", "MD", "SMD"),
    "hazard_ratio": ("HR",),
    "odds_ratio": ("OR",),
    "risk_ratio": ("RR",),
}

# param → 允许的 test 前缀（保守白名单；前缀匹配，大小写不敏感）
TEST_PREFIX = {
    "effect": ("ttest", "anova", "meta_planning"),
    "hazard_ratio": ("survival", "cox", "ni_survival", "gsd_survival",
                     "gsd_hazard", "competing", "recurrent"),
    "odds_ratio": ("ci_or", "regression_logistic"),
    "risk_ratio": ("ci_rr", "regression_poisson", "rates_ext"),
}

# param → 采纳时落地的 CLI 参数名（setattr 目标）。
# ci_or/ci_rr/regression_logistic/regression_poisson/rates_ext 的引擎分支均读
# params$effect 作为 OR/RR/率比值（run_task.R:2261/2277/2398/2419/2421），
# 故 OR/RR 参考采纳后写入 --effect，而非不存在的 --or/--rr。
TARGET_ARG = {
    "effect": "effect",
    "hazard_ratio": "hazard_ratio",
    "odds_ratio": "effect",
    "risk_ratio": "effect",
}

STALE_YEARS = 3  # as_of 超过该年限提示复查


def load_ref(path):
    """读取参考 JSON；返回 (data, err_msg)。"""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return None, "参考文件读取失败：%s" % e
    if not isinstance(data, dict) or not data.get("references"):
        return None, "参考文件缺少非空 references 数组"
    if not isinstance(data["references"], list):
        return None, "references 须为数组"
    return data, None


def validate(data):
    """校验每条参考记录；返回 (clean_refs, errors, warnings)。

    比值型参数（HR/OR/RR）额外要求估计与 CI 严格为正；CI 跨越零假设值
    （effect: 0；比值: 1）的记录打 `_crosses_null` 标记并告警——其效应量
    可能为 0 或反向，不能作为设计假设（pick 时硬拒绝）。
    """
    errors, warnings, clean = [], [], []
    for i, r in enumerate(data["references"]):
        tag = "reference[%d]" % i
        if not isinstance(r, dict):
            errors.append("%s: 须为对象" % tag)
            continue
        param = r.get("param")
        if param not in ADOPTABLE_PARAMS:
            errors.append("%s: param 须为 %s（其余参数涉及试验特异设定，不开放基准采纳）"
                          % (tag, "/".join(ADOPTABLE_PARAMS)))
            continue
        scale = r.get("scale")
        if scale not in PARAM_SCALES[param]:
            errors.append("%s: %s 的 scale 须为 %s"
                          % (tag, param, "/".join(PARAM_SCALES[param])))
            continue
        est, lo, hi = r.get("estimate"), r.get("ci_low"), r.get("ci_high")
        for k, v in (("estimate", est), ("ci_low", lo), ("ci_high", hi)):
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                errors.append("%s: %s 缺失或非数值" % (tag, k))
        if errors and errors[-1].startswith(tag):
            continue
        if not lo < hi:
            errors.append("%s: ci_low(%s) 须小于 ci_high(%s)" % (tag, lo, hi))
            continue
        if not (lo <= est <= hi):
            errors.append("%s: estimate(%s) 须落在参考 CI 内" % (tag, est))
            continue
        if param in RATIO_PARAMS and (est <= 0 or lo <= 0):
            errors.append("%s: %s 为比值型参数，estimate/ci_low 须严格为正（收到 est=%s, ci_low=%s）"
                          % (tag, param, est, lo))
            continue
        if not (r.get("source") or "").strip():
            errors.append("%s: source 必填（公开文献出处）" % tag)
            continue
        rr = dict(r)
        rr["_index"] = i
        null = ADOPTABLE_PARAMS[param]["null"]
        if lo <= null <= hi:
            rr["_crosses_null"] = True
            warnings.append("%s: CI[%s, %s] 跨越零假设值 %s（统计不显著）——"
                            "仅作展示，不能作为设计假设采纳" % (tag, lo, hi, null))
        as_of = rr.get("as_of") or data.get("as_of")
        if as_of:
            try:
                y, m, d = (int(x) for x in str(as_of).split("-"))
                age = (date.today() - date(y, m, d)).days / 365.25
                if age > STALE_YEARS:
                    rr["_stale"] = True
                    warnings.append("%s: as_of=%s 已超 %d 年，建议复查是否有更新荟萃"
                                    % (tag, as_of, STALE_YEARS))
            except Exception:
                warnings.append("%s: as_of 格式无法解析（期望 YYYY-MM-DD）" % tag)
        clean.append(rr)
    return clean, errors, warnings


def compatible(ref, test, args):
    """尺度/终点兼容性检查；返回 (ok, reason)。"""
    param = ref["param"]
    prefixes = TEST_PREFIX[param]
    t = (test or "").lower()
    if prefixes and not any(t.startswith(p) for p in prefixes):
        return False, ("参考 param=%s（%s）与当前 test=%s 的终点类型不符，拒绝采纳"
                       % (param, ADOPTABLE_PARAMS[param]["desc"], test))
    if param == "effect" and ref.get("scale") == "MD" and not getattr(args, "sd", None):
        return False, "参考为原始均差（MD），当前未提供 --sd，无法折算 Cohen's d，拒绝采纳"
    return True, ""


def _median(ests):
    s = sorted(ests)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def summarize(refs):
    """参考分布汇总：按 param 分组统计（混 param 文件不跨尺度聚合）+ 来源清单。

    顶层 min/median/max 仅在单一 param 时有意义（保持旧消费方兼容）；
    混 param 场景请用 by_param。
    """
    ests = [r["estimate"] for r in refs]
    by_param = {}
    for r in refs:
        g = by_param.setdefault(r["param"], {"n_sources": 0, "estimates": []})
        g["n_sources"] += 1
        g["estimates"].append(r["estimate"])
    for p, g in by_param.items():
        e = g.pop("estimates")
        g["estimate_min"], g["estimate_max"] = min(e), max(e)
        g["estimate_median"] = round(_median(e), 6)
        g["null"] = ADOPTABLE_PARAMS[p]["null"]
    return {
        "n_sources": len(ests),
        "estimate_min": min(ests),
        "estimate_median": round(_median(ests), 6),
        "estimate_max": max(ests),
        "by_param": by_param,
        "mixed_param": len(by_param) > 1,
        "stale_count": sum(1 for r in refs if r.get("_stale")),
        "crosses_null_count": sum(1 for r in refs if r.get("_crosses_null")),
        "sources": [{"index": r["_index"], "source": r["source"],
                     "param": r["param"], "scale": r["scale"],
                     "estimate": r["estimate"],
                     "ci": [r["ci_low"], r["ci_high"]],
                     "n": r.get("n"), "pmid": r.get("pmid"),
                     "as_of": r.get("as_of"),
                     "stale": bool(r.get("_stale")),
                     "crosses_null": bool(r.get("_crosses_null"))} for r in refs],
    }


def pick(refs, choice):
    """按 --adopt-ref 选择采纳值；返回 (adopted_dict, err_msg)。

    choice ∈ {median, conservative, low, high, <index>}
    conservative = 参考 CI 中最接近零假设的界（对样本量最不利）：
      effect 的零假设为 0，比值型（HR/OR/RR）为 1。

    护栏（2026-10-16 审查补）：
      1. 聚合选择（median/conservative/low/high）拒绝混 (param, scale) 文件——
         d 与 HR 不可跨尺度平均；d 与 MD 同 param 但尺度不同（标准化 vs 原始），
         同样不可混算；
      2. CI 跨越零假设的参考不得采纳（效应量可能为 0 或反向，代入即
         "拍脑袋假设"）：聚合选择先剔除再统计（basis 标注剔除数），
         显式 <index> 单选到跨零参考则硬拒绝；全部不合格报错；
      3. <index> 单选混 param 文件时，以所选来源自身的 param/scale 为准
         （不沿用 refs[0]，避免 param 错位）。
    """
    param = refs[0]["param"]
    null = ADOPTABLE_PARAMS[param]["null"]

    def _clean_only(cands, what):
        """聚合入口：剔除跨零参考；无剩余则报错。"""
        clean = [r for r in cands if not r.get("_crosses_null")]
        if not clean:
            names = ", ".join("[%d] CI[%s, %s]" % (r["_index"], r["ci_low"], r["ci_high"])
                              for r in cands)
            return None, ("%s：全部 %d 条参考的 CI 均跨越零假设值 %s（统计不显著），"
                          "拒绝采纳：%s" % (what, len(cands), null, names))
        return clean, None

    def _single(idx, what):
        match = [r for r in refs if r["_index"] == idx]
        if not match:
            return None, "来源序号 %d 不存在" % idx
        r = match[0]
        rnull = ADOPTABLE_PARAMS[r["param"]]["null"]
        if r.get("_crosses_null"):
            return None, ("%s：来源 [%d] 的 CI[%s, %s] 跨越零假设值 %s（统计不显著），"
                          "拒绝采纳；请改用显著来源"
                          % (what, idx, r["ci_low"], r["ci_high"], rnull))
        return r, None

    if choice in ("median", "conservative", "low", "high"):
        # 聚合守卫：单 (param, scale) 才能平均/取极值——
        # d 与 HR 不可混算；d 与 MD 同 param 但尺度不同（标准化 vs 原始），亦不可混算
        scales = {(r["param"], r["scale"]) for r in refs}
        if len(scales) > 1:
            return None, ("参考文件混用多种 param/scale（%s），%s 聚合无意义；"
                          "请拆分为单 param+scale 文件，或用 <index> 指定单一来源"
                          % ("; ".join("%s/%s" % ps for ps in sorted(scales)), choice))
        cands, err = _clean_only(refs, choice)
        if err:
            return None, err
        excluded = len(refs) - len(cands)
        chosen_scale = refs[0].get("scale")

    if choice == "median":
        s = summarize(cands)
        val = s["estimate_median"]
        basis = "median of %d public sources" % s["n_sources"]
        if excluded:
            basis += " (%d crossing-null excluded)" % excluded
        src = "; ".join(r["source"] for r in cands)
    elif choice == "conservative":
        best = min(cands, key=lambda r: min(abs(r["ci_low"] - null), abs(r["ci_high"] - null)))
        val = best["ci_low"] if abs(best["ci_low"] - null) <= abs(best["ci_high"] - null) else best["ci_high"]
        basis = "conservative CI bound (closest to null=%s)" % null
        if excluded:
            basis += " (%d crossing-null excluded)" % excluded
        src = best["source"]
    elif choice == "low":
        best = min(cands, key=lambda r: r["estimate"])
        val, basis, src = best["estimate"], "lowest estimate", best["source"]
        if excluded:
            basis += " (%d crossing-null excluded)" % excluded
    elif choice == "high":
        best = max(cands, key=lambda r: r["estimate"])
        val, basis, src = best["estimate"], "highest estimate", best["source"]
        if excluded:
            basis += " (%d crossing-null excluded)" % excluded
    else:
        try:
            idx = int(choice)
        except ValueError:
            return None, "adopt 选择须为 median/conservative/low/high 或来源序号，收到：%r" % choice
        best, err = _single(idx, "来源 #%d" % idx)
        if err:
            return None, err
        # 混 param 文件按 index 单选：以所选来源自身的 param/scale 为准
        #（不可沿用 refs[0]，否则 index 选到第二条时 param 错位）
        param = best["param"]
        chosen_scale = best.get("scale")
        val, basis, src = best["estimate"], "source #%d" % idx, best["source"]
    return {"param": param, "value": val, "scale": chosen_scale,
            "source": src, "basis": basis, "adopted": True}, None


DISCLAIMER = ("公开参考 ≠ 本试验假设：人群/终点/效应量尺度须可比；"
              "数据仅来自公开已发表荟萃，非任何商业策展数据库。")


def render(ref_data, summary, adopted, warnings):
    """控制台参考清单（展示段）。"""
    lines = []
    lines.append("-" * 60)
    lines.append("公开证据效应量参考（display-only，默认不代入）")
    lines.append("-" * 60)
    lines.append("TA/终点: %s / %s" % (ref_data.get("ta", "-"), ref_data.get("endpoint", "-")))
    for w in warnings:
        lines.append("  ⚠ %s" % w)
    if summary.get("mixed_param"):
        for p, g in summary["by_param"].items():
            lines.append("汇总[%s]: %d 条来源, estimate ∈ [%s, %s], median=%s（零假设 %s）"
                         % (p, g["n_sources"], g["estimate_min"],
                            g["estimate_max"], g["estimate_median"], g["null"]))
    else:
        lines.append("汇总: %d 条来源, estimate ∈ [%s, %s], median=%s"
                     % (summary["n_sources"], summary["estimate_min"],
                        summary["estimate_max"], summary["estimate_median"]))
    for s in summary["sources"]:
        stale = " [>3年，建议复查]" if s.get("stale") else ""
        cross = " [CI跨零假设，不可采纳]" if s.get("crosses_null") else ""
        lines.append("  [%d] %s %s=%s CI[%s, %s] (%s)%s%s"
                     % (s["index"], s["param"], s["scale"], s["estimate"], s["ci"][0], s["ci"][1],
                        s["source"], stale, cross))
    if adopted:
        lines.append("已采纳（--adopt-ref）: %s=%s（%s；来源: %s）"
                     % (adopted["param"], adopted["value"], adopted["basis"], adopted["source"]))
    else:
        lines.append("未采纳。如需代入请显式 --adopt-ref median|conservative|low|high|<index>")
    lines.append("声明: %s" % DISCLAIMER)
    return "\n".join(lines)


def _main():
    """独立冒烟入口：effect_ref.py <ref.json> [--adopt median]"""
    import argparse
    ap = argparse.ArgumentParser(description="公开效应量参考文件校验/汇总（MVP）")
    ap.add_argument("ref", help="参考 JSON 路径")
    ap.add_argument("--adopt", default=None)
    ap.add_argument("--test", default=None)
    a = ap.parse_args()
    data, err = load_ref(a.ref)
    if err:
        print(err, file=sys.stderr)
        return 1
    refs, errors, warnings = validate(data)
    if errors:
        for e in errors:
            print("✗ " + e, file=sys.stderr)
        return 1
    summary = summarize(refs)
    adopted = None
    if a.adopt:
        adopted, perr = pick(refs, a.adopt)
        if perr:
            print(perr, file=sys.stderr)
            return 1
        if a.test:
            ok, reason = compatible(adopted, a.test, type("A", (), {"sd": None})())
            if not ok:
                print(reason, file=sys.stderr)
                return 1
    print(render(data, summary, adopted, warnings))
    print(json.dumps({"summary": summary, "adopted": adopted},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
