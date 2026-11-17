## Description:

Helps organize Apple Photos libraries on macOS by identifying junk and duplicates, analyzing storage and photo history, and previewing cleanup and exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[and3rn3t](https://clawhub.ai/user/and3rn3t)

### License/Terms of Use:

MIT

## Use Case:

Mac users and their agents use this skill to review Photos libraries, find cleanup candidates, explore photo activity, and prepare exports before approving any changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to the Photos library exposes sensitive photo metadata.

Mitigation: Grant library read access only if comfortable with the running app accessing private photos.

Risk: Saved reports may reveal names, faces, locations, travel patterns, and shared-library participants.

Mitigation: Treat generated reports as private photos and limit where they are saved or shared.

Risk: Cleanup moves photos to Recently Deleted, and export writes copies to a folder.

Mitigation: Review each preview and approve its token-confirmed command before cleanup or export.

## Reference(s):

- [ClawHub release](https://clawhub.ai/and3rn3t/skills/apple-photos-cleaner)
- [Usage workflows](references/workflows.md)
- [Apple Photos database schema reference](references/database-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Text or Markdown guidance and commands; optional reports in JSON, Markdown, CSV, or human-readable text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis is read-only; cleanup and export require a preview and explicit confirmation.]

## Skill Version(s):

1.4.0 (source: ClawHub release, frontmatter, CHANGELOG, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
