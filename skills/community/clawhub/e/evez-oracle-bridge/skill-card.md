## Description:

Routes LLM calls through a Vultr oracle instance using four EVEZ-branded model mappings and exposes OpenAI-compatible endpoints plus EVEZ-OS circuit integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route agent LLM requests through a Vultr-backed EVEZ oracle bridge and inspect or trigger connected EVEZ-OS services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated network endpoints can expose the bridge to unwanted callers.

Mitigation: Bind the service to localhost or place it behind strong authentication before network exposure.

Risk: Network callers can consume Vultr inference quota through the configured Vultr API key.

Mitigation: Treat VULTR_API_KEY as sensitive, restrict bridge access, and monitor inference usage.

Risk: Bridge routes can invoke local EVEZ-OS service actions.

Mitigation: Run the bridge only where those local services are intended to be reachable, and limit access to trusted operators.

## Reference(s):

- [EVEZ Oracle Bridge on ClawHub](https://clawhub.ai/evezart/skills/evez-oracle-bridge)
- [Publisher profile: evezart](https://clawhub.ai/user/evezart)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint descriptions, Python bridge code, and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment-provided API credentials and can call Vultr Inference plus local EVEZ-OS services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
