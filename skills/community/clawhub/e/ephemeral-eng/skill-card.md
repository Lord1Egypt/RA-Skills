## Description:

Builds single-file HTML engineering calculators whose input panel produces a print-ready, paginated calculation report or evaluation letter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oasiseng](https://clawhub.ai/user/oasiseng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering practitioners use this skill to create or revise self-contained browser-based calculation tools and evaluation-letter generators for simple, hand-verifiable engineering checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated engineering tools could be mistaken for verified deliverables.

Mitigation: Keep the draft watermark and verification footer, and require independent review with a digit-for-digit hand calculation before use.

Risk: The skill may be invoked for engineering checks outside simple, hand-verifiable calculations.

Mitigation: Decline finite-element analysis, dynamic or seismic response, nonlinear analysis, and coupled-system analysis; direct those cases to validated commercial software.

Risk: Incorrect code coefficients or table values could create misleading results.

Mitigation: Expose uncertain code values as engineer-entered inputs instead of hard-coding guessed constants.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oasiseng/skills/ephemeral-eng)

## Skill Output:

**Output Type(s):** [Code, Markdown, Configuration, Guidance]

**Output Format:** [Single-file HTML with embedded CSS and JavaScript, Markdown guidance, and optional JSON input state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated tools are draft engineering deliverables that require independent verification before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
