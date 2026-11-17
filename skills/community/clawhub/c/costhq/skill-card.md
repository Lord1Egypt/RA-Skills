## Description:

Track agent session costs, file changes, and git commits with CostHQ, including budget limits, local model tracking, dashboard analytics, and Enterprise SOC2 audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brian-mwirigi](https://clawhub.ai/user/brian-mwirigi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use CostHQ to track agent task sessions, log AI usage costs, review file and commit activity, manage budgets, and inspect activity through a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CostHQ can record agent activity, usage details, file changes, commits, and repository metadata.

Mitigation: Install only in repositories where this monitoring is acceptable, prefer a pinned reviewed npm package version, and review collected session data before using it for audit or reporting.

Risk: The Semantic Caching Proxy intercepts API calls and may cache prompts or responses.

Mitigation: Avoid routing secrets, customer data, or regulated prompts through the proxy until retention, cache purge, and access-control behavior are clear.

Risk: Dashboard command controls can affect active tracked sessions and execute CostHQ CLI operations.

Mitigation: Restrict dashboard access to trusted users and avoid running installation or CostHQ commands with elevated privileges unless required.

## Reference(s):

- [CostHQ ClawHub Listing](https://clawhub.ai/brian-mwirigi/skills/costhq)
- [CostHQ GitHub Repository](https://github.com/brian-mwirigi/costhq)
- [CostHQ npm Package](https://www.npmjs.com/package/costhq)
- [CostHQ Changelog](https://github.com/brian-mwirigi/costhq/blob/main/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to use --json and may read or write local CostHQ session data.]

## Skill Version(s):

4.0.0 (source: server release metadata; artifact heading also states Latest v4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
