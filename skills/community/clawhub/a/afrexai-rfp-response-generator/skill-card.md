## Description:

Generates structured, compliant RFP, RFI, and RFQ response packages by extracting requirements, mapping company capabilities, flagging gaps, and drafting proposal sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afrexai-cto](https://clawhub.ai/user/afrexai-cto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, proposal teams, sales teams, and consultants use this skill to turn solicitation documents and company profiles into first-draft proposal packages with compliance mapping, response sections, and review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposal work may include confidential company or customer information.

Mitigation: Use only documents the user is authorized to process and review generated proposal content before sharing it.

Risk: Generated proposal claims or past-performance details may be unsupported if source materials are incomplete.

Mitigation: Verify all claims against provided company evidence and leave placeholders for missing project details instead of fabricating them.

Risk: The artifact references an unbundled SOUL.md style file that could influence narrative text if resolved at runtime.

Mitigation: Inspect and trust any external SOUL.md file before applying it, or ignore that reference when generating proposal sections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afrexai-cto/skills/afrexai-rfp-response-generator)
- [AfrexAI](https://afrexai.com)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown files with structured proposal sections, compliance tables, and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a compliance matrix, executive summary, technical response, management response, past-performance narratives, and final review checklist.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
