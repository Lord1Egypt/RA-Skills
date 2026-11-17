## Description:

Fetches recent works from Douyin, Kuaishou, Bilibili, and YouTube account pages, resolves download links, and can batch download authorized media locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessdy](https://clawhub.ai/user/jessdy)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, researchers, and agents use this skill to collect account video metadata, resolve media resource links, review results as Markdown or JSON, and optionally save authorized works to disk for backup, analysis, or offline review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account identifiers and work or video URLs are sent to the yige.zone API.

Mitigation: Use the skill only for media you are authorized to access and store, and prefer a scoped or disposable API key that can be rotated if exposed.

Risk: The skill downloads API-provided media URLs to local storage.

Mitigation: Run it with a limited output directory and available disk quotas, and review downloaded files before reuse or redistribution.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/jessdy/yige-skills/tree/main/skills/account-video-downloader)
- [ClawHub skill page](https://clawhub.ai/jessdy/skills/account-video-downloader-2)
- [Yige API key settings](https://yige.zone/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown tables or structured JSON, with optional downloaded media files in a local output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YIGE_API_KEY environment variable and supports platform, account, pagination, date range, count, rate limit, output directory, JSON, and download options.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
