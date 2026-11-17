#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coze_dispatch.py — ct-safety 轻本地端统一外发调度器（薄客户端 · 流式版）

WHY THIS EXISTS
───────────────
用户指令（2026-09-01）：「统一采用轻本地端的策略，本地所有的 safety 检索需求
一律改为外发 coze 实现。」本模块是这条指令的本地落地：

  - 所有安全性「检索」动作经 Coze 统一端点外发：
    · **快速路径** `/stream_run`（SSE 流式）——仅承担 60s 内能完成的轻检索
      （网关 stgw 60s 硬超时内最快、带 SSE 进度；超时主动切换下方路径）；
    · **主路径** `/run`（非流式）——响应形态自适应：
      同步返回 → 直接解析；`{status:accepted, run_id}` 异步协议 →
      轮询 `/run/status/{run_id}`（指数退避 5→30s，总上限 timeout 秒）。
      重检索（CN-PV 全栏目 / ICTRP 型深翻页）服务端可跑数分钟，同步响应必被
      网关 60s 掐断，只有异步轮询能完整回收（2026-10-19 改造）。
  - 本地仅负责 disproportionality / signal_score / check_event（labeled 判定）/
    报告生成等计算。
  - 出站凭据 / 授权闸门 / PII 剥离 / 计费透传 **复用 nmpa_coze 单一真相源**，
    不重复实现 token 解码与 config 校验。

架构规范：ct-base/BASE.md §20.14 — 词表留本地，抓取执行器上 Coze，长任务走异步轮询。

覆盖的 Coze source（与 ct-registry sources.py 注册一一对应）
──────────────────────────────────────────────────────
  faers / fda_label / dailymed / rxclass / fda_recall / hk_pv / nmpa_pv
（nmpa_pv 对应 NMPA 药物警戒通报检索，走 Coze 浏览器通道。）

端点（与 ct-literature 对齐）
──────────────────────────────
  快速路径：ct-search.coze.site/stream_run（SSE 流式，钳制 60s）
  主路径：  ct-search.coze.site/run（同步解析 / accepted+run_id 异步轮询自适应）
"""
import json
import os
import sys
import time
import threading
import urllib.error
import urllib.request

# 复用 nmpa_coze 的凭据/授权/PII/计费单一真相源（同目录）
from nmpa_coze import (
    get_token,
    check_outbound_authorization,
    _sanitize,
    _query_origin,
    _billing_fields,
    attach_coze_contract,
    DEFAULT_ENDPOINT,
)

# 中文药名 → 英文 INN 自动映射（复用 ct-base 共享 resolver，本地已注入 scripts/）。
# 单一真源 ct-base/references/drug_name_map.json（471 条），开发期本地优先读取
# ct-safety/references/drug_name_map.json（publish_inject 注入副本）。
try:
    _HERE = os.path.dirname(os.path.abspath(__file__))
    _SCRIPTS_DIR = os.path.join(os.path.dirname(_HERE), "scripts")
    if _SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, _SCRIPTS_DIR)
    from drug_name_resolver import is_non_ascii as _dnr_is_non_ascii, \
        resolve_for_dialog as _dnr_resolve
except Exception:  # pragma: no cover — resolver 缺失时降级为原样外发
    _dnr_is_non_ascii = None
    _dnr_resolve = None

# 中文事件词 → 英文（复用 ct-base 共享 kw_localize，本地已注入 scripts/）。
# 对照表（term_map.json / kw_lexicon.json）优先；表内没有的词走 online_translate
# 零密钥公共端点兜底（CT_TRANSLATE_ONLINE=0 可关）。对齐 bilingual_retrieval.md §2。
try:
    from kw_localize import detect_lang as _kwl_detect_lang, \
        localize_with_fallback as _kwl_localize_with_fallback
except Exception:  # pragma: no cover — 缺失时降级为原样外发
    _kwl_detect_lang = None
    _kwl_localize_with_fallback = None

# 可由本调度器外发的源（fail-closed：不在表内一律拒绝）
DISPATCHABLE_SOURCES = frozenset({
    "faers", "maude", "fda_label", "dailymed", "rxclass", "fda_recall", "hk_pv", "nmpa_pv",
})

# 这些源返回「佐证型 Evidence」结构（dailymed/rxclass/fda_recall）；
# 出错时也回传同构 error 载体，便于 corroborative_sources.collect() 无感消费。
_EVIDENCE_SOURCES = frozenset({"dailymed", "rxclass", "fda_recall"})

# 端点常量（与 ct-literature 对齐）
CT_SEARCH_ENDPOINT_STREAM = os.environ.get("CT_SEARCH_ENDPOINT_STREAM",
                                            "https://ct-search.coze.site/stream_run")
CT_SEARCH_ENDPOINT = os.environ.get("CT_SEARCH_ENDPOINT",
                                     "https://ct-search.coze.site/run")

# ── stream 快速路径上限（2026-10-19 异步化改造） ────────────────────────────
# Coze 云端网关 stgw 对 HTTP 请求有 60s 硬超时（ct-base §20.17.1 实测 60.0s 整
# 504，流式同样被杀——不是逃生通道）。把 stream 的 socket timeout 钳到 60s：
# 60s 内能完成的轻检索走 SSE（最快、带进度），到点主动切换 /run 主路径
# （同步解析 / accepted+run_id 异步轮询自适应），不在必死的连接上干等。
_STREAM_FAST_PATH_MAX = float(os.environ.get("CT_SEARCH_STREAM_TIMEOUT", "60"))

# 并发限流（ct-base §20.10）：相邻两次 Coze 调用间隔 ≥1 秒
_RATE_LIMIT_LOCK = threading.Lock()
_LAST_CALL_TS = 0.0


def _acquire_rate_limit():
    """相邻两次 Coze 调用之间至少间隔 1 秒（可由 COZE_MIN_INTERVAL 覆写）。"""
    try:
        interval = float(os.environ.get("COZE_MIN_INTERVAL", "1.0"))
    except (TypeError, ValueError):
        interval = 1.0
    if interval <= 0:
        return
    global _LAST_CALL_TS
    with _RATE_LIMIT_LOCK:
        now = time.monotonic()
        wait = interval - (now - _LAST_CALL_TS)
        if wait > 0:
            time.sleep(wait)
            now = time.monotonic()
        _LAST_CALL_TS = now


def _translate_drug(drug):
    """非 ASCII（中文）药名 → 英文 INN（来自 ct-base 共享 drug_name_map）。

    返回 (send_keyword, translated: bool)。英文 / 空 / 未命中映射时原样返回。
    仅在 dispatch() 调用，故只作用于英文源（faers / fda_label / dailymed /
    rxclass / fda_recall / hk_pv）；nmpa_pv 走中文关键词，不经此函数。
    """
    if not drug or _dnr_is_non_ascii is None or not _dnr_is_non_ascii(drug):
        return drug, False
    eng, translated = _dnr_resolve(drug)
    if eng and eng.strip() and eng != drug:
        return eng, translated
    return drug, False


def _translate_event(event):
    """非 ASCII（中文）事件词 → 英文（对照表优先 + 在线 API 兜底，来自 ct-base 共享 kw_localize）。

    返回 (send_event, translated: bool)。英文 / 空 / 未命中映射且在线兜底也失败时原样返回。
    对齐 bilingual_retrieval.md §2：翻译前置，表内没有的词外接翻译 API 兜底。
    事件词整短语保留（不截断），供 Coze 端整短语文引用。
    """
    if not event or _kwl_detect_lang is None or _kwl_detect_lang(event) != "zh":
        return event, False
    eng, st = _kwl_localize_with_fallback(event, "en")
    if eng and eng.strip() and eng != event:
        return eng, (st in ("term_map", "online"))
    return event, False


def _evidence_error(source, drug, event, err):
    """佐证源出错时的同构载体（与 Evidence.to_dict 形状一致，collect() 无感消费）。"""
    return {
        "source": source, "drug": drug, "event": event,
        "labeled": None, "detail": "", "record_count": 0,
        "records": [], "error": err,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def _generic_error(source, err):
    return {"error": err, "source": source}


# ──SSE 流式解析器 ───────────────────────────────────────────────────────
def _dig_output(node):
    """从单个流式事件（workflow_end / node_end）提取 output。

    兼容三种嵌套形态（与 ct-literature pdf_download._dig_output 同构）：
      - {"type": "workflow_end", "output": <...>}
      - {"type": "workflow_end", "data": {"output": <...>}}
      - {"type": "workflow_end", "data": {"data": {"output": <...>}}}
    output 可为 dict 或 str（JSON 字符串，由调用方 loads）。
    """
    if not isinstance(node, dict):
        return None
    out = node.get("output")
    if out is None and isinstance(node.get("data"), dict):
        out = node["data"].get("output")
    if (out is None and isinstance(node.get("data"), dict)
            and isinstance(node["data"].get("data"), dict)):
        out = node["data"]["data"].get("output")
    return out


def _has_real_output(o):
    """判定某事件输出是否携带真实结果（而非空容器）。

    Coze「Output 变量未绑定」时 workflow_end.output 返回空 {}，此时必须回退到
    node_end 输出——故空 dict / 空 list 不算「有结果」。键集与 ct-literature
    pdf_download._has_real_output 对齐（含 s3_url：回参超长外置）。
    """
    if isinstance(o, dict):
        return any(k in o for k in ("projects", "project_list", "s3_url",
                                    "status", "total_count", "counts"))
    if isinstance(o, str):
        try:
            d = json.loads(o)
        except Exception:
            return bool(o) and "[DONE]" not in o
        return isinstance(d, dict) and any(
            k in d for k in ("projects", "project_list", "s3_url",
                             "status", "total_count", "counts"))
    if isinstance(o, list):
        return len(o) > 0
    return False


def _parse_stream(resp):
    """解析 Coze stream_run 的 SSE 流，返回最终 output 载荷（dict|list|None）。

    v0.9.14 修复（双发根因）：本函数原先优先复用 ct-literature 的
    `adapters.pdf_download._parse_coze_stream`。该依赖**必须移除**，两个原因：

    ①跨技能隐式依赖 + 行为不可测。pdf_download 不在 ct-safety 技能树内
      （`adapters/` 下无此文件），独立运行时 import 必抛 ModuleNotFoundError →
      降级到本地解析器；但若同进程先跑过 ct-literature，其 `adapters` 包已进
      sys.modules 缓存，import 会**成功**并静默使用 ct-literature 的实现
      （实测：sys.path 顺序决定命中谁）。即：同一份 ct-safety 代码在不同会话
      里走两条不同解析路径，行为不可复现。
    ② 真缺陷：两条路径都只认「output.projects 是 list」的旧形态，而 ct-search
      的 faers 型 output 是 `{"project_list":"<json str>","total_count":N}`
      ——**无 projects 键** → 解析恒返回 None → dispatch 判定「流式无结果」
      → 回退 /run 再发一次。结果：每次检索在 Coze 侧留下两条 searchlog，
      retrieval 成本与时延翻倍。（实测：stream 43s 拿到完整 counts 却返回
      None，随后 /run 重跑一遍。）

    本实现保留 pdf_download 的两项**有效**能力（避免移除依赖造成能力回退）：
      - node_end 回退：workflow_end.output 为空 {} 时回退到最后一个含真实
        结果的 node_end（对应 Coze Output 变量未绑定的场景）
      - `_dig_output` 三种嵌套形态兼容
    不保留其s3_url 外置回拉（ct-safety 各源均不走 S3 外置，无此需求）。

    返回原始 output，归一交 _stream_output_to_result → _parse_run_response，
    与 /run 路径共用单一真相源，避免两条解析逻辑漂移。
    """
    return _parse_stream_output(resp)


def _parse_stream_output(resp):
    """SSE → 最终 output 载荷（dict|list）；无有效输出时 None。

    优先级：workflow_end.output（若携带真实结果）→ 最后一个含真实结果的
    node_end.output → 最后一个 node_end.output → 含 projects/project_list
    的事件 → 整块 JSON（应对非 SSE 返回）。
    """
    events = []
    buf = b""
    for chunk in resp:
        buf += chunk
        while b"\n" in buf:
            line_b, buf = buf.split(b"\n", 1)
            line = line_b.decode("utf-8", "ignore").rstrip("\r")
            if line.startswith("data:"):
                ds = line[len("data:"):].lstrip()
                if ds and ds != "[DONE]":
                    try:
                        events.append(json.loads(ds))
                    except Exception:
                        pass
    if not events:
        try:
            events.append(json.loads(buf.decode("utf-8", "ignore")))
        except Exception:
            return None

    workflow_end_out = None
    node_outputs = []
    for evt in events:
        if not isinstance(evt, dict):
            continue
        inner = evt.get("data")
        node = inner if (isinstance(inner, dict) and inner.get("type")) else evt
        etype = node.get("type") or evt.get("type")
        if etype == "workflow_end":
            workflow_end_out = _dig_output(node)
        elif etype == "node_end":
            o = _dig_output(node)
            if o is not None:
                node_outputs.append(o)

    final = None
    if _has_real_output(workflow_end_out):
        final = workflow_end_out
    else:
        for o in reversed(node_outputs):
            if _has_real_output(o):
                final = o
                break
        if final is None and node_outputs:
            final = node_outputs[-1]
    if final is None:
        for evt in reversed(events):
            if isinstance(evt, dict) and ("projects" in evt or "project_list" in evt):
                final = evt
                break
    if final is None:
        return None
    if isinstance(final, str):
        try:
            final = json.loads(final)
        except Exception:
            return None
    if not isinstance(final, (dict, list)):
        return None
    # v0.9.14：原实现在此强制提取 projects（`final["projects"]` / `final["project_list"]["projects"]`），
    # faers 型 output 无 projects 键 → 恒 None → 误判「流式无结果」并回退 /run（双发）。
    # 现原样返回 output，交 _stream_output_to_result 归一（与 /run 共用 _parse_run_response）。
    return final


def _stream_output_to_result(output, source):
    """workflow_end.output → 本地统一格式；无法归一时返回 None（触发 /run 回退）。

    与 _parse_run_response 共用同一解析器：output 顶层就带 project_list /
    total_count（faers / fda_label / dailymed 各型），直接喂给 _parse_run_response
    即可得到与 /run 路径**完全同构**的结果。

    判定「有效载荷」用**键存在性**而非真值（v0.9.14 修正）：稀疏 2×2（a=0）
    与上游 openFDA 报错都会让 counts/total_count 为空或None，若按真值判断会
    把合法结果误判为「无结果」→ 又触发一次 /run，双发重现。Coze 侧只要回过
    结构化 output（带 project_list / total_count / counts 任一键）即视为有效，
    由 _parse_run_response 忠实还原（含 counts=None 的错误态）。

    返回 None 仅表示「流式确实没给出结构化 output」（Output 未绑定、被
    rejected、响应非 SSE），此时回退 /run —— 这是设计意图，不是 bug。
    """
    if output is None:
        return None
    # 旧形态：output 本身就是 projects 列表
    if isinstance(output, list):
        return _projects_to_result(output, source)
    if isinstance(output, dict):
        # 结构化 output 的标志键（与 _has_real_output 同源，再加 counts）
        if any(k in output for k in ("projects", "project_list", "counts",
                                     "total_count", "s3_url", "status",
                                     "n_results", "record_count", "records",
                                     "labeled")):
            return _parse_run_response(dict(output), source)
    return None


def _coze_stream_once(body, timeout):
    """单次 /stream_run 请求 + SSE 解析；返回 workflow_end.output（dict|list）或 None，异常上抛。"""
    req = urllib.request.Request(CT_SEARCH_ENDPOINT_STREAM, data=body,
                                 headers=_stream_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return _parse_stream(resp)


def _stream_headers():
    """流式请求 headers（与 ct-literature 一致）。"""
    h = {"Content-Type": "application/json"}
    tok = get_token()
    if tok:
        h["Authorization"] = "Bearer " + tok
    return h


def _coze_async_poll(source, endpoint, run_id, out, timeout, drug=None, event=None):
    """异步协议：轮询 {endpoint_base}/run/status/{run_id}（照搬 ct-registry
    adapters/extsvc_client._run_async_poll，改 stdlib urllib 零依赖）。

    背景：ct-search 统一端点对重检索源（ICTRP/CDE 型深翻页、CN-PV 全栏目抓取）
    返回 `{status:"accepted", run_id}` 而非同步结果——服务端还要跑数分钟，
    同步响应必被网关 60s 掐断。此前客户端不识别该协议，把 accepted 信封当
    同步响应对待 → project_list 缺失 → 空结果/误判（2026-10-19 修复）。

    轮询策略（与 extsvc_client 对齐）：
      - 指数退避：首轮 5s，逐轮 ×2 封顶 30s；
      - 总上限 timeout 秒（调用方语义：总等待时间，默认 300s）；
      - 轮询 GET 为短请求：单次网络抖动 / 单次超时 / 404（最终一致性窗口）
        均续轮，不废弃服务端任务；401/403 鉴权问题立即失败（重试无意义）；
      - 终态 completed → data["result"] 或 data 本体 → _parse_run_response
        （与 /run 同步路径同一解析器）；failed/cancelled → 错误载体（不静默）；
      - 到期 → is_timeout 错误载体，附缩小关键字的引导。
    """
    base = endpoint.rsplit("/run", 1)[0].rstrip("/")
    status_url = "%s/run/status/%s" % (base, run_id)
    headers = _stream_headers()

    def _err(msg):
        print("[coze-dispatch][%s] %s" % (source, msg), file=sys.stderr)
        return _evidence_error(source, drug, event, msg) if source in _EVIDENCE_SOURCES \
            else _generic_error(source, msg)

    deadline = time.time() + timeout
    wait = 5.0
    while time.time() < deadline:
        try:
            req = urllib.request.Request(status_url, method="GET", headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # 最终一致性窗口：任务刚提交时 status 可能短暂 404 → 续轮
                pass
            elif e.code in (401, 403):
                print("[coze-dispatch] Token 无效或已过期，请更新 config/coze.dat",
                      file=sys.stderr)
                return _err("HTTP %s (poll /run/status)" % e.code)
            else:
                pass  # 其它 5xx：网关抖动，续轮等终态
            time.sleep(min(wait, max(1, deadline - time.time())))
            wait = min(wait * 2, 30)
            continue
        except Exception:
            # 连接抖动 / 单次超时：服务端任务不受影响，续轮（deadline 兜底）
            time.sleep(min(wait, max(1, deadline - time.time())))
            wait = min(wait * 2, 30)
            continue
        status = data.get("status")
        if status == "running":
            time.sleep(min(wait, max(1, deadline - time.time())))
            wait = min(wait * 2, 30)
            continue
        if status == "failed":
            return _err("remote run failed: %s" % data.get("error"))
        if status == "cancelled":
            return _err("remote run cancelled (run_id=%s)" % run_id)
        # completed（或 status 缺失的兜底）：最终结果两种形态
        #  (a) 平台已重命名：{"status", "result": {...}}
        #  (b) 直接是 result dict
        result_payload = data.get("result", data)
        result = _parse_run_response(result_payload, source)
        print("[coze-dispatch][%s] 异步检索完成（run_id=%s，轮询回收）"
              % (source, run_id), file=sys.stderr)
        _maybe_write_out(out, result)
        return result
    return _err("timeout after %ss (poll /run/status/%s) — Coze 异步检索超过等待上限；"
                "数据可能不全：建议缩小关键字 / 换其他注册源交叉验证"
                % (timeout, run_id))


# ── 统一外发检索 ──────────────────────────────────────────────────────────
def dispatch(source, drug, event=None, date_from=None, date_to=None,
             run=False, out=None, timeout=300, token=None, endpoint=None,
             account_id=None, billing_token=None, extra=None):
    """统一外发检索。返回解析后的 result dict（与本地模块同构）；run=False 仅预览。

    路径分工（2026-10-19 异步化改造）：
      - 快速路径 `/stream_run`（SSE）：socket timeout 钳制
        min(timeout, _STREAM_FAST_PATH_MAX=60s)——只承担 60s 内能完成的轻检索；
      - 主路径 `/run`：响应形态自适应——同步返回直接解析；
        `{status:accepted, run_id}` → `_coze_async_poll` 轮询回收（重检索唯一活路）。
    `out` 非空时把结果写盘，兼容 ct_safety.py 既有 `json.load(open(out))` 往返。

    nmpa_pv 特殊处理：drug 参数可为 dict（cn_pv_keywords.build_nmpa_pv_query 的返回），
    此时跳过 drug/event 翻译，直接使用 drug 作为 payload 基础。
    """
    if source not in DISPATCHABLE_SOURCES:
        raise ValueError("coze_dispatch: unsupported source %r (allowed: %s)"
                         % (source, sorted(DISPATCHABLE_SOURCES)))
    endpoint = endpoint or DEFAULT_ENDPOINT

    # nmpa_pv：结构化查询（drug 为 dict），不走 drug/event 翻译
    # Coze 端 nmpa_pv 节点期望 keyword + multi_keywords（非 drug_kws/event_kws）
    if source == "nmpa_pv" and isinstance(drug, dict):
        drug_kws = drug.get("drug_kws", [])
        event_kws = drug.get("event_kws", [])
        payload = {
            "source": source,
            "mode": "search",
            "keyword": " ".join(drug_kws) if len(drug_kws) > 1 else (drug_kws[0] if drug_kws else ""),
            "multi_keywords": " ".join(event_kws),
            "query_origin": _query_origin(),
        }
        # 保留可选字段（since/until/max_per/extra）
        for _k in ("since", "until", "max_per"):
            if drug.get(_k) is not None:
                payload[_k] = drug[_k]
        if extra:
            payload.update(extra)
        billing = _billing_fields(account_id, billing_token)
        if billing:
            payload.update(billing)
        attach_coze_contract(payload, query=" ".join(drug.get("drug_kws", [])))
    else:
        # ① 中文药名 → 英文 INN（仅作用于英文源；resolver 缺失时降级为原样）
        send_keyword, translated_drug = _translate_drug(drug)
        if translated_drug:
            print("[coze-dispatch][%s] 中文药名 %r → 英文 INN %r（自动映射）"
                  % (source, drug, send_keyword))
        # ② 中文事件词 → 英文（对照表优先 + 在线 API 兜底；整短语保留不截断）
        send_event, translated_event = _translate_event(event)
        if translated_event:
            print("[coze-dispatch][%s] 中文事件 %r → 英文 %r（自动映射）"
                  % (source, event, send_event))
        payload = {
            "source": source,
            "mode": "search",
            "keyword": send_keyword or "",
            "multi_keywords": (send_event or "").strip(),
            "query_origin": _query_origin(),
        }
        if date_from:
            payload["date_from"] = date_from
        if date_to:
            payload["date_to"] = date_to
        if extra:
            payload.update(extra)
        billing = _billing_fields(account_id, billing_token)
        if billing:
            payload.update(billing)

        # ct-base coze_io_contract §1：统一注入 skill_version(顶层) + user_language(params)
        # query 用用户原始输入（drug/event）做内容级语言检测，而非翻译后的英文 INN。
        attach_coze_contract(payload, query="%s %s" % (drug or "", event or ""))

    if not run:
        print("[PREVIEW] coze-dispatch[%s] payload=%s (no network; add run to execute)"
              % (source, json.dumps(payload, ensure_ascii=False)))
        return None
    if not check_outbound_authorization(endpoint):
        err = "AUTH-BLOCK: endpoint %s not in auto_approve_endpoints" % endpoint
        print("[coze-dispatch][%s] %s" % (source, err))
        return _evidence_error(source, drug, event, err) if source in _EVIDENCE_SOURCES \
            else _generic_error(source, err)

    # 限流
    _acquire_rate_limit()

    # HTTP POST to Coze —— 快速路径 /stream_run（钳制 60s），主路径 /run（同步/异步自适应）
    body = json.dumps(_sanitize(payload), ensure_ascii=False).encode("utf-8")
    try:
        # 钳制理由：网关 60s 硬超时（stgw），stream 超过即整次被杀——
        # 给它 300s socket timeout 只会干等到被杀，不如 60s 主动切换主路径。
        output = _coze_stream_once(body, min(timeout, _STREAM_FAST_PATH_MAX))
        if output is not None:
            result = _stream_output_to_result(output, source)
            if result is not None:
                _maybe_write_out(out, result)
                return result
        # 流式确无有效 output（workflow Output 未绑定 / 被 rejected）→ 回退 /run
        print("[coze-dispatch][%s] /stream_run 无有效结果，回退 /run" % source,
              file=sys.stderr)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        print("[coze-dispatch][%s] /stream_run HTTP %s，回退 /run: %s"
              % (source, e.code, err_body[:200]), file=sys.stderr)
    except Exception as e:
        print("[coze-dispatch][%s] /stream_run 失败(%s)，回退 /run: %s"
              % (source, type(e).__name__, e), file=sys.stderr)

    # 回退 /run（非流式）——用实际 endpoint（授权检查用的就是它，勿再打常量）
    try:
        _acquire_rate_limit()
        req2 = urllib.request.Request(endpoint, data=body,
                                      headers=_stream_headers(), method="POST")
        with urllib.request.urlopen(req2, timeout=timeout) as resp2:
            data = json.loads(resp2.read().decode("utf-8"))
        # 异步协议探测（2026-10-19）：重检索源返回 {status:accepted, run_id}
        # （服务端还要跑数分钟）。不识别该协议会被当同步响应对待 → 空结果。
        if isinstance(data, dict) and data.get("status") == "accepted" \
                and data.get("run_id"):
            print("[coze-dispatch][%s] /run 返回 accepted（run_id=%s），转异步轮询"
                  % (source, data["run_id"]), file=sys.stderr)
            return _coze_async_poll(source, endpoint, str(data["run_id"]), out,
                                    timeout, drug=drug, event=event)
        result = _parse_run_response(data, source)
        _maybe_write_out(out, result)
        return result
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        err = "HTTP %s: %s" % (e.code, err_body[:300])
        print("[coze-dispatch][%s] %s" % (source, err), file=sys.stderr)
        if e.code in (401, 403):
            print("[coze-dispatch] Token 无效或已过期，请更新 config/coze.dat",
                  file=sys.stderr)
        return _evidence_error(source, drug, event, err) if source in _EVIDENCE_SOURCES \
            else _generic_error(source, err)
    except Exception as e:
        err = "request failed: %s: %s" % (type(e).__name__, e)
        print("[coze-dispatch][%s] %s" % (source, err), file=sys.stderr)
        return _evidence_error(source, drug, event, err) if source in _EVIDENCE_SOURCES \
            else _generic_error(source, err)


def _projects_to_result(projects, source):
    """projects 列表 → 本地统一格式 dict（与 /run 返回结构同构）。"""
    return {
        "source": source,
        "count": len(projects),
        "projects": projects,
        "total_count": len(projects),
    }


def _parse_run_response(data, source):
    """解析 /run（非流式）返回体 → 本地统一格式 {"source","projects","count","total_count"}。

    兼容多种 project_list 格式：
      - 旧格式（str）：{"projects": [...], "total_count": N}
      - 新格式（str/dict）：
        · faers 型：{"counts": {...}, "top_events": [...], "drug_total": N, ...}
        · fda_label 型：{"n_results": N, "adverse_reactions": [...], "warnings": ...}
        · dailymed 型：{"labeled": bool, "records": [...], "record_count": N, ...}
        → 无 projects 时，用外层 total_count 或 pl 内 n_results/record_count 兜底，
          并透传关键字段，供 multi_source / corroborative_sources 消费。
    """
    pl_raw = data.get("project_list")
    if isinstance(pl_raw, str) and pl_raw:
        try:
            pl = json.loads(pl_raw)
        except (json.JSONDecodeError, TypeError):
            pl = None
    elif isinstance(pl_raw, dict):
        pl = pl_raw
    else:
        pl = None
    if isinstance(pl, dict):
        projects = pl.get("projects", [])
        # 优先用 pl 内 total_count；否则用外层 total_count；最后用 projects 长度
        tc = pl.get("total_count",
                     data.get("total_count",
                              pl.get("n_results",
                                      pl.get("record_count", len(projects)))))
        result = {
            "source": source,
            "count": tc,
            "projects": projects,
            "total_count": tc,
        }
        # 透传新格式计数字段
        # v0.9.14：增传 error——Coze 侧上游 openFDA 报错时（如500）会在 pl 里放
        # error 键；不透传则错误被静默吞成 counts=None，调用方误以为「无信号」。
        for _k in ("counts", "top_events", "drug_total", "event_total",
                   "grand_total", "drug", "api", "field",
                   "n_results", "adverse_reactions", "warnings",
                   "labeled", "detail", "records", "record_count",
                   "matched_drug_terms", "query", "error"):
            if _k in pl:
                result[_k] = pl[_k]
        return result
    if "projects" in data and "works" not in data:
        data["works"] = data.pop("projects")
        data["count"] = data.get("total_count", len(data["works"]))
    data["source"] = source
    return data


def _maybe_write_out(out, result):
    """out 非空时写盘。"""
    if not out:
        return
    try:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("[OK] coze-dispatch wrote %s" % out)
    except Exception as e:
        print("[WARN] coze-dispatch write %s failed: %s" % (out, e))


# ── 流式检索生成器 ──────────────────────────────────────────────────────────
def dispatch_stream(source, drug, event=None, date_from=None, date_to=None,
                    run=False, timeout=300, token=None, endpoint=None,
                    account_id=None, billing_token=None, extra=None,
                    batch_size=5, progress=None):
    """流式检索生成器：把 Coze 返回的 projects 按 batch_size 切片，依次 yield 给调用方。

    内部复用 dispatch()：dispatch 已改 /stream_run（SSE）+ /run 回退。
    每批最多 batch_size 条，最后一批可能不足。progress 回调逐批上报进度。
    """
    result = dispatch(source, drug, event, date_from, date_to,
                      run=run, timeout=timeout, token=token, endpoint=endpoint,
                      account_id=account_id, billing_token=billing_token, extra=extra)
    if result is None or result.get("error"):
        msg = "[coze-dispatch] 检索失败: %s" % (result.get("error") if result else "None")
        if progress:
            progress(msg)
        else:
            print(msg, file=sys.stderr)
        return
    projects = result.get("projects", [])
    total = len(projects)
    if progress:
        progress("[coze-dispatch] 检索完成，共 %d 条，按 %d 条/批返回" % (total, batch_size))
    for i in range(0, total, batch_size):
        batch = projects[i:i + batch_size]
        if progress:
            progress("[coze-dispatch] 返回第 %d 批（%d 条）" % (i // batch_size + 1, len(batch)))
        yield batch


# ═════════════════════════════════════════════════════════════════════════════
# ct_safety.py 用的薄垫片：把 fetch_faers / fetch_fda_label 的「检索」调用重定向到
# Coze；本地计算（check_event / _date_clause）与未外发的辅助检索（query_total /
# fetch_case_reports）保留本机直连。通过 rebind 模块全局名实现，调用点零改动。
# ═════════════════════════════════════════════════════════════════════════════
def _truncate_top_events(res, top, out):
    """按调用方 --top 截断 top_events（Coze 端固定返回 10 条）。

    统一端点不接收 top 参数，此前 `--top N`（含工作台「Top 事件数」）在统一端点
    路径下形同虚设——无论填几，报告里始终是 10 条。这里在本地做确定性截断，
    保证「用户说 top N」与「表里 N 行」一致；被截掉的候选仍在服务端原始响应中，
    需要时可调大 --top 重跑。
    """
    if not isinstance(res, dict):
        return res
    try:
        n = int(top)
    except (TypeError, ValueError):
        return res
    if n <= 0:
        return res
    te = res.get("top_events")
    if not isinstance(te, list) or len(te) <= n:
        return res
    res["top_events"] = te[:n]
    res["top_requested"] = n
    if out:
        try:
            with open(out, "w", encoding="utf-8") as f:
                json.dump(res, f, ensure_ascii=False, indent=2)
        except Exception as e:  # noqa: BLE001 - 截断失败不应中断主流程
            print("[coze-dispatch] 截断 top_events 后写盘失败: %s" % e, file=sys.stderr)
    return res


class FaersShim:
    """fetch_faers 的薄垫片：fetch_counts → Coze；其余保留本机直连。"""

    def __init__(self, real):
        self._real = real
        self._date_clause = real._date_clause  # 纯函数，本机直连

    def fetch_counts(self, drug, event=None, field="patient.drug.medicinalproduct",
                     top=10, api_key=None, run=False, out=None,
                     date_from=None, date_to=None, timeout=120, retries=3):
        # Coze 服务端用默认 field；忽略本地 api_key/retries（服务端自有 key/重试）
        res = dispatch("faers", drug, event, date_from=date_from, date_to=date_to,
                       run=run, out=out, timeout=max(int(timeout), 120))
        return _truncate_top_events(res, top, out)

    def query_total(self, search, api_key=None, timeout=120, retries=3):
        # 文档化例外：openFDA 任意检索式，结构化 state 无法承载 → 本机直连
        return self._real.query_total(search, api_key=api_key, timeout=timeout, retries=retries)

    def fetch_case_reports(self, drug, event=None, field="patient.drug.medicinalproduct",
                           n=20, api_key=None, run=False, out=None,
                           date_from=None, date_to=None, timeout=120, retries=3):
        # 文档化例外：个例报告直取 openFDA → 本机直连
        return self._real.fetch_case_reports(drug, event, field, n, api_key, run=run,
                                             out=out, date_from=date_from, date_to=date_to,
                                             timeout=timeout, retries=retries)

    def __getattr__(self, name):
        # 其它属性（如模块级常量）透明转发到真实模块
        return getattr(self._real, name)


class DeviceEventShim:
    """MAUDE（医疗器械不良事件）薄垫片：fetch_counts → Coze source='maude'。

    与 FaersShim 完全同构：器械计数同样经统一 Coze 端点（单一出口，与 ct-base
    §6 一致），本地不新增直连出口。真实模块 fetch_faers 需支持 source='maude'
    （device/event.json + patient.device.brand_name）。Coze 侧需部署对应
    maude 节点后计数才会返回真实数据（未部署时 dispatch 报错，由上层提示）。
    其余方法透明转发（fetch_case_reports 等仍走真实模块的本机直连例外）。
    """

    def __init__(self, real):
        self._real = real
        self._date_clause = real._date_clause

    def fetch_counts(self, drug, event=None, field=None, top=10, api_key=None,
                     run=False, out=None, date_from=None, date_to=None,
                     timeout=120, retries=3):
        # Coze maude 节点用器械默认维度；忽略本地 field/api_key/retries
        res = dispatch("maude", drug, event, date_from=date_from, date_to=date_to,
                       run=run, out=out, timeout=max(int(timeout), 120))
        return _truncate_top_events(res, top, out)

    def query_total(self, search, api_key=None, timeout=120, retries=3):
        # MAUDE 器械模式：配对/事件总数经 device/event.json（与 FaersShim 的
        # 本机直连例外对称，但端点须切换为 device 库，否则 patient.device.*
        # 字段在 drug 端点无索引会返回 0/被 skip，导致不成比例分析 2x2 不完整）。
        return self._real.query_total(search, api_key=api_key, timeout=timeout,
                                      retries=retries, source="maude")

    def count_field(self, search, field, api_key=None, limit=1000, timeout=60):
        # MAUDE 器械模式：时间序列 receivedate 计数分面经 device/event.json。
        return self._real.count_field(search, field, api_key=api_key, limit=limit,
                                      timeout=timeout, source="maude")

    def fetch_case_reports(self, drug, event=None, field="patient.device.brand_name",
                           n=20, api_key=None, run=False, out=None,
                           date_from=None, date_to=None, timeout=120, retries=3,
                           source="maude"):
        # MAUDE 器械模式：个例报告同样经 device/event.json（默认维度为器械名）。
        return self._real.fetch_case_reports(drug, event, field, n, api_key, run=run,
                                             out=out, date_from=date_from, date_to=date_to,
                                             timeout=timeout, retries=retries, source="maude")

    def __getattr__(self, name):
        return getattr(self._real, name)


class FdaLabelShim:
    """fetch_fda_label 的薄垫片：fetch_label → Coze；check_event 本地判定。"""

    def __init__(self, real):
        self._real = real

    def fetch_label(self, drug, api_key=None, run=False, out=None, limit=5,
                    timeout=120, retries=3):
        return dispatch("fda_label", drug, event=None, run=run, out=out,
                        timeout=max(int(timeout), 120))

    def check_event(self, label_data, event):
        # 本地判定（labeled/unlabeled），无网络
        return self._real.check_event(label_data, event)

    def __getattr__(self, name):
        return getattr(self._real, name)
