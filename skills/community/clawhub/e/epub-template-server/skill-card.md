## Description:

智能模板发现助手 - 为 AI 应用提供强大的 epub360 模板搜索能力

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to search epub360 templates by keyword and receive structured template results for selection or presentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use a scoped or revocable API key, keep the skill out of shared or repository working directories, and confirm .env is excluded from commits.

Risk: The skill can send the API key to a configurable API endpoint.

Mitigation: Before use, verify that XBY_GAOKAO_BASE_URL is absent or set to the trusted XiaoBenYang endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/epub-template-server)
- [Publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown or text summary derived from JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before successful API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
