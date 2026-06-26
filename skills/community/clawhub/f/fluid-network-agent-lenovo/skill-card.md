## Description: <br>
Reads steady-state incompressible fluid-network TOML files, solves node pressures and pipe flows, and reports scenario connectivity and load reliability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zebra6-web](https://clawhub.ai/user/Zebra6-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Engineers and developers use this skill to turn fluid-network TOML models into scenario reports comparing pressures, flows, connectivity, and PASS/FAIL reliability for loads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python code on TOML files supplied by the user. <br>
Mitigation: Use intended engineering inputs and review TOML content before execution. <br>
Risk: Report output can be written to a user-selected path. <br>
Mitigation: Choose output paths carefully to avoid overwriting files. <br>
Risk: Fluid-network calculations may be incomplete or unsuitable for real-world engineering decisions without review. <br>
Mitigation: Independently validate results before relying on them for physical fluid-system design or operation. <br>


## Reference(s): <br>
- [ClawHub release: Fluid Network Agent](https://clawhub.ai/Zebra6-web/fluid-network-agent-lenovo) <br>
- [TOML Schema](artifact/reference.md) <br>
- [Examples](artifact/examples.md) <br>
- [Example Network TOML](artifact/examples/example_network.toml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON scenario report with TOML configuration guidance and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include scenario connectivity, edge flow and pressure results, optional velocity, and load/function PASS/FAIL status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
