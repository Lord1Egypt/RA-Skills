## Description:

Patch a locally installed OpenClaw Control UI so browser tab titles show the active agent name instead of the static OpenClaw Control title.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolstar](https://clawhub.ai/user/symbolstar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and multi-agent OpenClaw users use this skill to apply, remove, or reapply a local Control UI patch that makes browser tabs easier to distinguish by active agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies an installed OpenClaw Control UI file on the local system.

Mitigation: Confirm the target index.html path before applying the patch and avoid elevated privileges unless they are required for that installation.

Risk: OpenClaw updates may overwrite the patched UI file.

Mitigation: Reapply the patch after OpenClaw updates if the browser tab title returns to the static Control UI title.

Risk: Rollback may fail or leave the UI broken if the backup is missing or the installed files changed unexpectedly.

Mitigation: Use the uninstall command first, then reinstall OpenClaw if rollback does not restore the UI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/symbolstar/skills/agent-tab-title)
- [Referenced upstream OpenClaw pull request](https://github.com/openclaw/openclaw/pull/80944)
- [Demo screenshot](https://raw.githubusercontent.com/SymbolStar/SymbolStar/main/assets/agent-tab-title-demo.png)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes apply, uninstall, custom target, verification, and rollback guidance.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
