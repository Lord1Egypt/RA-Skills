## Description:

Buy and return items on Amazon using browser automation for purchasing, reordering, checking order history, and processing returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

External users can use this skill to let an agent operate an authenticated Amazon browser session for purchases, reorders, order-history lookup, and returns. It is intended for browser-assisted shopping workflows that still require user oversight for payment, ordering, returns, and account access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent operates inside an authenticated Amazon browser profile and can affect purchases, returns, payments, and account activity.

Mitigation: Use a dedicated browser profile, monitor the session, and require explicit approval before every order or return submission.

Risk: The skill can encourage credential access through the browser profile workflow.

Mitigation: Require manual login and do not allow the agent to read passwords or retrieve credentials from a password manager.

Risk: Return condition answers can affect refund eligibility and accuracy.

Mitigation: Require the user to provide or confirm product-condition answers directly before submitting a return.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brennerspear/skills/amazon-ordering)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser-operation guidance, screenshots for user confirmation, order or return summaries, and setup commands for Chrome remote debugging.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
