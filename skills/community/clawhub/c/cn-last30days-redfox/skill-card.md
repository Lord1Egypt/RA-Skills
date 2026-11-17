## Description:

Searches recent discussions from Xiaohongshu, Douyin, and WeChat Official Accounts to help agents analyze Chinese social-media topics, sentiment trends, and brand or entity comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand operators, market researchers, and agents use this skill to research Chinese social-media trends over the last 30 days, compare reputation across platforms, and produce structured findings with source links and visual reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and queries may be sent to redfox.hk, which can expose sensitive internal names or confidential topics.

Mitigation: Use the skill only for intentional China social-media research and avoid confidential topics unless sharing them with redfox.hk is acceptable.

Risk: The release evidence reports unsafe generated HTML behavior and automatic opening of generated reports.

Mitigation: Do not allow automatic opening of generated HTML reports until HTML escaping and link validation issues are fixed.

Risk: The security summary describes broad automatic behavior around research, report generation, and local file output.

Mitigation: Review the skill before installing or executing it, including output paths, external requests, and generated files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yuanyi-github/skills/cn-last30days-redfox)
- [Output rules and report templates](references/output-rules.md)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox data source](https://redfox.hk?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown research report with linked sources, JSON data files, and interactive HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and uses REDFOX_API_KEY when configured; generated reports summarize Xiaohongshu, Douyin, and WeChat Official Account results.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter version is 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
