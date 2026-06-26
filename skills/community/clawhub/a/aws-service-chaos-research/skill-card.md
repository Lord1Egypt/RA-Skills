## Description: <br>
Use when the user asks about chaos engineering, fault injection, resilience testing, or HA verification for a specific AWS service such as RDS, EKS, MSK, ElastiCache, DynamoDB, S3, Lambda, or OpenSearch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panlm](https://clawhub.ai/user/panlm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and reliability engineers use this skill to research AWS service-specific chaos engineering and high availability verification plans. It produces structured markdown reports that prioritize AWS FIS Scenario Library coverage, regional FIS action availability, service-specific failure modes, stop conditions, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use the local AWS CLI profile to list regional FIS actions. <br>
Mitigation: Run it with a least-privilege AWS profile and confirm the target region before relying on the action inventory. <br>
Risk: Chaos-testing recommendations or command examples could affect production resilience work if applied without review. <br>
Mitigation: Treat reports as planning guidance and require manual approval before creating or running any FIS experiments or failover actions. <br>
Risk: The skill writes timestamped markdown reports to the local filesystem. <br>
Mitigation: Review generated files for environment details before sharing them outside the intended team. <br>


## Reference(s): <br>
- [AWS Knowledge MCP Server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server) <br>
- [AWS FIS Actions Reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html) <br>
- [Search Query Templates](references/search-queries.md) <br>
- [Output Template](references/output-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/panlm/aws-service-chaos-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report files with tables, prioritized scenarios, command examples, references, and terminal summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved locally with timestamped service-specific filenames; output language follows the user's input language.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
