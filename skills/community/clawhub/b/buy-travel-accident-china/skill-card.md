## Description:

Enables an agent to quote, purchase, manage, invoice, surrender, and refund China travel accident insurance through the UZYUN production API, including smart form-fill for Chinese ID cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pythons](https://clawhub.ai/user/pythons)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agencies and insurance operators use this skill to help users compare plans, calculate premiums, create orders, obtain payment links and policy documents, handle invoices, and process surrender or refund workflows for travel accident insurance in China.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can store authentication tokens, mobile numbers, policyholder identity data, insured-person details, and schema cache in plaintext .agent-state.json.

Mitigation: Use only in a private workspace, avoid committing or sharing .agent-state.json, and clear the file when the workflow is finished.

Risk: The skill can initiate commercial insurance actions including purchases, payment links, invoices, policy downloads, surrender, and refunds through a production API.

Mitigation: Confirm user intent and key identifiers before submitting orders, invoices, surrender requests, refunds, or payment actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pythons/skills/buy-travel-accident-china)
- [Publisher profile](https://clawhub.ai/user/pythons)
- [Production API base URL](https://prod.uzyun.cn/api/agent/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoints, JSON request fields, shell command examples, payment links, and ASCII QR codes when payments are created]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .agent-state.json with tokens, profile data, frequent insured details, and schema cache in the user's workspace.]

## Skill Version(s):

2.0.4 (source: server release, SKILL.md frontmatter, artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
