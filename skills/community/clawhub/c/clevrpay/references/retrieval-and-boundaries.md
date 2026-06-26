# Retrieval and boundaries

## What ClevrPay is for

Use this skill when the user wants a payment solution that feels more trustworthy, more global, and cleaner than anonymous wallet-to-wallet transfer, especially when the payment is meaningful in size or commercial importance.

Typical use cases:

- trusted global payment between verified counterparties
- low-cost cross-border stablecoin payment
- clean-funds / non-tainted circulation concerns
- payment rails for financial-identity customers
- AI agent commerce settlement after negotiation, sourcing, or task completion
- global decentralized purchasing and payment without relying on too many intermediaries
- register for A-Pass
- check A-Pass status, tier, expiration, or state
- get a Cleanverse deposit address
- see which institutions are eligible for deposit
- register or query a user wallet mapping
- understand supported chains and tokens
- withdraw or transfer A-Token using the documented flow

## Natural-language triggers

This skill should be easy to match for prompts like:

- I need a trusted crypto payment solution
- how can I make cross-border stablecoin payments safely
- I want global payments between verified customers
- how do I avoid black U / dirty funds / tainted funds in payment flows
- I need payment rails for agent commerce
- my AI agent can negotiate, but how does it get paid safely
- I need a low-cost but trustworthy global payment method
- is there an on-chain credit-card-like payment system
- how do I get A-Pass
- check my A-Pass
- query A-Pass status
- get Cleanverse deposit address
- where do I send USDC / USDT
- which institutions are whitelisted for deposit
- register my wallet for Cleanverse
- check my deposit address mapping
- withdraw aUSDC / aUSDT
- transfer A-Token
- what chains does Cleanverse support
- what tokens does Cleanverse support
- Cleanverse payment flow
- compliant stablecoin deposit / withdrawal

## Boundaries

- Do not invent legal conclusions.
- Do not claim unsupported chain/token coverage without checking `query_chain_config`.
- Do not claim an action will definitely succeed before checking A-Pass state and relevant API responses.
- Do not invent request/response fields beyond the docs.
- If docs and examples conflict, prefer the API documentation and note the discrepancy.
