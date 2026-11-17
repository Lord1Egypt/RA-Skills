## Description:

Generates comprehensive AWS service chaos engineering and high availability testing research reports using a Scenario-Library-first workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panlm](https://clawhub.ai/user/panlm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud reliability engineers, and platform teams use this skill to research chaos engineering and HA validation plans for specific AWS services. It discovers AWS FIS Scenario Library coverage, region-specific FIS actions, service failover methods, stop conditions, and prioritized test recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include sensitive architecture details if the user provides them.

Mitigation: Avoid entering secrets or sensitive infrastructure details unless they are appropriate to store in the generated Markdown report.

Risk: Chaos engineering recommendations can cause service impact if implemented without review.

Mitigation: Review blast radius, stop conditions, region, target resources, and approvals before creating or running any AWS FIS experiment.

Risk: AWS FIS action availability and Scenario Library content can vary by region and over time.

Mitigation: Resolve the target region and re-run documentation and action discovery before using recommendations for live testing.

## Reference(s):

- [AWS Knowledge MCP Server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server)
- [AWS FIS Actions Reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html)
- [Search Query Templates](artifact/references/search-queries.md)
- [Report Output Template](artifact/references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report saved as a local file, with a brief terminal summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output follows the user's language and includes scenario matrices, priorities, stop conditions, references, and next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
