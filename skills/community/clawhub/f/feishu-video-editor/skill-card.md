## Description:

Feishu Video Editor helps an agent download videos from Feishu cloud space, trim silence, crop by timestamp, generate Whisper-based subtitles, extract audio, and return edited results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using Feishu can use this skill to automate common video-editing tasks such as silence removal, timestamp cropping, subtitle generation, audio extraction, and result sharing through Feishu cloud space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command handling could allow crafted video paths or timestamps to run unintended system commands.

Mitigation: Run only in a constrained account or sandbox until shell execution is replaced with execFile or spawn argument arrays and paths and timestamps are validated.

Risk: Processed videos, extracted audio, generated subtitles, and uploaded results may contain sensitive content.

Mitigation: Treat generated files as sensitive, review retention and sharing settings, and disable automatic upload when processing confidential material.

Risk: Dependency versions are not fully pinned, which can change runtime behavior across installs.

Mitigation: Use pinned dependency versions or a lockfile before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rfdiosuao/skills/feishu-video-editor)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration]

**Output Format:** [Markdown status messages with JSON result data and generated media or subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce edited videos, extracted audio, SRT subtitle files, and Feishu cloud-space links when upload is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
