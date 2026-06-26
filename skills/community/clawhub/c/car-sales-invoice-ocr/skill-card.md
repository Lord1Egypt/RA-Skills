## Description: <br>
Extracts structured fields from motor vehicle sales invoice images or PDFs using Scnet's OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to extract invoice numbers, buyer and seller details, VIN, engine number, vehicle model, tax, amount, and related fields from motor vehicle sales invoices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle invoice images or PDFs can contain personal, vehicle, seller, buyer, tax, and payment data that is sent to Scnet's OCR service. <br>
Mitigation: Use the skill only for files you are authorized to share with Scnet, and avoid submitting invoices containing data you are not allowed to disclose. <br>
Risk: The skill requires an API key and allows the API base URL to be configured. <br>
Mitigation: Keep SCNET_API_KEY in config/.env with restricted permissions and verify SCNET_API_BASE before use. <br>
Risk: Parallel or high-volume requests can trigger the OCR service rate limit. <br>
Mitigation: Call the skill serially for batches and retry after waiting when 429 rate-limit responses occur. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API documentation summary](references/api-docs.md) <br>
- [Vehicle sales invoice field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/car-sales-invoice-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [Pretty-printed JSON on stdout for successful OCR results; human-readable text for errors and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY; sends the selected invoice file to Scnet's OCR service and returns the API data payload with confidence values removed by the wrapper script.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, skill.yaml, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
