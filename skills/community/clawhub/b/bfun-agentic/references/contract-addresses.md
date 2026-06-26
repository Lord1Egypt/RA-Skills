# Contract Addresses (BSC Mainnet)

These addresses are from the current repo sources. Use this file as a human reference only. Runtime calls use the CLI's built-in address selection.

## Core contracts

| Contract | Address |
|----------|---------|
| `bFunFactory` | `0x718Fa87734Cc6fCe3e7374663a0DAfa334aa4876` |
| `bFunFactoryImpl` | `0xf67BA0688aCb514AD3D5adE4AE140a2e8478C407` |
| `bFunFactoryTradeHelper` | `0x164319437119132bbf8b3bEe180c669ad450e817` |
| `bondingCurveImpl` | `0x7Bd40ef58c5D8Fe2ee97851Dd3b18956b5087F2B` |
| `bFunTokenSwap` | `0x569242A5269eFd635654214253dbE498B2eDb9eC` |
| `bFunTokenImplementation` | `0x84882b87929Eb8c62CD05658327B688cba789E31` |
| `bFunTaxTokenImplementation` | `0x91589835927D2133b8B18f71537A9bF06d7629AD` |
| `splitVaultFactory` | `0xB2935b344417e6240C380235262FA65e15746375` |
| `snowBallVaultFactory` | `0x68C082cC36ee2166CF2dd7D82f8AcfF36331Fd54` |
| `burnDividendVaultFactory` | `0xD4cDe006422348D1c62db86ade854FECA4eA77D2` |
| `giftVaultFactory` | `0xA158E4F7271441A4bD2181389153AC8B2b931e16` |
| `vaultKeeper` | `0x1f7f8a8963DF54E4bFC1315882ae517018CBB64a` |

## Chain config

| Field | Value |
|-------|-------|
| `UNISWAP_V2_ROUTER` | `0x10ED43C718714eb63d5aA57B78B54704E256024E` |
| `WETH` | `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` |
| `VAULT_KEEPER` | `0x1f7f8a8963DF54E4bFC1315882ae517018CBB64a` |
| `TARGET_COLLECTION_AMOUNT` | `12000000000000000000` |
| `VIRTUAL_COLLATERAL_RESERVES` | `4347826086956521739` |
| `FEE_BASIS_POINTS` | `100` |
| `FIRST_BUY_FEE` | `8000000000000000` |

## Collateral templates

| Pair | Token address | Decimals |
|------|---------------|----------|
| `ETH` | `0x0000000000000000000000000000000000000000` | 18 |
| `CAKE` | `0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82` | 18 |
| `USDT` | `0x55d398326f99059fF775485246999027B3197955` | 18 |
| `USD1` | `0x8d0D000Ee44948FC98c9B98A4FA4921476f08B0d` | 18 |
| `ASTER` | `0x000Ae314E2A2172a039B26378814C252734f556A` | 18 |
| `U` | `0xcE24439F2D9C6a2289F741120FE202248B666666` | 18 |
| `USDC` | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` | 18 |

## Notes

- Default chain is BSC mainnet (56).
- Native `ETH` in CLI flags means the BNB-native collateral path on BSC.
