## Description:

Design Swarm guides agents through smart-home design deliverables including 3D renders, wiring diagrams, product catalogs, device placement plans, and SVG icons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoshung1981888](https://clawhub.ai/user/gaoshung1981888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design operators use this skill to coordinate smart-home design work from requirements through device placement, wiring plans, 3D renders, product catalog preparation, and delivery packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent local task files that may contain customer or project details.

Mitigation: Constrain the write location, define retention rules, and avoid storing sensitive customer details unless required.

Risk: The documented customer-name path pattern may be unsafe if user input is not sanitized.

Mitigation: Sanitize customer and project names before using them in file paths, and reject path traversal or shell metacharacters.

Risk: The skill declares network access without a clear need in the security evidence.

Mitigation: Install or run it with network access disabled unless a reviewed workflow explicitly requires network calls.

Risk: Wiring plans and 3D renders may not reflect site-specific conditions.

Mitigation: Require qualified human review before external delivery or implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gaoshung1981888/skills/design-swarm)
- [Publisher profile](https://clawhub.ai/user/gaoshung1981888)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and structured workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create local task files and design deliverables such as PNG, PDF, SVG, JSON, and Markdown files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
