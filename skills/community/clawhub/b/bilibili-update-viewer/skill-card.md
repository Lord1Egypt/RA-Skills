## Description:

Checks a Bilibili uploader's latest videos and dynamics and reports whether the uploader posted a video today.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianguo99](https://clawhub.ai/user/jianguo99)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to look up Bilibili uploaders by mid or username, list recent videos or dynamics, and answer whether a selected uploader updated today.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires full Bilibili browser cookies even though it performs a read-only lookup.

Mitigation: Set BILIBILI_COOKIES only in the local shell, avoid sharing it in chats or logs, and clear or rotate the cookie after use.

Risk: Searches create a local user_cache.json containing public uploader metadata.

Mitigation: Review or delete the generated cache when local retention of searched uploader metadata is not desired.

Risk: Dependency installation is not fully pinned.

Mitigation: Install dependencies in an isolated environment and review the resolved requests package version before deployment.

Risk: Bilibili API rate limits or API changes can interrupt lookups.

Mitigation: Keep request volume low and report frequent-access or API-change failures plainly to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianguo99/skills/bilibili-update-viewer)
- [Bilibili](https://www.bilibili.com)
- [Bilibili API WBI signature documentation](https://socialsisteryi.github.io/bilibili-API-collect/docs/misc/sign/wbi.html)
- [bilibili-hot-monitor source inspiration](https://clawhub.ai/Jacobzwj/bilibili-hot-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with command output summaries and Bilibili video or dynamic links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, the requests package, and a local BILIBILI_COOKIES environment variable; declared OS support is darwin, linux, and win32.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
