## Description: <br>
Generate a chart image using Chart.js. Supports line, bar, pie, doughnut, radar, polarArea, bubble, and scatter chart types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate Chart.js-based chart images for reports, dashboards, emails, and chatbot workflows through the PDFAPIHub API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a reusable PDFAPIHub API key. <br>
Mitigation: Keep CLIENT-API-KEY secret, avoid logging it in commands or examples, and rotate it if exposure is suspected. <br>
Risk: Chart data is sent to pdfapihub.com and generated chart outputs may contain sensitive business or financial information. <br>
Mitigation: Use only chart data you are comfortable sending to PDFAPIHub, and avoid personal, regulated, confidential, or sensitive financial or business data unless the provider's privacy and retention terms have been reviewed and accepted. <br>


## Reference(s): <br>
- [PDFAPIHub documentation](https://pdfapihub.com/docs) <br>
- [PDFAPIHub chart generation endpoint](https://pdfapihub.com/api/v1/generateChart) <br>
- [ClawHub release page](https://clawhub.ai/rishabhdugar/generate-chart) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, image, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API request and response guidance, with chart output returned as a URL, base64 data, both, or an image.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLIENT-API-KEY header and accepts Chart.js data, options, chart dimensions, and output_format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
