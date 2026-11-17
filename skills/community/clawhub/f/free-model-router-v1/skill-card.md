## Description:

Provides OpenClaw with a local free-model routing proxy for provider setup, automatic polling, failover, model switching, and availability diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laodao-agent](https://clawhub.ai/user/laodao-agent)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to configure a local router that selects available free model providers, switches models, and diagnoses provider availability issues. It is intended for users who are comfortable running a persistent local proxy and reviewing provider data handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a persistent local router and stores provider API keys.

Mitigation: Install only when the local router is needed, keep provider keys scoped and revocable, and stop or uninstall the router when it is no longer in use.

Risk: The local admin surface may expose keys or high-impact controls too broadly.

Mitigation: Treat the admin UI as sensitive and avoid running the router while browsing untrusted sites until the local admin and CORS behavior has been reviewed and fixed.

Risk: The skill communicates with freemodel control servers for registration, provider metadata, and health reporting.

Mitigation: Review the configured control-server communication and leave optional health reporting disabled unless the user intentionally enables it.

Risk: Displayed curl-to-shell update commands can increase execution risk.

Mitigation: Avoid curl-to-shell updates; inspect downloaded update content and run explicit commands from trusted release artifacts instead.

Risk: Scheduled tasks may remain after uninstall.

Mitigation: After uninstalling, verify and remove any remaining scheduled tasks associated with free-model-router.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laodao-agent/skills/free-model-router-v1)
- [Publisher Profile](https://clawhub.ai/user/laodao-agent)
- [Setup Guide](references/setup-guide.md)
- [Event System](references/event-system.md)
- [Idempotency Guide](references/idempotency.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct the agent to run Node.js CLI commands, configure OpenClaw provider settings, and report router or provider status.]

## Skill Version(s):

2.2.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
