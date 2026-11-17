## Description:

Intelligent web search routing across Gemini and Brave APIs with quota management, circuit breaker, and web_fetch fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airaalfredsf](https://clawhub.ai/user/airaalfredsf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve up-to-date web information while routing searches across Gemini, Brave, and web_fetch fallback paths. It is also used to coordinate per-agent search quotas and release unused daily allocation back to a shared pool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and partial result summaries may be stored in local logs for up to 30 days.

Mitigation: Avoid secrets, private customer data, regulated content, and sensitive investigations unless logging is disabled, redirected, or redacted before use.

Risk: Queries may be sent to third-party search or API providers through automatic routing and web_fetch fallback.

Mitigation: Use non-sensitive queries, configure provider routing deliberately, and review network and data-sharing policies before deployment.

Risk: Setup installs npm dependencies during installation.

Mitigation: Pin and review dependencies in the deployment environment before running setup in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/airaalfredsf/skills/aira-smart-search)
- [Declared Project Homepage](https://github.com/Spear-Fox-Technologies/smart-search)
- [OpenClaw Configuration Reference](references/openclaw-config.md)
- [Quota System Deep Dive](references/quota-system.md)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Configuration]

**Output Format:** [JSON objects containing search results, provider metadata, quota status, released quota, warnings, or error fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result text may be capped; local log summaries are capped and retained for a limited period.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, package.json, _meta.json, and .clawhub/origin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
