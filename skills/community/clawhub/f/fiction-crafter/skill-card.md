## Description:

Fiction Crafter helps agents plan, write, format, and review serialized Chinese webnovel chapters while maintaining story memory for characters, locations, plot points, and world rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[followaf](https://clawhub.ai/user/followaf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a fiction direction or premise into a structured Chinese webnovel workflow, including prompt expansion, outline planning, chapter drafting, continuity tracking, review, and resume-from-breakpoint support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using init-novel.sh with --clean removes generated Markdown chapters and resets story memory files in the skill workspace.

Mitigation: Confirm the target workspace and back up needed output/ and .learnings/ files before using --clean; omit --clean when continuing an existing novel.

Risk: A file-backed long-form fiction workflow can drift from established characters, locations, plot points, or world rules if memory files are not maintained.

Mitigation: Read and update the .learnings/ files before each chapter and use the chapter review workflow to check continuity before continuing.

## Reference(s):

- [Fiction Crafter on ClawHub](https://clawhub.ai/followaf/skills/fiction-crafter)
- [Original ClawHub skill: novel-generator](https://clawhub.ai/ityhg/novel-generator)
- [Prompt Guide](references/prompt-guide.md)
- [Plot Structures](references/plot-structures.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, prose guidance, Mermaid diagrams, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates output/ chapter files and .learnings/ story memory files; optional scripts initialize a novel workspace and normalize chapter separators.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
