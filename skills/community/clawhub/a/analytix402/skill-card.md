## Description:

Analytix402 monitors and controls an OpenClaw agent's API spend and LLM costs with real-time tracking, budget limits, duplicate purchase detection, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[analytix402](https://clawhub.ai/user/analytix402)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to add spend observability and budget guardrails to OpenClaw agents that make API calls, LLM requests, or x402 payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad automatic tracking of API calls, LLM usage, payment-related events, and health heartbeats to Analytix402 or a configured base URL.

Mitigation: Confirm what telemetry fields are collected, whether prompts or request payloads are included, who can access dashboard data, and how tracking can be disabled before enabling the skill.

Risk: The server security verdict is suspicious because user control over external spend telemetry is not clearly defined.

Mitigation: Use a reviewed configuration, restrict the base URL to a trusted endpoint, and validate privacy and retention expectations before deployment.

## Reference(s):

- [Analytix402 Skill Page](https://clawhub.ai/analytix402/skills/analytix402)
- [Analytix402 Publisher Profile](https://clawhub.ai/user/analytix402)
- [Analytix402 Dashboard](https://analytix402.com)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown]

**Output Format:** [Markdown with YAML configuration examples and tool usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe spend reports, budget settings, budget checks, and purchase review flags.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
