## Description: <br>
Convert PDF bank statements to CSV or JSON using the Bank Statement Converter API, including password-protected files and processing status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BallerIndustries](https://clawhub.ai/user/BallerIndustries) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare shell commands for uploading bank statement PDFs to an external conversion service, checking processing status, and retrieving normalized CSV or JSON transaction data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends highly sensitive bank statements and optional PDF passwords to an external service. <br>
Mitigation: Review the provider's privacy, retention, and compliance posture before using real financial records; use test files first. <br>
Risk: The required API key metadata is incomplete, which can make credential handling expectations unclear. <br>
Mitigation: Use a limited or disposable API key when possible, avoid reused passwords, and do not use the skill for regulated or high-risk financial records unless the external processing arrangement is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BallerIndustries/bank-statement-converter) <br>
- [Bank Statement Converter registration](https://bankstatementconverter.com/legacy-register) <br>
- [Bank Statement Converter login](https://bankstatementconverter.com/login) <br>
- [Bank Statement Converter settings](https://bankstatementconverter.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, CSV] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BANKSTATEMENT_API_KEY and sends uploaded bank statement PDFs to an external API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
