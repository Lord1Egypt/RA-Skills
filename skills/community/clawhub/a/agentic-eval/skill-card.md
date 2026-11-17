## Description:

Patterns and techniques for evaluating and improving AI agent outputs through self-critique, evaluator-optimizer loops, test-driven code refinement, rubrics, and LLM-as-judge workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boleyn](https://clawhub.ai/user/boleyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design evaluation loops that critique, score, and refine agent outputs for quality-critical code, reports, analysis, and compliance-sensitive content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code and generated tests may be executed without sufficient containment.

Mitigation: Run generated code and tests only in a disposable, least-privilege sandbox with no inherited secrets, restricted file access, network disabled by default, and strict time and resource limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/boleyn/skills/agentic-eval)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown with Python code examples and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evaluation patterns, rubric guidance, and example refinement loops.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
