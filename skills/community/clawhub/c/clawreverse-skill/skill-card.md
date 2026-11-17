## Description:

Inspect, checkpoint, rollback, and branch OpenClaw sessions with the ClawReverse plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuangpjlab](https://clawhub.ai/user/binhuangpjlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use ClawReverse to recover OpenClaw work after bad tool or file changes, inspect session lineage, restore checkpoints, and branch from known-good states without rerunning a long session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollback, checkout, and restore workflows can overwrite live workspace files.

Mitigation: Confirm the target agent, session, checkpoint, and desired file-restoration behavior before running mutating commands; keep a backup before using --restore-workspace.

Risk: The plugin can persist session transcripts, prompts, checkpoint records, and workspace snapshots.

Mitigation: Use it only in workspaces where this data retention is acceptable, and review configured checkpoint, registry, runtime, and reports directories.

Risk: Continue workflows can create child agents, sessions, and copied workspaces.

Mitigation: Prefer read-only listing and inspection commands first, and use --clone-auth never when auth-like settings should not be copied.

Risk: The setup workflow can modify OpenClaw configuration.

Mitigation: Review openclaw.json changes after setup and restart the OpenClaw Gateway only after confirming the plugin entry and paths.

## Reference(s):

- [ClawReverse homepage](https://github.com/OpenKILab/ClawReverse)
- [Clawreverse ClawHub release](https://clawhub.ai/binhuangpjlab/skills/clawreverse-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a working OpenClaw installation and a valid openclaw.json.]

## Skill Version(s):

0.1.0 (source: evidence release, SKILL.md frontmatter, package.json, plugin manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
