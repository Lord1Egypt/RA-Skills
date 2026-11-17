## Description:

Aegis Quality Guardian provides contract-driven, design-first guardrails for AI-assisted full-stack development across design, contract, implementation, verification, and project management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterhiroshi](https://clawhub.ai/user/peterhiroshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure AI-assisted full-stack work around design briefs, API contracts, implementation constraints, verification gates, and multi-agent coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflows can persistently change repositories by writing guardrail scripts, Git hooks, and generated CI configuration.

Mitigation: Review planned file changes before applying setup workflows, use dry-run or manual review where available, and require explicit approval before writing hooks or CI in sensitive repositories.

Risk: Dependency and code-generation patterns were flagged as unsafe by the server security summary.

Mitigation: Pin dependency versions, inspect generated code and CI before execution, and defer sensitive-repository use until the reported code-generation injection issues are fixed.

## Reference(s):

- [Aegis Quality Guardian on ClawHub](https://clawhub.ai/peterhiroshi/skills/aegis-quality-guardian)
- [Contract-First Development Guide](references/contract-first-guide.md)
- [Contract-First Development Guide](references/contract-guide.md)
- [Dispatch Protocol](references/dispatch-protocol.md)
- [Multi-Agent Protocol](references/multi-agent-protocol.md)
- [Testing Strategy](references/testing-strategy.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, project templates, YAML configuration, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or modify project contract files, guardrail scripts, Git hooks, CI configuration, and design documentation when the user chooses setup workflows.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
