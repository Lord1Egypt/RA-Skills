import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { ConsensusProtocol, ConsensusProposal, Vote } from '../../src/core/Consensus';
import { DSNNodeConfig, GMFObject, SMFVector } from '../../src/core/types';

describe('ConsensusProtocol', () => {
  let protocol: ConsensusProtocol;
  const mockSmf: SMFVector = Array(16).fill(0.1) as unknown as SMFVector;
  // Make domain deterministic: idx 4-7 are cognitive.
  mockSmf[5] = 1.0; 

  const mockObject: GMFObject = {
    id: 'obj-1',
    semanticObject: { term: 'test', normalForm: 'test' },
    weight: 1,
    smf: mockSmf,
    insertedAt: Date.now(),
    proposalId: '',
    redundancyScore: 1,
    metadata: { nodeId: 'n1', consensusAchieved: false }
  };

  beforeEach(() => {
    protocol = new ConsensusProtocol('local-node');
  });

  describe('createProposal', () => {
    it('should create valid proposal if coherence high', () => {
      const prop = protocol.createProposal(mockObject, 'proposer-1', 100, 0.8);
      expect(prop.tickProof.valid).toBe(true);
      expect(prop.targetObject).toBe(mockObject);
    });

    it('should create invalid proposal if coherence low', () => {
      const prop = protocol.createProposal(mockObject, 'proposer-1', 100, 0.5);
      expect(prop.tickProof.valid).toBe(false);
    });
  });

  describe('calculateVoteWeight', () => {
    const baseVoter: DSNNodeConfig = {
      nodeId: 'voter-1',
      name: 'Voter',
      domain: 'cognitive',
      seaPublicKey: 'key',
      gunPeers: [],
      keyTriplet: {} as any,
      semanticDomain: 'cognitive', // Matches mockObject
      primeDomain: [],
      smfAxes: [],
      sriaCapable: true,
      bootstrapUrl: '',
      status: 'ONLINE',
      lastHeartbeat: 0,
      supportedProviders: [],
      hostedSkills: [],
      loadIndex: 0,
      stakingTier: 'Neophyte', // Multiplier 1
      alephBalance: 0
    };

    it('should give base weight for matching domain', () => {
      const prop = protocol.createProposal(mockObject, 'p1', 1, 1);
      const weight = protocol.calculateVoteWeight(baseVoter, prop);
      // Domain match (1.5) * Prime (1.0) * Axis (1+0) * Tier (1) = 1.5
      expect(weight).toBeCloseTo(1.5);
    });

    it('should penalty for domain mismatch', () => {
      const mismatchVoter = { ...baseVoter, semanticDomain: 'perceptual' as any };
      const prop = protocol.createProposal(mockObject, 'p1', 1, 1);
      const weight = protocol.calculateVoteWeight(mismatchVoter, prop);
      // Mismatch (0.5) ... = 0.5
      expect(weight).toBeCloseTo(0.5);
    });

    it('should apply tier multiplier', () => {
      const archonVoter = { ...baseVoter, stakingTier: 'Archon' as any };
      const prop = protocol.createProposal(mockObject, 'p1', 1, 1);
      const weight = protocol.calculateVoteWeight(archonVoter, prop);
      // 1.5 * 10 = 15
      expect(weight).toBeCloseTo(15.0);
    });
  });

  describe('evaluateProposal', () => {
    it('should reject if proof is invalid', () => {
      const prop = protocol.createProposal(mockObject, 'p1', 1, 0.1); // invalid
      const result = protocol.evaluateProposal(prop, []);
      expect(result.accepted).toBe(false);
      expect(result.reason).toContain('Invalid tick proof');
    });

    it('should reject if no votes', () => {
      const prop = protocol.createProposal(mockObject, 'p1', 1, 0.9);
      const result = protocol.evaluateProposal(prop, []);
      expect(result.accepted).toBe(false);
      expect(result.reason).toContain('No votes');
    });

    it('should achieve consensus with sufficient support', () => {
      const prop = protocol.createProposal(mockObject, 'p1', 1, 0.9);
      const votes: Vote[] = [
        { voterId: 'v1', vote: 'SUPPORT', stakeAmount: 10, weight: 10, timestamp: 0 },
        { voterId: 'v2', vote: 'SUPPORT', stakeAmount: 10, weight: 10, timestamp: 0 },
        { voterId: 'v3', vote: 'CONTEST', stakeAmount: 10, weight: 5, timestamp: 0 }
      ];
      // Total 25. Support 20. 20/25 = 0.8 >= 0.66
      const result = protocol.evaluateProposal(prop, votes);
      expect(result.accepted).toBe(true);
      expect(result.totalSupport).toBe(20);
    });

    it('should fail consensus with insufficient support', () => {
      const prop = protocol.createProposal(mockObject, 'p1', 1, 0.9);
      const votes: Vote[] = [
        { voterId: 'v1', vote: 'SUPPORT', stakeAmount: 10, weight: 5, timestamp: 0 },
        { voterId: 'v2', vote: 'CONTEST', stakeAmount: 10, weight: 10, timestamp: 0 }
      ];
      // Total 15. Support 5. 5/15 = 0.33 < 0.66
      const result = protocol.evaluateProposal(prop, votes);
      expect(result.accepted).toBe(false);
    });
  });

  describe('verifyCoherence', () => {
    it('should return true for similar context', () => {
      const prop = protocol.createProposal(mockObject, 'p1', 1, 1);
      // Same vector
      const result = protocol.verifyCoherence(prop, mockSmf);
      expect(result).toBe(true);
    });

    it('should return false for dissimilar context', () => {
      const prop = protocol.createProposal(mockObject, 'p1', 1, 1);
      // Orthogonal vector
      const diffSmf = Array(16).fill(0);
      diffSmf[0] = 1; // Perceptual
      // dot product approx 0
      const result = protocol.verifyCoherence(prop, diffSmf as unknown as SMFVector);
      expect(result).toBe(false);
    });
  });
});
