#!/usr/bin/env python3
"""search_ictrp.py - Unified Coze external-service caller (Tier-2): WHO ICTRP (source="who")

WHY (architecture decision 2026-07-27):
  WHO ICTRP was previously NOT a data source because its public portal (ASP.NET
  WebForms) had no clean API and required fragile browser scraping. A dedicated
  external workflow now exposes a clean JSON API for WHO ICTRP (source="who") and
  also for China drug trials (source="chinadrugtrials"). This revives WHO ICTRP as
  a Tier-2 external service. It is valuable because ICTRP mirrors 14+ primary
  registries (jRCT, DRKS, ANZCTR, ISRCTN, CTRI, TCTR, PACTR, IRCT, SLCTR, ...) in
  ONE call -- materially expanding ct-registry coverage beyond the registries we
  directly connect to. The bridging/de-dup value that ICTRP provides is preserved
  by feeding its records into aggregate.py, which re-derives cross-registry links
  (UTN/TRN + fuzzy match + embedded-registration-number scan on the `raw` field).

Endpoint: https://ct-search.coze.site/run  (POST; Bearer token REQUIRED)
  This is the UNIFIED Coze workflow endpoint. It serves:
    - source="who"            -> WHO ICTRP (registry aggregator, mirrors 14+ registries)
    - source="chinadrugtrials" -> China CDE (drug trials registry)
    - source="isrctn"         -> ISRCTN (UK registry; no clean public search API)
    - source="drks"           -> DRKS (German registry; JS/redirect-only search)
    - source="chictr"         -> ChiCTR (China academic trials; no public API)
  The last three are WHO-COVERED national registries that ct-registry retrieves
  INDEPENDENTLY as a fallback when WHO ICTRP (source="who") cannot retrieve. They
  share the single ICTRP Bearer token (embedded in adapters/endpoint_token.py; no .dat file dependency). Drive via --source
  (default who). The standalone CDE endpoint search_cde_workflow.py (archived under
  CDE/) -> ct-searchcde.coze.site/run is RETIRED (2026-08-12) -- local reference only;
  production CDE uses source="chinadrugtrials" on the unified endpoint.

Modes (`mode` field, required):
  search        - free-text `keyword` query (structured WHO fields not used)
  combined      - structured `who_*` filters (+ optional `keyword`)
  multi_keyword - multi_keywords (space separated, intersect)
  detail        - fetch project details from a project_list JSON string

Fetch strategy (`--fetch-mode`, optional; default = legacy auto-detect):
  list   - run a search ONLY (1 Coze call). (Legacy default when no --project-list.)
  detail - run detail ONLY (requires --project-list; 1 Coze call).
           (Legacy when --mode detail or --project-list is set.)
  both   - run the search, then AUTOMATICALLY fetch details from the returned
           project_list in the SAME invocation (2 Coze calls, but 1 demand_id
           charge thanks to DEMAND-BASED DEDUP). Symmetric across who /
           chinadrugtrials / isrctn / drks / chictr. Lists with >100 records skip
           auto-detail unless --auto-confirm (cost / timeout guard, mirrors the
           CDE _run_cde_detail skip logic in ct_registry.py).

Payload contract (mirrors CDE / Coze convention, verified for that family):
  - Send PLAIN STRINGS for who_* fields; OMIT unused fields entirely (do NOT send
    "" -- the endpoint rejects/poisons the query when empty fields are present).
  - who_*_operator: "AND" / "OR" / "NOT". who_*_no_synonyms: boolean.
  - max_pages: int (default 50 -> ~500 results; ~10 records per page).
  - Booleans: who_covid19 / who_with_results / who_rare_diseases / who_gene_editing.

Response schema:
  {"source":"who", "project_list":"<JSON string of records>", "total_count":N,
   "error_msg":"...", "scraped_data_json":"..." (detail mode)}
  `project_list` is a JSON STRING -> parsed here into a list of record dicts.
  Each record carries fields such as 登记号/Main ID, 药物名称/公共标题,
  适应症/健康状况, 试验状态/招募状态, 项目ID. norm_ictrp (normalize.py) probes
  candidate keys and stashes the FULL record in `raw` so aggregate.py can bridge
  on embedded registry numbers (NCT / JPRN / CTRI / ...).

⚠️ WHO combined 模式合同（2026-09-06 实测根因）：统一端点 WHO `combined` 模式**只认**
  who_country / who_phase / who_date_* / who_sponsor / who_secondary_id /
  who_recruitment_status 为「真筛选」；`who_condition` / `who_intervention` /
  `who_title` **不算**。仅传后者会在 project_list 内层返回
  `{"error":"combined 模式必须至少带一个筛选…"}` 并 0 条。`_build_who_payload`
  已对「combined 仅含文本字段」自动降级为 search 自由词——**不要**为了 disease+drug
  查询强行用 combined（会被后端拒）；需要字段级 AND 收敛时务必同时给一个真筛选。
  ChiCTR (`source="chictr"`) 截至 2026-09-06 对多个关键词均返回 `{"total_count":0,
  "projects":[]}` 且无 error（疑后端节点故障）；其 0 条应视为「源不可用」而非「无结果」，
  China 覆盖以 CDE (`source="chinadrugtrials"`) 为准。

Egress: only PUBLIC query terms leave. No confidential subject / protocol data ->
compliant with the ct-base confidentiality red line.

Safety model (ct-base §0.2): default SAFE PREVIEW. The script prints the exact
payload and the request it WOULD make, and performs NO network I/O unless --run.
"""
import argparse
import base64
import json
import os
import sys
import time          # 异步轮询指数退避用
import re            # 升级反馈环 keyword 粗粒度拆分用
import hashlib       # ct-base §8.6：query_origin = sha256(本机 hostname)，须由技能安装设备生成
import socket        # ct-base §8.6：禁止由 Coze 服务器生成（容器 hostname 漂移）

# Reuse the shared external-service token machinery (adapters/endpoint_token.py, XOR+base64 embedded; no .dat).
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "scripts"))  # shared pure-local utils (usage_guard, keyword_breadth)
# ── §8.6 硬件绑定机器标识：本技能 scripts/hardware_id.py（ct-base 共享件 vendored 副本）──
try:
    from hardware_id import hardware_id as _hardware_id
except Exception:  # pragma: no cover
    _hardware_id = None
from extsvc_client import (get_token, _status_guidance, _check_outbound_authorization,
                            _request, _sanitize_payload, _run_async_poll)
import usage_guard  # daily shared-resource call cap (100/day)
# 端点 URL 单一出口：统一检索端点由 endpoint_token 提供（架构评审#4）。
from endpoint_token import CT_SEARCH_ENDPOINT

# ct-base coze_io_contract §1.1：coze 请求用 user_language 备用入参（来自 scripts/i18n.py）。
# scripts/ 无 __init__.py，需把技能根目录加入 sys.path 才能 `from scripts.i18n import ...`
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SKILL_ROOT not in sys.path:
    sys.path.insert(0, _SKILL_ROOT)
from scripts.i18n import resolve_user_language
try:
    from soft_broad import is_soft_broad
except Exception:  # 软宽词层为 ct-registry 本地模块；缺失时降级为「非软宽」
    def is_soft_broad(kw):
        return False

# 端点 URL 单一出口：统一由 endpoint_token.CT_SEARCH_ENDPOINT 提供（架构评审#4）。
DEFAULT_ENDPOINT = CT_SEARCH_ENDPOINT

# API `source` field values for the unified endpoint.
# who = WHO ICTRP (registry aggregator); chinadrugtrials = China CDE (drug trials).
# isrctn / drks / chictr = the national registries WHO covers but which have no
#   clean public search API of their own — they are served by the SAME unified
#   workflow (extended to these sources) so ct-registry can fall back to them
#   independently when WHO ICTRP (source="who") cannot retrieve.
API_SOURCE = {"who": "who", "chinadrugtrials": "chinadrugtrials",
              "isrctn": "isrctn", "drks": "drks", "chictr": "chictr",
              "euctr": "euctr", "ctis": "ctis"}
# Internal record-source label (used by normalize.py adapter routing).
RECORD_SOURCE = {"who": "ICTRP", "chinadrugtrials": "CDE",
                 "isrctn": "ISRCTN", "drks": "DRKS", "chictr": "CHICTR",
                 "euctr": "EUCTR", "ctis": "CTIS"}

# 治理护栏 (0.5.09)：发文前拦截未注册 source，避免脏请求进飞书 / 统一端点。
# 历史 advisor_source_not_deployed 类 bug 即源于未注册 source 被静默当作 who 发出，
# 现改为显式拒绝——调用方立即看到明确错误，而非污染飞书审计列。
def _validate_source(args):
    """拒绝未注册 source；合法取值见 API_SOURCE 键集合。"""
    _src = getattr(args, "source", None)
    if _src not in API_SOURCE:
        sys.exit(
            f"[ictrp-extsvc][ERROR] 未注册 source={_src!r} —— "
            f"合法取值: {sorted(API_SOURCE.keys())}。"
            f"脏请求已拦截，未向统一端点发出。"
        )

# 健康对照词（2026-09-06 实测确认）：简单源（chictr/isrctn/drks）返回「0+无错误」时，
# 歧义极大——可能是真实零结果，也可能是后端节点故障。用各组**必有海量登记**的对照词
# 做一次性探针：若对照词也返回 0+无错误 → 判定源后端故障（节点坏），本次 0 条不可信；
# 若对照词有数据 → 本次 0 条为真实零结果。
#   对照组（均经 2026-09-06 在统一端点实测，ChiCTR 对以下词全部返回空 → 证伪"节点正常"）：
#     chictr: 肺癌 / 二甲双胍 / 高血压 / aspirin  —— 全部 total_count=0，无 error 无 log
#   结论：ChiCTR 后端节点自 2026-09-06 起持续返回空（疑似故障），China 覆盖务必以 CDE 为准。
CONTROL_TERMS = {
    "chictr": "肺癌",     # lung cancer — ChiCTR 上数千条登记，必有数据
    "isrctn": "cancer",   # ISRCTN 高体量通用词
    "drks": "diabetes",   # DRKS 高体量通用词
    "euctr": "cancer",    # EU-CTR/EudraCT 高体量通用词（WHO 亦镜像 EUCTR 记录）
}
# Token config is SHARED: both sources hit the SAME unified endpoint and use the
# SAME Coze token (adapters/endpoint_token.py embedded blob). The standalone CDE endpoint (search_cde_workflow.py,
# archived under CDE/) -> ct-searchcde.coze.site/run is RETIRED (2026-08-12), kept for local reference only.
TOKEN_SOURCE = "ICTRP"

# WHO ICTRP 检索语言约束（2026-09-07 实测）：WHO 端只认英文（中文关键词在统一端点
# 稳定返回 0 条，英文正常命中）。凡是 source=who 的检索（含 ChiCTR WAF fallback 切
# WHO 路径），keyword / multi_keywords 若为中文须先本地化为英文再发出。
# 本地化顺序：ct-base curated term_map（references/term_map.json，双向、权威）
# → kw_localize.online_translate（MyMemory，keyless，仅作长尾词兜底）。实测在线翻译
# 对医学术语不可靠（如 光生物调节→Photobioregulation 而非 photobiomodulation，WHO
# 命中 0），故新增领域词条一律进 term_map 而非依赖在线兜底。
_CJK = re.compile(r"[\u4e00-\u9fff]")
# WHO free-text 只吃空格分隔的关键词：翻译结果里的括号注释（如 "(PBM)"）会当成
# 附加搜索词，反而缩小命中集 → 发给 WHO 前剥离括号段（仅用于查询，不用于展示）。
_PAREN = re.compile(r"\s*\([^)]*\)")


def _localize_who_keyword(kw, args=None):
    """中文关键词 → 英文（WHO 只认英文）。返回 (localized_or_original, meta)。

    meta: dict {original, localized, source} —— source ∈ {same, term_map, online,
    miss}（miss = 词典未命中且在线翻译不可用/失败，维持原词并提示）。对已含英文或
    无 CJK 的词原样返回 source="same"，不触发任何网络调用。
    用 `args` 上的 --no-kw-localize 可整链路关闭（默认开启）。
    """
    if not kw or not _CJK.search(kw):
        return kw, {"source": "same", "original": kw, "localized": kw}
    if args is not None and getattr(args, "no_kw_localize", False):
        return kw, {"source": "same", "original": kw, "localized": kw}
    try:
        from scripts.kw_localize import detect_lang, localize_with_fallback
    except Exception:
        sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "scripts"))
        try:
            from scripts.kw_localize import detect_lang, localize_with_fallback  # noqa: F401
        except Exception:
            return kw, {"source": "miss", "original": kw, "localized": kw}
    if detect_lang(kw) != "zh":
        return kw, {"source": "same", "original": kw, "localized": kw}
    out, st = localize_with_fallback(kw, "en")
    if st in ("term_map", "online") and out and out != kw:
        # WHO free-text 检索去括号注释段（见 _PAREN 说明），保留主干
        clean = _PAREN.sub("", out).strip() or out
        return clean, {"source": st, "original": kw, "localized": clean}
    return kw, {"source": st or "miss", "original": kw, "localized": kw}


def _localize_who_payload(payload, args=None):
    """对 source=who 的 payload 做关键词中→英本地化（原地修改 + 返回 meta 列表）。

    覆盖 keyword 与 multi_keywords 两个字段；每次翻译都打印审计行，调用方负责把
    meta 写入最终信封（如 fallback_used / kw_localized 等字段）供下游与审计可见。
    """
    metas = []
    if not payload or payload.get("source") != "who":
        return metas
    if payload.get("keyword"):
        k = payload.get("keyword")
        loc, meta = _localize_who_keyword(k, args)
        if loc != k:
            payload["keyword"] = loc
        if meta.get("source") not in ("same",):
            metas.append(meta)
            print(f"[ictrp-extsvc][KW-LOCALIZE] WHO keyword 中→英: "
                  f"{meta.get('original')!r} → {loc!r} (source={meta.get('source')})")
    if payload.get("multi_keywords"):
        # multi_keyword 模式为空格分隔 AND；对每个含 CJK 的词组分别本地化
        parts = payload["multi_keywords"].split()
        out_parts, changed = [], False
        for p in parts:
            if _CJK.search(p):
                loc, meta = _localize_who_keyword(p, args)
                out_parts.append(loc)
                if loc != p:
                    changed = True
                if meta.get("source") not in ("same",):
                    metas.append(meta)
            else:
                out_parts.append(p)
        if changed:
            payload["multi_keywords"] = " ".join(out_parts)
            print(f"[ictrp-extsvc][KW-LOCALIZE] WHO multi_keywords 中→英: "
                  f"{' '.join(parts)!r} → {payload['multi_keywords']!r}")
    return metas


def _gate_records_from_who_metas(metas):
    """WHO 中→英本地化 meta 列表 → 翻译确认门契约记录（ct-base §5.2）。

    meta {original, localized, source}，source ∈ {same, term_map, online, miss}：
      same    → native_en（英文词直发英文源，放行）
      term_map/online → whole（已翻译，放行知会）
      miss    → fail_open + untranslated_risk=False（WHO 收录英文题目，
                原文直发可接受 → 放行知会，不阻断；与 ChiCTR 同口径）
    """
    recs = []
    for m in metas or []:
        src = m.get("source")
        base = {"original": m.get("original"), "localized": m.get("localized"),
                "ambiguous": False, "source": "WHO"}
        if src == "same":
            base.update({"candidates": [], "mode": "native_en"})
        elif src == "miss":
            base.update({"candidates": [], "mode": "fail_open", "untranslated_risk": False})
        else:
            base.update({"candidates": [m.get("localized")], "mode": "whole"})
        recs.append(base)
    return recs


def _compute_query_origin():
    """ct-base §8.6：query_origin = 硬件绑定的 sha256，标识调用来源机器。

    必须由技能安装设备（本机）生成并随请求携带；优先取硬件令牌
    （SMBIOS UUID / MachineGuid / machine-id，跨账号 / 改主机名 / 重装系统稳定），
    取不到时回退主机名。禁止由 Coze 服务器生成（Coze 容器 hostname 是实例标识，
    重建即漂移，且标识的是服务器而非来源机器）。SHA256 单向不可逆，不含明文
    主机名 / IP / 任何 PII。
    """
    if _hardware_id is not None:
        return _hardware_id()
    return "sha256:" + hashlib.sha256(socket.gethostname().encode("utf-8")).hexdigest()


# ── 入口标识 entry_point（ct-base coze_io_contract §1.3 / §2.3 · 2026-10-07）─────
# 区分「调用来源」：技能本身（"skill"）vs 工作台 Web 应用（"workbench"）vs 未来
# 第三方 API（"api"）。透传写入飞书**独立列** entry_point，供后台按来源直切筛选。
#
# 与 query_origin 的区别（🔴 不得混用）：query_origin 按**机器**（硬件 ID / 主机名
# 哈希），同一台机器上 skill / workbench 算出的哈希逐字节相同 → 无法区分界面来源，
# 故须独立字段（§1.3）。
# 进程启动期初值来源（2026-10-13 修复）：环境变量 CT_ENTRY_POINT。
# ct-registry 工作台是 Popen(ct_registry.py) 子进程架构，且 ct_registry.py 再以
# subprocess.run 调本模块（search_ictrp.py）——真正向 coze 发请求的是孙进程，
# 父进程（server.py）里调用 set_entry_point() 无法跨进程传递，历史上因此全树
# 零调用点、entry_point 恒为默认 "skill"（应用页面调用也落 "skill"）。
# 现由 server.py 在 Popen env 写 CT_ENTRY_POINT=workbench，环境变量沿
# server.py → ct_registry.py → search_ictrp.py 逐级继承，本模块加载时读取作初值；
# agent / 技能进程不设该变量 → 恒为 "skill"。非法值 / 空白一律回退 "skill"（§1.3）。
_ENTRY_POINT_WHITELIST = frozenset({"skill", "workbench", "api"})
_ENTRY_POINT_ENV = "CT_ENTRY_POINT"


def _entry_point_from_env():
    """进程启动期从环境变量解析 entry_point 初值（白名单外一律回退 "skill"）。"""
    v = (os.environ.get(_ENTRY_POINT_ENV) or "").strip()
    return v if v in _ENTRY_POINT_WHITELIST else "skill"


_ENTRY_POINT = _entry_point_from_env()


def set_entry_point(value):
    """覆盖进程级入口标识（工作台进程启动期调用以标记 workbench）。

    agent / 技能进程**不import** 工作台模块 → 两进程全局值天然隔离、无污染。
    空值 / 空白 / 非法值一律回退 "skill"，绝不写出 None 或脏值（§1.3 白名单校验）。
    """
    global _ENTRY_POINT
    v = (value or "").strip() if isinstance(value, str) else ""
    _ENTRY_POINT = v if v in _ENTRY_POINT_WHITELIST else "skill"


def entry_point():
    """当前进程级入口标识（永不为 None / 空串）。"""
    return _ENTRY_POINT or "skill"


def _skill_version(fallback="0.9.3"):
    """ct-base coze_io_contract §1.2：顶层信封字段 skill_version。

    读本技能 SKILL.md frontmatter 的 `version:`（单一事实来源，升版本免改代码）；
    读取失败回退内置常量。
    """
    try:
        skill_md = os.path.join(_SKILL_ROOT, "SKILL.md")
        with open(skill_md, encoding="utf-8") as f:
            for line in f:
                m = re.match(r'^version:\s*"?([^"\n\r]+)"?\s*$', line)
                if m:
                    return m.group(1).strip().strip('"')
    except Exception:
        pass
    return fallback


def _request_id(args=None):
    """request_id（0.5.02，2026-11-11）：一次用户请求的唯一 ID，落飞书独立列。

    解析优先级：CLI --request-id > env CT_REQUEST_ID（ct-advisor 跨技能透传的上游
    请求 ID，2026-11-11 Fix E）> env CT_REGISTRY_REQUEST_ID（ct_registry.py 子进程
    链共享同一 ID）> 本进程新生成 uuid4（缓存于 args，escalation/fallback 重发同 ID）。
    """
    rid = getattr(args, "request_id", None) if args is not None else None
    if rid:
        return rid
    # 2026-11-11 Fix E：ct-advisor 派发兄弟技能时注入 CT_REQUEST_ID，优先继承，
    # 使一次用户请求内所有端点调用共享同一 request_id（云端据此幂等去重）。
    rid = os.environ.get("CT_REQUEST_ID") or ""
    if rid:
        if args is not None:
            try: args.request_id = rid
            except Exception: pass
        return rid
    rid = os.environ.get("CT_REGISTRY_REQUEST_ID") or ""
    if rid:
        if args is not None:
            try: args.request_id = rid
            except Exception: pass
        return rid
    import uuid as _uuid
    rid = _uuid.uuid4().hex
    if args is not None:
        try: args.request_id = rid
        except Exception: pass
    return rid


def _attach_coze_contract(payload, args):
    """ct-base coze_io_contract §1.1 / §1.2 / §1.3：在出站 payload 注入统一信封字段。

    - skill_version：顶层（与 query_origin 同级），读 SKILL.md version:
    - user_language：params 子对象，由 resolve_user_language 三级判定（按用户输入文本）
    - entry_point（§1.3/§2.3，2026-10-07）：顶层，写入飞书独立列 entry_point
    - request_id（0.5.02，2026-11-11）：顶层，写入飞书独立列 request_id——同一次
      用户请求的多行记录（内部 escalation/fallback 重发）共享同一 ID，治理判重
      按 (request_id, call_type) 聚合，替代时间窗猜测。
    幂等：重复调用不重复嵌套；不影响既有检索字段。
    """
    if "skill_version" not in payload:
        payload["skill_version"] = _skill_version()
    if "entry_point" not in payload:
        payload["entry_point"] = entry_point()
    if "request_id" not in payload:
        payload["request_id"] = _request_id(args)
    q = (args.q or args.who_title or args.who_condition
         or args.who_sponsor or args.who_intervention or "")
    params = payload.get("params")
    if not isinstance(params, dict):
        params = {}
        payload["params"] = params
    if "user_language" not in params:
        params["user_language"] = resolve_user_language(q)
    return payload


def _map_status(status):
    """Map a ct_registry --status value to a WHO recruitment status if possible.

    WHO's recruitment_status enum is only Recruiting / All; other Chinese statuses
    (进行中 / 已完成 / ...) have no clean WHO equivalent, so we leave them generic.
    """
    if not status:
        return None
    s = status.strip()
    if s in ("招募中", "Recruiting"):
        return "Recruiting"
    return None


def build_payload(args):
    _validate_source(args)  # 治理护栏：未注册 source 拒发（detail / 程序化调用路径）
    api_source = API_SOURCE.get(args.source, "who")
    if args.mode == "detail" or args.project_list:
        # ---- detail fetch. project_list may be a JSON string OR a file path. ----
        pl = args.project_list
        if os.path.isfile(pl):
            try:
                d = json.load(open(pl, encoding="utf-8"))
            except Exception as e:
                sys.exit(f"[ictrp-extsvc][ERROR] --project-list 文件不是合法 JSON: {pl} ({e})")
            if isinstance(d, list):
                pl = d  # top-level array of records -> use directly
            elif isinstance(d, dict):
                # Prefer project_list_raw (wrapped {projects:[{project_id}]} string
                # preserved by a prior LIST call) so the endpoint can resolve details;
                # fall back to project_list / records (6-field summary) if absent.
                pl = (d.get("project_list_raw") or d.get("project_list") or d.get("records"))
                if pl is None:
                    sys.exit("[ictrp-extsvc][ERROR] --project-list 文件缺少 project_list_raw / project_list / records 字段，"
                              "无法用作 detail 输入。应指向 list 输出文件（含 project_list_raw）或 `{\"records\": [...]}` 格式。")
            else:
                pl = d
        if isinstance(pl, (list, dict)):
            pl = json.dumps(pl, ensure_ascii=False)
        payload = {"mode": "detail", "source": api_source, "project_list": pl}
        if getattr(args, "query_origin", None):
            payload["query_origin"] = args.query_origin
        return _attach_coze_contract(payload, args)

    if args.source == "chinadrugtrials":
        return _attach_coze_contract(_build_cde_payload(args, api_source), args)
    if args.source in ("isrctn", "drks", "chictr", "euctr", "ctis"):
        return _attach_coze_contract(_build_simple_payload(args, api_source), args)
    return _attach_coze_contract(_build_who_payload(args, api_source), args)


def _build_who_payload(args, api_source):
    # ---- search / combined / multi_keyword (WHO ICTRP, source="who") ----
    fields = {}
    if args.q:
        fields["keyword"] = args.q
    if args.who_title:
        fields["who_title"] = args.who_title
        if args.who_title_operator:
            fields["who_title_operator"] = args.who_title_operator
    if args.who_condition:
        fields["who_condition"] = args.who_condition
    iv = args.who_intervention or args.intr
    if iv:
        fields["who_intervention"] = iv
        if args.who_intervention_operator:
            fields["who_intervention_operator"] = args.who_intervention_operator
    sp = args.who_sponsor or args.sponsor
    if sp:
        fields["who_sponsor"] = sp
    if args.who_country:
        fields["who_country"] = args.who_country
    if args.who_phase:
        fields["who_phase"] = args.who_phase
    rs = args.who_recruitment_status or _map_status(args.status)
    if rs:
        fields["who_recruitment_status"] = rs
    if args.who_secondary_id:
        fields["who_secondary_id"] = args.who_secondary_id
    if args.who_date_start:
        fields["who_date_start"] = args.who_date_start
    if args.who_date_end:
        fields["who_date_end"] = args.who_date_end
    for b in ("who_covid19", "who_with_results", "who_rare_diseases", "who_gene_editing"):
        v = getattr(args, b, None)
        if v is not None:
            fields[b] = v

    # ---- mode selection (2026-08-14 rev: multi_keyword is the default anti-ban START point;
    #      "advanced" == combined, there is NO separate advanced mode) ----
    # Text query terms (q/title/condition/intervention/sponsor) can be folded into a single
    # multi_keyword AND. Structured filters (country/phase/date/recruitment/secondary-id/
    # booleans) ONLY take effect in combined mode.
    _q_words = args.q.split() if args.q else []
    text_terms = [v for v in (_q_words + [args.who_title, args.who_condition,
                              args.who_intervention or args.intr,
                              args.who_sponsor or args.sponsor]) if v]
    struct_filters = [v for v in (args.who_country, args.who_phase, args.who_date_start,
                                   args.who_date_end, rs, args.who_secondary_id) if v]
    if args.mode == "multi_keyword" or args.multi_keywords:
        mode = "multi_keyword"
        fields["multi_keywords"] = args.multi_keywords or args.q or " ".join(text_terms)
    elif args.mode:
        mode = args.mode
    elif struct_filters:
        mode = "combined"
    elif len(text_terms) >= 2:
        mode = "multi_keyword"
        fields["multi_keywords"] = " ".join(text_terms)
    else:
        mode = "search"

    # multi_keyword mode honors ONLY `multi_keywords`; drop the individual who_* TEXT fields
    # so the unified endpoint does NOT treat them as combined structured filters.
    if mode == "multi_keyword":
        for k in ("who_title", "who_title_operator", "who_condition", "who_intervention",
                  "who_intervention_operator", "who_sponsor", "keyword"):
            fields.pop(k, None)

    # ── WHO combined 模式合同约束（2026-09-06 实测根因修复）──
    # 统一端点 WHO combined 仅认 who_country / who_phase / who_date_* / who_sponsor /
    # who_secondary_id / who_recruitment_status 为"真筛选"；who_condition / who_intervention
    # / who_title 不算。若 combined 仅含文本字段（disease+drug 主路径），后端返回内层
    # error「combined 模式必须至少带一个筛选…」并 0 条。故显式降级为 search 自由词模式，
    # 用文本词构造关键词（实测 578~706 条，覆盖更全），避免静默 0 条。
    if api_source == "who" and mode == "combined":
        _real_filters = ("who_country", "who_phase", "who_date_start", "who_date_end",
                         "who_sponsor", "who_secondary_id", "who_recruitment_status")
        if not any(fields.get(k) or getattr(args, k, None) for k in _real_filters):
            _kt = [v for v in (args.q, args.who_title, args.who_condition,
                               args.who_intervention or args.intr,
                               args.who_sponsor or args.sponsor) if v]
            _kw = " ".join(_kt) if _kt else fields.get("keyword")
            # 清除残留 who_* 文本字段与 multi_keywords，避免 combined 语义泄漏到 search
            for _k in ("who_title", "who_title_operator", "who_condition",
                       "who_intervention", "who_intervention_operator",
                       "who_sponsor", "multi_keywords"):
                fields.pop(_k, None)
            if _kw:
                fields["keyword"] = _kw
            mode = "search"
            print("[ictrp-extsvc][WHO-COMBINED-FALLBACK] WHO combined 仅含 "
                  "condition/intervention/title（非真筛选），后端会校验失败返回 0 条；"
                  "已自动降级为 search 自由词模式以取回数据。")

    payload = {"mode": mode, "source": api_source}
    payload.update(fields)
    if args.max_pages:
        payload["max_pages"] = args.max_pages
    elif args.max:
        payload["max_pages"] = max(1, (args.max + 9) // 10)
    # C 层（2026-09-06）：断点续抓 + 显式翻页开关透传（服务端 who_search_node 配套支持）
    if getattr(args, "page_start", None):
        payload["page_start"] = int(args.page_start)
    if getattr(args, "paginate_all", None):
        payload["paginate_all"] = True
    if getattr(args, "query_origin", None):
        payload["query_origin"] = args.query_origin
    return payload


def _build_cde_payload(args, api_source):
    # ---- CDE search via unified endpoint (source="chinadrugtrials") ----
    # VERIFIED 2026-08-14 (3 variants, raw POST A/B): the unified CDE node ONLY honors
    # free-text `keyword`. Sending structured fields (drugs_name / indication /
    # appliers / trial_status / ...) makes the node build
    # `searchlist.dhtml?<field>=...` GET URLs that the LIVE CDE site's advanced-search
    # FORM ignores -> 0 records (returns 0 even when `keyword` is also present).
    # coze's own self-test uses `keyword` only, hence "normal". This is the root cause
    # of `ct_registry.py --cde --cde-drugs-name ...` always returning 0 (calling-method
    # bug, NOT upstream). FIX: fold every supplied CDE field into the free-text
    # `keyword` (space-joined) and emit ONLY `keyword` (+ mode). Do NOT emit
    # is_advanced_search or the individual structured fields for the unified endpoint.
    # Field-level AND precision is approximated by CDE's substring match across
    # 药物名称 / 适应症 / 题目 fields. multi_keyword mode keeps wide queries small.
    terms = []
    if args.q:
        terms.append(args.q)
    for cli in ["reg_no", "indication", "case_no", "drugs_name", "drugs_type",
                "appliers", "communities", "researchers", "agencies", "trial_status"]:
        v = getattr(args, cli, None)
        if v:
            terms.append(v)
    keyword = " ".join(terms).strip()
    fields = {}
    if keyword:
        fields["keyword"] = keyword
    if args.multi_keywords:
        # explicit multi-keyword AND (space-separated); fold CLI fields in too
        fields["multi_keywords"] = (keyword + " " + args.multi_keywords).strip() if keyword else args.multi_keywords
        mode = "multi_keyword"
    elif len(terms) > 1 and args.mode != "combined":
        # several structured terms -> multi_keyword AND keeps the result set small
        mode = "multi_keyword"
        fields["multi_keywords"] = keyword
    elif args.mode:
        mode = args.mode
    else:
        mode = "search"
    payload = {"mode": mode, "source": api_source}
    payload.update(fields)
    # 静默降级参数（CDE 中文检索 0 条时自动补发英文）
    if getattr(args, "silent_fallback", False):
        payload["silent_fallback"] = True
    if getattr(args, "fallback_keyword", None):
        payload["fallback_keyword"] = args.fallback_keyword
    if args.max_pages:
        payload["max_pages"] = args.max_pages
    elif args.max:
        payload["max_pages"] = max(1, (args.max + 9) // 10)
    if getattr(args, "query_origin", None):
        payload["query_origin"] = args.query_origin
    return payload


def _build_simple_payload(args, api_source):
    # ---- search / multi_keyword (ISRCTN / DRKS / ChiCTR via unified endpoint) ----
    # These national registries have NO clean public search API of their own
    # (ISRCTN query API 404 + JS page; DRKS JS/redirect; ChiCTR no API). The unified
    # Coze workflow serves them with a simple free-text `keyword` search (optionally
    # multi_keyword AND). No structured WHO/CDE fields are used. The backend returns
    # records shaped for the matching normalize adapter (ISRCTN -> isrctn/title/...;
    # DRKS -> drks_id/title/...; CHICTR -> registry_id/title/url).
    fields = {}
    if args.q:
        fields["keyword"] = args.q
    if args.multi_keywords:
        fields["multi_keywords"] = args.multi_keywords
    mode = "multi_keyword" if args.multi_keywords else "search"
    payload = {"mode": mode, "source": api_source}
    payload.update(fields)
    if args.max_pages:
        payload["max_pages"] = args.max_pages
    elif args.max:
        payload["max_pages"] = max(1, (args.max + 9) // 10)
    else:
        # 2026-09-08：慢响应源默认翻页收敛。EU-CTR 单页实测 ~13s、CTIS ~9s，
        # 节点侧默认 10 页会累积 100~130s+（易撞网关/客户端超时）；显式 --max-pages 可覆盖。
        if api_source in ("euctr", "ctis"):
            payload["max_pages"] = 3 if api_source == "euctr" else 2
            # EU-CTR 每页 20 条 → 3 页 ≈ 60 条；CTIS 每页 50 条 → 2 页 ≈ 100 条
            if args.source == "ctis" and not getattr(args, "quiet", False):
                print("[ictrp-extsvc][NOTE] CTIS 默认仅取前 2 页（~100 条）；需要更多请显式 --max-pages")

    # C 层（2026-09-06）：断点续抓 + 显式翻页开关透传（服务端 who_search_node 配套支持）
    if getattr(args, "page_start", None):
        payload["page_start"] = int(args.page_start)
    if getattr(args, "paginate_all", None):
        payload["paginate_all"] = True
    if getattr(args, "query_origin", None):
        payload["query_origin"] = args.query_origin
    return payload


def print_preview(payload, token, out, endpoint):
    print("[ictrp-extsvc][PREVIEW] No network request will be made. Add --run to execute.")
    print(f"[ictrp-extsvc][PREVIEW] Endpoint : {endpoint}")
    print("[ictrp-extsvc][PREVIEW] Auth     :",
          "Bearer <token set>" if token else "none (endpoint returns 401)")
    print(f"[ictrp-extsvc][PREVIEW] Payload:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"[ictrp-extsvc][PREVIEW] Output   : {out}")


def _resolve_out_path(out):
    """Normalize the --out path and ensure its parent directory exists.

    Robustness fix (2026-08-09): when the caller passes a POSIX-style path
    produced by Git Bash (e.g. `/tmp/ct_retest/A.json`), native Windows Python
    resolves it to `C:\\tmp\\ct_retest\\A.json`. If that directory does not
    exist the write fails with a raw traceback. We abspath + expanduser and
    create the parent dir up front so the write always lands somewhere
    predictable (and on Windows the POSIX path is anchored to the CWD drive).
    """
    p = os.path.expanduser(out)
    p = os.path.abspath(p)
    parent = os.path.dirname(p)
    if parent:
        try:
            os.makedirs(parent, exist_ok=True)
        except OSError:
            pass  # best-effort; the open() below will surface a clear error
    return p


# --fetch-mode both (2026-08-12): list-then-detail in ONE invocation.
# Lists with more than this many records skip auto-detail (cost / timeout guard),
# matching the CDE _run_cde_detail skip logic in ct_registry.py.
BOTH_DETAIL_LIMIT = 100


def _detail_out_path(out):
    """For --fetch-mode both: derive the detail-output path from the list-output path."""
    base, ext = os.path.splitext(out)
    return base + "_detail" + ext


def _read_project_list_raw(out):
    """Read a prior list output JSON and return its project_list_raw (wrapped string),
    or fall back to re-serializing its `records` list. None if unreadable / empty."""
    try:
        with open(out, encoding="utf-8") as f:
            obj = json.load(f)
    except Exception:
        return None
    raw = obj.get("project_list_raw")
    if isinstance(raw, str) and raw.strip():
        return raw
    recs = obj.get("records")
    if isinstance(recs, list) and recs:
        return json.dumps(recs, ensure_ascii=False)
    return None


def _read_record_count(out):
    """Read `total` (record count) from a prior list output JSON. None if unreadable."""
    try:
        with open(out, encoding="utf-8") as f:
            obj = json.load(f)
        return obj.get("total")
    except Exception:
        return None


def _resolve_fetch_mode(args):
    """Map CLI to one of list/detail/both.

    Legacy (no --fetch-mode): detail when --mode detail or --project-list is set,
    else list. --fetch-mode always wins when supplied.
    """
    if args.fetch_mode:
        return args.fetch_mode
    if args.mode == "detail" or args.project_list:
        return "detail"
    return "list"


def _write_out_json(out, obj):
    """Write the result dict as JSON; surface a clear error instead of a raw traceback."""
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        print(f"[ictrp-extsvc][ERROR] 无法写入输出文件 {out}: {e}")
        print(f"[ictrp-extsvc][ERROR] 请检查路径/父目录是否存在、是否有写权限；"
              f"建议改用绝对路径（如 C:/Users/you/out.json）。")
        return False


def _write_timeout_ictrp(out, source_label, timeout, phase):
    """统一写 is_timeout=True 占位输出（提交/轮询阶段超时共用），含高级检索建议菜单。"""
    out_obj = {
        "source": source_label,
        "records": [],
        "total": 0,
        "total_available": None,
        "total_count_reported": None,
        "error_msg": f"timeout after {timeout}s (Coze search exceeded wait limit)",
        "project_list_raw": None,
        "is_timeout": True,
        # 结构化建议：供代理（agent）转达为交互菜单。高级检索由代码实现，
        # 用户无需手动操作字段——代理把复合关键字按 药物→who_intervention /
        # 疾病→who_condition / 申办方→who_sponsor 拆分后，以 combined 模式发起，
        # 服务端做字段级 AND 过滤，返回量更小、通常更快。
        "suggestion": "advanced_combined_search",
        "suggestion_detail": (
            "可改用 WHO 高级检索（combined 模式，由代码实现）：把复合关键字按 "
            "药物→who_intervention、疾病→who_condition、申办方→who_sponsor 拆分，"
            "服务端做字段级 AND 过滤，返回量更小、通常更快。用户无需手动操作字段，"
            "由代理（agent）通过 ct_registry.py --who-mode combined 或 "
            "search_ictrp.py --mode combined 发起。注意：WHO 站点设定可能导致高级检索"
            "漏掉部分记录，若需最全覆盖可再用普通检索交叉验证。"),
    }
    if not _write_out_json(out, out_obj):
        return
    print(f"[ictrp-extsvc][TIMEOUT] Coze 检索超过 {timeout}s 仍未返回，已超时退出（is_timeout=True）。")
    print(f"[ictrp-extsvc][GUIDE] 数据可能不全。可选项（由代理转达为菜单，二选一/跳过）：")
    print(f"[ictrp-extsvc][GUIDE]   ① 改用 WHO 高级检索（combined 模式，代码自动拆分关键字做服务端 AND 过滤，返回量更小更快）")
    print(f"[ictrp-extsvc][GUIDE]   ② 缩小 / 更换关键字后重试")
    print(f"[ictrp-extsvc][GUIDE]   ③ 跳过 WHO，用其他已检索源（CT.gov / EU-CTR / CDE 等）出报告")


def _parse_response(data, source_label, payload, out, http_status=200, is_timeout=False):
    """把 Coze 响应解析为输出对象并落盘；同步分支与异步 completed 分支共用。"""
    # project_list shape:
    #   search/combined/multi_keyword -> a JSON STRING whose inner object holds
    #     {"total_count":N, "total_records":M, "projects":[...]}  (projects = records)
    #   detail                        -> a list of records (already JSON)
    pl = data.get("project_list")
    records = []
    total_available = None
    inner = None  # may stay None when project_list is dict-wrapped (detail mode)
    if isinstance(pl, str):
        try:
            inner = json.loads(pl)
        except Exception:
            inner = None
            print("[ictrp-extsvc][WARN] project_list not valid JSON; storing empty records.")
        if isinstance(inner, dict):
            total_available = inner.get("total_records")  # grand total available (e.g. 28933)
            pl = inner.get("projects") or inner.get("records")
        elif isinstance(inner, list):
            pl = inner
    elif isinstance(pl, dict):
        # detail mode may return a dict-wrapped project_list directly
        inner = pl
        total_available = pl.get("total_records") or pl.get("total_count")
        pl = pl.get("projects") or pl.get("records")
    if isinstance(pl, list):
        records = pl
    # fallback: records / projects at top level (some detail responses)
    if not records:
        fb = data.get("records") or data.get("projects")
        if isinstance(fb, list):
            records = fb
    # ---- detail-mode enrichment: prefer scraped_data_json (65-field detail) ----
    sdj = data.get("scraped_data_json")
    if sdj:
        try:
            parsed = json.loads(sdj) if isinstance(sdj, str) else sdj
            det = (parsed.get("projects") or parsed.get("records") or parsed
                   if isinstance(parsed, dict) else parsed) if not isinstance(parsed, list) else parsed
            if isinstance(det, list) and det:
                records = det
        except Exception:
            pass
    project_list_raw = data.get("project_list") if isinstance(data.get("project_list"), str) else None
    # 后端常把错误塞进 project_list 内层 JSON（如 WHO combined 校验失败：
    # 「combined 模式必须至少带一个筛选…」），而非顶层 error_msg。提升到 error_msg
    # 避免静默 0 条；同时供编排层据 error_msg 判定该源失败并优雅降级。
    if isinstance(inner, dict):
        _inner_err = inner.get("error")
        if _inner_err and not data.get("error_msg"):
            data = dict(data)
            data["error_msg"] = _inner_err
            print(f"[ictrp-extsvc][BACKEND-ERROR] {_inner_err}")
    # ── WHO/源后端抓取失败显式标记（2026-10-23 诊断补强）──────────────────────
    # 当 Coze 抓手（Playwright）在源门户等不到检索表单/超时，会把错误塞进
    # error_msg / log（如 "Page.fill: Timeout ... waiting for locator("#TextBox1")"）。
    # 此时 0 条是「源后端不可用」（WHO 门户 502 宕机 / WAF 拦截 / 节点故障），
    # 不是真实零结果，也绝非用户本机 IP 被封（链路是 用户机→Coze→源，源看到的是
    # Coze 的 IP）。显式置 who_down / source_likely_down 并改写 error_msg 为可读提示 +
    # 替代源清单，供编排层/用户直接判断，避免把 0 条误读成「无结果/被禁」。
    _BACKEND_ERR_SIG = ("Page.fill", "waiting for locator", "#TextBox", "playwright",
                        "net::", "element is not attached", "selector",
                        "Timeout 30000ms", "navigation timeout", "scrape")
    _err_blob = " ".join(str(x) for x in (data.get("error_msg") or "", data.get("log") or ""))
    _is_backend_err = bool(_err_blob) and any(s in _err_blob for s in _BACKEND_ERR_SIG)
    _src = (payload.get("source") if isinstance(payload, dict) else None) or "who"
    if _is_backend_err and not records:
        _backend_down_label = "WHO ICTRP" if _src == "who" else source_label
        _alt = ("CT.gov / EU-CTR（Tier-1 直连）" if _src == "who"
                else "CDE(chinadrugtrials) / CT.gov / EU-CTR")
        _who_down_msg = (f"{_backend_down_label} 检索后端抓取失败（Coze 抓手在源门户等不到检索表单/"
                         f"超时，原始错误见 error_msg / log）。这通常是源门户临时宕机或拦截，并非真实零结果，"
                         f"也非你的 IP 被封——是你的机器连 Coze、Coze 再去连源，源看到的是 Coze 的 IP。"
                         f"请稍后重试，或先用替代源：{_alt}。")
        data = dict(data)
        data["error_msg"] = _who_down_msg
        _WHO_DOWN_DETECTED = True
        print(f"[ictrp-extsvc][WHO-DOWN] ⚠️ {_who_down_msg}")
    else:
        _WHO_DOWN_DETECTED = False
    if not records and http_status == 200 and not data.get("error_msg"):
        print(f"[ictrp-extsvc][WARN] 0 records returned for source={source_label} "
              f"despite HTTP 200 and no error_msg. This is usually a TRANSIENT "
              f"scrape miss by the unified workflow (same query often recovers on "
              f"re-run), NOT a genuine zero-result — OR the source backend node is "
              f"currently down (ChiCTR has been observed returning empty repeatedly). "
              f"Downstream will simply lack this source; re-run or use an alternative "
              f"source (CDE for China).")
    req_pages = payload.get("max_pages") if isinstance(payload, dict) else None
    if req_pages and records:
        approx_cap = req_pages * 10
        if len(records) > approx_cap:
            print(f"[ictrp-extsvc][WARN] returned {len(records)} records but "
                  f"max_pages={req_pages} was requested (~{approx_cap} expected). "
                  f"The unified endpoint IGNORES max_pages and returns the full "
                  f"match — `--max` is NOT enforced for Coze sources "
                  f"(CDE/WHO/ChiCTR/ISRCTN/DRKS). Narrow the keyword to reduce volume.")
    out_obj = {
        "source": source_label,
        "records": records,
        "total": len(records),
        "total_available": total_available,
        "total_count_reported": data.get("total_count"),
        "error_msg": data.get("error_msg"),
        "project_list_raw": project_list_raw,
        "is_timeout": is_timeout,
        # 0 条 + 200 + 无错误：疑似后端节点故障（非真实零结果），标记供编排层披露
        "empty_no_error": (not records and http_status == 200 and not data.get("error_msg")),
        # 2026-10-23 诊断补强：源后端抓取失败（Playwright 超时等）显式标注，避免静默 0 条
        "who_down": (_WHO_DOWN_DETECTED and _src == "who"),
        "source_likely_down": _WHO_DOWN_DETECTED,
        "escalate_to_combined": inner.get("escalate_to_combined") if isinstance(inner, dict) else None,
        "large_result_set": inner.get("large_result_set") if isinstance(inner, dict) else None,
        "is_partial": (inner.get("is_partial", False) if isinstance(inner, dict) else False),
        "log": data.get("log", ""),
        "query_origin": data.get("query_origin", ""),
    }
    # ── P1-2（2026-11-11）：keyword_localization 完整透传 ──────────────────────
    # 内层 dict（CDE/ChiCTR 节点输出）可能带关键词本地化记录数组（翻译确认门契约，
    # 见 ct-base bilingual_retrieval.md §5）。此前仅字符串形态经 project_list_raw
    # 保留、dict 形态被丢弃 → 上层确认卡拿不到数据。此处以 dict 形态透传。
    _kl = inner.get("keyword_localization") if isinstance(inner, dict) else None
    if isinstance(_kl, list) and _kl:
        out_obj["keyword_localization"] = _kl
    # P1-followup (2026-08-12): surface partial-result gaps so the user knows they did
    # NOT get the full result set (unified gateway may return only part of a wide query).
    if out_obj.get("large_result_set"):
        out_obj["error_msg"] = out_obj.get("error_msg") or (
            "结果集过大（>WHO_RESULT_CEILING），已停止检索并避免翻页封禁。"
            "请加窄筛选字段（--who-condition/--who-country/--who-phase/--who-recruitment-status）后重试。")
        print(f"[ictrp-extsvc][LARGE-RESULT-SET] ⚠️ coze 回 large_result_set："
              f"combined 仍超阈值，已停止。{out_obj['error_msg']}")
    if total_available and isinstance(total_available, int) and len(records) < total_available:
        _gap = total_available - len(records)
        print(f"[ictrp-extsvc][PARTIAL] ⚠️ 仅取回 {len(records)} 条 / 共 {total_available} 条"
              f"（缺口 {_gap} 条）。统一网关对宽检索可能只返回部分结果；"
              f"建议缩小关键词或改用 --mode combined 字段过滤后重跑。")
    if not _write_out_json(out, out_obj):
        return None
    print(f"[ictrp-extsvc] {len(records)} records -> {out} "
          f"(total_count={out_obj['total']})")
    if data.get("log"):
        print(f"[ictrp-extsvc][LOG] {data['log']}")
    return out_obj


def _finalize_async_ictrp(source_label, endpoint_base, data, out, timeout, run_id, payload):
    """解析 /run/status 的最终结果（兼容两种返回形态）。"""
    if data.get("status") == "failed":
        sys.exit(f"[ictrp-extsvc][ERROR] remote run failed: {data.get('error')}")
    if data.get("status") == "cancelled":
        _write_timeout_ictrp(out, source_label, timeout, "cancelled")
        return
    # completed：data 可能是 {status, result} 或直接是 result dict
    result = data.get("result", data)
    is_timeout = bool(result.get("is_timeout"))
    _parse_response(result, source_label, payload, out, http_status=200, is_timeout=is_timeout)




def run(payload, token, out, timeout, endpoint, source_label, use_stream=False, args=None):
    """检索（含升级反馈环）：multi_keyword→combined 逐级收敛大结果集，combined 仍超限即报错。

    收到 coze 端 escalate_to_combined 信号时，自动构造 combined payload 重发；收到
    large_result_set 信号时停止并报错。最多 MAX_WHO_ESCALATION 次。目的：避免单次超宽
    检索硬翻数十页触发 WHO 限流/封禁（详见 coze/WHO_SEARCH_OPTIMIZATION.md §0.6）。

    ChiCTR WAF 自动切换：当 source=chictr 被判 `source_likely_down`（阿里云 WAF
    acw_sc__v2 拦截 / 后端节点故障）且 `--no-fallback-who` 未关闭时，自动改用 WHO
    ICTRP 线路（同一 keyword）专查 ChiCTR 来源记录回填，详见 `_fallback_who_for_chictr`。
    `args`（可选）用于取回 --no-fallback-who / 关键词 / max_pages 等 CLI 上下文。
    """
    out = _resolve_out_path(out)
    last_out = None
    cur_payload = payload
    # WHO 端只认英文：中文 keyword / multi_keywords 先本地化为英文（term_map → online）。
    # 覆盖直接 --source who --keyword 中文 与 ct_registry --with-ictrp 主路径。
    if payload.get("source") == "who":
        _who_metas = _localize_who_payload(cur_payload, args)
        _who_loc_recs = _gate_records_from_who_metas(_who_metas)
    else:
        _who_loc_recs = []
    for depth in range(MAX_WHO_ESCALATION + 1):
        last_out = _run_once(cur_payload, token, out, timeout, endpoint, source_label, use_stream)
        if last_out is None:
            return None
        if _who_loc_recs:
            # P1-2：WHO 本地化记录并入信封（补写盘——_run_once 落盘在前）
            merged = last_out.get("keyword_localization") or []
            last_out["keyword_localization"] = merged + \
                [r for r in _who_loc_recs if r not in merged]
            _write_out_json(out, last_out)
        # 已取到数据：不再因 escalate 信号丢弃已有结果。网关的 escalate_to_combined 是
        # 「结果过大请收窄」的**建议**，部分结果（如一页 10 条 / 共 578）远优于升级失败
        # 后覆盖成的 0 条。需要更全集时，由调用方改用 --mode combined + 真筛选重发。
        _n = len(last_out.get("records") or [])
        if _n > 0:
            if last_out.get("escalate_to_combined"):
                print(f"[ictrp-extsvc][NO-ESCALATE] 已取 {_n} 条，忽略 escalate 信号"
                      f"（避免升级失败丢失已有数据；如需更全请用 --mode combined + 真筛选）。")
            return last_out
        if depth >= MAX_WHO_ESCALATION:
            break
        if last_out.get("escalate_to_combined"):
            np = _escalate_payload(cur_payload, "combined")
            if np is None:
                break
            cur_payload = np
            print(f"[ictrp-extsvc][ESCALATE] search 0 条 → 升级 combined 重发（depth {depth + 1}）")
            continue
        # combined 仍超限（coze 回 large_result_set）-> 循环自然结束，最后 out_obj 带报错标记
        break
    # ===== WHO-COVERED 源兜底（chictr/isrctn/drks/euctr）：原站点不通 → 合并检索源(WHO ICTRP)备用 =====
    # 设计原则（对齐 ct-base §14.2 / §14.3）：
    #   (1) 凡 WHO ICTRP 镜像覆盖的源，原站点不通（迁移 / WAF 拦截 / 节点故障 / 显式 error）
    #       时，应改用 WHO ICTRP 线路取回该源来源记录作为备用方式，而非静默 0 条；
    #   (2) 凡确实站点异常（非真实零结果），必须返回明确提示信息（error_msg / note），
    #       不得把「源不可用」伪装成「无结果」。
    # 判定「原站点不通」：节点显式报错（error_msg 非空）→ 直接判定；否则（0+无错误歧义）
    #   用对照词探针 `_control_probe` 区分真实零结果 vs 节点故障。
    if (last_out and not (last_out.get("records") or [])
            and payload.get("source") in _SOURCE_ID_RE):
        _src = payload["source"]
        _explicit_err = bool(last_out.get("error_msg"))
        if _explicit_err:
            # 节点已显式报站点异常（DRKS 迁移 / ISRCTN 拦截 / 抓取失败…）→ 原站点不通，
            # 跳过对照探针直接走 WHO 兜底（节省一次对照词调用）。
            _down = True
            print(f"[ictrp-extsvc][SOURCE-DOWN] {source_label} 节点显式报错，判定原站点不通："
                  f"{last_out.get('error_msg')!r}")
        elif last_out.get("empty_no_error"):
            _down = _control_probe(_src, token, endpoint, timeout)
        else:
            _down = None
        if _down is True:
            if not _explicit_err:
                last_out["error_msg"] = (last_out.get("error_msg") or
                    f"{source_label} 后端节点疑似故障：对照词（{CONTROL_TERMS.get(_src)}）"
                    f"亦返回 0+无错误，判定为源不可用而非真实零结果。请以其他源覆盖"
                    f"（查中国用 CDE；查全球用 CT.gov / WHO）。")
            last_out["source_likely_down"] = True
            _write_out_json(out, last_out)
            # ---- 自动切换 WHO ICTRP 线路专查该源来源记录（合并检索源兜底）----
            if getattr(args, "fallback_who", True):
                chi, who_out = _fallback_who_for_source(
                    payload, _src, token, endpoint, timeout, source_label, args)
                last_out["fallback_attempted"] = True
                if chi:
                    # WHO 线路取回该源记录 → 数据可用，清除故障标记、保留 provenance 提示
                    last_out["records"] = chi
                    last_out["total"] = len(chi)
                    last_out["source_likely_down"] = False
                    last_out["empty_no_error"] = False
                    last_out["error_msg"] = None
                    last_out["fallback_used"] = "who_ictrp"
                    last_out["fallback_reason"] = f"{_src}_down"
                    last_out[f"{_src}_records_via_who"] = len(chi)
                    last_out["note"] = (f"{source_label} 直连不可用（{last_out.get('log') or '原站点异常'}），"
                                        f"已自动切换 WHO ICTRP 线路并筛出 {_src.upper()} 来源记录"
                                        f"（合并检索源兜底）。")
                    print(f"[ictrp-extsvc][FALLBACK-WHO] ✅ 已从 WHO 线路取回 {len(chi)} 条 "
                          f"{_src.upper()} 记录（覆盖原故障结果）。")
                    _write_out_json(out, last_out)
                else:
                    who_err = (who_out or {}).get("error_msg")
                    last_out["fallback_who_status"] = "who_error" if who_err else f"no_{_src}_in_who"
                    if who_err:
                        last_out["error_msg"] = (last_out.get("error_msg") or "") \
                            + f" [WHO 回退亦失败: {str(who_err)[:200]}]"
                    # 站点异常 + WHO 也无该源记录 → 保留明确提示，绝不伪装成无结果
                    print(f"[ictrp-extsvc][FALLBACK-WHO] WHO 线路"
                          f"{'亦报错' if who_err else '正常返回但无 ' + _src.upper() + ' 来源记录'}；"
                          f"维持源不可用标记，返回明确提示。查中国请用 CDE；查全球请用 CT.gov。")
                    _write_out_json(out, last_out)  # 持久化 fallback_attempted/fallback_who_status/error_msg
        elif _down is False:
            print(f"[ictrp-extsvc][SOURCE-OK] {source_label} 对照探针有数据 → "
                  f"本次 0 条为真实零结果（非源故障，不触发 WHO 兜底）。")
    return last_out


# ===== WHO-COVERED 源自动切换 WHO 线路（2026-09-07 新增，chictr 起步、泛化三源）=====
# WHO ICTRP 镜像 14+ 注册库（含 ChiCTR/ISRCTN/DRKS），当某 WHO-COVERED 简单源
# （chictr/isrctn/drks，经统一端点直连）被 WAF 拦截 / 后端节点故障（0 条 +
# source_likely_down）时，改用 WHO ICTRP 线路（同一 keyword）专查该源来源记录回填。
# 每源用各自的注册号正则甄别 WHO 记录是否源自该注册库。
_CHICTR_ID_RE = re.compile(r"ChiCTR(?:-[A-Za-z]{2,4})?-?\d{8,12}", re.IGNORECASE)
_ISRCTN_ID_RE = re.compile(r"ISRCTN\d{8}", re.IGNORECASE)
_DRKS_ID_RE = re.compile(r"DRKS\d+", re.IGNORECASE)
# EUCTR/EudraCT 号：YYYY-NNNNNN-NN（同形态亦为 CTIS 的 EU trial number，但 CTIS
# 新试验不在 WHO 镜像，故只给 euctr 登记 fallback，ctis 不登记）
_EUCTR_ID_RE = re.compile(r"\b\d{4}-\d{6}-\d{2}\b", re.IGNORECASE)
# source → 该源在 WHO 记录里识别用的正则（仅 WHO-COVERED 源登记；
# CTIS 非 WHO 一级注册机构镜像，无 WHO fallback）
_SOURCE_ID_RE = {
    "chictr": _CHICTR_ID_RE,
    "isrctn": _ISRCTN_ID_RE,
    "drks": _DRKS_ID_RE,
    "euctr": _EUCTR_ID_RE,
}


def _source_record_check(rec, src):
    """判一条 WHO/ICTRP 记录是否源自 WHO-COVERED 源 `src`（chictr/isrctn/drks/euctr）。

    WHO 镜像记录未必直接带 registry 字段，故三重兜底：
      (1) registry/source_registry/... 字段含该源名（chictr→'chictr'、isrctn→'isrctn'、
          drks→'drks'、euctr→'euctr'/'eudract'，各按子串匹配）；
      (2) 注册号字段（Main ID/登记号/registry_id/...）匹配该源注册号正则；
      (3) 整条 raw 文本含该源注册号（最兜底）。
    任一命中即视为该源来源。
    """
    if not isinstance(rec, dict):
        return False
    name = {"chictr": "chictr", "isrctn": "isrctn", "drks": "drks",
            "euctr": "euctr"}.get(src, src)
    reg = (rec.get("registry") or rec.get("source_registry") or rec.get("trial_registry")
           or rec.get("primary_registry") or rec.get("registry_name") or "").strip()
    # euctr 在 WHO 记录里常写 "EUCTR" / "EudraCT"，统一按 euctr|eudract 匹配
    if (name in reg.lower()) or (src == "euctr" and "eudract" in reg.lower()):
        return True
    id_re = _SOURCE_ID_RE.get(src)
    if id_re is None:
        return False
    for k in ("main_id", "registration_number", "registry_id", "登记号", "Main ID",
              "project_id", "trial_id", "id", "secondary_id", "primary_id"):
        v = rec.get(k)
        if isinstance(v, str) and id_re.search(v):
            return True
    raw = rec.get("raw")
    if isinstance(raw, dict):
        raw_s = json.dumps(raw, ensure_ascii=False)
    elif isinstance(raw, str):
        raw_s = raw
    else:
        raw_s = json.dumps(rec, ensure_ascii=False)
    return bool(id_re.search(raw_s))


def _fallback_who_for_source(payload, src, token, endpoint, timeout, source_label, args):
    """WHO-COVERED 简单源直连不可用 → 自动切换 WHO ICTRP 线路专查该源来源记录。

    用同一 keyword 发一次 WHO search，再从返回记录中筛出该源来源（见 `_source_record_check`），
    作为该源的替代覆盖。仅保留该源来源，保证「专查 <src> 结果」语义。

    返回 (matched_records, who_out) 二元组：
      - matched_records: 该源来源记录列表（WHO 镜像形态，source=ICTRP 以保留完整字段，
        由顶层信封 fallback_used=who_ictrp 标注其来源）；无命中时为空列表。
      - who_out: WHO 这次检索的 out_obj（含 error_msg 等），用于区分「WHO 自身也失败」
        与「WHO 正常返回但无该源命中」两种 0 条情形；调用方据此标注信封。
    """
    kw = (payload.get("keyword") or payload.get("multi_keywords")
          or (args.q if args else None))
    if not kw:
        return [], None
    who_payload = {
        "mode": "search",
        "source": "who",
        "keyword": kw,
        "max_pages": (payload.get("max_pages")
                      or (getattr(args, "max_pages", None) if args else None)
                      or 50),
    }
    # WHO 端只认英文：chictr 的 keyword 是中文，直接发 WHO 必 0 条 → 先本地化
    # 为英文（term_map 权威优先；词典 miss 的长尾词走 online 兜底并如实标注）。
    # isrctn/drks 关键词本就是英文，_localize_who_payload 对无 CJK 词原样放行。
    _fb_metas = _localize_who_payload(who_payload, args)
    if _fb_metas and who_payload.get("keyword") != kw:
        print(f"[ictrp-extsvc][FALLBACK-WHO] 关键词已中→英本地化 "
              f"({_fb_metas[0].get('original')!r} → {who_payload['keyword']!r}, "
              f"source={_fb_metas[0].get('source')})")
    try:
        who_payload = _attach_coze_contract(who_payload, args)
    except Exception:
        pass
    if args is not None and getattr(args, "query_origin", None):
        who_payload["query_origin"] = args.query_origin
    import tempfile
    tmp_path = os.path.join(tempfile.gettempdir(),
                            f"who_fb_{os.getpid()}_{int(time.time() * 1000)}.json")
    print(f"[ictrp-extsvc][FALLBACK-WHO] {source_label} 直连不可用 → 切 WHO ICTRP 线路"
          f"查 {src} 来源（keyword={kw!r}）…")
    who_out = None
    try:
        who_out = _run_once(who_payload, token, tmp_path, timeout, endpoint, "ICTRP",
                            getattr(args, "stream", True) if args else True)
    except Exception as e:
        print(f"[ictrp-extsvc][FALLBACK-WHO][WARN] WHO 回退调用异常 {e}，跳过")
        return [], None
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass
    if not who_out:
        return [], None
    _fb_recs = _gate_records_from_who_metas(_fb_metas)
    if _fb_recs:
        merged = who_out.get("keyword_localization") or []
        who_out["keyword_localization"] = merged + \
            [r for r in _fb_recs if r not in merged]
    recs = who_out.get("records") or []
    matched = [r for r in recs if _source_record_check(r, src)]
    print(f"[ictrp-extsvc][FALLBACK-WHO] WHO 命中 {len(recs)} 条，其中 {src} 来源 {len(matched)} 条")
    return matched, who_out


# 兼容别名：保留旧名，避免外部对 search_ictrp 旧 API 的引用失效
def _is_chictr_record(rec):
    return _source_record_check(rec, "chictr")


def _fallback_who_for_chictr(payload, token, endpoint, timeout, source_label, args):
    return _fallback_who_for_source(payload, "chictr", token, endpoint, timeout, source_label, args)


# ===== WHO 升级反馈环辅助函数（2026-08-14）=====
MAX_WHO_ESCALATION = 2          # multi_keyword→combined 最多 1 次升级重发（值留 2 作余量）

def _read_out_json(out):
    """读回已落盘的输出 JSON（异步轮询分支升级重发前取结果）。"""
    try:
        with open(out, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _control_probe(api_source, token, endpoint, timeout):
    """健康对照探针（仅简单源 chictr/isrctn/drks 用）。

    简单源返回「0 条 + 无错误」歧义极大。用该源**必有海量登记**的对照词发一次同步
    检索：若对照词也返回 0+无错误 → 后端节点故障（返回 True）；若对照词有数据 →
    本次 0 条是真实零结果（返回 False）；探针本身失败（网络/解析）→ 无法判定（返回 None）。

    简单源（chictr/isrctn/drks）在统一端点为**同步回包**（结果内联在 submit 响应，
    无需轮询 status），故此处直接读 submit 响应即可。
    """
    ctrl = CONTROL_TERMS.get(api_source)
    if not ctrl:
        return None
    # FIX(2026-09-06): 模块未导入 requests（本模块走 urllib/_request 通道），
    # 探针里 requests.post 抛 NameError 被 except 吞掉 → 永远返回 None、探针失效。
    # 在函数内局部导入；同时 ctrl 为 str 时不再按字符切分（ctrl[:2] 会把「肺癌」拆成「肺」「癌」）。
    import requests as _requests
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    # 逐个对照词发一次同步请求；任一对照词有数据 → 非节点故障(False)，
    # 全部对照词都空 → 后端节点疑似故障(True)；探针自身失败(网络/解析) → None。
    # FIX(2026-09-06): 旧代码把整个 ctrl 列表塞进 `keyword`(应为单字符串)，
    # 端点收 dict 而非 str 多抛异常被吞 → 探针永远返回 None、失效。
    kws = ctrl if isinstance(ctrl, (list, tuple)) else [ctrl]  # str → 单词一次
    for kw in kws[:2]:  # 取 2 个对照词已足够判定（如 metformin / 肺癌 在 ChiCTR 均海量）
        payload = {"mode": "search", "source": api_source, "keyword": kw, "max_pages": 1}
        try:
            resp = _requests.post(endpoint, headers=headers, json=payload,
                                  timeout=min(int(timeout or 60), 60))
            d = resp.json()
        except Exception:
            return None  # 探针自身失败，无法判定
        pl = d.get("project_list")
        recs = d.get("projects") or d.get("records")
        if isinstance(recs, str):
            try:
                recs = json.loads(recs)
            except Exception:
                recs = []
        if isinstance(pl, str):
            try:
                plj = json.loads(pl)
                if isinstance(plj, dict):
                    if not isinstance(recs, list) or not recs:
                        recs = plj.get("projects") or plj.get("records") or []
                    if plj.get("total_count") == 0:
                        recs = []
            except Exception:
                pass
        if isinstance(recs, list) and len(recs) > 0:
            return False  # 对照词有数据 → 非节点故障（本次 0 条是真实零结果）
    return True  # 所有对照词都空 → 后端节点疑似故障

# ===== 流式调用（/stream_run, SSE）=====
# 2026-08-14 实测结论（决定解析位置，已用真实 SSE 探测验证）：coze 对该 vibeflow 的流行为——
#   * 普通流式（不带 debug 头）：仅 workflow_start + workflow_end(output:{})，结果完全不进流 → 不可用。
#   * debug 流式（header x-workflow-stream-mode: debug）：发出 node_start/node_end；
#     主检索节点 search_node（detail 模式为 scrape_details_node）的 node_end.output
#     携带 {project_list, total_count, log}（即真正的回传参数）；workflow_end.output 恒为 {}。
# 因此流式【必须带 debug 头】，并从「主节点的 node_end.output」取结果；workflow_end 忽略。
# 取不到结果（非 debug / 流异常 / HTTP≠200）一律回退同步 /run，保证零回归。
_STREAM_DEBUG_HEADER = "x-workflow-stream-mode"
_PRIMARY_NODES = ("search_node", "scrape_details_node")


def _parse_sse(resp):
    """解析 /stream_run 的 SSE 流，取出主节点的回传参数。

    返回 (result_dict_or_None, stream_dropped, error_msg)：
      - result_dict: 主节点 node_end.output（含 project_list/total_count/log），可直接喂 _parse_response
      - stream_dropped: True 表示流中未取到任何可用结果（需回退 /run 同步）
      - error_msg: 流中 error 帧的错误文案（可能为 None）
    """
    result = None
    error_msg = None
    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue
        chunk = line[len("data:"):].strip()
        if not chunk:
            continue
        try:
            evt = json.loads(chunk)
        except Exception:
            continue
        etype = evt.get("type")
        if etype == "node_end":
            out = evt.get("output")
            nm = evt.get("node_name", "")
            if isinstance(out, dict) and (nm in _PRIMARY_NODES or "project_list" in out):
                # 主检索节点输出即最终回传参数；detail 模式下 scrape_details_node 覆盖 search_node
                result = out
        elif etype == "error":
            error_msg = evt.get("msg") or evt.get("error_message") or json.dumps(evt, ensure_ascii=False)
        # workflow_end.output 恒为 {}，忽略
    if result is None and error_msg is None:
        return None, True, None
    return result, False, error_msg


def _try_stream(payload, token, out, timeout, endpoint, source_label):
    """尝试 /stream_run（debug 模式）。成功取到结果返回 out_obj；否则返回 None（交由调用方回退 /run）。"""
    import requests
    stream_endpoint = endpoint.rsplit("/run", 1)[0] + "/stream_run"
    headers = {"Content-Type": "application/json", "Accept": "text/event-stream",
               _STREAM_DEBUG_HEADER: "debug"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    print(f"[ictrp-extsvc][STREAM] POST {stream_endpoint} (debug)")
    try:
        # ct-base §5.50：出站 payload 发送前脱敏；§5.49：代理残留自动重试
        resp = _request("POST", stream_endpoint, headers=headers,
                        json=_sanitize_payload(payload), stream=True, timeout=timeout)
    except requests.exceptions.Timeout:
        _write_timeout_ictrp(out, source_label, timeout, "submit-stream")
        return None
    except requests.RequestException as e:
        print(f"[ictrp-extsvc][STREAM][WARN] 流式请求异常 {e}，回退同步 /run")
        return None
    if resp.status_code != 200:
        print(f"[ictrp-extsvc][STREAM][WARN] /stream_run HTTP {resp.status_code}，回退同步 /run")
        return None
    result, dropped, err = _parse_sse(resp)
    if dropped:
        print("[ictrp-extsvc][STREAM][WARN] 流中无可用结果（确认 debug 头已带 / 端点支持流式），回退同步 /run")
        return None
    if err and result is None:
        print(f"[ictrp-extsvc][STREAM][ERROR-MSG] {err}")
        return None
    print("[ictrp-extsvc][STREAM] 已从主节点 node_end 取到回传参数，落盘")
    return _parse_response(result, source_label, payload, out, http_status=200)


def _run_once(payload, token, out, timeout, endpoint, source_label, use_stream=False):
    """单次提交+等待+解析（流式 /stream_run 优先，失败自动回退同步 /run），落盘并返回 out_obj；失败返回 None。"""
    # ---- 审计日志字段：把本次请求参数（不含 querystr / query_origin 自身）序列化，供 coze 端飞书 querystr 列记录 ----
    # query_origin 已由 coze 端飞书表独立列保存（ct-base §8.6），querystr 内不重复携带；
    # token 在 HTTP header（Authorization），从不进 payload；此处仅序列化检索参数，无凭据。
    if "querystr" not in payload:
        payload["querystr"] = json.dumps(
            {k: v for k, v in payload.items() if k not in ("querystr", "query_origin")},
            ensure_ascii=False, sort_keys=True)
    # ---- 流式优先（debug 模式，从主节点 node_end.output 取回传参数）----
    if use_stream:
        so = _try_stream(payload, token, out, timeout, endpoint, source_label)
        if so is not None:
            return so
        print("[ictrp-extsvc][STREAM] 回退同步 /run")
    import requests
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    else:
        print("[ictrp-extsvc][WARN] no token -> endpoint returns 401 (Bearer required)")
    # 阶段1：提交（异步协议应毫秒级返回 run_id；统一网关偶发抖动可能卡住）
    # ct-base §5.50：出站 payload 发送前脱敏；§5.49：代理残留自动重试
    # 2026-09-06 修复：提交超时（30s→60s）且最多重试 2 次，规避网关瞬时卡死导致的
    # 误判 0 条；重试用指数退避，避免对抖动端点持续施压。
    submit_resp = None
    for _attempt in range(3):
        try:
            submit_resp = _request("POST", endpoint, headers=headers,
                                   json=_sanitize_payload(payload), timeout=60)
            break
        except requests.exceptions.Timeout:
            if _attempt < 2:
                _backoff = 2 ** _attempt
                print(f"[ictrp-extsvc][WARN] 提交超时（第 {_attempt + 1}/3 次）；"
                      f"统一网关偶发抖动，{_backoff}s 后重试…")
                time.sleep(_backoff)
                continue
            _write_timeout_ictrp(out, source_label, timeout, "submit")
            return None
        except requests.RequestException as e:
            sys.exit(f"[ictrp-extsvc][ERROR] request failed: {e}")
    try:
        submit_data = submit_resp.json()
    except Exception:
        submit_data = {}
    if submit_data.get("status") == "accepted" and submit_data.get("run_id"):
        # 复用 extsvc_client 的共享轮询循环；ictrp 专属 finalize/timeout 通过回调注入，
        # 避免与共享件重复约 32 行轮询代码（P1-1 去分叉）。
        _run_async_poll(
            source_label, endpoint, token, submit_data["run_id"], out, timeout,
            finalize=lambda s, eb, d, o, t, rid: _finalize_async_ictrp(s, eb, d, o, t, rid, payload),
            on_timeout=lambda o, s, t, k: _write_timeout_ictrp(o, s, t, k),
        )
        return _read_out_json(out)
    # 同步协议分支
    print(f"[ictrp-extsvc] HTTP {submit_resp.status_code}")
    guide = _status_guidance(submit_resp.status_code)
    if guide:
        print(f"[ictrp-extsvc][GUIDE] {guide}")
    if submit_resp.status_code != 200:
        print(f"[ictrp-extsvc] body: {submit_resp.text[:600]}")
        print("[ictrp-extsvc] no successful response -> output NOT written.")
        return None
    try:
        data = submit_resp.json()
    except Exception:
        data = {"raw": submit_resp.text}
    if data.get("error_msg"):
        print(f"[ictrp-extsvc][ERROR-MSG] {data['error_msg']}")
    return _parse_response(data, source_label, payload, out, http_status=submit_resp.status_code)

def _escalate_payload(base, level):
    """构造升级重发 payload（仅 level="combined"）。无法升级时返回 None。

    multi_keyword/search 超限 -> combined：
      - 已有 who_* 结构化字段 -> 直接 mode=combined 复用。
      - 来自 multi_keyword（有 multi_keywords 自由文本）或单 keyword ->
        把自由文本词拆成 who_condition / who_intervention（前半/后半，含分隔符时），
        并加 who_recruitment_status=Recruiting 尽力收敛，mode=combined。
      精准拆分仍应由上层 ct_registry.py 用 --who-condition/--who-intervention 完成。
    """
    if level != "combined":
        return None
    p = dict(base)
    p.pop("multi_keywords", None)          # combined 模式不认 multi_keywords
    # 关键：不要把 keyword 直接丢弃——coze 端 combined 模式只认 who_* 字段、不认裸
    # keyword，若丢弃关键词会变成「仅 who_recruitment_status=Recruiting」的全库查询
    # （实测 283167 条）。必须把自由文本关键词映射成 who_condition/who_intervention
    # 才能保留过滤语义。
    if p.get("who_condition") or p.get("who_intervention") or p.get("who_country") \
            or p.get("who_phase") or p.get("who_sponsor"):
        p["mode"] = "combined"
        return p
    # 自由文本 -> 尽力拆成 who_* 字段 + Recruiting 收敛（始终保留关键词过滤）
    text = (p.get("keyword") or base.get("keyword")
            or p.get("multi_keywords") or base.get("multi_keywords") or "").strip()
    p.pop("keyword", None)                 # 已转为 who_* 字段，combined 不再发裸 keyword
    if text:
        if re.search(r"[\s,;]+", text):
            # 多词自由文本：不臆测拆分（首空格拆分会产生 "non-small" 这类无效片段），
            # 整句作 who_condition，保留完整检索语义；Recruiting 真筛选保证 combined 合法。
            p["who_condition"] = text
            print(f"[ictrp-extsvc][ESCALATE] 多词自由文本整句作 who_condition={text!r}"
                  f"（避免首空格拆分产生无效片段；精准字段拆分见 ct_registry.py）")
        else:
            # 单关键词：整词作 who_condition，保留过滤语义（避免升 combined 后变全库）
            p["who_condition"] = text
            print(f"[ictrp-extsvc][ESCALATE] 单关键词 {text!r} → who_condition={text!r}"
                  f"（启发式；精准字段拆分见 ct_registry.py）")
    if not p.get("who_recruitment_status"):
        p["who_recruitment_status"] = "Recruiting"   # 满足 coze combined 强制筛选校验
    p["mode"] = "combined"
    return p

def main():
    ap = argparse.ArgumentParser(
        description="WHO ICTRP search via external Coze workflow (Tier-2, no local browser)")
    ap.add_argument("--q", help="free-text query -> keyword (search mode)")
    ap.add_argument("--cond", dest="q", help="alias of --q (condition)")
    ap.add_argument("--intr", help="intervention -> who_intervention")
    ap.add_argument("--sponsor", help="sponsor -> who_sponsor")
    ap.add_argument("--status", help="status; mapped to who_recruitment_status when Recruiting")
    ap.add_argument("--mode", choices=["search", "combined", "multi_keyword", "detail"])
    ap.add_argument("--who-title", help="WHO title keyword")
    ap.add_argument("--who-title-operator", choices=["None", "NOT"])
    ap.add_argument("--who-condition", help="WHO health condition (override --q)")
    ap.add_argument("--who-intervention", help="WHO intervention (override --intr)")
    ap.add_argument("--who-intervention-operator", choices=["AND", "OR", "NOT"])
    ap.add_argument("--who-sponsor", help="WHO sponsor (override --sponsor)")
    ap.add_argument("--who-country", help="WHO recruiting country (comma-separated)")
    ap.add_argument("--who-phase", help="WHO phase (e.g. 'Phase 2,Phase 3')")
    ap.add_argument("--who-recruitment-status", help="WHO recruitment status (Recruiting/All)")
    ap.add_argument("--who-secondary-id", help="WHO secondary ID (e.g. an ISRCTN number)")
    ap.add_argument("--who-date-start", help="WHO reg date start (DD/MM/YYYY)")
    ap.add_argument("--who-date-end", help="WHO reg date end (DD/MM/YYYY)")
    ap.add_argument("--who-covid19", type=lambda x: str(x).lower() == "true",
                    help="boolean: COVID-19 studies only")
    ap.add_argument("--who-with-results", type=lambda x: str(x).lower() == "true",
                    help="boolean: studies with results only")
    ap.add_argument("--who-rare-diseases", type=lambda x: str(x).lower() == "true",
                    help="boolean: rare-disease / orphan-drug studies only")
    ap.add_argument("--who-gene-editing", type=lambda x: str(x).lower() == "true",
                    help="boolean: gene-editing studies only")
    ap.add_argument("--multi-keywords", help="multi_keyword mode: space-separated AND terms")
    ap.add_argument("--keyword", dest="q", help="alias of --q (free-text keyword)")
    ap.add_argument("--source", choices=["who", "chinadrugtrials", "isrctn", "drks", "chictr",
                                         "euctr", "ctis"],
                    default="who",
                    help="unified endpoint source selector: 'who' (WHO ICTRP, default), "
                         "'chinadrugtrials' (China CDE), 'isrctn'/'drks'/'chictr' "
                         "(national registries WHO covers, retrievable independently when "
                         "WHO cannot — used by the ct_registry fallback), "
                         "'euctr' (EU EudraCT legacy 存量) / 'ctis' (欧盟 CTIS 2022+ 新试验, "
                         "2026-09-07 上移服务端). "
                         "All hit ct-search.coze.site/run, sharing one ICTRP token.")
    # CDE (chinadrugtrials) search fields -- plain strings, mirroring search_cde_workflow.py.
    ap.add_argument("--reg-no", help="CDE registration number (reg_no)")
    ap.add_argument("--indication", help="CDE indication (适应症)")
    ap.add_argument("--case-no", help="CDE case number (case_no)")
    ap.add_argument("--drugs-name", help="CDE drug name (drugs_name)")
    ap.add_argument("--drugs-type", help="CDE drug type enum: 中药/天然药物/化学药物/生物制品")
    ap.add_argument("--appliers", help="CDE applicant / sponsor (appliers)")
    ap.add_argument("--communities", help="CDE communities")
    ap.add_argument("--researchers", help="CDE researchers")
    ap.add_argument("--agencies", help="CDE agencies")
    ap.add_argument("--trial-status", help="CDE trial status enum (11 values)")
    ap.add_argument("--is-advanced-search", action="store_true",
                    help="CDE search mode: treat supplied structured filters as advanced search")
    ap.add_argument("--project-list", help="detail mode: project_list JSON string or path")
    ap.add_argument("--fetch-mode", choices=["list", "detail", "both"],
                    help="(可选) 取数策略：list=仅检索列表(1次调用)；detail=仅下载详情(需 --project-list)；"
                         "both=检索列表后自动下载详情(同一次调用内2次Coze调用、计1次配额)。"
                         "省略时沿用旧逻辑(--mode detail 或 --project-list 触发 detail，否则 search)。")
    ap.add_argument("--auto-confirm", action="store_true",
                    help="--fetch-mode both 且列表 >100 条时，跳过成本护栏、强制拉取详情")
    ap.add_argument("--max", type=int, help="max records (converted to max_pages)")
    ap.add_argument("--max-pages", type=int, help="WHO max_pages (default 50)")
    ap.add_argument("--page-start", type=int, help="WHO 断点续抓起始页（配合 --paginate-all 多次调用累积）")
    ap.add_argument("--paginate-all", action="store_true",
                    help="WHO 总量>400 时仍在预算内尽力翻页（默认 False=早退+escalate）")
    ap.add_argument("--token", help="Bearer token (else env CT_REGISTRY_COZE_TOKEN / embedded blob in adapters/endpoint_token.py)")
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    ap.add_argument("--out", default="ictrp_extsvc.json")
    ap.add_argument("--demand-id",
                    help="检索需求标识：同一 demand_id 当日只计 1 次配额（WHO+CDE 合并、"
                         "关键词微调/重复检索均不重复计数）。省略则每次调用各计 1 次。")
    # CDE 静默降级参数（中文检索 0 条时自动补发英文检索，由 Coze workflow 处理）
    ap.add_argument("--silent-fallback", action="store_true",
                    help="CDE 静默降级：中文检索 0 条时自动补发英文检索（需配合 --fallback-keyword）")
    ap.add_argument("--fallback-keyword",
                    help="CDE 静默降级关键字（通常为中译英），由 Coze workflow 在中文 0 条时自动补发")
    ap.add_argument("--run", action="store_true",
                    help="actually POST (default = preview only, no network)")
    ap.add_argument("--no-fallback-who", dest="fallback_who", action="store_false", default=True,
                    help="(仅 chictr 源) 关闭『ChiCTR 直连被 WAF/节点故障拦截时自动切换 WHO "
                         "ICTRP 线路专查 ChiCTR 来源记录』的兜底；默认开启")
    ap.add_argument("--no-kw-localize", dest="no_kw_localize", action="store_true", default=False,
                    help="(仅 who 源) 关闭『中文关键词自动本地化为英文』（WHO 端只认英文；"
                         "默认 term_map 优先、词典 miss 走在线兜底）")
    ap.add_argument("--request-id",
                    help="请求唯一 ID（uuid4 hex）；缺省自动生成或取 env "
                         "CT_REGISTRY_REQUEST_ID。一次用户请求内所有端点调用共享，"
                         "落飞书独立 request_id 列，供治理按 (request_id, call_type) 判重")
    ap.add_argument("--no-stream", dest="stream", action="store_false", default=True,
                    help="强制同步 /run（默认走 /stream_run 流式；流式取不到结果会自动回退同步，此开关用于完全跳过流式）")
    ap.add_argument("--query-origin",
                    help="调用发起来源标识（sha256:<64 hex>），用于审计/限流；由技能安装设备（本机）"
                         "生成并携带，禁止由 Coze 服务器生成（ct-base §8.6）。未显式传参时自动计算注入")
    ap.add_argument("--timeout", type=int, default=600,
                    help="Coze 检索等待超时上限（秒），默认 600 = 10 分钟；超时退出时返回值 is_timeout=True")
    args = ap.parse_args()

    # 治理护栏 (0.5.09)：未注册 source 拒绝发文（避免脏请求进飞书）。
    _validate_source(args)

    # ct-base §8.6：query_origin 必须由技能安装设备（本机）生成并携带，
    # 禁止由 Coze 服务器兜底生成（容器 hostname 漂移，且标识非来源机器）。
    if not args.query_origin:
        args.query_origin = _compute_query_origin()

    api_source = API_SOURCE.get(args.source, "who")
    fetch_mode = _resolve_fetch_mode(args)
    token = get_token(args.token)
    endpoint = args.endpoint or DEFAULT_ENDPOINT
    source_label = RECORD_SOURCE.get(args.source, "ICTRP")

    # ---- resolve payload(s) per fetch strategy ----
    list_payload = None
    detail_payload = None
    if fetch_mode == "detail":
        if not args.project_list:
            sys.exit("[ictrp-extsvc][ERROR] --fetch-mode detail 需要 --project-list"
                     "（列表输出文件或 project_list JSON 字符串）。")
        detail_payload = build_payload(args)   # builds mode=detail from --project-list
    else:
        list_payload = build_payload(args)     # search/combined/multi_keyword
        if fetch_mode == "both":
            detail_payload = {"mode": "detail", "source": api_source, "project_list": None}

    # P1-4 (2026-08-12, extended 2026-08-12): breadth advisory for ANY bare-keyword
    # search (no structured filters) on the unified Coze gateway — not just WHO. A bare
    # wide keyword may hit the ~5-min wall and return only part of the results. Tier-2
    # broad disease classes (diabetes/hypertension/...) also warn here but do NOT abort.
    _no_struct = (args.mode in (None, "search") and not args.multi_keywords
                  and not any(getattr(args, f, None) for f in
                              ("who_title", "who_condition", "who_intervention", "who_sponsor",
                               "who_country", "who_phase", "who_secondary_id"))
                  and " " not in (args.q or ""))   # 多词 q 会走 multi_keyword，不告警
    if fetch_mode in ("list", "both") and _no_struct:
        reasons = []
        if args.q and is_soft_broad(args.q):
            reasons.append(f"关键词 {args.q!r} 属宽病类（如糖尿病/高血压），单独检索可能仅取回部分结果")
        if args.source == "who":
            reasons.append("WHO 纯关键词检索可能命中统一网关 ~5 分钟硬墙")
        if reasons:
            print("[ictrp-extsvc][BREADTH] " + "；".join(reasons)
                  + "。建议改用 --mode multi_keyword（多词 AND 缩窄，最快）或 --mode combined "
                    "（who_* 字段级 AND 过滤，更准），或收窄/组合关键词。"
                    "详见 README 「数据量与超时」一节。")
    if not args.run:
        preview_payload = list_payload or detail_payload
        print_preview(preview_payload, token, args.out, endpoint)
        if fetch_mode == "both":
            print(f"[ictrp-extsvc][PREVIEW] --fetch-mode both：列表返回后将自动拉取详情到 "
                  f"{_detail_out_path(args.out)}（同一次调用内、计 1 次配额）。")
        return
    # §5.212 outbound authorization gate (before quota check + network I/O).
    if not _check_outbound_authorization(endpoint):
        return
    # Daily shared-resource guard: caps WHO/CDE (all shared-endpoint) retrieval at 100/day,
    # charged ONCE per demand_id (WHO+CDE merged; tweaks/repeats within a demand are free).
    # For --fetch-mode both, list+detail share the SAME demand_id -> counted as 1 call.
    allowed, _remaining, guard_msg = usage_guard.check(
        demand_id=args.demand_id or os.environ.get("CT_DEMAND_ID"), source_label=source_label)
    print(guard_msg)
    if not allowed:
        return

    if fetch_mode == "detail":
        run(detail_payload, token, args.out, args.timeout, endpoint, source_label, args.stream, args=args)
    elif fetch_mode == "list":
        run(list_payload, token, args.out, args.timeout, endpoint, source_label, args.stream, args=args)
    else:  # both: search, then auto-detail from the returned project_list
        run(list_payload, token, args.out, args.timeout, endpoint, source_label, args.stream, args=args)
        pl_raw = _read_project_list_raw(args.out)
        if not pl_raw:
            print("[ictrp-extsvc][BOTH] 列表未返回可用的 project_list，跳过自动详情。")
        else:
            n = _read_record_count(args.out)
            if isinstance(n, int) and n > BOTH_DETAIL_LIMIT and not args.auto_confirm:
                print(f"[ictrp-extsvc][BOTH-SKIP] 列表 {n} 条 > {BOTH_DETAIL_LIMIT}，"
                      f"自动详情耗时长/易超时，默认跳过（加 --auto-confirm 强制拉取）。")
            else:
                detail_payload["project_list"] = pl_raw
                dout = _detail_out_path(args.out)
                run(detail_payload, token, dout, args.timeout, endpoint, source_label, args.stream)
                print(f"[ictrp-extsvc][BOTH] 列表+详情完成：列表 {args.out}；详情 {dout}。")


if __name__ == "__main__":
    main()
