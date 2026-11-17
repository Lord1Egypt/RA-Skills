## Description:

Use when measuring OpenClaw agent quality objectively via baseline benchmarks, regression detection, golden test suites, scoring, model comparison, security evaluation, and upgrade gating before accepting changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to design and run objective evaluations for OpenClaw agents, skills, workflows, and system changes. It supports baseline comparison, golden test suites, regression detection, scoring, security evaluation, and upgrade gating before changes are accepted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad security and sandbox evaluation guidance could lead an agent to probe protected resources if used without a defined scope.

Mitigation: Run security and sandbox tests only in authorized environments with written scope, harmless canary fixtures, and no production secrets or private files.

Risk: Non-Indonesian users may misunderstand operational guidance written partly in Indonesian.

Mitigation: Review a translation before relying on the instructions for evaluation or release decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pmuhammadagus-byte/skills/agent-evaluation-benchmark-engine)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with structured evaluation checklists, scoring criteria, and benchmark reporting instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces evaluation plans and decision guidance; it does not execute benchmark tooling by itself.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; SKILL.md frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
