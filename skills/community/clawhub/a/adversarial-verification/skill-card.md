## Description:

Adversarial Verification helps agents challenge assumptions, run real verification commands, and return clear PASS or FAIL outcomes for software changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minijoy-b](https://clawhub.ai/user/minijoy-b)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to plan and execute adversarial verification of frontend, backend, CLI, infrastructure, package, and bug-fix changes before commits, deployments, or reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The verifier can run target-controlled commands on the host without enforcing the sandboxing described by the skill.

Mitigation: Install and run it only in a disposable, credential-free sandbox; avoid production paths and untrusted repositories until command execution is isolated.

Risk: CLI filename handling may allow unsafe behavior when validating arbitrary targets.

Mitigation: Use controlled target paths and review command invocations before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/minijoy-b/skills/adversarial-verification)
- [Quick Start](examples/quick-start.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style verification report with command lists, result summaries, failure details, and PASS or FAIL verdicts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include executed commands, stdout or stderr summaries, reproduction steps, and suggested fixes.]

## Skill Version(s):

1.0.3 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
