## Description:

Calculate cold chain transport risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shanruoyu](https://clawhub.ai/user/shanruoyu)

### License/Terms of Use:

MIT-0

## Use Case:

Logistics, laboratory operations, and cold-chain support users can run this skill to estimate route risk from transport duration and packaging choice for temperature-sensitive shipments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The calculator is a draft estimator and may be mistaken for an authoritative logistics or compliance decision tool.

Mitigation: Use its results as advisory only and have qualified cold-chain or compliance personnel review decisions before shipment.

Risk: Duration input is not constrained to realistic positive values, which can produce misleading risk scores.

Mitigation: Run the script only with realistic positive transport durations and validate inputs in any operational wrapper.

Risk: The documentation mentions file input/output more broadly than the current script implements.

Mitigation: Confirm expected behavior before relying on workspace files or generated reports; the current script prints results to standard output.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text CLI output with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs route, duration, packaging, numeric risk score, and a Low/Medium/High risk level.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
