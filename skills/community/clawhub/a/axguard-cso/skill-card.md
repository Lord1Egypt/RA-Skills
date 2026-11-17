## Description:

Chief Security Officer workflow for AXguard - STRIDE-lite threat model, OWASP-oriented prioritization, confidence-gated findings, then audit/triage/fix/report handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuvonsec](https://clawhub.ai/user/shuvonsec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run an AXguard-led pre-ship security review, rank findings by OWASP-oriented impact, decide go/no-go status, and hand off audit, triage, fix, and report steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides security review and may produce local findings or suggested fixes that affect production or regulated codebases.

Mitigation: Review findings and proposed fixes before applying them, and use the skill's confidence gate to keep unsupported issues as needs-manual.

Risk: AXguard scanner severity can be treated as authoritative without considering reachable impact.

Mitigation: Use the skill's blast-radius re-ranking and go/no-go criteria before accepting blockers or waivers.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration]

**Output Format:** [Markdown with inline shell commands and a structured decision report contract]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local AXguard reports at .findings/axguard/axguard-report.{md,html,json}.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
