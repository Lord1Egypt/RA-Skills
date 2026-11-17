## Description:

Selects three random AI girl portrait images from a configured local directory, shows a preview for user choice, saves the selected image as an avatar, and records the selection preference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankchi2022](https://clawhub.ai/user/frankchi2022)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users can run this skill to choose a daily avatar from a local AI portrait image collection and persist the selected image and preference record. It is intended for local personal avatar rotation and image-selection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads and writes hardcoded local paths, including the image source directory, preview workspace, avatar file, and preference record.

Mitigation: Review and configure paths before running the skill, and limit execution to a local workspace where those reads and writes are expected.

Risk: The workflow overwrites ~/.openclaw/workspace/avatars/mimi-today.png when a selection is processed.

Mitigation: Back up the current avatar or require explicit confirmation before accepting a selected image.

Risk: Selection processing may not be bound to the current preview and can use fixed or user-provided filenames from the source directory.

Mitigation: Confirm that the chosen filename matches the current preview set before copying it to the avatar path.

Risk: Preference data is written locally to .learnings/AI-GIRL-PREFERENCES.md.

Mitigation: Inspect preference contents before sharing the workspace and ensure preference records are serialized safely.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankchi2022/skills/ai-girl-selection)
- [ClawHub publisher profile](https://clawhub.ai/user/frankchi2022)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text plus generated local HTML preview, avatar image file, and markdown preference record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and local filesystem access to the configured image, preview, avatar, and preference paths.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
