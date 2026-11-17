## Description:

Use this skill when the user provides AF2, ESMFold, AF3, Boltz-1, SASA, or MD results and needs a Gate 1-4 audit with a Go/Hold/Kill decision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barrett-cryptodna](https://clawhub.ai/user/barrett-cryptodna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and domain reviewers use this skill to audit computational vaccine-design evidence across structure, epitope exposure, molecular dynamics, manufacturability, and readiness for more expensive computation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports Go/Hold/Kill decisions for computational vaccine-design audits, which can be consequential if treated as definitive.

Mitigation: Use outputs as decision support and require domain expert review before scientific or engineering action.

Risk: The skill is a Chinese-language checklist focused on a narrow Gate 1-4 computational audit workflow.

Mitigation: Install only when users are comfortable reviewing Chinese-language audit guidance and can provide the expected structural prediction, exposure, MD, checkpoint, log, or trajectory-summary evidence.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown audit report with Gate 1-4 findings and a Go/Hold/Kill decision]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided structural prediction, SASA, MD, checkpoint, log, or trajectory-summary evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
