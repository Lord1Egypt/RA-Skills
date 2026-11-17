## Description:

Fast Fact-Check helps an agent quickly verify factual questions or claims with bounded web search, source corroboration, confidence labels, and citation-backed bottom-line answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill when they need a quick fact check for a factual question or claim. It triages simple versus complex questions, searches in parallel, and returns a citation-backed BLUF answer with confidence and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local validator checks citation structure, not whether each citation semantically proves the claim.

Mitigation: Review answers for source quality and ensure every load-bearing claim is supported by the cited source.

Risk: Fast web verification can rely on stale or weak sources for volatile facts.

Mitigation: Use recent dated sources for current facts, apply the source-reliability guidance, and lower confidence or add caveats when evidence is thin.

Risk: A hard time budget can leave contested or under-corroborated claims unresolved.

Mitigation: Use the complex or uncertain tier when needed and report Low confidence rather than guessing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vincentjiang06/skills/fast-fact-check)
- [Triage: simple vs complex, and the per-tier budget](rules/triage.md)
- [Search protocol: parallel, snippet-first, early-exit](rules/search-protocol.md)
- [Output contract: bottom-line-up-front, every claim cited](rules/output-contract.md)
- [Source reliability and freshness](references/source-reliability.md)
- [Metrics](references/metrics.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown answer with confidence, tier, key evidence, sources, and optional caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional local Node validator checks answer structure and citation resolution.]

## Skill Version(s):

0.1.0 (source: server release metadata and CHANGELOG, released 2026-06-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
