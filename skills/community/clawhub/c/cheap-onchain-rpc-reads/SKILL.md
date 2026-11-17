---
name: cheap-onchain-rpc-reads
description: >-
  Cheap, keyless on-chain reads for agents — native + ERC-20 balances, gas price,
  transaction status, token supply, ENS, nonce, across Base, Ethereum, Optimism,
  Arbitrum, Polygon. Use whenever an agent needs to read chain state without running
  a node or juggling RPC keys: check a wallet balance, current gas, whether a tx
  confirmed, a token's supply. ~$0.001/call, USDC on Base via x402, no API key, no signup.
metadata:
  tags: [onchain, rpc, base, ethereum, balance, gas, web3, blockchain, x402, agent-tools]
---
# Cheap On-chain RPC Reads (x402, ~$0.001/call)

Read chain state without a node or an RPC key. Each is one authenticated GET that settles ~$0.001 USDC on Base via your x402 client.
```
GET https://store.agentexchange.work/chain/balance?address=0x...&chain=base
GET https://store.agentexchange.work/chain/gas?chain=base
GET https://store.agentexchange.work/chain/tx?hash=0x...&chain=base
GET https://store.agentexchange.work/chain/ens?name=vitalik.eth
```
Chains: base | ethereum | optimism | arbitrum | polygon. Free sample: GET https://store.agentexchange.work/samples. Price shown in the 402 before you pay.
