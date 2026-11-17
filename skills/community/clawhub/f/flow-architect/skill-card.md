## Description: <br>
流程架构师 helps agents design and validate cross-platform automation workflows with YAML DSLs, dry-run checks, idempotency keys, field mapping validation, rate limiting patterns, and generated workflow documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and automation builders use this skill to design repeatable workflows for price monitoring, inventory sync, content publishing, data processing, customer service automation, project tracking, and related operational tasks. It emphasizes dry-run validation before live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow designs may include writes, uploads, notifications, or external API calls that affect live systems. <br>
Mitigation: Review YAML destinations, affected files, API endpoints, notification channels, credentials, and dry-run results before live automation; start with manual or dry-run execution. <br>
Risk: Incorrect branch logic, field mappings, idempotency keys, or rate limit settings can cause duplicate processing, wrong data, or failed batches. <br>
Mitigation: Use sample dry runs that cover each branch, validate source-to-target mappings, define idempotency keys, and apply retry, backoff, and rate limiting before production use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML workflow definitions, Python snippets, shell commands, tables, checklists, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reusable workflow templates, dry-run checklists, idempotency guidance, field mapping validation patterns, rate limiting patterns, and documentation generation examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
