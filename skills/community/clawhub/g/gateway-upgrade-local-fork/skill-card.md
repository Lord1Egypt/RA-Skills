## Description: <br>
Gateway Upgrade Local Fork guides local OpenClaw gateway upgrades through preflight checks, backups, service environment merging, verification, and rollback planning without forwarding data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent plan and assist with local OpenClaw gateway upgrades, especially preserving custom service environment variables, checking qmd and GPU health, rebuilding per-agent indexes, and preparing rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter local OpenClaw services and per-agent qmd databases. <br>
Mitigation: Confirm fresh service and database backups exist before running upgrade, rebuild, restart, or rollback commands. <br>
Risk: Reports and diff output can expose raw environment values. <br>
Mitigation: Redact environment values before sharing generated reports, logs, or command output. <br>
Risk: Rollback and cleanup examples include destructive deletion commands. <br>
Mitigation: Replace destructive cleanup with a confirmed rename or two-step deletion process and verify the target path before removal. <br>
Risk: The qmd rebuild script contains a sample agent list that may not match the local installation. <br>
Mitigation: Review and edit the agent list before rebuilding indexes so the command only targets intended agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/gateway-upgrade-local-fork) <br>
- [Preflight checks](references/01-preflight.md) <br>
- [Backup procedure](references/02-backup.md) <br>
- [Upgrade and environment merge](references/03-upgrade.md) <br>
- [Postflight checks](references/04-postflight.md) <br>
- [Verification](references/05-verify.md) <br>
- [Rollback](references/06-rollback.md) <br>
- [Operational notes](references/80-notes.md) <br>
- [qmd releases](https://github.com/tobi/qmd/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown procedures with inline bash commands and shell script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local OpenClaw service and database maintenance guidance; no credentials required.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
