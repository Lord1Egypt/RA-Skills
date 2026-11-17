## Description:

Provides a structured AI agent memory system separating episodic, semantic, and procedural memories to preserve knowledge and processes over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryancampbell](https://clawhub.ai/user/ryancampbell)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to set up persistent local memory, daily logs, feedback tracking, procedure templates, and search routines so agents can recover context and reuse how-to knowledge across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory files may contain sensitive workspace or personal information if users write it there.

Mitigation: Do not store API keys, tokens, passwords, private personal data, auth headers, confidential raw logs, or similar sensitive material in memory files.

Risk: Search results or exported memory snippets may reveal private workspace context.

Mitigation: Review exported search results before sharing them outside the workspace.

Risk: Deletion commands in uninstall guidance can remove local files if run from the wrong path.

Mitigation: Verify paths before running uninstall commands, especially any rm -rf line.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryancampbell/skills/agent-memory-kit)
- [README.md](README.md)
- [SEARCH.md](SEARCH.md)
- [INSTALLATION.md](INSTALLATION.md)
- [Memory Architecture Template](templates/ARCHITECTURE.md)
- [Compaction Survival Template](templates/compaction-survival.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation, reusable markdown templates, and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local file templates and optional bash search helper output.]

## Skill Version(s):

2.1.0 (source: server release evidence and CHANGELOG.md, released 2026-02-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
