## Description:

Creates, audits, or refactors engineering quality governance materials, including technical specifications, issue and improvement logs, risk-based verification workflows, and automated documentation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuworks](https://clawhub.ai/user/wuworks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to establish or maintain repository quality governance, including source-of-truth technical specs, structured defect and improvement history, proportional verification, and read-only documentation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Governance changes can encode incorrect project facts, overwrite useful history, or create misleading verification records.

Mitigation: Inspect the repository before editing, preserve existing history and identifiers, correct uncertain facts explicitly, and require verification evidence for completed records.

Risk: Repository scans or documentation updates can expose private research, secrets, or project-specific material.

Mitigation: Review paths and validator configuration before use, avoid unauthorized private areas, and keep validators read-only with explicit file inputs.

Risk: Context and command-output budgets can hide needed evidence if treated as hard safety limits.

Mitigation: Use budgets to reduce noise, but read additional evidence when risk, security review, or task scope requires it.

## Reference(s):

- [Project Quality Governance Skill Page](https://clawhub.ai/wuworks/skills/agent-project-quality-skill)
- [Technical Specification Architecture](references/technical-spec-architecture.md)
- [Issue and Improvement Log](references/issue-and-improvement-log.md)
- [Verification Workflow](references/verification-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should remain repository-neutral, evidence-based, diagnostic-only for validators, and scoped to the user's authorized project files.]

## Skill Version(s):

0.1.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
