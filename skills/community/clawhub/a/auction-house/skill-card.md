## Description: <br>
Scout, monitor, and bid on auctions on House (houseproto.fun), a crypto auction platform on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[im-still-thinking](https://clawhub.ai/user/im-still-thinking) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to connect an MCP-compatible agent to House so it can browse auctions, monitor user interests, create auctions, check wallet balances, and place bids with a funded bot wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can use a funded House bot wallet to place live bids or create auctions. <br>
Mitigation: Keep wallet balances low and require manual confirmation for valuable bids or auction creation. <br>
Risk: Broad standing auto-bid rules can spend more than the user intended. <br>
Mitigation: Use explicit token, auction, max-spend, and time limits for any auto-bid rule. <br>
Risk: An alternate AUCTION_HOUSE_URL can redirect activity to an endpoint the user did not intend to trust. <br>
Mitigation: Leave AUCTION_HOUSE_URL unset unless the alternate endpoint has been deliberately reviewed and trusted. <br>


## Reference(s): <br>
- [House platform](https://www.houseproto.fun) <br>
- [House bot API key settings](https://www.houseproto.fun/settings) <br>
- [ClawHub skill page](https://clawhub.ai/im-still-thinking/auction-house) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON configuration snippets, and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AUCTION_HOUSE_API_KEY; AUCTION_HOUSE_URL is optional for selecting an alternate House API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
