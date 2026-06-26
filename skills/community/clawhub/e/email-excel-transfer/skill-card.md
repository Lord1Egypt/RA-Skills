## Description: <br>
Automates transferring data from email attachments into Excel spreadsheets while defaulting to copied files so originals remain untouched. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomasz-pedzierski-infinity](https://clawhub.ai/user/tomasz-pedzierski-infinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and automation users use this skill to move data from selected email attachments into Excel workbooks. It guides an agent through mailbox access, attachment extraction, XLSX inspection, dry-run review, and saving approved updates to a copied workbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires mailbox access, which can expose email contents and attachments if the agent searches too broadly. <br>
Mitigation: Use a dedicated revocable mailbox or app password where possible, and require a specific sender, subject, date range, or explicit message selection before fetching mail. <br>
Risk: The skill can write spreadsheet values and could save incorrect changes if the selected attachment or cell updates are wrong. <br>
Mitigation: Confirm the exact attachment and planned cell changes before saving, and write only to a newly created copy rather than an original workbook. <br>
Risk: The artifact describes safety controls such as sender whitelisting and dry-run review, but users still need to ensure those controls are applied during execution. <br>
Mitigation: Require sender allowlisting or equivalent message constraints, keep preview mode enabled until changes are approved, and verify the output file path uses the copy prefix. <br>


## Reference(s): <br>
- [Gmail app passwords](https://myaccount.google.com) <br>
- [Microsoft account app passwords](https://account.microsoft.com) <br>
- [WP Poczta app passwords](https://poczta.wp.pl) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run preview and copy-only workbook handling guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
