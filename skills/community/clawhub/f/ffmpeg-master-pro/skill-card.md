## Description: <br>
FFmpeg Master Pro helps agents plan and run local FFmpeg workflows for video conversion, compression, editing, subtitle handling, optimization, batch processing, GIF conversion, audio extraction, merging, aspect-ratio changes, screenshots, and frame extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqbjqtd](https://clawhub.ai/user/aqbjqtd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media engineers, and content operations teams use this skill to choose FFmpeg commands, presets, and validation steps for routine and advanced video-processing tasks. It is useful when an agent needs to analyze input media, optimize encoding parameters, handle subtitles, perform precise cuts, or process videos in batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local FFmpeg commands can overwrite files or write processed media to unintended locations. <br>
Mitigation: Confirm the exact input files, output path, and overwrite behavior before execution. <br>
Risk: Untrusted media, subtitle files, custom presets, or raw batch commands can increase local processing risk. <br>
Mitigation: Process untrusted inputs in a sandbox and avoid untrusted custom preset names or raw batch commands. <br>
Risk: Generated encoding or editing commands can produce unexpected quality, timing, or compatibility results. <br>
Mitigation: Review proposed commands and validate outputs with ffprobe, playback checks, and quality metrics where appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aqbjqtd/ffmpeg-master-pro) <br>
- [FFmpeg](https://ffmpeg.org) <br>
- [Detailed Workflows](references/detailed_workflows.md) <br>
- [Smart Cut Guide](references/smart_cut_guide.md) <br>
- [Keyframe Analysis](references/keyframe_analysis.md) <br>
- [Optimization Guide](references/optimization_guide.md) <br>
- [Best Practices](references/best_practices.md) <br>
- [API Reference](references/api_reference.md) <br>
- [Quickstart](references/quickstart.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include FFmpeg or ffprobe commands, preset choices, output-path guidance, batch-processing steps, and validation checks.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
