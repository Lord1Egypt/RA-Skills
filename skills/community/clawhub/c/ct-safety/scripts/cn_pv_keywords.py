#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nmpa_pv_keywords.py / 中国药物警戒通报检索关键词构造（轻本地端）

WHY THIS EXISTS
──────────────
ct-base §20.14 架构下，nmpa_pv 的「词表扩展」留本地（drug_name_map.json +
事件同义词组），「抓取执行器」上 Coze 统一端点。本模块是本地侧的关键词
构造器：把用户输入的 drug/event 扩展为扁平关键词列表，供 coze_dispatch
外发至 Coze nmpa_pv 节点。

职责边界
────────
  - 做：药名双向扩展（zh↔en）、事件同义词展开、查询指纹生成
  - 不做：任何网络请求、HTML 解析、翻页、正文抓取（全部上 Coze）

词表来源（单一真源）
──────────────────
  - 药名：references/drug_name_map.json（publish_inject 注入副本）
  - 事件同义词：本模块内嵌（EVENT_SYNONYMS，与旧版 fetch_cn_pv 一致）
"""

import hashlib
import json
import os
import re
import sys

# ── 词表路径 ──────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(_HERE := __file__))
# 兼容直接运行和作为模块导入
if os.path.basename(_HERE) == "scripts":
    _SKILL_ROOT = os.path.dirname(_HERE)
else:
    _SKILL_ROOT = _HERE

_NAME_MAP_PATH = os.path.join(_SKILL_ROOT, "references", "drug_name_map.json")

# 事件同义词组（命中任一同义词即视为该事件命中；snippet 关键词取实际命中的词）
# 与旧版 fetch_cn_pv.EVENT_SYNONYMS 保持完全一致，确保行为连续
EVENT_SYNONYMS = {
    "肺炎": ["肺炎", "间质性肺炎", "间质性肺病", "肺毒性", "ILD"],
    "肝损伤": ["肝损伤", "肝功能异常", "药物性肝损伤", "肝毒性", "DILI", "转氨酶升高"],
    "肾损伤": ["肾损伤", "肾功能异常", "肾毒性", "急性肾损伤"],
    "心脏毒性": ["心脏毒性", "心力衰竭", "心肌损伤", "心律失常", "QT延长"],
    "皮肤反应": ["皮疹", "皮肤反应", "Stevens-Johnson", "中毒性表皮坏死", "SJS", "TEN"],
    "过敏反应": ["过敏反应", "超敏反应", "过敏性休克"],
    "骨髓抑制": ["骨髓抑制", "中性粒细胞减少", "白细胞减少", "血小板减少", "贫血"],
    "胃肠道反应": ["胃肠道反应", "腹泻", "恶心", "呕吐", "消化道出血"],
    "神经毒性": ["神经毒性", "周围神经病变", "神经病变"],
    "血栓": ["血栓", "静脉血栓", "肺栓塞", "血栓栓塞"],
    "输液反应": ["输液反应", "输注相关反应", "注射部位反应"],
    "免疫相关不良反应": ["免疫相关不良反应", "irAE", "免疫不良反应"],
}


def _load_name_map():
    """加载 drug_name_map.json -> {zh2en: {zh: [en...]}, en2zh: {en_lower: [zh...]}} 双向索引。"""
    idx = {"zh2en": {}, "en2zh": {}}
    try:
        with open(_NAME_MAP_PATH, encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        return idx
    for zh, ens in raw.items():
        if zh.startswith("_") or not isinstance(ens, list):
            continue
        idx["zh2en"][zh] = [e for e in ens if isinstance(e, str)]
        for e in ens:
            if isinstance(e, str):
                idx["en2zh"].setdefault(e.lower(), []).append(zh)
    return idx


def expand_drug_keywords(drug, drug_en=None, name_map=None):
    """把用户输入的药名扩展为关键词组：用户原词 + 词表反向/正向候选。

    drug 可为逗号分隔多别名（如 "奥希替尼,osimertinib,泰瑞沙"）。
    返回 list[str]，去重保序。
    """
    kws = []
    for part in (drug or "").split(","):
        p = part.strip()
        if p:
            kws.append(p)
    if drug_en and drug_en.strip():
        kws.append(drug_en.strip())
    if name_map is None:
        name_map = _load_name_map()
    for k in list(kws):
        low = k.lower()
        for cand in name_map["zh2en"].get(k, []) + name_map["en2zh"].get(low, []):
            if cand and cand not in kws:
                kws.append(cand)
    return kws


def expand_event_keywords(event):
    """事件词 -> [原词] + 同义词组命中词（组内任一原词出现即整组生效）。

    返回 list[str]，去重保序。
    """
    if not event or not event.strip():
        return []
    e = event.strip()
    out = [e]
    for keys, syns in EVENT_SYNONYMS.items():
        if e == keys or e in syns:
            for s in syns:
                if s.strip() and s not in out:
                    out.append(s.strip())
            break
    return [x for x in out if x]


def build_nmpa_pv_query(drug_zh, drug_en=None, event=None, terms=None,
                       max_per=10, since=None, until=None):
    """构造 nmpa_pv Coze 节点查询 payload（不含 source/mode，由 dispatch 注入）。

    返回 dict，可直接传入 coze_dispatch.dispatch("nmpa_pv", **query)。
    """
    drug_kw = expand_drug_keywords(drug_zh, drug_en)
    event_kw = expand_event_keywords(event)
    extra = [t.strip() for t in (terms or []) if t and t.strip()]

    return {
        "drug_kws": drug_kw,
        "event_kws": event_kw,
        "extra": extra,
        "max_per": max_per,
        "since": since,
        "until": until,
    }


def query_fingerprint(query):
    """生成查询指纹（sha1 前 16 位），用于缓存 key。"""
    return hashlib.sha1(json.dumps(query, sort_keys=True,
                                   ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


# ── CLI 快速验证 ──────────────────────────────────────────────────────────
def main():
    import argparse
    ap = argparse.ArgumentParser(description="NMPA-PV 关键词构造器（调试用）")
    ap.add_argument("--drug", required=True, help="药物名（中文/英文，逗号分隔别名）")
    ap.add_argument("--drug-en", help="药物英文名")
    ap.add_argument("--event", help="事件关键词")
    ap.add_argument("--terms", nargs="*", help="额外 AND 关键词")
    ap.add_argument("--max-per", type=int, default=10)
    ap.add_argument("--since", help="日期窗起点")
    ap.add_argument("--until", help="日期窗终点")
    args = ap.parse_args()

    q = build_nmpa_pv_query(args.drug, args.drug_en, args.event, args.terms,
                           args.max_per, args.since, args.until)
    print(json.dumps(q, ensure_ascii=False, indent=2))
    print("\n--- fingerprint: %s ---" % query_fingerprint(q))


if __name__ == "__main__":
    main()
