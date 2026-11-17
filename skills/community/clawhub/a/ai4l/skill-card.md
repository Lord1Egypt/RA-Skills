## Description:

AI4L helps agents create, audit, compare, and revise evidence-based Markdown reviews of health and longevity interventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epicoun](https://clawhub.ai/user/epicoun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate structured evidence reviews and QA audits for health and longevity interventions. It supports review creation, independent auditing, iterative fixes, and comparison of Markdown evidence-review files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated medical or longevity conclusions may be incomplete, incorrect, or unsuitable for an individual reader.

Mitigation: Review outputs before relying on them and treat the generated reviews as decision-support material rather than medical advice.

Risk: Private notes or sensitive content placed in ./results/ audit files may be copied into later audits.

Mitigation: Do not store secrets or private notes in ./results/ files, and inspect audit issue sections before running iterative workflows.

Risk: Explicit fix workflows can modify generated evidence-review Markdown files.

Mitigation: Confirm the target file before invoking fix or iterate commands and review the resulting file changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/epicoun/skills/ai4l)
- [Forever Healthy Foundation](https://forever-healthy.org)
- [AI4L quality assurance guideline](artifact/AI4L.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance, Code, Shell commands]

**Output Format:** [Markdown files and concise status messages, with occasional shell commands or small scripts for audit counting.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated evidence reviews and QA audits are written under ./results/; fix workflows may revise evidence-review Markdown files when explicitly invoked.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
