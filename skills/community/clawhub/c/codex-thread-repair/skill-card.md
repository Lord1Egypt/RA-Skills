## Description:

Diagnose and safely repair one local Codex Desktop task selected by its UI title or thread ID when recent turns are missing, truncated, merged into an interrupted turn, or hidden by damaged rollout ordering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to diagnose a single damaged local Codex Desktop thread and, when the supported corruption pattern is present, prepare and apply a guarded repair with verification and rollback support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair mutates local Codex state for the selected thread.

Mitigation: Use the skill only for the documented Codex thread repair case, review diagnosis output first, and quit Codex before applying mutation.

Risk: Backups may contain broader Codex state.

Mitigation: Keep backups only until the UI is confirmed fixed, then delete relevant ~/.codex-repair-backups entries.

Risk: Ambiguous selectors could point to the wrong local task.

Mitigation: Use exact thread IDs when a title is ambiguous and do not choose a candidate by recency alone.

Risk: Unsupported rollout damage may not be safely repairable by this skill.

Mitigation: Stop on unrecognized diagnoses and avoid automatic repair outside the narrowly validated ordinal-regression and orphan-turn pattern.

## Reference(s):

- [Supported and unsupported repair patterns](references/repair-patterns.md)
- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/codex-thread-repair)
- [Source repository path](https://github.com/Songhonglei/better-agent-skills/tree/main/skills/codex-thread-repair)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and structured status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local .command launcher and backup directory during the guarded repair workflow.]

## Skill Version(s):

1.0.1 (source: target metadata, server release evidence, SKILL.md, CHANGELOG released 2026-09-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
