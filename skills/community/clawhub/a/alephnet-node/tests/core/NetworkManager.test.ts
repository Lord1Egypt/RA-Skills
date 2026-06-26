import { describe, it, expect, beforeEach, afterEach, jest } from '@jest/globals';
import { NetworkManager } from '../../src/core/network/NetworkManager';
import { generateKeyTriplet } from '../../src/common/crypto';
import { KeyTriplet } from '../../src/common/crypto';
import { NetworkMessage } from '../../src/core/network/types';

describe('NetworkManager', () => {
  let networkManager: NetworkManager;
  let keyTriplet: KeyTriplet;

  beforeEach(() => {
    keyTriplet = generateKeyTriplet();
    networkManager = new NetworkManager({
      nodeId: 'test-node',
      semanticDomain: 'cognitive',
      bootstrapUrls: ['https://bootstrap.example.com']
    }, keyTriplet);
  });

  afterEach(async () => {
    await networkManager.stop();
  });

  describe('start', () => {
    it('should start and connect to bootstrap nodes', async () => {
      await networkManager.start();
      const peers = networkManager.getPeers();
      expect(peers.length).toBeGreaterThan(0);
      expect(peers[0].address).toBe('https://bootstrap.example.com');
    });
  });

  describe('messaging', () => {
    it('should create and route messages', async () => {
      await networkManager.start();
      
      // Mock message router
      const router = (networkManager as any).messageRouter;
      const routeSpy = jest.spyOn(router, 'routeMessage');
      
      const msgId = await networkManager.sendMessage('target-node', 'ping', { nonce: '123' });
      
      expect(msgId).toBeDefined();
      expect(routeSpy).toHaveBeenCalled();
      
      const message = routeSpy.mock.calls[0][0] as NetworkMessage;
      expect(message.type).toBe('ping');
      expect(message.to).toBe('target-node');
      expect(message.signature).toBeDefined();
    });

    it('should broadcast messages', async () => {
      await networkManager.start();
      
      const router = (networkManager as any).messageRouter;
      const routeSpy = jest.spyOn(router, 'routeMessage');
      
      await networkManager.broadcast('announce', { status: 'online' });
      
      const message = routeSpy.mock.calls[0][0] as NetworkMessage;
      expect(message.to).toBe('broadcast');
    });
  });
});
