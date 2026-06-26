# Trigger Reference

Use this reference when refining what kinds of user phrasing should activate the
skill.

## Trigger on these intents

Trigger when the user wants to:

- Bridge funds to Arbitrum
- Bridge funds from Arbitrum
- Move assets between Arbitrum chains through the official route
- Understand bridge timing
- Diagnose a stuck bridge
- Claim withdrawn funds
- Track bridge status
- Clarify USDC vs USDC.e on Arbitrum One

## Natural-language patterns that should count

- "bridge my usdc from ethereum to arbitrum"
- "bridge mu USDC from ethereum to arbitrum"
- "move eth to arb"
- "send my tokens from arb back to eth"
- "why is my arbitrum bridge stuck"
- "get my funds onto arbitrum"
- "get my usdc back to ethereum"
- "check my arbitrum withdrawal"
- "claim my arbitrum bridge withdrawal"
- "move funds from nova to one"

## Trigger cues

Treat these as strong cues when they appear with Arbitrum context:

- `bridge`
- `move`
- `send`
- `withdraw`
- `claim`
- `track`
- `check`
- `unstick`

Also allow:

- Abbreviations such as `arb`, `arb one`, `nova`, and `eth`
- Missing punctuation or compressed phrasing
- Minor typos such as `mu`, `etherum`, or `abitrum`

## Do not trigger on these

- General Arbitrum protocol education
- Gas price lookups
- Tokenomics comparisons
- Contract deployment help
- Generic scripting or coding tasks

## Example requests that should not trigger

- "Explain how Arbitrum Nitro works under the hood."
- "What are today's ETH gas prices?"
- "Compare Arbitrum and Optimism tokenomics."
- "Help me deploy a contract to Arbitrum Sepolia."
- "Write a Python script to monitor ERC-20 transfers."
