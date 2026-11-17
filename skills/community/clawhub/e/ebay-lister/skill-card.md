## Description:

Turns item photos into an eBay listing by identifying the item, researching sold-comparable pricing, assessing condition, preparing listing fields, and driving a logged-in Chrome session to create a live listing or save a draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelsonscott](https://clawhub.ai/user/nelsonscott)

### License/Terms of Use:

MIT

## Use Case:

External sellers and agents use this skill to convert photos and listing details into eBay.com listings, including title, condition, price, category, shipping, photos, and description. It is intended for workflows where the seller can review listing details and choose draft or publish mode.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can publish listings through a signed-in eBay seller session.

Mitigation: Use draft mode or dry-run before publishing, and review the title, price, condition, category, shipping, photos, and description before going live.

Risk: Incorrect identification, sold-comparable research, condition grading, or shipping details can create misleading listings.

Mitigation: Verify ambiguous photo details, inspect condition-sensitive fields, and treat sold-comparable pricing as decision support rather than final seller judgment.

Risk: A configured notifyCommand can execute a local shell command after publish, draft, or block events.

Mitigation: Leave notifyCommand unset unless the command is fully trusted and needed for the deployment.

Risk: Local debug screenshots, logs, and listing payloads may contain account or listing details.

Mitigation: Clean up local run artifacts when they may expose seller, account, item, or listing information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nelsonscott/skills/ebay-lister)
- [Project homepage](https://github.com/NelsonScott/ebay-lister)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live eBay item URLs, draft URLs, draft IDs, blocked-publish diagnostics, and concise listing summaries.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
