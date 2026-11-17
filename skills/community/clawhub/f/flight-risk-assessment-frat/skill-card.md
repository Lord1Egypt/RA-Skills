## Description:

Runs a pre-flight FRAT for pilots, dispatchers, chief pilots, or flight-school instructors by walking PAVE and IMSAFE, scoring risk, mapping Green/Yellow/Red status, and producing a draft FRAT log with mitigations and dispatch guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Pilots, dispatchers, chief pilots, and flight-school instructors use this skill to structure pre-flight and re-FRAT risk assessments for Part 91, 135, 137, 141, public-use, or business-aviation flights. The skill supports SMS documentation and mitigation planning while keeping final go/no-go authority with the pilot-in-command and operator roles.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Users could mistake the draft FRAT log for flight authorization or final go/no-go advice.

Mitigation: Keep the output explicitly marked as draft decision-support and leave final authority with the PIC, dispatcher, chief pilot, maintenance, or director of operations as applicable.

Risk: The assessment may be incomplete or stale if weather, NOTAMs, TFRs, MEL items, fatigue, route, passengers, or mission conditions change.

Mitigation: Require current official sources and operator procedures, and rerun the FRAT whenever material inputs change before takeoff.

Risk: Incorrect regulatory, airworthiness, or maintenance interpretation could affect a high-stakes aviation decision.

Mitigation: Use the skill as a structured checklist only; maintenance, airworthiness, regulatory compliance, and dispatch decisions remain with qualified human roles and the operator's procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/flight-risk-assessment-frat)
- [Skill README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown FRAT log with tables, scored rationale, mitigations, and dispatch-authority recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft only; requires current official sources, operator procedures, and human decision authority.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
