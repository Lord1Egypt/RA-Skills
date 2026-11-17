## Description:

Capture URLs into the user's CatchLinger bookmark collection. Resolves URLs, GitHub stars, or local Chrome/Edge bookmarks; extracts content; generates a title, summary and a few broad, reusable tags; then saves via REST or MCP. Use when the user asks to 收藏 / 收录 / 加入 CatchLinger / 保存这些链接 / 导入书签 / 同步 GitHub star / 整理收藏 / save links / bookmark this / add to CatchLinger / import bookmarks / sync GitHub stars / organize bookmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yqjc2003](https://clawhub.ai/user/yqjc2003)

### License/Terms of Use:

Apache-2.0

## Use Case:

Individuals and agents use this skill to review URLs, GitHub stars, or local browser bookmarks, prepare a language-appropriate title, summary, and reusable tags, and save the records to a CatchLinger collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags a potentially incomplete bookmark-tag merge that may delete a source tag before every bookmark has been migrated, and notes that some executable scripts were only partially inspected.

Mitigation: Review the merge impact with the documented dry-run option and verify affected bookmarks before applying it; inspect the scripts before use. Treat GITHUB_TOKEN as a secret and set it only when higher API quotas or private-star access are needed.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/yqjc2003/trove/tree/main/skills/catch-and-linger)
- [CatchLinger](https://catchlinger.sxyicheng.tech)
- [ClawHub release](https://clawhub.ai/yqjc2003/skills/catch-and-linger)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls]

**Output Format:** [Structured bookmark records with natural-language titles, summaries, and tags; REST or MCP save requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to three reusable tags per record; output follows the user's language preference]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
