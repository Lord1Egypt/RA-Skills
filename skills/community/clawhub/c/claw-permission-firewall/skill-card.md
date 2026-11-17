## Description:

Evaluates requested agent actions against least-privilege policy and returns allow, deny, or confirmation decisions with redacted actions and audit records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bharathjanumpally](https://clawhub.ai/user/bharathjanumpally)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to evaluate proposed HTTP, file, and command actions before execution, enforce policy-based decisions, redact secrets, and produce audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says verified implementation flaws mean this skill should not be trusted as a hard security boundary.

Mitigation: Use it as an advisory evaluator and keep executor-side allowlists and independent authorization checks for HTTP, file, and command actions.

Risk: Policy-bypass issues may affect protection of secrets and workspace boundaries.

Mitigation: Keep separate secret handling and workspace-boundary enforcement in the executor, audit dependency updates, and avoid real credentials in examples or test inputs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bharathjanumpally/skills/claw-permission-firewall)

## Skill Output:

**Output Type(s):** [json, configuration, guidance]

**Output Format:** [JSON decision object with optional confirmation prompt and structured audit record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes decision, riskScore, reasons, sanitizedAction, confirmation when needed, and audit metadata.]

## Skill Version(s):

1.0.0 (source: package.json, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
