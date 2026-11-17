## Description:

Use when you need to turn a local source video and one product image into a single-product placement video with the DPP pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kotot](https://clawhub.ai/user/kotot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video pipeline operators use this skill to run a staged single-product placement workflow from local video and product-image assets. It guides storyboard generation, material configuration, placement selection, best-segment composition, and final video assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends local media and media metadata to configurable Ark and TOS network endpoints.

Mitigation: Use only trusted endpoints, run the skill in an isolated workspace, and avoid processing sensitive or unreleasable media.

Risk: Credentials are required for Ark and may be required for TOS uploads.

Mitigation: Keep credentials narrowly scoped, store them only in the target workspace environment, and verify TOS settings before compose-best auto-upload.

Risk: Generated logs can contain prompts, media URLs, and task metadata.

Mitigation: Review and redact the log directory before sharing or publishing any generated artifacts.

## Reference(s):

- [DPP Commands](references/commands.md)
- [DPP Pipeline Runtime](references/runtime-readme.md)
- [Environment Example](references/env-example.txt)
- [ClawHub Skill Page](https://clawhub.ai/kotot/skills/dpp-pipeline)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline bash commands and workspace file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow creates JSON analysis files, reference clips, logs, and a final video artifact in the caller workspace.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
