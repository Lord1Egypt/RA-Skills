<div align="center">

# anti-ai-foolish

**Anti-AI-Foolish · De-AI Gatekeeper**

🇨🇳 [简体中文](README.md) | 🇬🇧 **English**

</div>

---

A pre-publish gatekeeper that answers one question: **is this draft safe to publish, or does it still read as AI-generated?**

Every decision rule is evidence-backed: 1,108 rules were **A/B-tested one by one against 52 fragments carrying real Tencent Zhuque detector labels** (95% confidence intervals). Rules that failed testing are marked as such — nothing unverified is passed off as effective.

## Quick start

```bash
git clone https://github.com/forrestneo/anti-ai-foolish.git
cd anti-ai-foolish

# One-command pre-publish gate
python scripts/preflight.py your_article.md
```

Sample output:

```
# Preflight — your_article.md
Body 2,689 chars | Z-score 0 (AI confirmed 1 − human confirmed 1)
  ✓ colons = 0
  ✓ em-dashes = 0
  ...
Gates 7/7 → ✅ ready to publish (re-test on Zhuque in chunks first)
```

## Install

Standard Agent Skill format — works with Claude Code / Codex / ZCode or anything that supports Agent Skills. Clone or download this repo, then copy the whole directory into your skills folder:

```bash
# ZCode
cp -r anti-ai-foolish ~/.zcode/skills/anti-ai-foolish
# Claude Code
cp -r anti-ai-foolish ~/.claude/skills/anti-ai-foolish
```

Requirements: Python 3.8+, standard library only. Zero third-party dependencies, fully offline, uploads nothing.

## How it works

Four-step workflow (see `SKILL.md`):

```
① Mechanical preflight     python scripts/preflight.py → 6 hard gates + Z-score
② Human judgment           experiential-"I" vs performative-"I" / people-as-subject / symmetrical triples
③ Seven-knife surgery      colons → concept-quoting → data dumps → golden-sentence symmetry
                           → structure → word list → *replace the skeleton*
④ Re-check + platform test re-run preflight to ✅; paste into Zhuque in 1,000–2,000-char chunks, target ≤ 0.40
```

**Three popular tips disproved by measurement** (n=52, 95% CI):

| Popular claim | Measured truth |
|---|---|
| Parallelism is an AI tell | Colloquial repetition is *denser in human* writing (r=-0.37); only symmetrical argument triples ("can X, yet cannot Y" ×3) hurt |
| Adding colloquialisms lowers scores | No protection (r=-0.25); performed colloquialism appeared in a 0.99-scored paragraph |
| Delete inner monologue | Outdated (r=-0.24) — modern AI already avoids it |

**Confirmed signals**: colons (r=+0.43, strongest single), the concept-quoting tic (quoting your own jargon — AI does it 5.5× more), question density, em-dashes.

**The core finding — the Skeleton–Fuel Law**: same author, same themes — lived experience as the skeleton scored **0.09** on Zhuque; concept framework as the skeleton with real events as fuel scored **0.75–0.995**. What decides the score is not whose voice or which words — it's whether the skeleton is *someone doing something* or *a concept reasoning about itself*.

## Field results

- Unedited AI drafts (Zhuque-measured 0.91 / 0.93) → preflight correctly blocks ✓
- Post-surgery drafts → 7/7 gates pass; Zhuque re-test moves the body into the **human-feature zone** (AIGC 0.14) ✓
- 13 legacy articles processed through the full pipeline, all passing mechanical gates

## Project layout

```
anti-ai-foolish/
├── SKILL.md            # skill entry: workflow + iron rules + limits
├── scripts/
│   ├── preflight.py    # pre-publish gate (6 hard gates + Z-score + verdict)
│   ├── scanner.py      # rule engine (1,108 rules → tiered report with fixes)
│   └── abtest.py       # A/B re-validation (corpus update re-scores everything)
├── rules/              # 13 rule libraries (each rule carries status/evidence/fix/exempt)
├── validation/         # 52 Zhuque-labeled fragments + results
└── references/         # methodology, evidence chain, eval report, roadmap
```

Every rule carries one of five statuses: `confirmed` / `reversed` / `directional` / `no_signal` / `insufficient`.

## Honest limitations

- 97% recall / 53% specificity — a **publishing quality gate**, not a human-vs-AI classifier; Z<0 does not prove "human-written"
- Mechanical ceiling ≈ 0.8 correlation; the remaining variance is exactly what the human-judgment step covers
- Corpus genre is Chinese self-media commentary; for other genres, add labeled fragments to `validation/corpus/` and re-run `scripts/abtest.py`
- Language-layer optimization only — never fabricates facts; every fix preserves the original meaning and evidence

## ⚠️ Before you fork

`validation/corpus/` contains raw fragments from detector reports. Before publishing your own copy, make sure this is safe to share for you and your corpus contributors; deleting the directory does not affect the tool.

## License

MIT
