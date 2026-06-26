## Description: <br>
Extract locational marginal prices (LMPs) from DC-OPF solutions using dual values. Use when computing nodal electricity prices, reserve clearing prices, or performing price impact analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and energy-market analysts use this skill to extract nodal prices, reserve clearing prices, binding-line indicators, and counterfactual price impacts from DC-OPF optimization results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security telemetry reports a clean verdict, but scan confidence is limited because full artifact inspection was unavailable to the scanner. <br>
Mitigation: Review the artifact SKILL.md and any scripts before installation, confirming permissions, data flows, and commands against the intended deployment. <br>
Risk: Incorrect optimization formulation, scaling, or dual sign conventions can produce misleading electricity price outputs. <br>
Mitigation: Validate balance-constraint formulation, baseMVA scaling, solver status, and sign convention against known test cases before relying on reported LMPs or reserve prices. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, markdown] <br>
**Output Format:** [Markdown with Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CVXPY-oriented extraction patterns and interpretation guidance for LMPs, reserve prices, binding lines, and counterfactual analysis.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
