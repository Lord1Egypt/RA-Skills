## Description: <br>
从银行/券商PDF流水自动提取信息，生成美化的CRS金融账户信息申报表。支持PDF解析、数据提取、表格生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MasterBenC](https://clawhub.ai/user/MasterBenC) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users with overseas bank or brokerage statements use this skill to extract account details from text-based PDFs and generate CRS financial account information reports. Users should manually review and complete any missing or sensitive fields before filing or sharing results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive financial PDFs and may write names, account numbers, tax identifiers, balances, or transaction details into generated Excel files despite redaction claims. <br>
Mitigation: Treat input PDFs and generated workbooks as confidential, process them locally, and manually inspect or remove sensitive fields before sharing or relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MasterBenC/crs-report-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python usage instructions and generated Excel files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local text-based PDF statements and can generate XLSX CRS report templates or populated workbooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
