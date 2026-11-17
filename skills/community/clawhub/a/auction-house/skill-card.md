## Description:

Scout, monitor, and bid on auctions on House (houseproto.fun), a crypto auction platform on Base, while proactively watching for items the user cares about.

This skill is ready for commercial/non-commercial use.

## Publisher:

[im-still-thinking](https://clawhub.ai/user/im-still-thinking)

### License/Terms of Use:

MIT

## Use Case:

External users and MCP-compatible agent clients use this skill to scout House auctions, monitor active bids, and create or place bids through a configured House bot wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create auctions and place real crypto bids using a House bot API key tied to a funded wallet.

Mitigation: Use a dedicated low-balance bot wallet, verify wallet balances before bidding, and require explicit user confirmation unless a narrow standing rule exists.

Risk: Broad autonomous auto-bid rules could spend more than intended.

Mitigation: Set explicit token, auction, and maximum-bid limits; avoid broad matching rules; and review active bids regularly.

Risk: AUCTION_HOUSE_URL can redirect API calls away from the default House endpoint.

Mitigation: Leave AUCTION_HOUSE_URL unset or verify that it points only to the intended House API before use.

Risk: Unversioned npx or global package installation can change behavior when the package updates.

Mitigation: Prefer a pinned, reviewed package version for deployment.

## Reference(s):

- [House platform](https://www.houseproto.fun)
- [House API key settings](https://www.houseproto.fun/settings)
- [ClawHub skill page](https://clawhub.ai/im-still-thinking/skills/auction-house)
- [ClawHub publisher profile](https://clawhub.ai/user/im-still-thinking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with MCP tool text responses and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AUCTION_HOUSE_API_KEY and a funded House bot wallet; optional AUCTION_HOUSE_URL should point only to the intended House API.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
