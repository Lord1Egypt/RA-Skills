## Description:

职业教育与职业发展助手，提供热门职业介绍、技能证书考试指南、职业规划建议、职教高考政策解读和实习就业指导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External vocational-school students, teachers, and early-career workers use this skill for Chinese-language career exploration, certificate planning, vocational-policy interpretation, internship guidance, and career-path recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Salary, policy, certificate, and job-market details can become stale or vary by region.

Mitigation: Treat the skill's answers as reference guidance and verify current details with official policy, examination, and recruiting sources before making decisions.

Risk: Career recommendations may be incomplete or overly general for an individual user's circumstances.

Mitigation: Present recommendations as decision support, ask follow-up questions when context is limited, and avoid framing outputs as definitive career decisions.

Risk: Optional commercial API integration could expose credentials or rely on an untrusted external service.

Mitigation: Use the local knowledge-base mode unless a trusted API endpoint has been separately reviewed, and do not provide real API keys to unverified integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/career-development-assistant)
- [热门职业数据库](references/careers.md)
- [技能证书指南参考](references/certificates.md)
- [就业指导参考](references/employment-guide.md)
- [职教政策知识库](references/vocational-policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown guidance with optional JSON or command-line output from the recommender script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses static local reference material by default; optional commercial API configuration may extend job-market, internship, and assessment data.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
