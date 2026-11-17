## Description:

Integrates the Playfilo shared-memory DAG into OpenClaw via pnpm patch on the embedded pi-coding-agent and layers on top of arianna-pi-integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujilabs](https://clawhub.ai/user/wujilabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Playfilo shared-memory DAG persistence, temporal tools, and prompt context injection into an OpenClaw checkout. It provides ordered patch, dependency, plugin, and verification guidance for a controlled OpenClaw worktree.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes an OpenClaw checkout and dependency patch.

Mitigation: Apply it only in a controlled OpenClaw worktree after reviewing the generated pnpm patch, dependency changes, and rollback path.

Risk: Local INCUBATION_SEED content is loaded into system prompt context.

Mitigation: Inspect the exact ~/.playfilo/INCUBATION_SEED.md contents before enabling the plugin and remove sensitive or untrusted text.

Risk: Prompt, tool, and model metadata can be stored in the shared Playfilo database.

Mitigation: Treat ~/.playfilo/playfilo.db as sensitive operational data and restrict access, backups, and sharing accordingly.

Risk: Temporal tools can remain available where an operator expected stricter tool restrictions.

Mitigation: Verify the effective OpenClaw tool policy after installation and disable or adjust the integration in restricted deployments.

## Reference(s):

- [Arianna homepage](https://arianna.run)
- [ClawHub release page](https://clawhub.ai/wujilabs/skills/arianna-openclaw-integration)
- [Skill overview](artifact/SKILL.md)
- [OpenClaw plugin files](artifact/plugin/)
- [Verification checklist](artifact/patches/verify.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with TypeScript, JSON, shell command, and patch snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ordered OpenClaw patch steps, plugin source, dependency notes, and verification checks.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
