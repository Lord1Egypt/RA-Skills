## Description:

小龙虾日报，将你最关心的资讯主动送到你眼前。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenhui7au](https://clawhub.ai/user/chenhui7au)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create twice-daily personalized news briefs from public hot topics and configured news labels. The skill initializes user preferences, fetches matching news, filters by the current Asia/Shanghai batch window, and formats a concise Markdown brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs on a scheduled heartbeat twice daily using Asia/Shanghai time.

Mitigation: Install only when the scheduled cadence is acceptable, and verify the heartbeat configuration during initialization.

Risk: User news preferences are stored in skill metadata.

Mitigation: Keep preference text limited to information appropriate for local skill configuration.

Risk: Brief generation depends on the configured news service and public web-fetching tools for hot topics.

Mitigation: Use the documented retry and fallback behavior, and do not fabricate news when sources fail or no items match the time window.

## Reference(s):

- [Claws Daily on ClawHub](https://clawhub.ai/chenhui7au/skills/claws-daily)
- [Install & Initialization](artifact/install.md)
- [Daily Brief Examples](artifact/daily_example.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown brief with setup guidance and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The brief uses fixed sections, supports zh-CN or en-US output, and limits the personalized news section to five items on initial output.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
