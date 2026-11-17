## Description:

AI科普视频全流程自动化制作技能，帮助代理规划脚本、生成数字人片段、克隆语音、渲染内容幻灯片和逐字字幕、修复音频、合成视频并执行专业QA审查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to produce Mandarin AI science explainer videos with a talking avatar, narrated slides, karaoke-style subtitles, FFmpeg compositing, and delivery QA. It is tuned for Apple Silicon Mac mini systems with 16GB memory while keeping rendering parameters adjustable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can involve sensitive portrait images, cloned voices, and a Google Flow account.

Mitigation: Use only voice and image inputs the operator has rights to process, and run Google Flow with a dedicated Chrome profile or separate Google account.

Risk: The subtitle script can install an unpinned Python package at runtime if Whisper is missing.

Mitigation: Run the scripts in an isolated environment and preinstall reviewed, pinned dependencies before execution.

Risk: Generated narration, subtitles, and educational claims may be inaccurate or misaligned with the source script.

Mitigation: Complete the bundled QA checklist, including Whisper cross-checks, subtitle timing review, pronunciation checks, and manual content review before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/ai-science-video-studio)
- [Script Format Specification](artifact/references/script_format.md)
- [Professional QA Review Checklist](artifact/references/qa_checklist.md)
- [Known Pitfalls & Solutions](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON examples, Python snippets, shell commands, and generated media-file workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce script.json plans, subtitle frame directories, rendered segment videos, audio QA reports, and final MP4 outputs when the agent executes the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
