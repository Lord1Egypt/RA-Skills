import { describe, it, expect, beforeEach, jest, afterEach } from '@jest/globals';
import { DSNNode, DSNNodeOptions } from '../../src/core/DSNNode';
import { SemanticDomain } from '../../src/core/types';

describe('DSNNode', () => {
  let node: DSNNode;
  const mockOptions: DSNNodeOptions = {
    nodeId: 'test-node-1',
    semanticDomain: 'cognitive',
    bootstrapUrl: 'https://test-bootstrap.com'
  };

  beforeEach(() => {
    jest.useFakeTimers();
    node = new DSNNode(mockOptions);
  });

  afterEach(() => {
    jest.clearAllTimers();
    jest.useRealTimers();
  });

  describe('Constructor', () => {
    it('should initialize with correct configuration', () => {
      expect(node.config.nodeId).toBe(mockOptions.nodeId);
      expect(node.config.semanticDomain).toBe(mockOptions.semanticDomain);
      expect(node.config.bootstrapUrl).toBe(mockOptions.bootstrapUrl);
      expect(node.config.status).toBe('OFFLINE');
    });

    it('should generate a real Ed25519 key triplet', () => {
      expect(node.config.keyTriplet).toBeDefined();
      // Real Ed25519 public keys are 32 bytes, base64 encoded (~44 chars with padding)
      expect(node.config.keyTriplet.pub).toMatch(/^[A-Za-z0-9+/]+=*$/);
      expect(node.config.keyTriplet.pub.length).toBeGreaterThanOrEqual(43);
      // Verify resonance field is a 16-dimensional vector
      expect(node.config.keyTriplet.resonance).toHaveLength(16);
      // Verify fingerprint exists
      expect(node.config.keyTriplet.fingerprint).toBeDefined();
      expect(node.config.keyTriplet.fingerprint.length).toBe(16);
      // bodyPrimes is optional but should exist after generation
      expect(node.config.keyTriplet.bodyPrimes).toBeDefined();
      expect(node.config.keyTriplet.bodyPrimes!.length).toBeGreaterThan(0);
    });
  });

  describe('start', () => {
    it('should set status to ONLINE and update lastHeartbeat', async () => {
      const gunMock = {};
      await node.start(gunMock);
      expect(node.config.status).toBe('ONLINE');
      expect(node.config.lastHeartbeat).toBeGreaterThan(0);
    });

    it('should use provided gun instance', async () => {
      const gunMock = { opt: jest.fn() };
      await node.start(gunMock);
      // Accessing private gun property via casting if necessary or just ensuring no error
      expect(node.config.status).toBe('ONLINE');
    });
  });

  describe('joinMesh', () => {
    it('should throw error if node is not started', async () => {
      await expect(node.joinMesh()).rejects.toThrow("Node must be started before joining mesh");
    });

    it('should return peers when started', async () => {
      await node.start({});
      const result = await node.joinMesh();
      expect(result.peers.length).toBeGreaterThan(0);
      expect(node.config.gunPeers).toEqual(result.peers);
    });

    it('should include gatewayUrl if provided', async () => {
      await node.start({});
      const gateway = 'https://custom-gateway.com';
      const result = await node.joinMesh({ gatewayUrl: gateway });
      expect(result.peers).toContain(gateway + '/gun');
    });
  });

  describe('heartbeat', () => {
    it('should update lastHeartbeat periodically', async () => {
      await node.start({});
      const initialHeartbeat = node.config.lastHeartbeat;
      
      // Advance time by 30 seconds + 1ms
      jest.advanceTimersByTime(30001);
      
      expect(node.config.lastHeartbeat).toBeGreaterThan(initialHeartbeat);
    });

    it('should not heartbeat if offline', async () => {
       // Access private method or just check logic if we could simulate offline while timer runs
       // But stop() clears status to OFFLINE.
       await node.start({});
       await node.stop();
       const stoppedHeartbeat = node.config.lastHeartbeat;
       
       jest.advanceTimersByTime(30001);
       expect(node.config.lastHeartbeat).toBe(stoppedHeartbeat);
    });
  });

  describe('stop', () => {
    it('should set status to OFFLINE', async () => {
      await node.start({});
      await node.stop();
      expect(node.config.status).toBe('OFFLINE');
    });
  });
});
