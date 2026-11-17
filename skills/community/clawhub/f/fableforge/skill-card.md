## Description:

Fableforge is a staged video-production SOP for agents that covers concept development, storyboard writing, TTS voice generation, media acquisition, HyperFrames timeline construction, rendering, and publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-kay8](https://clawhub.ai/user/lucas-kay8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-production agents use Fableforge to produce short-form management, analytical, or promotional videos through a controlled workflow with user confirmation checkpoints, media generation, audio timing, HTML/CSS composition, and render validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may download executable tools or media and install packages during setup.

Mitigation: Require user confirmation before downloads or package installs, pin and verify dependencies where possible, and review commands before execution.

Risk: The workflow may use a voice clone and handle voice samples.

Mitigation: Use voice cloning only with explicit user consent, keep voice samples out of version control, and review generated narration before publication.

Risk: The workflow modifies workspace files and may create Git commits or prepare content for publishing.

Mitigation: Review generated files and repository diffs before committing, require explicit approval for commits or pushes, and review promotional content before rendering or publishing.

Risk: Generated scripts, visuals, or promotional copy may be inaccurate, misleading, or unsuitable for the intended audience.

Mitigation: Apply the documented content quality gates and have a human reviewer approve the final script, assets, and rendered video.

## Reference(s):

- [Fableforge ClawHub skill page](https://clawhub.ai/lucas-kay8/skills/fableforge)
- [FableForge SOP](artifact/SKILL.md)
- [Stage 0 Scaffolding](artifact/resources/stages/stage_0_env.md)
- [Stage 1 Creatives](artifact/resources/stages/stage_1_creatives.md)
- [Stage 2 Timeline](artifact/resources/stages/stage_2_timeline.md)
- [Stage 3 Static Layout](artifact/resources/stages/stage_3_static.md)
- [Stage 4 Animation](artifact/resources/stages/stage_4_animation.md)
- [Stage 5 Publishing](artifact/resources/stages/stage_5_publish.md)
- [Visual Style Bible](artifact/resources/style_bible.md)
- [Troubleshooting Manual](artifact/resources/troubleshooting.md)
- [Voice Sample Guide](artifact/resources/voice-model/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, HTML/CSS/JavaScript templates, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes staged exit criteria, user confirmation checkpoints, and workspace file-generation guidance for scripts, media assets, timelines, templates, and rendered video outputs.]

## Skill Version(s):

1.2.0 (source: server evidence release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
