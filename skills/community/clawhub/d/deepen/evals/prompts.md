# /deepen eval prompts

Per skill-eval best practice: ≥5 positive + 2–3 negative trigger prompts; target ≥90% correct firing.

## Positive — the skill SHOULD trigger
1. "build genuine expertise in <topic>"
2. "/deepen <topic>"
3. "go deep on <topic> and take defensible positions on the open debates"
4. "become an expert on <topic> and start a knowledge base I can grow"
5. "research <topic> to mastery — weight the real experts, not the loud ones"
6. "what's actually true vs contested in <topic>, with your stance?"

## Negative — the skill should NOT trigger (guards against false positives)
1. "what's the capital of France?"  (simple fact lookup)
2. "summarize this email for me"  (one-off transform)
3. "fix the bug in this function"  (coding task)
4. "what time is my next meeting?"  (logistics)

## Capability ablation topics (matched skill-on vs skill-off)
Pick a compact, contestable topic so both arms are cheap to run and a stance is possible:
- "Pomodoro Technique — does it actually improve productivity?"
- "standing desks — health and productivity evidence"
- "spaced repetition — is it universally effective?"

## Targeted regression scenarios
- **Reconcile/retrieval (step 0):** point the skill at a topic where a *related* note exists under a
  *different vocabulary*. PASS = it finds and cross-links the related note instead of forking a duplicate KB.
- **Debiased judging (step 4.5):** a run with ≥2 competing claims. PASS = the skeptic cites external evidence
  (not "let me reconsider") and judging isn't a model grading only its own output.
- **Single-writer (step 2):** a deep-pass run. PASS = research fans out, but KB writes are single-threaded.
