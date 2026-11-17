## Description:

Fetches yesterday's arXiv papers, ranks them by keyword relevance, and pushes selected results to Feishu or Lark via webhook for multiple research groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ventaozzz](https://clawhub.ai/user/ventaozzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, research teams, and technical staff use this skill to automate daily arXiv monitoring by topic, rank papers against group-specific keywords, and send concise paper recommendations to a Feishu or Lark chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured webhook can expose selected paper titles, links, group names, and keyword-derived research interests to the destination chat.

Mitigation: Store the webhook URL as a secret, restrict access to configuration and logs, and send results only to approved Feishu or Lark chats.

Risk: Default network and logging behavior can expose or misuse the webhook during unattended scheduled runs.

Mitigation: Restrict cron log permissions, avoid printing secrets, pin dependencies, and review scheduled execution settings before deployment.

Risk: The fallback arXiv HTTP mode can forward untrusted cleartext API results into chat.

Mitigation: Prefer the arxiv_only mode or an HTTPS-protected fallback where available, and review pushed links before broad distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ventaozzz/skills/arxiv-daily-pusher)
- [arXiv API endpoint used by the artifact](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands]

**Output Format:** [Plain text Feishu/Lark messages and console output, with YAML configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks results with title matches weighted 2x and abstract matches weighted 1x; default top_k is 6 papers per group.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
