## Description:

Generate Excalidraw diagrams from text content in Obsidian Markdown, standard Excalidraw JSON, or animated Excalidraw JSON formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axtonliu](https://clawhub.ai/user/axtonliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writers use this skill to turn text descriptions into hand-drawn style Excalidraw diagrams for Obsidian notes, Excalidraw sharing, or animation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files may be saved automatically in the current working directory.

Mitigation: Use the skill from the intended workspace and review generated filenames before relying on the output.

Risk: Broad trigger words such as diagram or flowchart may activate the skill unexpectedly in environments that auto-load skills.

Mitigation: Narrow activation triggers or confirm before allowing file writes in shared or sensitive workspaces.

Risk: A generated diagram file could overwrite or collide with an existing filename.

Mitigation: Check for existing files and choose a distinct output name when preserving prior diagrams matters.

Risk: Diagram quality may vary with model version and input structure.

Mitigation: Review generated diagrams for accuracy, readability, spacing, and valid Excalidraw structure before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axtonliu/skills/excalidraw-diagram)
- [Excalidraw schema reference](artifact/references/excalidraw-schema.md)
- [Excalidraw](https://excalidraw.com)
- [Obsidian Excalidraw plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin)
- [excalidraw-animate](https://dai-shi.github.io/excalidraw-animate/)
- [Obsidian](https://obsidian.md/)

## Skill Output:

**Output Type(s):** [markdown, code, configuration, guidance]

**Output Format:** [Markdown files containing Excalidraw data or .excalidraw JSON files, plus brief usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may automatically save generated diagram files in the current working directory.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact metadata reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
