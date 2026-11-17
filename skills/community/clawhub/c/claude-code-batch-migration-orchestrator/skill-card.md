## Description:

Use when the user wants a large, mechanical change split into many independent units and executed in parallel with isolated workers and PRs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate broad codebase migrations by splitting work into isolated units, defining verification, and collecting mergeable outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad migration workflows can cause unintended repository-wide edits when scope boundaries are unclear.

Mitigation: Define explicit scope boundaries, isolated work units, and verification steps before running parallel migration work.

Risk: Parallel workers can conflict if they edit overlapping files or tightly coupled modules.

Mitigation: Parallelize only independent units and require each unit to validate its own changes before integration.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with structured plans, verification steps, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include parallel work-unit plans, worker prompts, PR or patch summaries, and failure summaries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
