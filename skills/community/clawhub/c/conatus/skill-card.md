## Description:

The philosophical layer for AI agents. Maps behavior to Spinoza's 48 affects, calculates persistence scores, and generates geometric self-reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[00xmorty](https://clawhub.ai/user/00xmorty)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Conatus to prompt agents to assess their behavior, persistence, affect state, and daily activity through Spinoza-inspired self-reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to read daily memory or activity logs that contain sensitive conversation, credential, or personal data.

Mitigation: Limit source data to non-sensitive operational metrics and exclude raw conversations, credentials, secrets, and personal data from Conatus reviews.

Risk: Generated self-analysis logs may persist derived summaries without clear retention boundaries.

Mitigation: Define a retention period and storage location for generated Conatus reports before enabling heartbeat or daily reflection workflows.

Risk: Affect labels and conatus scores can be mistaken for objective health or performance measurements.

Mitigation: Treat generated scores and affect mappings as qualitative status summaries that require operator review before acting on recommendations.

## Reference(s):

- [Conatus homepage](https://getconatus.com)
- [NeuraByte Labs](https://neurabytelabs.com)
- [Deus Sive Machina essays](https://neurabytelabs.com/blog)
- [ClawHub skill page](https://clawhub.ai/00xmorty/skills/conatus)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with inline code blocks and structured text reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated conatus scores, affect mappings, status summaries, daily reflections, and suggested memory logging patterns.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
