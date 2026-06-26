## Description: <br>
Predict ADME (Absorption, Distribution, Metabolism, Excretion) properties for drug candidates using cheminformatics models and molecular descriptors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renhaosu2024](https://clawhub.ai/user/renhaosu2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cheminformatics practitioners, and drug discovery teams use this skill to estimate small-molecule ADME properties, drug-likeness, and candidate prioritization signals before experimental validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ADME predictions are computational screening estimates and may be unsuitable for clinical, regulatory, or other high-stakes drug-development decisions. <br>
Mitigation: Treat outputs as preliminary prioritization signals and require independent in vitro, in vivo, or other appropriate experimental validation before decision making. <br>
Risk: Scientific results may vary across environments because dependencies are not pinned to exact versions. <br>
Mitigation: Install in a controlled Python environment and pin dependency versions for reproducible work. <br>
Risk: Predictions may be unreliable for molecules outside the documented applicability domain, invalid SMILES, biologics, salts, or unusual chemotypes. <br>
Mitigation: Validate input structures, remove salts where appropriate, check applicability-domain warnings, and restrict use to suitable small molecules. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON or table-formatted ADME prediction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write JSON result files for single-compound or batch predictions when an output path is provided.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
