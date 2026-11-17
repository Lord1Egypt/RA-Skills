## Description:

Helps agent operators keep assistants responsive by delegating long tasks, installing instruction rules, and auditing supported agent configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep an assistant available for user messages while longer work is delegated. It provides a dry-run-first installer for Hermes and Claude Code, a pasteable rule block for other platforms, and a file-level configuration audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the installer changes supported agent instruction files and may affect future assistant behavior.

Mitigation: Preview affected files without --apply, read the rule block, and keep the generated backups before applying changes.

Risk: A file-level audit does not establish that the agent has loaded the updated rules.

Mitigation: Restart or reload the affected agent and verify its behavior after the audit.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/agent-responsiveness-delegation)
- [Hermes implementation reference](references/hermes-implementation.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown, JSON audit reports]

**Output Format:** [Markdown instructions and rule block; optional JSON audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; applying changes backs up existing instruction files.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
