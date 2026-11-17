## Description:

Researches how people are using an AI tool (Claude Desktop, Cursor, OpenAI Codex, Google Gemini, or OpenClaw) and generates a Productivity Playbook plus a Skills Catalog in a consistent, rated, month-over-month format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nazmul87-wq](https://clawhub.ai/user/nazmul87-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and operators use this skill to produce monthly research updates for Claude, Cursor, Codex, Gemini, or OpenClaw. It creates persona-oriented productivity playbooks and rated skills catalogs that preserve a stable month-over-month structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill researches public sources and may include stale, incomplete, or misleading third-party claims in generated playbooks and catalogs.

Mitigation: Review cited sources and ratings before relying on recommendations or publishing the generated Markdown.

Risk: Generated third-party skill, plugin, or MCP install commands may grant tools access to shells, files, accounts, or private data.

Mitigation: Vet each recommended tool and command before execution, especially when it can run shell commands or access private accounts.

Risk: The skill writes or updates Markdown files and a run log in the selected output directory.

Mitigation: Run it in the intended workspace and review file diffs before committing or distributing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nazmul87-wq/skills/ai-tool-research)
- [README](artifact/README.md)
- [Playbook template](artifact/playbook-template.md)
- [Catalog template](artifact/catalog-template.md)
- [Rating system](artifact/rating-system.md)
- [Research queries](artifact/research-queries.md)
- [Agent Skills standard](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with dated research windows, links, ratings, tables, and run-log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one Productivity Playbook and one Skills Catalog per selected tool; an all-tools run can produce ten Markdown files plus a research log.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
