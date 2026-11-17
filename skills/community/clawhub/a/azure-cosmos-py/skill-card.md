## Description:

Azure Cosmos DB SDK for Python (NoSQL API) guidance for document CRUD, queries, containers, and globally distributed data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegovind](https://clawhub.ai/user/thegovind)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate Python guidance, examples, and setup commands for Azure Cosmos DB NoSQL containers, item operations, queries, partitioning, throughput, indexing, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud database credentials and mutation tooling can affect Azure Cosmos DB resources if run against the wrong account or with overbroad permissions.

Mitigation: Use least-privilege Azure credentials, verify COSMOS_ENDPOINT exactly matches the intended Cosmos account endpoint, and test create/delete/throughput examples only against non-production resources first.

Risk: Broad activation terms could cause an agent to apply Cosmos DB guidance in unrelated container or document contexts.

Mitigation: Review before installing or running, and confirm the task is specifically about Azure Cosmos DB NoSQL before following generated guidance.

## Reference(s):

- [Partition Key Strategies](references/partitioning.md)
- [Query Patterns Reference](references/query-patterns.md)
- [Cosmos DB Container Setup CLI Tool](scripts/setup_cosmos_container.py)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Azure Cosmos DB SDK examples and optional container setup CLI guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
