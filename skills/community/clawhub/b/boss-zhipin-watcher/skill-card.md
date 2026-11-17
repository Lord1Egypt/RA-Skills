## Description:

Boss Zhipin Watcher helps an agent find and capture BOSS Zhipin desktop windows, inspect screenshots, and support recruiting workflows such as chat review, candidate screening, greetings, resume handling, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxj20060702-del](https://clawhub.ai/user/lxj20060702-del)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and operators use this skill to inspect BOSS Zhipin desktop activity, capture local window screenshots and metadata, and run guided recruiting workflows. It can also help an agent prepare or execute scripted actions such as opening chats, sending recruiting messages, collecting resumes, and producing daily recruiting status output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review states that this skill can automate recruiting actions, messages, screenshots, and local data storage more broadly than a simple BOSS window screenshot helper.

Mitigation: Review carefully before installing, use only when the operator explicitly wants an agent to control a BOSS account, and require confirmation before every outbound message or resume action.

Risk: The skill can capture candidate screens and store local recruiting records.

Mitigation: Apply retention and redaction rules for captured candidate data, and prefer a narrower screenshot-only workflow when full recruiting automation is not required.

Risk: Desktop automation can click, scroll, type, and send messages in a live recruiting account.

Mitigation: Keep PyAutoGUI fail-safe enabled and stop for user confirmation when page detection or action verification is uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxj20060702-del/skills/boss-zhipin-watcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, local file paths, workflow configuration, screenshots, and JSON metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local captures, workflow state records, candidate-related screenshots, and structured metadata files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
