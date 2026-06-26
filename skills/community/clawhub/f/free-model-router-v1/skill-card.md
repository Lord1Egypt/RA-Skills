## Description: <br>
Provides an OpenClaw local model router for configuring providers, routing free model traffic, rotating models, failing over, and diagnosing model availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laodao-agent](https://clawhub.ai/user/laodao-agent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up a localhost router, configure model providers, switch primary or fallback models, and recover from provider or model outages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laodao-agent/free-model-router-v1) <br>
- [Setup guide](references/setup-guide.md) <br>
- [Event system](references/event-system.md) <br>
- [Idempotency guide](references/idempotency.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security posture: suspicious. Review the persistent localhost router, OpenClaw config modification, local provider key storage, freemodel server communication, and admin update surface before installation; keep the router bound to 127.0.0.1, avoid proxy or tunnel exposure, and leave reporting disabled unless explicitly needed.] <br>

## Skill Version(s): <br>
1.5.3 (source: evidence release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
