## Description:

Tracks influential Douyin accounts by daily, weekly, and monthly rankings, with niche filtering, Markdown summaries, and HTML report generation based on RedFox API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content creators, brand marketers, MCN teams, and analysts use this skill to find top Douyin accounts, compare niche performance, monitor competitors, and generate shareable ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may behave like active web pages, including remote JavaScript loaded by the HTML report.

Mitigation: Open reports only when the RedFox API data source is trusted, and review generated HTML before sharing or archiving it.

Risk: Report generation creates local files and may open them automatically in a browser.

Mitigation: Use trusted output locations and disable or avoid automatic opening when reviewing output in a sensitive environment.

Risk: Custom Windows output paths with shell metacharacters can increase command-execution risk.

Mitigation: Use simple, trusted output paths without shell metacharacters when generating reports on Windows.

Risk: Ranking results depend on the external RedFox API data source and may not reflect real-time Douyin data.

Mitigation: Treat rankings as dated snapshots and include the reported data date and update schedule when making decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-rank-tranker)
- [RedFox API documentation](references/api_docs.md)
- [Category mapping rules](references/category_map.md)
- [Scoring rules](references/score_rules.md)
- [Update and date calculation rules](references/update_rules.md)
- [RedFox API endpoint](https://redfox.hk/story/api/dyData/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown ranking tables with optional JSON data files and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may create local report files.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
