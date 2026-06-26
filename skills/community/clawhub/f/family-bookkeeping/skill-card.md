## Description: <br>
Manage a family bookkeeping workflow backed by Feishu Bitable for recording, querying, updating, importing, and reporting household transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzlawliet](https://clawhub.ai/user/hzlawliet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to maintain a shared household ledger in Feishu Bitable, including natural-language income and expense capture, WeChat or Alipay bill import, duplicate checks, record updates, and monthly or yearly summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change a live shared financial ledger. <br>
Mitigation: Use a least-privilege Feishu app limited to the intended table, confirm the target ledger before writes, and prefer dry-run or precheck paths before imports or edits. <br>
Risk: Sensitive ledger data may be left behind in temporary files. <br>
Mitigation: Clean generated temporary files after use or patch temporary-file handling before using the skill with real household financial data. <br>
Risk: The artifact may contain a syntax error in add_manual_record.py. <br>
Mitigation: Run tests or a syntax check before relying on manual record creation, and fix the script before live use if the error is present. <br>


## Reference(s): <br>
- [Family Bookkeeping ClawHub Page](https://clawhub.ai/hzlawliet/family-bookkeeping) <br>
- [Family Bookkeeping Category System](references/category-system.md) <br>
- [Family Bookkeeping Feishu Import](references/feishu-import.md) <br>
- [Family Bookkeeping Import Mapping](references/import-mapping.md) <br>
- [Family Bookkeeping Reporting](references/reporting.md) <br>
- [Family Bookkeeping Usage](references/usage.md) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files, API calls] <br>
**Output Format:** [Markdown guidance with shell command examples; helper scripts can produce JSON and CSV ledger files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu credentials and ledger identifiers through environment variables; direct-write workflows can change live Bitable records.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
