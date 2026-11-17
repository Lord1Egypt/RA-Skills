# Research Notes

This skill isn't a folk list — it's built from a mix of academic work on LLM output patterns, published community research on de-sloppinng, and industry reporting on AI-assisted coding. This file records the key findings and sources so the lists in `prose-tells.md` and `code-slop.md` can be sanity-checked or updated later as models and detection methods change.

## Terminology

"Slop," in this sense, means low-effort or formulaic AI-generated content that's noticeably worse than what a careful human (or careful model) would produce for the same task — recurring vocabulary, structures, and shortcuts that appear because they were statistically convenient during training, not because they best serve the specific content. The term picked up mainstream usage broadly enough to be recognized as a notable word of the era, alongside more technical use in the LLM research community for the specific phenomenon of repetitive pattern over-representation.

## Why slop patterns exist (mechanism, not just symptom)

Two separate mechanisms produce most of what this skill targets, and they're worth distinguishing because they call for different fixes:

1. **Training-data over-representation.** Certain words and phrases ("delve," formal academic hedges) are statistically common in the higher-quality/formal text that gets weighted heavily during training (academic papers, edited prose), so the model learned they're a "safe," high-probability choice for exploratory or explanatory contexts — and now over-uses them relative to how often actual humans reach for them in ordinary writing. A 2025 framework (Paech, Roush, Goldfeder, Shwartz-Ziv — "Antislop," accepted ICLR 2026) quantified this directly: some patterns appear vastly more often — the paper reports some phrases occurring on the order of 1,000× more frequently — in LLM output than in a comparable human-written baseline.

2. **RLHF / preference-model bias.** Separately from vocabulary, *formatting and structural* habits (bullet lists, bold text, emoji, hedge-everything caution, validating openers) are reinforced because human raters and reward models measurably prefer them at the surface level, independent of underlying content quality. A 2024 paper, *From Lists to Emojis: How Format Bias Affects Model Alignment* (Zhang, Xiong, Zhang et al.), found this bias present across human evaluators, GPT-4-as-judge, and top public reward models, and showed the bias is exploitable: format-optimized output can inflate benchmark scores without real quality gains. This is the mechanistic explanation for the widely reported "wall of bullets for a one-sentence question" complaint about modern chat assistants.

Sycophancy compounds both: a 2026 study on LLM behavior in creative-writing collaboration found validating/hedging behavior in a large majority of sampled interactions, describing it as "nearly ubiquitous" and calling out the tension between safety-alignment training and genuine collaborative pushback.

## Why word-banning alone doesn't work

This is the single most important design constraint behind how this skill is written, so it's worth spelling out the chain of evidence:

- The "Pink Elephant Problem" (Castricato, Lile, Anand, Schoelkopf, Verma, Biderman — *Suppressing Pink Elephants with Direct Principle Feedback*, 2024) documented that instructing a model not to mention a topic often paradoxically increases the odds it comes up, because negative constraints require representing the very concept they're trying to suppress.
- The Antislop paper cites this directly as the reason a pure prompt-level "don't use these words" instruction has limited efficacy, and builds a decoding-time solution instead — the Antislop Sampler backtracks and suppresses a pattern only *after* it starts to appear, rather than trying to pre-emptively censor the model's vocabulary. It also found plain token banning becomes unusable past roughly 2,000 banned strings (destroys fluency/collateral-damages unrelated words that share a token prefix), while their backtracking approach scaled to 8,000+ suppressed patterns without the same degradation.
- Independent practitioner writing on prompt design converges on the same practical conclusion from a different angle: a negative instruction ("don't be verbose") doesn't narrow the model's choices the way a positive target ("answer in under 80 words") does, because the negative leaves every alternative on the table and the model still has to guess which one you meant.

**Practical takeaway baked into this skill:** don't ask a drafting pass to avoid a list of words. Draft freely, then run a dedicated, positively-framed editing pass against concrete patterns already present in the text. This is strictly easier and more reliable than real-time avoidance, for the same reason it's easier to edit a sentence you can see than to avoid writing an unknown one in advance.

## Code slop: supporting data

- GitClear's large-scale analysis of changed lines across many repositories found code duplication increasing sharply and refactoring's share of all changes dropping as AI-assisted coding tools became mainstream — consistent with models defaulting to copy-and-extend rather than restructuring.
- A Carnegie Mellon study tracking real repositories after teams adopted AI coding tools found an initial 3-5x jump in lines changed, alongside static-analysis warnings up roughly 30% and code complexity up over 40% — and found the velocity gains faded after about two months while the added complexity did not.
- CodeRabbit's analysis of several hundred pull requests found AI-assisted PRs carrying meaningfully more flagged issues on average than human-authored ones.
- Industry write-ups (Aviator, TraycerAI, and others building AI-code review tooling) converge on the same taxonomy used in `code-slop.md`: plausible-but-wrong logic, over-engineered abstractions, convention-blindness, hallucinated API calls, and defensive-programming excess (over-broad try/catch, excessive logging) as the recurring, reviewable categories — distinct from outright bugs, which existing tests and linters already catch.
- Academic surveys of AI-generated code hallucination converge on training/context limitations (poor handling of private/repo-specific APIs, limited cross-file understanding, evaluation benchmarks that don't reflect real repo-level tasks) as root causes — which is the basis for this skill's recommendation to verify unfamiliar API surfaces rather than trust recall, especially for less common or fast-moving libraries.

## Maintenance note

Word-level slop lists have a shelf life — as this becomes common knowledge, deliberate avoidance of the most obvious tier-1 words is already visible in some current-generation model output, and new tells will emerge as training and RLHF processes evolve. The structural and mechanistic sections of this file (why word-banning fails, why formatting bias exists, the two-pass editing philosophy) are far more durable than any specific word list and should be weighted more heavily if the two ever seem to conflict. If revisiting this skill, a web search for recent "AI slop" / "LLM tells" writing is worth doing before assuming the existing lists are current — this is an actively evolving area with new community-compiled lists appearing frequently.
