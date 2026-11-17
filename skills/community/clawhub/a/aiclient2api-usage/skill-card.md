## Description:

Check AIClient2API usage statistics, quotas, and account status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limingdev-tech-2024](https://clawhub.ai/user/limingdev-tech-2024)

### License/Terms of Use:


## Use Case:

Developers and operators who run AIClient2API use this skill to inspect local usage metrics, credits, quotas, subscription status, expiration dates, and account health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local AIClient2API cache data and account details.

Mitigation: Install and run it only where access to that account data is appropriate, and avoid sharing generated usage reports without review.

Risk: Refresh scripts may use a local password and authenticate to a localhost service.

Mitigation: Ask before running authenticated refresh commands, verify the local service endpoint, and review credential handling before installation.

Risk: The security summary flags an unsafe temporary-script pattern.

Mitigation: Prefer a revised version that removes the predictable /tmp helper, or inspect the scripts before execution in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/limingdev-tech-2024/skills/aiclient2api-usage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and usage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize locally cached account, quota, subscription, and overage data when the referenced scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
