## Description:

Compares the same task across AgentScope chat models, reporting latency, output length, and failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can compare how different chat models respond to a shared agent task and inspect basic performance and completion results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A DashScope API key can be routed through an OpenAI chat client for unrecognized model names.

Mitigation: Do not set a DashScope key until provider routing is fixed or unknown model names are rejected; rotate a key already used through this path.

Risk: The comparison sends task prompts to external model providers.

Mitigation: Use only low-sensitivity prompts; do not include secrets or proprietary content.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/trend0522/skills/agentscope-model-compare)
- [AgentScope project homepage](https://github.com/agentscope-ai/agentscope)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown summary printed to the terminal]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists elapsed time and output length per model, or a failure message; does not report token usage.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
