## Description:

Generates or completes 8D reports from customer complaint data, with D1-D8 fill-in guidance, a standard template, and customer-specific format support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lams001](https://clawhub.ai/user/lams001)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, manufacturing, supplier quality, and customer-facing teams use this skill to draft or complete 8D/CAR reports for customer complaints, quality deviations, and recurrence prevention. It helps structure D1-D8 sections, custom customer layouts, root-cause analysis prompts, attachment placeholders, and Markdown output for downstream report systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad quality-report triggers may activate the skill during general quality discussions.

Mitigation: Confirm that the user wants an 8D or CAR report before drafting a full report.

Risk: Drafted report content can be incomplete or misleading because it relies on user-provided facts and placeholders.

Mitigation: Review all report sections, evidence references, and placeholders before sharing the report with customers or uploading it to a formal system.

Risk: Attachment placeholders do not include the actual images, videos, specifications, procedures, or approvals required for a complete quality record.

Mitigation: Attach the referenced files in Word or the final report system and verify document numbers, revisions, dates, and approvals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lams001/skills/complaint-8d-report)
- [8D methodology reference](artifact/reference.md)
- [Customer-specific format definitions](artifact/formats/README.md)
- [Automotive OEM example format](artifact/formats/automotive-oem-example.md)
- [8D report example snippet](artifact/examples/sample-8d-snippet.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report skeletons, tables, prompts, text or Mermaid-style diagrams, and attachment placeholders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses placeholders for missing facts and reminds users to attach images, videos, and documents in the final report system.]

## Skill Version(s):

1.1.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
