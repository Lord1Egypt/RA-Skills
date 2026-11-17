## Description:

Based on user goals, this skill evaluates candidate skill capabilities and conflict risks with installed skills, then delivers the best install recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaowh3613](https://clawhub.ai/user/zhaowh3613)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to compare candidate ClawHub skills against their goals and installed skill set, decide whether to replace or coexist with existing skills, and execute installs only after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A replacement or uninstall recommendation could affect security-critical or workflow-critical skills.

Mitigation: Before approving actions, review the exact skill names, versions, source, risk signals, and proposed uninstall.

Risk: Installing or uninstalling skills changes the local ClawHub skill set.

Mitigation: Require explicit user confirmation at the pre-install gate before any install or uninstall command runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaowh3613/skills/best-skill-recommendations)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zhaowh3613)
- [Author Profile](https://x.com/zhaowh3613)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown summaries with inline shell commands and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose install or uninstall commands, but execution is gated on explicit user confirmation.]

## Skill Version(s):

0.2.2 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
