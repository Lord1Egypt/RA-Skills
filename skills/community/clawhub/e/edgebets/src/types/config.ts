import type { Keypair, PublicKey, Transaction, VersionedTransaction } from '@solana/web3.js';

/**
 * Wallet adapter interface for signing transactions
 * Compatible with @solana/wallet-adapter-base
 */
export interface WalletAdapter {
  /** Wallet public key */
  publicKey: PublicKey;
  /** Sign a single transaction */
  signTransaction<T extends Transaction | VersionedTransaction>(transaction: T): Promise<T>;
  /** Sign multiple transactions (optional) */
  signAllTransactions?<T extends Transaction | VersionedTransaction>(transactions: T[]): Promise<T[]>;
}

/**
 * SDK configuration options
 */
export interface EdgeBetsConfig {
  /**
   * Solana wallet for signing payments
   * Can be a Keypair or a wallet adapter
   */
  wallet?: WalletAdapter | Keypair;

  /**
   * Solana RPC endpoint
   * @default "https://api.mainnet-beta.solana.com"
   */
  rpcEndpoint?: string;

  /**
   * EdgeBets API base URL
   * @default "https://api.edgebets.fun/api/v1"
   */
  apiBaseUrl?: string;

  /**
   * Polling interval for simulation results (ms)
   * @default 3000
   */
  pollingInterval?: number;

  /**
   * Polling timeout (ms)
   * @default 120000
   */
  pollingTimeout?: number;

  /**
   * Enable debug logging
   * @default false
   */
  debug?: boolean;

  /**
   * Maximum concurrent simulations
   * @default 1
   */
  maxConcurrent?: number;

  /**
   * Minimum delay between requests in ms
   * @default 2000
   */
  delayBetween?: number;
}

/**
 * Internal resolved configuration
 */
export interface ResolvedConfig {
  wallet: WalletAdapter | Keypair | null;
  rpcEndpoint: string;
  apiBaseUrl: string;
  pollingInterval: number;
  pollingTimeout: number;
  debug: boolean;
  maxConcurrent: number;
  delayBetween: number;
}

/**
 * Balance check result
 */
export interface BalanceResult {
  /** USDC balance in human-readable units */
  usdc: number;
  /** SOL balance for transaction fees */
  sol: number;
  /** Whether balance is sufficient for a simulation ($0.50) */
  sufficient: boolean;
}
