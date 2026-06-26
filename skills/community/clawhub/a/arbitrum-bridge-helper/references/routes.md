# Routes Reference

Use this reference when the user needs route clarification, timing expectations,
claim guidance, or edge-case handling for a specific chain pair.

## Core route rules

- Parent chain -> child chain = deposit flow
- Child chain -> parent chain = withdrawal flow
- Ethereum -> Arbitrum One or Arbitrum Nova = deposit
- Arbitrum One or Arbitrum Nova -> Ethereum = withdrawal
- Arbitrum One <-> Arbitrum Nova is not a direct one-step official bridge move

## Official One <-> Nova route

When the user wants to move assets between Arbitrum One and Arbitrum Nova
through the official bridge, explain the real route:

1. Withdraw from the source Arbitrum chain to Ethereum
2. Wait about 7-8 days for the withdrawal to become claimable
3. Claim on Ethereum
4. Deposit from Ethereum to the other Arbitrum chain

Do not describe this as a single-hop official transfer.

## Timing expectations

- Deposits generally arrive in about 15-30 minutes, depending on congestion
- Withdrawals from Arbitrum One or Nova to Ethereum generally require about 7-8 days
- Withdrawals are not complete until the later claim step is performed

## ERC-20 deposit note

For L1 -> L2 ERC-20 deposits, the user may need:

1. Approval transaction
2. Deposit transaction

Approval alone does not move funds.

## Network visibility and checking results

- Tell users to switch to the destination network to check for deposited funds
- Tell users to switch to the parent-network side to claim completed withdrawals
- Testnets such as Arbitrum Sepolia only appear when the correct parent testnet is selected

## Wallet support limits

- EOA wallets are the standard supported path
- Smart contract wallets have limited support
- ETH deposits and ETH withdrawals are not supported for smart contract wallets
- Token deposits and withdrawals may be supported for smart contract wallets

## Address-control note for claims

Do not assume the user controls the same address on both sides.

If the user does not control the initiating address needed on L1 for a withdrawal
claim, say that the normal claim path may not work and that they may need the
Arbitrum cross-chain dashboard flow.

## USDC on Arbitrum One

Before giving USDC guidance on Arbitrum One, resolve:

- `USDC` = native USDC
- `USDC.e` = bridged USDC

Do not treat them as the same asset.
