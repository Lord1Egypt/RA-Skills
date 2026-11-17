## Description:

Enforce system-wide consistency before code changes by guiding agents through global scans, source-of-truth identification, grouped edits, residue audits, and regression verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upsightx](https://clawhub.ai/user/upsightx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when refactoring, cleaning legacy paths, aligning schemas, consolidating state machines, or making other cross-file code changes that must preserve architectural consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual or npx installation could resolve to a source different from the reviewed ClawHub artifact.

Mitigation: Install from the reviewed ClawHub artifact when possible, or pin and verify the manual installation source.

Risk: Broad consistency scans can include irrelevant directories or produce an affected-file plan that is too wide for the intended change.

Mitigation: Review the proposed affected-file plan before edits and keep scans limited to relevant project directories.

Risk: Choosing the wrong source of truth can lead to misleading refactor guidance or incomplete cleanup.

Mitigation: Require the agent to name the canonical file or module, list competing sources, and document retained compatibility before making edits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upsightx/skills/architecture-consistency-guardian)
- [Workflow Details](references/workflow.md)
- [Output Template](references/output_template.md)
- [Common Consistency Risk Patterns](references/risk_patterns.md)
- [Architecture Contract Template](references/contract_template.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples, structured reports, and optional JSON scan summaries from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce affected-file plans, architecture contract drafts, consistency reports, residue scan summaries, and concrete verification commands.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
