## Description: <br>
Agent Message Bridge helps Python-based agents exchange JSON messages through a local file-backed inbox. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bojin-clawflow](https://clawhub.ai/user/bojin-clawflow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let multiple Python agents send, check, and poll local messages without a human relay. It is intended for trusted local multi-agent workflows using a file-backed message queue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local file handling is under-scoped and can expose messages in the message directory. <br>
Mitigation: Use only in a trusted local environment, avoid secrets or regulated data, and restrict filesystem permissions on the message directory. <br>
Risk: Message handling can silently delete messages after reading. <br>
Mitigation: Review the delete-on-read behavior before deployment and configure or patch storage handling for workflows that require durable history. <br>
Risk: Agent names and storage paths may be unsafe for multi-agent workflows without additional validation. <br>
Mitigation: Patch or configure storage paths and agent-name validation before relying on this skill across multiple agents. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bojin-clawflow/agent-message-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime messages are JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local filesystem storage for agent inboxes and outboxes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
