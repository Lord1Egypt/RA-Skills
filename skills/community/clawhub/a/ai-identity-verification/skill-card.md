## Description:

AI identity verification and provenance skill that applies the Three-Anchor-One-Vote method across account, behavior, and memory evidence to produce a Level 1-4 trust conclusion and evidence chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, auditors, and teams use this skill to assess whether AI conversations, agents, or generated content appear to come from the same AI identity or provenance chain. It structures user-provided evidence into account, behavior, and memory anchors, then reports a trust level, confidence, contradictions, and recommended follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to provide account, behavior, memory, or provenance details that could be sensitive.

Mitigation: Use only information the user is comfortable sharing, minimize personal or regulated data, and require human review for medical, legal, financial, or other sensitive contexts.

Risk: Identity and provenance conclusions are probabilistic and may be mistaken when evidence is incomplete or conflicting.

Mitigation: Report confidence, contradictions, and missing evidence clearly, and avoid treating Level 1-4 outputs as absolute proof.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-identity-verification)
- [ClawHub publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with trust level, evidence chain, contradictions, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only user-provided identity, behavior, memory, or provenance evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
