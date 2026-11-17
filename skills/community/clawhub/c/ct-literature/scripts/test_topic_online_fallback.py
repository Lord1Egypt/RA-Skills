#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_topic_translator_online_fallback.py -- online-fallback translation test

Scenarios:
  A. Pure English -> no translation (short-circuit)
  B. Local dict hit (Chinese term in drug_name_map / kw_lexicon)
  C. Local dict miss + online fallback recovers (mocked kw_localize)
  D. Local dict miss + online fallback fails -> original preserved
  E. online_fallback=False -> no network, original preserved
  F. CT_TRANSLATE_ONLINE=0 -> same as E
  G. No ct-base installed -> graceful degradation (no raise)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import topic_translator as tt

PASS, FAIL = 0, 0


def ck(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  OK   {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name} -- {detail}")


# -------- A. Pure English short-circuit --------
print("\n[A] Pure English -> no translation")
r = tt.translate_topic("osimertinib")
ck("translated=False", r["translated"] is False, repr(r["translated"]))
ck("topic_en == original", r["topic_en"] == "osimertinib", repr(r["topic_en"]))
ck("untranslated empty", r["untranslated"] == [], repr(r["untranslated"]))

# -------- B. Local dict hit --------
# "奥希替尼" (osimertinib) is in kw_lexicon.drug_en2zh / brand_generic
print("\n[B] Local dict hit -- Chinese term")
r = tt.translate_topic("奥希替尼")
print(f"  -> topic_en = {r['topic_en']}")
ck("translated=True", r["translated"] is True)
ck("osimertinib present", "osimertinib" in r["topic_en"].lower(), repr(r["topic_en"]))
ck("hits non-empty", len(r["hits"]) >= 1, f"n={len(r['hits'])}")
ck("sources has local entry",
   any(s in ["term_map", "drug_name_map", "kw_lexicon.drug_en2zh",
             "kw_lexicon.brand_generic", "kw_lexicon.extra", "kw_lexicon.synonyms"]
       for s in r["sources"]), repr(r["sources"]))
ck("untranslated empty", r["untranslated"] == [], repr(r["untranslated"]))

# -------- C. Online fallback (mocked) --------
# Use Chinese terms NOT in any local dictionary to force fallback
# "瓦西兰" / "西兰花" / "新靶点" are confirmed to survive local dict intact
print("\n[C] Online fallback -- unrecovered Chinese term via mock")


class FakeKwLocalizeOnline:
    def localize_with_fallback(self, text, target_lang):
        mapping = {
            "瓦西兰": "waxilan",
            "西兰花": "broccoli",
            "新靶点": "novel_target",
        }
        if text in mapping:
            return mapping[text], "online"
        return text, "miss"


orig_import = tt._import_kw_localize
tt._import_kw_localize = lambda: FakeKwLocalizeOnline()
r = tt.translate_topic("瓦西兰 西兰花 新靶点")
tt._import_kw_localize = orig_import
print(f"  -> topic_en = {r['topic_en']}")
ck("recovered: 瓦西兰 -> waxilan", "waxilan" in r["topic_en"].lower(), repr(r["topic_en"]))
ck("recovered: 西兰花 -> broccoli", "broccoli" in r["topic_en"].lower(), repr(r["topic_en"]))
ck("recovered: 新靶点 -> novel_target", "novel_target" in r["topic_en"].lower(), repr(r["topic_en"]))
ck("sources has 'online'", "online" in r["sources"], repr(r["sources"]))
ck("untranslated empty (recovered)", r["untranslated"] == [], repr(r["untranslated"]))

# -------- D. Online fallback also fails --------
print("\n[D] Online fallback fails -- unknown Chinese term")


class FakeKwLocalizeMiss:
    def localize_with_fallback(self, text, target_lang):
        return text, "miss"


tt._import_kw_localize = lambda: FakeKwLocalizeMiss()
r = tt.translate_topic("瓦西兰 西兰花")
tt._import_kw_localize = orig_import
print(f"  -> topic_en = {r['topic_en']}")
ck("original preserved: 瓦西兰", "瓦西兰" in r["topic_en"], repr(r["topic_en"]))
ck("original preserved: 西兰花", "西兰花" in r["topic_en"], repr(r["topic_en"]))
ck("untranslated non-empty", len(r["untranslated"]) >= 1, repr(r["untranslated"]))

# -------- E. online_fallback=False --------
print("\n[E] online_fallback=False")
r = tt.translate_topic("瓦西兰 西兰花 新靶点", online_fallback=False)
print(f"  -> topic_en = {r['topic_en']}")
ck("no fallback, 瓦西兰 preserved", "瓦西兰" in r["topic_en"], repr(r["topic_en"]))
ck("no fallback, 西兰花 preserved", "西兰花" in r["topic_en"], repr(r["topic_en"]))
ck("untranslated non-empty",
   any("瓦西兰" in u for u in r["untranslated"]),
   repr(r["untranslated"]))

# -------- F. CT_TRANSLATE_ONLINE=0 --------
print("\n[F] CT_TRANSLATE_ONLINE=0")
tt._CT_TRANSLATE_ONLINE = False
r = tt.translate_topic("瓦西兰 西兰花 新靶点")
tt._CT_TRANSLATE_ONLINE = True
print(f"  -> topic_en = {r['topic_en']}")
ck("no fallback, 瓦西兰 preserved", "瓦西兰" in r["topic_en"], repr(r["topic_en"]))

# -------- G. No ct-base installed --------
print("\n[G] ct-base module missing -> graceful degradation")
tt._import_kw_localize = lambda: None  # simulate missing kw_localize
r = tt.translate_topic("瓦西兰 西兰花 新靶点")
tt._import_kw_localize = orig_import
print(f"  -> topic_en = {r['topic_en']}")
ck("no exception raised", True)
ck("original preserved, 瓦西兰", "瓦西兰" in r["topic_en"], repr(r["topic_en"]))
ck("untranslated non-empty", len(r["untranslated"]) >= 1, repr(r["untranslated"]))

# -------- Summary --------
print(f"\n{'=' * 50}")
print(f"Total {PASS + FAIL} assertions, {PASS} passed, {FAIL} failed")
sys.exit(0 if FAIL == 0 else 1)
