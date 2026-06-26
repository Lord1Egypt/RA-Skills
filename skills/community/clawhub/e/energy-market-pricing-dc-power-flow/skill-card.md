## Description: <br>
DC power flow analysis for power systems. Use when computing power flows using DC approximation, building susceptance matrices, calculating line flows and loading percentages, or performing sensitivity analysis on transmission networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, power-system engineers, and energy-market analysts use this skill to apply DC power-flow approximations, construct susceptance matrices, calculate line flows, and reason about thermal loading in MATPOWER-style network data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network input data may be malformed, unexpected, or not MATPOWER-style, which can produce incorrect power-flow results. <br>
Mitigation: Review the local network JSON before running the helper script and confirm bus, branch, reactance, baseMVA, and rating fields match the expected MATPOWER-style structure. <br>
Risk: DC power-flow assumptions can omit AC effects such as losses, voltage magnitude variation, and large angle behavior. <br>
Mitigation: Use the outputs as DC approximation guidance and validate high-impact planning, operational, or market decisions with appropriate power-system review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wu-uk/energy-market-pricing-dc-power-flow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and local helper script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include calculations, matrix-building guidance, line-flow formulas, and review notes for local MATPOWER-style JSON inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
