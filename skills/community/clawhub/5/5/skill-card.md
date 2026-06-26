## Description: <br>
58区块同城 helps agents query a blockchain-based digital city platform for city rankings, city details, NFT avatar marketplace information, and block activity participation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to explore digital city information, check city popularity rankings and city details, browse or manage NFT avatars, and get information about block activities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-linked NFT purchases, trades, and governance actions can create financial or irreversible blockchain consequences. <br>
Mitigation: Require the agent to show every wallet connection, purchase, trade, vote, and exact amount, then obtain explicit user approval before taking action. <br>
Risk: External city, block, and NFT endpoints may return incomplete, stale, or untrusted information. <br>
Mitigation: Treat returned data as informational, cite the source endpoint when presenting results, and ask the user to confirm before relying on it for purchases or governance decisions. <br>
Risk: The skill declares local file read and write permissions, which may expose or modify user data if used too broadly. <br>
Mitigation: Keep file access read-only unless the user approves the exact file path and intended write operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/5) <br>
- [Publisher profile](https://clawhub.ai/user/hgta23) <br>
- [58区块同城 homepage](https://www.58.tl) <br>
- [City ranking endpoint](https://www.blockcity.vip/pages/block/area) <br>
- [City detail URL pattern](https://www.blockcity.vip/{city-area-code}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown or plain text summaries with optional API-derived city, block, and NFT data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access; wallet connection, purchase, trade, vote, and local file actions should be shown for explicit user approval before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
