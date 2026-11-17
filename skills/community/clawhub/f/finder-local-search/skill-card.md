## Description:

Finder 达人搜索 helps an agent search Finder for TikTok, YouTube, and Instagram creators using keywords, regions, languages, tags, follower ranges, views, and engagement filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaobai1226](https://clawhub.ai/user/xiaobai1226)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure Finder API access and search for creator candidates on TikTok, YouTube, and Instagram. It supports searches by platform, region, language, tags, follower ranges, average views, and engagement rate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finder API keys may be pasted into chat and then stored in plaintext local configuration.

Mitigation: Configure credentials yourself through a secure local mechanism when possible, avoid sharing long-lived API keys in conversation, and rotate or revoke any key that was pasted into chat.

Risk: The agent may access Finder APIs using the configured account credentials.

Mitigation: Install and use the skill only when Finder API access from the agent is acceptable, and review requested searches or project changes before execution.

Risk: The local Finder configuration file may expose credentials if file permissions are too broad.

Mitigation: Restrict permissions on ~/.finder/config.json or the Windows equivalent, and remove the file when the credential is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaobai1226/skills/finder-local-search)
- [Finder Website](https://finder.optell.com)
- [Finder API Key Page](https://finder.optell.com/api-key)
- [Finder API Base](https://finder.optell.com/api)
- [Finder Skill Configuration](references/config.md)
- [Finder Search Filters](references/filters.json)
- [Finder Example Dialogues](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and Finder search guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Finder API request parameters, cURL or PowerShell commands, creator-search results, and local Finder configuration guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
