## Description:

Transform long videos into viral short-form clips. Auto-detect best moments, add trendy captions, export for TikTok/Reels/Shorts. Self-contained, no external modules. 100% free tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayank8290](https://clawhub.ai/user/mayank8290)

### License/Terms of Use:


## Use Case:

Creators, editors, and agents use this skill to turn long-form videos or supported video URLs into short vertical clips with captions, transcript metadata, scored moments, and a summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output folder argument can write files outside the documented output area.

Mitigation: Keep outputs in a trusted directory and avoid untrusted --output values.

Risk: Processing private media or running agent-provided commands can expose sensitive content or create unintended files.

Mitigation: Review commands before execution, process only media you are authorized to use, and keep generated outputs in trusted storage.

Risk: The skill depends on local ffmpeg, yt-dlp, and whisper-cpp binaries.

Mitigation: Install runtime dependencies from trusted pinned sources where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayank8290/skills/clips-machine)
- [Project homepage](https://github.com/Mayank8290/openclaw-video-skills)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [MP4 video clips with JSON transcript and moment metadata, a Markdown summary, and Markdown guidance with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg, yt-dlp, and whisper-cpp; writes generated outputs under the configured output directory.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
