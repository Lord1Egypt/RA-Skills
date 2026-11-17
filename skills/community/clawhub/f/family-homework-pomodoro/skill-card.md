## Description:

Parent-confirmed homework intake, Pomodoro execution, nightly completion checks, and reward approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoma970](https://clawhub.ai/user/guoma970)

### License/Terms of Use:

MIT-0

## Use Case:

External users and families can use this skill to coordinate same-day homework intake, parent-approved start times, Pomodoro reminders, nightly completion checks, and reward approval without adding private household details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private family, school, account, health, or minor-identifying details could be entered into a generic public homework workflow.

Mitigation: Keep all homework examples and customization inputs generic; do not include real names, school names, account identifiers, health details, or private household schedules.

Risk: The assistant could overstep parent authority by choosing start times, declaring completion, or granting rewards.

Mitigation: Require parent confirmation for start times, completion status, follow-up decisions, and any reward approval before child-facing messages are sent.

Risk: Missing homework details could lead to invented deadlines, page numbers, signatures, or teacher instructions.

Mitigation: Record homework exactly as provided and ask a short clarification question when key details are missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoma970/skills/family-homework-pomodoro)
- [README](artifact/README.md)
- [Examples](artifact/EXAMPLES.md)
- [Customization Guide](artifact/CUSTOMIZATION.md)
- [Release 1.0.1](artifact/releases/1.0.1.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown-style conversational guidance and short reminder text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only skill; no tools, credentials, or MCP integrations were detected in the provided evidence.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, CHANGELOG, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
