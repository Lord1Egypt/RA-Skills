## Description:

中国高考升学规划助手，帮助高中生、家长和教师进行新高考选科、志愿填报、院校专业查询、录取分数线参考和政策解读。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External students, families, and educators use this skill to plan Chinese Gaokao subject choices, volunteer applications, university and major searches, score analysis, and policy interpretation. It can answer from a bundled knowledge base or, when configured, from a trusted admissions data API.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Admissions policies, score lines, rankings, and application requirements can become stale or vary by province.

Mitigation: Verify recommendations against official provincial examination authorities, label the source and year of admissions data, and state when detailed provincial data is unavailable.

Risk: Optional commercial API configuration may send planning queries to an external provider.

Mitigation: Configure only API endpoints and keys from providers the installer trusts, and avoid exposing sensitive personal information in prompts or outputs.

## Reference(s):

- [新高考选科指导参考](references/xinkao-guide.md)
- [院校信息数据库](references/universities.md)
- [高考政策知识库](references/policies.md)
- [北京市高考数据参考](references/provinces/beijing.md)
- [河北省高考数据参考](references/provinces/hebei.md)
- [河南省高考数据参考](references/provinces/henan.md)
- [湖北省高考数据参考](references/provinces/hubei.md)
- [江苏省高考数据参考](references/provinces/jiangsu.md)
- [山东省高考数据参考](references/provinces/shandong.md)
- [上海市高考数据参考](references/provinces/shanghai.md)
- [浙江省高考数据参考](references/provinces/zhejiang.md)
- [ClawHub Skill Page](https://clawhub.ai/yezhaowang888-stack/skills/college-admission-assistant)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yezhaowang888-stack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Analysis, Shell commands, Configuration]

**Output Format:** [Markdown or text guidance with optional JSON output from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should label data source and year, avoid unsupported estimates, and direct users to official provincial authorities for final decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
