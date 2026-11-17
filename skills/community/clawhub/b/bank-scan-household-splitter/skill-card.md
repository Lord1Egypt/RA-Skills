## Description:

Guides agents in sorting scanned identity cards and bank applications by person and producing a separate Word document for each household, with uncertain matches set aside for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Banking and legal operations staff use this skill to extract scanned documents, identify and group each person's identity-card images and application forms, and prepare individual Word files while separating uncertain matches for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full identity and application images are sent to an external vision API, potentially exposing sensitive client information without clear consent.

Mitigation: Obtain explicit approval before processing regulated or confidential material; confirm uploads, redact where possible, prefer local-only processing, and mask logs.

Risk: Document recognition or ambiguous matching can place an identity-card image in the wrong person's file.

Mitigation: Cross-check names and document matches, keep uncertain images separate, and manually verify completed files before delivery.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lingyu9495-source/skills/bank-scan-household-splitter)
- [Vision model selection notes](artifact/references/vision-model-selection.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Files]

**Output Format:** [Markdown instructions, per-person DOCX files, and optional JSON classification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unmatched or unreadable images are held for manual review; usage and cost estimates can be reported.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
