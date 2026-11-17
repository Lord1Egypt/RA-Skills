## Description:

Generates cinematic text-to-video and image-to-video story clips via WeryAI with film-language prompting, model-specific parameter guidance, and a required approval step before paid submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn short cinematic briefs or still images into WeryAI video-generation requests with expanded scene prompts, appropriate model parameters, and user approval before paid execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit paid WeryAI generation jobs.

Mitigation: Require explicit user approval of the model, duration, aspect ratio, audio settings, and full expanded prompt before running submit or wait commands.

Risk: Image-to-video flows can upload local files to WeryAI when local image paths are supplied.

Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing the behavior and receiving explicit user consent.

Risk: The executable helper includes an unaudited dependency outside the reviewed package.

Mitigation: Run in an isolated environment with a scoped WERYAI_API_KEY and prefer a package version that bundles or pins the external dependency.

## Reference(s):

- [WeryAI video CLI and JSON reference](references/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/cinematic-story-video-gen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with confirmation tables, inline shell commands, JSON request examples, and video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; submits paid WeryAI tasks only after explicit approval.]

## Skill Version(s):

0.1.0 (source: server release metadata; SKILL.md frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
