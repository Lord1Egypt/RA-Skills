## Description:

Helps agents query Douyin daily, weekly, and monthly top-account rankings by category, summarize ranked account data, generate HTML reports, and support scheduled ranking updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, brands, MCN teams, and analysts use this skill to identify high-performing Douyin accounts, compare niches, screen partnership candidates, monitor competitors, and produce shareable ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may render unescaped ranking data as HTML and load remote JavaScript.

Mitigation: Review the skill before installation and avoid generating or opening reports from untrusted JSON or API responses until HTML escaping is added and the report JavaScript is pinned or bundled.

Risk: The skill requires a RedFox API key and depends on RedFox as the data provider.

Mitigation: Use the skill only if RedFox is trusted, limit the key scope where possible, avoid exposing the key in prompts, logs, or outputs, and confirm the key can be reset or revoked.

Risk: Scheduled ranking subscriptions may create recurring automated tasks.

Mitigation: Confirm the requested subscription cadence with the user and make sure the user knows how to cancel or change the schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/dy-rank-tranker)
- [RedFox API documentation](references/api_docs.md)
- [Category mapping and matching rules](references/category_map.md)
- [Ranking score rules](references/score_rules.md)
- [Update and date selection rules](references/update_rules.md)
- [RedFox API provider](https://redfox.hk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown ranking tables, JSON data files, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a REDFOX_API_KEY for RedFox API access; generated reports may contain account links and ranking data returned by the API provider.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
