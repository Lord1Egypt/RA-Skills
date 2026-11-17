## Description:

Adversarial Design Review helps agents pressure-test risky software designs with parallel specialist reviews before implementation, then reconcile concrete failure scenarios and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before implementing hard-to-debug or hard-to-reverse systems work, such as drivers, protocols, concurrent code, storage formats, and CI gates. It guides a multi-agent adversarial review that returns concrete design failure scenarios, fixes, and validations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parallel review agents may inspect repository files named in the design brief or surrounding code needed to evaluate it.

Mitigation: Run the skill only in workspaces where that review is appropriate, and scope the brief to the files agents should inspect.

Risk: Adversarial findings are proposals and may be incorrect, overstated, or incomplete.

Mitigation: Reconcile each finding against the real code, apply only confirmed gaps, and gate resulting claims with runtime evidence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nickflach/skills/adversarial-design-review)
- [Field Playbook](docs/PLAYBOOK.md)
- [Attack Workflow Template](resources/attack-workflow.template.js)
- [QuantumOS Case Study Repository](https://github.com/flaukowski/QuantumOS)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with an optional JavaScript workflow template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review prompts, ranked findings, specific fixes, and implementation-gating guidance for the user's design brief.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
