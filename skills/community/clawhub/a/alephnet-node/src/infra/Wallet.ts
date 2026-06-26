import { KeyTriplet } from '../core/types';
import * as crypto from 'crypto';
import { LockPeriod, StakingTier } from '../common/types';
import { 
  WalletBalance, 
  TransactionReceipt, 
  StakeReceipt, 
  UnstakeReceipt,
  RewardReceipt,
  PaymentAuthorization, 
  TransactionType, 
  Transaction,
  StakeRecord
} from '../core/economics/types';
import { RewardCalculator } from '../core/economics/RewardCalculator';

// --- Implementation ---

/**
 * AlephWallet - Client-side wallet for managing Aleph tokens
 */
export class AlephWallet {
  public readonly address: string;

  constructor(
    public readonly keyTriplet: KeyTriplet,
    private gun: any
  ) {
    // Address is derived from fingerprint (usually identical or hashed)
    this.address = keyTriplet.fingerprint;
  }

  // ... (existing methods)

  // ═══════════════════════════════════════════════════════════════
  // UNSTAKING & REWARDS
  // ═══════════════════════════════════════════════════════════════

  public async unstake(stakeId: string): Promise<UnstakeReceipt> {
    return new Promise((resolve, reject) => {
        this.gun.get('ledger').get('stakes').get(stakeId).once(async (stake: StakeRecord) => {
            if (!stake || stake.owner !== this.address) {
                reject(new Error('Stake not found or unauthorized'));
                return;
            }
            if (stake.status !== 'ACTIVE') {
                reject(new Error('Stake is not active'));
                return;
            }
            if (Date.now() < stake.lockedUntil) {
                reject(new Error('Stake is still locked'));
                return;
            }

            const now = Date.now();
            const txId = crypto.randomUUID();

            // Update stake status
            this.gun.get('ledger').get('stakes').get(stakeId).put({
                status: 'UNSTAKED',
                unstakedAt: now
            });

            // Return funds to available
            const balance = await this.getBalance();
            const amount = BigInt(stake.amount);
            
            const newAvailable = balance.available + amount;
            const newStaked = balance.staked - amount;
            const newTier = this.calculateTier(newStaked);

            this.gun.get('ledger').get('accounts').get(this.address).put({
                available: newAvailable.toString(),
                staked: newStaked.toString(),
                stakingTier: newTier,
                updatedAt: now
            });

            // Log Transaction
            this.gun.get('ledger').get('transactions').get(txId).put({
                id: txId,
                type: 'UNSTAKE',
                from: 'STAKING_CONTRACT',
                to: this.address,
                amount: amount.toString(),
                timestamp: now,
                status: 'CONFIRMED'
            });

            resolve({
                stakeId,
                amount,
                releaseDate: now,
                transactionId: txId
            });
        });
    });
  }

  public async claimRewards(stakeId: string): Promise<RewardReceipt> {
      return new Promise((resolve, reject) => {
          this.gun.get('ledger').get('stakes').get(stakeId).once(async (stake: StakeRecord) => {
              if (!stake || stake.owner !== this.address) {
                  reject(new Error('Stake not found or unauthorized'));
                  return;
              }
              if (stake.status !== 'ACTIVE') {
                  reject(new Error('Stake is not active'));
                  return;
              }

              const reward = RewardCalculator.calculateRewards(stake);
              if (reward <= 0n) {
                  reject(new Error('No rewards to claim'));
                  return;
              }

              const now = Date.now();
              const txId = crypto.randomUUID();

              // Update last claim time
              this.gun.get('ledger').get('stakes').get(stakeId).put({
                  lastRewardClaim: now
              });

              // Add rewards to available balance
              const balance = await this.getBalance();
              const newAvailable = balance.available + reward;
              const newUnclaimed = balance.unclaimedRewards - reward; // Assuming we tracked it separately? 
              // Or just mint new tokens? Design implies inflation/minting.
              // We'll assume minting for now.

              this.gun.get('ledger').get('accounts').get(this.address).put({
                  available: newAvailable.toString(),
                  // unclaimedRewards: newUnclaimed.toString(), // If we track pending rewards
                  updatedAt: now
              });

              // Log Transaction
              this.gun.get('ledger').get('transactions').get(txId).put({
                  id: txId,
                  type: 'REWARD_CLAIM',
                  from: 'REWARD_POOL',
                  to: this.address,
                  amount: reward.toString(),
                  timestamp: now,
                  status: 'CONFIRMED'
              });

              resolve({
                  amount: reward,
                  transactionId: txId,
                  timestamp: now
              });
          });
      });
  }

  // ═══════════════════════════════════════════════════════════════
  // BALANCE
  // ═══════════════════════════════════════════════════════════════

  public async getBalance(): Promise<WalletBalance> {
    return new Promise((resolve) => {
      this.gun.get('ledger').get('accounts').get(this.address).once((data: any) => {
        if (!data) {
          // Initialize empty account
          resolve(this.emptyBalance());
        } else {
          resolve({
            total: BigInt(data.total || '0'), // Derived usually
            available: BigInt(data.available || '0'),
            staked: BigInt(data.staked || '0'),
            pendingUnstake: BigInt(data.pendingUnstake || '0'),
            reserved: BigInt(data.reserved || '0'),
            unclaimedRewards: BigInt(data.unclaimedRewards || '0'),
            stakingTier: (data.stakingTier as StakingTier) || 'Neophyte',
            updatedAt: data.updatedAt || Date.now()
          });
        }
      });
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // TRANSFERS
  // ═══════════════════════════════════════════════════════════════

  public async transfer(
    to: string,
    amount: bigint,
    options?: { purpose?: any; memo?: string }
  ): Promise<TransactionReceipt> {
    const balance = await this.getBalance();
    if (balance.available < amount) {
      throw new Error('Insufficient funds');
    }

    const txId = crypto.randomUUID();
    const timestamp = Date.now();

    const transaction: any = {
      id: txId,
      type: 'TRANSFER',
      from: this.address,
      to,
      amount: amount.toString(),
      fee: '0', // Zero fee for now
      timestamp,
      purpose: options?.purpose,
      memo: options?.memo,
      status: 'CONFIRMED' // Optimistic confirmation
    };

    // Atomic-ish update (not real atomic in Gun)
    // 1. Write Transaction
    this.gun.get('ledger').get('transactions').get(txId).put(transaction);

    // 2. Update Sender Balance
    const newAvailable = balance.available - amount;
    this.gun.get('ledger').get('accounts').get(this.address).put({
      available: newAvailable.toString(),
      updatedAt: timestamp
    });

    // 3. Update Recipient Balance
    // We need to fetch recipient balance first to add safely, but for simplicity here we assume
    // a "delta" or trusted update. In real implementation, this runs on a node or uses CRDT counters.
    // Here we simulate the logic:
    this.gun.get('ledger').get('accounts').get(to).once((data: any) => {
        const current = data ? BigInt(data.available || '0') : 0n;
        this.gun.get('ledger').get('accounts').get(to).put({
            available: (current + amount).toString(),
            updatedAt: timestamp
        });
    });

    return {
      transactionId: txId,
      status: 'CONFIRMED',
      timestamp
    };
  }

  // ═══════════════════════════════════════════════════════════════
  // PAYMENTS (ESCROW)
  // ═══════════════════════════════════════════════════════════════

  public async authorizePayment(
    to: string,
    maxAmount: bigint,
    purpose: any,
    expiresIn: number = 60000
  ): Promise<PaymentAuthorization> {
    const balance = await this.getBalance();
    if (balance.available < maxAmount) {
        throw new Error('Insufficient funds for authorization');
    }

    const authId = crypto.randomUUID();
    const now = Date.now();
    const expiresAt = now + expiresIn;

    const auth: any = {
        id: authId,
        from: this.address,
        to,
        maxAmount: maxAmount.toString(),
        purpose,
        status: 'PENDING',
        createdAt: now,
        expiresAt
    };

    // Reserve funds
    const newAvailable = balance.available - maxAmount;
    const newReserved = balance.reserved + maxAmount;

    this.gun.get('ledger').get('authorizations').get(authId).put(auth);
    this.gun.get('ledger').get('accounts').get(this.address).put({
        available: newAvailable.toString(),
        reserved: newReserved.toString(),
        updatedAt: now
    });

    // Return object with bigint
    return {
        ...auth,
        maxAmount: maxAmount
    };
  }

  public async finalizePayment(
      authorizationId: string,
      actualAmount?: bigint
  ): Promise<TransactionReceipt> {
      // Fetch auth
      return new Promise((resolve, reject) => {
          this.gun.get('ledger').get('authorizations').get(authorizationId).once(async (authData: any) => {
              if (!authData || authData.status !== 'PENDING') {
                  reject(new Error('Invalid or expired authorization'));
                  return;
              }

              const maxAmount = BigInt(authData.maxAmount);
              const finalAmount = actualAmount !== undefined ? actualAmount : maxAmount;

              if (finalAmount > maxAmount) {
                  reject(new Error('Final amount exceeds authorized maximum'));
                  return;
              }

              const now = Date.now();
              const txId = crypto.randomUUID();

              // 1. Update Auth Status
              this.gun.get('ledger').get('authorizations').get(authorizationId).put({
                  status: 'FINALIZED',
                  finalizedAmount: finalAmount.toString(),
                  transactionId: txId
              });

              // 2. Create Transaction
              const transaction = {
                  id: txId,
                  type: 'SERVICE_PAYMENT',
                  from: authData.from,
                  to: authData.to,
                  amount: finalAmount.toString(),
                  fee: '0',
                  timestamp: now,
                  purpose: authData.purpose,
                  status: 'CONFIRMED'
              };
              this.gun.get('ledger').get('transactions').get(txId).put(transaction);

              // 3. Update Sender Balance (Reserved -> Spent + Refund)
              // We reserved `maxAmount`. We spend `finalAmount`. Refund `maxAmount - finalAmount` to available.
              const refund = maxAmount - finalAmount;
              
              // Need fresh balance?
              // Assuming single writer for this wallet for simplicity, or we use relative ops.
              const balance = await this.getBalance();
              
              const newReserved = balance.reserved - maxAmount;
              const newAvailable = balance.available + refund;
              
              this.gun.get('ledger').get('accounts').get(this.address).put({
                  reserved: newReserved.toString(),
                  available: newAvailable.toString(),
                  updatedAt: now
              });

              // 4. Update Recipient Balance
              this.gun.get('ledger').get('accounts').get(authData.to).once((data: any) => {
                  const current = data ? BigInt(data.available || '0') : 0n;
                  this.gun.get('ledger').get('accounts').get(authData.to).put({
                      available: (current + finalAmount).toString(),
                      updatedAt: now
                  });
              });

              resolve({
                  transactionId: txId,
                  status: 'CONFIRMED',
                  timestamp: now
              });
          });
      });
  }

  // ═══════════════════════════════════════════════════════════════
  // STAKING
  // ═══════════════════════════════════════════════════════════════

  public async stake(amount: bigint, lockPeriod: LockPeriod): Promise<StakeReceipt> {
      const balance = await this.getBalance();
      if (balance.available < amount) throw new Error('Insufficient funds');

      const stakeId = crypto.randomUUID();
      const now = Date.now();
      
      // Calculate lock end
      const days = parseInt(lockPeriod); // 7, 30, etc.
      const lockDuration = days * 24 * 60 * 60 * 1000;
      const lockEndsAt = now + lockDuration;

      // Create Stake
      const stakeRecord = {
          id: stakeId,
          owner: this.address,
          amount: amount.toString(),
          lockPeriod,
          lockedUntil: lockEndsAt,
          createdAt: now,
          rewards: '0'
      };

      this.gun.get('ledger').get('stakes').get(stakeId).put(stakeRecord);

      // Update Balance
      const newAvailable = balance.available - amount;
      const newStaked = balance.staked + amount;
      
      // Determine new tier
      const newTier = this.calculateTier(newStaked);

      this.gun.get('ledger').get('accounts').get(this.address).put({
          available: newAvailable.toString(),
          staked: newStaked.toString(),
          stakingTier: newTier,
          updatedAt: now
      });

      // Log Transaction
      const txId = crypto.randomUUID();
      this.gun.get('ledger').get('transactions').get(txId).put({
          id: txId,
          type: 'STAKE',
          from: this.address,
          to: 'STAKING_CONTRACT',
          amount: amount.toString(),
          timestamp: now,
          status: 'CONFIRMED'
      });

      return {
          stakeId,
          amount,
          lockPeriod,
          lockEndsAt,
          newTier,
          transactionId: txId
      };
  }

  // --- Helpers ---

  private emptyBalance(): WalletBalance {
    return {
      total: 0n,
      available: 0n,
      staked: 0n,
      pendingUnstake: 0n,
      reserved: 0n,
      unclaimedRewards: 0n,
      stakingTier: 'Neophyte',
      updatedAt: Date.now()
    };
  }

  private calculateTier(stakedAmount: bigint): StakingTier {
      // 100, 1000, 10000 (assumed decimals handled by caller or units)
      // Assuming 18 decimals, 100 tokens = 100 * 10^18
      const E18 = 1000000000000000000n;
      if (stakedAmount >= 10000n * E18) return 'Archon';
      if (stakedAmount >= 1000n * E18) return 'Magus';
      if (stakedAmount >= 100n * E18) return 'Adept';
      return 'Neophyte';
  }
}
