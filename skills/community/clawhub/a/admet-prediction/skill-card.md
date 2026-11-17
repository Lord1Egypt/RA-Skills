## Description:

ADMET prediction for drug candidates, including drug-likeness, pharmacokinetic properties, and early toxicity screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huifer](https://clawhub.ai/user/huifer)

### License/Terms of Use:


## Use Case:

Drug discovery users can use this skill to estimate ADMET properties from SMILES strings or compound libraries and prioritize candidates for follow-up review. Results are appropriate for early screening and should be validated by domain experts before scientific, clinical, regulatory, or safety decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simplified ADMET and toxicity estimates could be mistaken for validated scientific predictions.

Mitigation: Treat outputs as early screening signals only and require expert review plus experimental validation before acting on hERG, DILI, Ames, or drug-likeness results.

Risk: The bundled script depends on chemistry packages and optional model packages.

Mitigation: Install the skill in an isolated environment with pinned, reviewed dependencies.

## Reference(s):

- [ADMET Properties Reference](reference/admet-properties.md)
- [Toxicity Alerts Reference](reference/toxicity-alerts.md)
- [ClawHub Skill Page](https://clawhub.ai/huifer/skills/admet-prediction)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown summaries, JSON result files, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize individual compounds, batch prediction results, or drug-likeness filter outcomes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
