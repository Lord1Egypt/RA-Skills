## Description:

Fetches recent homepage works from Douyin, Kuaishou, Bilibili, and YouTube accounts, resolves direct media resource links, and can optionally download the media to a local directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, operations teams, and agents use this skill to collect account video metadata, direct resource links, and optional local backups from supported social-video platforms. It is suited for authorized content review, creator research, account backup, and offline viewing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account identifiers and video targets are sent to redfox.hk.

Mitigation: Use the skill only for content the user is authorized to collect and treat submitted profile or video targets as shared with the third-party service.

Risk: The downloader can write media from remote URLs to the local filesystem.

Mitigation: Run in an isolated environment, choose a constrained output directory, and avoid bulk downloading on sensitive networks until URL allowlisting and file-size limits are in place.

Risk: Agent output can expose complete direct resource links.

Mitigation: Review output before sharing it outside the intended session and avoid using the skill for sensitive or private media workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/account-video-downloader)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [Chinese README](artifact/README.md)
- [English README](artifact/README.en.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown tables or JSON records, with optional downloaded media files written to a local directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include complete direct media links, account metadata, engagement counts, resource links, local file paths, and failure messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
