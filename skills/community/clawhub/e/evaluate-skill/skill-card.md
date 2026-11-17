## Description:

Measures a skill's reliability through repeated evaluations, eval design and interpretation, and comparisons against the base agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edonadei](https://clawhub.ai/user/edonadei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to design and run Caliper evaluations, measure repeatability, and compare a skill with an agent running without it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party evaluation specs can execute setup, cleanup, assertions, connectors, or git-sourced content.

Mitigation: Review setup, cleanup, assert, mcp, and git-source entries before running a spec.

Risk: User customizations can change results or make shared comparisons misleading.

Mitigation: Use isolated runs when comparing backends, sharing measurements, or measuring the bare agent.

Risk: Saved evaluation transcripts and snapshots may contain sensitive project or prompt data.

Mitigation: Keep .caliper/results out of commits and review saved results before sharing.

## Reference(s):

- [Evaluate Skill on ClawHub](https://clawhub.ai/edonadei/skills/evaluate-skill)
- [Caliper Reference](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Guidance, YAML configuration, Shell commands, Evaluation reports]

**Output Format:** [Markdown guidance, .eval.yaml specs, and Caliper results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create evaluation specs and save run results for later comparison.]

## Skill Version(s):

1.0.14 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
