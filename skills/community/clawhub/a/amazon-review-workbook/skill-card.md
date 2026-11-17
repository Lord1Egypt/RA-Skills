## Description:

Collect all customer reviews from an Amazon product URL or product-reviews URL through a logged-in Chrome session on port 9222, export a 14-column factual workbook, optionally fill translations through DeepLX, and then help the model tag the rows into a final delivery-ready spreadsheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aduo6668](https://clawhub.ai/user/aduo6668)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect Amazon review data, translate or label review rows, and produce a stable 14-column workbook for review analysis or delivery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in Chrome session through the local debugging port.

Mitigation: Use a separate temporary Chrome profile, keep remote debugging bound to localhost, and verify the target URL is a real Amazon domain before running collection commands.

Risk: Review text and an optional DeepLX key may be sent to a configured translation endpoint.

Mitigation: Review and trust the DeepLX endpoint before enabling translation, and leave translation disabled for sensitive datasets unless the destination is approved.

## Reference(s):

- [Skill page](https://clawhub.ai/aduo6668/skills/amazon-review-workbook)
- [Setup](references/setup.md)
- [Output Schema](references/output-schema.md)
- [Tagging Guidelines](references/tagging-guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON labeling payloads, and generated XLSX/CSV workbook files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces fixed 14-column factual and final review workbooks; optional DeepLX translation can fill Chinese review text before model labeling.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
