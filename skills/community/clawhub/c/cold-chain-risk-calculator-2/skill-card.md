## Description:

Calculate cold chain transport risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to estimate temperature excursion risk for cold chain transport routes based on route, duration, and packaging type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risk results can be misleading when invalid or unrealistic durations are supplied.

Mitigation: Validate transport duration before relying on the score, and treat the output as a lightweight estimate rather than operationally authoritative.

Risk: Future versions may add file output, input files, or data retention behavior.

Mitigation: Review and rescan future releases before deployment if those behaviors are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/cold-chain-risk-calculator-2)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints route, duration, packaging, numeric risk score, and risk level.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
