## Description:

Guides read-only comparison of external skill packages to identify gaps and improve an agent's own skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

All rights reserved (documentation and theory; MIT applies only to .py files, none included)

## Use Case:

Developers and skill authors compare external skill packages against their own to identify structural and metadata gaps and propose improvements without installing or copying the source skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants file-writing authority despite describing its workflow as read-only.

Mitigation: Remove Write permission or restrict edits to changes explicitly approved by the user before installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/agent-learn-external-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown comparison and improvement recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only gap list; does not install or reproduce external skills.]

## Skill Version(s):

1.0.3 (source: server-resolved release; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
