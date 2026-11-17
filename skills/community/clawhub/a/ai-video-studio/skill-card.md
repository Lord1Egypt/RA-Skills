## Description:

FableForge AI Video Studio is a command-level SOP for producing short-form management allegory videos from concept generation through scripting, TTS voice synthesis, asset creation, HyperFrames rendering, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-kay8](https://clawhub.ai/user/lucas-kay8)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and agent operators use this skill to plan and assemble short-form management allegory, business analysis, and product promotion videos. It guides the agent through staged content review, storyboard creation, voice generation, visual asset preparation, timeline construction, render checks, and release packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive voice samples and cloned-voice outputs may expose personal biometric information.

Mitigation: Require explicit consent before any cloned-voice use, store voice samples only in an ignored project directory, and review the project .gitignore before committing.

Risk: Tool and binary downloads may introduce unverified code into the video project.

Mitigation: Use a disposable or dedicated project environment, pin and verify dependencies and downloaded binaries, and remove unsafe download flags such as curl -k.

Risk: Automatic publishing or git commands may push unintended files or changes.

Mitigation: Disable automatic git push and require manual approval of the exact diff, remote, and branch before publishing.

Risk: Generated scripts, subtitles, or visuals may be misleading, low quality, or unsuitable for publication.

Mitigation: Apply the documented content, rhythm, image, timeline, and render preflight checks before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucas-kay8/skills/ai-video-studio)
- [FableForge AI Agent SOP (English)](artifact/SKILL.en.md)
- [FableForge Video Production SOP](artifact/SKILL.md)
- [Stage 0: Environment Scaffolding](artifact/resources/stages/stage_0_env.md)
- [Stage 1: Concept, Script, and Assets](artifact/resources/stages/stage_1_creatives.md)
- [Stage 2: Audio Timeline](artifact/resources/stages/stage_2_timeline.md)
- [Stage 3: Static Layout](artifact/resources/stages/stage_3_static.md)
- [Stage 4: Animation and Render Preflight](artifact/resources/stages/stage_4_animation.md)
- [Stage 5: Publishing and Archive](artifact/resources/stages/stage_5_publish.md)
- [Visual Style Bible](artifact/resources/style_bible.md)
- [Troubleshooting Manual](artifact/resources/troubleshooting.md)
- [Voice Sample Recording Guide](artifact/resources/voice-model/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, HTML/CSS/JavaScript snippets, storyboard templates, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged operating procedures and generated project files for video production; final media assets depend on external tools and user-provided inputs.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
