#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cloud brief 线上 canary（stdlib-only，不写任何文件、不改动技能状态）。

用途：两个 Coze 包发布后做端到端回归。覆盖
  1. ct-search 0.5.00 三个 advisor_*_brief source 的契约与护栏；
  2. 护栏违约 / 未知 source 的 fail-closed；
  3. ct-advisor 云端纯代码路径（tool_router → need_tool 执行卡；不传/强开开关两态对照）；
  3b. ct-advisor 混合意图 / 复杂混合调用（v1.61 P0-1 拆分 + v1.63 布尔标记）持久化回归；
  4. 本地链路（默认 handoff / brief 降为 opt-in、显式开启后真实取数、
     execute_card 端到端缝合、并行预取、失败回落、P0-2 短 TTL 缓存命中）；
  5. 性能 A/B（--only perf）：确认 ct-search 0.5.01 已部署、三源无 partial、
     串行耗时对照 0.5.00 基线（registry 24s / literature 18s / safety 12s）。

用法：
    C:/Tools/Anaconda3/python.exe scripts/canary_cloud_brief.py --only all
    --only search | guard | advisor | local | perf | all     默认 all
    --check                                          离线自检（不触网），校验契约与凭证
退出码：0 全通过 / 1 有 FAIL / 2 环境或凭证错误

注意：
  * 只发公开查询词（F33），绝不携带 doc_context / 附件内容。
  * 凭据仅存于本地技能/工作台；Coze 云端包内零凭据、不发起需凭据的外部调用，
    无需任何 Coze 控制台环境变量或输入变量配置。
  * 凭据轮换 SOP 见 config/brief_contract.json 的 credential_governance 段。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

S = Path(__file__).resolve().parents[1]
SKILLS = S.parent
for p in (str(S / "scripts"), str(S)):
    if p not in sys.path:
        sys.path.insert(0, p)

import cloud_brief as cb  # noqa: E402

CONTRACT = cb.load_contract()
SEARCH_URL = CONTRACT["endpoint"]["run_url"]
ADVISOR_URL = "https://ct-advisor.coze.site/run"
ORIGIN = "sha256:" + hashlib.sha256(b"ct-advisor-cloud-brief-canary").hexdigest()
HIST = [{"question": "上一轮问过 GCP 基本原则", "answer_summary": "已概述知情同意与受试者保护"}]
RESULTS: list[tuple[str, bool, str]] = []


def chk(label: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((label, bool(ok), detail))
    print("  [%s] %-46s %s" % ("PASS" if ok else "FAIL", label, detail))


def tokens() -> tuple[str, str]:
    try:
        from adapters import coze_token_embedded as tok
        adv = tok.get_token()
    except Exception:
        adv = ""
    return cb.get_token(), adv


def post(url: str, payload: dict, token: str, timeout: int = 115):
    req = urllib.request.Request(
        url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + token,
                 "Accept": "application/json, text/event-stream"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace"), time.time() - t
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), time.time() - t
    except Exception as e:
        return -1, "%s: %s" % (type(e).__name__, e), time.time() - t


def dig(raw: str, keys: tuple) -> dict:
    found = []

    def walk(o):
        if isinstance(o, dict):
            found.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str) and o.strip().startswith("{"):
            try:
                walk(json.loads(o))
            except ValueError:
                pass

    try:
        walk(json.loads(raw))
    except ValueError:
        for line in raw.splitlines():
            if line.strip().startswith("data:"):
                try:
                    walk(json.loads(line.strip()[5:]))
                except ValueError:
                    pass
    for d in found:
        if any(k in d for k in keys):
            return d
    return found[-1] if found else {}


def dig_field(raw: str, key: str):
    """字段级提取：遍历整棵 JSON，返回最后一个含该 key 的 dict 的值（稳健应对嵌套）。"""
    found = []

    def walk(o):
        if isinstance(o, dict):
            if key in o:
                found.append(o[key])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str) and o.strip().startswith("{"):
            try:
                walk(json.loads(o))
            except ValueError:
                pass

    try:
        walk(json.loads(raw))
    except ValueError:
        for line in raw.splitlines():
            if line.strip().startswith("data:"):
                try:
                    walk(json.loads(line.strip()[5:]))
                except ValueError:
                    pass
    return found[-1] if found else None


def _as_bool(v) -> bool:
    """跨端点版本归一化 `complexity_hint`，让同一套回归脚本兼容三种镜像：

    - v1.61：无该字段 → None → False
    - v1.62：整段提示文案（str）→ True（历史形态，v1.63 已撤销）
    - v1.63：纯布尔标记（bool）→ 原值

    端点逐步升级期间，末例仍能稳定判定「云端是否正确识别复杂混合调用」。
    """
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() not in ("", "false", "0", "none", "null")
    return bool(v)


def envelope(source: str, params: dict) -> dict:
    return {"source": source, "keyword": json.dumps(params, ensure_ascii=False),
            "mode": "search", "query_origin": ORIGIN,
            "skill_version": "ct-advisor/1.3.39", "locale": "zh-CN",
            "params": {"user_language": "zh-CN"}}


def search_canary(tk: str) -> None:
    print("\n=== 1. ct-search 三个 brief source ===")
    cases = [
        ("advisor_registry_brief", {"cond": "NSCLC", "max": 3}),
        ("advisor_safety_brief", {"drug": "aspirin", "event": "hepatic failure", "top": 3}),
        ("advisor_literature_brief", {"topic": "PD-1 NSCLC", "max": 3}),
    ]
    for source, params in cases:
        code, body, sec = post(SEARCH_URL, envelope(source, params), tk)
        d = dig(body, ("brief", "brief_kind"))
        skill = CONTRACT["sources"][source]["skill"]
        ok = (code == 200 and d.get("status") == "ok" and d.get("brief_kind") == source
              and d.get("disclaimer") == CONTRACT["disclaimer_text"]
              and d.get("suggest_skill") == skill
              and d.get("suggest_text") == CONTRACT["suggest_text"][skill]
              and d.get("param_allowlist") == CONTRACT["param_allowlist"][source])
        b = d.get("brief") or {}
        chk(source, ok, "%.1fs status=%s hits=%s partial=%s" %
            (sec, d.get("status"), b.get("total_hits", b.get("unique_works", "-")),
             b.get("partial_sources") or []))


def guard_canary(tk: str) -> None:
    print("\n=== 2. 护栏违约 / fail-closed ===")
    cases = [
        ("advisor_safety_brief", {"drug": "aspirin", "trend": True}, "PARAM_NOT_ALLOWLISTED"),
        ("advisor_registry_brief", {}, "MISSING_REQUIRED"),
        ("advisor_literature_brief", {"topic": "x", "pico": 1}, "PARAM_NOT_ALLOWLISTED"),
        ("advisor_source_not_deployed", {"x": 1}, "UNSUPPORTED_SOURCE"),
    ]
    for source, params, expect in cases:
        code, body, sec = post(SEARCH_URL, envelope(source, params), tk)
        d = dig(body, ("projects", "status"))
        hit = expect in (str(d.get("error")) + body)
        chk("拒绝 %s → %s" % (source, expect), hit, "%.1fs %s" % (sec, str(d.get("error"))[:70]))


def _advisor_payload(flag, salt: str = "", question: str = "") -> dict:
    q = question or "阿司匹林肝损伤在 FAERS 里的安全信号 PRR 和 ROR 是多少？"
    p = {"query_meta": {"difficulty": "", "category": "", "accuracy": "",
                        "query_origin": ORIGIN, "skill_version": "1.3.39"},
         "original_question": q,
         "draft_answer": "", "conversation_history": HIST,
         "params": {"user_language": "zh-CN"}}
    if salt:
        # 同一问题需要绕开答案缓存，否则两次请求拿到同一份草稿，对照无意义。
        p["conversation_history"] = [
            {"question": HIST[0]["question"] + "（" + salt + "）",
             "answer_summary": HIST[0]["answer_summary"]}]
    if flag is not None:
        p["cloud_brief_enabled"] = flag
    return p


def advisor_canary(tk: str) -> None:
    print("\n=== 3. ct-advisor 云端纯代码路径（无凭据、无外部调用）===")
    # 🔴 判据口径（2026-11-09 实测校准）：`@skill:ct-safety` 是 advisor 既有的
    #    技能导流 footer（route_tool.suggest_footer），属**合法文案**，不得计入
    #    brief 缝合判据。只有下面两个 brief 独有标记出现，才说明云端做了直连。
    BRIEF_MARKS = ("补充数据速览", "速览，非审计级")
    for label, flag, salt in (("不传开关", None, ""),
                              ("强制开关=true", True, "canary-on")):
        code, body, sec = post(ADVISOR_URL, _advisor_payload(flag, salt), tk)
        d = dig(body, ("final_answer", "need_tool"))
        fa = str(d.get("final_answer") or d.get("answer") or "")
        chk("%s → need_tool 执行卡 / 云端零缝合" % label,
            code == 200 and bool(d.get("need_tool"))
            and all(m not in fa for m in BRIEF_MARKS),
            "%.1fs need_tool=%s cache_hit=%s brief标记=%s" %
            (sec, d.get("need_tool"), d.get("cache_hit"),
             [m for m in BRIEF_MARKS if m in fa]))
    print("  [INFO] 凭据仅在本地技能；Coze 包内零凭据，无需任何控制台配置。")


def advisor_mixed_canary(tk: str) -> None:
    """持久化回归：v1.61（P0-1 混合意图拆分）+ v1.63（复杂混合调用布尔标记）。

    覆盖四种关键行为，固化 2026-11-09/10 线上实测结论：
      - 混合意图（原理/机制 + 执行动词/检索动词同现）→ 不再整体降级，仍下发 need_tool 执行卡；
      - 纯咨询 + 强词但无执行动词（如「什么是样本量」）→ need_tool 为空（不误派）；
      - 纯咨询·方法学（无执行动作）→ need_tool 为空；
      - 多工具命中的复杂混合调用 → complexity_hint=True（v1.63 起为纯布尔标记）。
    注：2026-11-10 v1.63 起云端**不再生成任何提示文案**，只回布尔元数据；面向用户的
    「拆分 / 超时终止重问」提示唯一真相源是技能端 route_tool.complexity_hint_text，
    由 entry.py 在调用之前（stderr）与答案最前（出口）独立保证并去重。本例仅校验
    云端标记是否随镜像发布，不代表用户会看到两次提示。_as_bool 兼容 v1.61/62/63。
    """
    print("\n=== 3b. ct-advisor 混合意图 / 复杂混合调用（v1.61 P0-1 + v1.63 布尔标记）===")
    # (label, question, expect_tool, expect_complexity_hint)
    #   expect_tool: "nonempty"=应下发 / "empty"=不应下发
    cases = [
        ("混合·原理+执行动词", "解释一下为什么用双侧检验，并帮我算一下样本量", "nonempty", False),
        ("混合·原理+检索动词", "先说明 PRR 的原理，再查一下阿司匹林肝损伤的 FAERS 信号", "nonempty", False),
        ("纯咨询+强词·无执行动词", "什么是样本量？", "empty", False),
        ("纯咨询·方法学", "非劣效界值怎么定才合理？", "empty", False),
        ("复杂混合·多工具", "查一下帕博利珠单抗在胃癌里的临床试验，并算一下对比 ORR 30% vs 45% 需要多少例",
         "nonempty", True),
    ]
    for i, (label, q, expect_tool, expect_hint) in enumerate(cases, 1):
        salt = "mix-%d-%d" % (i, int(time.time()) % 100000)
        code, body, sec = post(ADVISOR_URL, _advisor_payload(None, salt, q), tk, timeout=160)
        nt = dig_field(body, "need_tool")
        nt_nonempty = bool(nt)
        ok_tool = ((nt_nonempty if expect_tool == "nonempty"
                    else not nt_nonempty) if expect_tool in ("nonempty", "empty")
                   else (nt == expect_tool))
        raw_flag = dig_field(body, "complexity_hint")
        flag = _as_bool(raw_flag)
        ok_hint = (flag == expect_hint)
        detail = "%.1fs need_tool=%s flag=%s (%s)" % (
            sec, nt or "∅", flag, type(raw_flag).__name__)
        chk("%s → %s" % (label, ("下发工具" if expect_tool == "nonempty"
                                 else "不下发" if expect_tool == "empty" else expect_tool)),
            code == 200 and ok_tool and ok_hint, detail)
    print("  [INFO] 混合问句端点 LLM 生成偏慢（55–68s 常见），已放宽 timeout=160s；")
    print("  [INFO] 末例（复杂混合·多工具）校验 v1.63+ 的 complexity_hint 布尔标记；")
    print("         _as_bool 兼容 v1.61(无字段) / v1.62(文案) / v1.63+(bool) 三种端点；")
    print("         若该项 FAIL 且 flag=False，说明端点版本过低，需发布 v1.64 包"
          "（v1.62/v1.63 均未发布，直接发 v1.64）。")


def perf_canary(tk: str) -> None:
    print("\n=== 5. 性能 A/B（ct-search 0.5.01 部署后）===")
    baseline = {"advisor_registry_brief": 24, "advisor_literature_brief": 18,
                "advisor_safety_brief": 12}
    cases = [
        ("advisor_registry_brief", {"cond": "hepatocellular carcinoma", "max": 3}),
        ("advisor_literature_brief", {"topic": "CAR-T solid tumor", "max": 3}),
        ("advisor_safety_brief", {"drug": "ibuprofen", "event": "acute kidney injury", "top": 3}),
    ]
    rows = []
    for source, params in cases:
        env = envelope(source, params)
        # 唯一 query_origin + 不同检索词，绕开 Coze 端点结果缓存
        env["query_origin"] = "sha256:" + hashlib.sha256(
            ("perf-%s-%.6f" % (source, time.time())).encode()).hexdigest()
        code, body, sec = post(SEARCH_URL, env, tk)
        d = dig(body, ("brief", "brief_kind"))
        b = d.get("brief") or {}
        rows.append((source, code, sec, d.get("status"),
                     b.get("perf") or {}, b.get("partial_sources") or []))
    chk("perf.mode=parallel（确认 0.5.01 已部署）",
        all(r[4].get("mode") == "parallel" for r in rows),
        "缺 perf 字段 = 线上仍是 0.5.00 旧包")
    chk("三源 status=ok / HTTP 200",
        all(r[1] == 200 and r[3] == "ok" for r in rows))
    chk("无 partial_sources（软预算未误伤稳态）",
        all(not r[5] for r in rows),
        str([(r[0].replace("advisor_", ""), r[5]) for r in rows if r[5]]))
    print("  [INFO] 串行耗时对照（0.5.00 稳态基线；并行会引入网关排队噪音，故串行）")
    for source, code, sec, status, perf, part in rows:
        base = baseline[source]
        print("    %-28s %6.1fs  基线 %2ds %s  deadline=%ss elapsed=%ss partial=%s" %
              (source, sec, base, "更快" if sec < base else "未改善",
               perf.get("deadline_sec"), perf.get("elapsed_sec"), part or []))


def local_canary() -> None:
    print("\n=== 4. 本地链路：默认 handoff / 显式开 brief 取数 / 缝合 / 回落 / 缓存 ===")
    # 前几项必须测真实链路，先关缓存；末尾单独验缓存命中。
    os.environ["CT_ADVISOR_BRIEF_CACHE"] = "0"
    card = {"need_tool": "ct-safety",
            "params": {"drug": "aspirin", "event": "hepatic failure", "top": 3},
            "draft_answer": "", "original_question": "阿司匹林肝损伤安全信号？",
            "query_origin": ORIGIN, "locale": "zh-CN"}
    os.environ.pop("CT_ADVISOR_BRIEF_TOKEN", None)
    os.environ.pop("CT_ADVISOR_CLOUD_BRIEF", None)
    os.environ.pop("CT_ADVISOR_HANDOFF", None)
    # 2026-11-09 晚间：brief 降为 opt-in，默认主路径是 handoff。先验证默认态，
    # 再显式开启以保留原有的「真实取数 + 端到端缝合」回归覆盖。
    chk("CT_ADVISOR_CLOUD_BRIEF 未设 → 直连默认关闭", cb.enabled() is False)
    import handle_need_tool
    _default_card = handle_need_tool.execute_card(dict(card))
    chk("未设开关时 execute_card 走 handoff（默认主路径）",
        _default_card.get("status") == "handoff"
        and _default_card.get("mode") == "client_handoff",
        "status=%s" % _default_card.get("status"))
    os.environ["CT_ADVISOR_CLOUD_BRIEF"] = "1"
    chk("显式 CT_ADVISOR_CLOUD_BRIEF=1 可整条开启", cb.enabled() is True)

    text = cb.try_cloud_brief(card)
    chk("本地 cloud_brief 真实取数 + 三护栏渲染",
        bool(text) and all(x in text for x in ("补充数据速览", "速览，非审计级", "@skill:ct-safety", "PRR=")),
        "%d 字" % len(text or ""))

    # 2026-11-09 架构调整后，本地不只是薄客户端：还要验证两个真实调用入口
    # 能把 brief 结果缝合回答案（handle_need_tool 分流 / orchestrate 并行预取）。
    import orchestrate  # handle_need_tool 已在上方默认态验证时导入
    r = handle_need_tool.execute_card(dict(card))
    flat = json.dumps(r, ensure_ascii=False, default=str)
    chk("handle_need_tool.execute_card 端到端缝合",
        "补充数据速览" in flat and "速览，非审计级" in flat,
        "status=%s" % r.get("status"))
    pf = orchestrate._fire_prefetch(dict(card))
    chk("orchestrate._fire_prefetch 走 brief 直连",
        pf.get("mode") == "coze_brief" and pf.get("status") == "ok",
        "mode=%s" % pf.get("mode"))

    os.environ["CT_ADVISOR_BRIEF_TOKEN"] = "INVALID_FOR_FALLBACK_TEST"
    r = cb.try_cloud_brief(card)
    chk("无效凭证 → 回落本地执行卡（不伪造数据）", r is None)
    os.environ["CT_ADVISOR_CLOUD_BRIEF"] = "0"
    chk("显式 CT_ADVISOR_CLOUD_BRIEF=0 可整条关闭", cb.enabled() is False)
    os.environ.pop("CT_ADVISOR_BRIEF_TOKEN", None)
    # P0-2：短 TTL 缓存命中（前面已真实取数写入）；缓存段需重新显式开启 brief。
    os.environ["CT_ADVISOR_CLOUD_BRIEF"] = "1"
    os.environ.pop("CT_ADVISOR_BRIEF_CACHE", None)
    first = cb.try_cloud_brief(dict(card))   # 冷：写缓存
    t = time.time()
    hit = cb.try_cloud_brief(dict(card))     # 热：命中
    chk("P0-2 短 TTL 缓存命中且结果一致", bool(first) and hit == first,
        "%.3fs %d 字" % (time.time() - t, len(hit or "")))
    for k in ("CT_ADVISOR_BRIEF_TOKEN", "CT_ADVISOR_CLOUD_BRIEF", "CT_ADVISOR_BRIEF_CACHE"):
        os.environ.pop(k, None)


def main() -> int:
    ap = argparse.ArgumentParser(description="cloud brief 线上 canary")
    ap.add_argument("--only", default="all",
                    choices=("all", "search", "guard", "advisor", "mixed", "local", "perf"))
    ap.add_argument("--check", action="store_true", help="离线自检，不触网")
    a = ap.parse_args()
    if a.check:
        tk, adv = tokens()
        print("契约 sources=%d 白名单=%s" % (len(CONTRACT["sources"]),
              [len(v) for v in CONTRACT["param_allowlist"].values()]))
        print("ct-search 凭证可用=%s / advisor 凭证可用=%s" % (bool(tk), bool(adv)))
        return 0 if tk and adv else 2
    tk, adv = tokens()
    if not tk or not adv:
        print("凭证解析失败，退出", file=sys.stderr)
        return 2
    print("cloud brief 线上 canary · origin=%s…" % ORIGIN[:18])
    if a.only in ("all", "search"):
        search_canary(tk)
    if a.only in ("all", "guard"):
        guard_canary(tk)
    if a.only in ("all", "advisor"):
        advisor_canary(adv)
    if a.only in ("all", "mixed"):
        advisor_mixed_canary(adv)
    if a.only in ("all", "local"):
        local_canary()
    if a.only == "perf":
        perf_canary(tk)
    failed = [r for r in RESULTS if not r[1]]
    print("\n合计 %d 项，通过 %d，失败 %d" % (len(RESULTS), len(RESULTS) - len(failed), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
