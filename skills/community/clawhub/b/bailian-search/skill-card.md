## Description:

Real-time web search powered by Alibaba Cloud Bailian (DashScope) MCP service for latest news, real-time information, current events, and facts that may have changed recently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengxi](https://clawhub.ai/user/zengxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent retrieve current web search results through Alibaba Cloud Bailian DashScope when answering time-sensitive questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Alibaba Cloud DashScope.

Mitigation: Do not submit secrets, private internal data, or regulated personal information as search queries; use this skill only where DashScope use is acceptable.

Risk: Persistently storing DASHSCOPE_API_KEY in a shell profile can leave a long-lived credential on disk.

Mitigation: Prefer a temporary environment variable or managed OpenClaw environment configuration, and rotate the key if it is exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zengxi/skills/bailian-search)
- [Alibaba Cloud Bailian Console](https://bailian.console.aliyun.com)
- [DashScope Documentation](https://help.aliyun.com/document_detail/611474.html)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Plain text search results with titles, URLs, and snippets; setup guidance may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY; optional result count defaults to 5.]

## Skill Version(s):

1.1.0 (source: release metadata, package.json, README.md, search.sh, and changelog dated 2026-03-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
