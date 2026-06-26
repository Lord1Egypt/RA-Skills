## Description: <br>
Connects agent workflows to FiBuKI.com for PSD2 bank transaction browsing, receipt matching, expense categorization, and business partner management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felixtosh](https://clawhub.ai/user/felixtosh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operators use this skill to let an agent inspect European bank transactions, match receipts or invoices, categorize expenses, import transactions, and manage partners through FiBuKI.com. <br>

### Deployment Geography for Use: <br>
Europe <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad access to sensitive banking transactions, receipts, invoices, and partner data. <br>
Mitigation: Install only in agent environments trusted with financial data and revoke FIBUKI_API_KEY when access is no longer needed. <br>
Risk: The skill can perform account-changing actions such as source deletion, file uploads, transaction imports or edits, partner/category changes, and bulk AI matching. <br>
Mitigation: Require explicit user confirmation before destructive, bulk, or account-changing actions. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/felixtosh/fibuki) <br>
- [FiBuKI Homepage](https://fibuki.com) <br>
- [FiBuKI Machine-Readable Docs](https://fibuki.com/llm.txt) <br>
- [FiBuKI OpenAPI Spec](https://fibuki.com/api/openapi.json) <br>
- [FiBuKI MCP Endpoint](https://fibuki.com/api/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with HTTP API call instructions and structured tool arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIBUKI_API_KEY and FiBuKI plan features for file upload and AI matching actions.] <br>

## Skill Version(s): <br>
0.1.15 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
