## Description:

Echo syncs, encodes, embeds, and upserts OpenClaw markdown memory files to Supabase, with commands to restore files and check sync status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkw-21](https://clawhub.ai/user/kkw-21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Echo to synchronize OpenClaw markdown memory files between a local workspace and Supabase, including backup, restore, and sync status workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local agent memory files to Supabase, and the evidence does not define enough safeguards or scope for sensitive memory handling.

Mitigation: Use dry-run first, confirm the exact files selected for sync, verify the Supabase destination and credentials, and avoid syncing memories containing secrets, personal data, project details, or credentials.

Risk: The restore command can write markdown memory files back from Supabase to the local workspace.

Mitigation: Review restore targets and expected diffs before writing, and only restore from a trusted Supabase project controlled by the user or organization.

## Reference(s):

- [Echo ClawHub skill page](https://clawhub.ai/kkw-21/skills/echo-memory)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands include sync, restore, status, dry-run, and incremental sync options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
