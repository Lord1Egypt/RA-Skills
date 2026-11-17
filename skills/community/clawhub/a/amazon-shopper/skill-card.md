## Description:

Buy and return items on Amazon using browser automation for purchasing, reordering, checking order history, and processing returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

External users use this skill to automate Amazon shopping tasks, including purchases, reorders, order-history checks, and return processing through an authenticated browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control an authenticated Amazon session and may complete purchases or returns before the user reviews the final action.

Mitigation: Require manual login and explicit user approval before every purchase or return submission.

Risk: Browser automation may use saved Amazon credentials, shipping addresses, and payment methods.

Mitigation: Verify the active account, shipping address, payment method, refund method, and return drop-off details before submitting any transaction.

## Reference(s):

- [Amazon Shopper skill page](https://clawhub.ai/brennerspear/skills/amazon-shopper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with browser automation commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshots or brief purchase and return summaries when user review or completion reporting is needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
