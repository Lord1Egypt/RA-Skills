## Description:

eBay research agent. Search for deals, evaluate prices, and get fair value estimates using eBay REST APIs. No eBay account required - just a free developer API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephflu](https://clawhub.ai/user/josephflu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research eBay listings, estimate fair market value, evaluate deal quality, and maintain local price watches using eBay REST APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires eBay developer App ID and Cert ID values and uses them to request OAuth tokens from eBay.

Mitigation: Install only if you are comfortable allowing the skill to query eBay APIs with those developer credentials.

Risk: Seller API and selling-guide references include capabilities beyond the current research CLI.

Mitigation: Treat those references as informational and do not provide user OAuth seller tokens or authorize listing, fulfillment, or webhook actions unless that expanded use is intentional.

Risk: Watch commands create or update local watchlist state, and a custom state-file path can overwrite the chosen file.

Mitigation: Use the default watchlist path or choose a dedicated state file that does not contain unrelated data.

## Reference(s):

- [eBay Agent ClawHub Page](https://clawhub.ai/josephflu/skills/ebay-agent)
- [Project Homepage](https://github.com/josephflu/clawhub-skills)
- [eBay Developer Portal](https://developer.ebay.com)
- [eBay REST API Cheatsheet](references/ebay-api-cheatsheet.md)
- [eBay Scam Detection Guide](references/ebay-scam-detection.md)
- [The eBay Seller's Reference Guide](references/ebay-selling-guide.md)
- [eBay Tooling Ecosystem Landscape Research](docs/research/ecosystem-landscape.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown or plain text responses, with optional JSON output from CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses eBay developer credentials from environment variables and can write local watch state.]

## Skill Version(s):

0.5.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
