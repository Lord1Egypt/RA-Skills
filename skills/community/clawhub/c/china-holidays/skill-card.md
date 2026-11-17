## Description:

Provides China national statutory holiday schedules, including holiday dates and makeup workday adjustments, defaulting to the current year when no year is specified.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xzxiaoshan](https://clawhub.ai/user/xzxiaoshan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to retrieve China holiday schedules, makeup workday adjustments, specific holiday details, custom-formatted summaries, and cross-year comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A forced refresh can retrieve and cache a URL selected from remote search results without confirming that it remains on the expected government site.

Mitigation: Prefer cached holiday data when possible; when forcing a refresh, confirm the returned URL is an expected gov.cn notice before relying on or sharing the result.

Risk: Network refresh writes new cached notice files inside the skill assets directory.

Mitigation: Review cache changes after refresh and keep the bundled official notices as the preferred baseline for normal use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xzxiaoshan/skills/china-holidays)
- [China Government Website](https://www.gov.cn/)
- [2026 State Council Holiday Notice](https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Plain text or Markdown summaries, with JSON, tables, or lists when requested by the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use cached official notices when available and may refresh from the network when explicitly requested.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
