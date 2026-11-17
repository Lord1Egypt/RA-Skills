#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
source_registry.py — 连接器注册表 + 跨源熔断 + RRF 排名融合（架构韧性层）

WHY / 设计动机
─────────────
ct-literature 当前 6 个文献源全部经 fetch_coze_unified.dispatch 漏斗到单一 Coze
端点 ct-search.coze.site/run，且**没有跨源健康状态 / 熔断**：一旦该端点降级，
每个源都会重试图 Coze 再降级本地，等于把"端点级故障"放大成 6 倍重试 + 6 倍延迟，
且跨进程 / 跨 run 无法复用"端点已挂"的结论。

本文档引入三层韧性（借鉴文章 paper-search-mcp 连接器分层 + scholar-mcp RRF 融合）：
  1) SOURCE_REGISTRY：声明式源注册表。新增源（CNKI / ClinicalTrials.gov / Cochrane
     等）只需追加一条 entry，run() 不再硬编码源列表 → 可扩展性。
  2) ConnectorHealth：每源 + 全局 coze_endpoint 熔断。连续失败达阈值即"开路"，
     后续 run 直接走本地兜底、不再锤 Coze；冷却后放行一次试探，成功则闭合。
     状态持久化到 CT_LIT_RUNTIME_DIR/health.json，跨 run 复用（默认内存态）。
  3) rrf_fuse：跨源倒数排名融合（Reciprocal Rank Fusion），让"多源共识"论文
     （如同时被 OpenAlex 与 EuropePMC 高排）上浮，弥补单源 cited_by 偏差。

向后兼容
────────
  - fetch_source 内部复用 dispatch 的 coze→本地降级逻辑（行为 100% 不变）；
  - run() 调用 fetch_source 后输出 schema 不变（仅多一个忽略用 _provenance 键）；
  - --rank 新增 "rrf" 选项，默认仍为 "cited"（既有排序语义不变）。

零外部依赖：仅用标准库；coze_dispatch / DISPATCHABLE_SOURCES 延迟导入，
模块本身可在无 ct-registry / coze 环境下被 import 与单元测试。
"""
import json
import os
import sys
import threading
import time

# ── 路径 / 持久化 ─────────────────────────────────────────────────────────────
_RUNTIME_DIR = os.environ.get("CT_LIT_RUNTIME_DIR") or os.path.join(
    os.path.expanduser("~"), ".workbuddy", "ct-literature-runtime")
_HEALTH_PATH = os.path.join(_RUNTIME_DIR, "health.json")


def _health_path():
    """返回健康状态持久化路径；若运行态目录不存在且非 env 指定则不持久化（内存态）。"""
    if os.environ.get("CT_LIT_RUNTIME_DIR"):
        try:
            os.makedirs(_RUNTIME_DIR, exist_ok=True)
        except Exception:
            return None
        return _HEALTH_PATH
    if os.path.isdir(_RUNTIME_DIR):
        return _HEALTH_PATH
    return None


def _display_source(coze_id):
    return {
        "openalex": "OpenAlex", "europepmc": "EuropePMC", "biorxiv": "bioRxiv",
        "medrxiv": "medRxiv", "semantic_scholar": "SemanticScholar", "arxiv": "arXiv",
        "pubmed": "PubMed",
    }.get(coze_id, coze_id)


# ── 声明式源注册表（单一事实来源）────────────────────────────────────────────
# 新增源：在此追加一条 dict 即可；run() 遍历本表构建 jobs，不再硬编码。
#   display      : 规范显示名（与 normalize._SOURCE_CANON 对齐）
#   coze_id      : 传给 dispatch 的源 id（None 表示不走 Coze、纯本地/独立）
#   coze_routable: 是否经 Coze 统一端点（False 的源由 run() 单独处理，如 PROSPERO）
#   category     : 文献类别（bibliographic / preprint / registry / guideline）
#   rrf_weight   : RRF 融合权重（主源 1.0，补充源 0.6）
#   active       : 是否纳入默认检索（False = 预留扩展位，如 cnki / clinicaltrials）
SOURCE_REGISTRY = {
    "OpenAlex": {
        "display": "OpenAlex", "coze_id": "openalex", "coze_routable": True,
        "category": "bibliographic", "rrf_weight": 1.0, "active": True,
    },
    "EuropePMC": {
        "display": "EuropePMC", "coze_id": "europepmc", "coze_routable": True,
        "category": "bibliographic", "rrf_weight": 1.0, "active": True,
    },
    "bioRxiv": {
        "display": "bioRxiv", "coze_id": "biorxiv", "coze_routable": True,
        "category": "preprint", "rrf_weight": 0.6, "active": True,
    },
    "medRxiv": {
        "display": "medRxiv", "coze_id": "medrxiv", "coze_routable": True,
        "category": "preprint", "rrf_weight": 0.6, "active": True,
    },
    "SemanticScholar": {
        "display": "SemanticScholar", "coze_id": "semantic_scholar", "coze_routable": True,
        "category": "bibliographic", "rrf_weight": 0.6, "active": True,
    },
    "arXiv": {
        "display": "arXiv", "coze_id": "arxiv", "coze_routable": True,
        "category": "preprint", "rrf_weight": 0.6, "active": True,
    },
    # PubMed（NCBI E-utilities）——2026-11-03 新增，Europe PMC 的独立冗余通道。
    # 为什么必须是独立源：Europe PMC 是技能里**唯一**同时覆盖 PubMed/MEDLINE 与
    # Cochrane CDSR 的源，它一旦限流/不可达，Cochrane 检索直接归零。NCBI eutils
    # 与 ebi.ac.uk 是完全不同的基础设施，一条 `db=pubmed` 通道即可同时覆盖两者
    # （Cochrane 用 `Cochrane Database Syst Rev[ta]` 期刊字段过滤）。
    # 2026-11-04 S5（用户拍板「完整切到 Coze」）：Coze 0.3.97 已上线 pubmed_node
    # （线上 /run 实测 hit_count / provenance 均正常），coze_routable 改 True，
    # 主检索链路走统一端点，享受统一限速 / 缓存 / 计费 / 审计。
    # ⚠️ 原本 coze_routable=False 的理由之一是「避免检索词经第三方端点外发」；
    # 切换后主链路检索式会外发到 Coze，这是用户明确确认的取舍。
    # 检索式仍由本地构造：fetch_coze_unified.dispatch() 调
    # fetch_pubmed._build_query() 把 pt / 日期 / Cochrane 过滤编进 keyword 后
    # 才外发，节点只执行（§6.3）。本地 fetch_pubmed 完整保留，作 _local_only /
    # _offline_fallback 的 R1 降级（§20.19.7 红线 2：不取消本地引擎）。
    "PubMed": {
        "display": "PubMed", "coze_id": "pubmed", "coze_routable": True,
        "category": "bibliographic", "rrf_weight": 1.0, "active": True,
    },
    # ── 扩展位（当前 inactive，演示声明式新增流程，不进入默认检索）──
    # "CNKI": {
    #     "display": "CNKI", "coze_id": None, "coze_routable": False,
    #     "category": "bibliographic", "rrf_weight": 1.0, "active": False,
    # },
    # "ClinicalTrials": {
    #     "display": "ClinicalTrials", "coze_id": None, "coze_routable": False,
    #     "category": "registry", "rrf_weight": 1.0, "active": False,
    # },
}

_COZE_ENDPOINT_KEY = "coze_endpoint"  # 全局端点熔断键（非具体源）


def register_source(name, display, coze_id, coze_routable, category,
                    rrf_weight=1.0, active=True):
    """运行时注册新源（扩展用）。重复名覆盖。"""
    SOURCE_REGISTRY[name] = {
        "display": display, "coze_id": coze_id, "coze_routable": coze_routable,
        "category": category, "rrf_weight": rrf_weight, "active": active,
    }


# ── 熔断（Circuit Breaker）────────────────────────────────────────────────────
class ConnectorHealth:
    """每键（具体源 + 全局 coze_endpoint）独立熔断。

    状态机：closed → (连续失败 >= threshold) → open（冷却 cooldown 秒）→ 放行一次
    试探 → 成功闭合 / 失败重开。状态可选持久化，跨 run 复用。
    """

    def __init__(self, threshold=3, cooldown=600):
        self.threshold = threshold
        self.cooldown = cooldown
        self._lock = threading.Lock()
        self._state = {}  # key -> {"failures":int, "open_until":float, "last":float}
        self._load()

    # ── 持久化 ──
    def _load(self):
        p = _health_path()
        if not p or not os.path.isfile(p):
            return
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
            self._state = {k: v for k, v in (data.get("state") or {}).items()
                           if isinstance(v, dict)}
        except Exception:
            self._state = {}

    def _save(self):
        p = _health_path()
        if not p:
            return
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"state": self._state, "saved_at": time.time()}, f)
        except Exception:
            pass

    # ── 判定 ──
    def is_open(self, key):
        with self._lock:
            s = self._state.get(key)
            if not s:
                return False
            ou = s.get("open_until", 0) or 0
            if ou > time.time():
                return True
            # 冷却已过期 → 允许一次试探（视为 closed，但保留 failures 计数直到成功）
            return False

    def record_failure(self, key):
        with self._lock:
            s = self._state.setdefault(key, {"failures": 0, "open_until": 0, "last": 0})
            s["failures"] = s.get("failures", 0) + 1
            s["last"] = time.time()
            if s["failures"] >= self.threshold:
                s["open_until"] = time.time() + self.cooldown
            self._save()

    def record_success(self, key):
        with self._lock:
            s = self._state.get(key)
            if not s:
                return
            s["failures"] = 0
            s["open_until"] = 0
            s["last"] = time.time()
            self._save()

    def status(self, key):
        with self._lock:
            s = self._state.get(key)
            # 内联开放判定：不可调用 is_open()（会再次获取同一把非重入锁 → 自死锁）
            ou = (s or {}).get("open_until", 0) or 0
            if ou > time.time():
                return "open"
            if (s or {}).get("failures") or 0 > 0:
                return "degraded"
            return "closed"

    def reset(self, key=None):
        with self._lock:
            if key is None:
                self._state = {}
            else:
                self._state.pop(key, None)
            self._save()


# 模块级单例（懒初始化，避免 import 即触碰磁盘）
_HEALTH = None
_HEALTH_LOCK = threading.Lock()


def health():
    global _HEALTH
    if _HEALTH is None:
        with _HEALTH_LOCK:
            if _HEALTH is None:
                _HEALTH = ConnectorHealth()
    return _HEALTH


def reset_health():
    """清空全部熔断状态（CLI --health-reset 用）。"""
    h = health()
    h.reset()
    return True


def health_report():
    """返回可读健康快照（observability）。"""
    h = health()
    keys = set(h._state.keys()) | {_COZE_ENDPOINT_KEY}
    return {k: h.status(k) for k in sorted(keys)}


# ── 统一外发检索（含熔断 + coze→本地降级）────────────────────────────────────
def _coze_dispatch_lazy():
    """延迟导入 dispatch，避免无 coze 环境下 import 失败拖垮本模块。"""
    from adapters.fetch_coze_unified import dispatch as coze_dispatch  # noqa: F401
    return coze_dispatch


def _empty_payload(name):
    return {"source": name, "works": [], "count": 0, "total_count": 0,
            "_provenance": "empty"}


def fetch_source(name, keyword, year_from=None, year_to=None, max_results=50,
                 online=True, offline=False, date_from=None, date_to=None,
                 timeout=300, log_feishu=False, cochrane=False,
                 request_id=None):
    """统一外发检索（替换 run() 原先的 _coze_dispatch_with_fallback）。

    韧性行为：
      - offline / 非 online / 端点或源已熔断开路 → 直接本地兜底（不锤 Coze）；
      - 否则先试 Coze，失败（error 或非异常）→ 记一次失败并降级本地；
      - 成功 → 记一次成功（闭合熔断）。
    返回与 dispatch 同形 payload，并附加 _provenance（coze / local / empty）。

    `cochrane` 为 CDSR-only 车道：只在本地兜底路径生效（OpenAlex ISSN 过滤 /
    Europe PMC 期刊过滤）；Coze 云端无对应过滤器，online 路径靠调用方客户端过滤。
    """
    spec = SOURCE_REGISTRY.get(name)
    if spec is None:
        raise KeyError("unknown source: %s (not in SOURCE_REGISTRY)" % name)
    coze_id = spec["coze_id"]
    h = health()

    force_local = (offline or not online
                   or h.is_open(_COZE_ENDPOINT_KEY) or h.is_open(coze_id))

    try:
        coze_dispatch = _coze_dispatch_lazy()
    except Exception:
        coze_dispatch = None

    # request_id 透传统一端点（_strip 会在本地兜底路径自动剥掉该键）。
    _kw = dict(year_from=year_from, year_to=year_to, max_results=max_results,
               date_from=date_from, date_to=date_to, run=True, timeout=timeout,
               cochrane=cochrane, request_id=request_id)

    # 非 Coze 路由源（coze_routable=False，供未来纯本地源使用）：纯本地独立通道，
    # 不经过统一端点，也就没有 coze→local 降级可言——直接走本地 fetch。
    # 注：PubMed 已于 2026-11-04 S5 改为 coze_routable=True，不再走这个分支；
    # 其本地引擎改由 _local_only / fetch_coze_unified._offline_fallback 承担降级。
    # 注意：必须放在 _kw 构造之后（_local_only 依赖 _kw）。
    if coze_id is not None and not spec.get("coze_routable", True):
        result = _local_only(coze_id, keyword, _kw, log_feishu)
        result = result or _empty_payload(name)
        result["_provenance"] = "local"
        return result

    if force_local or coze_dispatch is None:
        if coze_dispatch is None:
            # 无 coze 环境：仅本地兜底
            result = _local_only(coze_id, keyword, _kw, log_feishu)
        else:
            if h.is_open(_COZE_ENDPOINT_KEY) or h.is_open(coze_id):
                h.record_failure(_COZE_ENDPOINT_KEY)  # 维持开路计时（不重置冷却）
                if h.is_open(coze_id):
                    h.record_failure(coze_id)
            result = coze_dispatch(coze_id, keyword, log_feishu=log_feishu, offline=True, **_kw)
        prov = "local"
    else:
        try:
            result = coze_dispatch(coze_id, keyword, log_feishu=log_feishu, **_kw)
            if result and not result.get("error"):
                h.record_success(coze_id)
                h.record_success(_COZE_ENDPOINT_KEY)
                prov = "coze"
            else:
                h.record_failure(coze_id)
                h.record_failure(_COZE_ENDPOINT_KEY)
                result = coze_dispatch(coze_id, keyword, log_feishu=True, offline=True, **_kw)
                prov = "local"
        except Exception:
            h.record_failure(coze_id)
            h.record_failure(_COZE_ENDPOINT_KEY)
            result = coze_dispatch(coze_id, keyword, log_feishu=True, offline=True, **_kw)
            prov = "local"

    result = result or _empty_payload(name)
    result["_provenance"] = prov
    return result


def _local_only(coze_id, keyword, _kw, log_feishu):
    """无 coze_dispatch 时：尝试直接调用本地 fetch_*.py（与 dispatch offline 同效）。

    注意：`_strip(_kw)` 已含 `run=True`，此处**不可**再显式传 `run=True`
    （否则 `fetch() got multiple values for keyword argument 'run'`，
    被下面的 except 吞掉后整条本地兜底静默退化为空结果）。
    """
    try:
        from adapters import fetch_openalex, fetch_europepmc, fetch_semantic_scholar
        from adapters import fetch_preprints, fetch_arxiv
        if coze_id == "openalex":
            return fetch_openalex.fetch(keyword, **_strip(_kw))
        if coze_id == "europepmc":
            return fetch_europepmc.fetch(keyword, **_strip(_kw))
        if coze_id == "pubmed":
            from adapters import fetch_pubmed
            return fetch_pubmed.fetch(keyword, **_strip(_kw))
        if coze_id == "semantic_scholar":
            return fetch_semantic_scholar.fetch(keyword, **_strip(_kw))
        if coze_id in ("biorxiv", "medrxiv"):
            return fetch_preprints.fetch(keyword, server=coze_id, **_strip(_kw))
        if coze_id == "arxiv":
            return fetch_arxiv.fetch(keyword, **_strip(_kw))
    except Exception as e:
        # 本地兜底失败必须留痕：静默返回空 payload 会被上游读成「该源没检索到」，
        # 与「兜底根本没跑起来」无法区分（2026-11-03 曾因重复 run=True 静默全灭）。
        print("[WARN] source_registry._local_only(%s) 失败：%s: %s"
              % (coze_id, type(e).__name__, e), file=sys.stderr)
    return _empty_payload(_display_source(coze_id))


def _strip(_kw):
    """本地 fetch 不接受 date_from/date_to/log_feishu/timeout，剥离之。

    `cochrane` 是本地 fetch 真实消费的参数（OpenAlex ISSN / Europe PMC 期刊过滤），
    必须保留；其余本地 fetch 未声明的键一律剥掉，避免 TypeError。
    """
    return {k: v for k, v in _kw.items()
            if k in ("year_from", "year_to", "max_results", "run", "cochrane")}


# ── RRF 排名融合 ──────────────────────────────────────────────────────────────
def _norm_doi(d):
    if not d:
        return None
    import re
    s = str(d).strip().lower()
    m = re.search(r"10\.\d{4,9}/[^\s]+", s)
    return m.group(0).rstrip(".,;:)]") if m else s


def _norm_title(t):
    if not t:
        return ""
    import re
    t = t.lower()
    t = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", t)
    return " ".join(t.split())


def _dedupe_key(w):
    """本地版 dedupe_key（与 normalize.dedupe_key 同语义，便于独立测试）。"""
    if not isinstance(w, dict):
        return None
    doi = _norm_doi(w.get("doi"))
    title = _norm_title(w.get("title"))
    key = doi or ("t:" + title)
    if not key or key == "t:":
        return None
    return key


def build_source_ranks(payloads):
    """从各源 payload（合并前）构建 {dedupe_key: {source_display: rank_int}}。

    rank = 该 work 在源结果列表中的位置（1-based）。供 rrf_fuse 使用。
    纯本地计算，无网络。
    """
    ranks = {}
    for p in payloads:
        if not p:
            continue
        if "works" not in p and "projects" in p:
            p["works"] = p.pop("projects")
        src = p.get("source")
        if not src:
            continue
        for i, w in enumerate(p.get("works", [])):
            if not isinstance(w, dict):
                continue
            key = _dedupe_key(w)
            if not key:
                continue
            ranks.setdefault(key, {})[src] = i + 1
    return ranks


def rrf_fuse(works, source_ranks, k=60, weights=None):
    """Reciprocal Rank Fusion：跨源排名融合。

    score = Σ_source  weight[source] / (k + rank_in_source)
    多源高排的论文（共识）得分高，上浮；单源噪声被稀释。
    k 为平滑常数（默认 60，Cormack 2009 推荐值）。

    Args:
        works:        merge 后的统一 work 列表（每条含 sources 列表）。
        source_ranks: build_source_ranks 产物。
        k:            平滑常数。
        weights:      {source_display: weight}；缺省取 SOURCE_REGISTRY 的 rrf_weight。
    Returns:
        新 work 列表（深拷贝并附加 rrf_score / _source_ranks），按 rrf_score 降序
        （同分时保留原序，稳定）。
    """
    if weights is None:
        weights = {s["display"]: s["rrf_weight"] for s in SOURCE_REGISTRY.values()}
    out = []
    for w in works:
        key = _dedupe_key(w)
        ranks = source_ranks.get(key, {})
        score = 0.0
        for src, r in ranks.items():
            wt = weights.get(src, 1.0)
            score += wt / (k + r)
        nw = dict(w)
        nw["rrf_score"] = round(score, 6)
        nw["_source_ranks"] = ranks
        out.append(nw)
    out.sort(key=lambda x: -x.get("rrf_score", 0))
    return out


if __name__ == "__main__":
    import sys
    # 简单自检（无网络）：RRF + 熔断 + 注册表完整性
    ok = True
    # 1) 注册表完整性
    for n, s in SOURCE_REGISTRY.items():
        for f in ("display", "coze_id", "coze_routable", "category", "rrf_weight", "active"):
            if f not in s:
                print("[FAIL] %s missing %s" % (n, f)); ok = False
    # 2) RRF 正确性
    sample = [
        {"source": "OpenAlex", "doi": "10.1/a", "title": "X"},
        {"source": "EuropePMC", "doi": "10.1/a", "title": "X"},
        {"source": "arXiv", "doi": "10.2/b", "title": "Y"},
    ]
    ranks = build_source_ranks([{"source": "OpenAlex", "works": [sample[0]]},
                               {"source": "EuropePMC", "works": [sample[1]]},
                               {"source": "arXiv", "works": [sample[2]]}])
    fused = rrf_fuse([{"doi": "10.1/a", "title": "X", "sources": ["OpenAlex", "EuropePMC"]},
                      {"doi": "10.2/b", "title": "Y", "sources": ["arXiv"]}], ranks)
    assert fused[0]["doi"] == "10.1/a", "RRF 应让双源共识论文上浮"
    print("[OK] registry=%d sources, RRF top=%s" % (len(SOURCE_REGISTRY), fused[0]["doi"]))
    # 3) 熔断开/闭
    h = ConnectorHealth(threshold=2, cooldown=1)
    h.reset()
    h.record_failure("test_src"); h.record_failure("test_src")
    assert h.is_open("test_src"), "连续失败应开路"
    h.record_success("test_src")
    assert not h.is_open("test_src"), "成功应闭合"
    print("[OK] circuit breaker open/close transitions")
    sys.exit(0 if ok else 1)
