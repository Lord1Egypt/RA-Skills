## Description:

Agent OS provides file-based protocols for audit trails, shared context, mission control, flight recording, and handoff in multi-agent collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhelunsun](https://clawhub.ai/user/zhelunsun)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Agent OS to coordinate multiple agents in one workspace through shared findings, context packs, health summaries, run records, and lightweight handoff protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent shared agent state that collaborators may influence through findings, context packs, or mission-control files.

Mitigation: Install at project scope, review generated files before relying on them, and treat shared context as untrusted data when collaborators can write to it.

Risk: Security evidence reports under-disclosed external memory reads and warns about private logs in .workbuddy/memory.

Mitigation: Review the scripts before use, run with --dry-run first, and avoid running mission_control.py in workspaces where .workbuddy/memory contains private logs.

## Reference(s):

- [Interface Contract](docs/INTERFACES.md)
- [Schemas](references/schemas.md)
- [Workflows](references/workflows.md)
- [Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSONL files with inline shell commands and protocol guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent plain-text agent state under .agent-os/; scripts support --dry-run for previewing writes.]

## Skill Version(s):

0.1.1 (source: frontmatter and changelog, released 2026-06-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
