import type { Address } from "viem"

// FlapSkill 合约（BSC mainnet）— 自动路由内盘(Portal)/外盘(PancakeSwap V2/V3)
export const FLAP_SKILL_ADDRESS = "0x03a9aeeb4f6e64d425126164f7262c2a754b3ff9" as Address

// USDT (BSC)
export const USDT_ADDRESS = "0x55d398326f99059fF775485246999027B3197955" as Address

// FLAP Portal — 查询代币状态
export const PORTAL_ADDRESS = "0xe2cE6ab80874Fa9Fa2aAE65D277Dd6B8e65C9De0" as Address

// FOMO 代币地址
export const FOMO_TOKEN = {
  mainnet: "0x13f26659398d7280737ffc9aba3d4f3cf53b7777" as Address,
  testnet: "0x57e3a4fd1fe7f837535ea3b86026916f8c7d5d46" as Address,
} as const

// FlapSkill ABI — buyTokens / sellTokens / sellTokensByPercent
export const FLAP_SKILL_ABI = [
  {
    inputs: [
      { internalType: "address", name: "_token", type: "address" },
      { internalType: "uint256", name: "_usdtAmount", type: "uint256" },
    ],
    name: "buyTokens",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [
      { internalType: "address", name: "_token", type: "address" },
      { internalType: "uint256", name: "_tokenAmount", type: "uint256" },
    ],
    name: "sellTokens",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [
      { internalType: "address", name: "_token", type: "address" },
      { internalType: "uint256", name: "_percentBps", type: "uint256" },
    ],
    name: "sellTokensByPercent",
    outputs: [{ internalType: "uint256", name: "", type: "uint256" }],
    stateMutability: "nonpayable",
    type: "function",
  },
] as const

// Portal ABI — getTokenV6 查询代币状态
// TokenStatus: 0=NotCreated, 1=Tradable(内盘), 2=DEX(外盘), 3=Locked
export const PORTAL_ABI = [
  {
    inputs: [{ internalType: "address", name: "_token", type: "address" }],
    name: "getTokenV6",
    outputs: [
      {
        components: [
          { internalType: "uint8", name: "status", type: "uint8" },
          { internalType: "address", name: "quoteToken", type: "address" },
          { internalType: "uint256", name: "currentPrice", type: "uint256" },
          { internalType: "uint256", name: "totalSupply", type: "uint256" },
          { internalType: "uint256", name: "reserveBalance", type: "uint256" },
          { internalType: "uint256", name: "progress", type: "uint256" },
        ],
        internalType: "struct TokenStateV6",
        name: "",
        type: "tuple",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
] as const

// 代币状态枚举
export const TOKEN_STATUS = {
  0: "NotCreated",
  1: "Tradable",   // 内盘（Portal bonding curve）
  2: "DEX",        // 外盘（已毕业到 PancakeSwap）
  3: "Locked",
} as const

export type TokenStatusCode = keyof typeof TOKEN_STATUS
