"""召回缺口识别引擎：影响面分析的召回补强、漏报原因分类与预测验证。

设计动机：向量语义匹配存在阈值性漏召（如消费方命中但定义方未命中）。
用确定性信号补强召回（路由供需闭包 + 需求路由关键词硬匹配），
并在 sync 时用实际变更验证预测，漏报按原因分类，驱动「识别缺口 → 回补能力」闭环。
"""
import hashlib
import json
import re
from datetime import datetime

from .module_detail_analyzer import CN_TO_EN_KEYWORDS


def hashes_fp(hashes: dict) -> str:
    """模块哈希指纹：判定 sync 时的基线是否仍是预测时的基线。"""
    return hashlib.sha256(json.dumps(hashes or {}, sort_keys=True).encode()).hexdigest()


def requirement_route_tokens(requirement_text: str) -> set[str]:
    """需求中的高精度路由匹配词：长度≥4 的英文 token + 有英文映射的中文词扩展，用于 defined 路由硬匹配。"""
    req = re.sub(r"[^一-龥a-zA-Z0-9]", " ", requirement_text).lower()
    tokens: set[str] = set()
    for token in req.split():
        if re.search(r"[一-龥]", token):
            for i in range(len(token) - 1):
                tokens.update(CN_TO_EN_KEYWORDS.get(token[i:i + 2], "").split())
        elif len(token) >= 4:
            tokens.add(token)
    return {t for t in tokens if len(t) >= 4}


def expand_recall(requirement_text: str, affected: set[str], baseline_modules: dict, base_via: str) -> dict:
    """召回补强：向量/关键词命中基础上，沿 defined↔referenced 路由闭包与需求路由关键词硬匹配扩展。

    返回 {module_id: {via, ...}}。模块级过召回由 ModuleDetailAnalyzer 的文件级相关度截断兜底。
    """
    sources: dict[str, set[str]] = {mid: {base_via} for mid in affected}
    owners: dict[str, str] = {}
    referencers: dict[str, set[str]] = {}
    for mid, m in baseline_modules.items():
        for a in m.get("apis", []):
            route, kind = a.get("route"), a.get("kind")
            if not route:
                continue
            if kind == "defined":
                owners.setdefault(route, mid)
            elif kind == "referenced":
                referencers.setdefault(route, set()).add(mid)
    for mid in list(sources):
        for a in baseline_modules.get(mid, {}).get("apis", []):
            route, kind = a.get("route"), a.get("kind")
            if kind == "referenced" and route in owners and owners[route] != mid:
                sources.setdefault(owners[route], set()).add("route_closure")
            elif kind == "defined":
                for consumer in referencers.get(route, ()):
                    if consumer != mid:
                        sources.setdefault(consumer, set()).add("route_closure")
    tokens = requirement_route_tokens(requirement_text)
    for route, mid in owners.items():
        if any(t in route.lower() for t in tokens):
            sources.setdefault(mid, set()).add("route_keyword")
    return sources


def classify_miss(module_id: str, requirement_text: str, baseline_modules: dict, predicted: set[str]) -> str:
    """漏报原因分类：route_keyword（需求词命中其定义路由）→ closure（与预测模块存在路由供需关系）→ vector。"""
    m = baseline_modules.get(module_id, {})
    defined = {a.get("route", "") for a in m.get("apis", []) if a.get("kind") == "defined"}
    referenced = {a.get("route", "") for a in m.get("apis", []) if a.get("kind") == "referenced"}
    if any(t in r.lower() for r in defined for t in requirement_route_tokens(requirement_text)):
        return "route_keyword_miss"
    predicted_defined, predicted_referenced = set(), set()
    for pid in predicted:
        for a in baseline_modules.get(pid, {}).get("apis", []):
            if a.get("kind") == "defined":
                predicted_defined.add(a.get("route", ""))
            elif a.get("kind") == "referenced":
                predicted_referenced.add(a.get("route", ""))
    if (defined & predicted_referenced) or (referenced & predicted_defined):
        return "closure_miss"
    return "vector_miss"


def recall_validate(baseline_mgr, old_hashes: dict, changed: set[str], baseline_modules: dict) -> dict | None:
    """召回验证：比对最近一次影响面预测与本次实际变更，形成缺口报告并消费预测文件。

    - 无预测文件 → None（不动作）
    - 缺 meta（旧格式遗留）或基线指纹不一致 → 丢弃陈旧预测，不验证
    - 指纹一致且本次无变更 → 保留预测（开发尚未发生）
    - 指纹一致且有变更 → 写 recall_report.json + 追加 recall_history.jsonl，消费预测文件
    """
    precise = baseline_mgr.read_json("precise_analysis.json")
    if not precise:
        return None
    meta = baseline_mgr.read_json("precise_meta.json")
    if not meta or meta.get("hashes_fp") != hashes_fp(old_hashes):
        baseline_mgr.delete("precise_analysis.json")
        baseline_mgr.delete("precise_meta.json")
        return {"action": "discarded_stale", "reason": "预测缺失基线指纹或指纹不一致，所属开发周期已结束"}
    if not changed:
        return {"action": "pending", "reason": "源码尚无变更，预测待开发后验证"}
    predicted = {e.get("module_id") for e in precise if isinstance(e, dict) and e.get("module_id")}
    requirement_text = meta.get("requirement", "")
    hits = sorted(changed & predicted)
    misses = sorted(changed - predicted)
    report = {
        "requirement": requirement_text,
        "predicted_modules": sorted(predicted),
        "changed_modules": sorted(changed),
        "hits": hits,
        "misses": [{"module_id": m, "reason": classify_miss(m, requirement_text, baseline_modules, predicted)} for m in misses],
        "recall": round(len(hits) / len(changed), 3),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    baseline_mgr.write_json("recall_report.json", report)
    history_line = json.dumps({"at": report["generated_at"], "requirement": requirement_text[:80], "recall": report["recall"], "missed": misses}, ensure_ascii=False)
    baseline_mgr.write_text("recall_history.jsonl", baseline_mgr.read_text("recall_history.jsonl") + history_line + "\n")
    baseline_mgr.delete("precise_analysis.json")
    baseline_mgr.delete("precise_meta.json")
    return {"action": "validated", "recall": report["recall"], "hits": hits, "misses": report["misses"]}
