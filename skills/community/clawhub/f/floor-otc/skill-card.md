## Description:

Use when an agent needs to quote a token swap, read the MENTAT open order book, check or prepare an OTC escrow deal, or verify a token by its address. MENTAT is the agent-native OTC venue. Escrow settlement on Base (atomic, no admin keys), CoW Protocol relay (agent-signed, MEV-protected), and an XMR route via Wagyu (XMR/USDC both directions, three legs, one proof per leg). Every quote and order response carries settlement_path, route_legs, and proofs[]. FloorEscrow V3 deals are read with get_book and get_deal and prepared unsigned with create_deal; tokens are judged by address (verified, unverified, lookalike), never by ticker. Quotes are free. MENTAT signs nothing for you, so get the human's explicit OK before any step is signed or sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agora0x](https://clawhub.ai/user/agora0x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use MENTAT to obtain token-swap quotes, inspect open orders and OTC deals, verify tokens by contract address, and prepare settlement steps. A human should review the transaction details and explicitly approve each step before it is signed or sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet signatures or transactions can move crypto assets, and token names or tickers may be misleading.

Mitigation: Use a wallet with spending limits and a separate approval step; verify the chain, token contract addresses, amounts, fees, expiry, destination, and transaction value before approving.

Risk: Orders and wallet addresses are shared with the service, and deal details—including private-link deals—remain public on-chain.

Mitigation: Avoid sharing unnecessary identifying information and treat on-chain deal terms as public.

Risk: The XMR route relies on Wagyu delivering funds, and live MENTAT endpoints and escrow-source claims were not independently verified during this review.

Mitigation: Check current route status and each leg's proof, and independently verify endpoints and contract addresses before interacting or relying on settlement.

## Reference(s):

- [MENTAT](https://mentat.market)
- [MENTAT contract and verified-token registry](https://api.mentat.market/.well-known/contracts.json)
- [MENTAT on ClawHub](https://clawhub.ai/agora0x/skills/mentat)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions, JSON]

**Output Format:** [JSON data and concise human-readable guidance; may include unsigned transaction or EIP-712 signing parameters and MCP configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transaction steps are prepared but not signed or sent by the skill; human approval is required.]

## Skill Version(s):

1.8.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
