## Description:

Downloads Douyin videos individually or in batches, with duplicate handling, watermark-free retrieval, and automatic backend selection through yt-dlp or Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to download public Douyin videos from single URLs or batch link files into a local output directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted or malformed URLs may be passed to the browser or downloader tools.

Mitigation: Accept only real Douyin HTTPS URLs and reject non-Douyin or non-HTTPS inputs before execution.

Risk: Custom output directories or filenames may create unsafe file paths.

Mitigation: Use a dedicated output directory and reject filenames containing path separators or .. components.

Risk: The browser is launched with sandboxing disabled.

Mitigation: Run the skill only in an isolated, unprivileged environment and avoid elevated privileges.

Risk: Privileged installation guidance for yt-dlp can install an unverified binary.

Mitigation: Install yt-dlp through a trusted package manager or verify the downloaded binary before placing it on PATH.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/skills/douyin-video-download)
- [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance]

**Output Format:** [CLI console text and local MP4 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads depend on network access, Douyin page availability, Playwright Chromium, and optional yt-dlp.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
