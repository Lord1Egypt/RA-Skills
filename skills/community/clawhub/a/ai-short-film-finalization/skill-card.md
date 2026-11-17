## Description:

Finalize an AI-generated short film using the free Route C pipeline (Google Flow Omni Flash text-to-video, Nano Banana 2 image generation, edge-tts narration, Chrome CDP automation). Covers shot generation, consistency checks, 1080p composition with subtitles/BGM, director review console, and highlight trailer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and film-production agents use this skill to turn an existing storyboard into AI-generated short-film assets, perform shot consistency review, compose a 1080p final cut with narration/subtitles/BGM, and prepare director feedback for targeted remakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow automates a logged-in Chrome profile through CDP, which can expose session state or perform unintended account actions.

Mitigation: Use an isolated project browser profile, review the active browser state before automation, and avoid using an everyday Chrome profile.

Risk: The director review flow can emit executable commands from editable project data.

Mitigation: Inspect generated execution commands before use or convert them to structured arguments instead of running exported commands blindly.

Risk: Storyboard fields and project names flow into HTML, paths, and shell-facing examples.

Mitigation: Treat storyboard and project metadata as untrusted input, sanitize names and titles, and review generated HTML and shell escaping before sharing or execution.

Risk: Unpinned dependencies and hardcoded local runtime paths may create reproducibility and supply-chain review gaps.

Mitigation: Pin Python and Node dependencies, document the runtime versions used, and verify FFmpeg, Playwright, and edge-tts installations in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/ai-short-film-finalization)
- [Google Flow](https://labs.google/fx/tools/flow)
- [Shot Consistency Checklist](references/consistency_checklist.md)
- [Fallback Prompts for Problematic Shots](references/fallback_prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, JSON, Python, and workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-specific commands, review manifests, self-contained HTML review consoles, and director fix-pack JSON for downstream film-finalization work.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
