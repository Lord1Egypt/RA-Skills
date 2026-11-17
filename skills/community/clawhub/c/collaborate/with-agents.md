# Agent Counterparts — Exchanges Between Model Instances

Two agent instances built from the same model and fed the same context are one mind sampled twice: asking the second instance is asking yourself with ceremony. Independence must be constructed — it never comes free from running the question again.

## Constructing Independence

Independence comes from varying, in order of power:

1. **Information** — give the counterpart the artifact and goal, NOT your chat history, reasoning, or discarded options. An agent that reads your reasoning continues it; an agent that reads only the artifact judges it. Blind first pass by default (`briefing.md` context dosing).
2. **Loss function** — assign the counter-role with its one-line loss function (`counterparts.md` catalog) and the one falsifiable question. Role labels without a loss function ("be a critical reviewer") produce criticism-flavored agreement.
3. **Model/prior** — a different model family, when available, brings genuinely different priors; reserve it for the attack round on high-stakes decisions. Same-model counterparts still work when 1 and 2 are done properly.

Run the exchange in a fresh session or isolated context — a counterpart inside your own context window has already read your mind.

## The Sycophancy Check

Run on the counterpart's first response, before engaging with its content:

- Opens by praising the plan, then offers only additive suggestions ("you could also...") → inherited your frame. Rebrief: loss function + kill question only.
- Agrees with your position while claiming to attack it ("one concern — though as you rightly note...") → same failure, softer costume.
- Pass condition: the response names at least one thing that is WRONG (would fail, observable how), not merely missing.

One rebrief attempt, same as any counterpart (`briefing.md` re-briefing); a second sycophantic pass means this setup cannot surprise you — change what you vary (different information, different model), or route the question to a human.

## Verify Before You Update

Agent critiques fabricate with full confidence: nonexistent API behaviors, misremembered defaults, invented failure modes. Every factual claim in the critique gets the same verification you would apply to your own claims BEFORE it moves your position. A confident false attack that you steelman and absorb is worse than no exchange — you retreated from a working design on fiction. Position movement (SKILL.md Rule 6) counts only on verified claims.

## One Strong Round Beats N Weak Opinions

Majority-voting several same-model instances measures the model's prior, not the truth — the errors are correlated, so agreement adds confidence without adding evidence. Budget accordingly: one counterpart with constructed independence and a real round structure (SKILL.md Running the Exchange) outperforms a poll of clones. Fanning out many genuinely different viewpoints before any is worth an exchange is divergence — route to `diverge`, then bring the strongest back here.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Pasting the whole conversation as context | Counterpart continues your reasoning instead of judging the artifact | Artifact + goal + constraints only |
| "Play devil's advocate" with no loss function | Produces generic objections against nothing in particular | One-line loss function + one falsifiable question |
| Treating agreement as validation | Correlated priors agree by construction | Only a survived ATTACK validates; agreement is absence of signal |
| Updating on unverified claims | Fabricated critique moves you off a working design | Verify facts first; movement counts on verified claims only |
| Endless agent-vs-agent rounds | No social cost, no fatigue — nothing stops it but you | Same `round_cap` (default 3) as every exchange |
