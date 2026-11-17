## Description:

AI-native accounting for UK micro-businesses. Use when the user wants to track transactions, manage VAT, check deadlines, or do any bookkeeping for a UK limited company.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulgosnell](https://clawhub.ai/user/paulgosnell)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to manage bookkeeping for UK micro-businesses, including transaction tracking, VAT summaries, deadline monitoring, document handling, and invoice checks.

### Deployment Geography for Use:

United Kingdom

## Known Risks and Mitigations:

Risk: The skill can encourage account creation and API key use for an external bookkeeping service.

Mitigation: Prefer user-created accounts and API keys, and require explicit approval before sending signup details.

Risk: The API key may allow read and write access to financial records.

Mitigation: Use the lowest scope that works and require confirmation before creating, updating, or uploading financial data.

Risk: The skill may handle company details, personal details, and business documents.

Mitigation: Send only necessary data and confirm with the user before uploading documents or transmitting sensitive bookkeeping information.

## Reference(s):

- [AccountsOS ClawHub skill page](https://clawhub.ai/paulgosnell/skills/accountsos)
- [AccountsOS homepage](https://accounts-os.com)
- [AccountsOS MCP API endpoint](https://accounts-os.com/api/mcp)
- [AccountsOS agent signup endpoint](https://accounts-os.com/api/agent-signup)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with JSON request bodies and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ACCOUNTSOS_API_KEY and network access to accounts-os.com.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
