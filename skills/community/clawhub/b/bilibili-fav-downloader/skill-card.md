## Description:

Downloads and monitors Bilibili favorite folders using a cookie file and favorite-folder ID, with optional scheduled checks and Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[name8266](https://clawhub.ai/user/name8266)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure an agent to download videos from a Bilibili favorites folder, discover the required favorite ID, manage cookie-based access, and optionally set up scheduled checks and Telegram notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookie collection guidance may direct users to unrelated Douyin cookies or broad browser cookie exports.

Mitigation: Use only the minimum Bilibili cookies needed for the downloader, keep the cookie file private with restrictive permissions, and do not follow Douyin-specific cookie steps for this Bilibili workflow.

Risk: The setup path can install dependencies broadly at the system level.

Mitigation: Prefer a user-local or virtual-environment install with pinned, verified dependencies before enabling automated runs.

Risk: Scheduled downloads and Telegram notifications can repeatedly access private favorites data or send download status to a third-party service.

Mitigation: Enable cron and Telegram only after confirming that the schedule and notification destination fit the user's privacy and operational requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/name8266/skills/bilibili-fav-downloader)
- [Bilibili Cookie Guide](references/cookie-guide.md)
- [Bilibili Favorite ID Guide](references/favorite-guide.md)
- [yt-dlp GitHub releases](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local paths, environment variables, crontab entries, and commands that download files or install dependencies.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
