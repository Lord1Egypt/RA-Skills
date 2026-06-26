## Description: <br>
DevOps Insight helps agents analyze incidents, troubleshoot production issues, investigate alerts, create tickets, perform root cause analysis, and support DevOps/SRE observability workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cafechen](https://clawhub.ai/user/cafechen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and DevOps engineers use this skill to collect observability context, analyze production alerts and outages, assess code-change impact, create incident tickets, and propose remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require broad access to production observability systems, databases, GitHub, and ticketing workflows. <br>
Mitigation: Use dedicated read-only or least-privilege credentials and scope each MCP server or integration to the minimum resources needed for incident review. <br>
Risk: The skill describes write-capable actions such as ticket updates, branch creation, commits, pull requests, monitoring changes, and publication. <br>
Mitigation: Require manual approval before any ticket update, repository change, monitoring change, production action, or publication. <br>
Risk: Automatic EvoMap heartbeat and publishing can share incident details outside the local environment. <br>
Mitigation: Disable EvoMap heartbeat and autoPublish unless external sharing is intended, and redact logs, service details, code diffs, customer data, secrets, and other sensitive context before publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cafechen/devops-insight) <br>
- [Model Context Protocol documentation](https://modelcontextprotocol.io/) <br>
- [GitHub CLI documentation](https://cli.github.com/) <br>
- [Kubernetes debugging documentation](https://kubernetes.io/docs/tasks/debug/) <br>
- [Apache SkyWalking documentation](https://skywalking.apache.org/) <br>
- [Elasticsearch guide](https://www.elastic.co/guide/) <br>
- [EvoMap A2A protocol](https://evomap.ai/wiki/05-a2a-protocol) <br>
- [EvoMap agent guide](https://evomap.ai/wiki/03-for-ai-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON, SQL, shell command, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include incident reports, ticket fields, fix suggestions, monitoring recommendations, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
