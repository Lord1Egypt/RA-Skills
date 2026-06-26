import type { TierAmount } from "./domain";

export interface PaymentContext {
  payer: string;
  txHash: string;
  atomicAmount: string;
  tierAmount: TierAmount;
  totalCostUsd: number;
}

export interface WalletContext {
  address: string;
  timestamp: number;
}
