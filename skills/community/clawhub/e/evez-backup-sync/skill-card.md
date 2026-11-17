## Description:

Auto-backup and sync engine for AI agent workspaces. Git commit and push to GitHub on schedule. Supabase cloud backup for critical state. mem0 persistent memory for knowledge retention. Full state snapshot every 15 minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run scheduled backups for an AI agent workspace, including git pushes, Supabase state backups, mem0 memory saves, and status/API access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful git, cloud backup, and memory operations through an unauthenticated network service.

Mitigation: Run it only in an isolated environment, bind it to localhost, and add authentication before giving it workspace, git, Supabase, or memory access.

Risk: Backup endpoints can commit and push broad workspace changes or sync sensitive state to external services.

Mitigation: Replace broad git staging with an allowlist, verify configured remotes and credentials, and restrict Supabase and memory endpoints to approved data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-backup-sync)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, bash commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local backup state, commit workspace changes, push git remotes, and sync data to configured Supabase or mem0 services when run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
