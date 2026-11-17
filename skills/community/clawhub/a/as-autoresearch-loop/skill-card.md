## Description:

Applies Karpathy's autoresearch methodology to iteratively improve measurable artifacts such as Claude skills, n8n workflows, system prompts, business processes, or reusable documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autosolutionsai-didac](https://clawhub.ai/user/autosolutionsai-didac)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and workflow owners use this skill to set up a measured improvement loop for a reusable artifact. It guides them to define the artifact, fixed evaluation set, metric, budget, experiment log, and stop conditions before iterating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes nested and historical skill copies with broad trigger and unbounded loop language.

Mitigation: Review the package before installation and remove or quarantine obsolete nested/versioned skill copies so only the intended bounded release is active.

Risk: The skill can guide an agent to edit files, run evaluations, and keep persistent experiment logs.

Mitigation: Run loops in a sandbox, branch, or copied workspace with explicit time, iteration, and cost limits before applying a winning artifact.

Risk: Evaluation data can overfit the artifact or expose real user data if handled carelessly.

Mitigation: Keep evals separate from artifact editing, redact sensitive data, and reserve holdout or regression prompts for validation rather than optimization.

Risk: Automated or unattended loops can create misleading improvements or unsafe production changes.

Mitigation: Require deterministic evals, anomaly alerts, periodic human review, and human approval before any production deployment.

## Reference(s):

- [Karpathy autoresearch methodology](https://github.com/karpathy/autoresearch)
- [ClawHub AS Autoresearch Loop release page](https://clawhub.ai/autosolutionsai-didac/skills/as-autoresearch-loop)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with example commands, checklists, and tabular experiment logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update experiment logs, evaluation rubrics, backup instructions, and candidate artifact changes when the user authorizes an improvement loop.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
