## Description:

Build digital twin patient models to test drug efficacy and toxicity in virtual environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and clinical simulation teams use this skill to model patient-specific genotype, clinical, and imaging data for virtual drug efficacy, toxicity, and dose optimization analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive patient and genomic data.

Mitigation: Use only synthetic or properly de-identified data unless operating in a controlled environment with permission to process patient information.

Risk: Dose recommendations and medical simulation outputs are unvalidated.

Mitigation: Treat all efficacy, toxicity, and dosing outputs as research output that requires qualified medical review before any clinical use.

Risk: The skill writes simulation results and accepts user-supplied input and output paths.

Mitigation: Restrict input and output paths to the workspace and review outputs before sharing.

Risk: Network/API behavior is not adequately documented by the publisher.

Mitigation: Do not enable or assume network/API use until the publisher documents what data leaves the machine.

Risk: Dependency behavior may change across installs.

Mitigation: Pin and review dependencies before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/aipoch-ai/skills/digital-twin-patient-builder)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [JSON simulation results with console text and Python API objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dose-level efficacy, toxicity risk, optimal dose, PK metrics, and concentration profile data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
