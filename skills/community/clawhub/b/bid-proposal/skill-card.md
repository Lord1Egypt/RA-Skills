## Description:

Bid Proposal guides an agent through structured Chinese technical bid proposal drafting, from tender requirement analysis to outline recommendation, chapter drafting, and Word document output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elle-yu](https://clawhub.ai/user/elle-yu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, proposal writers, and delivery teams use this skill to draft security-service, product-delivery, compliance-assessment, and comprehensive cybersecurity bid technical proposals from tender requirements. It helps extract scoring criteria, recommend a chapter outline, generate Markdown proposal sections, maintain progress state, and prepare a Word document for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive tender and proposal materials.

Mitigation: Use explicit commands, provide only relevant tender files, and avoid sending unrelated .docx files into the chat.

Risk: Imported material-library content may contain confidential client names, pricing, internal costs, or unsuitable source material.

Mitigation: Review imported material before reuse and remove confidential or unauthorized content before it is incorporated into prompts or proposals.

Risk: Word-file processing and generated proposal output can introduce incorrect, misleading, or unintended content.

Mitigation: Run the skill in an isolated environment with pinned dependencies and review generated documents before delivery.

## Reference(s):

- [Bid Proposal Skill Page](https://clawhub.ai/elle-yu/skills/bid-proposal)
- [Scene Mapping](artifact/references/scene-mapping.json)
- [Chapter Templates](artifact/references/chapter-templates.md)
- [Material Library README](artifact/material-lib/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown dialogue, JSON state, and .docx document output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated bid content and reused material should be reviewed before delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
