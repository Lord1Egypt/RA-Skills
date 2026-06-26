// ClawPurse configuration for Neutaro (Timpi) chain

export const NEUTARO_CONFIG = {
  chainId: 'Neutaro-1',
  rpcEndpoint: 'https://rpc2.neutaro.io',
  restEndpoint: 'https://api2.neutaro.io',
  
  // Native token
  denom: 'uneutaro',
  displayDenom: 'NTMPI',
  decimals: 6,
  
  // Gas settings
  gasPrice: '0.025uneutaro',
  defaultGasLimit: 200000,
  
  // Address prefix
  bech32Prefix: 'neutaro',
} as const;

export const KEYSTORE_CONFIG = {
  // Default keystore location
  defaultPath: '.clawpurse/keystore.enc',
  
  // Encryption settings (scrypt - balanced security/performance)
  scryptN: 2 ** 14, // 16384 - secure but fast enough
  scryptR: 8,
  scryptP: 1,
  
  // Safety defaults
  maxSendAmount: 1000_000000, // 1000 NTMPI in micro units
  requireConfirmAbove: 100_000000, // 100 NTMPI
} as const;

export const CLI_CONFIG = {
  name: 'clawpurse',
  version: '2.0.0',
  description: 'Local Timpi/NTMPI wallet for agentic AI, automation, and individuals',
} as const;
