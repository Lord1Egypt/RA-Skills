## Description:

Invokes ChatDev ability units through a local API so an agent can browse, inspect, run, upload, and manage multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[na-wen](https://clawhub.ai/user/na-wen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent operate ChatDev 2.0 ability units through the local API for tasks such as paper review, data visualization, and custom multi-agent workflow execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can administer a local ChatDev backend, including deleting workflows and overwriting executable local tool files.

Mitigation: Require explicit approval before upload, update, rename, copy, delete, output-directory moves, and local tool create or overwrite actions.

Risk: Hot-update endpoints can change executable Python tool files.

Mitigation: Use the hot-update endpoint only after reviewing the exact filename and Python code and confirming a rollback path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/na-wen/skills/chatdev)
- [Publisher profile](https://clawhub.ai/user/na-wen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payloads, and YAML workflow templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return ChatDev final_message text and move generated output directories into the workspace when workflows produce artifacts.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
