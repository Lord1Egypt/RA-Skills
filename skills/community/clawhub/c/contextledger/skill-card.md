## Description:

ContextLedger is an evidence-first knowledge auditing skill that turns notes, documents, research, or connector outputs into an auditable conclusion card with source traceability, freshness judgment, conflict flags, evidence grading, and a best current judgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, analysts, and knowledge workers use this skill to audit claims across provided notes, reports, meeting summaries, research outputs, or connector results. It helps identify supporting sources, stale or undated evidence, source conflicts, inference boundaries, and the most reliable next judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used on stale, undated, conflicting, or thin evidence where overconfident conclusions would mislead the user.

Mitigation: Label undated or thin evidence plainly, preserve material conflicts, lower the strength of the judgment, and recommend the single best next verification step.

Risk: The skill can process notes, reports, meeting summaries, and connector outputs that may contain sensitive or untrusted content.

Mitigation: Use only documents the user intentionally provides or connector outputs the user trusts, and keep provenance and evidence boundaries visible in the output.

## Reference(s):

- [Audit Heuristics](references/audit-heuristics.md)
- [Conclusion Cards](references/conclusion-cards.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/contextledger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown audit card with source ledger, freshness signal, conflict notes, evidence-versus-inference split, and next step]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-oriented default response style; no required binaries or external tools.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, clawhub.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
