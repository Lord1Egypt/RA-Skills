## Description:

Ai Drama Prompt Factory.Skip helps agents turn a novel or original story idea into a structured short-drama prompt package with planning, character and scene design, scripts, diagnostics, storyboard prompts, video prompts, audio specifications, and API-ready JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huang-shao](https://clawhub.ai/user/huang-shao)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to convert source novels or original short-drama ideas into staged project files and JSON prompt packages for downstream image, video, and audio generation tools. The skill produces prompt data only and does not generate media directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled document indexing and retrieval helpers can read and persist more local story or source content than the creative workflow clearly scopes.

Mitigation: Keep indexing limited to the intended story or source directory, and review or delete generated index files before sharing or deployment.

Risk: Generated indexes or prompt packages may contain private file paths, content-derived keywords, or user-provided story material.

Mitigation: Avoid processing confidential or rights-restricted source material unless the deployment has appropriate data handling and review controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huang-shao/skills/ai-drama-prompt-factory-skip)
- [API output schema](references/api-schema.md)
- [Assembly rules](references/assembly-rules.md)
- [Continuity guide](references/continuity-guide.md)
- [Design guide](references/design-guide.md)
- [Diagnosis guide](references/diagnosis-guide.md)
- [Document reader guide](references/doc-reader-guide.md)
- [Manga drama guide](references/manga-drama-guide.md)
- [Planning guide](references/planning-guide.md)
- [Platform adapters](references/platform-adapters.md)
- [Prompt examples](references/prompt-examples.md)
- [Script generation guide](references/script-generation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus JSON project files, prompt packages, configuration objects, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first workflow; prompt packages can include storyboard_prompt, video_prompt, and audio_spec fields, while final media generation remains out of scope.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
