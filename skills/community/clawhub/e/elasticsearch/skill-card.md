## Description:

Elasticsearch helps agents design, query, debug, and operate Elasticsearch clusters, covering mappings, analyzers, query DSL, aggregations, indexing, shard sizing, security, vector search, lifecycle management, snapshots, upgrades, and cluster health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, search engineers, and operators use this skill to draft, review, and troubleshoot Elasticsearch requests, mappings, analyzers, aggregations, indexing workflows, lifecycle plans, and operational runbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Elasticsearch requests may change cluster state or data, including deletes, reindexing, alias swaps, force merges, and cluster settings.

Mitigation: Review cluster-changing requests before running them and prefer reviewed request output for destructive operations.

Risk: Credentials or sensitive cluster details could be exposed if users place them in examples or local memory/config files.

Mitigation: Keep real credentials out of prompts, examples, and files under ~/Clawic/data/elasticsearch/.

Risk: Operational guidance can be incorrect for a specific deployment, managed service, OpenSearch variant, version, or license tier.

Mitigation: Set deployment type, major version, client, and license tier before applying generated requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/elasticsearch)
- [Clawic Elasticsearch skill page](https://clawic.com/skills/elasticsearch)
- [Elasticsearch skill source](artifact/SKILL.md)
- [Setup and local preferences](artifact/setup.md)
- [Security guidance](artifact/security.md)
- [Incident operations](artifact/incidents.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Elasticsearch REST examples, shell commands, JSON request bodies, configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before applying cluster-changing requests.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
