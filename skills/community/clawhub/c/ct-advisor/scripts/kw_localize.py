#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# §16.9 exempt — keyword localization calls the translation API and must stay local
# (infra-shared exemption per §16.9); not a retrieval/website call subject to adapters/.
"""
kw_localize.py -- search-keyword language localization for the ct- clinical-trial
library (shared standard; lives in ct-base/scripts and is consumed by ct-registry,
ct-literature, ct-safety, and any other ct- skill that needs keyword search).

Problem it solves
-----------------
When a user types ONE search keyword (e.g. --cond "非小细胞肺癌"), a ct- skill
fans it out to multiple sources that expect DIFFERENT languages:
  - Foreign registries (CT.gov, EU CTR, ISRCTN, DRKS) expect ENGLISH.
  - Domestic China sources (CDE, ChiCTR) expect CHINESE (and also accept ENGLISH).

This module auto-switches the keyword to the target source's language so the
user never has to supply --cond AND --cde-keyword separately.

Two-phase resolution policy (ct-registry optimization 2026-07-24)
------------------------------------------------------------------
1. TERMINOLOGY FIRST: every switch first consults the curated bilingual term
   map (references/term_map.json, ~190 entries). A hit -> trusted translation.
2. CONFIRM-ON-MISS: if a keyword is NOT in the map, we do NOT silently keep the
   original text for a FOREIGN source (that would silently miss hits). Instead
   the caller raises a confirmation gate: it prints a *suggested* translation
   (from a fallback `_EXTRA` dict or the agent's own knowledge) and STOPS until
   the user confirms the translation (via --confirm-* or by rewriting the arg).
   Domestic CDE is bilingual-friendly, so an unmatched keyword there is logged
   but still searched (and bilingual mode also tries the other language).

Design constraints (ct- library philosophy)
-------------------------------------------
- Local-first, offline by default. The curated lexicon is authoritative; an
  online translation API is used ONLY as a last-resort fallback when the
  lexicon misses (`online_translate()`, keyless public endpoint, keeps
  zero-secret egress; disable via env `CT_TRANSLATE_ONLINE=0` or CLI
  `--no-online-translate`). `_EXTRA` (externalized in kw_lexicon.json) is a
  small curated safety net only. (2026-08-25: policy relaxed from
  "no live translation API" to "local-first, online fallback on miss" — see
  ct-base references/keyword_expand.md.)
- Deterministic and auditable: every switch / miss is logged by the caller.

Public API
----------
  detect_lang(text) -> "zh" | "en"
  localize(text, target_lang) -> (result, source)
      source in {"empty","same","term_map","miss"}
        empty    : text is None/""            -> result = text
        same     : text already in target_lang -> result = text (no change)
        term_map : translated via the curated map -> result = translation
        miss     : not in map, opposite language -> result = original (CALLER
                   should trigger the confirm gate)
  online_translate(text, target_lang) -> str | None
      Last-resort keyless online translation (Google gtx endpoint); None on
      any failure / when disabled (env CT_TRANSLATE_ONLINE=0). Never raises.
  localize_with_fallback(text, target_lang) -> (result, source)
      Localize, then online-fallback on miss. source in {"empty","same",
      "term_map","online","miss"}.
  localize_for_source(text, source) -> (result, source)
      source in {"ctgov","cde","chictr","eu_ctr","isrctn","drks","ictrp"}.
  bilingual_pair(text) -> (zh, en)
      Best-effort (zh, en) pair for `text`; if only one language is known,
      both slots carry that same text.
  suggest(text, target_lang) -> str | None
      A candidate translation from `_EXTRA` (or the map) when `text` is not in
      the target language; None if nothing known (caller/agent must supply).
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TERM_PATH = os.path.join(HERE, "..", "references", "term_map.json")

# source -> required keyword language
SOURCE_LANG = {
    "ctgov": "en",
    "cde": "zh",
    "chictr": "zh",
    "eu_ctr": "en",
    "isrctn": "en",
    "drks": "en",
    "ictrp": "en",
}

# Embedded fallback dictionary for the confirm gate: well-known terms beyond the
# curated term_map.json. Kept small and conservative -- only terms we are
# certain about. Anything NOT here returns None and the agent must translate.
# ---------------------------------------------------------------------------
# Externalized lexicon (fully externalized 2026-07-31, NO in-code fallback)
# ---------------------------------------------------------------------------
# All curated keyword data -- synonyms, brand<->generic, drug-class members,
# mAb target families, mechanism aliases, class EN->ZH suffixes, and the
# translation safety-net `_EXTRA` -- now lives in kw_lexicon.json next to this
# file. There is NO in-code fallback: if the JSON is missing, corrupt, or
# missing a required key, the module fails loudly at import time, so the agent
# never silently runs with an empty lexicon.
LEX_PATH = os.path.join(HERE, "kw_lexicon.json")
_LEX_REQUIRED = ("extra", "class_en2zh", "class_members", "mab_families",
                 "class_alias", "synonyms", "brand_generic", "drug_en2zh")


def _load_lexicon():
    """Load the externalized keyword lexicon; fail loudly if unusable."""
    if not os.path.exists(LEX_PATH):
        sys.exit(
            "[kw_localize] FATAL: lexicon file missing: %s\n"
            "  Restore ct-base/scripts/kw_lexicon.json (no in-code fallback by design)."
            % LEX_PATH
        )
    try:
        with open(LEX_PATH, encoding="utf-8") as _f:
            _data = json.load(_f)
    except Exception as _e:  # noqa: BLE001
        sys.exit("[kw_localize] FATAL: cannot parse %s: %s" % (LEX_PATH, _e))
    _missing = [k for k in _LEX_REQUIRED if k not in _data]
    if _missing:
        sys.exit("[kw_localize] FATAL: %s missing required keys: %s"
                 % (LEX_PATH, ", ".join(_missing)))
    return _data


_LEX = _load_lexicon()
_EXTRA = _LEX["extra"]
_CLASS_EN2ZH = _LEX["class_en2zh"]
_CLASS_ZH2EN = {zh: en for en, zh in _CLASS_EN2ZH.items()}  # reverse map (ZH class suffix -> EN token)
_CLASS_MEMBERS = _LEX["class_members"]
_MAB_FAMILIES = _LEX["mab_families"]
_CLASS_ALIAS = _LEX["class_alias"]
_SYNONYMS = _LEX["synonyms"]
_BRAND_GENERIC = _LEX["brand_generic"]
_DRUG_EN2ZH = _LEX["drug_en2zh"]

# Bilingual runtime prompts: delegate to ct-base's shared i18n.py (single source
# of truth for all ct- bilingual strings). EN by default; auto-switches to ZH on a
# zh-* OS locale. Per ct-base language_policy: only UI-frame LABELS are localized;
# raw data values (drug names, Chinese class suffixes) are NEVER translated.
# kw_localize.py now lives in ct-base/scripts alongside i18n.py, so a plain
# sibling import resolves in every context (direct run, or imported by a ct-
# skill that has added ct-base/scripts to sys.path).
try:
    from i18n import t as _t, is_chinese_os  # noqa: F401
except Exception:  # noqa: BLE001  (ct-base is a guaranteed sibling in the ct- lib)
    def _t(key, **kw):
        return kw.get("_default", key)
    def is_chinese_os():
        return False

_zh2en = {}
_en2zh = {}
_loaded = False


def _load():
    global _zh2en, _en2zh, _loaded
    if _loaded:
        return
    try:
        with open(TERM_PATH, encoding="utf-8") as f:
            _zh2en = json.load(f)
    except Exception:
        _zh2en = {}
    for zh, en in _zh2en.items():
        _en2zh[en.lower()] = zh
        # clean full name without parenthetical also maps to zh, so the bare
        # English phrase (e.g. "non-small cell lung cancer") round-trips too.
        clean = re.sub(r"\s*\([^)]*\)\s*", " ", en).strip().lower()
        if clean and clean != en.lower():
            _en2zh[clean] = zh
        # also index parenthetical abbreviations, e.g. "(NSCLC)" -> 非小细胞肺癌
        m = re.search(r"\(([^)]+)\)", en)
        if m:
            _en2zh[m.group(1).strip().lower()] = zh
    # Merge the embedded fallback dicts into BOTH directions so localize() (not
    # just suggest()) can actually use them. Previously _EXTRA was only reachable
    # via suggest(), so an English->Chinese or Chinese->English lookup of those
    # terms silently fell through to "miss" inside localize().
    for zh, en in _EXTRA.items():
        _zh2en.setdefault(zh, en)
        _en2zh.setdefault(en.lower(), zh)
        clean = re.sub(r"\s*\([^)]*\)\s*", " ", en).strip().lower()
        if clean and clean != en.lower():
            _en2zh.setdefault(clean, zh)
        m = re.search(r"\(([^)]+)\)", en)
        if m:
            _en2zh.setdefault(m.group(1).strip().lower(), zh)
    for en, zh in _DRUG_EN2ZH.items():
        _en2zh.setdefault(en.lower(), zh)
    for en, zh in _CLASS_EN2ZH.items():
        _en2zh.setdefault(en.lower(), zh)
    # merge _SYNONYMS (zh<->en) into both directions
    for zh, en in _SYNONYMS:
        _zh2en.setdefault(zh, en)
        _en2zh.setdefault(en.lower(), zh)
    # merge _BRAND_GENERIC (brand_zh, brand_en, generic_en, generic_zh)
    for bzh, ben, gen, gzh in _BRAND_GENERIC:
        bzh = bzh.strip()
        _zh2en.setdefault(bzh, gen)             # 泰瑞沙 -> osimertinib
        _zh2en.setdefault(gzh, gen)             # 奥希替尼 -> osimertinib
        _en2zh.setdefault(ben.lower(), bzh)     # Tagrisso -> 泰瑞沙
        _en2zh.setdefault(gen.lower(), gzh)     # osimertinib -> 奥希替尼
        _en2zh.setdefault(gzh.lower(), gen)     # 奥希替尼 -> osimertinib (zh->en back)
    # Merge drug_name_map.json (Chinese drug name -> INN/English generic) so
    # localize() can resolve common drug names (e.g. 坎地沙坦 -> candesartan)
    # without falling back to the online translation API.
    _DRUG_MAP_PATH = os.path.join(HERE, "..", "references", "drug_name_map.json")
    try:
        with open(_DRUG_MAP_PATH, encoding="utf-8") as _f:
            _drug_data = json.load(_f)
        for _zh, _en_list in _drug_data.items():
            if not isinstance(_en_list, list) or not _en_list:
                continue
            _en_first = _en_list[0].strip()
            if not _en_first:
                continue
            _zh2en.setdefault(_zh, _en_first)           # 坎地沙坦 -> candesartan
            _en2zh.setdefault(_en_first.lower(), _zh)   # candesartan -> 坎地沙坦
    except Exception:
        pass
    _loaded = True


def detect_lang(text):
    """Return 'zh' if the text contains CJK / fullwidth CJK punctuation, else 'en'."""
    if not text:
        return "en"
    for ch in text:
        o = ord(ch)
        if (0x4E00 <= o <= 0x9FFF) or (0x3400 <= o <= 0x4DBF) or \
           (0x3000 <= o <= 0x303F) or (0xFF00 <= o <= 0xFFEF):
            return "zh"
    return "en"


def _has_cjk(text):
    return detect_lang(text) == "zh"


def localize(text, target_lang):
    """Localize `text` to `target_lang` ('zh' | 'en').

    Returns (result, source) where source in:
      - 'empty'    : text is None/""            -> (text, 'empty')
      - 'same'     : text already in target_lang -> (text, 'same')  (no change)
      - 'term_map' : translated via the curated map -> (translation, 'term_map')
      - 'miss'     : not in map, opposite language -> (text, 'miss')
                     (caller should raise the confirm gate)
    """
    _load()
    if not text:
        return text, "empty"
    src = detect_lang(text)
    if src == target_lang:
        return text, "same"

    if target_lang == "en":
        # Chinese -> English
        if text in _zh2en:
            return _zh2en[text], "term_map"
        # phrase-level: replace known Chinese terms (longest first to avoid
        # partial overlaps), wrapping with spaces.
        result = text
        for zh, en in sorted(_zh2en.items(), key=lambda kv: -len(kv[0])):
            if zh in result:
                result = result.replace(zh, " " + en + " ")
        result = re.sub(r"\s+", " ", result).strip()
        # For a FOREIGN source, residual CJK means the query is NOT safely
        # translated -> treat as a miss so the caller raises the confirm gate
        # (we must not silently search CT.gov with Chinese text).
        if result != text and not _has_cjk(result):
            return result, "term_map"
        return result, "miss"

    # English -> Chinese
    low = text.lower()
    if low in _en2zh:
        return _en2zh[low], "term_map"
    # phrase-level: longest English term first, case-insensitive substring replace
    # (so multi-word terms like "brain metastasis" match as a whole).
    result = text
    changed = False
    for en_term, zh_term in sorted(_en2zh.items(), key=lambda kv: -len(kv[0])):
        if not en_term:
            continue
        pat = re.compile(re.escape(en_term), re.IGNORECASE)
        if pat.search(result):
            result = pat.sub(zh_term, result)
            changed = True
    return result, ("term_map" if changed else "miss")


# ---------------------------------------------------------------------------
# Online translation fallback (2026-08-25, ct-base references/keyword_expand.md)
# Local-first policy: the lexicon above is authoritative; the online API is
# consulted ONLY when a keyword misses locally, and only while enabled
# (default on; disable via env CT_TRANSLATE_ONLINE=0 or CLI
# --no-online-translate for air-gapped / confidential searches).
# Keyless public endpoint (Google gtx) keeps zero-secret egress. Any failure
# returns None and the caller degrades to the confirm gate — never blocks.
# ---------------------------------------------------------------------------
_CT_TRANSLATE_ONLINE = os.environ.get("CT_TRANSLATE_ONLINE", "1").strip().lower() \
    not in ("0", "false", "no", "off")


def online_translate(text, target_lang="en", timeout=6):
    """Best-effort keyless online translation — last-resort fallback.

    Primary endpoint: MyMemory (api.mymemory.translated.net, free, no key,
    per-IP daily quota); fallback: Google gtx public endpoint (unreachable in
    CN networks, kept as backup).

    Retry policy (P1 2026-10-08):
      - MyMemory: 2 attempts, ``timeout`` seconds each (CN-reachable primary).
      - Google gtx: 1 attempt, min(timeout, 3) seconds (likely blocked in CN;
        short timeout avoids long hangs). Skip entirely when env
        ``CT_TRANSLATE_GOOGLE=0``.
      - 0.3 s backoff between retries (avoids per-IP throttling on MyMemory).

    Returns the translated string, or None when disabled / on any failure
    (network, timeout, malformed payload). Never raises. Only call after the
    local lexicon has missed.
    """
    if not _CT_TRANSLATE_ONLINE or not text:
        return None
    if detect_lang(text) == target_lang:
        return None
    import time
    import urllib.parse
    import urllib.request
    sl, tl = ("zh-CN", "en") if target_lang == "en" else ("en", "zh-CN")
    q = urllib.parse.quote(text)

    def _get(url, t):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=t) as r:
            return json.loads(r.read().decode("utf-8"))

    # 1) MyMemory (primary, CN-reachable, free & keyless) — 2 retries
    for attempt in range(2):
        try:
            data = _get("https://api.mymemory.translated.net/get?q=%s&langpair=%s|%s"
                        % (q, sl, tl), timeout)
            if data.get("responseStatus") == 200:
                out = (data.get("responseData") or {}).get("translatedText") or ""
                out = out.strip()
                if out and out.lower() != text.lower():
                    return out
        except Exception:  # noqa: BLE001
            pass
        if attempt == 0:
            time.sleep(0.3)  # short backoff before retry

    # 2) Google gtx (backup; likely blocked in CN — short timeout, 1 attempt)
    if os.environ.get("CT_TRANSLATE_GOOGLE", "1").strip().lower() not in ("0", "false", "no", "off"):
        try:
            gtx_timeout = min(timeout, 3)
            data = _get("https://translate.googleapis.com/translate_a/single"
                        "?client=gtx&dt=t&sl=%s&tl=%s&q=%s" % (sl, tl, q), gtx_timeout)
            seg = data[0] if isinstance(data, list) and data else None
            parts = [s[0] for s in seg if isinstance(s, list) and s and s[0]] \
                if isinstance(seg, list) else []
            out = "".join(parts).strip()
            if out:
                return out
        except Exception:  # noqa: BLE001  (fallback must never raise)
            pass
    return None


def localize_with_fallback(text, target_lang):
    """Localize, then fall back to the online API on a local miss.

    Returns (result, source) with source in
    {"empty","same","term_map","online","miss"}.
    """
    result, st = localize(text, target_lang)
    if st != "miss":
        return result, st
    tr = online_translate(text, target_lang)
    if tr:
        return tr, "online"
    return result, "miss"


def localize_for_source(text, source):
    """Localize `text` for a given registry `source` (see SOURCE_LANG)."""
    lang = SOURCE_LANG.get(source, "en")
    return localize(text, lang)


def bilingual_pair(text):
    """Return a best-effort (zh, en) pair for `text`.

    - If `text` is a known Chinese term -> (zh, en_translation).
    - If `text` is a known English term -> (zh_translation, en).
    - Otherwise -> (text, text) (only one language is known).
    """
    _load()
    if not text:
        return ("", "")
    if text in _zh2en:
        return (text, _zh2en[text])
    low = text.lower()
    if low in _en2zh:
        return (_en2zh[low], text)
    return (text, text)


def suggest(text, target_lang):
    """Return a candidate translation for `text` into `target_lang`, or None.

    Used by the confirm gate to *propose* a translation when the curated map
    misses. Consults `_EXTRA` (and the map) only -- never fabricates.
    """
    _load()
    if not text:
        return None
    if detect_lang(text) == target_lang:
        return None
    if target_lang == "en":
        if text in _zh2en:
            return _zh2en[text]
        if text in _EXTRA:
            return _EXTRA[text]
    else:
        low = text.lower()
        if low in _en2zh:
            return _en2zh[low]
        rv = {v.lower(): k for k, v in _EXTRA.items()}
        if low in rv:
            return rv[low]
    return None


def class_token_of(text):
    """If `text` is (or contains) a known drug CLASS token, return its canonical
    English class key (e.g. 'sartan' / 'statin'); else None."""
    _load()
    if not text:
        return None
    low = text.lower().strip()
    if low in _CLASS_EN2ZH:
        return low                       # canonical English class key
    if low in _CLASS_ZH2EN:
        return _CLASS_ZH2EN[low]        # Chinese suffix -> English key
    # also accept the bare Chinese class suffix (e.g. '沙坦')
    if text in _CLASS_ZH2EN:
        return _CLASS_ZH2EN[text]
    return None


def kw_match_candidates(text, source=None):
    """Return a MENU of candidate keyword interpretations for a non-standard
    (miss / category / ambiguous) `text`. Implements the ct-base §8 keyword
    disambiguation menu ('未找到结果。您是否想检索：{suggestion}？') so the
    user picks the right interpretation instead of the agent silently
    trial-and-erroring combinations.

    Each candidate is a dict: {"strategy", "value", "note"}.
    Strategies reflect the empirically observed endpoint matching semantics
    (see references/keyword_match.md):
      - as_is        : use the original text verbatim (risk of 0 hits)
      - translate    : term_map / embedded dict translation (zh<->en)
      - class_suffix : map a drug CLASS to its Chinese class suffix (CDE wins)
      - enumerate    : list specific members of a class (WHO needs exact names)
      - structured   : WHO structured condition+intervention fields
    """
    _load()
    if not text:
        return []
    lang = detect_lang(text)
    opp = "zh" if lang == "en" else "en"
    cands = []
    seen = set()

    def add(strategy, value, note):
        if value is None:
            return
        if isinstance(value, list):
            key = (strategy, "|".join(value))
        else:
            key = (strategy, str(value))
        if key in seen:
            return
        seen.add(key)
        cands.append({"strategy": strategy, "value": value, "note": note})

    add("as_is", text, "直接使用原文 (可能漏检, 尤其外文源对中文/类别词)")
    tr, st = localize(text, opp)
    if st == "term_map" and tr != text:
        add("translate", tr, f"术语表/扩展词库翻译 -> {opp}")

    cls = class_token_of(text)
    if cls:
        zh_suffix = _CLASS_EN2ZH.get(cls)
        if zh_suffix and zh_suffix != text:
            add("class_suffix", zh_suffix,
                "类别词 -> 中文类名后缀 (适合 CDE 子串匹配)")
        members = _CLASS_MEMBERS.get(cls)
        if members:
            add("enumerate", members,
                "枚举类别具体成员 (适合 WHO 精确药名匹配)")
        if source in (None, "who", "ictrp"):
            add("structured", f"who_condition + who_intervention=具体成员",
                "WHO 结构化字段 (类别词直接填无结果, 须具体药名)")

    # de-duplicate as_is if a translate already equals the original
    return cands


def render_kw_menu(text, candidates):
    """Render the candidate list as a numbered, user-selectable menu string."""
    if not candidates:
        return (f"[ct_registry][KW-MENU] 关键字 {text!r} 无可用解释, "
                f"请直接提供 --cde-keyword / --confirm-* 指定译文。")
    L = [f"[ct_registry][KW-MENU] 关键字 {text!r} 非标准/未命中术语表, "
         f"请选择检索解释 (避免反复试错):"]
    for i, c in enumerate(candidates, 1):
        v = c["value"]
        if isinstance(v, list):
            v = " / ".join(v)
        L.append(f"  {i}. [{c['strategy']}] {v}  — {c['note']}")
    L.append("  0. 取消")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# Keyword expansion engine (ct-registry v0.4 — keyword-system confirmation gate)
# ---------------------------------------------------------------------------

# Intent code -> i18n key. The label is a UI-frame label, so it is localized at
# render time; raw data values (drug names, Chinese class suffixes) are NEVER
# localized.
_INTENT_LABEL_KEYS = {
    "disease": "kw_gate.intent_disease",
    "intervention": "kw_gate.intent_intervention",
    "drug": "kw_gate.intent_drug",
    "drug_class": "kw_gate.intent_drug_class",
    "auto": "kw_gate.intent_auto",
}

def _mab_family_of(base):
    """Return the target-family key in _MAB_FAMILIES matching base, or None."""
    rules = [
        ("anti-PD-1", ["pd-1", "pd 1", "pd1"]),
        ("anti-PD-L1", ["pd-l1", "pd l1", "pdl1"]),
        ("anti-CTLA-4", ["ctla-4", "ctla4", "ctla"]),
        ("anti-HER2", ["her2", "her-2"]),
        ("anti-EGFR", ["egfr"]),
        ("anti-VEGF", ["vegf"]),
        ("anti-CD20", ["cd20", "cd-20"]),
        ("anti-CD38", ["cd38", "cd-38"]),
        ("anti-IL", ["il-", "il ", "白介素", "白细胞介素"]),
        ("anti-TNF", ["tnf", "肿瘤坏死因子"]),
        ("anti-PCSK9", ["pcsk9"]),
        ("anti-RANKL", ["rankl", "rank-l"]),
        ("anti-IgE", ["ige"]),
        ("anti-CD52", ["cd52"]),
        ("anti-BCMA", ["bcma"]),
        ("anti-CD19", ["cd19"]),
        ("anti-Claudin18.2", ["claudin18", "claudin 18", "claudin18.2"]),
    ]
    low = base.lower()
    for fam, keys in rules:
        if any(k in low for k in keys):
            return fam
    return None


def _detect_intent(base, intent):
    """Resolve intent: honor explicit value unless 'auto'."""
    if intent and intent != "auto":
        return intent
    low = base.lower()
    if (class_token_of(base) == "mab" or "单抗" in base or low.endswith("mab")
            or _mab_family_of(base)
            or any(k in base for k in ("PD-1", "PD-L1", "CTLA-4", "HER2",
                                       "EGFR", "VEGF", "PCSK9"))):
        return "drug_class"
    if class_token_of(base) or base.lower() in _CLASS_ALIAS:
        return "drug_class"
    for bzh, ben, gen, gzh in _BRAND_GENERIC:
        if base in (bzh, ben, gen, gzh) or low == gen.lower() or low == ben.lower():
            return "drug"
    if low in _DRUG_EN2ZH or base in _DRUG_EN2ZH.values():
        return "drug"
    if base in _zh2en or low in _en2zh:
        return "disease"
    return "intervention"


def _expand_from_lexicon(base):
    """Return (zh_set, en_set) of all synonym / brand / generic aliases of base."""
    zh, en = set(), set()
    if detect_lang(base) == "zh":
        zh.add(base)
    else:
        en.add(base.lower())
    for z, e in _SYNONYMS:
        if base in (z, e) or base.lower() == e.lower():
            zh.add(z)
            en.add(e.lower())
    for bzh, ben, gen, gzh in _BRAND_GENERIC:
        if base in (bzh, ben, gen, gzh) or base.lower() == gen.lower() \
                or base.lower() == ben.lower():
            zh.add(bzh.strip())
            zh.add(gzh)
            en.add(gen.lower())
            en.add(ben.lower())
    return zh, en


def _class_members(cls):
    """Member English drug names for a class token (mAb handled separately)."""
    if cls == "mab":
        return []
    return _CLASS_MEMBERS.get(cls, [])


def _assign_per_source(zh, en, cls, members_en):
    """Build per_source keyword sets per registry matching semantics."""
    en_kw = sorted(members_en) if members_en else sorted(en)
    if cls == "mab":
        cde_kw = [next(iter(sorted(zh)))] if zh else []
        cde_note = "子串匹配，取首个靶点族成员中文名兜底（可改更窄）"
    elif members_en and len(members_en) >= 3 and cls:
        zh_suffix = _CLASS_EN2ZH.get(cls)
        cde_kw = [zh_suffix] if zh_suffix else sorted(zh)
        cde_note = "子串匹配 → 单「后缀」一次覆盖全部（勿加「类」字）"
    else:
        cde_kw = sorted(zh)
        cde_note = "子串匹配，多词兜底"
    return {
        "ctgov":  {"lang": "en", "keywords": en_kw,
                   "note": "精确匹配 → 类别/靶点族枚举具体药名；裸类别易漏"},
        "who":    {"lang": "en", "keywords": en_kw,
                   "note": "同 CT.gov；结构化须填具体药名"},
        "cde":    {"lang": "zh", "keywords": cde_kw, "note": cde_note},
        "chictr": {"lang": "zh", "keywords": cde_kw, "note": "子串匹配，多词兜底"},
    }


def _kw_risks(base, cls):
    risks = []
    if cls and cls != "mab":
        risks.append("WHO/CT.gov 精确匹配下裸类别词易漏检 → 已枚举成员兜底")
        zh_suffix = _CLASS_EN2ZH.get(cls)
        if zh_suffix:
            risks.append(f"CDE 子串匹配下务必去掉「类」字（{zh_suffix}类=0，{zh_suffix}=命中）")
    if cls == "mab":
        risks.append("单抗(mAb)已按靶点族枚举具体成员；WHO 需具体药名，勿用裸「单抗」")
    if not cls:
        risks.append("未识别为药物类别，按疾病/干预词直接中英互译检索")
    return risks


def expand_keyword(base, intent="auto"):
    """Expand a narrow user keyword into a structured keyword Manifest.

    Core three-piece set (ct-registry v0.4):
      1) zh<->en translation (localize / term_map / _EXTRA / _SYNONYMS / brand)
      2) synonym / alias + brand<->generic (_SYNONYMS / _BRAND_GENERIC)
      3) drug-class enumeration (_CLASS_MEMBERS; mAb by target family)
    Returns a dict (Manifest) or None when base is empty.
    """
    _load()
    base = (base or "").strip()
    if not base:
        return None
    intent = _detect_intent(base, intent)
    zh, en = _expand_from_lexicon(base)
    if detect_lang(base) == "zh":
        tr, st = localize(base, "en")
        if tr and tr != base and st in ("term_map", "same"):
            en.add(tr.lower())
    else:
        tr, st = localize(base, "zh")
        if tr and tr != base and st in ("term_map", "same"):
            zh.add(tr)
    cls = class_token_of(base)
    if cls is None:
        cls = _CLASS_ALIAS.get(base.lower())
    fam = _mab_family_of(base)
    members_en = set()
    if fam:
        for m in _MAB_FAMILIES.get(fam, []):
            members_en.add(m)
            mz, _ = localize(m, "zh")
            if mz and mz != m:
                zh.add(mz)
    elif cls == "mab":
        pass  # bare '单抗'/'mab' without a target -> cannot enumerate members
    elif cls:
        for m in _class_members(cls):
            members_en.add(m)
            mz, _ = localize(m, "zh")
            if mz and mz != m:
                zh.add(mz)
    en |= members_en
    per_source = _assign_per_source(zh, en, cls, members_en)
    risks = _kw_risks(base, cls)
    confidence = {"term_map": sorted(zh | en), "alias": [], "class_enum": sorted(members_en),
                  "speculative": []}
    return {
        "base": base,
        "intent": intent,
        "zh": sorted(zh),
        "en": sorted(en),
        "per_source": per_source,
        "risks": risks,
        "confidence": confidence,
    }


# --- session Manifest cache (disk-backed; avoids re-confirming the same term) ---
_KW_CACHE_PATH = os.path.join(HERE, "..", "config", "kw_system_cache.json")


def _kw_cache_key(base, intent):
    import hashlib
    return hashlib.md5(f"{base}|{intent}".encode("utf-8")).hexdigest()


def load_kw_cache():
    try:
        with open(_KW_CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_kw_cache(cache):
    try:
        os.makedirs(os.path.dirname(_KW_CACHE_PATH), exist_ok=True)
        with open(_KW_CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get_cached_manifest(base, intent):
    return load_kw_cache().get(_kw_cache_key(base, intent))


def cache_manifest(manifest, intent=None):
    """Persist an adopted Manifest. Keyed by the REQUESTED intent (the same value
    ``get_cached_manifest`` looks up with), NOT the resolved ``manifest['intent']``,
    so a later lookup with the same requested intent hits the cache."""
    cache = load_kw_cache()
    key = _kw_cache_key(manifest["base"], intent or manifest["intent"])
    cache[key] = manifest
    save_kw_cache(cache)


def render_kw_system_menu(manifest, title_override=None):
    """Render the keyword-system confirmation menu (forced, before Gate 1).

    Framework labels are localized via ct-base i18n (EN default, ZH on a zh-*
    OS). Raw data values (drug names, Chinese class suffixes, user-supplied
    terms) are NEVER translated.
    """
    if not manifest:
        return _t("kw_gate.empty")
    m = manifest
    intent_label = _t(_INTENT_LABEL_KEYS.get(m["intent"], "kw_gate.intent_auto"))
    L = []
    L.append("🔍 " + (title_override or _t("kw_gate.title")))
    L.append("")
    L.append(_t("kw_gate.original", base=m["base"], intent=intent_label))
    zh_terms = ", ".join(m["zh"]) if m["zh"] else _t("kw_gate.none")
    en_terms = ", ".join(m["en"]) if m["en"] else _t("kw_gate.none")
    L.append(f"{_t('kw_gate.zh')}: {zh_terms}")
    L.append(f"{_t('kw_gate.en')}: {en_terms}")
    L.append("")
    L.append(_t("kw_gate.per_source"))
    ps = m["per_source"]
    L.append(f"  · {_t('kw_gate.ctgov')}: {' / '.join(ps['ctgov']['keywords'])}")
    L.append(f"  · {_t('kw_gate.cde')}: {' / '.join(ps['cde']['keywords'])}")
    if m["risks"]:
        L.append("")
        L.append(_t("kw_gate.risk"))
        for r in m["risks"]:
            L.append(f"  - {r}")
    spec = m["confidence"].get("speculative")
    L.append("")
    L.append(f"{_t('kw_gate.speculative')} {', '.join(spec) if spec else _t('kw_gate.none')}")
    L.append("")
    L.append(_t("kw_gate.confirm"))
    L.append("  " + _t("kw_gate.opt_adopt"))
    L.append("  " + _t("kw_gate.opt_del"))
    L.append("  " + _t("kw_gate.opt_add"))
    L.append("  " + _t("kw_gate.opt_scope"))
    L.append("  " + _t("kw_gate.opt_cancel"))
    L.append("")
    L.append(_t("kw_gate.after"))
    return "\n".join(L)


def render_kw_system_menu_multi(manifests):
    """Render a consolidated keyword-system confirmation menu for multiple axes
    (e.g. condition + intervention). Each manifest block reuses the single-axis
    template (with a per-axis title override); one shared action menu is appended.

    `manifests`: list of (axis, base, manifest) tuples, axis in
    {"condition", "intervention"}.
    """
    if not manifests:
        return _t("kw_gate.empty")
    blocks = []
    for i, (axis, base, m) in enumerate(manifests, 1):
        axis_label = _t("kw_gate.axis_condition" if axis == "condition"
                        else "kw_gate.axis_intervention")
        block = render_kw_system_menu(
            m, title_override=_t("kw_gate.title_multi", i=i, axis=axis_label))
        blocks.append(block)
    menu = "\n\n".join(blocks)
    menu += "\n\n" + "─" * 40
    menu += "\n" + _t("kw_gate.multi_confirm", n=len(manifests))
    menu += "\n  " + _t("kw_gate.multi_opt_adopt")
    menu += "\n  " + _t("kw_gate.opt_del")
    menu += "\n  " + _t("kw_gate.opt_add")
    menu += "\n  " + _t("kw_gate.opt_scope")
    menu += "\n  " + _t("kw_gate.opt_cancel")
    menu += "\n\n" + _t("kw_gate.after")
    return menu


if __name__ == "__main__":
    # quick self-check
    tests = [
        ("非小细胞肺癌", "en"),
        ("NSCLC", "zh"),
        ("osimertinib", "zh"),
        ("奥希替尼", "en"),
        ("non-small cell lung cancer", "zh"),
        ("非小细胞肺癌 脑转移", "en"),
        ("罕见未知药物XYZ", "en"),   # miss -> confirm gate candidate
        ("高血压", "en"),            # _EXTRA hit
    ]
    for t, lang in tests:
        r, s = localize(t, lang)
        print(f"[{s:>8}][->{lang}] {t!r} => {r!r}")
    print("--- bilingual_pair ---")
    for t in ["非小细胞肺癌", "NSCLC", "奥希替尼", "糖尿病", "未知词"]:
        print(f"{t!r} -> zh/en {bilingual_pair(t)}")
    print("--- suggest ---")
    for t, lang in [("高血压", "en"), ("糖尿病", "en"), ("未知词", "en"), ("NSCLC", "zh")]:
        print(f"suggest({t!r}->{lang}) = {suggest(t, lang)!r}")
    print("--- class + drug coverage (CDE target) ---")
    for t in ["sartan", "valsartan", "losartan", "statin", "metformin", "ARB", "高血压"]:
        r, s = localize(t, "zh")
        print(f"localize({t!r}->zh) = [{s}] {r!r}")
    print("--- kw_match_candidates ---")
    for t in ["sartan", "高血压", "valsartan"]:
        print(f"* {t!r}:")
        for c in kw_match_candidates(t, "cde"):
            v = c["value"] if not isinstance(c["value"], list) else " / ".join(c["value"])
            print(f"    [{c['strategy']}] {v}  — {c['note']}")
