## Description:

Bootstrap skill for DrawForge that helps an agent onboard into the DrawForge GitHub repository, understand the project structure, run the canonical cold-start smoke test, and begin working with the Visio-based drawing loop safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qweadzchn](https://clawhub.ai/user/qweadzchn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to onboard into DrawForge, validate a local Visio bridge with the canonical smoke test, and begin producing editable Visio diagram outputs from reference figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to clone and run external DrawForge code without a server-resolved provenance record.

Mitigation: Review the upstream repository and pin or verify a specific commit before running the smoke test.

Risk: The Visio bridge flow uses VISIO_BRIDGE_TOKEN for local bridge access.

Mitigation: Provide the token only to commands that need bridge access and avoid exposing it during clone, setup, or general troubleshooting.

## Reference(s):

- [DrawForge GitHub repository](https://github.com/qweadzchn/DrawForge)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [References an external repository and local Visio bridge token requirements.]

## Skill Version(s):

0.1.2 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
