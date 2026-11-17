## Description:

Configures, optimizes, and troubleshoots CDN deployments, including cache strategy, security hardening, performance tuning, and incident diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to plan, validate, and troubleshoot CDN configurations, cache behavior, HTTPS/WAF settings, and performance issues across CDN providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide shell and API actions for CDN administration without clear built-in confirmation boundaries.

Mitigation: Use it in a constrained workspace and require explicit approval before executing commands or API calls.

Risk: Generated CDN, WAF, cache, DNS, or security changes could affect production traffic or weaken protections if applied blindly.

Mitigation: Review proposed changes against provider documentation, test in a non-production or staged scope, and apply least-privilege change controls.

Risk: CDN credentials or tokens may be exposed or misused when the agent has cloud/CDN access.

Mitigation: Provide CDN tokens only when needed, scope them narrowly, avoid committing secrets, and rotate credentials after sensitive sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cdn-toolkit)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CDN configuration summaries, diagnostic findings, cache and security recommendations, and API call examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
