## Description: <br>
Queries a knowledge base using AI-powered search, combining web search with chat AI for comprehensive answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c7934597](https://clawhub.ai/user/c7934597) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to search internal knowledge bases, retrieve current web information, synthesize answers, and translate results when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic trigger phrases can route ordinary questions into internal knowledge-base or web search workflows without clear user intent. <br>
Mitigation: Configure the skill for explicit invocation and confirm that the user wants internal or external search before querying private knowledge bases or the web. <br>
Risk: Use with private knowledge bases may expose or rely on proprietary content in generated answers. <br>
Mitigation: Limit MCP access to approved knowledge bases and review deployment settings before using the skill with private or sensitive data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/c7934597/akashic-knowledge-base) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text answers with citations when search results are used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include synthesized search results, translated content, and source citations depending on the query.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
