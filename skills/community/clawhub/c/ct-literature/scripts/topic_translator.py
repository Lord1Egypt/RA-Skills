#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
topic_translator.py — 检索词 中文→英文 翻译（本地词典聚合 + 联网兜底）

词典来源（全部为 ct- 库共享件 / 本地文件，按优先级合并）：
  1. references/term_map.json         中文医学通用术语 → 英文（~240 条，ct-base 真源同步）
  2. references/drug_name_map.json    中文药物名 → 英文 INN/通用名 列表（~470 条）
  3. scripts/kw_lexicon.json          ct-base 共享关键字体系：
       extra        中文 → 英文（高血压→hypertension 等 ~47）
       synonyms     中英同义词对（[非小细胞肺癌, non-small cell lung cancer] 等）
       brand_generic 商品名↔通用名全链（[泰瑞沙, Tagrisso, osimertinib, 奥希替尼]）
       class_alias  中文类别别名 → 英文类（dpp-4抑制剂 → gliptin）
       drug_en2zh   英文药 → 中文（翻转后并入）
  4. references/mesh_terms_mapping.json  MeSH 主题词 entry_terms（英文同义词表，用于翻译后 OR 扩展）
  5. references/user_terms.json        用户自定义词典（可选，gitignored；{zh: "en" | ["en1","en2"]}，
       覆盖内置同名条目——未收录词的用户出口）

策略：
  - 贪心最长匹配（长词优先，避免"肺癌"吃掉"非小细胞肺癌"）
  - 命中条目的多个英文同义词 → query 生成 `(main OR syn1 OR syn2)`（OpenAlex / Europe PMC 均支持布尔 OR）
  - 通用术语（term_map / extra）命中后，若 MeSH entry_terms 有等价同义词 → 追加 OR 扩展（最多 2 个）
  - 未命中的中文片段：调用 ct-base `kw_localize.localize_with_fallback()` 联网兜底
    （MyMemory 公开端点，无密钥；CT_TRANSLATE_ONLINE=0 或 --no-online-translate 关闭）
  - 兜底也失败的片段保留原样，untranslated 记录（配合运行时 partial 提示）

输出 dict：
  topic_zh / topic_en / translated / hits[(zh, en_primary), ...] /
  untranslated[中文残留] / sources[命中的词典来源（含 "online"）]

用法：
  from topic_translator import translate_topic
  info = translate_topic("奥希替尼 间质性肺病")
"""

import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REF = os.path.join(_HERE, "..", "references")
_HAN = re.compile(r"[\u4e00-\u9fff]+")

_CACHE = None

# 联网翻译开关（默认开，与 ct-base 同口径；CT_TRANSLATE_ONLINE=0 关闭）
_CT_TRANSLATE_ONLINE = os.environ.get("CT_TRANSLATE_ONLINE", "1").strip().lower() \
    not in ("0", "false", "no", "off")


def _import_kw_localize():
    """懒加载 ct-base 的 kw_localize 模块，找不到时返回 None（联网兜底不可用）。"""
    # 尝试从 workspace 目录导入（发布包 / 开发环境通用）
    candidate_dirs = []
    # 同级目录（开发环境：skills/ct-base/scripts/）
    candidate_dirs.append(os.path.join(_HERE, "..", "ct-base", "scripts"))
    # 上级目录（备选）
    candidate_dirs.append(os.path.join(_HERE, "..", "..", "ct-base", "scripts"))
    for d in candidate_dirs:
        if os.path.isfile(os.path.join(d, "kw_localize.py")):
            if d not in sys.path:
                sys.path.insert(0, d)
            try:
                import importlib
                return importlib.import_module("kw_localize")
            except Exception:
                pass
    return None


def _online_translate_fragment(zh_text):
    """对单个中文片段调用联网兜底翻译。返回 (en_text, source) 或 (None, None)。"""
    if not _CT_TRANSLATE_ONLINE or not zh_text:
        return None, None
    kw = _import_kw_localize()
    if kw is None:
        return None, None
    try:
        # kw_localize 只做术语级匹配；整句兜底用 localize_with_fallback（含 MyMemory 端点）
        en, source = kw.localize_with_fallback(zh_text, "en")
        if source in ("online", "term_map") and en and not _HAN.search(en):
            return en, source
        # source == "miss" 或仍含中文 → 兜底也失败
        return None, None
    except Exception:
        return None, None


def _load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _zh_keys(data):
    """过滤出含中文的 key（term_map/kw_lexicon 等混合方向时只取中文 key）。"""
    out = {}
    if not isinstance(data, dict):
        return out
    for k, v in data.items():
        if k == "_meta" or not isinstance(k, str) or not _HAN.search(k):
            continue
        out[k] = v
    return out


def _merge_entry(mapping, zh, en_main, en_syns=(), source=""):
    """合并中→英条目：已有则并集同义词，主名取 INN/首个。"""
    en_syns = [s for s in en_syns if s and s != en_main]
    cur = mapping.get(zh)
    if cur is None:
        mapping[zh] = {"main": en_main, "syns": en_syns, "sources": [source] if source else []}
    else:
        if en_main not in (cur["main"],) + tuple(cur["syns"]):
            cur["syns"].append(en_main)
        for s in en_syns:
            if s not in (cur["main"],) + tuple(cur["syns"]):
                cur["syns"].append(s)
        if source and source not in cur["sources"]:
            cur["sources"].append(source)


def load_dict():
    """聚合所有词典源（懒加载 + 缓存）。返回 {"zh2en": {...}, "mesh": {...}}。"""
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    zh2en = {}

    # 1) term_map.json（中文key → 英文str）
    tm = _load_json(os.path.join(_REF, "term_map.json"))
    for zh, en in _zh_keys(tm).items():
        if isinstance(en, str):
            _merge_entry(zh2en, zh, en.strip(), (), "term_map")

    # 2) drug_name_map.json（中文key → [英文...]）
    dm = _load_json(os.path.join(_REF, "drug_name_map.json"))
    for zh, ens in _zh_keys(dm).items():
        if isinstance(ens, list) and ens:
            _merge_entry(zh2en, zh, str(ens[0]).strip(), [str(x).strip() for x in ens[1:] if x], "drug_name_map")

    # 3) kw_lexicon.json（同目录共享件）
    kw = _load_json(os.path.join(_HERE, "kw_lexicon.json"))
    if isinstance(kw, dict):
        for zh, en in _zh_keys(kw.get("extra") or {}).items():
            if isinstance(en, str):
                _merge_entry(zh2en, zh, en.strip(), (), "kw_lexicon.extra")
        # synonyms: [[a, b], ...] —— 第一个元素含中文才收
        for pair in (kw.get("synonyms") or []):
            if isinstance(pair, list) and len(pair) >= 2 and _HAN.search(str(pair[0])):
                _merge_entry(zh2en, str(pair[0]), str(pair[1]).strip(), (), "kw_lexicon.synonyms")
        # brand_generic: [[中文名..., 英文名...], ...] —— 中文元素 → 英文元素（OR 扩展）
        for chain in (kw.get("brand_generic") or []):
            if not isinstance(chain, list):
                continue
            ens = [str(x).strip() for x in chain if x and not _HAN.search(str(x))]
            zhs = [str(x).strip() for x in chain if x and _HAN.search(str(x))]
            if ens and zhs:
                for zh in zhs:
                    _merge_entry(zh2en, zh, ens[0], ens[1:], "kw_lexicon.brand_generic")
        # class_alias: {zh: en}
        for zh, en in _zh_keys(kw.get("class_alias") or {}).items():
            if isinstance(en, str):
                _merge_entry(zh2en, zh, en.strip(), (), "kw_lexicon.class_alias")
        # drug_en2zh: {en: zh} → 翻转 {zh: en}
        for en, zh in (kw.get("drug_en2zh") or {}).items():
            if isinstance(en, str) and isinstance(zh, str) and _HAN.search(zh):
                _merge_entry(zh2en, zh, en.strip(), (), "kw_lexicon.drug_en2zh")

    # 4) user_terms.json（用户自定义，覆盖优先——后加载覆盖同 key 的 main/syns）
    ut = _load_json(os.path.join(_REF, "user_terms.json"))
    for zh, val in _zh_keys(ut).items():
        if isinstance(val, list) and val:
            _merge_entry(zh2en, zh, str(val[0]).strip(), [str(x).strip() for x in val[1:] if x], "user_terms")
        elif isinstance(val, str):
            _merge_entry(zh2en, zh, val.strip(), (), "user_terms")

    # 5) MeSH entry_terms 同义词表（英文侧 OR 扩展用）
    mesh = {}
    mm = _load_json(os.path.join(_REF, "mesh_terms_mapping.json"))
    if isinstance(mm, dict):
        for tname, tinfo in (mm.get("terms") or {}).items():
            ents = [str(tname)] + [str(x) for x in (tinfo.get("entry_terms") or []) if x]
            ents = list(dict.fromkeys(ents))  # 去重保序
            for e in ents:
                mesh.setdefault(e.lower(), ents)

    _CACHE = {"zh2en": zh2en, "mesh": mesh}
    return _CACHE


def _mesh_syns(mesh, en, limit=2):
    """MeSH entry_terms 等价同义词（排除自身，限 2 个）。"""
    group = mesh.get((en or "").lower())
    if not group:
        return []
    others = [e for e in group if e.lower() != (en or "").lower()]
    return list(dict.fromkeys(others))[:limit]


def translate_topic(topic, mesh_expand=True, online_fallback=True):
    """翻译检索词。返回 dict；无中文字符 → 原样返回 translated=False。

    策略：
      1. 本地词典贪心匹配（长词优先）
      2. 残留未译片段：联网兜底（ct-base kw_localize，可关闭）
    """
    topic = (topic or "").strip()
    if not _HAN.search(topic):
        return {"topic_zh": topic, "topic_en": topic, "translated": False,
                "hits": [], "untranslated": [], "sources": []}

    data = load_dict()
    zh2en, mesh = data["zh2en"], data["mesh"]
    keys = sorted(zh2en, key=len, reverse=True)
    hits = []
    hit_sources = []

    def _repl(m):
        zh = m.group(0)
        info = zh2en[zh]
        parts = [info["main"]] + [s for s in info["syns"] if s != info["main"]]
        if mesh_expand and len(parts) == 1:  # 通用术语 → MeSH 等价同义词 OR 扩展
            parts += [s for s in _mesh_syns(mesh, info["main"]) if s != info["main"]]
        parts = list(dict.fromkeys(parts))[:4]  # 上限 4 个（主名 + ≤3 同义）
        hits.append((zh, info["main"]))
        for s in info["sources"]:
            if s not in hit_sources:
                hit_sources.append(s)
        if len(parts) > 1:
            return "(" + " OR ".join(parts) + ")"
        return parts[0]

    if keys:
        pattern = re.compile("|".join(re.escape(k) for k in keys))
        query = pattern.sub(_repl, topic)
    else:
        query = topic

    # 2) 联网兜底：对残留的未翻译片段调用 ct-base kw_localize
    untranslated = []
    if online_fallback and _HAN.search(query):
        def _repl_online(m):
            zh = m.group(0)
            en, src = _online_translate_fragment(zh)
            if en:
                hits.append((zh, en))
                if src and src not in hit_sources:
                    hit_sources.append(src)
                return en
            # 兜底也失败 → 保留原样
            untranslated.append(zh)
            return zh
        query = re.sub(r"[\u4e00-\u9fff]+", _repl_online, query)
    else:
        untranslated = sorted(set(_HAN.findall(query)))

    return {"topic_zh": topic, "topic_en": query, "translated": True,
            "hits": hits, "untranslated": untranslated, "sources": hit_sources}


def gate_records(info):
    """translate_topic 结果 → 翻译确认门契约记录数组（ct-base bilingual_retrieval §5.2）。

    目标源是国际英文库（OpenAlex / Europe PMC / PubMed…），中文残留原文直发属
    真实漏检风险 → fail_open 不豁免（untranslated_risk 缺省=true，阻断询问）。
    词典/联网命中的词按 whole 记录；命中条目多同义词走 OR 扩展（布尔 OR 非
    AND），不构成歧义 → ambiguous 恒 false。info.translated=False（纯英文输入）
    返回空列表——无翻译发生即无门。
    """
    if not info or not info.get("translated"):
        return []
    recs = []
    for zh, en in (info.get("hits") or []):
        recs.append({"original": zh, "localized": en, "candidates": [en],
                     "mode": "whole", "ambiguous": False, "source": "literature"})
    for zh in (info.get("untranslated") or []):
        recs.append({"original": zh, "localized": zh, "candidates": [],
                     "mode": "fail_open", "ambiguous": False, "source": "literature"})
    return recs


if __name__ == "__main__":
    import sys
    # 解析 --no-online-translate（与 ct-base 同口径）
    args = sys.argv[1:]
    if "--no-online-translate" in args:
        _CT_TRANSLATE_ONLINE = False
        args.remove("--no-online-translate")
    for t in args or ["奥希替尼 间质性肺病", "泰瑞沙 肺癌 一线治疗",
                       "肺癌 免疫治疗 不良反应", "osimertinib interstitial lung disease"]:
        r = translate_topic(t)
        print("IN :", r["topic_zh"])
        print("OUT:", r["topic_en"], "| translated:", r["translated"])
        print("HITS:", r["hits"])
        print("SRC :", r["sources"])
        if r["untranslated"]:
            print("UNTRANSLATED:", r["untranslated"])
        print("-" * 50)
