## Description:

Scans installed skills and AGENTS.md to generate a routing config that maps conversation intents to skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ordo-tech](https://clawhub.ai/user/ordo-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate and refresh skill_routing rules from installed skill descriptions and existing AGENTS.md context. It helps maintain a human-readable routing reference for larger skill libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent routing changes based on third-party skill descriptions can introduce overly broad, misleading, or suspicious triggers.

Mitigation: Review the generated routing block before allowing it into AGENTS.md, especially when third-party skills are installed.

Risk: Refreshing the generated Skill Routing section can overwrite manual routing edits.

Mitigation: Preserve custom rules outside the generated block and prefer writing router.yml first when reviewing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ordo-tech/skills/auto-invoke-router)
- [Publisher skill homepage](https://clawhub.com/@ordo-tech/auto-invoke-router)

## Skill Output:

**Output Type(s):** [configuration, markdown, shell commands, guidance]

**Output Format:** [Markdown with YAML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a generated Skill Routing section to AGENTS.md or a standalone router.yml, plus a summary of mapped, skipped, and ambiguous triggers.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
