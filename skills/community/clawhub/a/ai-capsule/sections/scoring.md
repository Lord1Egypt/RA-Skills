# Scoring Framework (RUND+WPS)

**Rational dimensions (RUND)**

| Dim | Name | Scoring criteria |
|-----|------|-----------------|
| R | Relevance | Precise match to tech stack/scenario=10; requires cross-language adaptation=7; same broad domain but not directly reusable=4; unrelated=0 |
| U | Utility | **solve/scout mode**: contains directly usable code/data/templates=9-10; complete step-by-step guide=7-8; opinion/info only=5-6; no substantive content=0-4. **learn mode**: what can you do after reading that you couldn't before — large clear capability gain=9-10; has methodology but needs self-practice=7-8; only conceptual awareness=5-6; no real cognitive gain=0-4 |
| N | Novelty | **solve/scout mode**: paradigm-shifting new architecture=10; major SOTA breakthrough=7-8; routine iteration=5; already known=0-3. **learn mode**: this direction/concept is still unfamiliar to most engineers=9-10; rapidly evolving and worth tracking=7-8; mainstream but still learnable=5-6; already widely known=0-3 |
| D | Depth | Source code / original paper / math derivation=10; detailed long-form with solid evidence=7-8; summary/brief=5; clickbait=0-3 |

**Emotional dimensions (WPS)**

| Dim | Name | Scoring criteria |
|-----|------|-----------------|
| W | Wow | Results completely counter-intuitive / algorithm elegantly surprising=10; industrial-grade polish=8; adequate=6; mediocre=0-5 |
| P | Perspective | Defines an entirely new category/concept=10; reframes an old problem with a new lens=8-9; stays within conventional frameworks=0-7 |
| S | Cross-domain | Unexpected combination from a completely unrelated field=10; borrowing from adjacent domain=8-9; within expected range=0-7 |

**Weight vectors** (determined by DEFAULT_PROFILE; say "score from a researcher's perspective" to switch at runtime)

- `learn`: D×0.35, N×0.25, R×0.2, U×0.1, WPS×0.1
- `solve`: U×0.45, R×0.3, D×0.1, N×0.1, WPS×0.05
- `scout`: W×0.25, P×0.2, N×0.2, S×0.15, R×0.15, U×0.05

Calculation: `total = R×wR + U×wU + N×wN + D×wD + (W+P+S)/3×wWPS`, rounded to one decimal.

---

## Personal Fit (F dimension)

Read `familiar_areas` and `dislikes` from config.yaml to assess how closely the article matches the user's specific tech stack.

**Scoring criteria:**

| F score | Meaning |
|---------|---------|
| 9-10 | Article's core technology/scenario directly overlaps with `familiar_areas` (e.g. user knows Agent frameworks, article is a concrete Agent implementation) |
| 7-8  | Related technical direction, but lower-level or requires some conversion cost (e.g. user builds LLM apps, article is about inference optimization) |
| 4-6  | Same broad AI domain but no direct intersection (e.g. user does app development, article is about speech recognition) |
| 1-3  | Almost no relation to user's tech stack (e.g. model pre-training, chip architecture) |
| 0    | Hits `dislikes` (pure marketing content, trend analysis with no code, etc.) |

**Final sort score (final_score):**

```
final_score = total × (0.7 + 0.3 × F/10)
```

- F=10: final_score = total × 1.0 (no boost or penalty)
- F=5:  final_score = total × 0.85
- F=0:  final_score = total × 0.7

> final_score is used for sorting only — never shown to the user. Card headers still display `total`.

---

## Action Tags

Determined automatically from article content and score — three levels:

| Tag | Meaning | When to use |
|-----|---------|-------------|
| `TRY` | Has code/tool/hands-on content | Contains GitHub repo, runnable example, or dataset download |
| `READ` | Recommended for full reading | Has methodology, paper, or deep analysis worth careful reading |
| `SCAN` | 30-second skim of title + abstract | News brief, trend overview, or low-score item |

**Decision rules:**
1. Article contains a GitHub link / code block / downloadable tool → `TRY` (regardless of score)
2. total ≥ 7 and no executable code → `READ`
3. Everything else → `SCAN`
