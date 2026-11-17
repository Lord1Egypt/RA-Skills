## Description:

Monitors battery-market policy, subsidy, regulatory, safety, and investment news across China, the United States, India, Russia, and South Korea, then generates Chinese research-style weekly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardcoder849](https://clawhub.ai/user/richardcoder849)

### License/Terms of Use:

MIT-0

## Use Case:

Market analysts, investors, and agents use this skill to collect recent battery-policy, safety, recall, subsidy, and investment news, classify likely market impact, and generate Chinese weekly research briefs for five target countries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches news detail pages from unvalidated URLs.

Mitigation: Restrict detail fetching to approved public news hosts and block private, localhost, metadata IP, and unsafe redirect targets before routine use.

Risk: Generated reports may be copied outside the skill data folder to the user's Desktop.

Mitigation: Make Desktop export opt-in or keep generated reports inside the local data folder by default.

Risk: Runtime dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Pin dependency versions and review updates before installation in managed environments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/richardcoder849/skills/battery-market-watch)
- [Publisher profile](https://clawhub.ai/user/richardcoder849)
- [Configured source hosts and RSS feeds](artifact/config.json)
- [NewsAPI](https://newsapi.org/)
- [GNews](https://gnews.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, DOCX, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses dated local filenames for raw news, parsed news, analysis, Markdown reports, and Word reports.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
