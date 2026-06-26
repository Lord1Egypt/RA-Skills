## Description: <br>
AI-native accounting for UK micro-businesses. Use when the user wants to track transactions, manage VAT, check deadlines, or do any bookkeeping for a UK limited company. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgosnell](https://clawhub.ai/user/paulgosnell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to maintain bookkeeping workflows for UK micro-businesses, including tracking transactions, VAT position, deadlines, documents, invoices, and categorization. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create accounts and obtain API keys through agent self-signup. <br>
Mitigation: Prefer human-created accounts and require explicit user approval before an agent creates an account or stores an API key. <br>
Risk: The skill can change bookkeeping records, deadlines, transaction categories, and uploaded financial documents. <br>
Mitigation: Use the least-privilege API key available and require human approval before write actions or document uploads. <br>
Risk: The skill handles financial records where incorrect entries or categorization may affect tax and reporting workflows. <br>
Mitigation: Have a qualified human review VAT summaries, deadlines, categorization, and records before filing or relying on them for business decisions. <br>


## Reference(s): <br>
- [AccountsOS app](https://accounts-os.com) <br>
- [AccountsOS MCP API](https://accounts-os.com/api/mcp) <br>
- [AccountsOS agent signup API](https://accounts-os.com/api/agent-signup) <br>
- [Publisher profile](https://clawhub.ai/user/paulgosnell) <br>
- [Skill page](https://clawhub.ai/paulgosnell/accountsos) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ACCOUNTSOS_API_KEY and network access to the AccountsOS API.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
