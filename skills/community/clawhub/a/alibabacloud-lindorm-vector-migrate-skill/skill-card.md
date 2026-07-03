## Description: <br>
Helps agents migrate vector data from Milvus, Elasticsearch, Lindorm, Qdrant, or CSV files in OSS to Alibaba Cloud Lindorm by collecting parameters, generating migration code, running pre-checks, and validating results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and run vector database migrations into Alibaba Cloud Lindorm Search Engine, including schema mapping, target index creation, checkpoint resume, post-migration validation, and source-specific application code migration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration scripts may run database operations with sensitive credentials. <br>
Mitigation: Review scripts before execution, pass credentials through environment variables or runtime prompts, and use least-privilege temporary credentials. <br>
Risk: Migration actions can create, overwrite, clear, or delete target indexes. <br>
Mitigation: Test in staging, take backups, and require explicit confirmation before target index creation, overwrite, clear, or deletion. <br>
Risk: Plain HTTP credential examples can expose secrets on untrusted networks. <br>
Mitigation: Prefer TLS/HTTPS or private trusted networks and avoid pasting real passwords into command lines or chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-lindorm-vector-migrate-skill) <br>
- [Migration workflow](references/01-dev/workflow.md) <br>
- [Milvus migration guide](references/01-dev/milvus-migrate.md) <br>
- [Elasticsearch migration guide](references/01-dev/elasticsearch-migrate.md) <br>
- [Lindorm migration guide](references/01-dev/lindorm-migrate.md) <br>
- [Qdrant migration guide](references/01-dev/qdrant-migrate.md) <br>
- [CSV import from OSS](references/01-dev/csv-import.md) <br>
- [Checkpoint resume](references/02-ops/checkpoint-resume.md) <br>
- [Post-migration validation](references/02-ops/postcheck.md) <br>
- [Type mapping](references/03-ref/type-mapping.md) <br>
- [Bulk write and index operations](references/03-ref/bulk-write.md) <br>
- [Official documentation references](references/03-ref/official-refs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate migration scripts and operational checklists that require user confirmation before execution.] <br>

## Skill Version(s): <br>
0.0.1-beta.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
