## Description:

Create SplitXCH royalty split addresses from plain language descriptions for splitting XCH payments, royalties, or revenue between multiple recipients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koba42corp](https://clawhub.ai/user/koba42corp)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn plain-language Chia payment split instructions into validated recipient allocations, API payloads, generated SplitXCH addresses, and human-readable summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send recipient names, XCH wallet addresses, and allocation details to SplitXCH.

Mitigation: Ask for a dry-run preview and confirm the final recipients, percentages, basis points, nested fee impact, and purpose before any API call.

Risk: The skill can create live Chia split addresses and the artifact does not require a mandatory confirmation step before creation.

Mitigation: Require explicit user confirmation before submitting a payload to SplitXCH, especially for nested splits or revenue distributions.

Risk: Nested split levels each incur the SplitXCH platform fee, which can change the effective payout distribution.

Mitigation: Show the full split tree and fee note for every level before creating parent or child split addresses.

## Reference(s):

- [SplitXCH API Reference](references/api.md)
- [SplitXCH Compute API](https://splitxch.com/api/compute/fast)
- [ClawHub Skill Page](https://clawhub.ai/koba42corp/skills/chia-splitxch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payload examples, shell command examples, split addresses, summary tables, and fee notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call the SplitXCH API after required wallet addresses and allocation details are available; dry-run previews can show calculated basis points without an API call.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
