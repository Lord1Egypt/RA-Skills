## Description:

查询 Xtreme Gaming (XG) 战队的下一场比赛信息。通过 Liquipedia API 获取精准、实时的赛程数据。当用户询问 XG 何时有比赛或下一场对手是谁时调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[earthking11](https://clawhub.ai/user/earthking11)

### License/Terms of Use:

MIT-0

## Use Case:

External users and Dota 2 followers use this skill to ask when Xtreme Gaming next plays, who the opponent is, and what match context is available. The agent fetches public Liquipedia schedule data, converts times to Beijing time, and summarizes the result in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses intentionally mocking fan-commentary about Ame.

Mitigation: Review and edit the output style before use when neutral or broadly appropriate match reporting is required.

Risk: The skill depends on public Liquipedia data fetched through curl.

Mitigation: Confirm network access, User-Agent requirements, and returned schedule data before relying on the match summary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/earthking11/skills/dota2-xg-next-game)
- [Liquipedia Dota 2 API endpoint for Xtreme Gaming](https://liquipedia.net/dota2/api.php?action=parse&page=Xtreme_Gaming&format=json&prop=text|sections)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese natural-language Markdown with emphasized match details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; output reports times in Beijing time and may include fan-mocking commentary about Ame.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
