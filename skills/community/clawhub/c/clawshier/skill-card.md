## Description:

Processes receipt or invoice images into structured expenses and logs them to Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdocr](https://clawhub.ai/user/fdocr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Clawshier to scan receipt or invoice images, extract expense details, validate duplicates, and record the results in Google Sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically delete the default Sheet1 tab in the target spreadsheet.

Mitigation: Install it only with a dedicated empty spreadsheet and back up any spreadsheet before first use.

Risk: Receipt images and extracted text are sent to OpenAI by default unless local OCR is forced.

Mitigation: Use CLAWSHIER_VISION_PROVIDER=ollama for local-only OCR when receipts contain sensitive data.

Risk: Receipt text may be written to Sheets in a way spreadsheet software can treat as formulas.

Mitigation: Avoid processing receipts from untrusted sources until formula neutralization or RAW sheet writes are added.

## Reference(s):

- [Clawshier on ClawHub](https://clawhub.ai/fdocr/skills/clawshier)
- [Google Cloud Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
- [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown replies with inline shell commands and JSON-backed pipeline outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs OCR, structuring, validation, deduplication, and Google Sheets storage; optional trace summaries are returned only when requested.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
