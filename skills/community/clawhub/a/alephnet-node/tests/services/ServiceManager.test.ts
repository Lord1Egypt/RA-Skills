import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { ServiceManager } from '../../src/services/ServiceManager';
import { AlephWallet } from '../../src/infra/Wallet';
import { generateKeyTriplet } from '../../src/common/crypto';

describe('ServiceManager', () => {
  let manager: ServiceManager;
  let mockGun: any;
  let mockWallet: AlephWallet;

  beforeEach(() => {
    mockGun = {
      get: jest.fn().mockReturnThis(),
      put: jest.fn(),
      map: jest.fn().mockReturnThis(),
      once: jest.fn(),
      on: jest.fn(),
      off: jest.fn()
    };
    
    // Mock wallet
    mockWallet = {
        authorizePayment: jest.fn<any>().mockResolvedValue({ id: 'auth-1' }),
        finalizePayment: jest.fn<any>().mockResolvedValue({ transactionId: 'tx-1' })
    } as unknown as AlephWallet;

    manager = new ServiceManager(mockGun, mockWallet, 'local-node');
  });

  describe('registerService', () => {
    it('should register a service', async () => {
      const def: any = { id: 'svc-1', name: 'Test Service' };
      
      // Mock put callback
      mockGun.put.mockImplementation((data: any, cb: Function) => cb({}));

      const result = await manager.registerService(def);
      
      expect(result.serviceId).toBe('svc-1');
      expect(mockGun.get).toHaveBeenCalledWith('services');
    });
  });

  describe('subscribeToService', () => {
    it('should subscribe to a topic', async () => {
      // Mock getServiceDefinition
      mockGun.once.mockImplementation((cb: Function) => cb({ definition: { id: 'svc-1' } }));
      
      const handler = jest.fn();
      const sub = await manager.subscribeToService('svc-1', 'topic-1', handler);
      
      expect(sub).toBeDefined();
      expect(mockGun.on).toHaveBeenCalled();
      
      sub.unsubscribe();
      expect(mockGun.off).toHaveBeenCalled();
    });
  });
});
