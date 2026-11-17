## Description:

Is Anthropic, OpenAI, Cloudflare, GitHub or Cohere having an incident right now? One read-only call, refreshed every 15 minutes, linked to each provider's own status page. Free, no key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikerawsonnz](https://clawhub.ai/user/mikerawsonnz)

### License/Terms of Use:

MIT-0

## Use Case:

AI agent operators and developers can check whether Anthropic, OpenAI, Cloudflare, GitHub, or Cohere reports an incident when model calls fail or slow down. They can use the incident links and status timestamps to guide troubleshooting and escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delayed, stale, or unavailable status data could mislead operational decisions.

Mitigation: Check the result timestamp and the provider's official status page before making operational changes; treat data older than one hour or marked unknown as unknown. Keep provider switches within existing authorization.

## Reference(s):

- [AI Provider Status service](https://ai-status.getvda.ai/)
- [Current provider status snapshot](https://ai-status.getvda.ai/now.json)
- [Incident history Atom feed](https://ai-status.getvda.ai/feed.atom)
- [ClawHub release page](https://clawhub.ai/mikerawsonnz/skills/ai-provider-status)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Provider status data summarized in text with incident links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public status check. Snapshot data is refreshed every 15 minutes; stale data should be treated as unknown.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
