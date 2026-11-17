## Description:

Official-style Amber24 molecular dynamics workflow guide for proteins, including a standard end-to-end procedure, command templates, input-file templates, and a manual worked example from PDB download through RMSD/RMSF analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ning-kun](https://clawhub.ai/user/ning-kun)

### License/Terms of Use:

MIT-0

## Use Case:

Scientists, educators, and technical users use this skill to plan and manually run reproducible Amber protein molecular dynamics workflows, from structure preparation through trajectory analysis. It provides workflow guidance, command templates, and quality checks rather than executable automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amber simulations can consume substantial compute or GPU time and create local output files.

Mitigation: Review commands before execution, validate with the documented 1 ns workflow first, and run in an appropriate project directory with expected storage and compute capacity.

Risk: Scientific results can be misleading if input structures, ligands, atom masks, or imaging choices are inappropriate.

Mitigation: Follow the documented quality checks, remove or parameterize unsupported ligands, use consistent atom masks, and apply trajectory imaging correction before interpreting RMSD or RMSF.

## Reference(s):

- [Amber Parameter Guide](references/amber_parameter_guide.md)
- [cpptraj Analysis Guide](references/cpptraj_analysis_guide.md)
- [1AKI PDB Download](https://files.rcsb.org/download/1AKI.pdb)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and Amber input-file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; users review and run commands manually in their Amber environment.]

## Skill Version(s):

1.0.4 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
