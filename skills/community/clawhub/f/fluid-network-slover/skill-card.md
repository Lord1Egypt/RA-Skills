## Description: <br>
Solve and analyze steady incompressible fluid networks from TOML definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w1965857192yf-dotcom](https://clawhub.ai/user/w1965857192yf-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to define or validate TOML fluid-network models, run named operating or fault scenarios, and review pressure, flow, connectivity, and load reliability results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads TOML inputs and can write reports, JSON results, or generated templates to local paths. <br>
Mitigation: Review input and output paths before running the skill, and install it in a project-specific environment. <br>
Risk: Python dependencies are specified without exact pins. <br>
Mitigation: Pin or lock the Python dependencies before reproducible or production use. <br>
Risk: Network model files or generated reports may contain sensitive operational data. <br>
Mitigation: Avoid feeding sensitive data unless needed and handle generated outputs according to the project data policy. <br>


## Reference(s): <br>
- [TOML Schema Reference](references/toml_schema.md) <br>
- [Fluid Network Solver on ClawHub](https://clawhub.ai/w1965857192yf-dotcom/fluid-network-slover) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text analysis, JSON result payloads, Markdown reports, and TOML configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write report, JSON, or generated TOML files to user-specified local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
