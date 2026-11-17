## Description:

End-to-end guide for running MM/GBSA binding free energy calculations using AmberTools/Amber on a pre-existing receptor-ligand complex without molecular dynamics sampling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ning-kun](https://clawhub.ai/user/ning-kun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational chemists, and structural biology users use this skill to prepare receptor-ligand systems and run single-structure Amber MM/GBSA calculations for rapid pose scoring and mechanistic energy decomposition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local AmberTools commands create project files, logs, topologies, coordinates, and trajectory files based on user-supplied molecular inputs.

Mitigation: Review commands before execution and verify receptor structure, ligand charge, generated parameters, and log output before relying on results.

Risk: Single-structure MM/GBSA estimates can be misleading when used as quantitative affinities or for ranking ligands, especially when electrostatic terms are large and cancel.

Mitigation: Treat results as directional estimates unless validated, and use MD ensemble sampling with appropriate uncertainty analysis for comparative ranking or publication-grade claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ning-kun/skills/amber-mmgbsa)
- [Publisher profile](https://clawhub.ai/user/ning-kun)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, Python, text, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow instructions and interpretation guidance; it does not execute AmberTools commands by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
