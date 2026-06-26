## Description: <br>
Recognizes online education certificate verification reports and extracts structured fields such as name, update date, enrollment date, ID number, institution, education category, and major. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to submit education certificate electronic registration report images or PDFs to SCNet OCR and receive structured JSON for filing, review, or downstream document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Education document images or PDFs are sent to SCNet's OCR API for processing. <br>
Mitigation: Upload only documents the user is authorized to process, and verify SCNet privacy, retention, residency, and contractual terms before regulated or high-sensitivity use. <br>
Risk: The skill requires an SCNET_API_KEY credential. <br>
Mitigation: Store the key in an environment variable or protected config/.env file, and do not paste it into chat or commit it to source control. <br>
Risk: The OCR API has a documented 10 QPS limit and may return 429 responses when called too quickly. <br>
Mitigation: Call the skill serially or throttle requests; the script backs off and retries up to three times for 429 responses. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API documentation](references/api-docs.md) <br>
- [Recognized field summary](assets/templates/fields-summary.md) <br>
- [SCNet website](https://www.scnet.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON on standard output, with human-readable error text on failure.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ocrType value and a local file path; the script prints the returned data array after removing top-level confidence fields from each result item.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.yaml, CHANGELOG released 2025-05-29, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
