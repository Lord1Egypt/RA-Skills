# Skill Review Rubric · 技能审查度量尺

This is the measurable bar for "全球最牛逼" (globally best). Use it in two situations:
1. **Review mode** — audit ANY skill (someone else's, or a skill you just forged) before declaring it done.
2. **Meta self-audit** — apply it to skill-forge itself to prove the meta-skill practices what it preaches.

A skill is NOT "best" because it feels thorough. It is "best" only when it scores in the Global-Best band on this rubric AND has survived an external benchmark + a live-test.

## Scoring model
- Each dimension scored **0–5** (0 = absent, 3 = acceptable, 5 = exemplary).
- Weighted to a **0–100** total: `total = Σ (score/5 × weight%)`.
- Be honest. A 5 means "truly best-in-class with evidence", not "I wrote something about it".

## Dimensions

| # | Dimension | Weight | What a 5 looks like |
|---|-----------|--------|---------------------|
| D1 | **Trigger precision** | 15% | Description is a sharp "when-to-use" trigger (not a what-is); correct `allowed-tools`/`recommends`; zero false-trigger; the agent finds it reliably. |
| D2 | **Scope discipline** | 10% | Explicitly states when NOT to use a skill / when a plain prompt suffices; no overreach beyond its mandate. |
| D3 | **Token efficiency / progressive disclosure** | 12% | SKILL.md lean (<500 lines, <5k words); all detail pushed to `references/`; loads only what's needed. |
| D4 | **Coverage completeness** | 13% | Audited against the domain's standard taxonomy; blank branches named honestly; gaps listed with REAL material ids (no fabrication). |
| D5 | **Evidence integrity** | 12% | Every cited source has a REAL, fetchable id; confidence bound to evidence; zero hallucinated ISBN/DOI/id. |
| D6 | **Differentiation** | 8% | Not a generic prompt; has a unique angle (voice / method / structure) that a vanilla LLM lacks. |
| D7 | **Verification** | 10% | Ran 2–3 real questions (or a small eval harness); when target users are unreachable, ran **community-sourced real questions** (see `simulation-testing.md`) across every trigger class; design proven to help. |
| D8 | **Robustness** | 8% | Edge cases, failure modes, and red lines documented; degrades gracefully. |
| D9 | **Maintainability** | 7% | Versioned (SemVer); iteration/changelog log; references structured & reusable; ships a **non-intrusive in-the-wild feedback loop** (see `feedback-loop.md`) so it keeps improving after launch. |
| D10 | **Reviewability** | 5% | The skill can itself be reviewed/critiqued; ships with or invites a self-audit. |

## Classification bands
- **< 50 — Thin**: rewrite. A "folder with a prompt".
- **50–69 — Solid**: usable, real gaps; iterate before shipping wide.
- **70–84 — Excellent**: strong; one or two weak dims to shore up.
- **85–100 — Global-Best candidate**: must ALSO have (a) an external benchmark vs the top **globally-found** public skills / papers / tools / knowledge (全网扫描所得，不得仅限某比赛/平台), and (b) a passing live-test. Without both, cap at 84 regardless of score.

## Review report template
```
# Review: <skill-name> v<ver>
## Verdict: <band> (score X/100)
## Dimension scores
D1 Trigger .... X/5 | D2 Scope ..... X/5 | D3 Tokens .... X/5
D4 Coverage ... X/5 | D5 Evidence .. X/5 | D6 Diff ...... X/5
D7 Verify ..... X/5 | D8 Robust .... X/5 | D9 Maint ..... X/5
D10 Review .... X/5
## Strengths (keep)
- ...
## Gaps (fix)
- [P0] <dim>: <concrete gap> → <fix>
- [P1] <dim>: ...
- [P2] <dim>: ...
## Benchmark note (required for Global-Best)
- Compared against: <ALL globally-findable public skills / repos / papers / tools / knowledge（全网，不得仅限某场比赛或某平台）>
- Differentiation retained: <what we keep that they lack>
```

## Red lines for the reviewer
- Never inflate a score to please the author. A 68 that says "Solid" is more useful than a 90 that lies.
- If you cannot verify a cited id, mark D5 down — do not assume.
- A skill that fails D5 (fabricated evidence) cannot exceed 69 no matter how pretty.
