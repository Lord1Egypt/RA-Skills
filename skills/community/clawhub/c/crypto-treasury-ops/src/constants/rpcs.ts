import type { ChainName } from "../types.js";

export const DEFAULT_EVM_RPC_URLS: Record<ChainName, string[]> = {
  ethereum: [
    "https://ethereum-rpc.publicnode.com",
    "https://eth.llamarpc.com",
    "https://cloudflare-eth.com"
  ],
  polygon: [
    "https://polygon-rpc.com",
    "https://polygon-bor-rpc.publicnode.com",
    "https://polygon.llamarpc.com"
  ],
  arbitrum: [
    "https://arb1.arbitrum.io/rpc",
    "https://arbitrum-one-rpc.publicnode.com",
    "https://arbitrum.llamarpc.com"
  ],
  base: [
    "https://mainnet.base.org",
    "https://base.llamarpc.com",
    "https://base-rpc.publicnode.com"
  ]
};

export const DEFAULT_SOLANA_RPC_URLS: string[] = [
  "https://solana.drpc.org",
  "https://api.mainnet-beta.solana.com",
  "https://solana-rpc.publicnode.com"
];
