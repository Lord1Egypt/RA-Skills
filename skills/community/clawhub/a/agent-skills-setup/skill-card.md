## Description:

Helps developers migrate, back up, restore, and compare AI-coding-agent skills, instructions, and MCP configurations across supported profiles and computers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckycat133](https://clawhub.ai/user/luckycat133)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to preview, migrate, verify, back up, or restore selected AI-agent context across supported coding assistants and devices. Plugin packages and session handoff require explicit opt-in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration can read or change sensitive local agent-context files.

Mitigation: Limit scope to selected profiles, review the saved plan before applying, and retain backups and rollback manifests.

Risk: A broad device-wide snapshot can collect more context than intended.

Mitigation: Request device-wide discovery only when needed; otherwise select specific products and scopes.

Risk: Plugin and session opt-ins expose additional local surfaces.

Mitigation: Enable these options only after reviewing the additional material and destinations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/luckycat133/skills/agent-skills-setup)
- [CLI workflow](references/cli-workflow.md)
- [Migration safety](references/migration-safety.md)
- [Bundle workflow](references/bundle-workflow.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report plan and bundle paths, verification results, backups, and remaining manual work.]

## Skill Version(s):

0.10.2 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
