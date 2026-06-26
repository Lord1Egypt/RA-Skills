## Description: <br>
Accounting Assistant is a bilingual expense tracking and bookkeeping skill that records natural-language spending, produces reports and exports, and generates expense charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swiftuis](https://clawhub.ai/user/swiftuis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to record daily expenses in Chinese or English, categorize transactions, manage currencies and budgets, and generate personal spending reports, exports, and charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The chart script may fall back to a full-screen macOS screenshot when normal chart rendering fails, which can capture unrelated visible screen content. <br>
Mitigation: Review chart output before sharing it and avoid the chart PNG/report feature on macOS unless the screenshot fallback is removed or clearly gated. <br>


## Reference(s): <br>
- [Expense Categories Reference](references/categories.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/swiftuis/accounting-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Bilingual text or Markdown responses, JSON script results, and local CSV, JSON, HTML, or PNG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores ledger data, exports, and chart artifacts under ~/.qclaw/workspace/expense-ledger/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
