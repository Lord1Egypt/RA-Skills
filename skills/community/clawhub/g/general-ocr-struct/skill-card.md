## Description: <br>
Offline OCR extracts and structures Chinese and English screenshot text into raw or cleaned rows and fields for receipts, tables, chat screenshots, statements, and other text-heavy images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[9penny](https://clawhub.ai/user/9penny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to run local OCR on user-selected images, review raw recognized text, and structure clear transaction-like screenshots into reusable fields without sending image content over a network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images may contain financial, chat, identity, or other sensitive details. <br>
Mitigation: Use the skill only on images intentionally selected by the user and review the raw OCR output before using structured fields. <br>
Risk: Fixed structuring heuristics can mis-group rows or merchant names in transaction screenshots. <br>
Mitigation: Treat raw OCR as the source of truth, mark ambiguous fields as requiring confirmation, and request a higher-resolution source image when OCR quality is weak. <br>


## Reference(s): <br>
- [Structuring notes](artifact/references.md) <br>
- [ClawHub skill page](https://clawhub.ai/9penny/general-ocr-struct) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON, commonly summarized in Markdown with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Raw OCR text should be reviewed before relying on structured fields; uncertain fields are marked for confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
