## Description: <br>
Veryfi Documents AI helps agents use Veryfi's OCR and document extraction APIs for receipts, invoices, bank statements, checks, tax forms, document classification, fraud signals, and raw OCR text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbirulia](https://clawhub.ai/user/dbirulia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and AI-agent builders use this skill to send authorized documents to Veryfi for OCR, structured data extraction, document classification, fraud indicators, and raw OCR text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded documents leave the user's environment and may contain sensitive personal, financial, medical, tax, or identity data. <br>
Mitigation: Process only documents approved for third-party handling, test with sample documents first, and review Veryfi privacy, retention, and compliance terms before sending sensitive files. <br>
Risk: Veryfi API credentials are required and could be exposed if stored directly in local configuration or committed files. <br>
Mitigation: Use environment variables or a secret store, avoid committing credentials, restrict local config permissions, and rotate keys when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dbirulia/documents-ai) <br>
- [Veryfi API documentation](https://docs.veryfi.com/) <br>
- [Veryfi API credentials](https://app.veryfi.com/api/settings/keys/) <br>
- [Veryfi website](https://veryfi.com) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, text, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with curl commands and Veryfi JSON API responses, including plain-text ocr_text fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VERYFI_CLIENT_ID, VERYFI_USERNAME, and VERYFI_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
