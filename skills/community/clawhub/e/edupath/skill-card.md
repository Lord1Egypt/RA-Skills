## Description:

接收用户输入的【本科专业】，输出一份"总-分-总"结构的考研专业与院校方向选择指导报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsingliuwin](https://clawhub.ai/user/tsingliuwin)

### License/Terms of Use:

MIT-0

## Use Case:

External education consultants and postgraduate applicants use Edupath to generate China-focused kaoyan planning reports from an undergraduate major. The reports compare undergraduate employment, postgraduate paths, university tiers, industry alignment, and career outcomes with cited data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live search queries may send unnecessary personal details to external services.

Mitigation: Ask users to omit unnecessary personal details and review query content before live Baidu or education-data lookups.

Risk: Globally loading GEMINI.md or CLAUDE.md may apply their general coding and file-editing guidance outside Edupath.

Mitigation: Scope those files to this skill or review them before enabling global agent instructions.

Risk: Planning reports can become misleading if live lookup data is missing, stale, or uncited.

Mitigation: Require source labels for reported data, use the skill's MCP-first fallback flow, and review cited sources before relying on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsingliuwin/skills/edupath)
- [ClawHub publisher profile](https://clawhub.ai/user/tsingliuwin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with tables and source labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to use live Baidu search and education-data lookups, include data-source labels, and avoid uncited or future-dated claims.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
