## Description:

Bravado turns a project website, GitHub repository, resume, or portfolio into a sourced, short motion film with an editable project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dktrn9ne](https://clawhub.ai/user/dktrn9ne)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and teams use this skill to turn a public product link or supplied portfolio into a sourced visual story, storyboard, rendered MP4, and editable project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source inspection may fetch public project URLs and query GitHub repository metadata.

Mitigation: Review the URLs before use and supply private repositories only if you intend their content to be processed for the film.

Risk: A supplied resume or portfolio may contain personal information that could appear in generated artifacts.

Mitigation: Provide only material intended for the film and review the brief and export for sensitive details before sharing.

Risk: The workflow downloads verified fonts and runs local Python and ffmpeg commands that write render artifacts.

Mitigation: Review the destination and generated project before running it; use the supplied font verification and inspect outputs before publishing.

## Reference(s):

- [Bravado on ClawHub](https://clawhub.ai/dktrn9ne/skills/bravado)
- [Bravado production workflow](references/workflow.md)
- [Bravado review bar](references/quality-bar.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Shell commands, Guidance]

**Output Format:** [Sourced brief and storyboard, JSON project brief, editable Python project, and MP4 video]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes review stills and export checks; the starter targets 1920×1080, 30 fps, and approximately 31 seconds.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
