## Description:

Ai Short Film Studio helps agents plan, generate, and assemble short AI films using storyboard workflows, video-generation services, TTS narration, subtitles, and FFmpeg-based composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and agent operators use this skill to turn scripts or short-form video ideas into storyboards, generated clips, narration, subtitles, and final composed videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Google Flow route uses Chrome remote debugging and may expose an active browser session.

Mitigation: Use a dedicated Chrome profile and isolated Google account, avoid running it against a normal browser session, and close the remotely debuggable browser after use.

Risk: Batch scripts rename and delete generated video-* files in the configured output directory.

Mitigation: Run batch generation only in a dedicated project directory that does not contain valuable pre-existing video-* files.

Risk: The workflow sends prompts, scripts, audio, video, or other media to third-party services.

Mitigation: Do not submit sensitive scripts or media, replace any example cloud identifiers with user-owned placeholders, and review each service's terms before use.

Risk: The workflow depends on external automation and media-generation services whose behavior may change.

Mitigation: Review the skill before installing, pin trusted dependencies where possible, and test the complete workflow in an isolated environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/ai-short-film-studio)
- [Production workflow reference](artifact/references/production_workflow.md)
- [Sucuang API reference](artifact/references/sucuang_api.md)
- [Sucuang API documentation](https://api.wuyinkeji.com/doc)
- [Google Flow](https://labs.google/fx/tools/flow)
- [Kling image-to-video API endpoint](https://api-beijing.klingai.com/v1/videos/image2video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, JavaScript helpers, and Python composition code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce storyboard JSON, project files, generated media paths, progress reports, subtitles, narration audio, and composed video outputs when paired with external services and local tools.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
