## Description:

Helps coding agents and work assistants turn session lessons into concise AGENTS.md rules, merge them into existing guidance, and propose changes for user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelegele](https://clawhub.ai/user/kelegele)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to preserve recurring lessons as concise, maintainable AGENTS.md guidance for coding or document-focused workspaces. It proposes file changes for user approval before writing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious with medium confidence, citing reported project-file writes and skill updates that may not align with the documented approval expectations.

Mitigation: Review the verdict before installing, and check whether automatic lifecycle logging and self-updates fit your needs.

Risk: Installation commands are unpinned, and the lifecycle hook can leave persistent project records.

Mitigation: Use a version-pinned installation when possible, and review the hook configuration and generated records before enabling it.

## Reference(s):

- [Agents.md specification](https://agents.md/)
- [Project homepage](https://github.com/kelegele/agentsmd-skill)
- [ClawHub release](https://clawhub.ai/kelegele/skills/agentsmd)
- [Agents.md reference in the skill](references/agents-md-spec.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown AGENTS.md rules and a proposed change plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rules are concise and actionable; file changes are proposed for user approval.]

## Skill Version(s):

1.6.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
