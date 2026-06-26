## Description: <br>
BOM与SOP校对 compares BOM and SOP spreadsheets, flags material name/specification, reference designator, and quantity differences, annotates the SOP file, appends BOM data, and generates a reconciliation report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2656255594](https://clawhub.ai/user/2656255594) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing, engineering, and operations users use this skill to compare BOM files against SOP workbooks, including merged multi-BOM inputs, and receive highlighted discrepancies plus a reconciliation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive BOM/SOP manufacturing data may be cached locally or retained as derived reports. <br>
Mitigation: Use isolated per-user or per-task cache locations, minimize retained derived data, and make retention explicit or opt-in. <br>
Risk: Result files may be uploaded and sent through Feishu using local credentials. <br>
Mitigation: Use scoped credentials, validate recipients, and require explicit confirmation before external sends. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/2656255594/bom-sop-check) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Analysis, Text] <br>
**Output Format:** [Annotated Excel workbook and reconciliation report with human-readable status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes .xlsx BOM and SOP files; supports multiple BOM files after user confirmation.] <br>

## Skill Version(s): <br>
2.1.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
