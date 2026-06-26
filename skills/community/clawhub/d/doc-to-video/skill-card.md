## Description: <br>
Converts Markdown technical documentation into narrated 1920x1080 tutorial videos using edge-tts audio generation, Remotion visual scenes, and FFmpeg merging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengbin92](https://clawhub.ai/user/mengbin92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and educators use this skill to turn Markdown project documentation, tutorials, and knowledge-sharing material into narrated instructional videos with generated audio, scene code, and merge commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Narration text is sent to an external TTS provider. <br>
Mitigation: Use the skill only with documents approved for external TTS processing, and avoid confidential or regulated content unless that provider is approved. <br>
Risk: The workflow runs local build, render, audio, and merge commands. <br>
Mitigation: Review generated shell commands, dependency installs, and output paths before execution, especially FFmpeg, Remotion, npm, and cleanup steps. <br>
Risk: Maintenance and sync guidance can copy, overwrite, or modify installed skill directories across agent environments. <br>
Mitigation: Check source and destination paths before running sync or cleanup commands, and preserve environment-specific metadata files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mengbin92/doc-to-video) <br>
- [ClawHub homepage metadata](https://clawhub.ai/skills/doc-to-video) <br>
- [Changelog](CHANGELOG.md) <br>
- [Batch rendering workflow](references/batch-rendering.md) <br>
- [macOS gotchas](references/macos-gotchas.md) <br>
- [Second-video reuse pattern](references/second-video-pattern.md) <br>
- [Syncing to OpenClaw workflow](references/syncing-to-openclaw.md) <br>
- [Voice swap and iteration workflow](references/voice-swap-and-iterate.md) <br>
- [Worked example: TSP Solidity 04](references/worked-example-tsp-solidity04.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline Python, TypeScript, JSON, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local Remotion project files, edge-tts audio files, FFmpeg merge artifacts, and final MP4 videos.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
