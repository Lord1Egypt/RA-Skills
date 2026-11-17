## Description:

Agent Advisor recommends Claude models from either recent OpenClaw conversation history or a task description, and can report an OpenClaw gateway security score from local configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrkangzubin](https://clawhub.ai/user/mrkangzubin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to choose a Claude model for a described or recently observed task and to review basic OpenClaw gateway security posture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto mode can analyze recent local OpenClaw conversation history.

Mitigation: Use recommend mode with an explicit task description when prior chat content should not be read.

Risk: Security reporting reads local OpenClaw configuration to score gateway posture.

Mitigation: Review local OpenClaw configuration access before running the security or full report modes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrkangzubin/skills/agent-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Markdown-style terminal report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include model recommendations, matched task signals, configured-model availability notes, OpenClaw security score details, and configuration improvement guidance.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
