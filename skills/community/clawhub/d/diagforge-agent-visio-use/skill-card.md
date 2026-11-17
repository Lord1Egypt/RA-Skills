## Description:

Bootstrap skill for DiagForge that helps an agent find the repository, understand the project structure, run the canonical cold-start smoke test, and start the Visio-based drawing loop safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qweadzchn](https://clawhub.ai/user/qweadzchn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to onboard into the DiagForge workflow, validate the local Visio bridge path, and begin producing editable Visio diagram assets from reference figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to clone and run unpinned external repository code.

Mitigation: Verify the DiagForge repository state and maintainer before running commands, and execute cloned code with the least filesystem and environment access practical.

Risk: The local Visio bridge uses VISIO_BRIDGE_TOKEN for bridge-backed smoke tests and execution.

Mitigation: Avoid exposing VISIO_BRIDGE_TOKEN until the bridge is needed, and keep the token scoped to the user's local bridge environment.

## Reference(s):

- [DiagForge GitHub repository](https://github.com/qweadzchn/DiagForge)
- [ClawHub skill page](https://clawhub.ai/qweadzchn/skills/diagforge-agent-visio-use)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, configuration]

**Output Format:** [Markdown guidance with shell and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides repository cloning, document read order, smoke-test execution, and expected editable Visio outputs.]

## Skill Version(s):

0.1.2 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
