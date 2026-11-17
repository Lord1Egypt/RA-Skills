## Description: <br>
Cloud Manager helps agents manage cloud-storage workflows across multiple providers, including unified file views, migrations, sharing permissions, scheduled backups, storage analysis, version comparison, deduplication, and cross-provider search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, families, and small teams use this skill to coordinate cloud-storage administration tasks such as multi-cloud browsing, file migration, shared-folder permissions, scheduled backups, cleanup, and storage reporting. Use it only for explicit cloud-storage management requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud-storage operations may change permissions, migrate files, delete data, prune version history, run cleanup or deduplication, or create scheduled backups. <br>
Mitigation: Require explicit user confirmation before any permission change, migration, cleanup, deduplication, version-history pruning, scheduled backup, or destructive command. <br>
Risk: Commands may touch OAuth credentials or cloud-account configuration. <br>
Mitigation: Confirm credential-related commands manually, keep tokens out of skill files and version control, and limit credential access to the intended cloud-storage task. <br>
Risk: The scanner reports poor scoping and mismatched generic review behavior. <br>
Mitigation: Route only explicit cloud-storage management tasks to this skill and avoid using it for generic analytics, code review, or unrelated requests. <br>


## Reference(s): <br>
- [Cloud Manager on ClawHub](https://clawhub.ai/thcjp/skills/cloud-manager) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and structured JSON-style responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cloud-provider CLI commands and configuration changes that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
