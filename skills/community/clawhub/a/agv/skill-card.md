## Description:

Agv is presented as an automated guided vehicle route planner, while server security review identifies this artifact as a local record store with status, add, list, search, remove, export, stats, and config commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill to run a local command-line record manager for AGV-related entries, exports, and configuration. It should not be used as an operational AGV route planner or status system without correcting the documented purpose mismatch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact is advertised as an AGV route planner, but server security review says it behaves like a generic local record store.

Mitigation: Do not use it for safety-critical AGV routing or operational status decisions unless the implementation is corrected and independently validated.

Risk: The script writes persistent data, can delete entries, can export files, and can change configuration.

Mitigation: Run it with a controlled AGV_DIR in a non-production workspace and review delete, export, and config commands before execution.

Risk: Server security guidance identifies an unsafe config update path and shell escaping concerns.

Mitigation: Avoid untrusted input for config and search operations until input handling is fixed and retested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/agv)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text command output with optional JSONL or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AGV_DIR to choose the local data directory; defaults to ~/.agv.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
