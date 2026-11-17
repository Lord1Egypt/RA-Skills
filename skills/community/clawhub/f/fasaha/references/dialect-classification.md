# Dialect Classification Reference

Full breakdown from QALB Guidelines Section 5.6 (Dialectal Usage Correction).
Source: http://nlp.qatar.cmu.edu/qalb/QALB-guidelines_0.90.pdf

QALB's own annotators were instructed NOT to do systematic dialect-to-MSA translation — only to
correct spelling inconsistency. The six categories below determine which dialectal words are
close enough to MSA to warrant correction, and which aren't.

## 5.6.1 — Lexical choices (not related to MSA at all)

Words specific to a region, not morphologically related to any MSA word. Not in standard
dictionaries. **No correction — these have no MSA equivalent to correct to.**

| Dialect word | Correction |
|---|---|
| كرهبة (Tunisian) | كرهبة (no correction required) |
| زعلان | زعلان (no correction required) |
| بلش | بلش (no correction required) |
| ماطيشة | ماطيشة (no correction required) |
| برشا | برشا (no correction required) |
| شلونك | شلونك (no correction required) |

## 5.6.2 — Pseudo-dialectal lexical choices

Words that *look* dialectal but are actually valid, dictionary-attested MSA (may be uncommon in
literature but not wrong). **No correction — check a dictionary before "fixing" these.**

| Word | Status |
|---|---|
| زعلان | Valid — no correction required |
| أنت مزعوج | Valid — no correction required |
| أوتوبيس | Valid — no correction required |

## 5.6.3 — Morphological choices

Dialectal verb/pronoun forms morphologically related to an MSA word by a regional variation.
**Correction required — translate to the MSA form.**

| Dialect | MSA |
|---|---|
| انتو جعلتوا | أنتم جعلتم |
| بيكتب | سيكتب |

Full-sentence example:
- Source (Levantine dialect, marked words in bold): لا نحترم اللي في الخارج في فندق خمس نجوم
  بشحدو علينا
- Corrected: لا نحترم الذين في الخارج في فندق خمس نجوم يشحذون علينا

## 5.6.4 — Phonological choices

Dialectal words phonologically (sound-)related to an MSA word by regional variation.
**Correction required.**

| Dialect | MSA |
|---|---|
| جذور | جزور |
| زريتك | ذريتك |
| كهك | كعك |

## 5.6.5 — Closed-class dialectal words

A limited, known set of pronouns and verbal particles that are clearly dialectal and can be
safely corrected. **Correction required — this is a short, memorizable list.**

| Dialect | MSA |
|---|---|
| اللي | الذي / الذين |
| عم ناكل | سنأكل |
| هذي | هذه |
| هايدي | هذه |
| مش | ليس / لم (حسب السياق) |
| موش | ليس / لم (حسب السياق) |

**Note on `مش`/`موش`:** these negate the predicate *copula* ("is not"), so the general MSA
mapping is `ليس` / `ليست` (e.g. `هو مش طويل` → `ليس طويلاً`). They only map to `لم` when the
sense is negation of a past action (`هو مش راح` → `لم يذهب`). Match the mapping to the actual
predicate; don't blanket-replace with `لم`.

## 5.6.6 — Foreign words and proper names

**No correction unless the spelling is clearly wrong** — don't "fix" the word choice, only fix
genuine misspellings.

| Word | Status |
|---|---|
| كاتشيب | No correction required (valid spelling) |
| كانيلوني | No correction required (valid spelling) |
| وايت هاوس | No correction required (valid spelling) |
| جورج بوش | No correction required (valid spelling) |

If the spelling is clearly wrong (verify via search-frequency comparison — see
`references/qalb-spelling-rules.md` "When Still Unsure"), correct it:

| Wrong | Right |
|---|---|
| كطشيب | كاتشيب |
| كنيوني | كانيلوني |
| وات هاوص | وايت هاوس |
| جورح بش | جورج بوش |

## When Text Is Mostly Dialectal

Per QALB's own rule: if a passage is more than roughly one-third (33%) dialectal, or uses a
dialect the reviewer isn't confident interpreting correctly, don't attempt word-by-word MSA
correction — flag the passage instead. Partial correction of heavily dialectal text tends to
produce a worse result than either leaving it as-is or asking for clarification, because it
creates a false impression of full MSA correctness while dialectal structure remains underneath.
