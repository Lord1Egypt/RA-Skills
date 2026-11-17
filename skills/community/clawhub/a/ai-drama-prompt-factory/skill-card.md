## Description:

Converts novels, source stories, or original short-drama ideas into structured prompt packages for characters, scenes, props, storyboard images, video, audio, and downstream API JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhgarylu](https://clawhub.ai/user/zhgarylu)

### License/Terms of Use:


## Use Case:

External creators and developers use this skill to plan short-drama projects, design story assets, generate episode scripts, diagnose adaptation fidelity, and assemble prompt/API JSON packages for external AI generation tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled document tools can broadly index and read local files without enough containment.

Mitigation: Install only for trusted story or project folders, avoid pointing indexing tools at home directories or repositories with secrets, regenerate indexes from approved source text, and review outputs before sharing them externally.

## Reference(s):

- [Planning Guide](references/planning-guide.md)
- [Design Guide](references/design-guide.md)
- [Script Generation Guide](references/script-generation-guide.md)
- [Diagnosis Guide](references/diagnosis-guide.md)
- [Assembly Rules](references/assembly-rules.md)
- [Continuity Guide](references/continuity-guide.md)
- [API Output Schema](references/api-schema.md)
- [Platform Adapters](references/platform-adapters.md)
- [Document Reader Guide](references/doc-reader-guide.md)
- [Prompt Examples](references/prompt-examples.md)
- [ClawHub skill page](https://clawhub.ai/zhgarylu/skills/ai-drama-prompt-factory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus structured JSON prompt-package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompt data only; it does not generate images, video, or audio.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
