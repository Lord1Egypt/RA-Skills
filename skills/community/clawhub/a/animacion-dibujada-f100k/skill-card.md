## Description:

Creates 9:16 drawn animation clips and 30-90 second shorts from canvas and JavaScript, including social-video insert styles, character scenes, subtitles, transitions, and local rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent operators use this skill to plan, assemble, preview, and render code-drawn animation assets for short-form marketing videos. It helps produce HTML animation scenes, JSON plans, shell commands, and rendered MP4 deliverables from project scripts, media, and brand inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plan files or pasted JavaScript values can become code inside the local renderer.

Mitigation: Use only trusted project plans and media sources; review plan JSON and JavaScript values before rendering.

Risk: User photos, face JSON, voice files, and render caches may contain personal data.

Mitigation: Handle media as personal data, keep it scoped to the project, and delete temporary caches and source media when the project is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/animacion-dibujada-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)
- [Skill instructions](SKILL.md)
- [Shorts documentation](cortos/LEEME.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JavaScript, JSON, shell commands, and generated HTML/MP4 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local rendering depends on Node, ffmpeg, Chrome, and optional local speech or image-processing tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
