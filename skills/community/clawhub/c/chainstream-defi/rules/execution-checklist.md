# Execution Checklist

Step-by-step verification for DeFi operations. Follow in order.

## Pre-Execution

- [ ] User intent is clear (which token, how much, which chain)
- [ ] Input token address validated (format matches chain)
- [ ] Output token address validated
- [ ] Chain is supported (sol/bsc/eth)
- [ ] Wallet is configured (`chainstream config auth` shows active wallet)
- [ ] Amount is reasonable (not zero, not exceeding known balance)
- [ ] Slippage is within bounds (0-100, integer percentage, e.g. 5 = 5%)

## Quote Phase

- [ ] `dex route` called successfully
- [ ] Price impact calculated and displayed
- [ ] Expected output amount shown
- [ ] Gas estimate shown (if available)
- [ ] User has reviewed the summary

## Confirmation Phase

- [ ] User explicitly confirmed (typed "y" or "yes")
- [ ] Confirmation was NOT auto-generated or implied

## Execution Phase

- [ ] `dex swap` called with confirmed parameters
- [ ] Transaction signed (TEE or local)
- [ ] Signed tx broadcast via `/v2/transaction/:chain/send`
- [ ] Job ID received

## Post-Execution

- [ ] Job polled to completion (or timeout)
- [ ] Actual fill amounts displayed (input consumed, output received)
- [ ] Block explorer link displayed
- [ ] If failed: error shown, no auto-retry
