## Description:

Helps agents manage beehiiv publications, subscribers, posts, segments, and automations through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Newsletter operators and developers use this skill to inspect beehiiv publications and subscriptions, manage subscriber data and posts, and configure approved automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Maton grants access to the user's beehiiv account and newsletter data.

Mitigation: Confirm authorization with the user, prefer OAuth and narrow scopes, and revoke unused connections.

Risk: Writes or hosted functions may alter subscriptions, posts, or other newsletter records.

Mitigation: Start with read-only requests and confirm the exact target and effect before each write or function.

Risk: Triggers and destinations can repeatedly send subscriber or other event data to external services.

Mitigation: Get separate approval for each destination, limit event scope and shared fields, and review automated actions before enabling them.

## Reference(s):

- [beehiiv skill release](https://clawhub.ai/byungkyu/skills/beehiiv)
- [beehiiv API Reference](https://developers.beehiiv.com/api-reference)
- [Maton](https://maton.ai)
- [Maton CLI Manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command, code, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton account, network access, and an authorized beehiiv connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
