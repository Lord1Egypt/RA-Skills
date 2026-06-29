# /deepen eval rubric

Score a run's output (or the KB it produced) against the skill's own promises. Each criterion 0/1/2
(absent / partial / full). A skill-OFF baseline ("just research X and brief me") typically scores low on
1–3, 5–6 — that gap is the skill's value.

| # | Criterion | 2 = full | 0 = absent |
|---|---|---|---|
| 1 | **Falsifiable stance** | Takes ≥1 position with calibrated confidence **and an explicit falsifier** | "both sides have merit" / no position |
| 2 | **Cite-or-flag** | Every claim cites a source or is tagged `[inference]`/`[convention]` | bare assertions presented as fact |
| 3 | **Track-record weighting** | Sources ranked by checkable record (proxy ladder); names loud-but-wrong consensus | ranked by fame / not ranked |
| 4 | **Adversarial gate** | Stances carry a survived-refutation note (skeptic used external evidence) | no red-team |
| 5 | **Honest thin spots** | States confidence levels + flags weak/unverified areas | uniform false confidence |
| 6 | **Context-tuned tactics** | Ranked, concrete, applied to your actual context | generic field advice |
| 7 | **Structure** | KB files (`_map` w/ depth dashboard, principles+misconceptions, experts, disagreements, tactics, changelog) or the 5-part brief | prose dump |

**Total /14.** Pass ≥ 11. Capability evals start low and climb; once skill-on is consistently ≥11 it becomes
a **regression** guard. Record solution-quality + (optionally) cost/runtime per the eval best practice.
