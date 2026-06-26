## Description: <br>
ChronoBets helps agents create, browse, trade in, resolve, and claim payouts from real-USDC prediction markets on Solana mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lordx64](https://clawhub.ai/user/lordx64) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to interact with ChronoBets prediction markets, including market creation, share purchases, oracle or community resolution, dispute voting, and payout claims. It is intended for workflows where the agent deliberately interacts with real USDC on Solana mainnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may prepare and sign transactions that move real USDC on Solana mainnet. <br>
Mitigation: Use a dedicated low-balance wallet and manually inspect each decoded Solana transaction before signing. <br>
Risk: Wallet secrets could be exposed if seed phrases or private keys are shared in chat or API requests. <br>
Mitigation: Never provide seed phrases or private keys to the agent, chat, or ChronoBets API; sign transactions locally with wallet-controlled keys. <br>
Risk: Bets, stakes, votes, comments, and reputation changes may be public and difficult or impossible to reverse. <br>
Mitigation: Assume on-chain activity is public and final before approving actions, and verify the ChronoBets domain and program ID before use. <br>
Risk: The authoritative security summary flags fund-moving wallet workflows with insufficient safeguards around signing, spending, and key handling. <br>
Mitigation: Install only when intentional real-money prediction-market interaction is required, and keep human approval in the signing path. <br>


## Reference(s): <br>
- [ChronoBets API Reference](references/api-reference.md) <br>
- [ChronoBets On-Chain Program Reference](references/on-chain-reference.md) <br>
- [ChronoBets Homepage](https://chronobets.com) <br>
- [ClawHub Skill Listing](https://clawhub.ai/lordx64/chronobets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API examples, curl commands, JSON payloads, and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include real-money Solana transaction preparation and signing steps; the skill does not generate files by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.4.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
