## Description: <br>
Production deployment checklist for AI agent infrastructure covering dedicated Mac Mini and server deployments with base installation, IAM configuration, client software setup, security hardening, memory scaffolding, starter crons, and day-1 onboarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and deployment engineers use this skill to plan and check production AI agent deployments on dedicated client hardware. It is intended for client onboarding, infrastructure setup, security hardening, monitoring, backup planning, and day-1 validation, not for cloud/serverless or containerized deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential and secret handling is sensitive for production client agent systems. <br>
Mitigation: Use one defined secret-management approach, keep credentials out of git, restrict .env permissions, scope tokens to each client, and document rotation. <br>
Risk: Backups may copy client memory, secrets, logs, or cron metadata into less-protected storage. <br>
Mitigation: Narrow backup scope, exclude secrets where possible, encrypt backups, restrict access, and verify restores only in protected environments. <br>
Risk: Installer and API-check snippets can perform network downloads or live service calls. <br>
Mitigation: Review commands before execution, use pinned and verified installers where possible, and run validation calls with least-privilege credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samledger67-dotcom/agent-deployment-checklist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown checklists with bash snippets, cron templates, and markdown file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-reviewed deployment checklist material; it does not automatically install or configure infrastructure.] <br>

## Skill Version(s): <br>
98.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
