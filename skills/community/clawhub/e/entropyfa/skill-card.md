## Description:

Verified financial planning data and blazing-fast, deterministic calculators for Monte Carlo projection, goal solving, Roth conversions, RMDs, income tax, estate tax, and pension analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flath12](https://clawhub.ai/user/flath12)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and financial-planning practitioners use this skill to retrieve source-backed planning reference data and run deterministic local calculations through the entropyfa CLI for tax, retirement, estate, pension, projection, and goal-solving workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial planning, tax, and legal calculations may be mistaken for professional advice.

Mitigation: Treat outputs as planning calculations with provenance and not as a substitute for professional financial, tax, or legal advice.

Risk: Sensitive financial inputs may be sent to the local CLI during calculations.

Mitigation: Review financial inputs before sending them to the entropyfa CLI and install only if the CLI source is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flath12/skills/entropyfa)
- [entropyFA OpenClaw Homepage](https://github.com/Entropy-Financial-Technologies/entropyfa-cli/tree/main/integrations/openclaw/entropyfa)
- [Workflows](references/workflows.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Text]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Projection commands default to machine-readable JSON unless terminal visuals are explicitly requested.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
