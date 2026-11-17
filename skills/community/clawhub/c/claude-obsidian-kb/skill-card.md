## Description:

Builds and maintains an Obsidian-style personal knowledge vault by organizing raw notes into structured wiki pages, creating bidirectional links, and generating maintenance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and knowledge workers use this skill to turn loose notes, source material, and project knowledge into an Obsidian-style vault with raw, wiki, and output layers. The skill guides agents to create structured Markdown notes, apply frontmatter, maintain links, detect contradictions, and run vault maintenance scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad persistent changes to an Obsidian-style vault.

Mitigation: Use dry-run or preview workflows where available, keep backups before batch organization, and review proposed changes before applying them.

Risk: The auto-link workflow can generate a .claude_fix_suggestions.sh shell script.

Mitigation: Inspect the generated shell script carefully before execution and run only commands that are necessary and understood.

Risk: Notebook content may include confidential information that could be processed through an API-based workflow.

Mitigation: Confirm where note content is sent before processing confidential material and avoid external API workflows when data handling is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/skills/claude-obsidian-kb)
- [Scripts usage guide](references/scripts.md)
- [Claude-Obsidian x iBrain integration](references/ibrain-integration.md)
- [Frontmatter templates](assets/frontmatter_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated vault files or reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Markdown vault content, frontmatter, bidirectional links, index files, .cache/hot_cache.json, and .claude_fix_suggestions.sh.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
