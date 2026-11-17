# deep-research-discipline

An AgentSkill that describes **how to make research auditable**, not how to search harder.

Most "deep research" prompts optimize for volume: more queries, more pages, longer output. This one optimizes for a different property — every claim in the final report should be traceable, graded, and open to challenge after the fact.

It is a small engineering idea, published in case it is useful to someone else. No product, no service, no dependencies.
## Provenance

This skill was **produced and refined in agent operation**: drafted, exercised against real research tasks, corrected after failures, and re-validated by an AI agent, with human direction on scope and acceptance. It is not a hand-written prompt template.

The process rules exist because they were needed in practice — not because they read well. Where a rule was found to be wrong or too strict, it was revised; the report format and the review gate are the parts that survived repeated use.


## The three ideas

1. **Three evidence states.** Every material claim is `verified` (two independent sources, or one authoritative primary source), `single-source`, or `unresolved`. There is no unlabeled claim.
2. **Review is a blocking step.** A separate reviewer re-checks 3–5 core data points against primary sources without seeing the draft's conclusion first. If no independent reviewer exists, the report must say `not performed` — self-review cannot be presented as independent review.
3. **Degradation must be explicit.** If the environment lacks social sources, document extraction, or recency filters, the report says so in its limitations. Missing capability never turns into silence.

These are process constraints, not accuracy guarantees. The goal is that a reader can tell *which parts* of a report are solid and which are not.

## Quickstart

```
your-skills-dir/
└── deep-research-discipline/
    ├── SKILL.md
    └── references/
        └── adapters.md
```

Copy the directory into your agent's skills folder. No configuration, no keys, no install step.

Required capabilities are only: web search, page fetch, file read/write. If your agent has those three, the full workflow runs. Anything else — social sources, PDF extraction, date filters — is optional and degrades explicitly.

## What it produces

```
# <topic>
## One-line answer
## Key findings (3–5, each with evidence state)
## Key data (number, source, date)
## Conflicting or missing evidence
## Analysis (per sub-question, traceable)
## Limitations (capability gaps, paywalls, coverage)
## Independent review record (BLOCKING)
## References (URL + retrieval time)
```

Example of the labeling style:

```
- The default context window is 1,000,000 tokens. [verified: vendor docs, 2026-11-05; independent report, 2026-11-05]
- ACP initialisation fails on DSH 0.2.1 with bridge 0.1.3. [single-source: local reproduction, 2026-11-06]
- Whether the fix also covers Windows is unresolved. [unresolved: no source found; two queries tried]
```

## What this is not

- Not a search strategy library. It does not tell you which engines to use.
- Not a guarantee of correctness. It reduces the chance of unsupported claims; it cannot eliminate error.
- Not suitable for real-time values (prices, scores, incidents), private/internal data, or legal and medical advice.
- Not a substitute for domain expertise. Traceability is not judgment.

Known limits are listed in `SKILL.md` and must be repeated in each report's limitations section: paywalls and login walls, search index lag (absence of evidence is not evidence of absence), weak coverage of non-English and offline material, and secondary sources inheriting primary errors.

## Adapting to your environment

`references/adapters.md` describes four optional shapes — `search`, `fetch`, `extract_document`, `list_social` — in plain terms. Map your own tools to them; do not add vendor names, install commands, or local paths to the skill. If a shape is unavailable, mark the capability `no` and say what that costs the report.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The workflow: applicability, capability check, steps 1–7, degradation rules, self-check. |
| `references/adapters.md` | Optional interface shapes and the degradation table. Read only if you want richer coverage. |
| `examples/sample-report.md` | A sanitized worked example with evidence labels and a review record. |
| `benchmarks/` | A 10-case protocol and a partial run; no aggregate accuracy claim is made. |

## License

MIT. Use it, fork it, rewrite it. Attribution is appreciated but not required.
