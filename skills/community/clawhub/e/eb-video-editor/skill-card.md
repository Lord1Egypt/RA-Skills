## Description:

Edits existing videos with ffmpeg and Python for trimming, joining, audio changes, subtitles, overlays, conversion, compression, thumbnails, GIFs, and batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and content operators use this skill to plan and execute video transformations through ffmpeg commands and Python snippets while preserving originals and verifying outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a batch pattern that can execute arbitrary shell commands from a jobs.txt file.

Mitigation: Use only trusted media and trusted working directories, avoid the jobs.txt bash -c pattern, and review each generated command before execution.

Risk: Optional package installation commands can alter the user's Python environment.

Mitigation: Approve dependency installation explicitly and prefer a virtual environment or container with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emersonbraun/skills/eb-video-editor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated command sequences, batch scripts, ffprobe analysis guidance, and verification steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
