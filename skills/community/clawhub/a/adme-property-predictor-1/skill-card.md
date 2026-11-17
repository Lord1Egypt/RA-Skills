## Description:

Predicts small-molecule ADME properties and drug-likeness from SMILES or CSV inputs using a reproducible RDKit-based workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and scientists use this skill to screen small-molecule drug candidates for predicted absorption, distribution, metabolism, excretion, and drug-likeness properties before prioritizing follow-up review or experiments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned dependencies can change runtime behavior or supply-chain exposure.

Mitigation: Install in an isolated environment and pin or review RDKit before use; remove the unnecessary dataclasses dependency for Python 3.10+.

Risk: Untrusted molecule inputs or CSV files may produce unreliable runs or expose local file handling issues.

Mitigation: Provide only trusted CSV files or molecule SMILES, and validate inputs before execution.

Risk: The script can overwrite files at the selected output path.

Mitigation: Use explicit output paths and check for existing files before writing results.

Risk: The --properties option should not be relied on to limit calculation scope.

Mitigation: Assume the current implementation may calculate the full ADME result set until the option behavior is fixed and verified.

Risk: Predicted ADME values can be mistaken for experimental or clinical evidence.

Mitigation: Treat outputs as screening estimates for prioritization and require experimental validation before scientific, clinical, or regulatory decisions.

## Reference(s):

- [Runtime Checklist](references/runtime_checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/adme-property-predictor-1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; execution can produce JSON, CSV, or table-formatted ADME reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces screening estimates for small molecules and may write results to a user-specified output file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
