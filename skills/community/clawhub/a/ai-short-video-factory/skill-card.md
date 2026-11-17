## Description:

AI Short Video Factory creates MP4 videos from HTML using HyperFrames for captioned talking-head edits, product launches, data visualizations, code walkthroughs, social clips, GSAP animations, transitions, audio muxing, and deterministic rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrzqbr](https://clawhub.ai/user/zrzqbr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and content producers use this skill to turn text ideas, structured scripts, or content outlines into HTML/CSS/GSAP video projects and rendered MP4 short videos. It supports tech news, product launches, data visualization, code walkthroughs, social clips, and captioned talking-head post-production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs mutable package commands and can download browser components for video rendering.

Mitigation: Pin HyperFrames and Python package versions where practical, review generated commands before execution, and run renders in a disposable container or VM.

Risk: Rendering may require disabling the browser sandbox for Headless Chrome.

Mitigation: Use sandbox disabling only inside an isolated rendering environment and avoid using it on a sensitive host.

Risk: Troubleshooting guidance includes a sudo ownership workaround for cache permissions.

Mitigation: Diagnose the exact permission problem first and avoid broad sudo ownership changes unless the target path and impact are understood.

Risk: The skill performs shell-driven media processing with FFmpeg and generated assets.

Mitigation: Constrain input and output paths, keep original media backups, and verify final duration, audio coverage, and visual quality before delivery.

## Reference(s):

- [HyperFrames Composition Rules](references/composition-rules.md)
- [HyperFrames Animation Guide](references/animation-guide.md)
- [HyperFrames Caption & Subtitle Patterns](references/caption-patterns.md)
- [AI Short Video Factory README](README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with HTML/CSS/JavaScript snippets, shell commands, configuration details, and generated project file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify HyperFrames project files, captions, WAV audio, and final MP4 render outputs.]

## Skill Version(s):

1.2.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
