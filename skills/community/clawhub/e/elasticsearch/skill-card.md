## Description: <br>
Query and index Elasticsearch with proper mappings, analyzers, and search patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as Elasticsearch reference guidance for mapping design, query construction, indexing patterns, pagination, aggregation behavior, and common operational errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-proposed Elasticsearch actions can change data or cluster state, including reindexing, bulk indexing, ILM deletion, cluster-setting resets, and closing indices. <br>
Mitigation: Confirm the target cluster and review any data-changing or cluster-state-changing command before approval. <br>
Risk: Incorrect mapping, analyzer, pagination, or aggregation guidance can affect search behavior or indexing outcomes. <br>
Mitigation: Review proposed mappings and queries against the intended index design and test changes in a non-production environment before applying them to critical clusters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Elasticsearch examples and command-oriented recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl when command examples are used; no credentials or persistent code are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
