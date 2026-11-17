## Description:

FCP Assistant helps agents assemble videos from scripts, collect stock footage, generate local TTS voiceovers, create subtitles and thumbnails, and run ffmpeg-based editing helpers for Final Cut Pro workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lasbder-ops](https://clawhub.ai/user/lasbder-ops)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and developers use this skill to draft script-to-video workflows, collect media, generate voiceover audio, assemble finished videos, and produce editing support files for Final Cut Pro-oriented projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports suspicious shell-script handling where crafted subtitle language input could run local code.

Mitigation: Review shell scripts before installation, avoid passing untrusted values to multi-lang-subtitles.sh, and prefer manually running checked commands with known-safe arguments.

Risk: The shipped files rely on local command execution and media-processing tools such as ffmpeg, ffprobe, curl, jq, and osascript.

Mitigation: Run the skill in a controlled local environment with the required binaries installed, and inspect generated commands and file paths before execution.

Risk: The security guidance states that advertised Final Cut Pro automation and batch export features are not fully present in the shipped files.

Mitigation: Treat FCP automation claims as limited to the included artifacts, verify expected scripts exist before planning a workflow, and fall back to manual Final Cut Pro steps where needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lasbder-ops/skills/fcp-assistant)
- [FCP Assistant Skill Definition](artifact/SKILL.md)
- [FCP Assistant Quick Start Guide](artifact/GUIDE.md)
- [Pexels API](https://www.pexels.com/api/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated media/configuration file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for running local shell scripts that can create media files, metadata, subtitles, thumbnails, tags, and edited video outputs.]

## Skill Version(s):

2.2.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
