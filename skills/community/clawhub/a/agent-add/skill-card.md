## Description:

Creates new OpenClaw agents by guiding setup questions, running OpenClaw registration, initializing a workspace, and recording the creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyangupday](https://clawhub.ai/user/yangyangupday)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to create a new agent through a guided question flow, register it with OpenClaw, initialize workspace documents, and update identity and persona files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy private main-agent workspace files into a new agent workspace without redaction or clear isolation controls.

Mitigation: Review the source workspace before installation and use; prefer clean packaged templates and confirm before copying existing workspace files.

Risk: The skill writes files, modifies OpenClaw configuration, and appends creation records during agent setup.

Mitigation: Review the summarized target path and generated document list before execution, and back up important workspaces before creating a new agent.

## Reference(s):

- [Agent Add ClawHub page](https://clawhub.ai/yangyangupday/skills/agent-add)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides interactive agent setup and may execute OpenClaw commands that create or modify local workspace files.]

## Skill Version(s):

1.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
