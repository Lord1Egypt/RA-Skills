# Clicks Protocol — Contract Reference

## Base Mainnet (Chain ID 8453)

| Contract | Address | Basescan |
|----------|---------|----------|
| ClicksRegistry | `0x23bb0Ea69b2BD2e527D5DbA6093155A6E1D0C0a3` | [View](https://basescan.org/address/0x23bb0Ea69b2BD2e527D5DbA6093155A6E1D0C0a3) |
| ClicksFeeV2 | `0x8C4E07bBF0BDc3949eA133D636601D8ba17e0fb5` | [View](https://basescan.org/address/0x8C4E07bBF0BDc3949eA133D636601D8ba17e0fb5) |
| ClicksYieldRouter | `0x053167a233d18E05Bc65a8d5F3F8808782a3EECD` | [View](https://basescan.org/address/0x053167a233d18E05Bc65a8d5F3F8808782a3EECD) |
| ClicksSplitterV4 | `0xB7E0016d543bD443ED2A6f23d5008400255bf3C8` | [View](https://basescan.org/address/0xB7E0016d543bD443ED2A6f23d5008400255bf3C8) |
| ClicksReferral | `0x1E5Ab896D3b3A542C5E91852e221b2D849944ccC` | [View](https://basescan.org/address/0x1E5Ab896D3b3A542C5E91852e221b2D849944ccC) |
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | [View](https://basescan.org/address/0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913) |

## Yield Sources

| Protocol | Current APY | Market |
|----------|------------|--------|
| Aave V3 | ~2.3% | USDC Supply |
| Morpho Blue | ~13.4% | cbBTC/USDC (89% utilization) |

Router automatically selects the highest APY.

## SDK Quick Reference

```typescript
import { ClicksClient } from '@clicks-protocol/sdk';

// Read-only (no signer needed)
const clicks = new ClicksClient(provider);
await clicks.getAgentInfo(address);
await clicks.simulateSplit('1000', address);
await clicks.getYieldInfo();

// Write (needs signer with USDC)
const clicks = new ClicksClient(signer);
await clicks.quickStart('1000', agentAddress);
await clicks.receivePayment('500', agentAddress);
await clicks.withdrawYield(agentAddress);
```

## Fee Model
- 2% on yield earned (never on principal)
- Referral: 40% L1, 20% L2, 10% L3 of protocol fee
- Referred agent pays nothing extra
