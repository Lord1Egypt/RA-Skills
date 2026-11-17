## Description:

Audit a codebase through every lens its stack calls for, verify each finding, cluster them by root cause, deliver the fixes as a ticketed map, and untangle the structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit a codebase for concrete failures across the lenses relevant to its stack, verify findings, and organize them into a ticketed fix plan. They can also use it to apply authorized fixes or carry out a structural refactor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious, citing broad activation, approval handling, potentially unsafe operations, and partial inspection of referenced content.

Mitigation: Review the skill before installing. Limit its access to the files and shell it needs, and do not treat approvals stored in a handoff file as proof of authorization.

Risk: Security scan coverage was partial: 21 of 22 components were scanned, and one shell script was only partially inspected.

Mitigation: Review the partially inspected shell script and related behavior before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orensegal/skills/codebase-audit)
- [Project homepage listed in Clawdis metadata](https://github.com/OrenSegal/codebase-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code]

**Output Format:** [Markdown audit reports, findings, handoff notes, and ticketed fix plans; optional source code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source changes require --fix or an authorized ticket; audits otherwise report and deliver findings first.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
