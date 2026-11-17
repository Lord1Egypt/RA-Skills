## Description:

Converts Douyin video links into readable HTML reports by retrieving video content, extracting audio and frames, transcribing Chinese speech, analyzing visuals, and assembling a report for delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahtungl](https://clawhub.ai/user/wahtungl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize Douyin videos into reports that combine transcript and visual observations. Review consent, URL validation, command safety, and external processing before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell command construction can expose users to command-injection risk.

Mitigation: Require the publisher to replace shell-string execution with argument-vector subprocess calls and validate all user-supplied paths and URLs before release.

Risk: Network requests may fetch untrusted or unintended URLs.

Mitigation: Restrict inputs to validated Douyin hosts and run the skill with minimal network permissions until URL scoping is fixed.

Risk: The workflow processes downloaded media, audio, image frames, and delivery artifacts through external services without clearly scoped consent.

Mitigation: Require explicit user consent before downloading media, transcribing audio, analyzing images, or sending report artifacts to external services.

Risk: Broad trigger phrases may invoke the skill for ambiguous requests.

Mitigation: Narrow triggers and require confirmation when a request does not include a clear Douyin URL and reporting intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wahtungl/skills/douyin-video-to-report)
- [Publisher profile](https://clawhub.ai/user/wahtungl)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact pipeline script](artifact/douyin_pipeline.py)
- [Douyin website](https://www.douyin.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated HTML report artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local video, audio, frame, transcript, analysis, and report files during execution.]

## Skill Version(s):

1.0.0 (source: frontmatter, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
