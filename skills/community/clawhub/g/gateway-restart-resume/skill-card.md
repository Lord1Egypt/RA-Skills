## Description:

Use when an OpenClaw gateway-backed agent is asked through Discord, Slack, Matrix, SMS, web chat, CLI relay, ACP, cron, or another channel to restart, stop, reload, update, or repair the gateway and needs a durable post-restart callback, same-thread reply, recovery status, or lost follow-up prevention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udaymanish6](https://clawhub.ai/user/udaymanish6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to restart, reload, update, or repair a gateway-backed agent without losing the user-facing follow-up. It guides the agent to capture a minimal reply route, create a durable resume callback, verify recovery, and report status back to the original conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron callback examples include shell-style dynamic placeholders in a restart workflow.

Mitigation: Prefer a structured OpenClaw cron or task API, validate route identifiers, and avoid shell interpolation for callback payloads.

Risk: The skill assumes the installing environment intentionally grants gateway restart authority and one-shot callback capability.

Mitigation: Install only in environments where restart authority and durable resume callbacks are expected, reviewed, and operationally approved.

## Reference(s):

- [OpenClaw Cron Resume Pattern](references/openclaw-cron-resume.md)
- [ClawHub Skill Page](https://clawhub.ai/udaymanish6/skills/gateway-restart-resume)
- [ClawHub Publisher Profile](https://clawhub.ai/user/udaymanish6)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline text, JSON examples, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operator-facing restart and recovery status guidance; it does not restart OpenClaw by itself.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
