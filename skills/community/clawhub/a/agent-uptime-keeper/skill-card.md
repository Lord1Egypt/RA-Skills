## Description:

Keep always-on agents honestly reachable: register each agent endpoint with an external heartbeat watch, poll its verdict daily, and escalate when it goes dark. Use when running long-lived agents, before promising uptime to a counterparty, or after an outage nobody noticed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcircuitbreaker](https://clawhub.ai/user/0xcircuitbreaker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to register external heartbeat monitoring for agent endpoints, review reachability and outage alerts, and report measured uptime without overstating what the probes prove.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A monitored health endpoint or response could expose sensitive information.

Mitigation: Use a public health endpoint and keep secrets out of its URL and response.

Risk: Paid registration, polling, or retries may incur charges, and the provider website could not be independently verified during review.

Mitigation: Confirm the provider and payment amount before paid retries or recurring polling, and set a spending limit.

## Reference(s):

- [Monitoring service homepage](https://agents.daedalusdevelopmentgroup.com)
- [ClawHub skill release](https://clawhub.ai/0xcircuitbreaker/skills/agent-uptime-keeper)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes monitoring setup and status polling steps, plus observed uptime and alert report fields; uptime claims are limited to the watch's observation period.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
