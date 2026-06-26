## Description: <br>
智能记账助手。用户提到记账、支出、收入、账本、流水、应收、应付、发票、票据、报销等关键词时使用此技能。支持文字直接记账，也可调用其他技能预处理图片/语音/文件后进行记账。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heygallon](https://clawhub.ai/user/heygallon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn Chinese-language bookkeeping requests, receipts, invoices, and parsed document text into accounting queries or entries against the caiwu888.cn accounting backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real accounting records from inferred text, OCR, speech, or document parsing. <br>
Mitigation: Require the agent to preview normalized fields and obtain explicit user approval before every add operation. <br>
Risk: The skill depends on ACCOUNTING_API_TOKEN for access to the caiwu888.cn backend. <br>
Mitigation: Use a scoped token, keep it in the environment, and avoid exposing it in prompts, logs, command output, or shared files. <br>
Risk: Parsed receipts, invoices, PDFs, spreadsheets, or audio may contain incorrect or ambiguous financial details. <br>
Mitigation: Verify amount, transaction type, ledger, dates, company, invoice status, and due dates with the user before writing records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heygallon/accountingforcaijin) <br>
- [caiwu888.cn accounting API endpoint](https://api.caiwu888.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON request or response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and ACCOUNTING_API_TOKEN; commands can read accounting metadata, query transactions, and add accounting records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
