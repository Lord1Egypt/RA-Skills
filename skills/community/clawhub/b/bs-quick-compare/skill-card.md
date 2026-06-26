## Description: <br>
Period-over-period variance analysis on the Balance Sheet pulled from QuickBooks Online, producing a four-tab Excel workbook with Summary, Detail, Flags, and CDC Log tabs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting and finance operators use this skill to compare QuickBooks Online balance sheet periods during close, lender review, investor analysis, or investigation of material changes in assets, liabilities, and equity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workbooks and CDC cache can contain sensitive client financial data. <br>
Mitigation: Run only with a trusted local QuickBooks client, confirm the company slug before execution, and protect or delete generated reports and cache files when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samledger67-dotcom/bs-quick-compare) <br>
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands and a generated Excel workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces BS_QuickCompare_{slug}_{as-of-date}.xlsx with Summary, Detail, Flags, and CDC Log tabs; CDC cache may be written under .cache/bs-quick-compare.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
