## Description:

Advanced handling for agent-changelog requests (history, diffs, restores, rollbacks, snapshots) using git and OpenClaw scripts with clear, user-focused summaries and outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noambens](https://clawhub.ai/user/noambens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw workspace users use this skill to inspect attributed workspace history, compare changes, create snapshots, and stage controlled file restores or rollbacks. It also supports setup guidance for automatic versioning and optional external sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automatic hooks can stage and commit tracked workspace files, and optional sync can send committed content to an external provider.

Mitigation: Enable the skill only for workspaces that need automatic versioning, narrow .agent-changelog.json before setup, and audit tracked files plus .gitignore for secrets before any remote sync.

Risk: PromptLayer pull can modify local workspace files from a remote collection.

Mitigation: Pull only from trusted PromptLayer collections and versions, review local changes first, and use force only after confirming the target snapshot.

Risk: The security evidence flags unsafe Git and PromptLayer paths that can expose or modify workspace data.

Mitigation: Prefer a release with shell-safe Git calls and validated archive extraction, and test in a disposable workspace before using it on sensitive projects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noambens/skills/agent-changelog)
- [PromptLayer API endpoint used by optional sync](https://api.promptlayer.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stage or summarize workspace file changes when invoked through its scripts and hooks.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
