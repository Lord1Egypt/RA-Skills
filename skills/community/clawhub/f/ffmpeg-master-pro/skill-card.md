## Description:

Ffmpeg Master Pro helps agents plan and run FFmpeg and ffprobe workflows for video conversion, compression, editing, subtitles, batching, GIF creation, audio extraction, merging, screenshots, frame extraction, and output validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqbjqtd](https://clawhub.ai/user/aqbjqtd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, media engineers, and content operators use this skill to inspect media, choose encoding parameters, build FFmpeg commands, and validate or troubleshoot video-processing outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some documented workflows can silently overwrite files.

Mitigation: Review generated FFmpeg commands before execution, choose output paths deliberately, and remove or avoid overwrite flags unless replacement is intentional.

Risk: A referenced frame-rate example uses unsafe Python evaluation on media metadata.

Mitigation: Do not copy that eval() example into runnable code; parse frame-rate values with a safe numeric parser instead.

Risk: The skill may probe local hardware and create a small user configuration directory for presets.

Mitigation: Install only in environments where local GPU probes and user-level preset configuration are acceptable.

## Reference(s):

- [FFmpeg](https://ffmpeg.org)
- [Detailed Workflows](references/detailed_workflows.md)
- [Smart Cut Guide](references/smart_cut_guide.md)
- [Keyframe Analysis Guide](references/keyframe_analysis.md)
- [Optimization Guide](references/optimization_guide.md)
- [Best Practices](references/best_practices.md)
- [API Reference](references/api_reference.md)
- [Quickstart](references/quickstart.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline FFmpeg shell commands and Python code examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local media files when the proposed commands are executed by the agent.]

## Skill Version(s):

2.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
