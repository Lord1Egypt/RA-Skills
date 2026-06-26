## Description: <br>
AC branch pi-model power flow equations (P/Q and |S|) with transformer tap ratio and phase shift, matching `acopf-math-model.md` and MATPOWER branch fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power-systems engineers use this skill to compute MATPOWER-compatible AC branch pi-model flows in both directions, aggregate bus injections for nodal balance, check MVA limits, and debug sign or unit issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect or unintended datasets can produce misleading AC power-flow results. <br>
Mitigation: Use only datasets intended for local processing and replace the sample `/root/network.json` path with the correct input path. <br>
Risk: The helper requires numpy and aligned MATPOWER-style bus and branch arrays. <br>
Mitigation: Confirm numpy is installed and validate bus indexing, baseMVA, voltage magnitudes, and voltage angles before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/wu-uk/energy-ac-optimal-power-flow-ac-branch-pi-model) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown guidance with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local per-unit branch-flow calculations and MVA loading values from MATPOWER-style branch and bus arrays.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
