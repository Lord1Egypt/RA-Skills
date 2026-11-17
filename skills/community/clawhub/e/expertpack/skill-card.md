## Description:

ExpertPack helps agents load, create, hydrate, and configure retrieval for structured knowledge packs that also work as Obsidian vaults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhearn](https://clawhub.ai/user/brianhearn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to consume ExpertPacks as agent context, create or hydrate new packs, configure RAG over pack directories, and work with packs in Obsidian-compatible workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could read or index ExpertPack directories that the user did not intend to expose as context.

Mitigation: Point RAG only at approved pack directories and review pack contents before adding them to agent memory paths.

Risk: Optional companion tools or Obsidian plugins can add behavior outside this Markdown guidance package.

Mitigation: Review companion tools and Obsidian plugins separately before installing or enabling them.

## Reference(s):

- [ExpertPack Homepage](https://expertpack.ai)
- [Consumption Reference](references/consumption.md)
- [Hydration Reference](references/hydration.md)
- [ExpertPack Schemas Reference](references/schemas.md)
- [ExpertPack Schema Docs](https://expertpack.ai/#schemas)
- [Obsidian Compatibility](https://expertpack.ai/#obsidian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration snippets and shell command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for ExpertPack consumption, hydration, RAG setup, Obsidian workflows, and companion-tool selection.]

## Skill Version(s):

1.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
