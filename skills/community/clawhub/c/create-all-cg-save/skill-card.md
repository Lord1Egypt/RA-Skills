## Description:

Finds a local single-player game's save file, identifies its format, and creates a backed-up, reversible patch to unlock CG and gallery content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixi048](https://clawhub.ai/user/xixi048)

### License/Terms of Use:

MIT

## Use Case:

Players use this skill to unlock CG, recollection rooms, galleries, or differential sprites in a local offline single-player save.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Save edits can overwrite progress or change game state beyond CG and gallery unlocks.

Mitigation: Keep a verified backup, inspect the proposed changes, and patch only fields confirmed to control the requested unlocks.

Risk: The --all option may affect switches beyond unlocks.

Mitigation: Review the dry-run report and limit changes to confirmed CG-related switches where possible.

Risk: Rollback may write to the save even when run as a dry run.

Mitigation: Treat rollback as a write operation; confirm the target and backup before running it.

## Reference(s):

- [ClawHub release](https://clawhub.ai/xixi048/skills/create-all-cg-save)
- [Publisher profile](https://clawhub.ai/user/xixi048)
- [Save format and engine guide](references/engines.md)
- [Save diff workflow](references/diff-method.md)
- [Safety guidance](references/safety.md)
- [Unlock plan schema](references/unlock-plan-schema.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [JSON diff and unlock-plan files, shell command instructions, and patched local save files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans target the user's local save and support backup and rollback.]

## Skill Version(s):

1.2.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
