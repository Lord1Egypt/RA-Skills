## Description:

Use this skill when evolving OpenClaw skills through benchmarking, red-teaming, regression protection, and iterative refinement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to evaluate and improve OpenClaw skills with baselines, golden tests, red-team cases, regression checks, and rollback-aware deployment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production skill changes can affect shared tools, credentials, financial workflows, deletion behavior, security boundaries, or system-wide behavior.

Mitigation: Keep production changes under human review and require sandbox candidates, diffs, tests, and rollback plans before deployment.

Risk: Skill evolution guidance can produce incorrect or misleading proposals if benchmarks, red-team cases, or regression checks are skipped.

Mitigation: Require baselines, golden tests, red-team tests, and comparison against the previous stable behavior before accepting a candidate change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/agent-skill-evolution)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists, candidate changes, test plans, shell commands, and review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed diffs, benchmark results, risk notes, and rollback steps.]

## Skill Version(s):

1.0.1 (source: frontmatter, _meta.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
