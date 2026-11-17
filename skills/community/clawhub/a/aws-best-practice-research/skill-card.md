## Description:

Researches, compiles, and optionally assesses AWS service best practices against official AWS documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panlm](https://clawhub.ai/user/panlm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to compile AWS HA, disaster recovery, security, and operational best-practice checklists from official AWS documentation. When read-only AWS access details are provided, it can compare live AWS resources against the generated checklist and produce an assessment report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live assessment can collect AWS infrastructure metadata, including topology, tags, events, subnet details, and security settings.

Mitigation: Use least-privilege read-only credentials and limit assessments to accounts and resources whose inventory may enter agent context or logs.

Risk: Sourcing a user-provided credential file can expose credentials or run unexpected shell content.

Mitigation: Prefer preconfigured AWS profiles or environment variables, and inspect any credential file before use.

Risk: Generated best-practice checklists or assessments can be incomplete if documentation search misses important AWS sources.

Mitigation: Review source annotations and validate findings against official AWS documentation before using results for production decisions.

## Reference(s):

- [AWS Knowledge MCP Server](https://github.com/awslabs/mcp/tree/main/src/aws-knowledge-mcp-server)
- [Assessment Workflow](references/assessment-workflow.md)
- [Output Template](references/output-template.md)
- [Search Query Templates](references/search-queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown checklist or assessment report with tables, source annotations, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local Markdown file; live assessment uses read-only AWS CLI commands when credentials, region, and resource identifiers are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
