## Description:

Enforces a Human-in-the-Right-Loop lifecycle for remote agent tasks with plan approval, evidence-logged execution, and result sign-off gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toliuweijing](https://clawhub.ai/user/toliuweijing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they need structured human oversight for remote agent work, including approval before execution and explicit sign-off before task closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task journals are persisted in Draft pages and may be published for review.

Mitigation: Avoid including secrets, tokens, sensitive personal data, or raw command output in plans, logs, and result summaries.

Risk: The skill depends on an external, unpinned draft-cli installation.

Mitigation: Use a pinned or otherwise verified draft-cli dependency in higher-risk environments.

Risk: Approval gates can be bypassed if the agent proceeds without explicit chat confirmation.

Mitigation: Require approval and sign-off phrases in chat before moving between planning, execution, and closure phases.

## Reference(s):

- [Draft Agent Loop on ClawHub](https://clawhub.ai/toliuweijing/skills/draft-agent-loop)
- [draft-cli dependency on ClawHub](https://clawhub.ai/toliuweijing/draft-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and task-journal templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the draft CLI and may use GLOBAL_INVITE_CODE for publishing Draft pages.]

## Skill Version(s):

1.6.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
