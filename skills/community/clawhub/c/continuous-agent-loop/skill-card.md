## Description:

Provides patterns for autonomous agent loops, including sequential, RFC, CI/PR, and exploratory workflows, with quality gates, evaluations, and recovery controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:


## Use Case:

Developers use this skill to choose and structure autonomous agent loops, define quality gates and evaluations, and recover from stalled or failing iterations. It also provides a local repository harness audit workflow and guidance for keeping human approval around long-running loops and remote changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent loop or repository workflow could make broad changes or affect shared remote systems.

Mitigation: Scope each run to one intended repository, prefer a dry run when available, and require explicit confirmation before starting persistent loops or creating, pushing, merging, or publishing remote changes.

Risk: Audit scores could be mistaken for a complete security assessment.

Mitigation: Treat scores as a structural checklist rather than proof of security; the provided security review did not exercise live loop behavior.

## Reference(s):

- [Continuous Agent Loop on ClawHub](https://clawhub.ai/djc00p/skills/continuous-agent-loop)
- [Harness Audit Command](references/harness-audit.md)
- [Harness Audit Script](scripts/harness-audit.js)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Text, JSON]

**Output Format:** [Loop recommendations and operating guidance in Markdown; deterministic audit scorecards in text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The audit can be scoped with AUDIT_ROOT or --root. Its score is a structural checklist, not proof of security.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
