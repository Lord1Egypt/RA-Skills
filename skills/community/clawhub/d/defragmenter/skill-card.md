## Description:

Structural knowledge defragmentation for OpenClaw workspaces. Finds information, rules, and operational facts that are spread across the wrong files or embedded in the wrong layer, then rewrites them into the proper files without deleting source material. Use when the workspace feels fragmented, logic is embedded in cron/jobs instead of flow files, preferences are scattered, or facts exist but are not assembled into one coherent working structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balukov](https://clawhub.ai/user/balukov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use Defragmenter to scan OpenClaw workspaces for scattered operational knowledge, workflow rules, and preferences, then propose how to reorganize that information into the appropriate source-of-truth files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved edits can affect persistent memory, flow, container state, or preference files that shape future agent behavior.

Mitigation: Review the dry-run report before approval and confirm each proposed write is appropriate for the target source-of-truth file.

Risk: Silent or overly broad writes could alter sensitive files, skill definitions, scripts, credentials, or files outside the intended workspace.

Mitigation: Allow writes only after explicit confirmation and only to the documented allowed targets: MEMORY.md, memory/*.md, CONTAINER_STATE.md, flows/*.md, and workspace preference files.

Risk: Reorganized knowledge could be placed in the wrong file or obscure the intended source of truth.

Mitigation: Use the proposed structural change report to verify the destination and preserve source material rather than deleting it.

## Reference(s):

- [ClawHub Defragmenter skill page](https://clawhub.ai/balukov/skills/defragmenter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown dry-run reports and confirmation summaries, with approved edits to workspace Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Begins with a read-only scan; file writes require explicit user approval and are limited to allowed workspace targets.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
