import { readFileSync, writeFileSync, existsSync } from "fs"
import { resolve, dirname } from "path"
import { fileURLToPath } from "url"
import type { Address } from "viem"

const __dirname = dirname(fileURLToPath(import.meta.url))
const ROOT = resolve(__dirname, "../..")
const CONFIG_PATH = resolve(ROOT, "config.json")

export interface Config {
  privateKey: string
  network: "testnet" | "mainnet"
  rpcUrl?: string
  fomo3dDiamond?: Address
  slotDiamond?: Address
}

function readConfigFile(): Partial<Config> | null {
  if (!existsSync(CONFIG_PATH)) return null
  try {
    return JSON.parse(readFileSync(CONFIG_PATH, "utf-8"))
  } catch {
    return null
  }
}

export function readConfig(): Config {
  const file = readConfigFile()
  return {
    privateKey: process.env.FOMO3D_PRIVATE_KEY ?? file?.privateKey ?? "",
    network: (process.env.FOMO3D_NETWORK as Config["network"]) ?? file?.network ?? "testnet",
    rpcUrl: process.env.FOMO3D_RPC_URL ?? file?.rpcUrl,
    fomo3dDiamond: file?.fomo3dDiamond,
    slotDiamond: file?.slotDiamond,
  }
}

export function writeConfig(config: Partial<Config>): void {
  const existing = readConfigFile() ?? {}
  const merged = { ...existing, ...config }
  writeFileSync(CONFIG_PATH, JSON.stringify(merged, null, 2) + "\n")
}

export function requirePrivateKey(config: Config): `0x${string}` {
  if (!config.privateKey) {
    console.error("No private key configured. Run: fomo3d setup")
    process.exit(1)
  }
  const key = config.privateKey.startsWith("0x") ? config.privateKey : `0x${config.privateKey}`
  return key as `0x${string}`
}

// 默认合约地址
export const ADDRESSES = {
  testnet: {
    fomo3dDiamond: "0x22E309c31Bed932afB505308434fB774cB2B23a6" as Address,
    slotDiamond: "0x007813509FA42B830db82C773f0Dd243fBEbF678" as Address,
    fomoToken: "0x57e3a4fd1fe7f837535ea3b86026916f8c7d5d46" as Address,
  },
  mainnet: {
    fomo3dDiamond: "0x062AfaBEA853178E58a038b808EDEA119fF5948b" as Address,
    slotDiamond: "0x6eB59fFEc7CC639DFF4238D09B99Ea4c9150156E" as Address,
    fomoToken: "0x13f26659398d7280737ffc9aba3d4f3cf53b7777" as Address,
  },
} as const

export const RPC_URLS = {
  testnet: "https://bsc-testnet-rpc.publicnode.com",
  mainnet: "https://bsc-rpc.publicnode.com",
} as const

export function getDiamondAddress(config: Config): Address {
  return config.fomo3dDiamond ?? ADDRESSES[config.network].fomo3dDiamond
}

export function getSlotDiamondAddress(config: Config): Address {
  return config.slotDiamond ?? ADDRESSES[config.network].slotDiamond
}
