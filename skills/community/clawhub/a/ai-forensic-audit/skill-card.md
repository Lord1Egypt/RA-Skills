## Description:

Reviews user-supplied materials about AI-generated content, agent behavior, or conversations and produces a structured audit report with an evidence chain, cross-checks, confidence level, risks, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams can use the skill to review supplied AI content, agent activity, or conversation records for provenance, compliance, or leak-tracing questions. It organizes available evidence, checks for consistency, and reports supported conclusions and follow-up recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic trigger words may activate the skill for unrelated requests.

Mitigation: Use it for a clearly defined audit and confirm that the request matches its intended scope.

Risk: Audit materials may include credentials or unnecessary personal information.

Mitigation: Provide only relevant materials and remove credentials and unnecessary personal information from logs.

Risk: Reports may be mistaken for certified attribution or regulatory approval; references to standards alone do not demonstrate technical verification.

Mitigation: Treat reports as evidence-based assistance, not certification or regulatory approval, and seek qualified review when a formal determination is needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-forensic-audit)
- [Publisher homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [Formal paper linked in the skill materials](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Structured Markdown audit report with an evidence list, verification matrix, confidence level, risks, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-based conclusions; includes an audit date and supporting references when available.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
