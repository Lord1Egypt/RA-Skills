## Description: <br>
Element Market API integration. This skill strictly requires the 'ELEMENT_API_KEY' environment variable to function. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beelzebub520](https://clawhub.ai/user/beelzebub520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Element Market for NFT collection statistics, rankings, wallet holdings, received offers, and recent sale activity. Wallet-address lookups should only be run after user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet lookups can disclose NFT holdings, offers, and recent trading activity to Element Market. <br>
Mitigation: Ask for explicit user approval before querying any wallet address, and only submit addresses the user is willing to share with that service. <br>
Risk: The skill depends on an Element API key and sends read-only requests to Element Market. <br>
Mitigation: Configure ELEMENT_API_KEY only in an appropriate agent environment and review outbound API calls before use. <br>


## Reference(s): <br>
- [Element NFT Tracker Homepage](https://github.com/beelzebub520/element-nft-tracker) <br>
- [Element API Documentation](https://element.readme.io/reference/api-overview) <br>
- [Element API Key Setup](https://element.market/apikeys) <br>
- [Element Market](https://element.market) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and the ELEMENT_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
