## Description:

Calculate temperature excursion risks for cold chain transport, including route risk, packaging suitability, and monitoring requirements for biological samples and pharmaceuticals requiring controlled-temperature shipping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quality teams, and logistics operators use this skill to assess temperature-excursion risk for cold-chain transport scenarios using route, duration, and packaging inputs. It is suited to preliminary shipping risk documentation for biological samples, vaccines, and temperature-sensitive pharmaceuticals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The calculator may be used for regulated shipping decisions even though the documented model and packaged script behavior do not fully match.

Mitigation: Verify the calculator's correctness and confirm assumptions before relying on its results for regulated or quality-critical shipments.

Risk: The simplified risk model does not account for route complexity, transit legs, or ambient temperature variability.

Mitigation: Treat results as preliminary screening guidance and document unresolved route and environmental factors before shipment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/cold-chain-risk-calculator-1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill documents structured JSON output, but the packaged script prints plain-text route, duration, packaging, risk score, and risk level lines.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
