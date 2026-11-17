## Description:

Create explainer videos with narration and AI-generated visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xfango](https://clawhub.ai/user/0xfango)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a topic, product introduction, concept explanation, or tutorial into a narrated explainer script or a full explainer video with AI-generated visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided topics or source text are sent to ListenHub/Marswave for generation.

Mitigation: Use the skill only with content approved for that service, and avoid submitting secrets or private material.

Risk: Generated scripts, audio, or local preferences may be saved under .listenhub/explainer when download-oriented output modes are used.

Mitigation: Choose inline output when local persistence is not desired, and review generated files before sharing or retaining them.

## Reference(s):

- [Explainer skill page](https://clawhub.ai/0xfango/skills/explainer-video)
- [Video Guide](references/video-guide.md)
- [ListenHub explainer app](https://listenhub.ai/app/explainer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with bash command snippets, local configuration and output files, and ListenHub media links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports script-only or text-plus-video generation; uses one narrator and inline, download, or combined output modes.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
