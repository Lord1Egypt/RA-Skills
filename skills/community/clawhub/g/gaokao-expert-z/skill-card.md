## Description:

提供高考志愿相关工具，获取学校和专业以往的录取分数线，提供推荐信息等；往年数据为真实数据，2026 年数据未发布前暂以 2025 年数据虚拟补充体验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Students, families, admissions advisors, and agents use this skill to query Chinese Gaokao control lines, school and major admission scores, admissions plans, score-to-rank data, and recommendation-oriented school matches. It requires a XiaoBenYang API key and should present admissions outputs as decision support rather than guaranteed admission results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a low-privilege or revocable API key, restrict .env file permissions, and avoid shared, synced, or commit-prone workspaces.

Risk: Admissions-query details and the API key are sent to the upstream XiaoBenYang service.

Mitigation: Install only when that data sharing is acceptable, and review the configured upstream endpoint before use.

Risk: The artifact states that 2026 data is temporarily virtualized from 2025 data until current-year data is released.

Mitigation: Clearly disclose that limitation in responses and verify consequential admissions decisions against official current-year sources.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cainingnk/skills/gaokao-expert-z)
- [XiaoBenYang API key and service site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown summaries and structured JSON from admissions API tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XBY_APIKEY; tool results include raw upstream API data with success and message fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
