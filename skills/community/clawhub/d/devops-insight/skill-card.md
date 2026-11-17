## Description:

DevOps Insight helps DevOps and SRE teams analyze alerts, troubleshoot production incidents, create incident tickets, assess code-change impact, and recommend fixes using monitoring, GitHub, ticket, and EvoMap integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cafechen](https://clawhub.ai/user/cafechen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DevOps engineers, and SRE teams use this skill to investigate production alerts and outages, correlate monitoring and code-change evidence, generate incident reports or tickets, and propose remediation steps. The skill can also publish incident knowledge as EvoMap Capsules and Genes when that workflow is enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can combine broad production monitoring access with ticket, branch, pull request, or production-change workflows.

Mitigation: Use read-only and tightly scoped MCP, GitHub, and ticket credentials where possible, and require explicit human confirmation before mutation-capable actions.

Risk: Automatic EvoMap heartbeat or publishing can send incident knowledge outside the local environment.

Mitigation: Disable EvoMap heartbeat and autoPublish unless the organization has approved the destination, payload content, and data handling requirements.

Risk: Monitoring data, logs, tickets, and incident reports may contain credentials, user data, or other sensitive operational details.

Mitigation: Sanitize sensitive information before creating tickets, reports, pull requests, or EvoMap Capsules and Genes.

Risk: The database setup script is not suitable for non-disposable environments without review.

Mitigation: Fix and review the database setup script before using it outside a disposable environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cafechen/skills/devops-insight)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [GitHub CLI Documentation](https://cli.github.com/)
- [Kubernetes Debugging Documentation](https://kubernetes.io/docs/tasks/debug/)
- [Apache SkyWalking Documentation](https://skywalking.apache.org/)
- [Elasticsearch Query Guide](https://www.elastic.co/guide/)
- [EvoMap A2A Protocol](https://evomap.ai/wiki/05-a2a-protocol)
- [EvoMap Agent Guide](https://evomap.ai/wiki/03-for-ai-agents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON snippets, SQL, shell commands, configuration examples, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include incident reports, health reports, ticket payloads, root-cause analyses, pull request or branch suggestions, monitoring recommendations, and EvoMap Capsule or Gene publishing guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
