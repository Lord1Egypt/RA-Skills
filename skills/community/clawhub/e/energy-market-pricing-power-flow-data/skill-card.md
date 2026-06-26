## Description: <br>
Power system network data formats and topology. Use when parsing bus, generator, and branch data for power flow analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power systems engineers use this skill for guidance on loading, interpreting, and mapping MATPOWER-style network JSON data for power flow analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large power-flow JSON files can consume significant memory when loaded at once. <br>
Mitigation: Check file size before loading and use an environment with sufficient memory; consider streaming or preprocessing for unusually large datasets. <br>
Risk: Untrusted or malformed network JSON can lead to incorrect analysis or failed parsing. <br>
Mitigation: Use trusted datasets and validate required MATPOWER-style fields before relying on parsed bus, generator, branch, or reserve values. <br>


## Reference(s): <br>
- [PGLib-OPF benchmark library](https://github.com/power-grid-lib/pglib-opf) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no network, credential, persistence, or hidden execution behavior found in server security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
