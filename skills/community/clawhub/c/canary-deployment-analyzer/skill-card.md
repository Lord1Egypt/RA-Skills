## Description:

Analyze canary deployments by comparing metrics between canary and baseline. Provide data-driven promotion/rollback recommendations based on error rates, latency percentiles, and custom business metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to evaluate progressive deployments by comparing canary and baseline metrics, logs, and promotion thresholds before deciding whether to promote, hold, or roll back.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may help query production observability systems and logs.

Mitigation: Review proposed commands before execution and confirm the agent should access Prometheus, Datadog, CloudWatch, or Kubernetes log data.

Risk: Commands may involve Datadog API keys, AWS credentials, or Kubernetes log access.

Mitigation: Use least-privilege credentials, avoid exposing secrets in prompts or logs, and verify the target environment before running commands.

Risk: Promotion or rollback recommendations can be misleading if metrics, traffic split, or observation windows are incomplete.

Mitigation: Validate the underlying metric sources, compare canary and baseline over an appropriate window, and require human approval for deployment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/canary-deployment-analyzer)
- [Datadog metrics query API endpoint](https://api.datadoghq.com/api/v1/query)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include metric comparisons, promotion or rollback recommendations, threshold guidance, and progressive delivery plans.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
