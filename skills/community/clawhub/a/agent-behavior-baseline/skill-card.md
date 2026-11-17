## Description:

Establish an observable baseline for an AI agent before changing it by using a minimal SQLite trace store, a fixed eval suite with stable IDs, real-task wiring, memory retrieval measurements, and adherence checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cengcengcai-creator](https://clawhub.ai/user/cengcengcai-creator)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use it before changing an agent's prompts, tools, or retrieval setup to establish and compare trace, evaluation, memory retrieval, and rule-adherence baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An untrusted task suite may provide commands that the evaluation script runs through a shell.

Mitigation: Run only trusted task suites and keep them reviewed and controlled.

## Reference(s):

- [Agent Behavior Baseline on ClawHub](https://clawhub.ai/cengcengcai-creator/skills/agent-behavior-baseline)
- [Adherence eval](references/adherence-eval.md)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance and reports, Python scripts, JSON evaluation tasks and results, and SQLite trace data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates environment smoke checks from behavior quality results; reports sample denominators and limits.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
