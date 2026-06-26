## Description: <br>
Extracts structured data from aviation electronic ticket itineraries, including passenger name, identification number, flight number, route, departure and arrival times, fare, fuel surcharge, civil aviation fund, and electronic ticket number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to submit a local flight itinerary, ticket, or invoice file to Scnet OCR and receive structured recognition results for travel-document processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected itinerary, ticket, or invoice files are uploaded to Scnet's hosted OCR API. <br>
Mitigation: Use the skill only for documents approved for Scnet processing and confirm the exact local file path before running it. <br>
Risk: The skill requires a sensitive Scnet API key. <br>
Mitigation: Store the key in SCNET_API_KEY or the local config file with restricted permissions, and do not paste the key into chat. <br>
Risk: OCR output may contain personal or travel-document data extracted from the submitted file. <br>
Mitigation: Handle the returned JSON as sensitive workflow data and share it only with intended recipients or systems. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API Documentation](references/api-docs.md) <br>
- [OCR Field Summary](assets/templates/fields-summary.md) <br>
- [Scnet](https://www.scnet.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/flight-itinerary-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON recognition results on standard output, with human-readable error messages when configuration, file access, network, or API failures occur.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCNET_API_KEY; supports SCNET_API_BASE override; removes confidence fields from returned API results before printing.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
