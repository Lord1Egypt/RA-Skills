## Description: <br>
Alibaba Cloud Lindorm cloud native multi-model database Skill covering operations management, monitoring, troubleshooting, backup, migration, permissions, SQL development, search, vector retrieval, AI engine calls, multimodal search, and knowledge base search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to answer Alibaba Cloud Lindorm development and operations questions, prepare SQL and CLI workflows, troubleshoot instances, and understand search, vector, AI, and knowledge-retrieval patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents that use Alibaba Cloud credentials and Lindorm database access. <br>
Mitigation: Use least-privilege RAM credentials, prefer read-only access where possible, and avoid pasting secrets into chat or shell commands. <br>
Risk: Generated SQL or CLI actions could write data, delete data, change permissions, disable SSL, or remove safe-mode protection. <br>
Mitigation: Require explicit human review before executing high-impact SQL or cloud commands. <br>
Risk: Local CLI installation or downloads may affect the user's environment. <br>
Mitigation: Verify downloaded CLI tools manually before installation or use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-lindorm-agent-skill) <br>
- [AI Guide](references/01-dev/ai-guide.md) <br>
- [Connection Guide](references/01-dev/connection-guide.md) <br>
- [Knowledge Search Scene](references/01-dev/knowledge-search-scene.md) <br>
- [Multimodal Search Scene](references/01-dev/multimodal-search-scene.md) <br>
- [Quick Start Guide](references/01-dev/quick-start-guide.md) <br>
- [Search Guide](references/01-dev/search-guide.md) <br>
- [SQL Client Guide](references/01-dev/sql-client-guide.md) <br>
- [SQL Operations](references/01-dev/sql-operations.md) <br>
- [SQL Usage Notes](references/01-dev/sql-usage-notes.md) <br>
- [Table Design](references/01-dev/table-design.md) <br>
- [Vector Guide](references/01-dev/vector-guide.md) <br>
- [Backup Restore](references/02-ops/backup-restore.md) <br>
- [Connection Troubleshoot](references/02-ops/connection-troubleshoot.md) <br>
- [Data Migration](references/02-ops/data-migration.md) <br>
- [Error Troubleshoot](references/02-ops/error-troubleshoot.md) <br>
- [Instance Management](references/02-ops/instance-management.md) <br>
- [Monitoring Guide](references/02-ops/monitoring-guide.md) <br>
- [Slow Query Analysis](references/02-ops/slow-query-analysis.md) <br>
- [Storage Analysis](references/02-ops/storage-analysis.md) <br>
- [User Permission](references/02-ops/user-permission.md) <br>
- [Acceptance Criteria](references/03-ref/acceptance-criteria.md) <br>
- [CLI Installation Guide](references/03-ref/cli-installation-guide.md) <br>
- [HBase Shell Guide](references/03-ref/hbase-shell-guide.md) <br>
- [Lindorm CLI Guide](references/03-ref/lindorm-cli-guide.md) <br>
- [RAM Policies](references/03-ref/ram-policies.md) <br>
- [Related Commands](references/03-ref/related-commands.md) <br>
- [Verification Method](references/03-ref/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline SQL, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should cite the bundled skill documents or official Alibaba Cloud documentation for Lindorm-specific answers.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
