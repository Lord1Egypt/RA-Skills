## Description:

提供高考志愿填报相关工具，用于查询学校和专业历年录取分数线、招生计划、学校与专业信息，并生成志愿推荐参考。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Students, families, and admissions advisors use this skill to explore Chinese gaokao admissions options by querying score lines, school and major admission history, enrollment plans, rank conversion, and admission-probability guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that API keys may be stored in plaintext and can expose the key and query data.

Mitigation: Use only a key suitable for local storage, keep .env out of source control and backups, and rotate the key if exposure is suspected.

Risk: The security review reports that local configuration can persistently affect future API calls.

Mitigation: Review before installing and prefer a fixed version that validates keys and locks the API host.

Risk: The release notes and security guidance state that 2026 admissions results are simulated preview data.

Mitigation: Verify final admissions decisions against official admissions sources before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/gaokao-expert-v)
- [XiaoBenYang API key provider](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown summaries with API-returned JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; 2026 admissions results are described as simulated preview data based on 2025 data.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
