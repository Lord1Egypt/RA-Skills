## Description:

Track, analyze, and optimize AI API costs across OpenAI, Anthropic, OpenRouter, Google, and other LLM providers by parsing billing data, usage logs, or API responses into cost breakdowns, trends, budget alerts, and optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to analyze AI API spending from billing exports, usage logs, or provider API responses and to produce cost reports, budget checks, and optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing and usage exports may contain sensitive account, project, usage, or spending data.

Mitigation: Use trusted local exports, limit report sharing, and review generated outputs before redistribution.

Risk: Environment/API-key based access can query provider account data when explicitly enabled.

Mitigation: Prefer user-provided export files, and only provide API keys when live account access is intended.

Risk: Built-in pricing may differ from current provider pricing or negotiated account rates.

Mitigation: Override pricing with a custom pricing JSON file and verify figures against provider billing before making financial decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance]

**Output Format:** [Terminal tables, Markdown reports, JSON objects, CSV exports, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use user-provided billing or usage exports; pricing data can be overridden with a custom JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
