## Description:

Calls the Scnet online OCR service to identify commercial invoices and extract invoice numbers, dates, amounts, issuer details, letter-of-credit details, contract numbers, and trade terms from uploaded local images or PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to submit local commercial invoice images or PDFs to Scnet cloud OCR and receive structured invoice fields for downstream review or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commercial invoices can contain sensitive business information and the skill uploads selected files to Scnet cloud OCR.

Mitigation: Confirm each document is authorized to leave the local environment before use and avoid submitting files that policy, contract, or regulation prohibits sharing.

Risk: A configurable API base URL could redirect invoice files and the Scnet API token away from the intended Scnet endpoint.

Mitigation: Keep SCNET_API_BASE set to the official Scnet HTTPS endpoint and review any change to that value before running the skill.

Risk: The Scnet API key can be exposed if pasted into chats, committed, or stored in an overly permissive config file.

Mitigation: Store credentials in a private environment variable or config/.env file with restrictive permissions, and do not paste API keys into conversation logs.

Risk: Rapid repeated OCR calls can hit the documented Scnet rate limit.

Mitigation: Run requests serially where practical and honor retry or backoff behavior after 429 responses.

## Reference(s):

- [Sugon-Scnet OCR API documentation](references/api-docs.md)
- [Commercial invoice field summary](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/commercial-invoice-ocr)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [Structured JSON printed to standard output, with human-readable text for errors and setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script removes confidence fields before printing OCR results and sends selected files to Scnet cloud OCR.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
