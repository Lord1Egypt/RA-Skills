## Description: <br>
Standard Operating Procedure (SOP) that bridges extraction logic to CRM append operations via atomic nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations users use this skill to extract CRM entities from business emails or notes and append them to a CRM spreadsheet with verification stops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM contact data can be written to a spreadsheet from broadly defined business messages without a clear approval or scoping gate. <br>
Mitigation: Use a limited test spreadsheet first, require explicit approval before each append, and confirm the source message, extracted fields, destination sheet, and duplicate handling. <br>
Risk: Extraction errors or failed append operations can create incomplete or incorrect CRM records. <br>
Mitigation: Review the extracted JSON before writing, verify each append confirmation, and stop for manual handling when retries fail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/crm-entity-extraction) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls] <br>
**Output Format:** [JSON summary with append confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires access to a Google Sheets append-capable atomic node or equivalent CRM spreadsheet integration.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
