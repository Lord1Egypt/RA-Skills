## Description:

Avatar Helper helps an agent browse a designated avatar gallery, present an avatar choice, and download the selected image locally after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to choose an avatar from a specified gallery, preview the selected image, and save it as a local avatar asset after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may proactively ask to choose an avatar and may give weak control to user preferences or cancellation requests.

Mitigation: Require explicit confirmation before browsing, selecting, or downloading, and treat user preferences and cancellation requests as authoritative.

Risk: The skill browses a specific external wallpaper site and downloads an image.

Mitigation: Confirm the site and target image URL before download, and review the selected image source before saving.

Risk: The default save path can overwrite workspace/assets/avatar.jpg.

Mitigation: Ask for the destination path or check for an existing file before writing.

## Reference(s):

- [Avatar Helper ClawHub page](https://clawhub.ai/adminlove520/skills/avatar-helper)
- [adminlove520 publisher profile](https://clawhub.ai/user/adminlove520)
- [Designated avatar gallery](https://wallpaper.dfyx.click/avatar)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with browser-action examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May browse an external avatar gallery and save the selected image to workspace/assets/avatar.jpg after confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact _meta.json and CHANGELOG.md list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
