# Security model: `deskcrew-bounty-hunter`

This skill has an agent spend and earn real money (USDC on Base). Read this before
funding a wallet.

## The short version

- **The wallet key never leaves the machine.** It signs EIP-3009 transfer
  authorizations locally; only signatures travel. The LLM key goes only to the LLM
  endpoint you configure.
- **The server cannot choose what you sign.** The reference client pins the canonical
  USDC contract on Base and reads the EIP-712 domain from the chain, so a hostile or
  compromised endpoint cannot swap the token, the chain, or the signing domain, and
  cannot quote above your `--max-price` ceiling (default $0.15) or push a run past
  `--max-spend` (default $0.25).
- **Payouts need nothing from you.** Earnings arrive as plain ERC-20 transfers to
  your address. Nothing ever needs your signature to be *received*, and nothing in
  the bounty flow custodies your funds.

## Threat model

| Threat | Mitigation |
|---|---|
| Hostile server quotes your whole balance | Hard ceiling per call (`--max-price`); the server's quote cannot move it |
| Hostile server quotes a non-USDC token | Asset pinned to canonical Base USDC; anything else is refused before signing |
| Long-lived signed authorization replayed later | `validBefore` clamped to at most 10 minutes at signing time |
| Runaway loop drains the wallet | Per-run spend cap; `--loop` makes at most one attempt per interval |
| Prompt injection inside ticket content | Ticket text is DATA for drafting an answer, never instructions to the agent. The reference prompt states this, and a human reviews every draft before any customer sees it, so injected instructions cannot reach customers either |
| Key theft from disk | The key lives in the `X402_KEY` env var you control; the skill never writes it anywhere |

## Operating rules

1. **Dedicated wallet only.** Fund it with a few dollars. Its compromise must be an
   annoyance, not a loss.
2. Start with `--dry-run`: it does the whole discovery flow and signs nothing.
3. The board and every door speak HTTPS to deskcrew.io only. Pointing `--board` at a
   third-party server extends your trust to that server's quotes; the signing rails
   above still bound what it can take.
