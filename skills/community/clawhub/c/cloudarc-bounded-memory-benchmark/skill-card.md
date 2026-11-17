## Description:

Make CloudArc large-package performance reproducible, measurable and safe to ship.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to benchmark CloudArc large-package workflows, verify bounded-memory pack and unpack behavior, validate multi-file deduplication, check remote-search telemetry, and keep CI and manual benchmark gates aligned with the release contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark commands can consume significant CPU, memory, runtime, and temporary disk, especially the manual 1/5/10 GiB profile.

Mitigation: Run the skill only in an appropriate CloudArc development repository, prefer smoke or selfcheck commands for routine validation, and use the manual benchmark only when the large run is intentional.

Risk: Cleanup commands and generated reports affect the working directory and local temporary directories.

Mitigation: Review cleanup commands before execution in unusual environments and verify generated JSON and Markdown artifacts before relying on benchmark results.

## Reference(s):

- [CloudArc Benchmark Contract](artifact/references/contract.md)
- [CloudArc Bounded-Memory Benchmark Release Notes](artifact/references/release-notes.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands, Python entry points, JSON telemetry examples, and CI workflow expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces benchmark and telemetry guidance for agent execution; helper commands may produce JSON, Markdown, and SVG result artifacts.]

## Skill Version(s):

1.4.2 (source: frontmatter, VERSION, release metadata, release notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
