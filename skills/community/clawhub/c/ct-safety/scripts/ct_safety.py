#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ct_safety.py / 编排入口

One-shot pipeline: fetch FAERS (openFDA) -> disproportionality -> Markdown report.
Reads only public data; zero confidential data or information input. / 一次性流水线：取数→信号检测→报告。
仅读公开数据，零保密数据或信息输入。

Usage:
  python scripts/ct_safety.py --drug "osimertinib" --event "PNEUMONITIS" --run --out-dir ./out
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_faers
import faers_dedup
import disproportionality
import report as report_mod
import report_xlsx
import fetch_cn_pv
import time_series
import adjust_ror
import fetch_fda_label
import signal_score
import drug_name_resolver
import causality
import signal_verification
import meddra_coding
import signal_prioritizer
import psur_generator


# ── 轻本地端：所有检索外发 Coze（2026-09-07 移除本地降级路径）────────────────
# fetch_faers / fetch_fda_label / fetch_cn_pv 的「检索」全部经 Coze 统一端点外发；
# 本地仅保留计算（disproportionality / signal_score / check_event）与辅助检索
# （query_total / fetch_case_reports 直连 openFDA，结构化 state 无法上 Coze）。
try:
    _ADAPTERS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 os.pardir, "adapters")
    if _ADAPTERS_DIR not in sys.path:
        sys.path.insert(0, _ADAPTERS_DIR)
    import coze_dispatch
    _COZE_DISPATCH_OK = True
except Exception as _e:  # pragma: no cover
    coze_dispatch = None
    _COZE_DISPATCH_OK = False
    print("[WARN] coze_dispatch 不可用: %s" % _e)

if _COZE_DISPATCH_OK:
    # rebind 模块全局名 → 薄垫片：调用点零改动，下游无感消费同构 JSON
    fetch_faers = coze_dispatch.FaersShim(fetch_faers)
    fetch_fda_label = coze_dispatch.FdaLabelShim(fetch_fda_label)
    print("[ct_safety] 检索后端：Coze 统一端点 ct-search.coze.site（轻本地端 · 无本地降级）")
else:
    print("[ct_safety] 检索后端：coze_dispatch 不可用（部分功能受限）")


def enable_device_mode():
    """切换到 MAUDE（医疗器械不良事件）来源：把 fetch_faers 换成 DeviceEventShim。

    器械计数同样经 Coze 统一端点（source='maude'），本地不新增直连出口；2x2
    结构与 FAERS 同构，下游不均衡计算无需改动。需 Coze 侧已部署 maude 节点。
    """
    global fetch_faers
    real = getattr(fetch_faers, "_real", fetch_faers)
    fetch_faers = coze_dispatch.DeviceEventShim(real)
    return fetch_faers


def _render_top_events(data, drug, cn_pv=None, source="faers"):
    """Top-events-only report when no --event is supplied (no 2x2 disproportionality)."""
    drug_total = data.get("drug_total")
    top_ev = data.get("top_events", []) or []
    date_from = data.get("date_from")
    date_to = data.get("date_to")
    win = ""
    if date_from or date_to:
        win = "（时间窗 %s ~ %s）" % (date_from or "…", date_to or "…")
    _dev = (source in ("device", "maude"))
    lines = []
    lines.append("# MAUDE 器械不良事件概览 / MAUDE Device Event Overview\n" if _dev
                 else "# FAERS 安全性信号分析 / FAERS Safety Signal\n")
    lines.append("- %s: **%s**" % ("器械 Device" if _dev else "药物 Drug", drug))
    lines.append("- 事件 Event: **（未指定 — 仅列高频不良事件，未做信号检测）**")
    lines.append("- 数据源 Source: FDA MAUDE (openFDA device/event.json)" if _dev
                 else "- 数据源 Source: FDA FAERS (openFDA public API)")
    if win:
        lines.append("- 时间窗 Date window: **%s**" % win)
    lines.append("- %s: **%s**%s\n" % (
        "该器械报告总数 Device total reports" if _dev else "该药报告总数 Drug total reports",
        (drug_total if drug_total is not None else "?"), win))
    lines.append("## 高频不良事件 Top adverse events%s\n" % (
        "（器械事件类型 / device event type）" if _dev else " (MedDRA PT)"))
    if top_ev:
        lines.append("| 不良事件 Reaction (MedDRA PT) | SOC | 报告数 Count |")
        lines.append("|---|---|---|")
        for e in top_ev:
            term = e.get("term")
            soc = disproportionality.map_soc(term)
            lines.append("| %s | %s | %s |" % (term, soc, e.get("count")))
    else:
        lines.append("_（无数据）_")
    lines.append("")
    lines.append("> 未指定 `--event`，故仅展示该药高频不良事件；需对具体药物-事件组合做信号检测时，请加 `--event <MedDRA PT>`。")
    lines.append("> 仅供信号筛查，非因果结论；监管提交须按 GCP / ICH E2 另行评估。")
    # China official PV bulletins (qualitative corroboration only)
    lines.append("")
    lines.append("## 中国官方药物警戒通报 / China Official PV Bulletins (定性佐证 / Qualitative)\n")
    # 覆盖率提示：与 report.py 主路径保持一致，避免「抓取失败」被读成「官方无通报」
    if cn_pv:
        cov = cn_pv.get("coverage_note")
        if cov:
            lines.append("> 覆盖率 Coverage: %s\n" % cov)
        if cn_pv.get("degraded"):
            lines.append("> ⚠️ **本次抓取不完整**（存在栏目/文章失败）——0 命中不可解读为「官方无相关通报」。\n")
    if cn_pv and cn_pv.get("hit_count"):
        lines.append("命中 **%d** 条（当前 `--cn-max-pages` 页 / `--cn-since` 日期窗内）：\n"
                     % cn_pv["hit_count"])
        tier_counts = cn_pv.get("tier_counts")
        if tier_counts:
            tier_disp = "、".join("%s %d" % (k, v) for k, v in tier_counts.items() if v)
            if tier_disp:
                lines.append("按佐证等级 / By evidence tier: %s\n" % tier_disp)
        lines.append("| 佐证等级 Tier | 日期 Date | 栏目 Column | 标题 Title | 命中词 Kw | 链接 Link |")
        lines.append("|---|---|---|---|---|---|")
        for h in cn_pv["hits"]:
            title = (h.get("title") or "").replace("|", "/")
            lines.append("| %s | %s | %s | %s | %s | [原文](%s) |" % (
                h.get("tier") or "-", h.get("date") or "-", h.get("column", "-"),
                title, ", ".join(h.get("matched_keywords", [])), h.get("url", "")))
    else:
        st = (cn_pv or {}).get("stats") or {}
        scanned = st.get("scanned", 0)
        if cn_pv is None:
            lines.append("未启用中国 PV 源（`--with-cn-pv`，或工作台勾选「中国药物警戒」）——"
                         "本节不参与本次分析，**不代表检索后零命中**。")
        elif scanned == 0:
            lines.append("**本次未扫描到任何通报条目（扫描 0 条 / %d 栏目）——覆盖率为零，"
                         "不可解读为「官方无相关通报」**；多为站点结构变更或网络受限所致，"
                         "请重跑或补中文事件词后复核。"
                         % len(cn_pv.get("searched_columns") or []))
        else:
            lines.append("未命中中国官方通报（已扫描 %d 条，当前 `--cn-max-pages` 页 / `--cn-since` 日期窗内）。"
                         "如需更广覆盖，可增大 `--cn-max-pages`、放宽 `--cn-since`，"
                         "或显式传入中文事件词 `--event-cn`。" % scanned)
    return "\n".join(lines)


def run(drug, event, field, top, api_key, out_dir, with_cn_pv=False,
        drug_cn=None, event_cn=None, cn_terms=None, cn_max=10,
        cn_max_pages=1, cn_since=None, cn_until=None, cn_use_cache=True,
        with_nmpa_coze=False, nmpa_out=None,
        date_from=None, date_to=None, benchmark_drugs=None, top_events_signal=None,
        continuity=True, trend=False, compare_drugs=None, with_fda_label=False,
        case_level=0, resolve_drug_name=True, with_causality=False,
        naranjo_evidence=None, verify_signal=False, code_verbatim=None,
        prioritize=False, psur=False, psur_period=None,
        case_dedup=True, dedup_jaccard=0.8, drop_suspected_dupes=False,
        lang="zh", source="faers"):
    # 不良事件维度（器材模式为 event_type，药品模式为 reaction MedDRA PT）
    ev_field = fetch_faers.SOURCE_DEFAULTS.get(source, {}).get(
        "ev_field", "patient.reaction.reactionmeddrapt")
    # 预处理：非 ASCII 药物名 → 英文标准名（CLI 菜单确认）
    if resolve_drug_name and drug_name_resolver.is_non_ascii(drug):
        resolved, _ = drug_name_resolver.resolve(drug, event=event, auto=True)
        if resolved:
            drug = resolved
        else:
            print("[ct_safety] 药物名为空或已取消，退出。")
            return None

    # P1-D: MedDRA verbatim -> PT coding helper (opt-in). If --code-verbatim is
    # given and no --event, use the top suggested PT as the event to analyse.
    # Pure local (built-in dict); the optional LLM mode is NOT auto-enabled.
    if code_verbatim:
        try:
            vc = meddra_coding.VerbatimCoder()
            coded = vc.code(code_verbatim, top_k=5)
            print("[ct_safety][meddra-coding] %r ->" % code_verbatim)
            for s in coded.get("suggested_pt", [])[:3]:
                print("   - %s (code=%s, soc=%s, conf=%.2f, %s)"
                      % (s["name"], s["code"], s.get("soc", ""),
                         s["confidence"], s.get("match_type")))
            print("   note: %s" % coded.get("coding_notes", ""))
            if event is None and coded.get("suggested_pt"):
                event = coded["suggested_pt"][0]["name"].upper()
                print("[ct_safety][meddra-coding] using top PT as --event: %s" % event)
        except Exception as e:  # noqa: BLE001 - best-effort helper
            print("[WARN] meddra coding failed (continues): %s" % e)

    os.makedirs(out_dir, exist_ok=True)
    fetch_json = os.path.join(out_dir, "faers_fetch.json")
    disp_json = os.path.join(out_dir, "disproportionality.json")
    md_out = os.path.join(out_dir, "faers_report.md")

    fetch_faers.fetch_counts(drug, event, field, top, api_key,
                             run=True, out=fetch_json,
                             date_from=date_from, date_to=date_to)
    # compute disproportionality from saved fetch (only when an event pair is given)
    data = json.load(open(fetch_json, encoding="utf-8"))
    cnt = data.get("counts")
    res = None
    if cnt is not None and event:
        res = disproportionality.compute(cnt["a"], cnt["b"], cnt["c"], cnt["d"],
                                         continuity=continuity)
        res["drug"] = drug
        res["event"] = event
        with open(disp_json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

    # Optional: China official PV bulletins (qualitative corroboration only)
    cn_pv = None
    trend_res = None
    if with_cn_pv:
        cn_pv_json = os.path.join(out_dir, "cn_pv.json")
        cn_drug = drug_cn or drug
        cn_event = event_cn or event
        if not drug_cn:
            print("[TIP] CN-PV uses --drug=%r on cdr-adr.org.cn; pass --drug-cn (Chinese "
                  "name) for higher recall." % drug)
        cn_pv = fetch_cn_pv.search(cn_drug, None, cn_event, cn_terms, cn_max,
                                  out=cn_pv_json,
                                  since=cn_since, until=cn_until,
                                  use_cache=cn_use_cache)

    # Optional: NMPA bulletins via Coze browser channel (WAF-blocked locally)
    nmpa_res = None
    if with_nmpa_coze:
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(
                os.path.abspath(__file__)), os.pardir, "adapters"))
            import nmpa_coze
        except ImportError:
            nmpa_coze = None
            print("[WARN] adapters/nmpa_coze.py not found; skip NMPA channel")
        if nmpa_coze is not None:
            nm_drug = drug_cn or drug
            nm_event = event_cn or event
            from cn_pv_keywords import expand_drug_keywords, expand_event_keywords
            nm_out = nmpa_out or os.path.join(out_dir, "nmpa_coze.json")
            nmpa_res = nmpa_coze.search_nmpa(
                expand_drug_keywords(nm_drug),
                expand_event_keywords(nm_event), cn_terms, cn_max_pages,
                run=True, out=nm_out)
            if nmpa_res and nmpa_res.get("hit_count"):
                if cn_pv is None:
                    cn_pv = {"source": "NMPA via coze", "hit_count": 0, "hits": []}
                cn_pv = dict(cn_pv)
                cn_pv["hit_count"] = cn_pv.get("hit_count", 0) + nmpa_res["hit_count"]
                # 保留服务端 nmpa_pv 节点定级的 tier（通报专文 / 提及），
                # 仅补 column 别名；tier 不强制覆盖。
                cn_pv["hits"] = list(cn_pv.get("hits", [])) + [
                    dict(h, column=h.get("source_column", "NMPA通报"),
                         tier=h.get("tier", "NMPA通报")) for h in nmpa_res["hits"]]
                cn_pv.setdefault("tier_counts", {})
                # 按服务端真实 tier 汇总；无 tier_counts 时回退单一键
                nmpa_tc = nmpa_res.get("tier_counts") or {}
                if nmpa_tc:
                    for _t, _c in nmpa_tc.items():
                        cn_pv["tier_counts"][_t] = cn_pv["tier_counts"].get(_t, 0) + _c
                else:
                    cn_pv["tier_counts"]["NMPA通报"] = cn_pv["tier_counts"].get(
                        "NMPA通报", 0) + nmpa_res["hit_count"]

    if res is not None:
        md = report_mod.render(res, cn_pv=cn_pv, source=source)
    else:
        # no event -> top adverse events only, no 2x2 disproportionality
        md = _render_top_events(data, drug, cn_pv=cn_pv, source=source)

    # ② case_id linkage (R14): fetch individual FAERS case safety reports when requested
    cases_data = None
    dedup_summary = None
    if case_level and event:
        faers_cases_json = os.path.join(out_dir, "faers_cases.json")
        try:
            cr = fetch_faers.fetch_case_reports(drug, event, field, n=case_level,
                                                run=True, out=faers_cases_json,
                                                date_from=date_from, date_to=date_to)
            cases_data = (cr or {}).get("cases")
        except Exception as e:  # noqa: BLE001 - best-effort; degrade gracefully
            print("[ct_safety][case-level] fetch failed: %s" % e)

        # P1-A: case-level de-duplication (pure local, zero extra network).
        # FAERS re-ingests the same case as follow-up report versions and via
        # multiple reporters, so a raw individual-case listing over-counts.
        # L1 (version collapse) is a correctness fix and is on by default;
        # L2 (suspected duplicates) only FLAGS unless --drop-suspected-dupes,
        # because silently dropping PV cases is dangerous.
        if case_dedup and cases_data:
            try:
                deduped, dedup_summary = faers_dedup.dedup_cases(
                    cases_data, jaccard_threshold=dedup_jaccard,
                    drop_suspected=drop_suspected_dupes)
                cases_data = deduped
                dedup_json = os.path.join(out_dir, "faers_cases_dedup.json")
                with open(dedup_json, "w", encoding="utf-8") as fp:
                    json.dump({"summary": dedup_summary, "cases": deduped},
                              fp, ensure_ascii=False, indent=2)
                print("[OK] case-level dedup -> %s (raw %d -> final %d)" % (
                    dedup_json, dedup_summary["raw_cases"],
                    dedup_summary["final_cases"]))
                md += _render_case_dedup(dedup_summary)
            except Exception as e:  # noqa: BLE001 - never break the report
                print("[WARN] case-level dedup failed (report continues): %s" % e)
                dedup_summary = None

    # R5: cross-competitor safety benchmarking — same event, horizontal comparison
    bench = None
    if benchmark_drugs:
        bench = _run_benchmark(benchmark_drugs, event, field, top, api_key,
                               out_dir, date_from, date_to, continuity=continuity)
        md += _render_benchmark(bench)

    # R13: multi-event safety signal detection for the focal drug (top AE terms)
    multi = None
    if top_events_signal:
        try:
            multi = _run_multi_event(drug, top_events_signal, field, top, api_key,
                                      out_dir, date_from, date_to, continuity=continuity,
                                      source=source, ev_field=ev_field)
            if multi:
                md += _render_multi_event(multi)
        except Exception as e:
            print("[WARN] R13 multi-event detection failed (report continues): %s" % e)

    # #5: temporal anomaly detection for the focal drug-event pair
    if trend and event:
        try:
            trend_res = _run_trend(drug, event, field, api_key, out_dir,
                                   date_from, date_to, source=source, ev_field=ev_field)
            md += _render_trend(trend_res)
        except Exception as e:
            print("[WARN] trend detection failed (report continues): %s" % e)
    elif trend and not event:
        print("[WARN] --trend requires --event; skipped")

    # P1-C: signal verification workflow (temporal / dose-response / deconvolution).
    # Reuses the trend quarterly series when --trend was also requested; otherwise
    # fetches the monthly series itself. Dose-response & deconvolution need
    # case-level data (--case-level) and gracefully report "insufficient" otherwise.
    if verify_signal and event:
        try:
            verify_res = _run_verify_signal(drug, event, field, api_key, out_dir,
                                            date_from, date_to, trend_res,
                                            source=source, ev_field=ev_field)
            md += _render_verify(verify_res)
        except Exception as e:
            print("[WARN] signal verification failed (report continues): %s" % e)
    elif verify_signal and not event:
        print("[WARN] --verify-signal requires --event; skipped")

    # #3: multi-drug comparison via adjusted ROR (focal vs pooled reference)
    if compare_drugs and len(compare_drugs) >= 2 and event:
        try:
            cmp = _run_compare_drugs(compare_drugs[0], compare_drugs[1:], event,
                                     field, top, api_key, out_dir,
                                     date_from, date_to)
            md += _render_compare(cmp)
        except Exception as e:
            print("[WARN] compare-drugs failed (report continues): %s" % e)
    elif compare_drugs and len(compare_drugs) < 2:
        print("[WARN] --compare-drugs needs >=2 drugs (focal + >=1 reference); skipped")
    elif compare_drugs and not event:
        print("[WARN] --compare-drugs requires --event; skipped")

    # #4: composite Safety Signal Score + evidence tier (FAERS x FDA Label x CN-PV)
    score_res = None
    if res is not None and event:
        try:
            label_status = "skipped"
            if with_fda_label:
                label_json = os.path.join(out_dir, "fda_label.json")
                label_data = fetch_fda_label.fetch_label(
                    drug, api_key, run=True, out=label_json)
                chk = fetch_fda_label.check_event(label_data, event)
                label_status = chk["status"]
            cn_hits = (cn_pv or {}).get("hit_count", 0) if cn_pv else 0
            trend_flag = False
            if trend_res:
                trend_flag = bool((trend_res.get("detection") or {}).get("anomaly_flag"))
            # lightweight control-anchor check (#6): if the queried drug-event is
            # itself a known positive/negative control, score pipeline agreement
            # without extra network calls.
            control_pair = None
            dk = str(drug).strip().lower()
            ek = str(event).strip().upper()
            for grp in ("positive", "negative"):
                for cd, ce in disproportionality.CONTROL_DRUGS[grp]:
                    if cd.lower() == dk and ce == ek:
                        control_pair = {"group": grp,
                                        "expected": grp == "positive",
                                        "signal": bool(res.get("signal_overall", False))}
                        break
                if control_pair:
                    break
            score_res = signal_score.safety_signal_score(
                res, fda_label_status=label_status, cn_pv_hits=cn_hits,
                trend_flag=trend_flag, control_pair=control_pair)
            md += _render_score(score_res, label_status, drug, event)
            # 2026-11-08: 同时落一份结构化评分产物，供工作台结果卡渲染。
            # 此前 score_res 只被渲染进 Markdown 文本，工作台无法读取
            # Safety Signal Score (0-100) 与证据分级 T1-T4。纯增量产物，
            # 不改变任何 CLI 行为；写失败不影响主报告。
            try:
                with open(os.path.join(out_dir, "signal_score.json"), "w",
                          encoding="utf-8") as fp:
                    json.dump(score_res, fp, ensure_ascii=False, indent=2)
            except Exception as e:
                print("[WARN] signal score json write failed: %s" % e)
        except Exception as e:
            print("[WARN] signal score failed (report continues): %s" % e)

    # P1-E (+K): signal prioritization & risk tiering. This layer ALSO consumes the
    # label-gap (expectedness from --with-fda-label) and the temporal-trend (from
    # --trend) -> this is exactly the "label-gap & temporal-trend signal
    # prioritization layer" called for in upgrade K.
    prio = None
    if prioritize and res is not None and event:
        try:
            prio = _run_prioritize(drug, event, res, multi, label_status,
                                  trend_res, cn_pv, bench, out_dir)
            if prio:
                md += _render_prioritize(prio, drug)
        except Exception as e:
            print("[WARN] prioritize failed (report continues): %s" % e)

    # P1-F: PSUR/PBRER auto-report generation from the detected signals.
    if psur and res is not None and event:
        try:
            psur_md = _run_psur(drug, event, res, multi, prio,
                                psur_period or "latest", out_dir, score_res)
            if psur_md:
                md += "\n\n" + psur_md
        except Exception as e:
            print("[WARN] psur generation failed (report continues): %s" % e)

    # P0-A: Naranjo causal-attribution layer (qualitative supplement, INDEPENDENT
    # of disproportionality). Only attached when explicitly requested (--with-causality)
    # and an event pair is present. Never feeds PRR/ROR/IC/EBGM.
    if with_causality and event:
        try:
            naranjo_ev = None
            if naranjo_evidence:
                if isinstance(naranjo_evidence, str):
                    naranjo_ev = causality._load_input(naranjo_evidence) \
                        if naranjo_evidence.endswith(".json") else None
                elif isinstance(naranjo_evidence, dict):
                    naranjo_ev = naranjo_evidence
            if naranjo_ev is None:
                if cases_data:
                    # aggregate FAERS case-level features (time / dechallenge /
                    # rechallenge) into a conservative representative evidence dict
                    naranjo_ev = causality.from_faers_cases(cases_data)
                else:
                    # no individual-case data: default unknowns, but if FDA label
                    # was checked, reflect known_reaction_pattern from label status
                    _kr = 0
                    if "label_status" in dir() and label_status == "labeled":
                        _kr = 1
                    elif "label_status" in dir() and label_status == "unlabeled":
                        _kr = -1
                    naranjo_ev = {"known_reaction_pattern": _kr}
            naranjo_res = causality.naranjo_assessment(
                naranjo_ev, meta={"drug": drug, "event": event})
            md += _render_causality(naranjo_res, drug, event)
            naranjo_json = os.path.join(out_dir, "naranjo_causality.json")
            with open(naranjo_json, "w", encoding="utf-8") as fp:
                json.dump(naranjo_res, fp, ensure_ascii=False, indent=2)
            print("[OK] naranjo causality ->", naranjo_json)
        except Exception as e:  # noqa: BLE001 - best-effort; degrade gracefully
            print("[WARN] naranjo causality failed (report continues): %s" % e)

    with open(md_out, "w", encoding="utf-8") as f:
        f.write(md)
    print("[OK] report ->", md_out)

    # Default deliverable is HTML (rich, viewable in the browser preview panel).
    html_out = os.path.join(out_dir, "faers_report.html")
    try:
        html = report_mod.wrap_html(
            report_mod.md_to_html(md),
            title="%s — %s | FAERS Safety Signal" % (drug, event))
        with open(html_out, "w", encoding="utf-8") as f:
            f.write(html)
        print("[OK] html report ->", html_out)
    except Exception as e:  # noqa: BLE001 - HTML is a best-effort companion output
        print("[WARN] html render failed (md still written): %s" % e)

    # Core companion deliverable: XLSX workbook with ALL raw information.
    xlsx_out = os.path.join(out_dir, "faers_report.xlsx")
    try:
        report_xlsx.build_signal_xlsx(
            xlsx_out, drug=drug, event=event, fetch_data=data,
            cases_data=cases_data, disp_res=res,
            cn_pv=cn_pv,
            label_data=label_data if (with_fda_label and res is not None and event) else None,
            label_status=label_status if (with_fda_label and res is not None and event) else None,
            score_res=score_res if (res is not None and event and with_fda_label) else None,
            lang=lang)
        print("[OK] xlsx workbook ->", xlsx_out)
    except Exception as e:  # noqa: BLE001 - XLSX is a best-effort companion output
        print("[WARN] xlsx render failed (html/md still written): %s" % e)

    # ---- final deliverable statement (two core artifacts) ----
    print("")
    print("======== 核心交付物 / Core Deliverables ========")
    print("  ① HTML 报告（可视化，便于快速阅读）: %s" % html_out)
    print("  ② XLSX 数据簿（全部原始信息与计算明细，供逐条查阅/审计）: %s" % xlsx_out)
    print("  — Markdown (%s) 仅作兼容备份。" % md_out)
    print("=================================================")
    return html_out


def _run_benchmark(drugs, event, field, top, api_key, out_dir, date_from, date_to, continuity=True):
    """R5: compute FAERS disproportionality for a set of competitor drugs against
    the SAME event, producing a horizontal safety comparison. Writes
    benchmark.json. Each drug is one openFDA query (no key needed, low-volume)."""
    import os as _os
    rows = []
    for d in drugs:
        tmp = _os.path.join(out_dir, "bench_%s.json" % re.sub(r"[^A-Za-z0-9]", "_", d))
        fetch_faers.fetch_counts(d, event, field, top, api_key,
                                 run=True, out=tmp,
                                 date_from=date_from, date_to=date_to)
        j = json.load(open(tmp, encoding="utf-8"))
        c = j.get("counts")
        if not c:
            print("[WARN] benchmark %r: no counts (event pair empty?)" % d)
            rows.append({"drug": d, "available": False})
            continue
        r = disproportionality.compute(c["a"], c["b"], c["c"], c["d"], continuity=continuity)
        r["drug"] = d
        r["event"] = event
        r["available"] = True
        rows.append(r)
    # R5+: Benjamini-Hochberg FDR control across benchmarked drugs (same event)
    _avail = [r for r in rows if r.get("available")]
    if _avail:
        _pvals = [r["PRR"]["p_value"] for r in _avail]
        _qs = disproportionality.benjamini_hochberg(_pvals)
        for _r, _q in zip(_avail, _qs):
            _r["fdr_q"] = round(_q, 6)
            _r["fdr_signal"] = _q < 0.05
    bench = {"event": event, "benchmark": rows}
    out = _os.path.join(out_dir, "benchmark.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(bench, f, ensure_ascii=False, indent=2)
    print("[OK] benchmark ->", out)
    return bench


# R13: terms that are NOT adverse events (terminal / disease-progression / etc.)
_NON_AE_HINTS = ("DEATH", "PROGRESSION", "RESISTANCE", "MUTATION", "OFF LABEL",
                "DISEASE", "NEOPLASM", "TUMOUR", "TUMOR", "CONDITION", "LABEL")


def _src_date_field(source):
    """数据源的日期维度字段：FAERS=receivedate，MAUDE(device)=date_received。"""
    cfg = getattr(fetch_faers, "SOURCE_DEFAULTS", {}) or {}
    return (cfg.get(source) or {}).get("date_field", "receivedate")


def _is_adverse_event(term):
    u = (term or "").upper()
    return not any(h in u for h in _NON_AE_HINTS)


def _run_multi_event(drug, top_n, field, top, api_key, out_dir, date_from, date_to,
                     continuity=True, source="faers", ev_field=None):
    """R13: detect FAERS disproportionality for the focal drug's top adverse
    events (excluding terminal / disease-progression terms).

    Performance / robustness: the up-front top-events + drug-total + grand-total
    query runs ONCE (via fetch_counts). For each of the top-N events we then issue
    only the TWO queries needed for the 2x2 (drug&event pair, and event total),
    reusing the already-known drug-total / grand-total.

    Each per-event query is run in a DAEMON THREAD with a hard join-timeout. This
    is the key guard: in some sandboxed network environments `requests`' own
    socket timeout is NOT reliably honored when openFDA holds a connection, so a
    single hung query could otherwise stall the whole sweep until the outer
    wall-clock kills the process silently. The thread cap guarantees a hung query
    is abandoned after ~20s and the event is skipped (not fatal). A global
    wall-clock budget additionally bounds the loop so the run always completes.
    """
    import os as _os
    import time as _time
    import threading
    _TIMEOUT, _RETRIES = 15, 1
    _HARD_CAP = _TIMEOUT + 5  # thread join ceiling; > requests timeout
    _WALL_BUDGET = 150  # seconds; break the event loop past this to stay < tool kill
    _START = _time.time()

    def _timed_total(search):
        box = {}
        def _worker():
            try:
                box["v"] = fetch_faers.query_total(search, api_key=api_key,
                                                  timeout=_TIMEOUT, retries=_RETRIES)
            except Exception as e:  # noqa: BLE001 - any failure => skip this event
                box["err"] = e
        th = threading.Thread(target=_worker, daemon=True)
        th.start()
        th.join(_HARD_CAP)  # hard cap regardless of requests' timeout honoring
        if th.is_alive():
            return None, "hard-timeout(>%ds)" % _HARD_CAP
        if "err" in box:
            return None, "%s: %s" % (type(box["err"]).__name__, box["err"])
        return box.get("v"), None

    fetch_json = _os.path.join(out_dir, "faers_top_events.json")
    if not _os.path.exists(fetch_json):
        try:
            fetch_faers.fetch_counts(drug, None, field, top, api_key, run=True,
                                     out=fetch_json, date_from=date_from,
                                     date_to=date_to, timeout=_TIMEOUT, retries=_RETRIES)
        except Exception as e:
            print("[WARN] top-events fetch failed: %s" % e)
    if not _os.path.exists(fetch_json):
        print("[WARN] cannot obtain top adverse events; skip R13 multi-event detection")
        return {"drug": drug, "events": [], "error": "top_events_fetch_failed"}
    data = json.load(open(fetch_json, encoding="utf-8"))
    drug_total = data.get("drug_total")
    grand_total = data.get("grand_total")
    clause = fetch_faers._date_clause(date_from, date_to,
                                      date_field=_src_date_field(source))
    if ev_field is None:
        ev_field = "patient.reaction.reactionmeddrapt"
    drug_term = '%s:"%s"%s' % (field, drug, clause)
    events = [e["term"] for e in data.get("top_events", [])
              if (e.get("term") or "").strip() and _is_adverse_event(e.get("term"))][:top_n]
    # 候选池口径留痕：池大小 / 被剔除的术语 / 实际筛查数，供报告显式披露
    _pool_terms = [e["term"] for e in data.get("top_events", []) if (e.get("term") or "").strip()]
    _dropped_terms = [t for t in _pool_terms if not _is_adverse_event(t)]
    rows = []
    for ev in events:
        if _time.time() - _START > _WALL_BUDGET:
            print("[WARN] multi-event time budget reached; remaining events skipped")
            break
        pair, err1 = _timed_total('%s AND %s:"%s"' % (drug_term, ev_field, ev))
        if err1:
            print("[WARN] multi-event %r pair query failed (skipped): %s" % (ev, err1))
            rows.append({"event": ev, "available": False})
            continue
        event_total, err2 = _timed_total('%s:"%s"%s' % (ev_field, ev, clause))
        if err2:
            print("[WARN] multi-event %r event-total query failed (skipped): %s" % (ev, err2))
            rows.append({"event": ev, "available": False})
            continue
        a = pair
        if drug_total is None or grand_total is None or event_total < a:
            print("[WARN] multi-event %r: inconsistent counts; skipped" % ev)
            rows.append({"event": ev, "available": False})
            continue
        b = drug_total - a
        c = event_total - a
        d = grand_total - a - b - c
        r = disproportionality.compute(a, b, c, d, continuity=continuity)
        r["event"] = ev
        r["available"] = True
        rows.append(r)
        _time.sleep(0.4)  # tiny gap between events to avoid hammering openFDA
    # R13+: Benjamini-Hochberg FDR control across all tested events
    _avail = [r for r in rows if r.get("available")]
    if _avail:
        _pvals = [r["PRR"]["p_value"] for r in _avail]
        _qs = disproportionality.benjamini_hochberg(_pvals)
        for _r, _q in zip(_avail, _qs):
            _r["fdr_q"] = round(_q, 6)
            _r["fdr_signal"] = _q < 0.05
    multi = {"drug": drug, "events": rows,
             "pool_size": len(_pool_terms),
             "dropped_terms": _dropped_terms,
             "screened": len(events),
             "requested": top_n}
    out = _os.path.join(out_dir, "multi_event_disp.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(multi, f, ensure_ascii=False, indent=2)
    print("[OK] multi-event dispatch ->", out)
    return multi


def _render_multi_event(multi):
    rows = [r for r in multi.get("events", []) if r.get("available")]
    if not rows:
        return "\n\n## 主药多事件安全性信号 (R13)\n\n_（无可用数据）_\n"

    def _n_fired(r):
        """How many of the four methods fired for this event."""
        return sum(1 for k in ("ROR", "PRR", "IC", "EBGM")
                   if (r.get(k) or {}).get("signal"))

    # 多方法阳性优先，其次按报告数；便于「先看最像信号的」
    rows = sorted(rows, key=lambda r: (-_n_fired(r), -(r["table"]["a"])))

    lines = ["\n\n## 主药多事件安全性信号 (R13) / Multi-Event Safety Signals\n"]
    lines.append("药物 Drug: **%s**（各 AE 相对全库自发报告的信号强度；"
                 "判定 ROR_lb>1 / PRR≥2&χ²≥4 / IC025>0 / EB05≥2，任一阳性即「信号=是」）\n"
                 % multi.get("drug"))
    lines.append("| 不良事件 Event | SOC | a | ROR (95% CI) | PRR (χ²) | IC025 | EBGM(EB05) | FDR(q) | 命中数 (of 4) | 信号 Signal |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        a = r["table"]["a"]
        ror = r["ROR"]; prr = r["PRR"]; ic = r["IC"]; eb = r.get("EBGM") or {}
        soc = disproportionality.map_soc(r["event"])
        q = r.get("fdr_q")
        fdr_disp = ("%.4f" % q) if q is not None else "—"
        sig = "是" if r["signal_overall"] else "否"
        lines.append("| %s | %s | %s | %.2f (%.2f–%.2f) | %.2f (%.0f) | %.2f | %.2f(%.0f) | %s | %d | %s |" % (
            r["event"], soc, int(a), ror["value"], ror["ci_low"], ror["ci_high"],
            prr["value"], prr["chi2"], ic["ci_low"], eb.get("value", 0.0), eb.get("eb05", 0.0),
            fdr_disp, _n_fired(r), sig))
    _pos = sum(1 for r in rows if r["signal_overall"])
    _multi = sum(1 for r in rows if _n_fired(r) >= 2)
    lines.append("\n**小结 Summary:** 本次实际筛查 **%d** 个事件，其中 **%d** 个判定为信号阳性，"
                 "**%d** 个为多方法（≥2 法）同时阳性。" % (len(rows), _pos, _multi))

    # 候选池 -> 实际筛查 的差额必须显式说明，否则读者会把「少了几个」误读为「只有这几个」
    _pool = multi.get("pool_size")
    _dropped = multi.get("dropped_terms") or []
    _unavail = [r["event"] for r in multi.get("events", []) if not r.get("available")]
    if _pool is not None and _pool > len(rows):
        _why = []
        if _dropped:
            _why.append("剔除终末/疾病进展类等非特异性术语 %d 个（%s）"
                        % (len(_dropped), "、".join(_dropped[:8])
                           + ("…" if len(_dropped) > 8 else "")))
        if _unavail:
            _why.append("查询超时/计数不一致未取得结果 %d 个（%s）"
                        % (len(_unavail), "、".join(_unavail[:8])
                           + ("…" if len(_unavail) > 8 else "")))
        if _why:
            lines.append("\n> ⚠️ **覆盖率 Coverage:** 候选事件池 %d 个 → 实际进入表格 %d 个；%s。"
                         "被剔除项仍可能是有意义的信号，需人工复核或单独指定 `--event`。"
                         % (_pool, len(rows), "；".join(_why)))

    lines.append("\n> 多事件信号仅作横向参考，各事件报告量/临床意义不同；FDR(q) 为 Benjamini-Hochberg "
                 "多重比较校正后的 q 值，q<0.05 表示该信号在整体错误发现率控制下仍显著。"
                 "PNEUMONITIS 等特异性信号须结合 RCT 与标签解读，非因果结论。")
    return "\n".join(lines)


def _render_benchmark(bench):
    """Render the cross-competitor safety benchmark as a Markdown comparison table."""
    rows = [r for r in bench.get("benchmark", []) if r.get("available")]
    if not rows:
        return "\n\n## 跨竞品安全性标杆 / Cross-Competitor Safety Benchmark (R5)\n\n_（无可用数据）_\n"
    lines = ["\n\n## 跨竞品安全性标杆 / Cross-Competitor Safety Benchmark (R5)\n"]
    lines.append("事件 Event: **%s**（与焦点资产同事件横向对比；信号判定 ROR_lb>1 / PRR≥2&χ²≥4 / IC025>0）\n"
                 % (bench.get("event") or "—"))
    soc = disproportionality.map_soc(bench.get("event") or "")
    lines.append("| 药物 Drug | SOC | a | ROR (95% CI) | PRR (χ²) | IC025 | EBGM(EB05) | FDR(q) | 信号 Signal |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in bench.get("benchmark", []):
        if not r.get("available"):
            lines.append("| %s | — | — | — | — | — | — | — | 无可用数据 |" % r.get("drug", "?"))
            continue
        a = r["table"]["a"]
        ror = r["ROR"]; prr = r["PRR"]; ic = r["IC"]; eb = r.get("EBGM") or {}
        q = r.get("fdr_q")
        fdr_disp = ("%.4f" % q) if q is not None else "—"
        sig = "是" if r["signal_overall"] else "否"
        lines.append("| %s | %s | %s | %.2f (%.2f–%.2f) | %.2f (%.0f) | %.2f | %.2f(%.0f) | %s | %s |" % (
            r["drug"], soc, int(a), ror["value"], ror["ci_low"], ror["ci_high"],
            prr["value"], prr["chi2"], ic["ci_low"], eb.get("value", 0.0), eb.get("eb05", 0.0),
            fdr_disp, sig))
    lines.append("\n> 标杆仅作横向信号强度参考，非因果比较；各药报告量/适应症人群不同，须结合说明书与头对头研究解读。")
    return "\n".join(lines)


def _run_trend(drug, event, field, api_key, out_dir, date_from, date_to,
               source="faers", ev_field=None):
    """#5: fetch the (drug, event) monthly reporting series (one receivedate count
    facet), aggregate to quarters, and run anomaly detection (CUSUM / rolling Z /
    changepoint). Writes trend.json. *ev_field* selects the adverse-event
    dimension (reaction MedDRA PT for FAERS, event_type for MAUDE)."""
    import os as _os
    if ev_field is None:
        ev_field = "patient.reaction.reactionmeddrapt"
    monthly = time_series.fetch_monthly_series(drug, event, field, api_key,
                                               date_from, date_to,
                                               fetch_mod=fetch_faers,
                                               ev_field=ev_field,
                                               date_field=_src_date_field(source))
    quarterly = time_series.to_quarterly(monthly)
    series = [q["count"] for q in quarterly]
    det = time_series.detect_anomaly(series)
    res = {"drug": drug, "event": event, "monthly": monthly,
           "quarterly": quarterly, "detection": det}
    out = _os.path.join(out_dir, "trend.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("[OK] trend ->", out)
    return res


def _render_trend(trend):
    q = trend.get("quarterly") or []
    if not q:
        return "\n\n## 时间趋势异常 / Time-Series Anomaly\n\n_（无可用月度数据）_\n"
    det = trend.get("detection") or {}
    lines = ["\n\n## 时间趋势异常 / Time-Series Anomaly (季度报告数)\n"]
    lines.append("药物 Drug: **%s** / 事件 Event: **%s**（季度报告数随时间的突变检测；"
                 "CUSUM / rolling Z / changepoint）\n" % (trend.get("drug"), trend.get("event")))
    lines.append("| 季度 Quarter | 报告数 Count |")
    lines.append("|---|---|")
    for x in q:
        lines.append("| %s | %s |" % (x["q"], x["count"]))
    flag = det.get("anomaly_flag")
    lines.append("\n- 总体判定 Overall: **%s**" % (
        "⚠️ 检测到异常抬升" if flag else "未检测到显著时间异常"))
    if det.get("cusum_flag"):
        lines.append("- CUSUM：持续正向偏移（累积和=%.2f）" % det.get("cusum_max"))
    if det.get("rolling_z_flag"):
        lines.append("- Rolling Z：单季尖峰（z=%.2f @ 第 %s 季）" % (
            det.get("rolling_z"), det.get("rolling_z_at")))
    if det.get("changepoint_idx") is not None:
        lift = det.get("changepoint_lift")
        lines.append("- Changepoint：均数阶跃（t=%.2f，抬升 %s）" % (
            det.get("changepoint_t"),
            ("%.1f%%" % (lift * 100)) if lift is not None else "—"))
    lines.append("\n> 时间趋势仅反映报告数相对历史水平的突变，受媒体关注 / 法规提醒等人为因素显著影响；"
                 "须结合 RCT 与标签变更解读，非因果结论。")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# P1-C: signal verification workflow (temporal / dose-response / deconvolution)
# ---------------------------------------------------------------------------
def _run_verify_signal(drug, event, field, api_key, out_dir,
                      date_from, date_to, trend_res=None,
                      source="faers", ev_field=None):
    """Fetch (or reuse) the (drug, event) quarterly reporting series and run the
    signal-verification workflow: temporal CUSUM/Poisson, dose-response and
    deconvolution. Dose-response & deconvolution need case-level data (--case-level)
    and report 'insufficient_data' when absent. Writes signal_verification.json."""
    import os as _os
    if ev_field is None:
        ev_field = "patient.reaction.reactionmeddrapt"
    if trend_res and trend_res.get("quarterly"):
        quarterly = trend_res["quarterly"]
    else:
        monthly = time_series.fetch_monthly_series(drug, event, field, api_key,
                                                   date_from, date_to,
                                                   fetch_mod=fetch_faers,
                                                   ev_field=ev_field,
                                                   date_field=_src_date_field(source))
        quarterly = time_series.to_quarterly(monthly)
    ts_data = [{"period": q["q"], "count": q["count"]} for q in quarterly]
    temporal = signal_verification.temporal_analysis(drug, event, ts_data)
    dose = signal_verification.dose_response_analysis(drug, event, [])
    deconv = signal_verification.deconvolution_analysis(drug, event, "", [])
    res = {"drug": drug, "event": event, "temporal": temporal,
           "dose_response": dose, "deconvolution": deconv}
    out = _os.path.join(out_dir, "signal_verification.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("[OK] signal verification ->", out)
    return res


def _render_verify(v):
    t = v.get("temporal") or {}
    lines = ["\n\n## 信号验证工作流 / Signal Verification (P1-C)\n"]
    lines.append("药物 Drug: **%s** / 事件 Event: **%s**\n" % (v.get("drug"), v.get("event")))
    lines.append("- 时序证据强度 Temporal evidence: **%s**" % t.get("evidence_level", "N/A"))
    cusum = t.get("cusum") or {}
    poi = t.get("poisson_trend") or {}
    if cusum:
        lines.append("  - CUSUM: %s (max=%.2f)" % (cusum.get("trend"), cusum.get("cusum_max", 0)))
    if poi:
        lines.append("  - Poisson 趋势: %s (p=%.4f, %s)" % (
            poi.get("trend"), poi.get("p_value", 1),
            "显著" if poi.get("significant") else "不显著"))
    lines.append("- 时序结论 Conclusion: %s" % t.get("conclusion", "—"))
    d = v.get("dose_response") or {}
    if d.get("error"):
        lines.append("- 剂量-反应 Dose-response: %s（需 --case-level 个案级剂量数据）" % d.get("error"))
    dc = v.get("deconvolution") or {}
    lines.append("- 去卷积 Deconvolution: %s" % dc.get("conclusion", dc.get("deconvolution", "—")))
    lines.append("\n> 验证工作流为信号确证补充：时序趋势增强报告数突变的可信度；剂量-反应与去卷积需个案级 FAERS 数据方能计算，公开计数接口仅支持时序维度。")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# P1-E (+K): signal prioritization & risk tiering layer
#   K = the layer ALSO ingests label-gap (expectedness from --with-fda-label)
#       and temporal-trend (from --trend) as two of its scoring dimensions.
# ---------------------------------------------------------------------------
_SOC_SEVERITY = {
    "Cardiac disorders": "hospitalization",
    "Hepatobiliary disorders": "hospitalization",
    "Vascular disorders": "life_threatening",
    "Respiratory, thoracic and mediastinal disorders": "hospitalization",
    "Renal and urinary disorders": "hospitalization",
    "Blood and lymphatic system disorders": "hospitalization",
    "Nervous system disorders": "hospitalization",
    "Immune system disorders": "life_threatening",
    "Psychiatric disorders": "important_medical_event",
    "Endocrine disorders": "requires_intervention",
    "Eye disorders": "requires_intervention",
    "Infections and infestations": "important_medical_event",
    "Skin and subcutaneous tissue disorders": "moderate",
    "Gastrointestinal disorders": "moderate",
    "Musculoskeletal and connective tissue disorders": "moderate",
    "Metabolism and nutrition disorders": "moderate",
    "General disorders and administration site conditions": "mild",
}


def _soc_severity(soc):
    return _SOC_SEVERITY.get(soc, "moderate")


def _run_prioritize(drug, event, res, multi, label_status, trend_res,
                   cn_pv, bench, out_dir):
    """Assemble detected signals (single + multi-event) and prioritize by risk tier.
    label_gap (K): an UNLABELED event is treated as a new signal; temporal-trend (K):
    an anomaly raises the trend dimension."""
    import os as _os
    label_gap = (label_status == "unlabeled")
    novelty = ("new_signal" if label_gap
               else ("expected_event" if label_status == "labeled" else "unknown"))
    trend_flag = bool((trend_res or {}).get("detection", {}).get("anomaly_flag"))
    trend_dim = "increasing" if trend_flag else ("stable" if trend_res else "unknown")
    has_cn = bool(cn_pv and cn_pv.get("hit_count"))
    has_bench = bool(bench)
    if has_cn and has_bench:
        multi_src = "three_source"
    elif has_cn or has_bench:
        multi_src = "two_source"
    else:
        multi_src = "single_source"

    signals = []
    if res is not None and event:
        signals.append({
            "signal_id": "S1", "drug": drug, "event": event,
            "severity": _soc_severity(disproportionality.map_soc(event)),
            "novelty": novelty, "frequency": int(res["table"]["a"]),
            "trend": trend_dim, "multi_source": multi_src,
        })
    if multi:
        for i, r in enumerate(
                [x for x in multi.get("events", []) if x.get("available")], start=2):
            ev = r["event"]
            signals.append({
                "signal_id": "M%d" % i, "drug": drug, "event": ev,
                "severity": _soc_severity(disproportionality.map_soc(ev)),
                "novelty": "unknown", "frequency": int(r["table"]["a"]),
                "trend": "unknown", "multi_source": multi_src,
            })
    if not signals:
        print("[WARN] no signals to prioritize")
        return None
    pr = signal_prioritizer.SignalPrioritizer()
    results = pr.prioritize(signals)
    out = _os.path.join(out_dir, "priority.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("[OK] priority ->", out)
    return results


def _render_prioritize(results, drug):
    lines = ["\n\n## 信号优先级排序与风险分级 / Signal Prioritization & Risk Tier (P1-E)\n"]
    lines.append("（合并 label-gap 预期性 + 时间趋势维度 = K 的优先级层）\n")
    lines.append("| 排名 | 药物 | 事件 | 得分 | 风险等级 | 建议 |")
    lines.append("|---|---|---|---|---|---|")
    for i, r in enumerate(results, 1):
        lines.append("| %d | %s | %s | %.2f | %s | %s |" % (
            i, r["drug"], r["event"], r["priority_score"],
            r["risk_level"], r["action_recommendation"]))
    lines.append("\n> 风险分级为自动化综合研判辅助（临床严重程度 × 新颖性 × 频率 × 趋势 × 多源），非监管结论；须医学审核。")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# P1-F: PSUR/PBRER auto-report generation
# ---------------------------------------------------------------------------
def _run_psur(drug, event, res, multi, prio, period, out_dir, score_res=None):
    """Build a signal list (single + multi-event) and generate a PSUR/PBRER
    markdown report. Risk tier from the prioritization layer (P1-E) when available.
    Writes psur.md."""
    import os as _os
    prio_by_event = {p["event"]: p for p in (prio or [])}

    def _row(d, ev, r):
        p = prio_by_event.get(ev, {})
        prr = (r.get("PRR") or {}).get("value")
        ror = (r.get("ROR") or {}).get("value")
        ebgm = (r.get("EBGM") or {}).get("value")
        ic = (r.get("IC") or {}).get("value")
        # 证据分级 T1-T4 只在焦点药-事件上有（综合评分层产出），多事件行留空
        tier = None
        if score_res and ev == event:
            tier = score_res.get("tier") or score_res.get("evidence_tier")
        return {
            "drug": d, "event": ev,
            "prr": prr, "ror": ror, "ebgm": ebgm, "ic": ic, "tier": tier,
            "status": "new",
            "risk_level": p.get("risk_level", "MEDIUM"),
            "action": p.get("action_recommendation", "常规评估"),
        }

    signals = []
    if res is not None and event:
        signals.append(_row(drug, event, res))
    if multi:
        for r in [x for x in multi.get("events", []) if x.get("available")]:
            signals.append(_row(drug, r["event"], r))
    if not signals:
        return None
    report = psur_generator.generate_psur(signals, period, fmt="md")
    out = _os.path.join(out_dir, "psur.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(report)
    print("[OK] PSUR ->", out)
    return report


def _run_compare_drugs(focal, refs, event, field, top, api_key, out_dir,
                       date_from, date_to):
    """#3: compare the FOCAL drug against a POOLED reference group on a single
    event, computing an aggregate adjusted ROR (aROR). Each drug is one openFDA
    query (pair count a + drug total n); the reference group is pooled. Writes
    compare_drugs.json."""
    import os as _os

    def _fetch(d):
        tmp = _os.path.join(out_dir, "cmp_%s.json" % re.sub(r"[^A-Za-z0-9]", "_", d))
        fetch_faers.fetch_counts(d, event, field, top, api_key, run=True, out=tmp,
                                 date_from=date_from, date_to=date_to)
        j = json.load(open(tmp, encoding="utf-8"))
        c = j.get("counts")
        if not c:
            return None
        return {"a": c["a"], "n": j.get("drug_total")}

    f = _fetch(focal)
    if not f:
        print("[WARN] compare focal %r: no counts" % focal)
        return {"focal": focal, "event": event, "error": "focal_no_counts"}
    ref_rows = []
    ra_sum = 0
    rn_sum = 0
    for r in refs:
        rr = _fetch(r)
        if not rr:
            print("[WARN] compare ref %r: no counts (skipped)" % r)
            continue
        ra_sum += rr["a"]
        rn_sum += rr["n"]
        ref_rows.append({"drug": r, "a": rr["a"], "n": rr["n"]})
    if rn_sum == 0:
        print("[WARN] compare: all references empty; skipped")
        return {"focal": focal, "event": event, "error": "ref_empty"}
    agg = adjust_ror.adjusted_ror_aggregate(f["a"], f["n"], ra_sum, rn_sum)
    res = {"focal": focal, "event": event, "focal_a": f["a"], "focal_n": f["n"],
           "ref_pooled_a": ra_sum, "ref_pooled_n": rn_sum,
           "ref_drugs": ref_rows, "aROR": agg}
    out = _os.path.join(out_dir, "compare_drugs.json")
    with open(out, "w", encoding="utf-8") as fp:
        json.dump(res, fp, ensure_ascii=False, indent=2)
    print("[OK] compare-drugs ->", out)
    return res


def _render_compare(cmp):
    if cmp.get("error"):
        return "\n\n## 多药比较 · 调整 ROR (aROR)\n\n_（%s）_\n" % cmp["error"]
    focal = cmp["focal"]; ev = cmp["event"]; ar = cmp["aROR"]
    ref_names = ", ".join(r["drug"] for r in cmp["ref_drugs"]) or "—"
    soc = disproportionality.map_soc(ev)
    lines = ["\n\n## 多药比较 · 调整 ROR (aROR) / Multi-Drug Comparison\n"]
    lines.append("焦点药 Focal: **%s** vs 参照组合池 Pooled reference（%s），事件 Event: **%s**\n"
                 % (focal, ref_names, ev))
    lines.append("- 目标 SOC（按事件归类）: **%s**" % soc)
    lines.append("| 药物 Drug | 事件报告数 a | 该药总报告 n |")
    lines.append("|---|---|---|")
    lines.append("| %s (焦点) | %s | %s |" % (focal, cmp["focal_a"], cmp["focal_n"]))
    for r in cmp["ref_drugs"]:
        lines.append("| %s (参照) | %s | %s |" % (r["drug"], r["a"], r["n"]))
    lines.append("\n### 调整 ROR (aROR, 聚合层面)\n")
    lines.append("- aROR = %.3f（95%% CI %.3f–%.3f）" % (ar["or"], ar["ci_low"], ar["ci_high"]))
    verdict = ("焦点药在该事件上报告倾向**高于**参照组" if ar["signal"]
               else "焦点药在该事件上报告倾向不高于参照组")
    lines.append("- 判定：%s%s" % (verdict, " ⚠️" if ar["signal"] else ""))
    if ar["sparse"]:
        lines.append("- ⚠️ 稀疏表（含零细胞），已启用 Haldane-Anscombe 连续性校正，结果保守。")
    lines.append("\n> aROR 为 FAERS **聚合层面**焦点药 vs 参照组合池的调整报告比值；"
                 "未纳入个体协变量（年龄 / 性别 / 合并用药），因 openFDA 计数接口不提供个案。"
                 "若需真正协变量调整，请用个体级 `logistic_irls`（adjust_ror.py）拉取个案后计算。"
                 "仅作横向参考，非因果比较。")
    return "\n".join(lines)


def _render_score(score, label_status, drug, event):
    """Render the composite Safety Signal Score + evidence tier section (#4)."""
    sc = score.get("score")
    tier = score.get("tier")
    tier_label = score.get("tier_label")
    comp = score.get("components", {})
    corr = score.get("corroborate_sources", [])
    lines = ["\n\n## 综合安全信号评分与证据分级 / Composite Safety Signal Score & Evidence Tier (#4)\n"]
    lines.append("药物 Drug: **%s** / 事件 Event: **%s**\n" % (drug, event))
    lines.append("### 定量评分 Safety Signal Score: **%s / 100**\n" % sc)
    lines.append("- 证据分级 Evidence Tier: **%s — %s**" % (tier, tier_label))
    lines.append("- 独立佐证源 Corroborating sources: %s" % (
        "、".join(corr) if corr else "（无独立源佐证）"))
    lines.append("\n### 评分分量 Components\n")
    labels = {
        "faers_base": "FAERS 信号强度 (≤50)",
        "fdr": "FDR 多重比较一致性 (≤10)",
        "trend": "时间序列异常 #5 (≤15)",
        "cn_pv": "中国 PV 定性佐证 (≤20)",
        "controls": "控制验证一致性 #6 (≤10)",
        "label_extra": "FDA Label 新信号 (≤5)",
    }
    lines.append("| 分量 Component | 得分 Points |")
    lines.append("|---|---|")
    for k, lab in labels.items():
        lines.append("| %s | %s |" % (lab, comp.get(k, 0)))
    lines.append("\n- 一句话理由 Rationale: %s" % score.get("rationale", ""))
    if label_status == "labeled":
        lines.append("\n> FDA 标签**已收录**该风险（已知 / 预期风险）。")
    elif label_status == "unlabeled":
        lines.append("\n> ⚠️ FDA 标签**未收录**该风险 — 提示为**新信号 / 未预期**风险，优先级提升。")
    elif label_status == "unknown":
        lines.append("\n> FDA 标签检索无结果，无法判断 labeled / unlabeled。")
    else:
        lines.append("\n> 未启用 FDA Label 源（--with-fda-label）；当前为 FAERS × 中国 PV 双源 + 置信因子。")
    lines.append("\n> 评分与分级为自动化综合研判辅助，非监管结论；最终须结合 RCT、标签与临床判断。")
    return "\n".join(lines)


def _render_causality(assessment, drug, event):
    """Render the Naranjo causality attribution as an INDEPENDENT report section.

    P0-A: qualitative supplement only. The section title and body explicitly state
    that this score is NON-CAUSAL, is NOT mixed with disproportionality statistics,
    and is NOT fed into PRR / ROR / IC / EBGM. Wording uses "提示/可能" (suggests /
    may), never "证明" (proves).
    """
    cat = assessment.get("category_zh", "—")
    code = assessment.get("category_code", "—")
    total = assessment.get("total", 0)
    lines = ["\n\n## Naranjo 因果归因（定性补充，non-causal，不作为因果结论）\n"]
    lines.append("药物 Drug: **%s** / 事件 Event: **%s**\n" % (drug, event))
    lines.append("- 归因判定 Causality category: **%s (%s)**" % (cat, code))
    lines.append("- Naranjo 总分 Total score: **%d**" % total)
    lines.append("\n### 7 准则打分 / Seven Criteria\n")
    lines.append("| # | 准则 Criterion | 问题 Question | 得分 Score |")
    lines.append("|---|---|---|---|")
    for i, c in enumerate(assessment.get("criteria", []), 1):
        sc = c.get("score", 0)
        sc_disp = ("+1" if sc > 0 else ("-1" if sc < 0 else "0"))
        lines.append("| %d | %s / %s | %s | %s |" % (
            i, c.get("zh"), c.get("en"), c.get("question"), sc_disp))
    lines.append("\n> ⚠️ **本模块为纯启发式、定性、non-definitive 的因果归因补充，**"
                 "用于提示该药物-事件组合**可能**属于 drug-specific / class-wide / confounding 中的哪类线索。")
    lines.append("> **该分数不与 dispropor­tionality 统计信号混算，也不喂入 PRR / ROR / IC / EBGM**"
                 "——它独立于上述定量信号，仅作定性旁证。")
    lines.append("> 文案用「提示 / 可能」而非「证明」；自发报告存在报告偏倚、混杂与低报，"
                 "Naranjo 评分**不能建立因果结论**，须结合 RCT、产品标签与合格临床/监管判断（ICH E2 家族）。")
    lines.append("> 缺字段默认按「未知 (unknown = 0)」兜底，避免对证据不足的准则过度声称。")
    return "\n".join(lines)


def _render_case_dedup(s):
    """P1-A: render the case-level de-duplication audit trail as a report section.

    FAERS re-ingests the same case as follow-up report versions and through
    multiple reporters, so a raw individual-case listing over-counts. This
    section states exactly how many records were collapsed / flagged and — most
    importantly — that disproportionality (PRR/ROR/IC/EBGM) is NOT corrected,
    because those counts come from openFDA aggregate endpoints.
    """
    if not s:
        return ""
    raw = s.get("raw_cases", 0)
    final = s.get("final_cases", 0)
    lines = ["\n\n## 个案级去重 / Case-level de-duplication (P1-A)\n"]
    lines.append("| 环节 Stage | 计数 Count |")
    lines.append("|---|---|")
    lines.append("| 原始个案 Raw cases | %d |" % raw)
    lines.append("| L1 后续报告版本折叠 Version collapse (same safetyreportid) | -%d |"
                 % s.get("l1_versions_superseded", 0))
    lines.append("| L1 后个案 After L1 | %d |" % s.get("after_l1_version_collapse", 0))
    lines.append("| L2 疑似重复 Suspected duplicates (flagged) | %d（exact %d / probable %d，"
                 "%d 簇 clusters） |" % (
                     s.get("l2_suspected_duplicate_cases", 0), s.get("l2_exact", 0),
                     s.get("l2_probable", 0), s.get("l2_clusters", 0)))
    if s.get("drop_suspected"):
        lines.append("| L2 已剔除 Dropped (--drop-suspected-dupes) | -%d |"
                     % s.get("l2_dropped", 0))
    lines.append("| **最终个案 Final cases** | **%d** |" % final)
    if raw and final != raw:
        lines.append("\n- 去重率 De-duplication rate: **%.1f%%**（%d → %d）"
                     % (100.0 * (raw - final) / raw, raw, final))
    lines.append("- L2 Jaccard 阈值 threshold: **%.2f**（人口学一致 + 反应 PT 集合相似度）"
                 % float(s.get("jaccard_threshold", 0.8)))
    if not s.get("drop_suspected"):
        lines.append("- L2 策略 Policy: **仅标记不删除 flag-only**"
                     "（药物警戒场景静默删除病例有风险；需剔除请显式加 `--drop-suspected-dupes`）")
    lines.append("- 逐条依据见 `faers_cases_dedup.json` 的 `dedup_reason` / `dedup_level` 字段。")
    lines.append("\n> ⚠️ **重要局限 Limitation**：%s" % s.get("limitation", ""))
    lines.append("> 换言之：本段修正的是**个案清单**的重复计数偏倚，"
                 "**不修正**上文 PRR / ROR / IC / EBGM——后者的分子分母来自 openFDA 聚合端点，"
                 "本地无从拆到病例层面。解读信号强度时须记住 FAERS 计数本身仍含重复上报偏倚。")
    return "\n".join(lines)


def _run_validate_controls(out_dir, api_key, field, top, continuity=True):
    """--validate-controls: fetch known positive/negative control pairs from FAERS,
    compute disproportionality (with continuity correction), and check whether the
    pipeline flags positives as signals and does NOT flag negatives. Reports the
    agreement rate for each control group plus a Markdown summary.
    """
    import os as _os
    recs = []
    for group in ("positive", "negative"):
        for drug, event in disproportionality.CONTROL_DRUGS[group]:
            tmp = _os.path.join(out_dir, "ctrl_%s_%s.json" % (
                group, re.sub(r"[^A-Za-z0-9]", "_", "%s_%s" % (drug, event))))
            try:
                fetch_faers.fetch_counts(drug, event, field, top, api_key, run=True, out=tmp)
                j = json.load(open(tmp, encoding="utf-8"))
                c = j.get("counts")
                if not c:
                    recs.append({"drug": drug, "event": event, "group": group,
                                 "expected": group == "positive", "signal": None,
                                 "note": "no counts"})
                    continue
                r = disproportionality.compute(c["a"], c["b"], c["c"], c["d"],
                                               continuity=continuity)
                recs.append({"drug": drug, "event": event, "group": group,
                             "expected": group == "positive",
                             "signal": r["signal_overall"],
                             "ROR": r["ROR"]["value"], "PRR": r["PRR"]["value"]})
            except Exception as e:  # noqa: BLE001 - record and continue
                recs.append({"drug": drug, "event": event, "group": group,
                             "expected": group == "positive", "signal": None,
                             "note": "error: %s" % e})
    summary = disproportionality.summarize_control_validation(recs)
    out = _os.path.join(out_dir, "control_validation.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "records": recs}, f, ensure_ascii=False, indent=2)
    lines = ["\n\n## 流水线自检 / Pipeline Self-Validation (对照验证)\n"]
    lines.append("阳性对照 Positive controls（预期有信号）与阴性对照 Negative controls（预期无信号）"
                 "用于检验检测流水线是否系统性漏检/误报。连续性校正 continuity=%s。\n" % continuity)
    lines.append("| 组别 Group | 药物 Drug | 事件 Event | 预期 Expected | 实测信号 Signal | 一致 Match |")
    lines.append("|---|---|---|---|---|---|")
    for r in recs:
        exp = "有信号" if r["expected"] else "无信号"
        sig = "—" if r.get("signal") is None else ("是" if r["signal"] else "否")
        match = "—" if r.get("signal") is None else ("是" if r["signal"] == r["expected"] else "否")
        lines.append("| %s | %s | %s | %s | %s | %s |" % (
            r["group"], r["drug"], r["event"], exp, sig, match))
    p = summary["positive"]; n = summary["negative"]
    lines.append("\n- 阳性对照一致率 Positive agreement: %s/%s (%s)" % (
        p["agree"], p["n"], ("%.1f%%" % (p["rate"] * 100)) if p["rate"] is not None else "—"))
    lines.append("- 阴性对照一致率 Negative agreement: %s/%s (%s)" % (
        n["agree"], n["n"], ("%.1f%%" % (n["rate"] * 100)) if n["rate"] is not None else "—"))
    md = "\n".join(lines)
    md_out = _os.path.join(out_dir, "control_validation.md")
    with open(md_out, "w", encoding="utf-8") as f:
        f.write(md)
    print("[OK] control validation ->", out, md_out)
    return md


def main():
    ap = argparse.ArgumentParser(description="ct-safety pipeline (FAERS + optional CN-PV).")
    ap.add_argument("--drug", required=False, default=None,
                    help="target drug (MedDRA/INN; openFDA medicinalproduct form)")
    ap.add_argument("--event")
    ap.add_argument("--field", default="patient.drug.medicinalproduct")
    ap.add_argument("--device", action="store_true",
                    help="target MAUDE device adverse events instead of FAERS "
                         "(器械不良事件；经 Coze source='maude'，需 Coze 侧已部署 maude 节点；"
                         "默认维度字段切换为 patient.device.brand_name)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--api-key", help="openFDA API key (raises quota to 120k/day). "
                                        "Also read from env OPENFDA_API_KEY or skill-root .env (git-ignored). "
                                        "Optional: keyless anonymous quota works for low-volume use.")
    ap.add_argument("--date-from", help="filter receivedate >= YYYYMMDD (e.g. 20200101)")
    ap.add_argument("--date-to", help="filter receivedate <= YYYYMMDD (e.g. 20261231)")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--out-dir", default="./out")
    # #6: continuity correction + control validation
    ap.add_argument("--no-continuity", action="store_true",
                    help="disable Haldane-Anscombe continuity correction "
                         "(reproduce v0.1.8 behaviour)")
    ap.add_argument("--validate-controls", action="store_true",
                    help="run positive/negative control pairs to self-check the "
                         "detection pipeline (ignores --drug/--event)")
    # upgrade E (2026-09-29): user-supplied SOC map + external control benchmark
    ap.add_argument("--soc-map", default=None,
                    help="upgrade E: user PT→SOC extension file (JSON/CSV) merged over "
                         "the built-in dictionary; also honors env CT_SAFETY_SOC_MAP. "
                         "Sponsor's own licensed MedDRA mapping — never bundled.")
    ap.add_argument("--control-pairs", default=None,
                    help="upgrade E: external benchmark control-pairs file (JSON/CSV) "
                         "merged into the --validate-controls positive/negative set "
                         "(used with --validate-controls).")
    # #5: temporal anomaly detection (quarterly reporting-count jump)
    ap.add_argument("--trend", action="store_true",
                    help="detect temporal anomaly (quarterly reporting-count jump) "
                         "for --drug/--event (requires --event)")
    # #3: multi-drug comparison (adjusted ROR, focal vs pooled reference)
    ap.add_argument("--compare-drugs", nargs="*", default=None,
                    help="multi-drug comparison: FIRST drug = focal, rest = reference "
                         "pool; requires --event. e.g. --compare-drugs osimertinib "
                         "gefitinib erlotinib")
    # #4: multi-source triangulation — FDA Label (openFDA, no key) as 3rd source
    ap.add_argument("--with-fda-label", action="store_true",
                    help="include FDA Label (openFDA drug/label.json) as the 3rd "
                         "evidence source for the drug-event pair (requires --event); "
                         "flags labeled vs unlabeled risk")
    # optional CN-PV (qualitative corroboration)
    ap.add_argument("--with-cn-pv", action="store_true",
                    help="also search China official PV bulletins (cdr-adr.org.cn)")
    ap.add_argument("--drug-cn", help="Chinese drug name for CN-PV (higher recall)")
    ap.add_argument("--event-cn", help="Chinese event keyword for CN-PV")
    ap.add_argument("--cn-terms", nargs="*", help="extra AND keywords for CN-PV")
    ap.add_argument("--cn-max", type=int, default=10,
                    help="max latest articles scraped per CN-PV column")
    # CN-PV v2: pagination / date window / cache control
    ap.add_argument("--cn-max-pages", type=int, default=1,
                    help="CN-PV listing pages to traverse per column (default 1 = "
                         "latest page only; 3-5 covers history)")
    ap.add_argument("--cn-since", help="CN-PV date window start (YYYY or YYYY-MM-DD)")
    ap.add_argument("--cn-until", help="CN-PV date window end (YYYY or YYYY-MM-DD)")
    ap.add_argument("--cn-no-cache", action="store_true",
                    help="disable CN-PV result cache (cn_pv_cache.json)")
    # NMPA 通报 via Coze 浏览器通道（NMPA 主站 WAF 拦截，本地不直连）
    ap.add_argument("--with-nmpa-coze", action="store_true",
                    help="additionally search NMPA adverse-reaction bulletins via the "
                         "Coze browser channel (adapters/nmpa_coze.py); requires the "
                         "endpoint in adapters/config.json auto_approve_endpoints")
    ap.add_argument("--nmpa-out", default=None,
                    help="output JSON for the NMPA coze result "
                         "(default: <out-dir>/nmpa_coze.json)")
    # R5: cross-competitor safety benchmark (same event, horizontal comparison)
    ap.add_argument("--benchmark-drug", nargs="*", default=None,
                    help="competitor drugs to benchmark against the same --event "
                         "(FAERS disproportionality). e.g. --benchmark-drug gefitinib erlotinib")
    # R13: multi-event safety signal detection for the focal drug
    ap.add_argument("--top-events-signal", type=int, default=None,
                    help="R13: detect FAERS disproportionality for the top N focal-drug "
                         "adverse events (excluding terminal/disease-progression terms). "
                         "e.g. --top-events-signal 6")
    # R14 ②: individual FAERS case safety reports (case_id linkage)
    ap.add_argument("--case-level", type=int, default=0,
                    help="R14 ②: fetch up to N individual FAERS case safety reports "
                         "(case_id linkage). 0 = off. Requires --event (ignored "
                         "otherwise). NOTE: single-page fetch, hard cap 100 — "
                         "larger N is truncated with a warning; for bulk pulls "
                         "use scripts/fetch_reports.py --max <n> instead.")
    # P1-A: case-level de-duplication of the individual-case listing (pure local)
    ap.add_argument("--no-case-dedup", action="store_true",
                    help="P1-A: 关闭个案级去重（默认开启：L1 折叠同一 safetyreportid 的"
                         "后续报告版本，L2 仅标记疑似重复病例）")
    ap.add_argument("--dedup-jaccard", type=float, default=0.8,
                    help="P1-A: L2 疑似重复的反应 PT 集合 Jaccard 阈值（默认 0.8，越低越激进）")
    ap.add_argument("--drop-suspected-dupes", action="store_true",
                    help="P1-A: L2 疑似重复簇仅保留 1 条代表（默认只标记不删除；"
                         "药物警戒场景静默删除病例有风险，需显式开启）")
    # 非 ASCII 药物名自动翻译为英文名
    ap.add_argument("--no-resolve-drug-name", action="store_true",
                    help="禁用非 ASCII（如中文）药物名自动翻译为英文名的预处理")
    # P0-A: Naranjo 因果归因层（定性补充，non-causal；独立于 disproportionality）
    ap.add_argument("--with-causality", action="store_true",
                    help="附加 Naranjo 7 准则因果归因独立章节（定性补充，non-causal，"
                         "不与 PRR/ROR/IC/EBGM 混算）")
    ap.add_argument("--naranjo-evidence", help="Naranjo 证据 JSON 路径：单个 7 键 "
                    "evidence dict，或 FAERS 病例 dict 列表（用于从病例聚合）。"
                    "缺省则尝试用 --case-level 病例聚合，或按 unknown 兜底。")
    # ---- P1 upgrades (2026-08-16, v0.1.38) ----
    # P1-C: signal verification workflow (temporal / dose-response / deconvolution)
    ap.add_argument("--verify-signal", action="store_true",
                    help="P1-C: 运行信号验证工作流（时序 CUSUM/Poisson / 剂量-反应 / "
                         "去卷积）于 --drug/--event（需 --event 与 --run；复用 --trend 序列）")
    # P1-D: MedDRA verbatim -> PT coding helper (local default; LLM opt-in)
    ap.add_argument("--code-verbatim", default=None,
                    help="P1-D: 将 verbatim AE 术语编码为建议 PT（内置字典；LLM 模式 "
                         "为 opt-in，不自动开启）。未给 --event 时以首选项 PT 作为事件")
    # P1-E (+K): signal prioritization & risk tiering (ingests label-gap + trend)
    ap.add_argument("--prioritize", action="store_true",
                    help="P1-E: 按风险分级对信号排序（合并 --with-fda-label 的 label-gap "
                         "预期性 + --trend 的时间趋势维度 = K 的优先级层）")
    # P1-F: PSUR/PBRER auto-report generation
    ap.add_argument("--psur", action="store_true",
                    help="P1-F: 由检测到的信号自动生成 PSUR/PBRER Markdown 报告（psur.md）")
    ap.add_argument("--psur-period", default=None,
                    help="P1-F: PSUR 报告期间标签（如 2025-Q1 / 2026H1）")
    ap.add_argument("--lang", default="zh",
                    help="Report language: zh (default, Chinese UI) or en (English UI). "
                         "Workbench passes user's language preference; CLI defaults to zh.")
    args = ap.parse_args()

    # 器械不良事件（MAUDE）模式：切换到 DeviceEventShim + 器械默认维度字段。
    # 仅当用户未显式传 --field 时才改默认字段（显式 --field 优先）。
    if getattr(args, "device", False):
        if not _COZE_DISPATCH_OK:
            sys.exit("[错误] --device 依赖统一出口(coze_dispatch)以路由 source='maude'；"
                     "当前不可用。请检查 ct-safety/adapters/coze_dispatch.py 与端点配置。")
        enable_device_mode()
        if args.field == "patient.drug.medicinalproduct":
            args.field = "device.brand_name"
        print("[ct-safety] 模式：MAUDE 器械不良事件（source=maude，维度=%s）" % args.field)

    # upgrade E: apply user SOC map (CLI --soc-map wins over env), before any
    # map_soc() call downstream; and merge external control benchmark pairs.
    try:
        if getattr(args, "soc_map", None):
            n = disproportionality.load_user_soc_map(args.soc_map)
            print("[OK] user SOC map merged: %d entries" % n)
        else:
            n = disproportionality.init_soc_map_from_env()
            if n:
                print("[OK] user SOC map merged (env CT_SAFETY_SOC_MAP): %d entries" % n)
        if getattr(args, "control_pairs", None):
            added = disproportionality.load_control_pairs(args.control_pairs)
            print("[OK] external control pairs merged: positive+%s negative+%s"
                  % (added["positive"], added["negative"]))
    except Exception as _e:  # noqa: BLE001 - extension must never break the run
        print("[WARN] upgrade-E extension not applied: %s" % _e)

    # --validate-controls: standalone QA when no drug (early return), but when a
    # drug is also given it becomes an *add-on* to the focal-drug analysis instead
    # of short-circuiting it (workbench maps 对照验证 → --validate-controls, and
    # expects the drug signal result too). Previously this branch always returned,
    # which silently skipped the main FAERS pipeline whenever 对照验证 was on.
    if args.validate_controls and not args.drug:
        _run_validate_controls(args.out_dir, args.api_key, args.field, args.top,
                               continuity=not args.no_continuity)
        return

    if not args.drug:
        ap.error("--drug is required (unless --validate-controls)")

    if not args.run:
        if args.with_cn_pv:
            print("[PREVIEW] would run FAERS pipeline + CN-PV (cdr-adr.org.cn) for "
                  "drug=%r event=%r (use --run)" % (args.drug, args.event))
        elif args.benchmark_drug:
            print("[PREVIEW] would benchmark %r vs event=%r (use --run)"
                  % (args.benchmark_drug, args.event))
        else:
            print("[PREVIEW] would run FAERS pipeline for drug=%r event=%r (use --run)"
                  % (args.drug, args.event))
        return
    run(args.drug, args.event, args.field, args.top, args.api_key, args.out_dir,
        args.with_cn_pv, args.drug_cn, args.event_cn, args.cn_terms, args.cn_max,
        cn_max_pages=args.cn_max_pages, cn_since=args.cn_since,
        cn_until=args.cn_until, cn_use_cache=not args.cn_no_cache,
        date_from=args.date_from, date_to=args.date_to,
        benchmark_drugs=args.benchmark_drug, top_events_signal=args.top_events_signal,
        with_nmpa_coze=args.with_nmpa_coze, nmpa_out=args.nmpa_out,
        continuity=not args.no_continuity, trend=args.trend,
        compare_drugs=args.compare_drugs, with_fda_label=args.with_fda_label,
        case_level=args.case_level,
        resolve_drug_name=not args.no_resolve_drug_name,
        with_causality=args.with_causality,
        naranjo_evidence=args.naranjo_evidence,
        verify_signal=args.verify_signal, code_verbatim=args.code_verbatim,
        prioritize=args.prioritize, psur=args.psur, psur_period=args.psur_period,
        case_dedup=not args.no_case_dedup, dedup_jaccard=args.dedup_jaccard,
        drop_suspected_dupes=args.drop_suspected_dupes,
        lang=args.lang,
        source=("maude" if getattr(args, "device", False) else "faers"))
    # When 对照验证 (--validate-controls) is requested together with a focal drug,
    # run it as an add-on *after* the main pipeline (rather than replacing it).
    if args.validate_controls and args.drug:
        _run_validate_controls(args.out_dir, args.api_key, args.field, args.top,
                               continuity=not args.no_continuity)


if __name__ == "__main__":
    main()
