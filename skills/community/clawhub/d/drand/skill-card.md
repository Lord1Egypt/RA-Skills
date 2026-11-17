## Description:

drand-mcp-server是一个提供可验证随机数的服务，用于AI应用中的模型驱动流程，支持通过时间或轮次获取随机数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to retrieve verifiable drand quicknet randomness for model-driven workflows by latest value, round, or timestamp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Xiaobenyang API key and persists it in a plaintext .env file in the working directory.

Mitigation: Install only when this credential handling is acceptable; prefer environment-scoped or non-persistent secret handling and avoid committing .env files.

Risk: Server security evidence flags a mismatch between the advertised random-number service and unrelated Gaokao/Xiaobenyang references.

Mitigation: Review the skill before installation and prefer a version that narrows the API client and documentation to the documented drand randomness calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/drand)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text summarizing JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns raw upstream JSON with success and message fields; requires a Xiaobenyang API key.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
