export enum ChainId {
  BASE = "base",
  SKALE = "skale",
}

export interface ChainConfig {
  chainId: number;
  name: string;
  /**
   * Reference RPC URL for chain identification only.
   * The ClawTrust SDK never calls this URL directly.
   * All blockchain reads/writes go through https://clawtrust.org/api server-side.
   * This field is provided so developers can verify chain identity and connect
   * their own wallet providers (MetaMask, viem, ethers.js) to the correct network.
   */
  rpcUrl: string;
  blockExplorerUrl: string;
  contracts: {
    ClawCardNFT: string;
    /**
     * ERC-8004 Identity Registry for this chain.
     * Base Sepolia: ClawTrust's own identity registry (0xBeb8a61b...).
     * SKALE Base Sepolia: canonical global registry from erc-8004-contracts PR #56.
     */
    ERC8004IdentityRegistry: string;
    /**
     * ERC-8004 Reputation Registry for this chain.
     * Base Sepolia: ClawTrustRepAdapter serves this role (no standalone registry).
     * SKALE Base Sepolia: canonical global registry from erc-8004-contracts PR #56.
     */
    ERC8004ReputationRegistry: string;
    ClawTrustEscrow: string;
    ClawTrustRepAdapter: string;
    ClawTrustSwarmValidator: string;
    ClawTrustBond: string;
    ClawTrustCrew: string;
    ClawTrustRegistry: string;
    ClawTrustAC: string;
  };
  usdc: string;
}

/**
 * Base Sepolia (chainId 84532) — primary ClawTrust chain.
 *
 * NOTE: rpcUrl is reference metadata only. The SDK never calls it directly.
 * All API calls go through https://clawtrust.org/api server-side.
 */
export const BASE_CONFIG: ChainConfig = {
  chainId: 84532,
  name: "Base Sepolia",
  rpcUrl: "https://sepolia.base.org",
  blockExplorerUrl: "https://sepolia.basescan.org",
  contracts: {
    ClawCardNFT:                "0xf24e41980ed48576Eb379D2116C1AaD075B342C4",
    // ClawTrust ERC-8004 Identity Registry on Base Sepolia (not the SKALE canonical)
    ERC8004IdentityRegistry:    "0xBeb8a61b6bBc53934f1b89cE0cBa0c42830855CF",
    // Base Sepolia has no standalone ERC-8004 reputation registry;
    // ClawTrustRepAdapter fulfills this role.
    ERC8004ReputationRegistry:  "0xEfF3d3170e37998C7db987eFA628e7e56E1866DB",
    ClawTrustEscrow:            "0x6B676744B8c4900F9999E9a9323728C160706126",
    ClawTrustRepAdapter:        "0xEfF3d3170e37998C7db987eFA628e7e56E1866DB",
    ClawTrustSwarmValidator:    "0xb219ddb4a65934Cea396C606e7F6bcfBF2F68743",
    ClawTrustBond:              "0x23a1E1e958C932639906d0650A13283f6E60132c",
    ClawTrustCrew:              "0xFF9B75BD080F6D2FAe7Ffa500451716b78fde5F3",
    ClawTrustRegistry:          "0x82AEAA9921aC1408626851c90FCf74410D059dF4",
    ClawTrustAC:                "0x1933D67CDB911653765e84758f47c60A1E868bC0",
  },
  usdc: "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
};

/**
 * SKALE Base Sepolia (chainId 324705682) — zero gas, BITE encrypted, sub-second finality.
 * Deployed 2026-03-18 via scripts/deploy-skale-base.mjs.
 * ERC-8004 canonical addresses from erc-8004-contracts PR #56 (TheGreatAxios / Sawyer Cutler).
 *
 * NOTE: rpcUrl is reference metadata only. The SDK never calls it directly.
 * All API calls go through https://clawtrust.org/api server-side.
 */
export const SKALE_CONFIG: ChainConfig = {
  chainId: 324705682,
  name: "SKALE Base Sepolia",
  rpcUrl: "https://base-sepolia-testnet.skalenodes.com/v1/jubilant-horrible-ancha",
  blockExplorerUrl: "https://base-sepolia-testnet-explorer.skalenodes.com",
  contracts: {
    ClawCardNFT:                "0xdB7F6cCf57D6c6AA90ccCC1a510589513f28cb83",
    // Canonical global ERC-8004 identity registry from erc-8004-contracts PR #56
    ERC8004IdentityRegistry:    "0x8004A818BFB912233c491871b3d84c89A494BD9e",
    // Canonical global ERC-8004 reputation registry from erc-8004-contracts PR #56
    ERC8004ReputationRegistry:  "0x8004B663056A597Dffe9eCcC1965A193B7388713",
    ClawTrustEscrow:            "0x39601883CD9A115Aba0228fe0620f468Dc710d54",
    ClawTrustRepAdapter:        "0xFafCA23a7c085A842E827f53A853141C8243F924",
    ClawTrustSwarmValidator:    "0x7693a841Eec79Da879241BC0eCcc80710F39f399",
    ClawTrustBond:              "0x5bC40A7a47A2b767D948FEEc475b24c027B43867",
    ClawTrustCrew:              "0x00d02550f2a8Fd2CeCa0d6b7882f05Beead1E5d0",
    ClawTrustRegistry:          "0xED668f205eC9Ba9DA0c1D74B5866428b8e270084",
    ClawTrustAC:                "0x101F37D9bf445E92A237F8721CA7D12205D61Fe6",
  },
  usdc: "0x2e08028E3C4c2356572E096d8EF835cD5C6030bD",
};

const CHAIN_CONFIGS: Record<ChainId, ChainConfig> = {
  [ChainId.BASE]: BASE_CONFIG,
  [ChainId.SKALE]: SKALE_CONFIG,
};

const CHAIN_ID_MAP: Record<number, ChainId> = {
  [BASE_CONFIG.chainId]: ChainId.BASE,
  [SKALE_CONFIG.chainId]: ChainId.SKALE,
};

export function getChainConfig(chain: ChainId): ChainConfig {
  const config = CHAIN_CONFIGS[chain];
  if (!config) {
    throw new Error(`Unknown chain: ${chain}. Supported chains: ${Object.values(ChainId).join(", ")}`);
  }
  return config;
}

export function chainIdToChain(numericChainId: number): ChainId | undefined {
  return CHAIN_ID_MAP[numericChainId];
}

export function getSupportedChainIds(): number[] {
  return Object.keys(CHAIN_ID_MAP).map(Number);
}
