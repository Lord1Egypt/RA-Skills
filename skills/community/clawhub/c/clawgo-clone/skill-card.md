## Description:

Downloads a zip from clawgo.me by key, backs up current OpenClaw workspace Markdown, and copies selected archive files into the local workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenjunyeee](https://clawhub.ai/user/chenjunyeee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw operators use this skill to restore or synchronize workspace instruction files from a 12-character ClawGo key while retaining backups of current files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A ClawGo key can resolve to an unauthenticated remote zip that replaces persistent OpenClaw instruction files.

Mitigation: Use keys only from trusted providers, inspect archive contents and diffs before restore, and require per-file approval before replacing workspace files.

Risk: Weak staging and validation controls can allow unsafe archive contents or unexpected file replacement behavior.

Mitigation: Use private temporary directories, validate zip members before extraction, and prefer signed manifests or verified hashes for downloaded payloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenjunyeee/skills/clawgo-clone)
- [ClawGo service](https://clawgo.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file-operation summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May copy selected Markdown files into ~/.openclaw/workspace after explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
