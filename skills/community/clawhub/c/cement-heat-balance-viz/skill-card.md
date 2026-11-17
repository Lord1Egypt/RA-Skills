## Description:

Generate visualizations for cement production heat balance analysis including process flow diagrams, energy distribution charts, and temperature profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luozhengrongyn](https://clawhub.ai/user/luozhengrongyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cement process engineers use this skill to turn heat-balance data into browser-viewable process flow, energy distribution, temperature profile, KPI, and combined technical visualizations for reports or presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include values from input heat-balance data, and the security evidence warns that malicious third-party JSON could inject browser-executed script.

Mitigation: Use trusted or sanitized input data, validate fields such as stage type, temperature, percentages, labels, and descriptions, and avoid opening or sharing generated reports from untrusted data until HTML escaping is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luozhengrongyn/skills/cement-heat-balance-viz)

## Skill Output:

**Output Type(s):** [code, shell commands, guidance, files]

**Output Format:** [Standalone HTML file and supporting agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML is intended for modern browsers and may include bilingual labels.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
