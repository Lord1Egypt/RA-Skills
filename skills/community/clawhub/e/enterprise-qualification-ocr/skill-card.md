## Description: <br>
Extracts structured OCR data from images, PDFs, and archives containing business licenses or other enterprise qualification certificates by calling the Scnet OCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents use this skill when a user needs text or structured fields extracted from enterprise qualification documents such as business licenses, social organization registrations, trade union certificates, religious activity registrations, private non-enterprise registrations, institution legal-person certificates, or unified social credit code certificates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send sensitive local certificate, license, or business-document images to a third-party OCR API. <br>
Mitigation: Confirm each file upload with the user, avoid processing IDs, licenses, or certificates unless Scnet is approved for that data, and disclose that the document is sent to Scnet for OCR. <br>
Risk: The skill requires a Scnet API key and could expose credentials if the key is pasted into chat or stored with broad permissions. <br>
Mitigation: Store SCNET_API_KEY in a restricted environment or config file, keep config file permissions limited, and never paste the API key into conversation text. <br>
Risk: The OCR service can rate-limit requests and repeated calls may fail or duplicate document uploads. <br>
Mitigation: Run calls serially, respect the documented 10 QPS limit, and wait before retrying after 429 responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/enterprise-qualification-ocr) <br>
- [Publisher profile](https://clawhub.ai/user/scnet-sugon) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [Scnet OCR API docs](references/api-docs.md) <br>
- [OCR field summary](assets/templates/fields-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, guidance] <br>
**Output Format:** [JSON emitted to standard output, with friendly text errors for configuration, authentication, file, network, rate-limit, and API failures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an SCNET_API_KEY and uploads the target document to the Scnet OCR API; successful responses return the API data array with document-specific elements.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter, skill.yaml, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
