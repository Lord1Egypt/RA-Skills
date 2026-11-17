## Description:

Helps developers revise a previously advanced feature decision by assessing its impact first, then reconciling requirements, design, tasks, implementation, and validation within confirmed, recoverable boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songzhuozhu](https://clawhub.ai/user/songzhuozhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to assess the effects of a changed feature decision, obtain approval for a bounded revision, and reconcile project artifacts through a verifiable completion or restoration process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved revisions may change or delete project files outside the intended scope.

Mitigation: Review the initial read-only assessment and confirm writable roots and deletion lists narrowly before allowing edits.

Risk: A local recovery record may contain original sensitive content or large file payloads until closure or restoration.

Mitigation: Avoid approving sensitive or large recovery payloads unless their temporary local retention is acceptable.

## Reference(s):

- [ClawHub release](https://clawhub.ai/songzhuozhu/skills/feature-retcon)
- [Read-only assessment](references/assessment.md)
- [Stage gates](references/stage-gates.md)
- [Reconciliation contract and recovery](references/contract-schema.md)
- [Closure evidence](references/closure-evidence.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports and project file changes, with JSON closure evidence when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Begins with a read-only assessment; changes require explicit confirmation and a recoverable revision record.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
