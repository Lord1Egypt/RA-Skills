## Description:

Analyze and optimize Aptos Move contracts for gas efficiency, identifying expensive operations and suggesting optimizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Aptos Move contracts for gas-heavy storage, computation, reference, event, and collection patterns before deployment or high-frequency use. It helps produce optimization recommendations, measurement steps, and report-ready findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gas optimization recommendations could weaken a contract if security checks or validation paths are removed.

Mitigation: Review proposed changes carefully and keep access control, input validation, and other security checks intact.

Risk: Suggested optimizations may not produce the expected cost reduction or may change behavior without measurement.

Mitigation: Profile before and after each change, run tests, and document gas costs for public functions before deployment.

Risk: Gas analysis could expose sensitive local Aptos configuration if private-key or profile files are read unnecessarily.

Mitigation: Avoid using local private-key files or Aptos profile files during analysis unless a separate trusted workflow explicitly requires them.

## Reference(s):

- [Aptos Gas Schedule](https://github.com/aptos-labs/aptos-core/blob/main/aptos-move/aptos-gas-schedule)
- [Move VM Gas Metering](https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/aptos-vm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Move and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optimization checklists, before-and-after examples, gas measurement steps, and report-style recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
