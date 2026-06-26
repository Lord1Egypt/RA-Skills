/**
 * SRIA Module - Self-Reflective Intelligence Architecture
 * 
 * Complete Active Inference implementation for agent cognition.
 */

// Types
export * from './types';

// Free Energy calculations
export {
  calculateVariationalFreeEnergy,
  calculateKLDivergence,
  calculateAccuracy,
  predictObservation,
  calculateExpectedFreeEnergy,
  calculateEpistemicValue,
  calculatePragmaticValue,
  calculateRisk,
  calculateBeliefEntropy,
  calculatePredictionError,
  updateBeliefs,
  normalizeBeliefs,
  calculateSurprisal
} from './FreeEnergy';

// Belief Dynamics
export {
  beliefsToQuaternion,
  updateQuaternionFromError,
  smoothBeliefTransition,
  updateAttention,
  applyAttention,
  createBelief,
  pruneBeliefs,
  mergeBeliefs,
  calculateBeliefSimilarity
} from './BeliefDynamics';

// Policy Selection
export {
  generatePolicies,
  createPolicy,
  evaluatePolicies,
  selectPolicy,
  getTopPolicies,
  refinePolicyFromOutcome,
  refinePolicyParameters,
  getDefaultPoliciesForState
} from './PolicySelection';

// Main Engine
export { SRIAEngine } from './SRIAEngine';
