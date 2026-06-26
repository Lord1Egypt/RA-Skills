## Description: <br>
Generates or completes 8D reports from customer complaint data, with D1-D8 fill-in guidance, a standard template, and support for customer-specific formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lams001](https://clawhub.ai/user/lams001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Quality, manufacturing, supplier quality, and customer response teams use this skill to draft or complete 8D/CAR reports for customer complaints, quality deviations, root cause analysis, containment, corrective action, and recurrence prevention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated 8D reports may contain incomplete or incorrect complaint details if source evidence is missing or inaccurate. <br>
Mitigation: Review each report before external use and replace placeholders with verified complaint, product, lot, customer, root cause, corrective action, and closure evidence. <br>
Risk: Complaint evidence, customer templates, photos, videos, procedures, and internal quality records may be sensitive. <br>
Mitigation: Provide only information your organization permits in the current OpenClaw session and attach or distribute final evidence through approved systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lams001/complaint-8d-report) <br>
- [8D methodology reference](artifact/reference.md) <br>
- [Customer-specific format definitions](artifact/formats/README.md) <br>
- [Automotive OEM example format](artifact/formats/automotive-oem-example.md) <br>
- [Sample 8D snippets](artifact/examples/sample-8d-snippet.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report drafts with tables, placeholders, prompts, and optional text or Mermaid-style diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit placeholders for missing data and attachment reminders for photos, videos, charts, procedures, and customer closure evidence.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact/clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
