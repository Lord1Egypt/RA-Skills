## Description: <br>
Data Mover Skill helps agents automate cross-system data movement with OCR, screen capture, clipboard operations, field mapping, and local validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers can use this skill to extract data from screenshots, documents, spreadsheets, and business applications, then move validated records into target systems such as CRM, ERP, databases, or spreadsheets. It is best suited for supervised local RPA workflows where screen, clipboard, and destination-system access are intentionally granted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screen capture and OCR can collect credentials, regulated records, or other sensitive information visible on the desktop. <br>
Mitigation: Run only in a constrained workspace, close unrelated windows, avoid screens containing secrets or regulated data, and use test data before production use. <br>
Risk: Clipboard and keyboard or mouse automation can move incorrect data into business systems if source and destination windows are misidentified. <br>
Mitigation: Restrict source and destination windows or files, use dry-run or supervised operation first, and require human confirmation before writes to CRM, ERP, databases, or spreadsheets. <br>
Risk: OCR, field mapping, or validation errors can create inaccurate records at scale. <br>
Mitigation: Review confidence thresholds and validation summaries, verify mapping rules with sample records, and audit logs after each batch. <br>
Risk: Unpinned or unreviewed automation and OCR dependencies can increase supply-chain or runtime risk. <br>
Mitigation: Pin dependencies from trusted sources and review installed packages before enabling the skill. <br>


## Reference(s): <br>
- [Data Mover Skill on ClawHub](https://clawhub.ai/SxLiuYu/data-mover-skill) <br>
- [SxLiuYu publisher profile](https://clawhub.ai/user/SxLiuYu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command and JSON configuration examples; runtime script output may be JSON or console logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OCR results, validation summaries, local screenshots, and operation logs depending on how the automation is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
