## Description: <br>
Clawmerge helps OpenClaw users back up, restore, and merge workspaces, including disaster backups for workspace data, system configuration, cron tasks, agent authentication, and sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinoslug](https://clawhub.ai/user/sinoslug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and operators use this skill to create workspace or disaster backups, preview restores, and safely merge restored files when migrating devices or recovering an OpenClaw environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain credentials, sessions, cron definitions, environment files, and other sensitive OpenClaw configuration. <br>
Mitigation: Treat backup archives as sensitive credential archives: store them encrypted, avoid sharing them, and use --no-sessions unless session recovery is required. <br>
Risk: Restoring untrusted or unreviewed backups can alter configuration, authentication, cron jobs, dependencies, scripts, or live sessions. <br>
Mitigation: Prefer --dry-run first, avoid restoring untrusted backups, and review cron, .env, auth, session, requirements.txt, and script inventory changes before applying them. <br>
Risk: Destructive restore behavior can overwrite live OpenClaw state when explicitly requested. <br>
Mitigation: Use the default safe restore mode for normal recovery and reserve --unsafe-overwrite only for cases where overwriting the current environment is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sinoslug/clawmerge) <br>
- [Usage guide](artifact/USAGE.md) <br>
- [Skill source](artifact/SKILL.md) <br>
- [Configuration tools guide](artifact/scripts/INSTALL-CONFIG-TOOLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and backup or restore file artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce tar.gz backup archives, manifests, restore reports, candidate configuration files, and dry-run summaries.] <br>

## Skill Version(s): <br>
4.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
