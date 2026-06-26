## Description: <br>
eBay research agent for searching deals, evaluating prices, and estimating fair value with eBay REST APIs using developer API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephflu](https://clawhub.ai/user/josephflu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research eBay listings, compare prices, estimate fair market value, and maintain local watch searches for deals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires eBay developer credentials for API access. <br>
Mitigation: Provide EBAY_APP_ID and EBAY_CERT_ID only for the intended eBay developer app, prefer sandbox credentials for testing, and avoid sharing environment dumps that include secrets. <br>
Risk: Bundled reference material includes seller-side listing, order, and webhook operations beyond the normal research workflow. <br>
Mitigation: Treat seller API sections as reference-only unless intentionally performing account-changing seller operations with appropriate OAuth tokens and prior sandbox testing. <br>
Risk: Saved watch searches are stored in a local JSON file by default. <br>
Mitigation: Review the watch state file for sensitive search terms and use the --state-file option when storage location needs to be controlled. <br>
Risk: Search, valuation, and deal ratings can influence purchase decisions. <br>
Mitigation: Use results as research guidance and manually verify listing condition, seller trust, total price, shipping terms, and scam indicators before buying. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/josephflu/ebay-agent) <br>
- [Project Homepage](https://github.com/josephflu/clawhub-skills) <br>
- [eBay REST API Cheatsheet](references/ebay-api-cheatsheet.md) <br>
- [eBay Scam Detection Guide](references/ebay-scam-detection.md) <br>
- [eBay Selling Guide](references/ebay-selling-guide.md) <br>
- [eBay Tooling Ecosystem Landscape Research](docs/research/ecosystem-landscape.md) <br>
- [eBay Developer Portal](https://developer.ebay.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown or terminal text, with optional JSON from CLI commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ranked listings, valuation ranges, deal ratings, watch results, links, and credential setup guidance.] <br>

## Skill Version(s): <br>
0.5.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
