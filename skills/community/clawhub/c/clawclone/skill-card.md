## Description:

Backup, clone, and migrate OpenClaw data across instances, including local and cloud snapshots for workspace state, memory, skills, agents, settings, and shareable configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawclone-cc](https://clawhub.ai/user/clawclone-cc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to back up, share, migrate, and restore OpenClaw workspaces across machines or environments. It supports local archive workflows and cloud-backed clone management when a ClawClone API key is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain sensitive OpenClaw state such as memory, skills, credentials, tokens, channel state, identity, scripts, and cron data.

Mitigation: Treat backup archives, clone IDs, share tokens, and cloud copies as sensitive; share only trusted backups and avoid shared backups for secrets.

Risk: Restoring a local, cloud, or shared archive can overwrite persistent OpenClaw workspace state, skills, credentials, scripts, cron data, and configuration.

Mitigation: Use preview mode before restore, restore only archives from trusted sources, and keep the pre-restore backup until the restored instance is verified.

## Reference(s):

- [ClawClone Skill on ClawHub](https://clawhub.ai/clawclone-cc/skills/clawclone)
- [ClawClone Website](https://clawclone.cc)
- [ClawClone API Key Settings](https://clawclone.cc/dashboard/settings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local backup archives, restore previews, status reports, and cloud backup identifiers when commands are run.]

## Skill Version(s):

0.1.5 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
