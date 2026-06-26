## Description: <br>
Verifies identity documents via the Didit standalone API for passports, ID cards, driver's licenses, and residence permits, including OCR extraction, MRZ parsing, authenticity checks, and KYC document validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosasalberto](https://clawhub.ai/user/rosasalberto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and identity-verification teams use this skill to submit user-provided identity document images to Didit and interpret verification status, extracted document fields, and warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected identity document images to Didit for verification. <br>
Mitigation: Use it only when authorized to process the document holder's ID images and when the user understands the data will be sent to Didit. <br>
Risk: The Didit API key is required for requests. <br>
Mitigation: Store DIDIT_API_KEY as a secret environment variable and avoid placing it in source files, command history, logs, or shared transcripts. <br>
Risk: Returned JSON can include highly sensitive identity data such as document numbers, birth dates, addresses, portraits, and document images. <br>
Mitigation: Protect the response as sensitive personal data, minimize retention, avoid unnecessary vendor_data, and use --no-save when provider-side saving is not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rosasalberto/didit-id-document-verification) <br>
- [Didit Documentation](https://docs.didit.me) <br>
- [Didit ID Verification API Reference](https://docs.didit.me/standalone-apis/id-verification) <br>
- [Didit ID Verification Feature Guide](https://docs.didit.me/core-technology/id-verification/overview) <br>
- [Didit Supported Documents](https://docs.didit.me/core-technology/id-verification/supported-documents-id-verification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, code examples, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIDIT_API_KEY and a front document image; may use an optional back image, vendor_data, and --no-save.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
