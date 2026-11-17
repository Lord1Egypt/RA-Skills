## Description:

clawsync helps agents back up, migrate, restore, and serve OpenClaw state using Git-native workflows, local archives, restore safety checks, and token-protected archive access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linsheng9731](https://clawhub.ai/user/linsheng9731)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide OpenClaw backup, migration, restore, remote branch pruning, periodic backup, and local archive serving workflows. It is intended for agents helping users preserve or move OpenClaw state while applying dry-run, confirmation, and token-handling safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow executes a mutable remote GitHub script directly in the shell.

Mitigation: Review or download the installer before execution, prefer an immutable commit or release with checksum or signature verification, and avoid sudo.

Risk: Backups and archives may contain sensitive OpenClaw state such as configuration, credentials, sessions, and tokens.

Mitigation: Keep backup remotes private, use the skill's sanitization guidance, protect archives, and avoid sharing generated tokens or archive contents.

Risk: Restore operations can overwrite or merge local OpenClaw state.

Mitigation: Run dry-runs first, review high-risk paths, require explicit confirmation before applying changes, and preserve pre-restore snapshots.

Risk: The local archive server can expose backup data if made reachable without sufficient protections.

Mitigation: Use a strong token, keep the service local or behind appropriate network controls, and avoid direct public exposure without TLS or a reverse proxy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linsheng9731/skills/clawgitsync)
- [Installer script referenced by artifact](https://raw.githubusercontent.com/linsheng9731/clawsync/main/scripts/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup and restore checklists, dry-run guidance, command sequences, and token-handling reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
