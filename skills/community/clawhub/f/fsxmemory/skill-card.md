## Description:

Structured memory system for AI agents. Context death resilience (checkpoint/recover), structured storage, Obsidian-compatible markdown, and local semantic search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azrijamil](https://clawhub.ai/user/azrijamil)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to install and operate a structured local memory vault for decisions, lessons, procedures, projects, handoffs, and other continuity records. It supports session recovery, Markdown-based memory templates, search workflows, and migration from other Markdown vault formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on unpinned global third-party installs that may change over time and will handle persistent private memory data.

Mitigation: Review before installing, prefer pinned versions or a sandboxed local install, and verify the npm package and qmd source before use.

Risk: Memory vaults can contain sensitive personal, project, or relationship data.

Mitigation: Keep vaults scoped to non-sensitive data unless the installed tools are trusted, and confirm whether embedding or search workflows send vault content to external services.

Risk: Migration and auto-linking workflows can modify existing Markdown vault files.

Mitigation: Use dry-run and backup options before migration or auto-linking, and keep recoverable backups for rollback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/azrijamil/skills/fsxmemory)
- [npm package](https://www.npmjs.com/package/@foresigxt/foresigxt-cli-memory)
- [qmd search dependency](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured memory templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for local vault setup, memory capture, recovery, search, migration, and template-based Markdown records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
