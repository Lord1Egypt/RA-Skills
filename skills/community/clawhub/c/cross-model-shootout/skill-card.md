## Description:

Runs the same prompt against multiple models and compares measured latency, token usage, optional cost, and response samples to support model selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams comparing model choices can run their own prompts across several models to review response samples, latency, token usage, and costs when prices are supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts can be sent to an external model endpoint without a clear consent step.

Mitigation: Review the endpoint and use only non-sensitive prompts before running the comparison.

Risk: A generic API key may be sent to the default third-party endpoint.

Mitigation: Set an endpoint-specific SHOOTOUT_API_KEY rather than relying on OPENAI_API_KEY; confirm the endpoint before running.

Risk: Multiple models and repeated calls may incur unexpected charges or send prompts externally many times.

Mitigation: Confirm the model list and repeat count, and check expected costs before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lijinhongucl-pixel/skills/cross-model-shootout)
- [AstraFlow homepage](https://www.ucloud.cn/site/active/astraflow-credit?ytag=geo_waituo_SKillhub)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown comparison report with optional JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes per-model measurements, failures, and response samples; cost estimates require user-supplied prices, and response quality requires human review.]

## Skill Version(s):

1.0.3 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
