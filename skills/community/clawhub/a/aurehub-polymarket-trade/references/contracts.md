# Polygon Contract Addresses

## USDC.e (Bridged USDC)

```
0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174
```
[Polygonscan](https://polygonscan.com/address/0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174)

## CTF Exchange (Standard Markets)

```
0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E
```
[Polygonscan](https://polygonscan.com/address/0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E)

Used for: BUY approval target (non-neg_risk markets); SELL `setApprovalForAll` operator (non-neg_risk markets)

## Neg Risk Exchange

```
0xC5d563A36AE78145C45a50134d48A1215220f80a
```
[Polygonscan](https://polygonscan.com/address/0xC5d563A36AE78145C45a50134d48A1215220f80a)

Used for: BUY approval target (neg_risk markets); SELL `setApprovalForAll` operator (neg_risk markets)

## CTF Contract (ERC-1155 Conditional Tokens)

```
0x4D97DCd97eC945f40cF65F87097ACe5EA0476045
```
[Polygonscan](https://polygonscan.com/address/0x4D97DCd97eC945f40cF65F87097ACe5EA0476045)

Used for: checking YES/NO share balances (`balanceOf(address, tokenId)`)

## Approval Pattern

**For BUY (non-neg_risk):** `usdc_e.approve(ctf_exchange, exactAmount)` — exact USDC.e, not MaxUint256

**For BUY (neg_risk):** `usdc_e.approve(neg_risk_exchange, exactAmount)`

**For SELL (non-neg_risk):** `ctf_contract.setApprovalForAll(ctf_exchange, true)`

**For SELL (neg_risk):** `ctf_contract.setApprovalForAll(neg_risk_exchange, true)`
