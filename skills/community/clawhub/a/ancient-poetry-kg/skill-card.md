## Description:

围绕中国古代诗词名称，作者，朝代，经典词句的知识图谱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query an ancient Chinese poetry knowledge graph for schema information and read-only Cypher query results about poems, authors, dynasties, and notable lines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the Xiaobenyang API key in a local plaintext .env file.

Mitigation: Use a low-privilege, revocable key and remove or protect the .env file after use.

Risk: The skill sends graph queries and API credentials to an external Xiaobenyang service.

Mitigation: Install and use it only if the service is trusted, and avoid submitting sensitive queries.

Risk: The artifact contains mismatched poetry and gaokao documentation, which may confuse expected behavior.

Mitigation: Review the tool descriptions and confirm they match the intended ancient-poetry graph before approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/ancient-poetry-kg)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API responses, Configuration guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key and returns schema or read-only Cypher query results from the upstream service.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
