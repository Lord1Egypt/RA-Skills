## Description:

Generate a chart image using Chart.js. Supports line, bar, pie, doughnut, radar, polarArea, bubble, and scatter chart types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabhdugar](https://clawhub.ai/user/rishabhdugar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to generate Chart.js chart images for reports, dashboards, emails, chatbots, and other programmatic workflows without browser or frontend rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart configuration data is sent to PDFAPIHub.

Mitigation: Avoid sending confidential business, financial, or personal data unless PDFAPIHub's retention and privacy terms fit the use case.

Risk: The skill requires a PDFAPIHub API key.

Mitigation: Treat the API key as sensitive, provide it only through the required CLIENT-API-KEY header, and keep it out of shared logs or artifacts.

## Reference(s):

- [PDFAPIHub Documentation](https://pdfapihub.com/docs)
- [PDFAPIHub Generate Chart API](https://pdfapihub.com/api/v1/generateChart)
- [ClawHub Skill Page](https://clawhub.ai/rishabhdugar/skills/generate-chart)

## Skill Output:

**Output Type(s):** [Images, URLs, JSON]

**Output Format:** [Chart image URL, base64 payload, binary image, or JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports url, base64, both, and image output formats.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
