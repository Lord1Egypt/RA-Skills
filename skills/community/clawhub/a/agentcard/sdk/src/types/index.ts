/**
 * @asgcard/sdk — type definitions
 * x402 payment protocol on Stellar (Soroban SAC USDC)
 */

// ── Wallet Adapter ───────────────────────────────────────

/** Adapter for external wallet signing (e.g. browser extension) */
export interface WalletAdapter {
  /** Stellar public key (G...) */
  publicKey: string;
  /** Sign a Stellar XDR transaction envelope, return signed XDR */
  signTransaction(transactionXDR: string, networkPassphrase: string): Promise<string>;
}

// ── Client Config ────────────────────────────────────────

export interface ASGCardClientConfig {
  /** Stellar secret key (S...) — provide either this or walletAdapter */
  privateKey?: string;
  /** External wallet adapter — provide either this or privateKey */
  walletAdapter?: WalletAdapter;
  /** API base URL (default: https://api.asgcard.dev) */
  baseUrl?: string;
  /** Soroban RPC URL (default: https://mainnet.sorobanrpc.com) */
  rpcUrl?: string;
  /** Horizon URL (default: https://horizon.stellar.org) */
  horizonUrl?: string;
  /** Request timeout in ms (default: 60000) */
  timeout?: number;
}

// ── Card Operations ──────────────────────────────────────

export interface CreateCardParams {
  amount: 10 | 25 | 50 | 100 | 200 | 500;
  nameOnCard: string;
  email: string;
}

export interface FundCardParams {
  amount: 10 | 25 | 50 | 100 | 200 | 500;
  cardId: string;
}

// ── Tier Catalog ─────────────────────────────────────────

export interface TierEntry {
  loadAmount?: number;
  fundAmount?: number;
  totalCost: number;
  endpoint: string;
  breakdown?: Record<string, number>;
}

export interface TierResponse {
  creation: TierEntry[];
  funding: TierEntry[];
}

// ── Card Result ──────────────────────────────────────────

export interface BillingAddress {
  street: string;
  city: string;
  state: string;
  zip: string;
  country: string;
}

export interface SensitiveCardDetails {
  cardNumber: string;
  expiryMonth: number;
  expiryYear: number;
  cvv: string;
  billingAddress: BillingAddress;
}

export interface CardResult {
  success: boolean;
  card: {
    cardId: string;
    nameOnCard: string;
    balance: number;
    status: string;
    createdAt: string;
  };
  payment: {
    amountCharged: number;
    txHash: string;
    network: string;
  };
  /** Sensitive card details (agent-first model, one-time access on create) */
  detailsEnvelope?: {
    cardNumber: string;
    expiryMonth: number;
    expiryYear: number;
    cvv: string;
    billingAddress: BillingAddress;
    oneTimeAccess: boolean;
    expiresInSeconds: number;
  };
}

export interface FundResult {
  success: boolean;
  cardId: string;
  fundedAmount: number;
  newBalance: number;
  payment: {
    amountCharged: number;
    txHash: string;
    network: string;
  };
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

// ── x402 Types ───────────────────────────────────────────

export interface X402Accept {
  scheme: "exact";
  network: string;
  asset: string;
  amount: string;
  payTo: string;
  maxTimeoutSeconds: number;
  extra?: {
    areFeesSponsored?: boolean;
    [key: string]: unknown;
  };
}

export interface X402Challenge {
  x402Version: 2;
  accepts: X402Accept[];
  resource?: {
    url: string;
    description: string;
    mimeType: string;
  };
}

export interface X402PaymentPayload {
  x402Version: 2;
  accepted: X402Accept;
  payload: {
    transaction: string;
  };
}
