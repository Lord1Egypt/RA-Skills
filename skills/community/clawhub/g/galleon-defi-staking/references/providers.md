# Staking providers and exit mechanics

Primary-source review: **2026-09-05**. Interfaces below are documented by their providers; this package does not claim a live signer, MCP or transaction test. No dedicated retail agent MCP was established for these four providers. Use maintained SDKs and exact deployed contracts rather than inventing adapters or installing community servers automatically.

| Provider | Official integration | Identity and access boundary |
| --- | --- | --- |
| Lido | `@lidofinance/lido-ethereum-sdk`, LidoLocator and withdrawal contracts | Ethereum stake/wrap/queue; bridged receipt tokens are not automatically redeemable on that chain |
| Rocket Pool | Official contracts; Smartnode for operators | Retail rETH acquisition/burn differs from validator/node operation |
| EigenLayer | Restaker contract guides and versioned core contracts | LST restaking differs from native EigenPod/validator withdrawal credentials |
| Symbiotic | Core vault, delegator, slasher interfaces | Vault collateral, curator, epoch, access and network/operator choices determine risk |

## Lido

[SDKs and UI libraries - Lido](https://docs.lido.fi/integrations/sdk/) links the maintained Ethereum TypeScript SDK. Read SDK network support and use a public client for research; a wallet client is unnecessary for balance reads. Validate chain ID independently of copied examples.

[Token integration guide - Lido](https://docs.lido.fi/guides/lido-tokens-integration-guide/) explains rebasing stETH and wrapped-token accounting. A fixed wstETH balance can represent changing stETH value; do not report zero yield solely from token count.

[WithdrawalQueueERC721 - Lido](https://docs.lido.fi/contracts/withdrawal-queue-erc721/) is a request/finalize/claim FIFO queue. An `unstETH` NFT conveys the claim; transferring it changes the owner entitled to claim. Queued tokens stop earning rewards, but retain loss exposure before finalization. Read current request bounds, pause state, finalization and ownership. An NFT/request receipt does not prove ETH arrived; verify claim and recipient balance separately. A DEX swap exits at market price and liquidity, not at the queue's exchange terms.

## Rocket Pool

[RocketTokenRETH source - Rocket Pool](https://raw.githubusercontent.com/rocket-pool/rocketpool/master/contracts/contract/token/RocketTokenRETH.sol) illustrates `getEthValue`, exchange-rate and available-collateral reads plus liquidity-checked `burn`. Verify the current deployed implementation before relying on source behavior. Exchange value is variable ETH per rETH, not 1:1; protocol redemption requires available ETH. A secondary-market discount is not the protocol's accounting rate.

[Smartnode CLI introduction - Rocket Pool](https://docs.rocketpool.net/node-staking/cli-intro) is for operating validators/nodes. Do not require Smartnode for a retail LST workflow or silently create node duties. [Official documentation source - Rocket Pool](https://github.com/rocket-pool/docs.rocketpool.net) is a fallback because some public liquid-staking routes returned only a generic landing page during this review. That retrieval gap is not evidence a feature is unavailable.

## EigenLayer / EigenCloud

[Restaking developer guide - Eigen Labs](https://docs.eigencloud.xyz/eigenlayer/restakers/restaking-guides/restaking-developer-guide) supplies direct contract integration. Inspect the release/deployment and slashing model; do not reuse an old contract ABI solely because the address label matches.

[Unstake and Withdraw - Eigen Labs](https://docs.eigencloud.xyz/eigenlayer/restakers/restaking-guides/restaking-user-guide/liquid-restaking/withdraw-from-eigenlayer) distinguishes queueing/escrow from final transfer. [Withdrawal Delay - Eigen Labs](https://docs.eigencloud.xyz/eigenlayer/security/withdrawal-delay) documents pause/upgrade and escrow boundaries. Official historical sources have used different delays and an escrow link resolved to a testnet page in this review. Read current deployed delay and request eligibility rather than embedding 7, 14 or 17.5 days as a universal rule.

[Slashing for stakers - Eigen Labs](https://blog.eigencloud.xyz/intro-to-slashing-on-eigenlayer-stakers-edition/) explains operator allocations and slashable operator sets. Monitor allocation changes and current safety-delay parameters; a new deposit may join existing exposure. Native restaking includes validator exits, proof/checkpoint steps and EigenPod withdrawal credentials, which are outside ordinary LST-only consent.

## Symbiotic

[Accounting - Symbiotic](https://docs.symbiotic.fi/modules/vault/accounting) describes active balances, queued withdrawals, curator management and optional deposit access controls. Total slashable balance, active stake and claimable withdrawals are different quantities.

[Epochs and Delays - Symbiotic](https://docs.symbiotic.fi/learn/mechanics/epochs-and-delays): request in epoch `k` becomes claimable after epoch `k+1` ends, producing a delay in `[E, 2E)`. Queued funds remain slashable until that boundary. Read the vault's actual epoch duration and state, including later configuration changes; don't promise one epoch from request time.

[Network - Symbiotic](https://docs.symbiotic.fi/learn/core-concepts/network) explains captures, operator/network opt-ins and allocations. Check delegator, slasher/veto/resolver configuration, rewards and curator permissions. Symbiotic's Relay SDK is network-security middleware, not the Relay cross-chain trading provider or a retail staking SDK.
