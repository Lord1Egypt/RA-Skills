## Description:

TKSeller helps users run an AI-assisted short-video commerce workflow that logs in to a SaaS service, recommends or analyzes videos, presents review cards, and drives approval, generation, and publishing steps through Discord or webchat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanholt921](https://clawhub.ai/user/evanholt921)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub and OpenClaw users use this skill to connect a TKSeller SaaS account, review recommended short-video commerce opportunities, approve content workflow steps, and publish through chat-based controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles user passwords and stores a reusable SaaS token locally while the configured service endpoint uses HTTP.

Mitigation: Do not enter real passwords until the service uses HTTPS or a safer OAuth/device-login flow and stores tokens securely.

Risk: The skill can use OpenClaw messaging or gateway credentials and chat action buttons for commerce workflow decisions.

Mitigation: Restrict the skill to authorized users and channels, verify button actors where possible, and review commerce decisions before approval or publishing.

Risk: The workflow can keep a background poller running after a recommendation or action starts.

Mitigation: Use clear start and stop controls, and confirm polling stops when the workflow completes, the token expires, or the user pauses work.

## Reference(s):

- [TKSeller ClawHub listing](https://clawhub.ai/evanholt921/skills/clawshop-pro)
- [OpenClaw Discord channel documentation](https://docs.openclaw.ai/channels/discord)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chat text, Discord or webchat review cards, JSON status, and shell command invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream chat and command outputs; background polling may continue after start until workflow completion or stop conditions.]

## Skill Version(s):

3.3.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
