## Description: <br>
Azure Cosmos DB SDK for Python (NoSQL API) guidance for document CRUD, queries, containers, and globally distributed data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to draft Python Cosmos DB client code, container setup commands, query patterns, and configuration guidance for Azure Cosmos DB NoSQL workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples and the setup script can change live Azure Cosmos DB databases, containers, data, throughput, TTL, indexing, and cloud costs. <br>
Mitigation: Verify the endpoint, database, container, partition key, TTL, and throughput values before execution, and review or back up production data before delete, replace, upsert, batch, or throughput changes. <br>
Risk: Broad credentials or account keys could allow unintended access to Cosmos DB resources. <br>
Mitigation: Prefer least-privilege Azure Identity credentials and avoid using broad account keys unless they are explicitly required and protected. <br>


## Reference(s): <br>
- [Partition Key Strategies](references/partitioning.md) <br>
- [Query Patterns Reference](references/query-patterns.md) <br>
- [Cosmos DB Container Setup CLI Tool](scripts/setup_cosmos_container.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, shell, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
