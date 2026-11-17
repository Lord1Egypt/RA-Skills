## Description:

Dream actively maintains OpenClaw memory by distilling daily memory files into MEMORY.md, archiving stale entries, detecting re-emergence, and indexing selected content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teman2050](https://clawhub.ai/user/teman2050)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Dream to keep long-running personal memory concise, searchable, and current while preserving older important context in an append-only ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dream preserves and reuses personal memory long term, including a permanent ledger that `dream forget` does not erase.

Mitigation: Use it only where long-term memory retention is acceptable, and review retention expectations before installation in sensitive, shared, regulated, or multi-user workspaces.

Risk: Dream can perform silent scheduled maintenance and broad memory indexing.

Mitigation: Enable scheduled distillation only in workspaces where automatic memory rewriting and indexing are intended, and review the configured vault path before use.

Risk: The security summary says helper-script paths can exceed the advertised file scope.

Mitigation: Review and fix helper-script path scoping before deployment, and run the skill with a constrained OpenClaw workspace and Dream vault.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teman2050/skills/dream)
- [Project homepage](https://github.com/teman2050/dream-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and file update instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md, ledger files, metadata files, and Obsidian index files through the bundled shell helper.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
