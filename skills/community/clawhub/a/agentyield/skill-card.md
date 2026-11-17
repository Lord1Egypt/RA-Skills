## Description:

Automatic waste detection and cost optimization for every LLM and tool call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philg](https://clawhub.ai/user/philg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to add an observability layer to OpenClaw sessions that reports redacted LLM and tool-call telemetry for cost and waste analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session telemetry leaves the local environment and is sent to AgentYield, including model names, token counts, costs, tool names, timestamps, purpose tags, and salted tool-input hashes.

Mitigation: Review the disclosed telemetry categories before installation and use an ay_test_ API key for evaluation when persistence is not desired.

Risk: The required AGENTYIELD_API_KEY is a bearer credential scoped to an AgentYield user account.

Mitigation: Provide the key only through the AGENTYIELD_API_KEY environment variable, prefer test keys for evaluation, and revoke unused keys from the AgentYield settings page.

Risk: Tool-input hashes can still support repeat detection within a run.

Mitigation: Use the skill's local per-tenant salt behavior and confirm that raw tool inputs, raw outputs, and salt material are not transmitted.

## Reference(s):

- [AgentYield homepage](https://agentyield.co)
- [AgentYield public skill source](https://agentyield.co/skills/agentyield.md)
- [AgentYield developer SDK reference](https://agentyield.co/developer/sdk)
- [AgentYield privacy and retention](https://agentyield.co/privacy)
- [AgentYield data deletion documentation](https://agentyield.co/docs#data-deletion)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, text]

**Output Format:** [Markdown instructions with structured JSON telemetry examples and HTTPS API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTYIELD_API_KEY and sends bounded, redacted checkpoint telemetry to AgentYield.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 0.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
