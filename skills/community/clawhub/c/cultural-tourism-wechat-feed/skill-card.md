## Description:

Searches WeChat Official Account cultural tourism articles, ranks popular items by read count, clusters them by topic, and generates an HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, scenic spot or tourism professionals, and tourism researchers use this skill to monitor trending WeChat cultural tourism content, compare topics, and receive a report for daily hotspot tracking or keyword-based research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription mode can create persistent scheduled jobs on the user's system.

Mitigation: Use one-time report generation by default; enable subscription only after review and remove it with the unsubscribe path when it is no longer needed.

Risk: API keys can be handled unsafely when stored in scheduler or local configuration files.

Mitigation: Prefer environment-injected or keychain-managed API keys, avoid plaintext local configuration, and rotate or revoke keys that may have been exposed.

Risk: The release security verdict is suspicious because subscription behavior and secret handling require extra review.

Mitigation: Review carefully before installing, avoid subscription mode until the publisher resolves the security concerns, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/cultural-tourism-wechat-feed)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown summary with category counts, shell command invocation, and generated HTML report file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; supports optional keyword, date range, output directory, and subscription flags.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
