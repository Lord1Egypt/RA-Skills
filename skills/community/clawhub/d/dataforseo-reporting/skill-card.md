## Description:

Run SEO, SERP, keyword, and search intelligence workflows with DataForSEO -- powered by ClawLink.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw agent to DataForSEO through ClawLink, run SEO and search-intelligence tasks, and retrieve async task results for reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external ClawLink plugin that brokers DataForSEO access and handles account pairing.

Mitigation: Before installation, verify the ClawLink plugin publisher, version, source, and requested permissions.

Risk: DataForSEO tasks may consume paid account credits, especially large crawls and bulk queries.

Mitigation: Require explicit user confirmation before large crawls, bulk queries, or any action likely to affect account spending.

Risk: Local device credentials are stored by the OpenClaw plugin configuration.

Mitigation: Use trusted devices and review local credential handling before pairing production DataForSEO accounts.

## Reference(s):

- [ClawHub DataForSEO Skill Page](https://clawhub.ai/hith3sh/skills/dataforseo-reporting)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=dataforseo-reporting)
- [ClawLink DataForSEO Dashboard](https://claw-link.dev/dashboard?add=dataforseo)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API calls, Markdown]

**Output Format:** [Markdown guidance with shell commands, JavaScript examples, and tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DataForSEO async task IDs for create/get workflows; some actions can consume paid DataForSEO credits.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
