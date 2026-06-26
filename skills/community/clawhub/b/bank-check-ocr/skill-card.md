## Description: <br>
Extracts structured data from bank check images, including check number, issue date, written and numeric amounts, and issuer signature or seal details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scnet-sugon](https://clawhub.ai/user/scnet-sugon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send local bank check images or PDFs to the Scnet OCR API and receive structured JSON fields for downstream review, extraction, or workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank check images may contain account numbers, names, amounts, signatures, and seals that are uploaded to Scnet's remote OCR API. <br>
Mitigation: Use only files you are authorized to process, verify Scnet's privacy and retention terms before deployment, and require explicit confirmation before each upload. <br>
Risk: The skill requires a sensitive SCNET_API_KEY credential. <br>
Mitigation: Store the key in an environment variable or a local config file with restrictive permissions, keep it out of chat, and rotate it if exposed. <br>
Risk: The OCR API has rate limits and repeated requests may fail or be throttled. <br>
Mitigation: Run calls sequentially and rely on the built-in retry and backoff behavior for 429 responses. <br>


## Reference(s): <br>
- [Sugon-Scnet OCR API docs](references/api-docs.md) <br>
- [Bank check field summary](assets/templates/fields-summary.md) <br>
- [Scnet website](https://www.scnet.cn) <br>
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/bank-check-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [JSON emitted to standard output, with setup and troubleshooting guidance in Markdown documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recognized data is returned from the API data field; the script removes top-level per-item confidence values before printing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.yaml, changelog, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
