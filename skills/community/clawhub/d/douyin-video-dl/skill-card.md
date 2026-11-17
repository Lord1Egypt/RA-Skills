## Description:

Downloads Douyin videos through the TikHub API from short links, full Douyin URLs, query-parameter modal IDs, or bare video IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch a direct Douyin video URL or save a Douyin video file from a supported Douyin link or video ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run on incidental Douyin links or bare long numbers.

Mitigation: Require explicit user confirmation before invoking the downloader, especially when the input was only an incidental URL or number.

Risk: The skill sends Douyin links or IDs to TikHub using a local TikHub API token.

Mitigation: Use only when the user is comfortable sharing the link or ID with TikHub, and protect the local API token configuration.

Risk: Network requests may be made before the input host is narrowly validated.

Mitigation: Prefer a revised version that validates v.douyin.com hostnames before making network requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mfang0126/skills/douyin-video-dl)
- [TikHub API Token Registration](https://user.tikhub.io/register)
- [TikHub Douyin Fetch Video API](https://api.tikhub.io/api/v1/douyin/web/fetch_one_video)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print a direct video URL or save an MP4 file to the default or user-specified download directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
