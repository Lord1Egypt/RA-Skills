## Description:

Bootstrap skill for DiagForge. Use this skill to onboard an agent into the DiagForge GitHub repository, understand the project structure, run the canonical cold-start smoke test, and begin working with the Visio-based drawing loop safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qweadzchn](https://clawhub.ai/user/qweadzchn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to bootstrap into the DiagForge repository, follow the intended first-read documents, validate the Visio bridge with a cold-start smoke test, and begin figure reproduction work that targets editable Visio outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to clone and run unpinned external repository code while using a token-bearing environment.

Mitigation: Review or trust the DiagForge repository before running scripts, use an isolated environment, pin or inspect a specific commit, and expose VISIO_BRIDGE_TOKEN only when required.

## Reference(s):

- [DiagForge repository](https://github.com/qweadzchn/DiagForge)
- [Agent Visio User on ClawHub](https://clawhub.ai/qweadzchn/skills/diagforge-agent-visio-user)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes repository links, read-order guidance, smoke-test commands, and environment requirements for git, python, and VISIO_BRIDGE_TOKEN.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
