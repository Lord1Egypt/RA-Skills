# Troubleshooting Reference

Use this reference when the user says a bridge is stuck, missing, not claimable,
or behaving unexpectedly.

Format to follow:

- Symptom
- Likely cause
- What to verify
- What to say next

## No wallet popup

- Likely cause: insufficient source-chain ETH for gas, wrong network, or wallet connection issue
- What to verify: source-chain ETH balance, connected wallet, selected network, whether approval is expected first
- What to say next: "A missing popup usually means the transaction cannot start yet. Please check source-chain ETH for gas and confirm the correct wallet and network are selected."

## No source-chain gas

- Likely cause: insufficient ETH on the source chain
- What to verify: ETH balance on the source chain, not only the token being bridged
- What to say next: "You need enough source-chain ETH for gas before the bridge can submit. Without it, the transaction may not prompt or may fail."

## First-time ERC-20 approval

- Likely cause: token allowance has not yet been granted
- What to verify: whether the UI prompted an approval before the deposit
- What to say next: "That is normal for many first-time ERC-20 deposits. Approval and deposit are separate transactions."

## Approval succeeded but deposit did not

- Likely cause: approval completed, but the deposit transaction was not submitted or failed
- What to verify: whether a separate deposit hash exists, bridge UI status, source-chain gas balance
- What to say next: "Approval alone does not move funds. If there is no deposit transaction hash, the deposit likely still needs to be submitted."

## Deposit appears delayed

- Likely cause: normal congestion, wrong destination network, or pending finalization
- What to verify: transaction hash, elapsed time, destination network selection
- What to say next: "Deposits commonly take about 15-30 minutes. If you are still within that window, some delay can be normal. Also check the destination network."

## Withdrawal appears stuck

- Likely cause: normal 7-8 day waiting period, or checking before claim is available
- What to verify: withdrawal initiation time, countdown status, transaction hash
- What to say next: "Official withdrawals to Ethereum are not immediate. A multi-day countdown is expected before the claim step becomes available."

## Claim button unavailable

- Likely cause: countdown not finished, wrong network, wrong account, or missing address control
- What to verify: countdown status, selected network, connected address, withdrawal hash
- What to say next: "If the countdown has not reached zero yet, the claim button can remain unavailable. Once it finishes, reconnect on the parent-network side and try again."

## User wants to cancel a withdrawal

- Likely cause: misunderstanding of official bridge behavior
- What to verify: whether the withdrawal was already initiated
- What to say next: "Official Arbitrum withdrawals cannot be canceled once initiated."

## User wants instant official withdrawal

- Likely cause: expectation mismatch
- What to verify: whether they specifically want the official bridge path
- What to say next: "The official bridge does not provide instant withdrawals to Ethereum. The normal official path is withdrawal, wait, then claim."

## Smart contract wallet user

- Likely cause: wallet type has limited support
- What to verify: wallet type and whether the asset is ETH or an ERC-20 token
- What to say next: "Smart contract wallet support is limited. ETH deposits and ETH withdrawals are not supported there."

## Cannot claim with current L1 wallet

- Likely cause: the needed initiating address is not controlled in the current setup
- What to verify: which address initiated the withdrawal and whether the user controls it on L1
- What to say next: "Do not assume any L1 address can claim. If you do not control the initiating address, the standard direct claim flow may not work."

## User wants One <-> Nova in one step

- Likely cause: misunderstanding of the official route
- What to verify: source chain, destination chain, and whether they require the official bridge
- What to say next: "The official bridge route is not direct between One and Nova. The supported path is withdraw to Ethereum, wait and claim, then deposit to the other Arbitrum chain."

## User is confused about USDC vs USDC.e

- Likely cause: both assets exist on Arbitrum One and are easy to conflate
- What to verify: token symbol shown in the wallet or UI, and the asset currently held
- What to say next: "On Arbitrum One, `USDC` and `USDC.e` are distinct assets. We need to confirm which one you mean before giving route-specific guidance."

## Testnet route not showing

- Likely cause: wrong parent testnet or wrong network context
- What to verify: exact parent testnet and displayed destination options
- What to say next: "Arbitrum testnets only appear when the matching parent testnet is selected."

## User checking on wrong network

- Likely cause: checking source-chain state instead of destination-chain or claim-chain state
- What to verify: current wallet network and what result the user expects to see
- What to say next: "Switch to the destination network to check deposit results, or to the parent-network side when checking claim readiness."
