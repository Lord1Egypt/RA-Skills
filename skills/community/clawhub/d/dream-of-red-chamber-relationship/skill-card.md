## Description:

关于《红楼梦》人物之间关系的知识图谱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can query a Dream of the Red Chamber relationship graph by retrieving graph schema information and running read-only Cypher queries through the XiaoBenYang service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a XiaoBenYang API key in plaintext in a local .env file.

Mitigation: Use a dedicated low-privilege key, keep .env out of commits and shared logs, and prefer secure secret storage where available.

Risk: The skill depends on remote API calls to an upstream service.

Mitigation: Install and use it only when the publisher and upstream service are trusted, and review returned data before relying on it.

Risk: The artifact contains inconsistent project/domain references.

Mitigation: Review the release before installation and prefer a version with unrelated scaffolding removed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/dream-of-red-chamber-relationship)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Guidance]

**Output Format:** [Markdown summaries of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and remote API access.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
