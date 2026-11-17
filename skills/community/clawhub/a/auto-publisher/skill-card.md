## Description:

Auto Publisher helps agents prepare and run multi-platform video publishing workflows for Douyin, WeChat Channels, Xiaohongshu, Bilibili, YouTube, and related platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[954215110](https://clawhub.ai/user/954215110)

### License/Terms of Use:

MIT

## Use Case:

Creators, operators, and developers use this skill to automate or guide video uploads, captions, tags, account configuration, and publish logging across multiple social media platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content publicly across multiple social accounts.

Mitigation: Use it only with accounts where automated posting is acceptable, begin with one selected platform, and run in a visible browser until the workflow is verified.

Risk: Local account configuration, saved sessions, cookies, and publish logs may expose account or posting data.

Mitigation: Do not store real passwords in config/accounts.json, protect or delete config and publish_log.json files after use, and treat saved browser sessions or cookies as account credentials.

## Reference(s):

- [Auto Publisher ClawHub Skill Page](https://clawhub.ai/954215110/skills/auto-publisher)
- [Publisher Profile](https://clawhub.ai/users/954215110)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python command examples, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local account configuration and publish logs when the publishing script is executed.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
