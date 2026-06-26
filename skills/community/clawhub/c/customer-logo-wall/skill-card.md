## Description: <br>
Automates customer spreadsheet processing, Chinese company-name lookup, logo download and verification, logo format normalization, and generation of a customer logo-wall PowerPoint deck. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, sales, and marketing users use this skill to turn customer Excel lists into tiered logo-wall PowerPoint decks with Chinese company names and standardized logo assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer or company names may be sent to public search engines and web services during logo and Chinese-name lookup. <br>
Mitigation: Use only customer lists approved for external lookup, avoid confidential customer data, and confirm that public search is permitted before running the workflow. <br>
Risk: The workflow can overwrite business workbooks and replace downloaded logo assets. <br>
Mitigation: Back up the workbook first and require confirmation before overwriting Excel files or replacing existing logo assets. <br>
Risk: Downloaded logos or generated filenames may be incorrect or misleading. <br>
Mitigation: Review generated filenames, logo sources, and the final logo-wall output before using it in business materials. <br>


## Reference(s): <br>
- [Customer Logo Wall Skill on ClawHub](https://clawhub.ai/heavenchenggong/customer-logo-wall) <br>
- [Logo automatic verification](references/logo-verification.md) <br>
- [Logo format issues and solutions](references/logo-format-issues.md) <br>
- [PowerPoint design specification](references/ppt-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands plus generated Excel, JSON, PNG, and PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may update the input workbook and replace local logo assets when run.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
