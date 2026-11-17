## Description:

将 Markdown 技术文档自动转换成带配音旁白的专业视频。使用 edge-tts 生成自然人声、Remotion 渲染视觉场景、FFmpeg 合并音视频，输出 1920×1080 全高清视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbin92](https://clawhub.ai/user/mengbin92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical content creators use this skill to convert Markdown documentation into narrated 1920×1080 tutorial videos. It guides narration generation, scene rendering, timing checks, and final audio/video merging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation commands can introduce unreviewed Python or Node packages into the user environment.

Mitigation: Run the templates in a dedicated project or virtual environment, pin dependencies, and update or audit packages before running npm or pip commands.

Risk: Maintenance and sync instructions can overwrite active Hermes or OpenClaw skill files.

Mitigation: Use the sync workflow only when replacement is intentional, review the target paths first, and verify file hashes after synchronization.

Risk: Cleanup and copy commands can remove or replace project files when run from the wrong directory.

Mitigation: Confirm the working directory and target paths before running cleanup commands such as rm or recursive copy operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengbin92/skills/doc-to-video)
- [ClawHub homepage metadata](https://clawhub.ai/skills/doc-to-video)
- [Voice swap and iteration workflow](references/voice-swap-and-iterate.md)
- [macOS environment and troubleshooting notes](references/macos-gotchas.md)
- [Batch rendering workflow](references/batch-rendering.md)
- [Second-video reuse pattern](references/second-video-pattern.md)
- [OpenClaw sync workflow](references/syncing-to-openclaw.md)
- [Worked example: Solidity error-handling video](references/worked-example-tsp-solidity04.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and reusable template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can result in generated Python, TypeScript, Remotion configuration, FFmpeg commands, and narrated MP4 project assets.]

## Skill Version(s):

1.0.4 (source: server release evidence and target metadata; artifact frontmatter reports 1.0.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
