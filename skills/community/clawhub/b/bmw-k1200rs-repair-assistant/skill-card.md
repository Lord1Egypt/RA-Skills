## Description:

BMW K1200RS Repair Assistant helps agents provide cautious, manual-backed motorcycle repair triage, diagnostics, maintenance planning, workshop checklists, and verification guidance for BMW K1200RS motorcycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[levomm](https://clawhub.ai/user/levomm)

### License/Terms of Use:

MIT

## Use Case:

External users and mechanics use this skill to reason from BMW K1200RS symptoms to safe checks, likely causes, required tools, manual lookups, and repair verification steps. It is intended as decision support and requires user-provided, legally obtained BMW Repair Manual evidence for factory values and procedures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent could give repair guidance that users mistake for professional certification of safety or roadworthiness.

Mitigation: State that the skill is decision support only and direct users to a qualified technician for safety-critical or uncertain work.

Risk: Factory specifications, torque values, wiring details, or procedures could be wrong if supplied without source evidence.

Mitigation: Require users to verify those details in a legally obtained BMW Repair Manual and avoid inventing exact values or sequences.

Risk: Motorcycle repair work can create safety hazards involving brakes, steering, suspension, fuel, throttle, ABS, electrical systems, or road tests.

Mitigation: Begin with hazard checks, call out stop conditions, and require static checks, leak checks, fastener checks, brake checks, and cautious low-speed verification before normal riding.

Risk: The skill could be used to reproduce proprietary BMW repair manual content.

Mitigation: Use only short user-provided excerpts when needed, paraphrase the rest, and point users back to their own legally obtained manual.

## Reference(s):

- [Manual Policy](references/manual-policy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured diagnostic and maintenance sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include safety precautions, ranked checks, manual lookup items, tools and parts, and verification steps.]

## Skill Version(s):

1.0.0 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
