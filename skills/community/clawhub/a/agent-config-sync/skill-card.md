## Description:

Synchronizes configuration versions across OpenClaw multi-agent deployments by tracking master workspace changes and dispatching pending sync updates to downstream agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevensongxx](https://clawhub.ai/user/stevensongxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep configuration, version sentinel files, changelog entries, and sync manifests aligned across two or more OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent cross-workspace sync behavior with weak safety controls and exploitable shell/path handling according to the server security summary.

Mitigation: Review and preferably fix shell eval usage, canonical path validation, confirmation flow, and manifest authentication before installation or broad rollout.

Risk: Configuration sync could move API keys or sensitive agent prompt/config files across workspaces.

Mitigation: Do not use this skill to sync API keys or sensitive agent prompt/config files unless a separate approval, signing, backup, and rollback process is in place.

Risk: The server security verdict is suspicious for this release.

Mitigation: Run dry-run previews first, limit testing to controlled OpenClaw workspaces, and review the SECURITY.md permission boundaries before enabling writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevensongxx/skills/agent-config-sync)
- [OpenClaw](https://openclaw.ai)
- [Quickstart](references/quickstart.md)
- [Sync setup](references/sync-setup.md)
- [Sync journal](references/sync-journal.md)
- [Pending sync template](references/pending-sync-template.md)
- [Agent registry](references/agent-registry.json)
- [Security model](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and generated configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run and confirmation-oriented operational guidance for local OpenClaw workspaces.]

## Skill Version(s):

1.5.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
