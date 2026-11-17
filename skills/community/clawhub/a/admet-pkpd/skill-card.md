## Description:

ADMET and pharmacokinetic/pharmacodynamic property prediction workflows using ADMET Predictor, AOMP, OBA, Graph-pKa, DeepEsol, and Molecular Descriptors through SciMiner.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sciminer](https://clawhub.ai/user/sciminer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational chemistry users use this skill to select and run SciMiner ADMET, PK/PD, metabolism, pKa, solvation, and molecular descriptor workflows for small-molecule assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a SciMiner API key and may upload molecule data or user-provided files to SciMiner.

Mitigation: Use a dedicated, revocable API key and avoid proprietary molecule data or files unless the upload is approved.

Risk: Live remote Markdown documentation determines request parameters and executable API behavior.

Mitigation: Verify the selected SciMiner documentation URL, request destination, parameters, and upload behavior before allowing generated code to run.

Risk: Generated prediction results may affect chemistry or drug-discovery decisions.

Mitigation: Treat outputs as computational predictions and review them with qualified domain experts before downstream use.

## Reference(s):

- [ADMET PK/PD Predict ClawHub page](https://clawhub.ai/sciminer/skills/admet-pkpd)
- [SciMiner tool API Markdown documentation](https://sciminer.tech/tool_api_files/)
- [SciMiner API key utility](https://sciminer.tech/utility)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON snippets, inline code, and SciMiner share URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs and share URLs for SciMiner prediction results.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
