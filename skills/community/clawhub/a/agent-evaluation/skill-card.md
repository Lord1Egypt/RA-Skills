## Description:

Testing and benchmarking LLM agents, including behavioral testing, capability assessment, reliability metrics, and production monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rustyorb](https://clawhub.ai/user/rustyorb)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to design and review LLM agent evaluations, including behavioral tests, capability assessments, reliability metrics, adversarial tests, and production monitoring practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adversarial evaluation suggestions could be applied to agents or test data the user is not authorized to assess.

Mitigation: Use the skill only with authorized agents, systems, and data, and review adversarial test plans before execution.

Risk: Evaluation data leakage can make benchmark or regression results misleading.

Mitigation: Keep held-out test data separate from training data, prompts, and optimization loops.

Risk: Single-run LLM agent tests can produce unstable or misleading pass/fail results.

Mitigation: Run tests multiple times and evaluate result distributions, invariants, and reliability metrics.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rustyorb/skills/agent-evaluation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include evaluation plans, behavioral test cases, benchmark designs, reliability metrics, and monitoring guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
