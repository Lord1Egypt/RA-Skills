## Description:

POI 详情页问题排查编排器会在用户提供 gsid、traceId 或 POI 信息时，协调 sourceId 查询、日志查询、请求复现、响应解析、代码阅读和问题定位，生成结构化排查报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hnyyghk](https://clawhub.ai/user/hnyyghk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and service operators use this skill to investigate Gaode POI detail page issues by correlating sourceId mappings, Loghouse records, replayed requests, parsed response fields, and related service code. It is intended for authorized internal troubleshooting of POI modules such as contentPerson, shopBaseInfo, and shopSettlement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query sensitive internal logs and expose GSIDs, trace IDs, logged URLs, response bodies, and generated reports.

Mitigation: Use only in an authorized internal environment, treat all investigation data as sensitive, and keep outputs in private storage with cleanup.

Risk: The workflow can replay captured requests from production-like logs.

Mitigation: Require operator confirmation before log queries or request replay, validate identifiers and environment inputs, and limit replay to approved internal endpoints.

Risk: The shell script uses user-provided inputs and writes shared temporary files.

Mitigation: Tighten argument validation, quote and constrain inputs, and prefer per-run private output directories with restrictive permissions.

Risk: Some replay examples use plaintext HTTP endpoints.

Mitigation: Prefer HTTPS where supported and restrict use to approved internal networks when plaintext endpoints are unavoidable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hnyyghk/skills/gaode-c3-us-shop)
- [POI 详情页模块 - sourceId 映射表](references/source_id_map.md)
- [POI 详情页关键字段说明](references/fields.md)
- [POI Debug Orchestrator FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown investigation report with shell command snippets and optional JSON response artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may save local investigation outputs under temporary paths such as /tmp/poi-debug-results/ and /tmp/poi_response_*.json.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json; artifact SKILL.md frontmatter reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
