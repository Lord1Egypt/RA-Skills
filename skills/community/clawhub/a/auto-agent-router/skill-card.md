## Description:

Routes command-prefixed DingTalk/OpenClaw messages to configured specialist sub-agents such as coder, writer, analyst, researcher, reviewer, or devops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill in OpenClaw and DingTalk workflows to parse command-prefixed messages, delegate substantial tasks to configured specialist sub-agents, and leave simple or unrecognized messages in the main session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic routing may inspect group messages and delegate chat content unexpectedly.

Mitigation: Disable automatic keyword routing unless explicitly desired, and require clear command triggers or user confirmation before delegation.

Risk: Sensitive requests may be routed to high-impact agents such as devops or researcher.

Mitigation: Restrict the allowed agent set and require confirmation before invoking sensitive routes.

Risk: Message-derived data may be retained in /tmp logs with weak retention or redaction controls.

Mitigation: Move logs to a controlled location, redact sensitive content, and define retention limits before deployment.

Risk: Automatic bot-name learning may persist newly observed identifiers.

Mitigation: Turn off automatic bot-name learning or review learned names before saving them to configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/skills/auto-agent-router)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown-style status text, JSON result objects, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes recognized command prefixes and configured keyword or length rules; logs may be written to /tmp/auto-route-handler.log.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
