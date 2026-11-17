## Description:

Furnace temperature and control manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators evaluating this third-party CLI can use it to record, list, search, export, and configure local furnace-labeled entries. Server security evidence says it should not be trusted for furnace or industrial-control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is materially mislabeled as furnace control while behaving like a local record store.

Mitigation: Do not use it for furnace, safety, or industrial-control workflows; restrict evaluation to non-critical local records.

Risk: Unsafe command handling could run unintended local commands.

Mitigation: Avoid untrusted config or add values, and review the shell script before execution.

Risk: Export and remove operations modify files in the current working directory or local data store.

Mitigation: Run only in a disposable working directory and back up any local data before using export or remove.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/furnace)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured stdout from shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSONL storage under the configured FURNACE_DIR, defaulting to ~/.furnace/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
