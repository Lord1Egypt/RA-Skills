## Description:

Bidding Compliance Advisor helps bidders compare tender requirements against bid-package materials and produce structured checklists for disqualification risks, qualification documents, formatting, deadlines, and related tender-law review boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External bidders and compliance reviewers use this skill before submission to identify missing signatures, seals, guarantees, qualification proof, format issues, deadline risks, and scoped tender-law review questions. It supports checklist preparation and risk triage, but does not replace formal legal or compliance review.

### Deployment Geography for Use:

China (Chinese tendering and bidding law contexts)

## Known Risks and Mitigations:

Risk: Bidding materials can contain confidential pricing, credentials, CA passwords, or other sensitive commercial information.

Mitigation: Install and use the skill only in an approved environment for confidential bidding materials, and avoid sharing raw credentials or sensitive pricing unless the workspace is approved for that data.

Risk: Tender-law guidance can become outdated or be misapplied to high-stakes decisions.

Mitigation: Treat outputs as checklist support, verify current law and official sources, and obtain professional review for major legal or compliance decisions.

Risk: The skill excludes government-procurement goods and services workflows and may be inappropriate if the procurement regime is misidentified.

Mitigation: Confirm the applicable procurement regime before use and route government-procurement matters to an appropriate workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bidding-compliance-advisor-1-3-1)
- [Compliance signals](references/compliance-signals.md)
- [Legal core](references/legal_core.md)
- [FAQ](references/faq.md)
- [Few-shot calibration](references/few_shot.md)
- [Checklist template](templates/checklist-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown checklist tables with risk labels and deadline workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured bidder-facing checklists with scoped legal-reference guidance and current-law verification reminders.]

## Skill Version(s):

1.3.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
