---
name: rug-pull-detector
description: Detects potential rug-pulls and scams on new Solana memecoins by analyzing their DexScreener page. Use this when a user asks to check a Solana token for safety, rug-pulls, or scams.
---

# Rug-Pull Detector for Solana Tokens

This skill provides a standard operating procedure for analyzing Solana tokens (especially memecoins) to detect potential rug-pulls or scams using DexScreener.

## Prerequisites

Before starting the analysis, you MUST have the token address (contract address) provided by the user. If the user hasn't provided it, ask for it first.

## Workflow

When asked to analyze a Solana token for rug-pulls or scams, follow these steps:

### 1. Navigate to DexScreener

Use your browser tool to navigate to the DexScreener page for the specific Solana token:
`https://dexscreener.com/solana/<TOKEN_ADDRESS>`

### 2. Analyze Security Indicators

Once the page is loaded, carefully examine the page content for the following critical security indicators:

- **Liquidity**: Check if the liquidity is locked or burned. Low or unlocked liquidity is a major red flag for a rug-pull.
- **Top Holders**: Look at the distribution of token holders. If a small number of wallets hold a massive percentage of the supply, they can easily dump and crash the price.
- **Mint Authority**: Check if the mint authority is revoked. If it's still active, the creator can mint infinite new tokens, diluting the value to zero.
- **Freeze Authority**: Check if the freeze authority is disabled. If active, the creator can freeze users' ability to sell the token (a honeypot).
- **Market Cap (Mkt Cap) vs Fully Diluted Valuation (FDV)**: Compare these values.
- **Recent Transactions**: Look at the recent buy/sell history. Are there only buys and no sells? (Indicator of a honeypot). Are insiders dumping?

### 3. Report Findings

Compile a comprehensive report for the user based on your findings. Your report should include:

1. **Token Overview**: Name, Symbol, Current Price, Market Cap, and Liquidity.
2. **Security Analysis**: Detail the status of Mint Authority, Freeze Authority, Liquidity Lock/Burn, and Top Holders concentration.
3. **Risk Assessment**: Provide a clear conclusion on the risk level (Low, Medium, High, Extreme) based on the gathered data. Highlight any red flags that suggest a potential rug-pull or scam.

## Important Notes

- Always rely on the live data from the DexScreener page.
- If certain information is not immediately visible, you may need to interact with the page (e.g., clicking on specific tabs like "Security" or "Holders" if available) using your browser tool.
- Remind the user that this analysis is for informational purposes and does not constitute financial advice. Scammers constantly evolve their methods, and even tokens that appear safe can still be risky.
