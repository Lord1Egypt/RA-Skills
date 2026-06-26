/**
 * Economics Types
 * 
 * Core type definitions for the AlephNet economics layer.
 */

import { LockPeriod, StakingTier } from '../../common/types';

export interface WalletBalance {
  total: bigint;
  available: bigint;
  staked: bigint;
  pendingUnstake: bigint;
  reserved: bigint;
  unclaimedRewards: bigint;
  stakingTier: StakingTier;
  updatedAt: number;
}

export interface TransactionReceipt {
  transactionId: string;
  status: 'PENDING' | 'CONFIRMED' | 'FAILED';
  timestamp: number;
  error?: string;
}

export interface StakeReceipt {
  stakeId: string;
  amount: bigint;
  lockPeriod: LockPeriod;
  lockEndsAt: number;
  newTier: StakingTier;
  transactionId: string;
}

export interface UnstakeReceipt {
  stakeId: string;
  amount: bigint;
  releaseDate: number;
  transactionId: string;
}

export interface RewardReceipt {
  amount: bigint;
  transactionId: string;
  timestamp: number;
}

export interface PaymentAuthorization {
  id: string;
  from: string;
  to: string;
  maxAmount: bigint;
  purpose: any;
  status: 'PENDING' | 'FINALIZED' | 'CANCELLED' | 'EXPIRED';
  createdAt: number;
  expiresAt: number;
  finalizedAmount?: bigint;
  transactionId?: string;
}

export type TransactionType = 
  | 'TRANSFER'
  | 'STAKE'
  | 'UNSTAKE'
  | 'REWARD_CLAIM'
  | 'SERVICE_PAYMENT'
  | 'SUBSCRIPTION'
  | 'COHERENCE_STAKE'
  | 'COHERENCE_REWARD'
  | 'TIP'
  | 'NETWORK_FEE';

export interface Transaction {
  id: string;
  type: TransactionType;
  from: string;
  to: string;
  amount: bigint;
  fee: bigint;
  timestamp: number;
  purpose?: any;
  memo?: string;
  status: 'PENDING' | 'CONFIRMED' | 'FAILED';
  signature?: string;
}

export interface StakeRecord {
  id: string;
  owner: string;
  amount: bigint;
  lockPeriod: LockPeriod;
  lockedUntil: number;
  createdAt: number;
  lastRewardClaim: number;
  status: 'ACTIVE' | 'UNSTAKING' | 'UNSTAKED';
}

export const LOCK_MULTIPLIERS: Record<LockPeriod, number> = {
  '7d': 1.0,
  '30d': 1.1,
  '90d': 1.25,
  '180d': 1.5,
  '365d': 2.0
};

export const BASE_APY = 0.05; // 5% base APY
