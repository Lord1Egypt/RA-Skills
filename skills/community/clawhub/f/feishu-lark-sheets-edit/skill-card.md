## Description: <br>
This skill lets an agent read, write, and manage Lark/Feishu Sheets and download Lark/Feishu Drive files through the official OpenAPI, including local PDF text and image extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mli-cj](https://clawhub.ai/user/mli-cj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to let an agent export or update Lark/Feishu spreadsheet data, add or clone sheet tabs, download cloud files, and extract PDF content for summaries, reports, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Feishu/Lark app credentials to access spreadsheets and cloud files. <br>
Mitigation: Install only when this credential access is intended, configure least-privilege app scopes, and share only the intended sheets or files with the app. <br>
Risk: Sheet write operations can change cloud data. <br>
Mitigation: Confirm spreadsheet tokens, target ranges, and values before writes; use the documented dry-run flow when previewing changes. <br>
Risk: PDF extraction may install runtime Python dependencies. <br>
Mitigation: Preinstall reviewed PDF libraries in managed environments instead of relying on runtime package installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mli-cj/feishu-lark-sheets-edit) <br>
- [Lark/Feishu Sheets and Drive OpenAPI reference](artifact/references/lark-sheets-api.md) <br>
- [Skill README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; helper scripts can produce CSV, JSON, downloaded files, extracted text, and extracted images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and local Feishu/Lark app credentials in ~/.openclaw/openclaw.json; PDF helpers may install Python packages at runtime.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
