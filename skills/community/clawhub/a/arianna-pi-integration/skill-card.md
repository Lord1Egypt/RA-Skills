## Description:

Integrates the Playfilo shared-memory DAG into the pi-mono coding agent. Adds DAG persistence, time-travel tools (tobe, life, recall, trace), and cross-session memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujilabs](https://clawhub.ai/user/wujilabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to patch pi-mono's coding agent with Playfilo DAG persistence, cross-session memory, temporal navigation tools, and a system-prompt seed extension.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cross-session memory may store prompts, reasoning, tool outputs, code, and secrets in local Playfilo files.

Mitigation: Use this skill only when persistent agent memory is intended; treat ~/.playfilo/playfilo.db and ~/.playfilo/tobe_debug.log as sensitive; add redaction, permissions, retention, and delete controls for sensitive workspaces.

Risk: The skill installs persistent system-prompt-changing behavior through a Pi extension.

Mitigation: Review or remove the seed extension before use, and document any prompt changes for users and operators.

Risk: Patch and dependency changes can alter a coding agent's runtime behavior.

Mitigation: Pin dependencies, review patches before execution, and run the bundled verification checklist in a non-sensitive checkout before deployment.

## Reference(s):

- [Arianna homepage](https://arianna.run)
- [ClawHub skill page](https://clawhub.ai/wujilabs/skills/arianna-pi-integration)
- [Playfilo integration skill](SKILL.md)
- [Playtiss-backed storage module notes](playtiss/core/README.md)
- [Verification checklist](filo/patches/verify.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown patch instructions with TypeScript source and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces additive integration guidance and bundled source for a target pi-mono checkout; patch application is performed by the consuming agent or developer.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
