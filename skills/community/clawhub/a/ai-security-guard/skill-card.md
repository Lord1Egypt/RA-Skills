## Description:

AI Security Guard helps agents apply command-risk classification, permission modes, hook checks, sandbox isolation, and audit practices for safer shell-command workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as guidance for classifying risky shell commands, configuring permission rules, adding pre-execution checks, and auditing AI-assisted command behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is reference guidance and may be mistaken for a complete enforcement system.

Mitigation: Review and implement enforcement logic, hooks, and audit logging before relying on it for persistent command controls.

Risk: Bypass or auto permission modes can execute risky commands without adequate review in untrusted projects.

Mitigation: Use default or readonly modes for untrusted workspaces and require confirmation for high-risk command classes.

Risk: Sandbox network access may broaden exposure if enabled unnecessarily.

Mitigation: Disable sandbox network access unless the workflow explicitly requires it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/e2e5g/skills/ai-security-guard)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides reference patterns and checklists; it does not by itself enforce runtime policy.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
