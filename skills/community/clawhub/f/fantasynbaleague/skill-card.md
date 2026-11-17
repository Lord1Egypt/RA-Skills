## Description:

一个为Fantasy NBA以色列联赛提供统计数据、排名和分析的MCP服务器。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Fantasy NBA Israel league teams, standings, rotisserie rankings, shooting totals, team details, and player statistics through the XiaoBenYang service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in plaintext in a local .env file.

Mitigation: Use a dedicated, limited-privilege key, keep the working directory private, and remove stale credentials when the skill is no longer needed.

Risk: The skill depends on the external XiaoBenYang service for Fantasy NBA data.

Mitigation: Install and use it only when you trust the XiaoBenYang service and are comfortable sending requests to that provider.

Risk: The security evidence reports mismatched configuration names related to gaokao.

Mitigation: Review the local configuration before installation and remove or correct stale gaokao settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/fantasynbaleague)
- [XiaoBenYang service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries of JSON API results and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key before API-backed results can be returned.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
