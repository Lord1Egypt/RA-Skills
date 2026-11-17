## Description:

Generates Korean SNS copy, images, and optional 20-second videos for Gyeonggi Provincial Office of Education Startup and Employment Support Center posts triggered by /가자고.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sang-su0916](https://clawhub.ai/user/sang-su0916)

### License/Terms of Use:

MIT-0

## Use Case:

Communications staff and agents use this skill to turn Korean source text, keywords, and optional photos into channel-specific Instagram, Facebook, and Band promotional content. It can also guide creation of branded image assets and a short slideshow video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes a Gemini API key.

Mitigation: Revoke the exposed key, remove it from the skill text, and require users to provide GEMINI_API_KEY through their own environment.

Risk: The skill uses hardcoded local paths, outputs, and background service commands.

Mitigation: Make input paths, output directories, and service startup explicit user-configurable options before installation or execution.

Risk: Generated content may be shared through Telegram or other third-party channels.

Mitigation: Require an explicit opt-in before external sharing and clearly show which files or messages will be sent.

Risk: The workflow may download external media for background music.

Mitigation: Bundle approved media or verify downloaded files with integrity checks before use.

Risk: Video scripts include hardcoded local photos and scene text.

Mitigation: Update the scripts to honor user-supplied inputs and fail clearly when required inputs are missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sang-su0916/skills/gajago-sns)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, channel-specific SNS copy, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Instagram, Facebook, and Band copy; image asset instructions; and an optional 20-second MP4 slideshow workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
