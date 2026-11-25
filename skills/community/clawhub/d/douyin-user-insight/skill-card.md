## Description:

基于抖音公开数据搜索视频、账号、作品和评论，并帮助团队发现用户需求与产品机会。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

产品、营销和内容团队可用它研究抖音公开内容，分析用户需求、评论反馈、热点和对标账号，为产品机会、选题和市场判断提供数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links or video IDs are sent to the third-party API.

Mitigation: Review submitted terms and links before running a query, and avoid sending information you do not intend to share with that service.

Risk: The security scan was partial and has medium confidence; account search is an additional capability.

Mitigation: Review the skill's requested account-search capability and the available scan guidance before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-user-insight)
- [Product and token access](https://www.guaikei.com)
- [Usage guide](artifact/SKILL.md)
- [Demand mining guide](artifact/references/demand-mining.md)
- [Customer acquisition guide](artifact/references/customer-acquisition.md)
- [CLI options](artifact/references/options.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON results with concise analysis guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be saved as JSON log files for later analysis.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
