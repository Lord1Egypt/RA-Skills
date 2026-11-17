## Description:

Generate FFmpeg commands from natural language video editing requests - cut, trim, convert, compress, change aspect ratio, extract audio, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahmoudadelbghany](https://clawhub.ai/user/mahmoudadelbghany)

### License/Terms of Use:


## Use Case:

Developers, creators, and video operators use this skill to turn natural language video editing requests into FFmpeg commands for trimming, conversion, resizing, compression, audio extraction, subtitles, watermarks, screenshots, and related edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated commands include overwrite behavior that can silently replace existing files.

Mitigation: Review commands before execution, remove -y when overwrite is not intended, and use unique output filenames.

Risk: Untrusted filenames, paths, or filter values can make generated shell commands unsafe.

Mitigation: Reject or sanitize shell metacharacters such as $(), backticks, quotes, semicolons, and newlines before running commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with bash code blocks and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands include assumed filenames when needed and use FFmpeg flags such as -y and -hide_banner.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
