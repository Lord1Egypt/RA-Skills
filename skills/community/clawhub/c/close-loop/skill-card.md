## Description:

End-of-session workflow for shipping changes, consolidating memory, applying self-improvements, and preparing publishable outputs with safety gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Close Loop to end coding sessions with repo state checks, gated shipping actions, structured memory consolidation, self-improvement triage, and a consolidated wrap-up report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrap-up flow can commit changes, move files, and write lasting agent memory or rules without strong per-action confirmation.

Mitigation: Use dry-run mode first, review proposed commits and file moves, and require explicit approval before memory/rule writes, pushes, deploys, or commits that could include unrelated or sensitive files.

## Reference(s):

- [Close Loop on ClawHub](https://clawhub.ai/clarezoe/skills/close-loop)
- [Memory Frameworks](references/memory-frameworks.md)
- [Wrap Report Template](assets/templates/wrap-report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report with an embedded machine-readable JSON block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run or execute mode, confidence labels, evidence sources, KPI fields, and gated follow-up commands.]

## Skill Version(s):

2.3.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
