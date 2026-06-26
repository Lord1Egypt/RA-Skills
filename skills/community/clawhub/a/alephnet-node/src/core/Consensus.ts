import { 
  DSNNodeConfig, 
  GMFObject, 
  CoherenceClaim, 
  CoherenceStake, 
  SMFVector,
  SemanticDomain
} from '../core/types';
import { determineDomain, cosineSimilarity } from '../common/math';
// Reuse helper

// Interface for a Proposal being voted on
export interface ConsensusProposal {
  id: string;
  targetObject: GMFObject; // The object being proposed
  proposerId: string;
  tickProof: {
    tickNumber: number;
    coherence: number; // 0.0 to 1.0
    valid: boolean;
  };
  smfHash: string;
  primeDomain?: number[]; // Optional prime factors if available
}

export interface Vote {
  voterId: string;
  vote: 'SUPPORT' | 'CONTEST';
  stakeAmount: number; // Amount staked on this vote
  weight: number; // Calculated semantic weight
  timestamp: number;
}

export interface ConsensusResult {
  accepted: boolean;
  totalSupport: number;
  totalContest: number;
  weightedRedundancy: number;
  reason: string;
}

/**
 * Coherent-Commit Protocol
 * 
 * Implements the logic for semantic consensus in AlephNet.
 * Calculates vote weights based on domain expertise and historical accuracy.
 * Validates proposals against coherence proofs.
 */
export class ConsensusProtocol {
  
  // Configuration
  private readonly MIN_COHERENCE_THRESHOLD = 0.7;
  private readonly CONSENSUS_THRESHOLD = 0.66; // 2/3 majority
  private readonly BASE_STAKE = 10;

  constructor(
    private localNodeId: string
    // In a real system, we'd inject a ReputationManager or HistoryService here
  ) {}

  /**
   * Create a new proposal for an object.
   */
  public createProposal(
    object: GMFObject, 
    proposerId: string,
    currentTick: number,
    coherenceScore: number
  ): ConsensusProposal {
    // In reality, proof generation involves cryptographic signing
    return {
      id: `prop-${object.id}-${Date.now()}`,
      targetObject: object,
      proposerId,
      tickProof: {
        tickNumber: currentTick,
        coherence: coherenceScore,
        valid: coherenceScore >= this.MIN_COHERENCE_THRESHOLD
      },
      smfHash: this.computeSmfHash(object.smf)
    };
  }

  /**
   * Calculate the semantic weight of a vote from a specific node.
   * Weight = (DomainOverlap * Reputation) + StakeBonus
   */
  public calculateVoteWeight(
    voter: DSNNodeConfig, 
    proposal: ConsensusProposal
  ): number {
    // 1. Semantic Domain Alignment
    // Does the voter specialize in the proposal's domain?
    const proposalDomain = determineDomain(proposal.targetObject.smf as SMFVector);
    const domainMatch = voter.semanticDomain === proposalDomain ? 1.5 : 0.5;

    // 2. Prime Domain Overlap
    // Intersection of voter's known primes vs proposal's primes (if available)
    let primeOverlap = 1.0;
    if (proposal.primeDomain && voter.primeDomain) {
      const intersection = voter.primeDomain.filter(p => proposal.primeDomain!.includes(p));
      const union = new Set([...voter.primeDomain, ...proposal.primeDomain!]);
      const jaccard = intersection.length / union.size;
      primeOverlap = 1.0 + jaccard; // 1.0 to 2.0 multiplier
    }

    // 3. SMF Alignment (Expertise Check)
    // If voter exposes their SMF expertise vector (e.g. in smfAxes which might be a vector or just indices)
    // Assuming smfAxes are indices of dimensions they are strong in.
    let axisBonus = 0;
    if (voter.smfAxes && voter.smfAxes.length > 0) {
        // Calculate average magnitude of proposal in voter's axes
        const propSmf = proposal.targetObject.smf;
        let axisMag = 0;
        voter.smfAxes.forEach(idx => {
            if (idx >= 0 && idx < 16) axisMag += Math.abs(propSmf[idx]);
        });
        axisBonus = axisMag / voter.smfAxes.length; // 0 to 1 approx
    }

    // 4. Staking Tier Multiplier
    const tierMultipliers = {
        'Neophyte': 1,
        'Adept': 2,
        'Magus': 5,
        'Archon': 10
    };
    const tierMult = tierMultipliers[voter.stakingTier] || 1;

    // Final Calculation
    // Base weight 1.0
    const rawWeight = 1.0 * domainMatch * primeOverlap * (1 + axisBonus) * tierMult;
    
    return parseFloat(rawWeight.toFixed(4));
  }

  /**
   * Evaluate a proposal given a set of votes.
   */
  public evaluateProposal(
    proposal: ConsensusProposal, 
    votes: Vote[]
  ): ConsensusResult {
    // 1. Validate Pre-conditions
    if (!proposal.tickProof.valid) {
      return {
        accepted: false,
        totalSupport: 0,
        totalContest: 0,
        weightedRedundancy: 0,
        reason: 'Invalid tick proof (low coherence)'
      };
    }

    // 2. Tally Votes
    let supportWeight = 0;
    let contestWeight = 0;

    for (const vote of votes) {
      if (vote.vote === 'SUPPORT') {
        supportWeight += vote.weight;
      } else {
        contestWeight += vote.weight;
      }
    }

    const totalWeight = supportWeight + contestWeight;
    if (totalWeight === 0) {
        return {
            accepted: false,
            totalSupport: 0,
            totalContest: 0,
            weightedRedundancy: 0,
            reason: 'No votes'
        };
    }

    // 3. Determine Consensus
    const supportRatio = supportWeight / totalWeight;
    const accepted = supportRatio >= this.CONSENSUS_THRESHOLD;

    return {
      accepted,
      totalSupport: supportWeight,
      totalContest: contestWeight,
      weightedRedundancy: supportRatio,
      reason: accepted ? 'Consensus achieved' : `Insufficient support (${(supportRatio*100).toFixed(1)}%)`
    };
  }

  /**
   * Verify if a proposal is coherent with local state.
   * (Used by a voter to decide how to vote)
   */
  public verifyCoherence(
    proposal: ConsensusProposal, 
    localSmfContext: SMFVector
  ): boolean {
    // Check semantic distance between proposal and local context
    // If too far, might be hallucination or irrelevant
    const similarity = cosineSimilarity(
        proposal.targetObject.smf as SMFVector, 
        localSmfContext
    );

    // Threshold depends on domain strictness, here hardcoded for simplicity
    return similarity > 0.4; 
  }

  private computeSmfHash(smf: number[]): string {
    // Simple hash of the vector for integrity
    // In production, use consistent float precision
    return smf.map(n => n.toFixed(6)).join(',');
  }
}
