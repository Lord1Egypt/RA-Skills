## Description:

Extract, structure, research, and visualize family history from raw text. Builds knowledge graphs, generates Mermaid trees, Obsidian vaults, and GEDCOM exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flobo3](https://clawhub.ai/user/flobo3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract family-history facts from raw text, build local genealogy data, research ancestors with search and LLM assistance, and export the results into genealogy and note-taking formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive family details may be sent to third-party LLM or search services during extraction or ancestor research.

Mitigation: Use a contained environment and avoid entering details about living or sensitive relatives unless that exposure is acceptable.

Risk: File-writing tools can create or overwrite local outputs such as graphs, GEDCOM files, Mermaid diagrams, and Obsidian vault files.

Mitigation: Choose output paths carefully and review generated files before using them as authoritative family records.

Risk: Shell-style tool commands and dependency installation are weakly scoped in the release evidence.

Mitigation: Review commands before execution, prefer pinned dependencies, and use argument-safe tool execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON, JSONL, Markdown, Mermaid Markdown, GEDCOM, and Obsidian-compatible Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files from user-provided family data and may call external LLM and search services when extraction or research tools are used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
