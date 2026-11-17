## Description:

Fetches recent Douyin works for one or more Douyin IDs, parses watermark-free media links through RedFoxHub, and can present results or batch download media locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, operations teams, MCNs, brands, and learners use this skill to retrieve Douyin account work metadata, inspect download links, filter by page or date range, and optionally save authorized media locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin account IDs, work URLs, and the RedFox API key to redfox.hk.

Mitigation: Use only API keys from a verified RedFoxHub account, confirm key scope and revocation options, and keep keys out of prompts, logs, code, and output files.

Risk: Broad third-party media downloading can retrieve content the user is not authorized to download or reuse.

Mitigation: Use the skill only for content the user owns, has permission to download, or is otherwise authorized to process.

Risk: Full download links in Markdown or JSON output may expose private or sensitive media URLs.

Mitigation: Review outputs before sharing, avoid publishing raw result tables, and treat returned links as sensitive.

Risk: Batch downloads may consume significant disk space and bandwidth.

Mitigation: Choose a controlled output directory, limit page size and account count, and confirm available storage before bulk downloads.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/redfox-data/redfox-community/tree/main/skills/douyin-video-downloader)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-video-downloader-2)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=github)
- [Douyin ID example](https://lyy.redfox.hk/page/ljq.png)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown table or JSON, with optional downloaded media files in a local output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and sends Douyin IDs and work URLs to redfox.hk.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
