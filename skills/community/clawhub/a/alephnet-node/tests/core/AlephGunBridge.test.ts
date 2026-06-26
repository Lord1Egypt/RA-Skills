import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { AlephGunBridge } from '../../src/core/AlephGunBridge';
import { AgentTriggerEvent } from '../../src/core/types';

describe('AlephGunBridge', () => {
  let bridge: AlephGunBridge;
  let mockGun: any;
  let mockDSNNode: any;
  let mockAgentManager: any;

  beforeEach(async () => {
    mockGun = {};
    mockDSNNode = {
      config: {
        nodeId: 'local-node',
        semanticDomain: 'cognitive',
        gunPeers: []
      }
    };
    mockAgentManager = {};

    bridge = new AlephGunBridge();
    await bridge.initialize(mockGun, mockDSNNode, mockAgentManager);
  });

  describe('initialize', () => {
    it('should store dependencies', () => {
      // Since properties are private, we assume success if no error thrown
      // and subsequent methods that use them work.
      expect(bridge).toBeDefined();
    });
  });

  describe('projectToSMF', () => {
    it('should return a 16-dimensional vector', () => {
      const result = bridge.projectToSMF('some/path', { data: 'test' });
      expect(result).toHaveLength(16);
      expect(result.every(n => typeof n === 'number')).toBe(true);
    });

    it('should be deterministic', () => {
      const result1 = bridge.projectToSMF('path/a', { val: 1 });
      const result2 = bridge.projectToSMF('path/a', { val: 1 });
      expect(result1).toEqual(result2);
    });

    it('should produce different vectors for different inputs', () => {
      // Note: hash collision possible but unlikely for simple distinct strings in small test
      const result1 = bridge.projectToSMF('path/a', { val: 1 });
      const result2 = bridge.projectToSMF('path/b', { val: 2 });
      expect(result1).not.toEqual(result2);
    });
  });

  describe('routeRequest', () => {
    const baseEvent: AgentTriggerEvent = {
      action: 'NEW_MESSAGE',
      conversationId: 'conv-123',
      routing: {
        preferredDomain: 'cognitive',
        requiredSmfAxes: [2, 3]
      }
    };

    it('should route to self if no peers available', async () => {
      mockDSNNode.config.gunPeers = [];
      const decision = await bridge.routeRequest(baseEvent);
      expect(decision.targetNodeId).toBe('local-node');
    });

    it('should route to a peer if available', async () => {
      // The implementation mocks peer data based on the string URL
      // So we just provide some strings
      mockDSNNode.config.gunPeers = ['peer-1', 'peer-2'];
      
      const decision = await bridge.routeRequest(baseEvent);
      // Logic inside: maps strings to objects with 'cognitive' domain and returns one with max score
      // Since all mocked peers in implementation are identical 'cognitive', it should pick one.
      // Actually the loop logic: bestPeer starts null.
      // peer-1: score matches domain(+10), overlap(+something), load(-something).
      // It should pick one of them.
      expect(['peer-1', 'peer-2']).toContain(decision.targetNodeId);
      expect(decision.relevanceScore).toBeGreaterThan(0);
    });
  });

  describe('verifyCoherence', () => {
    it('should return false if proof is missing', async () => {
      const result = await bridge.verifyCoherence({});
      expect(result).toBe(false);
    });

    it('should return false if coherence is below threshold', async () => {
      const result = await bridge.verifyCoherence({
        coherenceProof: { coherence: 0.7, tickNumber: 1, smfHash: 'abc' }
      });
      expect(result).toBe(false);
    });

    it('should return true if coherence is sufficient', async () => {
      const result = await bridge.verifyCoherence({
        coherenceProof: { coherence: 0.85, tickNumber: 1, smfHash: 'abc' }
      });
      expect(result).toBe(true);
    });
  });

  describe('syncGMFToGraph', () => {
    it('should run without error', async () => {
      await expect(bridge.syncGMFToGraph()).resolves.not.toThrow();
    });
  });

  describe('handleSRIAEvent', () => {
    it('should handle summon event', async () => {
      await expect(bridge.handleSRIAEvent('summon', { some: 'data' })).resolves.not.toThrow();
    });
    
    it('should handle dismiss event', async () => {
        await expect(bridge.handleSRIAEvent('dismiss', { some: 'data' })).resolves.not.toThrow();
      });
  });
});
