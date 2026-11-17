## Description:

gate-switch is a claim-verification gate engine that lets agents express completion claims as JSON specs and mechanically checks them before returning pass, block, clarify, or violation verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xu-jin-cs](https://clawhub.ai/user/xu-jin-cs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use gate-switch to add mechanical verification gates to agent workflows, turning required truths into JSON specs that produce pass/block verdicts and audit logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Specs using script_exit can execute shell commands with the agent's current permissions.

Mitigation: Install only trusted specs; remove or disable script_exit, or require an allowlisted argv-style runner and sandbox in shared, automated, or sensitive environments.

Risk: Audit log bindings and file paths may reveal private project details.

Mitigation: Review the audit log location before use and avoid logging sensitive paths or values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xu-jin-cs/skills/gate-switch)
- [CLAIM_GATE_TEMPLATE.md](artifact/templates/CLAIM_GATE_TEMPLATE.md)
- [L3_FRAMEWORK_TEMPLATE.md](artifact/templates/L3_FRAMEWORK_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON spec examples and shell commands; the runner emits JSON verdict data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write JSONL audit logs at the configured log path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
