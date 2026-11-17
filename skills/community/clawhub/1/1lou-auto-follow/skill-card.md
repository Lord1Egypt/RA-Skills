## Description:

管理追剧清单，自动检查并推送1lou网站的最新剧集更新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluepop1991-cloud](https://clawhub.ai/user/bluepop1991-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to maintain a Chinese-language drama watchlist, check 1lou for newly available episodes, report matching results, and assist with confirmed torrent download handoff to qBittorrent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is tailored to a specific local watchlist path and private qBittorrent network address.

Mitigation: Review and replace the disclosed macOS path and private IP settings before installation or execution.

Risk: The skill contacts listed 1lou domains and can help add torrent files to qBittorrent after confirmation.

Mitigation: Install only when those network actions are expected, and require explicit user confirmation before download or qBittorrent handoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bluepop1991-cloud/skills/1lou-auto-follow)
- [Publisher profile](https://clawhub.ai/user/bluepop1991-cloud)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages with links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update a local JSON watchlist and may prepare torrent files after user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
