## Description:

Analyzes declines in acceptance rate through staged attribution, first identifying abnormal slices and then checking capital-side, asset-dimension, and sensitive-funding-side explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzhou1982](https://clawhub.ai/user/mzhou1982)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts and operations teams use this skill to investigate why acceptance rates declined over day or week windows. It guides the agent through staged data queries and concise business-facing explanations without exposing internal routing fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded and ambient credentials may be used during metric queries.

Mitigation: Revoke or remove embedded tokens before installation and require explicit, approved credential injection for controlled environments.

Risk: Metric requests may be sent to an unrestricted or unintended endpoint.

Mitigation: Allowlist approved endpoint destinations and review endpoint overrides before running the skill.

Risk: Raw business query payloads and responses may be persisted in debug logs.

Mitigation: Disable raw query logging by default or redact sensitive payloads before logs are written or shared.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzhou1982/skills/acceptance-rate-analysis-new-2)
- [Publisher profile](https://clawhub.ai/user/mzhou1982)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, guidance]

**Output Format:** [Markdown prose and tables backed by JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses day or week granularity and staged stop conditions for attribution.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
