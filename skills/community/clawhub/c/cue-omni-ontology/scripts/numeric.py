"""cue-omni-ontology numeric pack (since 0.3.0; developed as unpublished dev-0.2.7..0.2.8) — deterministic numeric pack (host-extracted statement/note figures) + narrative items + credit-causal layer.

The host computes figures with deterministic code (no model) and narrative items with a model; this module only VALIDATES and SERVES:
  * numeric-import: every delta must carry, for BOTH years, value (number), unit, page (int), table_id and fy; every excerpt / quote /
    event line must be an exact substring of that page in the packaged source pages.
  * dev-0.2.8 replaces the size/total-assets severity with a deterministic CREDIT-CAUSAL ordering (see SKILL.md "Causal ordering"):
      drivers first   - collection deterioration (receivables vs revenue, provision jumps, aging shift, prepayments), cash vs short-term
                        debt coverage, overdue borrowings / defaults, guarantees and related-party funds, restricted cash, audit
                        opinion / going concern / error-correction restatements, then short-term debt growth;
      consequences    - net loss, impairment totals, goodwill write-downs, equity decline: ranked after drivers, each linked to the
                        drivers that plausibly explain it;
      explained-normal- same-control-merger restatements, presentation/basis changes (net vs gross, reclassification; statement line
                        unchanged), accounting-policy changes, scale changes from acquisitions/new consolidation: labelled and ranked last.
  * numeric: overview | drivers | consequences | normal | deltas | restatements | checks | narrative views."""
import json, hashlib, os, shutil
from pathlib import Path

NUMERIC_SCHEMA = "numeric-0.2"
class Invalid(ValueError): pass
def need(c, msg):
    if not c: raise Invalid(msg)
def _num(x): return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float("inf")

def load_pages(src_dir):
    pages = {}
    for f in sorted(Path(src_dir).glob("FY*.pages.jsonl")):
        fy = int(f.name[2:6]); d = {}
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.strip():
                p = json.loads(line); d[int(p["page"])] = p["text"]
        pages[fy] = d
    return pages

def _point_ok(pt, pages, where):
    need(isinstance(pt, dict), f"{where}: point must be an object")
    for k in ("fy", "value", "page", "table_id"):
        need(k in pt, f"{where}: missing {k}")
    need(_num(pt["value"]), f"{where}: value must be a finite number")
    need(isinstance(pt["page"], int) and pt["page"] > 0, f"{where}: page must be a positive int")
    need(isinstance(pt["table_id"], str) and pt["table_id"], f"{where}: table_id required")
    need(pt["fy"] in pages, f"{where}: no source pages for FY{pt['fy']}")
    need(pt["page"] in pages[pt["fy"]], f"{where}: page {pt['page']} not in FY{pt['fy']} source")
    ex = pt.get("excerpt")
    if ex:
        need(ex in pages[pt["fy"]][pt["page"]], f"{where}: excerpt is not verbatim on FY{pt['fy']} p{pt['page']}")
def _verbatim(fy, page, ex, pages, where):
    need(fy in pages and page in pages[fy], f"{where}: page not in sources")
    need(isinstance(ex, str) and ex and ex in pages[fy][page], f"{where}: excerpt not verbatim on FY{fy} p{page}")
# ----------------------------------------------------------------------------------------------- credit-causal layer (dev-0.2.8)
import re
# Deterministic, documented in SKILL.md "Causal ordering". Inputs: validated deltas, flags, aging, events, narrative, restatement
# classes supplied by the host. Nothing here calls a model.
CAT_CN = {"collection": "回款恶化", "liquidity": "现金对短期债务覆盖", "overdue_default": "逾期/违约", "guarantee_related": "担保与关联方资金",
          "restricted_cash": "受限资金", "audit_going_concern": "审计意见/持续经营/会计质量", "debt_growth": "债务扩张"}
DRIVER_ORDER = ["overdue_default", "audit_going_concern", "liquidity", "collection", "guarantee_related", "restricted_cash", "debt_growth"]
ITEM_ROLE = [  # (prefix/exact, role, category)
    ("应收账款-账龄", "driver", "collection"), ("应收账款坏账准备", "driver", "collection"), ("应收账款账面余额", "driver", "collection"),
    ("应收账款", "driver", "collection"), ("合同资产", "driver", "collection"), ("其他应收款坏账准备", "driver", "collection"),
    ("其他应收款", "driver", "guarantee_related"), ("预付款项", "driver", "collection"),
    ("已逾期未偿还", "driver", "overdue_default"), ("对外担保", "driver", "guarantee_related"), ("应收关联方", "driver", "guarantee_related"),
    ("受限货币资金", "driver", "restricted_cash"), ("货币资金", "driver", "liquidity"), ("短期借款", "driver", "liquidity"),
    ("一年内到期的非流动负债", "driver", "liquidity"), ("应付票据", "driver", "liquidity"),
    ("长期借款", "driver", "debt_growth"), ("应付债券", "driver", "debt_growth"), ("负债合计", "driver", "debt_growth"),
    ("商誉账面原值", "context", None), ("净利润", "consequence", "loss"), ("归属于母公司所有者的净利润", "consequence", "loss"), ("信用减值损失", "consequence", "impairment"),
    ("资产减值损失", "consequence", "impairment"), ("商誉减值准备", "consequence", "goodwill"), ("商誉", "consequence", "goodwill"),
    ("存货跌价准备", "consequence", "impairment"), ("归属于母公司所有者权益合计", "consequence", "equity"),
]
CONS_CN = {"loss": "亏损", "impairment": "减值损失", "goodwill": "商誉减记", "equity": "净资产下降"}
CONS_LINKS = {"impairment": ["collection", "audit_going_concern"], "loss": ["collection", "liquidity", "overdue_default", "guarantee_related", "audit_going_concern"],
              "goodwill": ["collection", "audit_going_concern"], "equity": ["collection", "liquidity", "overdue_default", "guarantee_related"]}
RESTATE_CLASS_OK = {None, "same_control_merger", "accounting_policy_change", "error_correction", "unexplained", "presentation_or_basis_change",
                    "same_control_merger+accounting_policy_change", "same_control_merger+error_correction", "accounting_policy_change+error_correction",
                    "same_control_merger+accounting_policy_change+error_correction"}
NORMAL_CN = {"same_control_merger": "同一控制下企业合并：上期数已按合并后口径重述（正常，非风险）",
             "presentation_or_basis_change": "列示/口径变化（净额与总额、明细重分类等），报表项目本身未变（正常，非风险）",
             "accounting_policy_change": "会计政策变更带来的追溯调整或期初调整（正常，非风险）",
             "acquisition_scale_change": "非同一控制下收购/新纳入合并：同期资产负债规模增长部分来自合并范围扩大（正常，需扣除后再判断）"}
def role_of(item):
    for p, role, cat in ITEM_ROLE:
        if item == p or item.startswith(p):
            return role, cat
    return "context", None
def _pct(a, b):
    return None if not b else 100.0 * (a - b) / abs(b)
def _get(D, item, period="latest"):
    return next((d for d in D if d["item"] == item and d.get("period") == period), None)
def causal(rows, flags, aging, events, narr, scale, restatement_reason):
    D = rows; drivers = []; normals = []; cons = []
    def add_driver(cat, indicator, strength, summary, evidence, period="latest", explained_by=None):
        if strength <= 0: return None
        k = {"id": f"k{len(drivers)+1:02d}", "category": cat, "category_cn": CAT_CN[cat], "indicator": indicator, "period": period,
             "strength": int(min(3, strength)), "summary": summary, "evidence": evidence}
        if explained_by: k["explained_by"] = explained_by
        drivers.append(k); return k
    # ---- normal events
    ev_by = {}
    for e in events: ev_by.setdefault(e["kind"], []).append(e)
    fy = max([e["fy"] for e in events], default=None)
    reason = (restatement_reason or {}).get("reason") or ""
    restated = [d for d in D if d.get("restated")]
    def add_normal(kind, fy_, evidence, explains, note=None):
        n = {"id": f"e{len(normals)+1:02d}", "kind": kind, "label_cn": NORMAL_CN[kind], "fy": fy_, "evidence": evidence, "explains": explains}
        if note: n["note"] = note
        normals.append(n); return n
    sc = [d["id"] for d in D if "same_control_merger" in str(d.get("restatement_class"))]
    if sc:
        ev = [{"fy": restatement_reason["fy"], "page": restatement_reason.get("reason_page") or restatement_reason["page"],
               "excerpt": restatement_reason.get("reason_excerpt") or restatement_reason["excerpt"]}] if restatement_reason else []
        cross = [d["id"] for d in D if d.get("basis") == "cross_report" and d.get("period") == "latest" and d["item"].startswith("对外担保")]
        add_normal("same_control_merger", restatement_reason and restatement_reason.get("fy"), ev, sc + cross,
                   note="重述数是合并后口径，本期 vs 上期（本报告口径）是同口径比较；跨报告比较（担保余额等）的上年数不含被合并方，口径不同，不能直接当增长")
    pb = [d["id"] for d in D if d.get("restatement_class") == "presentation_or_basis_change"]
    if pb:
        add_normal("presentation_or_basis_change", fy, [{"fy": d["current"]["fy"], "page": d["prior"]["page"], "excerpt": d["prior"].get("excerpt")} for d in D if d["id"] in pb[:3]],
                   pb, note="上年原报与本报告期初不同，但对应报表项目未重述")
    pc = [d["id"] for d in D if "accounting_policy_change" in str(d.get("restatement_class"))]
    pol = ev_by.get("policy_first_adoption", [])
    if pc or pol:
        ev = [{"fy": e["fy"], "page": e["page"], "excerpt": e["excerpt"]} for e in pol]
        if pc and restatement_reason: ev.insert(0, {"fy": restatement_reason["fy"], "page": restatement_reason.get("reason_page") or restatement_reason["page"], "excerpt": restatement_reason.get("reason_excerpt") or restatement_reason["excerpt"]})
        add_normal("accounting_policy_change", fy, ev, pc, note="首次执行新准则时期初数按新准则调整，部分附注期初与上年原报不同")
    acq_ids = {}
    for e in ev_by.get("acquisition", []):
        period = "latest" if e["fy"] == fy else "earlier"
        gw = _get(D, "商誉账面原值", period)
        grow = [d["id"] for d in D if d.get("period") == period and d["item"] in ("应收账款", "存货", "短期借款", "长期借款", "资产总计", "负债合计", "商誉账面原值", "商誉") and (d.get("delta") or 0) > 0]
        ev = [{"fy": e["fy"], "page": e["page"], "excerpt": e["excerpt"]}] + ([{"fy": e["fy"], "page": e["detail_page"], "excerpt": e["detail_excerpt"]}] if e.get("detail_excerpt") else [])
        ta_p = scale.get("total_assets") if period == "latest" else scale.get("total_assets_fy_prev_report")
        material = bool(gw and ta_p and gw.get("delta", 0) >= 0.005 * ta_p)
        n = add_normal("acquisition_scale_change", e["fy"], ev, grow if material else [],
                       note=(("同期商誉原值增加 %.2f 元（≥0.5%% 总资产），增长型驱动因素降一级" % gw["delta"]) if material else
                             "同期有非同一控制下企业合并，但商誉原值增加不足总资产 0.5%（或未能取得），不调整驱动因素"))
        if material: acq_ids[period] = n["id"]
    # ---- drivers
    ta = scale.get("total_assets") or 0
    for period in ("latest", "earlier"):
        ar = _get(D, "应收账款", period); rv = _get(D, "营业收入", period)
        if ar and rv and ar["prior"]["value"] and rv["prior"]["value"]:
            ga = _pct(ar["current"]["value"], ar["prior"]["value"]); gr = _pct(rv["current"]["value"], rv["prior"]["value"])
            gap = ga - gr; s = 3 if gap >= 30 else 2 if gap >= 15 else 1 if gap >= 5 else 0
            if s and ar["current"]["value"] < 0.02 * (ta or 1): s -= 1
            ex = acq_ids.get(period)
            if ex and s: s -= 1
            add_driver("collection", "应收账款增速 - 营业收入增速", s, f"应收账款 {ga:+.1f}% vs 营业收入 {gr:+.1f}%（差 {gap:+.1f} 个百分点）",
                       [ar["id"], rv["id"]], period, [ex] if ex else None)
        pv = _get(D, "应收账款坏账准备", period)
        if pv and pv["prior"]["value"]:
            g = _pct(pv["current"]["value"], pv["prior"]["value"]); rel = abs(pv["delta"]) / ta * 100 if ta else 0
            s = 3 if (g >= 50 and rel >= 0.5) else 2 if g >= 25 else 1 if g >= 10 else 0
            add_driver("collection", "应收账款坏账准备跳升", s, f"应收账款坏账准备 {g:+.1f}%（{pv['prior']['value']:,.0f} → {pv['current']['value']:,.0f} 元）", [pv["id"]], period)
    ag = sorted(aging, key=lambda a: a["fy"])
    if len(ag) >= 2:
        a0, a1 = ag[-2], ag[-1]; ch = 100 * (a1["share_gt1"] - a0["share_gt1"])
        s = 3 if ch >= 10 else 2 if ch >= 5 else 1 if ch >= 2 else 0
        if s and a1["share_gt1"] >= 0.5: s += 1
        dl = _get(D, "应收账款-账龄1年以上余额", "latest")
        add_driver("collection", "应收账款账龄结构恶化", s, f"账龄1年以上占比 {a0['share_gt1']*100:.1f}% → {a1['share_gt1']*100:.1f}%（2年以上 {a0['share_gt2']*100:.1f}% → {a1['share_gt2']*100:.1f}%）",
                   ([dl["id"]] if dl else []) + [f"aging:FY{a0['fy']}", f"aging:FY{a1['fy']}"])
    elif len(ag) == 1 and ag[0]["share_gt1"] >= 0.5:
        add_driver("collection", "应收账款账龄偏长", 2 if ag[0]["share_gt1"] >= 0.6 else 1, f"账龄1年以上占比 {ag[0]['share_gt1']*100:.1f}%（2年以上 {ag[0]['share_gt2']*100:.1f}%）", [f"aging:FY{ag[0]['fy']}"])
    pre = _get(D, "预付款项", "latest"); rv = _get(D, "营业收入", "latest")
    if pre and rv and pre["prior"]["value"] and rv["prior"]["value"]:
        gp = _pct(pre["current"]["value"], pre["prior"]["value"]); gr = _pct(rv["current"]["value"], rv["prior"]["value"])
        rel = abs(pre["delta"]) / ta * 100 if ta else 0
        s = 2 if (gp - gr >= 50 and rel >= 1) else 1 if (gp - gr >= 30 and rel >= 0.5) else 0
        add_driver("collection", "预付款项异常增长", s, f"预付款项 {gp:+.1f}% vs 营业收入 {gr:+.1f}%", [pre["id"]])
    # liquidity: unrestricted cash vs short-term debt (both columns of the latest report, and the earlier report)
    for period in ("latest", "earlier"):
        cash = _get(D, "货币资金", period); st = _get(D, "短期借款", period); cur = _get(D, "一年内到期的非流动负债", period); rs = _get(D, "受限货币资金", period)
        if not cash or not (st or cur): continue
        def cov(side):
            c = cash[side]["value"] - (rs[side]["value"] if rs else 0)
            debt = (st[side]["value"] if st else 0) + (cur[side]["value"] if cur else 0)
            return (c / debt) if debt > 0 else None, c, debt
        r1, c1, d1 = cov("current"); r0, c0, d0 = cov("prior")
        if r1 is None: continue
        s = 3 if r1 < 0.3 else 2 if r1 < 0.6 else 1 if r1 < 1.0 else 0
        if s and r0 and r1 < 0.8 * r0: s += 1
        add_driver("liquidity", "非受限货币资金 / (短期借款+一年内到期的非流动负债)", s,
                   f"覆盖率 {('%.2f' % r0) if r0 is not None else '-'} → {r1:.2f}（非受限现金 {c1:,.0f} 元，短期债务 {d1:,.0f} 元{'；已扣除受限资金' if rs else '；未能扣除受限资金'}）",
                   [x["id"] for x in (cash, st, cur, rs) if x], period)
        ex = acq_ids.get(period); g = _pct(d1, d0) if d0 else None
        if g is not None:
            s2 = 2 if (g >= 50 and (d1 - d0) >= 0.02 * (ta or 1)) else 1 if g >= 25 else 0
            if ex and s2: s2 -= 1
            add_driver("debt_growth", "短期债务增长", s2, f"短期借款+一年内到期的非流动负债 {g:+.1f}%", [x["id"] for x in (st, cur) if x], period, [ex] if ex else None)
    od = [f for f in flags if f.get("flag", "").startswith("已逾期")]
    for f in od:
        add_driver("overdue_default", "已逾期未偿还的借款", 3, f"FY{f['fy']} 已逾期未偿还的短期借款 {f.get('value', 0):,.0f} 元", [f"flag:{f['flag']}:FY{f['fy']}"])
    for it in narr:
        t = it.get("type"); q = it.get("quote") or ""
        if t == "guarantee_or_default" and any(w in q for w in ("逾期", "违约", "冻结", "查封", "未能按期", "未按期", "追偿")):
            add_driver("overdue_default", "逾期/违约/冻结的叙述披露", 3, (it.get("summary") or "")[:60], [f"narrative:{it['id']}"])
        elif t == "fund_occupation":
            add_driver("guarantee_related", "关联方资金占用", 3, (it.get("summary") or "")[:60], [f"narrative:{it['id']}"])
        elif t == "audit_opinion" and any(w in q for w in ("保留意见", "无法表示意见", "否定意见")) and "无保留" not in q:
            add_driver("audit_going_concern", "非标准审计意见", 3, (it.get("summary") or "")[:60], [f"narrative:{it['id']}"])
        elif t == "going_concern" or (t == "emphasis_paragraph" and "持续经营" in q):
            add_driver("audit_going_concern", "持续经营重大不确定性", 3, (it.get("summary") or "")[:60], [f"narrative:{it['id']}"])
        elif t == "emphasis_paragraph":
            add_driver("audit_going_concern", "审计报告强调事项", 2, (it.get("summary") or "")[:60], [f"narrative:{it['id']}"])
        elif t == "regulatory":
            add_driver("audit_going_concern", "监管调查/处罚/风险警示", 2, (it.get("summary") or "")[:60], [f"narrative:{it['id']}"])
        elif t == "auditor_change" and re.search(r"变更|更换|改聘|解聘", q + (it.get("summary") or "")) and not re.search(r"未改聘|续聘|未变更|未发生变更|不存在", q + (it.get("summary") or "")):
            add_driver("audit_going_concern", "更换会计师事务所", 1, (it.get("summary") or "")[:60], [f"narrative:{it['id']}"])
    ec = [d["id"] for d in D if "error_correction" in str(d.get("restatement_class"))]
    if ec:
        add_driver("audit_going_concern", "前期会计差错更正（重述）", 2, f"{len(ec)} 个项目因会计差错更正被重述", ec)
    gr = sorted([f for f in flags if f.get("flag") == "担保总额占净资产比例"], key=lambda f: f["fy"])
    if gr:
        g1 = gr[-1]; v = g1["value_pct"]; s = 3 if v >= 100 else 2 if v >= 50 else 1 if v >= 30 else 0
        if len(gr) >= 2 and v - gr[-2]["value_pct"] >= 20 and s: s += 1
        add_driver("guarantee_related", "担保总额占净资产比例", s, " → ".join(f"FY{f['fy']} {f['value_pct']}%" for f in gr), [f"flag:{f['flag']}:FY{f['fy']}" for f in gr])
    rp = _get(D, "应收关联方款项(已解析行合计)", "latest")
    if rp and ta and rp["current"]["value"] / ta >= 0.03 and rp["delta"] > 0:
        add_driver("guarantee_related", "应收关联方款项", 2 if rp["current"]["value"] / ta >= 0.08 else 1, f"应收关联方款项 {rp['prior']['value']:,.0f} → {rp['current']['value']:,.0f} 元", [rp["id"]])
    orc = _get(D, "其他应收款", "latest")
    if orc and ta and orc["prior"]["value"]:
        g = _pct(orc["current"]["value"], orc["prior"]["value"]); rel = orc["delta"] / ta * 100
        s = 2 if (g >= 50 and rel >= 2) else 1 if (g >= 30 and rel >= 1) else 0
        add_driver("guarantee_related", "其他应收款（往来/资金拆借）增长", s, f"其他应收款 {g:+.1f}%（占总资产变动 {rel:+.1f} 个百分点）", [orc["id"]])
    for period in ("latest",):
        cash = _get(D, "货币资金", period); rs = _get(D, "受限货币资金", period)
        if cash and rs and cash["current"]["value"]:
            sh = rs["current"]["value"] / cash["current"]["value"]; s = 3 if sh >= 0.5 else 2 if sh >= 0.3 else 1 if sh >= 0.15 else 0
            add_driver("restricted_cash", "受限资金占货币资金比例", s, f"受限 {rs['current']['value']:,.0f} / 货币资金 {cash['current']['value']:,.0f} 元 = {sh*100:.1f}%", [cash["id"], rs["id"]], period)
    # ---- consequences, each linked to the drivers that plausibly explain it
    dcat = {}
    for k in drivers: dcat.setdefault(k["category"], []).append(k)
    for d in D:
        role, cat = role_of(d["item"])
        if role != "consequence" or d.get("period") != "latest": continue
        bad = (d["delta"] < 0) if cat in ("loss", "equity") or d["item"] == "商誉" else (d["delta"] > 0)
        if not bad: continue
        links = [k["id"] for c in CONS_LINKS.get(cat, []) for k in sorted(dcat.get(c, []), key=lambda k: -k["strength"]) if k["strength"] >= 1][:4]
        why = []
        if cat == "goodwill" and "earlier" in acq_ids or (cat == "goodwill" and "latest" in acq_ids):
            why.append("前期/本期收购形成的商誉")
        cons.append({"id": f"q{len(cons)+1:02d}", "delta_id": d["id"], "item": d["item"], "kind": cat, "kind_cn": CONS_CN[cat],
                     "summary": f"{d['item']} {d['prior']['value']:,.0f} → {d['current']['value']:,.0f} 元", "linked_drivers": links,
                     "note": "后果项：通常是驱动因素（回款、流动性、担保等）恶化的结果，排序在驱动因素之后" + (("；" + "；".join(why)) if why else "")})
    # ---- per-delta causal labels and ordering
    expl = {}
    for n in normals:
        for i in n["explains"]: expl.setdefault(i, []).append(n["id"])
    dstr = {}
    for k in drivers:
        for e in k["evidence"]:
            dstr[e] = max(dstr.get(e, 0), k["strength"])
    order = {c: i for i, c in enumerate(DRIVER_ORDER)}
    out = []
    for d in D:
        role, cat = role_of(d["item"])
        r = dict(d, causal_role=role)
        if cat: r["causal_category"] = cat
        if d["id"] in expl: r["explained_by"] = expl[d["id"]]
        st = dstr.get(d["id"], 0)
        if role == "driver": r["driver_strength"] = st
        size = (100 * abs(d["delta"]) / ta) if ta else 0
        tier = 0 if (role == "driver" and st >= 2) else 1 if (role == "driver" and st == 1) else 2 if role == "consequence" else 3
        if d["id"] in expl and (role == "context" or d.get("basis") == "cross_report"): tier = 4   # explained-normal, not risk
        r["causal_tier"] = tier
        r["_key"] = (tier, -st, order.get(cat, 9) if role == "driver" else 9, -size, d["id"])
        out.append(r)
    out.sort(key=lambda r: r["_key"])
    for i, r in enumerate(out, 1):
        r["rank"] = i; del r["_key"]
    drivers.sort(key=lambda k: (-k["strength"], order.get(k["category"], 9), 0 if k["period"] == "latest" else 1))
    return out, drivers, cons, normals

def size_pct(d, scale):
    prev = d.get("period") == "earlier"
    s = (scale.get("revenue_fy_prev_report") if prev else scale.get("revenue")) if d.get("scale_kind") == "revenue" else \
        (scale.get("total_assets_fy_prev_report") if prev else scale.get("total_assets"))
    return round(100 * abs(d["delta"]) / s, 4) if s and s > 0 else None

def import_pack(numeric_path, narrative_path, sources_dir, out):
    out = Path(out); need(not out.exists(), "output exists (packages are immutable)")
    N = json.loads(Path(numeric_path).read_text(encoding="utf-8"))
    R = json.loads(Path(narrative_path).read_text(encoding="utf-8")) if narrative_path else {"items": []}
    pages = load_pages(sources_dir); need(pages, "no FY*.pages.jsonl source files")
    need(isinstance(N.get("deltas"), list), "deltas list required")
    scale = N.get("scale") or {}
    checks = N.get("checks") or []
    ids = set()
    for c in checks:
        need(isinstance(c.get("id"), str) and isinstance(c.get("ok"), bool), "check needs id and ok")
        need(c["id"] not in ids, "duplicate check id"); ids.add(c["id"])
    cb = {c["id"]: c for c in checks}
    seen = set(); rows = []
    for d in N["deltas"]:
        need(isinstance(d.get("id"), str) and d["id"] not in seen, "delta id missing/duplicate"); seen.add(d["id"])
        need(d.get("unit"), f"{d['id']}: unit required")
        need(d.get("scale_kind") in ("assets", "revenue"), f"{d['id']}: scale_kind must be assets|revenue")
        _point_ok(d.get("current"), pages, d["id"] + ".current"); _point_ok(d.get("prior"), pages, d["id"] + ".prior")
        if d.get("prior_as_originally_reported"): _point_ok(d["prior_as_originally_reported"], pages, d["id"] + ".prior_as_originally_reported")
        want = round(d["current"]["value"] - d["prior"]["value"], 2)
        need(abs(want - d["delta"]) <= 0.01, f"{d['id']}: delta != current - prior")
        for c in d.get("check_ids", []): need(c in cb, f"{d['id']}: unknown check {c}")
        need(d.get("restatement_class") in RESTATE_CLASS_OK, f"{d['id']}: unknown restatement_class")
        need(not (d.get("restatement_class") == "presentation_or_basis_change" and d.get("restated")), f"{d['id']}: basis change cannot be restated")
        failed = [c for c in d.get("check_ids", []) if not cb[c]["ok"]]
        rows.append(dict(d, size_pct_of_scale=size_pct(d, scale), failed_check_ids=failed))
    flags = []
    for f in N.get("flags") or []:
        need(f.get("fy") in pages and f.get("page") in pages[f["fy"]], "flag page not in sources")
        if f.get("excerpt"): need(f["excerpt"] in pages[f["fy"]][f["page"]], "flag excerpt not verbatim")
        flags.append(f)
    aging = []
    for a in N.get("aging") or []:
        _verbatim(a.get("fy"), a.get("page"), a.get("excerpt"), pages, f"aging FY{a.get('fy')}")
        need(all(_num(a.get(k)) for k in ("le1", "y1_2", "y2_3", "gt3", "total", "share_gt1", "share_gt2")), "aging: numbers required")
        need(abs(a["le1"] + a["y1_2"] + a["y2_3"] + a["gt3"] - a["total"]) <= 0.006 * abs(a["total"]) + 1, "aging: buckets must sum to total")
        aging.append(a)
    events = []
    for e in N.get("events") or []:
        _verbatim(e.get("fy"), e.get("page"), e.get("excerpt"), pages, f"event {e.get('kind')}")
        if e.get("reason_excerpt"): _verbatim(e["fy"], e.get("reason_page"), e["reason_excerpt"], pages, "event reason")
        if e.get("detail_excerpt"): _verbatim(e["fy"], e.get("detail_page"), e["detail_excerpt"], pages, "event detail")
        events.append(e)
    rr = N.get("restatement_reason")
    if rr:
        _verbatim(rr.get("fy"), rr.get("page"), rr.get("excerpt"), pages, "restatement_reason")
        if rr.get("reason_excerpt"): _verbatim(rr["fy"], rr.get("reason_page"), rr["reason_excerpt"], pages, "restatement_reason.reason")
    narr = []
    for it in R.get("items") or []:
        need(it.get("fy") in pages and it.get("page") in pages[it["fy"]], f"narrative {it.get('id')}: page not in sources")
        need(it.get("quote") and it["quote"] in pages[it["fy"]][it["page"]], f"narrative {it.get('id')}: quote not verbatim")
        narr.append(it)
    ranked, drivers, cons, normals = causal(rows, flags, aging, events, narr, scale, rr)
    for n in normals:
        for e in n["evidence"]:
            if e.get("excerpt"): _verbatim(e["fy"], e["page"], e["excerpt"], pages, f"normal {n['id']}")
    pack = {"schema": NUMERIC_SCHEMA, "company": N.get("company"), "fy": N.get("fy"), "fy_prev": N.get("fy_prev"), "unit": N.get("unit", "元"),
            "scale": scale, "deltas": ranked, "drivers": drivers, "consequences": cons, "normal_events": normals,
            "restatements": N.get("restatements") or [], "basis_changes": N.get("basis_changes") or [], "restatement_reason": rr,
            "checks": checks, "flags": flags, "aging": aging, "events": events, "narrative": narr}
    out.mkdir(parents=True)
    shutil.copytree(sources_dir, out / "sources")
    body = json.dumps(pack, ensure_ascii=False, indent=1, allow_nan=False)
    (out / "numeric.json").write_text(body + "\n", encoding="utf-8")
    man = {"numeric_sha256": hashlib.sha256((body + "\n").encode()).hexdigest(),
           "sources": {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((out / "sources").glob("*"))}}
    (out / "numeric-manifest.json").write_text(json.dumps(man, indent=1) + "\n", encoding="utf-8")
    return {"status": "imported", "deltas": len(ranked), "drivers": len(drivers), "consequences": len(cons), "normal_events": len(normals),
            "checks": len(checks), "failed_checks": sum(1 for c in checks if not c["ok"]), "restatements": len(pack["restatements"]),
            "basis_changes": len(pack["basis_changes"]), "flags": len(flags), "narrative": len(narr)}

def load(pkg):
    pkg = Path(pkg); body = (pkg / "numeric.json").read_text(encoding="utf-8")
    man = json.loads((pkg / "numeric-manifest.json").read_text(encoding="utf-8"))
    need(hashlib.sha256(body.encode()).hexdigest() == man["numeric_sha256"], "numeric.json hash mismatch")
    return json.loads(body)

ROLE_CN = {"driver": "驱动因素", "consequence": "后果", "context": "背景"}
def _brief(d, excerpt=True):
    keep = ["rank", "id", "item", "causal_role", "causal_category", "driver_strength", "explained_by", "period", "unit", "delta", "delta_pct", "basis",
            "restated", "restatement_class", "restatement_subclass", "restatement_diff", "size_pct_of_scale", "failed_check_ids", "note"]
    o = {k: d[k] for k in keep if k in d and d[k] not in (None, [])}
    for side in ("current", "prior", "prior_as_originally_reported"):
        if d.get(side):
            p = d[side]; o[side] = {k: p[k] for k in ("report", "column", "value", "page", "table_id") if k in p}
            if excerpt and p.get("excerpt"): o[side]["excerpt"] = p["excerpt"]
    return o

def _resolve(P, ev):
    """expand evidence references of a driver into verbatim points"""
    D = {d["id"]: d for d in P["deltas"]}; N = {n["id"]: n for n in P["narrative"]}; out = []
    for e in ev:
        if e in D:
            d = D[e]; out.append({"delta_id": e, "item": d["item"], "current": {k: d["current"].get(k) for k in ("report", "value", "page", "excerpt")},
                                  "prior": {k: d["prior"].get(k) for k in ("report", "value", "page", "excerpt")}})
        elif e.startswith("narrative:") and e[10:] in N:
            n = N[e[10:]]; out.append({"narrative_id": n["id"], "report": n["report"], "page": n["page"], "quote": n["quote"]})
        elif e.startswith("aging:FY"):
            a = next((a for a in P["aging"] if a["fy"] == int(e[8:])), None)
            if a: out.append({"aging": f"FY{a['fy']}", "report": a["report"], "page": a["page"], "excerpt": a["excerpt"], "share_gt1": a["share_gt1"], "share_gt2": a["share_gt2"]})
        elif e.startswith("flag:"):
            f = next((f for f in P["flags"] if f"flag:{f['flag']}:FY{f['fy']}" == e), None)
            if f: out.append({"flag": f["flag"], "fy": f["fy"], "page": f["page"], "excerpt": f.get("excerpt"), "value": f.get("value", f.get("value_pct"))})
    return out

def view(pkg, kind="overview", period="all", item=None, offset=0, limit=15, failed_only=False, ntype=None, excerpt=True, role=None, category=None):
    P = load(pkg)
    if kind == "summary": kind = "overview"
    need(kind in ("overview", "drivers", "consequences", "normal", "deltas", "restatements", "checks", "narrative"), "unknown view")
    need(isinstance(offset, int) and offset >= 0 and isinstance(limit, int) and 1 <= limit <= 50, "bad offset/limit")
    if kind == "overview":
        cnt = {}
        for it in P["narrative"]: cnt[it.get("type")] = cnt.get(it.get("type"), 0) + 1
        return {"company": P["company"], "fy": P["fy"], "fy_prev": P["fy_prev"], "unit": P["unit"], "scale": P["scale"],
                "ordering_rule": "驱动因素在前（逾期/违约、审计与持续经营、现金对短债覆盖、回款恶化、担保与关联方资金、受限资金、短债增长），"
                                 "后果在后（亏损、减值、商誉减记、净资产下降，均链接到可能的驱动因素），已解释的正常事项最后",
                "drivers_top": [{k: x[k] for k in ("id", "category_cn", "indicator", "period", "strength", "summary") if k in x} | ({"explained_by": x["explained_by"]} if x.get("explained_by") else {}) for x in P["drivers"][:10]],
                "consequences": [{k: x[k] for k in ("id", "kind_cn", "summary", "linked_drivers")} for x in P["consequences"]],
                "normal_events": [{k: x[k] for k in ("id", "kind", "label_cn", "fy")} | {"explains_n": len(x["explains"])} for x in P["normal_events"]],
                "counts": {"deltas": len(P["deltas"]), "drivers": len(P["drivers"]), "restatements": len(P["restatements"]), "basis_changes": len(P["basis_changes"]),
                           "failed_checks": sum(1 for c in P["checks"] if not c["ok"]), "narrative_by_type": cnt},
                "flags": P["flags"]}
    if kind == "drivers":
        rows = [x for x in P["drivers"] if not category or x["category"] == category or x["category_cn"] == category]
        return {"total": len(rows), "drivers": [dict(x, evidence=_resolve(P, x["evidence"])) for x in rows[offset:offset + limit]],
                "next_offset": offset + limit if offset + limit < len(rows) else None}
    if kind == "consequences":
        K = {k["id"]: k for k in P["drivers"]}; D = {d["id"]: d for d in P["deltas"]}
        return {"consequences": [dict(x, evidence=_resolve(P, [x["delta_id"]]), linked=[{k: K[i][k] for k in ("id", "category_cn", "indicator", "strength", "summary")} for i in x["linked_drivers"] if i in K]) for x in P["consequences"]]}
    if kind == "normal":
        D = {d["id"]: d for d in P["deltas"]}
        return {"normal_events": [dict(x, explains=[{"delta_id": i, "item": D[i]["item"], "period": D[i]["period"]} for i in x["explains"] if i in D]) for x in P["normal_events"]],
                "basis_changes": P["basis_changes"]}
    if kind == "deltas":
        rows = [d for d in P["deltas"] if period == "all" or d.get("period") == period]
        if item: rows = [d for d in rows if item in d["item"]]
        if role: rows = [d for d in rows if d.get("causal_role") == role]
        return {"total": len(rows), "offset": offset, "deltas": [_brief(d, excerpt) for d in rows[offset:offset + limit]],
                "next_offset": offset + limit if offset + limit < len(rows) else None}
    if kind == "restatements":
        return {"restatement_reason": P["restatement_reason"], "restatements": P["restatements"], "basis_changes_not_restatements": P["basis_changes"]}
    if kind == "checks":
        rows = [c for c in P["checks"] if not failed_only or not c["ok"]]
        return {"total": len(rows), "checks": rows[offset:offset + limit], "next_offset": offset + limit if offset + limit < len(rows) else None}
    rows = [it for it in P["narrative"] if not ntype or it.get("type") == ntype]
    return {"total": len(rows), "items": rows[offset:offset + limit], "next_offset": offset + limit if offset + limit < len(rows) else None}
