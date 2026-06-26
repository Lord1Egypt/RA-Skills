## Description: <br>
Clawshier processes receipt or invoice images into structured expenses and logs them to Google Sheets, using OpenAI OCR by default with optional local Ollama OCR. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fdocr](https://clawhub.ai/user/fdocr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Clawshier to scan receipt or invoice images, extract expense details, validate duplicates, and record the result in a Google spreadsheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt or invoice data may be sent to cloud services, including OpenAI for OCR or expense structuring and Google Sheets for storage. <br>
Mitigation: Use local OCR mode for images that should not be sent to OpenAI, keep cloud credentials narrowly scoped, and account for the fact that expense structuring still uses OpenAI outside test mode. <br>
Risk: The skill can automatically delete the default Sheet1 tab and restructure spreadsheet tabs. <br>
Mitigation: Install it with a dedicated empty Google spreadsheet shared only with the service account, and review or change the Sheet1 deletion behavior before using it with important spreadsheets. <br>
Risk: Service account and API credentials are required for normal operation. <br>
Mitigation: Store credentials outside shared project files, grant the service account access only to the intended spreadsheet, and run smoke tests with CLAWSHIER_TEST_MODE=1 before touching real APIs. <br>


## Reference(s): <br>
- [Clawshier on ClawHub](https://clawhub.ai/fdocr/clawshier) <br>
- [Google Cloud Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) <br>
- [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and short status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit a compact trace summary only when the user asks for tracing, debugging, or cost information.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
