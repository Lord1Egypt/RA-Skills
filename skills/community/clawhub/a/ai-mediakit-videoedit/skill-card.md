## Description:

AI MEDIAKIT VIDEO EDIT helps an agent analyze subtitles and Bilibili-style danmaku, propose clip selections, splice video segments with FFmpeg, and optionally add rendered text effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-ai-mediakit](https://clawhub.ai/user/volc-ai-mediakit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-production agents use this skill to turn local videos, subtitles, and optional danmaku files into an editable plan, then generate clipped and merged videos with optional text effects after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Remotion rendering path uses vulnerable and unlocked npm dependencies.

Mitigation: Upgrade Remotion and related packages to at least 4.0.410, commit and review a lockfile, and run dependency review before installation.

Risk: Installing npm or system dependencies with elevated privileges can increase host impact if a dependency is compromised.

Mitigation: Install dependencies in a least-privileged project environment and avoid root or administrator installs unless the operator has explicitly accepted the risk.

Risk: Audio normalization behavior can be misunderstood because documentation and script defaults differ.

Mitigation: Ask the user to confirm audio normalization explicitly before execution and record the chosen value in the clip configuration.

Risk: Video content understanding depends on subtitle or danmaku evidence and may produce incorrect clip boundaries when those inputs are missing or noisy.

Mitigation: Present the proposed segments, transition choice, and output path for user confirmation before running FFmpeg.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volc-ai-mediakit/skills/ai-mediakit-videoedit)
- [Bilibili Danmaku XML Format Reference](artifact/references/danmaku_format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Video files, Guidance]

**Output Format:** [Markdown plans, JSON clip/effects configuration, shell commands, and MP4 video outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local video inputs and installed FFmpeg; optional text effects use Node.js and Remotion.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact SKILL.md lists v1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
