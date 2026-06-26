## Description: <br>
Emoji Today lets an agent cast a paid onchain vote in the daily emoji.today election and optionally mint that vote as an NFT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bill-makes](https://clawhub.ai/user/bill-makes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents with a Farcaster FID and a funded Base wallet use this skill to vote for a daily emoji, then share or mint the result when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EVM private key and can sign paid onchain transactions. <br>
Mitigation: Use a fresh low-balance wallet, never use a primary wallet key, and keep only the funds needed for expected votes or mints. <br>
Risk: Voting costs USDC on Base, and optional minting costs additional USDC. <br>
Mitigation: Personally confirm every vote, mint, recipient address, and social post before execution. <br>
Risk: Overriding EMOJI_TODAY_URL can redirect signing and payment requests to a different endpoint. <br>
Mitigation: Leave EMOJI_TODAY_URL at the default unless the replacement endpoint is fully trusted. <br>


## Reference(s): <br>
- [Emoji Today](https://emoji.today) <br>
- [Emoji Today Vote API](https://emoji.today/api/vote) <br>
- [Emoji Today Mint API](https://emoji.today/api/vote/mint) <br>
- [Neynar Farcaster ID lookup](https://neynar.com/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the voting and minting script prints JSON responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, EVM_PRIVATE_KEY, FARCASTER_FID, and a wallet with USDC on Base.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
