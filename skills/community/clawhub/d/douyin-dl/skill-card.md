## Description:

Downloads Douyin short videos from supported Douyin URLs by opening the page in a headless browser, extracting the video source, and downloading the MP4 with curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lskun](https://clawhub.ai/user/lskun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save Douyin clips from supported video page, search modal, share, and note URLs as local MP4 files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader script can execute local shell commands if given crafted URLs, filenames, output paths, or page-controlled video sources.

Mitigation: Review before installing; use only trusted Douyin URLs, filenames, and output directories until shell command construction, domain validation, filename sanitization, and dependency pinning are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lskun/skills/douyin-dl)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown with shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MP4 video files when executed; requires agent-browser and curl.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
