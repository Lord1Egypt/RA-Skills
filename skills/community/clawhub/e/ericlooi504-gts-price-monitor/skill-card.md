## Description:

Monitor competitor product prices across Shopee, Lazada, Amazon, and other e-commerce platforms with automated tracking, alerts, and comparison reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, dropshippers, and small business owners use this skill to track competitor product prices, receive price-change alerts, and generate comparison reports that inform pricing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may visit configured product URLs, save local price and alert data, and create recurring scans.

Mitigation: Confirm the tracked URLs, review stored data expectations, and approve any recurring scan schedule before enabling automation.

Risk: E-commerce pages may show dynamic, region-specific, logged-in, or anti-bot-influenced prices.

Mitigation: Validate extracted prices before logging, preserve raw price text, and flag unusually large price changes for review.

## Reference(s):

- [Advanced Configuration](references/CONFIG.md)
- [Platform-Specific Notes](references/PLATFORMS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, local JSON/JSONL state files, and optional CSV reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save product, alert, and price-history data locally and may configure recurring scans when the user requests a schedule.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
