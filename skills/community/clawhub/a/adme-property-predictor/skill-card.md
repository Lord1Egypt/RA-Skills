## Description:

Predict ADME (Absorption, Distribution, Metabolism, Excretion) properties for drug candidates using cheminformatics models and molecular descriptors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renhaosu2024](https://clawhub.ai/user/renhaosu2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational chemists, and drug discovery teams use this skill to estimate small-molecule ADME properties, drug-likeness, and prioritization signals before experimental validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned dependencies can change across installs and may introduce supply-chain or reproducibility risk.

Mitigation: Install in an isolated environment and pin dependencies with hashes from trusted package sources before operational use.

Risk: The shipped script uses heuristic descriptor rules while the skill text describes more mature model behavior.

Mitigation: Present outputs as rough prioritization signals and require expert review plus experimental validation before research, regulatory, or clinical decisions.

Risk: ADME predictions can be unreliable for invalid structures, biologics, unusual chemotypes, salt forms, or molecules outside the model domain.

Mitigation: Validate and standardize SMILES inputs, remove salts when appropriate, check applicability domain, and route unsupported molecule classes to specialized workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renhaosu2024/skills/adme-property-predictor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; the bundled script emits JSON or plain-text table reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local prediction reports intended as prioritization signals, not validated pharmacokinetic evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
