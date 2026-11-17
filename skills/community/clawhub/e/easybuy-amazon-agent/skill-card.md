## Description:

Tracks Amazon prices, monitors orders, scrapes reviews, fetches order details, drafts refund messages, and manages refund cases efficiently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skillpack to inspect Amazon product, order, review, and messaging pages, collect case evidence, draft after-sales messages, and guide refund, return, replacement, and price-check workflows.

### Deployment Geography for Use:

Global, with live playbook evidence for Amazon.com and Amazon.com.au marketplaces.

## Known Risks and Mitigations:

Risk: The extension requests broad browser automation authority and browser-wide access beyond the Amazon-focused use case.

Mitigation: Install only when that level of browser access is acceptable, use it on intended Amazon pages, and review each requested tool action before approval.

Risk: The extension can store screenshots, DOM snippets, order details, traces, and API configuration in local browser storage.

Mitigation: Avoid entering valuable API keys unless the endpoint is trusted and keys can be rotated or scoped; clear stored extension data when retained screenshots or order details are no longer needed.

Risk: Message drafting and form-filling flows can type or submit after-sales messages if auto-send is enabled.

Mitigation: Keep auto-send disabled unless intentional and review generated messages and form actions before approving submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/skills/easybuy-amazon-agent)
- [Publisher profile](https://clawhub.ai/user/luoqianchenguni-max)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [JSON tool results and short text drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted order, product, review, price, message-thread, URL, DOM snippet, screenshot artifact, and case export identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest version is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
