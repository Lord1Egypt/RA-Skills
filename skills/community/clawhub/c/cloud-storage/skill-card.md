## Description: <br>
Manage files across cloud providers with authentication, cost awareness, and multi-provider operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to upload, download, sync, and manage files across object storage and consumer cloud storage providers while accounting for authentication, rate limits, verification, and costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud storage credentials or tokens could be exposed through chat, logs, or overly broad credential use. <br>
Mitigation: Use least-privilege credentials, prefer managed identity or short-lived credentials, and avoid pasting real secrets into chat or logs. <br>
Risk: Bulk transfers, permission changes, or deletes could affect large amounts of data if executed without review. <br>
Mitigation: Require explicit review before bulk operations, verify backups are restorable before deletion, and define checksum, count, or spot-check verification before execution. <br>
Risk: Large transfers can create unexpected egress, API, or storage costs. <br>
Mitigation: Estimate transfer, operation, and storage costs before large operations and re-check current provider pricing. <br>


## Reference(s): <br>
- [Cloud Storage skill page](https://clawhub.ai/ivangdavila/cloud-storage) <br>
- [Provider-Specific Patterns](artifact/providers.md) <br>
- [Authentication Setup](artifact/auth.md) <br>
- [Cost Calculation](artifact/costs.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with checklists, tables, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no bundled executable tools or required binaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
