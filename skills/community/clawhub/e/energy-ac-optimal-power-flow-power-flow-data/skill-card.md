## Description: <br>
Power system network data formats and topology. Use when parsing bus, generator, and branch data for power flow analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power-system engineers use this skill to interpret MATPOWER-style network JSON, map buses, generators, and branches, and compute basic power-flow data summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Very large network JSON files may consume significant memory when loaded fully. <br>
Mitigation: Use the skill's recommended quick size checks and only load network JSON files that are intended for analysis. <br>


## Reference(s): <br>
- [PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf) <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/energy-ac-optimal-power-flow-power-flow-data) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance focuses on local JSON parsing and topology interpretation; very large network files may require significant memory when loaded fully.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
