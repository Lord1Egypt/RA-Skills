import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { AlephWallet } from '../../src/infra/Wallet';
import { generateKeyTriplet } from '../../src/common/crypto';
import { StakeRecord } from '../../src/core/economics/types';

describe('AlephWallet', () => {
  let wallet: AlephWallet;
  let mockGun: any;
  let mockStake: StakeRecord;

  beforeEach(() => {
    mockGun = {
      get: jest.fn().mockReturnThis(),
      put: jest.fn(),
      once: jest.fn()
    };
    wallet = new AlephWallet(generateKeyTriplet(), mockGun);
    
    mockStake = {
      id: 'stake-1',
      owner: wallet.address,
      amount: 1000n * 1000000000000000000n, // 1000 tokens
      lockPeriod: '7d',
      lockedUntil: Date.now() - 1000, // Unlocked
      createdAt: Date.now() - 8 * 24 * 60 * 60 * 1000,
      lastRewardClaim: Date.now() - 7 * 24 * 60 * 60 * 1000,
      status: 'ACTIVE'
    };
  });

  describe('unstake', () => {
    it('should unstake if eligible', async () => {
      // Mock get stake
      mockGun.once.mockImplementationOnce((cb: Function) => cb(mockStake));
      
      // Mock getBalance
      mockGun.once.mockImplementationOnce((cb: Function) => cb({ available: '1000', staked: '1000', total: '2000' }));

      const receipt = await wallet.unstake('stake-1');
      
      expect(receipt.stakeId).toBe('stake-1');
      expect(receipt.amount).toBe(1000n * 1000000000000000000n);
      expect(mockGun.put).toHaveBeenCalledWith(expect.objectContaining({ status: 'UNSTAKED' }));
    });

    it('should fail if locked', async () => {
      mockStake.lockedUntil = Date.now() + 100000;
      mockGun.once.mockImplementationOnce((cb: Function) => cb(mockStake));

      await expect(wallet.unstake('stake-1')).rejects.toThrow('Stake is still locked');
    });
  });

  describe('claimRewards', () => {
    it('should claim rewards', async () => {
      // Mock get stake
      mockGun.once.mockImplementationOnce((cb: Function) => cb(mockStake));
      
      // Mock getBalance
      mockGun.once.mockImplementationOnce((cb: Function) => cb({ available: '1000' }));

      const receipt = await wallet.claimRewards('stake-1');
      
      expect(receipt.amount).toBeGreaterThan(0n);
      expect(mockGun.put).toHaveBeenCalledWith(expect.objectContaining({ lastRewardClaim: expect.any(Number) }));
    });
  });
});
