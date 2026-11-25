## Description:

Validate OpenClaw PR stacks and custom builds with OCM and Crabbox evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to compose and validate a fixed OpenClaw custom candidate, prove requested behavior locally with OCM, and use Crabbox when remote reproduction adds useful evidence. It records results while keeping the personal installation intact unless adoption is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign with medium confidence, and two scripts were not fully evaluated.

Mitigation: Review script behavior and confirm the skill’s environment access and tool scope fit your needs before installing.

Risk: The workflow notes that OCM is not an OS security sandbox for untrusted PR code and that copied integrations may have external activity.

Mitigation: Use secretless isolated reproduction, verify fixture containment, and keep copied external activity inactive until authorized.

## Reference(s):

- [Patch stack and incremental refresh](artifact/references/patch-refresh.md)
- [Optional fixture diagnostics](artifact/references/diagnostics.md)
- [Pending completion across a Gateway restart](artifact/references/stateful-restart.md)
- [Adopt an exact validated candidate](artifact/references/adoption.md)
- [Structured result and native comment publisher](artifact/references/reporting.md)
- [Check source without changing the run](artifact/references/skill-updates.md)
- [ClawHub skill page](https://clawhub.ai/theangrypit/skills/custom-build-validation)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, JSON, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown validation worksheet and evidence summary, with a structured JSON report when closing out a run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope varies by candidate components, requested tests, and whether remote proof is needed.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
