/**
 * Reward Calculator
 * 
 * Logic for calculating staking rewards based on lock periods and tiers.
 */

import { StakeRecord, LOCK_MULTIPLIERS, BASE_APY } from './types';
import { LockPeriod } from '../../common/types';

export class RewardCalculator {
  /**
   * Calculate accrued rewards for a stake
   */
  static calculateRewards(stake: StakeRecord, now: number = Date.now()): bigint {
    if (stake.status !== 'ACTIVE') return 0n;
    
    const timeStaked = now - stake.lastRewardClaim;
    if (timeStaked <= 0) return 0n;
    
    const yearsStaked = timeStaked / (365 * 24 * 60 * 60 * 1000);
    const multiplier = LOCK_MULTIPLIERS[stake.lockPeriod] || 1.0;
    const apy = BASE_APY * multiplier;
    
    // Reward = Principal * APY * Years
    // Using BigInt math with precision scaling
    const PRECISION = 1000000000n; // 9 decimals of precision
    const amount = stake.amount;
    const apyBig = BigInt(Math.floor(apy * Number(PRECISION)));
    const yearsBig = BigInt(Math.floor(yearsStaked * Number(PRECISION)));
    
    const reward = (amount * apyBig * yearsBig) / (PRECISION * PRECISION);
    
    return reward;
  }
  
  /**
   * Calculate projected APY for a lock period
   */
  static getProjectedAPY(lockPeriod: LockPeriod): number {
    return BASE_APY * (LOCK_MULTIPLIERS[lockPeriod] || 1.0);
  }
}
