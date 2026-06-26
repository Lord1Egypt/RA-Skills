## Description: <br>
OpenClaw Cloudways integration reference and workflow guide for creating, editing, reviewing, debugging, or extending the built-in Cloudways feature across account auth, inventory, vault-backed credentials, WordPress review flows, DB Manager access, guarded SQL execution, and the Control UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Cloudways/OpenClaw operators use this skill to maintain the Cloudways integration workflow, including account setup, inventory loading, secure credential handling, WordPress review metadata, DB access testing, guarded SQL execution, and related UI behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow involves Cloudways, WordPress, SSH/SFTP, database, and vault-backed credentials that could expose sensitive operational access if copied into shared packages or prompts. <br>
Mitigation: Keep live credentials, API keys, DB Manager URLs, server/app IDs, SSH keys, passwords, and local secrets/config files out of shared artifacts; use placeholders and scrubbed examples only. <br>
Risk: Database write queries can affect production data. <br>
Mitigation: Verify the actual OpenClaw implementation before use, use least-privilege accounts where possible, require the documented confirmation phrase, prefer dry-run review, and retain audit logging for write attempts. <br>
Risk: DB Manager automation and Cloudways API behavior may fail or change with remote platform updates. <br>
Mitigation: Treat connection tests, inventory refreshes, and DB access checks as live operational validation steps before relying on generated guidance for real sites. <br>


## Reference(s): <br>
- [Cloudways Integration Implementation](references/implementation.md) <br>
- [Cloudways Gateway Methods](references/request-methods.md) <br>
- [Cloudways API Notes For This Integration](references/cloudways-api-notes.md) <br>
- [Cloudways UI Design](references/ui-design.md) <br>
- [Cloudways Integration on ClawHub](https://clawhub.ai/maverick-software/cloudways-integration) <br>
- [Publisher Profile](https://clawhub.ai/user/maverick-software) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code, shell command, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include implementation notes, operational checklists, API behavior, UI guidance, guarded SQL guidance, and scrubbed example payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
