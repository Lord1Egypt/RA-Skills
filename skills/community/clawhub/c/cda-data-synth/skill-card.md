## Description: <br>
CDA Data Synth generates CDA-compatible synthetic causal datasets from domain descriptions, including Entity-State Graph JSON, causal edges, timestamped trajectories, Hamiltonian parameters, and metadata for thermodynamics, mechanics, fluid, and coupled physical domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn physical-domain scenario descriptions into CDA-ready synthetic causal datasets for training, validation, and benchmark generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated physics data may be incorrect or unsuitable for production or safety-critical use. <br>
Mitigation: Independently verify generated datasets, physical assumptions, and constraints before using the outputs for production, safety-critical systems, or model evaluation. <br>
Risk: Writing generated JSON into an existing directory may overwrite important files. <br>
Mitigation: Choose output directories deliberately and review proposed filenames before writing or replacing files. <br>


## Reference(s): <br>
- [CDA Data Format Specification](references/data-format-spec.md) <br>
- [CDA Synthesis Protocols](references/synthesis-protocols.md) <br>
- [Thermal Building Example](references/thermal-building-example.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Guidance] <br>
**Output Format:** [CDA JSON files with concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected file families include graph, trajectory, hamiltonian, and metadata JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
