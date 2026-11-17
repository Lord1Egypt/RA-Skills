## Description:

Audit agentic framework directories, prompt systems, skills, planner files, workflow guidance, memory-like files, configs, and agent-facing documentation for behavioral failures, prompt bloat, instruction conflicts, over-enforcement, unsafe autonomy, prompt-injection exposure, inefficient tool-use guidance, layer drift, review-integrity risks, and production-readiness issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[illimitedenterprise](https://clawhub.ai/user/illimitedenterprise)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit agentic framework projects, prompts, skills, workflows, configs, and local instructions for behavioral-control risks before release or deployment. It supports report-only review, deterministic findings, fix planning, and optional bounded same-agent review evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads local project text and writes report artifacts, so an unintended target or output path can expose or alter files outside the intended audit scope.

Mitigation: Confirm target roots before running the scanner, keep output in a dedicated directory, and use a simple filename-only artifact prefix.

Risk: Crafted symlinks or attacker-controlled trees can cause scans to reach content outside the expected folders.

Mitigation: Avoid running the skill on attacker-controlled directory trees with symlinks, or inspect and remove unsafe links before scanning.

Risk: Sensitive files may be included if the operator explicitly broadens scope.

Mitigation: Leave sensitive-file scanning disabled unless that scope is intentional, and do not include home or credential-bearing files by default.

## Reference(s):

- [Audit Taxonomy](references/audit-taxonomy.md)
- [Framework Profiles](references/framework-profiles.md)
- [ClawHub Release Checklist](references/clawhub-release.md)
- [ClawHub Skill Page](https://clawhub.ai/illimitedenterprise/skills/agentic-framework-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON findings and review packets, CSV inventories, instruction graphs, fix plans, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report-only by default; optional same-agent review packets require deterministic gate readiness and an accountable reviewer identity.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
