## Description:

Analyzes Douyin videos and produces a structured report covering engagement data, content structure, visual style, captions, speech transcription, and reusable creative elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franklu0819-lang](https://clawhub.ai/user/franklu0819-lang)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and developers use this skill to inspect Douyin links or local video files and generate a Markdown breakdown of metrics, visual patterns, speech content, hooks, and reusable production tactics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video frames and audio segments may be sent to Zhipu AI for analysis and transcription.

Mitigation: Use only public or approved videos, avoid private or sensitive content unless that external processing is acceptable, and disclose the data transfer to users.

Risk: The security summary flags unsafe execution and network-scoping risks around local tools and user-provided URLs or file paths.

Mitigation: Run the skill in an isolated workspace or container, restrict inputs to trusted Douyin URLs or local files, and require shell-execution hardening plus URL allowlisting before broader deployment.

Risk: Installer and dependency behavior may change over time because the install command and dependency ranges are not fully pinned.

Mitigation: Pin installer inputs and dependency versions, review lockfile changes, and scan dependencies before release.

Risk: Temporary video, frame, and audio files may remain if analysis exits early or cleanup fails.

Mitigation: Use a dedicated temporary directory per run, inspect and delete temporary media after failures, and strengthen cleanup paths before handling sensitive media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/franklu0819-lang/skills/douyin-video-analyzer)
- [Zhipu AI chat completions endpoint](https://open.bigmodel.cn/api/paas/v4/chat/completions)
- [Zhipu AI audio transcriptions endpoint](https://open.bigmodel.cn/api/paas/v4/audio/transcriptions)
- [FFmpeg downloads](https://ffmpeg.org/download.html)
- [Douyin website](https://www.douyin.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report printed to stdout with structured sections and AI-derived analysis content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One CLI run produces one report; selected frames and audio segments are processed through Zhipu AI, and temporary media files are intended to be cleaned after analysis.]

## Skill Version(s):

3.7.4 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
