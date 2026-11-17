## Description:

Generates detailed IT disaster recovery plans with RTO/RPO targets, failover procedures, backup strategies, communication plans, testing schedules, cost modeling, and compliance mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Operations, infrastructure, security, and compliance teams use this skill to draft actionable disaster recovery plans, including recovery targets, failover runbooks, backup procedures, incident communications, testing schedules, cost estimates, and compliance mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated failover commands or backup procedures may not match the user's production infrastructure.

Mitigation: Review generated procedures with infrastructure owners before using them in production.

Risk: Prompts may accidentally include secrets, private keys, or sensitive operational data.

Mitigation: Avoid providing secrets or private keys in prompts.

Risk: Generated cost estimates may use assumptions that do not match the user's region, currency, or provider pricing.

Mitigation: Adjust cost estimates for the user's actual region, currency, and environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-disaster-recovery)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, runbooks, command examples, and compliance mappings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RTO/RPO targets, risk scoring, tiered recommendations, cost estimates in USD, and time estimates for recovery steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
