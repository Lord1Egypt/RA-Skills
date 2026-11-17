## Description:

Uploads video or audio to BytePlus VOD and helps agents submit automatic OCR precision-erasure jobs for subtitles or on-screen text, returning Vid references, playback links, and processed media metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and media operations teams use this skill to upload local files or public media URLs into BytePlus VOD, then run subtitle-only or broader on-screen text erasure on selected media. Agents can guide credential setup, choose the upload or erasure workflow, produce runnable commands, and interpret JSON results or timeout resume hints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files and public media URLs can be transmitted to BytePlus/TOS using the configured credentials.

Mitigation: Use narrowly scoped BytePlus credentials, keep upload inputs to known media files, and confirm the intended VOD space before execution.

Risk: Endpoint controls are broad enough to change the VOD API host.

Mitigation: Avoid setting VOD_HOST unless necessary, and review environment configuration before running upload or erasure commands.

Risk: Precision erasure creates processed media assets in the configured VOD account.

Mitigation: Confirm the target media, space, and erasure scope; prefer the subtitle-only default unless full on-screen text erasure is required.

## Reference(s):

- [BytePlus VOD Python SDK](https://docs.byteplus.com/en/docs/byteplus-vod/docs-python-sdk)
- [BytePlus VOD precision subtitle erasure](https://docs.byteplus.com/en/docs/byteplus-vod/docs-precision-subtitle-erasure)
- [Precision erasure parameter reference](references/precise_erase.md)
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-byteplus-vod-precision-erasure)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with runnable shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BytePlus credentials and a VOD space name; upload and erasure jobs may require polling or resume commands.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, pyproject.toml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
