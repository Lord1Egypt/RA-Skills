## Description:

Team coordination layer for multi-agent workflows with mailbox, task board, and lease-based task management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femto](https://clawhub.ai/user/femto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI workflow operators use Acp Team to coordinate multiple agent sessions with shared task boards, mailbox-style messaging, task assignment, and lease-based task claiming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global npm installs may change behavior between installs.

Mitigation: Review the npm packages and consider pinned, project-local versions before use.

Risk: Initialization, task mutation, inbox-draining, and spawn commands can create persistent project state or launch additional agent sessions.

Mitigation: Run these commands only in projects where .team/ and .tasks/ state and additional agent sessions are acceptable.

## Reference(s):

- [Acp Team on ClawHub](https://clawhub.ai/femto/skills/acp-team)
- [acp-team npm package](https://www.npmjs.com/package/acp-team)
- [acpx GitHub repository](https://github.com/openclaw/acpx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .team/ and .tasks/ project state when suggested commands are executed.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
