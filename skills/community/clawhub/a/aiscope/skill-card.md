## Description:

Audits local AI coding instructions for duplicates, conflicts, and scope problems using AIScope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayanth-mkv](https://clawhub.ai/user/jayanth-mkv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify conflicting or duplicated AI coding rules across project instruction files and review their scope before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit relies on an external AIScope CLI that reads local AI instruction files.

Mitigation: Confirm the CLI source is trusted before installing and run it only on projects you intend to audit.

Risk: Including user-wide memory can expose additional private instructions to the audit.

Mitigation: Use --user only when user-wide memory is explicitly requested, and keep private instruction content out of public reports.

## Reference(s):

- [AIScope on ClawHub](https://clawhub.ai/jayanth-mkv/skills/aiscope)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate conflicts include source file and line references, scope, and severity; token counts are estimates.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
