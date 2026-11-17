## Description:

Reviews engineering documents by cross-checking them against code, related documents, facts, and documentation standards, then reports findings and suggested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation owners use this skill to review PRDs, designs, ADRs, runbooks, and related engineering documents. It produces a structured report with severity-ranked findings, cross-check records, and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The review instructions may allow last-verified metadata to change despite the report-only restriction.

Mitigation: Confirm whether metadata updates are authorized and require explicit approval before changing last-verified.

## Reference(s):

- [Document review checklist](references/checklists.md)
- [Source repository provenance](https://github.com/zengfr/document-governance-skills/tree/main/doc-reviewer)
- [ClawHub skill release](https://clawhub.ai/zengfr/skills/doc-reviewer)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Structured Markdown review report with findings, verification records, and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-ranked findings with locations and recommendations]

## Skill Version(s):

0.1.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
