/**
 * Policy Selection for Active Inference
 * 
 * Implements policy generation, evaluation, and selection based on
 * expected free energy minimization.
 */

import { 
  Policy, 
  PolicyType, 
  BeliefState, 
  Prediction, 
  GenerativeModelParams,
  ActionOutcome
} from './types';
import { calculateExpectedFreeEnergy } from './FreeEnergy';
import { generateId } from '../../common/hash';

// ═══════════════════════════════════════════════════════════════════════════
// POLICY GENERATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Generate candidate policies based on current beliefs
 */
export function generatePolicies(
  beliefs: BeliefState[],
  currentFreeEnergy: number,
  availableActions: PolicyType[]
): Policy[] {
  const policies: Policy[] = [];
  
  for (const type of availableActions) {
    const policy = createPolicy(type, beliefs, currentFreeEnergy);
    policies.push(policy);
  }
  
  return policies;
}

/**
 * Create a policy of a specific type
 */
export function createPolicy(
  type: PolicyType,
  beliefs: BeliefState[],
  currentFreeEnergy: number
): Policy {
  const id = generateId(`policy-${type}`);
  const baseParams = getPolicyBaseParameters(type);
  
  return {
    id,
    type,
    parameters: baseParams,
    expectedFreeEnergy: estimateExpectedFreeEnergy(type, beliefs, currentFreeEnergy),
    epistemic: estimateEpistemicValue(type, beliefs),
    pragmatic: estimatePragmaticValue(type, beliefs),
    risk: estimateRisk(type, beliefs)
  };
}

/**
 * Get default parameters for a policy type
 */
function getPolicyBaseParameters(type: PolicyType): Record<string, unknown> {
  switch (type) {
    case 'PERCEIVE':
      return { duration: 1, channels: ['visual', 'semantic'] };
    case 'THINK':
      return { depth: 2, focus: 'current' };
    case 'RESPOND':
      return { format: 'text', length: 'medium' };
    case 'TOOL_CALL':
      return { tool: null, args: {} };
    case 'QUERY':
      return { questionType: 'clarification' };
    case 'CONSOLIDATE':
      return { target: 'gmf', priority: 'high' };
    case 'SLEEP':
      return { duration: 1, consolidate: true };
    default:
      return {};
  }
}

/**
 * Estimate expected free energy for a policy type
 */
function estimateExpectedFreeEnergy(
  type: PolicyType,
  beliefs: BeliefState[],
  currentFreeEnergy: number
): number {
  // Baseline estimates based on policy type
  const baseEstimates: Record<PolicyType, number> = {
    PERCEIVE: -0.2,    // Usually reduces uncertainty
    THINK: -0.15,      // Internal processing
    RESPOND: 0.1,      // Commits to action
    TOOL_CALL: -0.3,   // External information
    QUERY: -0.25,      // Direct information seeking
    CONSOLIDATE: 0.0,  // Memory operation
    SLEEP: 0.0         // Background processing
  };
  
  // Adjust based on belief entropy
  const beliefEntropy = beliefs.reduce((acc, b) => acc + b.entropy, 0);
  const entropyFactor = beliefEntropy > 1 ? 1.2 : 0.8;
  
  return (baseEstimates[type] * entropyFactor) + currentFreeEnergy * 0.1;
}

/**
 * Estimate epistemic value (information gain potential)
 */
function estimateEpistemicValue(type: PolicyType, beliefs: BeliefState[]): number {
  const epistemicPotential: Record<PolicyType, number> = {
    PERCEIVE: 0.8,
    THINK: 0.4,
    RESPOND: 0.1,
    TOOL_CALL: 0.9,
    QUERY: 0.95,
    CONSOLIDATE: 0.0,
    SLEEP: 0.0
  };
  
  // Higher entropy beliefs = more to gain from epistemic actions
  const avgEntropy = beliefs.length > 0 
    ? beliefs.reduce((acc, b) => acc + b.entropy, 0) / beliefs.length
    : 0;
  
  return epistemicPotential[type] * (1 + avgEntropy);
}

/**
 * Estimate pragmatic value (goal achievement potential)
 */
function estimatePragmaticValue(type: PolicyType, beliefs: BeliefState[]): number {
  const pragmaticPotential: Record<PolicyType, number> = {
    PERCEIVE: 0.1,
    THINK: 0.3,
    RESPOND: 0.9,
    TOOL_CALL: 0.7,
    QUERY: 0.2,
    CONSOLIDATE: 0.1,
    SLEEP: 0.0
  };
  
  // Higher confidence beliefs = more to gain from pragmatic actions
  const avgConfidence = beliefs.length > 0 
    ? beliefs.reduce((acc, b) => acc + b.probability, 0) / beliefs.length
    : 0;
  
  return pragmaticPotential[type] * avgConfidence;
}

/**
 * Estimate risk (potential for bad outcomes)
 */
function estimateRisk(type: PolicyType, beliefs: BeliefState[]): number {
  const riskLevels: Record<PolicyType, number> = {
    PERCEIVE: 0.05,
    THINK: 0.1,
    RESPOND: 0.3,
    TOOL_CALL: 0.4,
    QUERY: 0.2,
    CONSOLIDATE: 0.05,
    SLEEP: 0.0
  };
  
  // Lower confidence = higher risk
  const avgConfidence = beliefs.length > 0 
    ? beliefs.reduce((acc, b) => acc + b.probability, 0) / beliefs.length
    : 0;
  
  return riskLevels[type] * (1 - avgConfidence);
}

// ═══════════════════════════════════════════════════════════════════════════
// POLICY EVALUATION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Evaluate policies and compute expected free energy
 */
export function evaluatePolicies(
  policies: Policy[],
  beliefs: BeliefState[],
  goalState: number[],
  modelParams: GenerativeModelParams
): Policy[] {
  return policies.map(policy => {
    // Generate predictions for this policy
    const predictions = predictPolicyOutcome(policy, beliefs);
    
    // Calculate expected free energy
    const efe = calculateExpectedFreeEnergy(
      beliefs,
      goalState,
      predictions,
      modelParams
    );
    
    return {
      ...policy,
      expectedFreeEnergy: efe.total,
      epistemic: efe.epistemic,
      pragmatic: efe.pragmatic,
      risk: efe.risk
    };
  });
}

/**
 * Generate predictions for policy outcomes
 */
function predictPolicyOutcome(
  policy: Policy,
  beliefs: BeliefState[]
): Prediction[] {
  const predictions: Prediction[] = [];
  
  // Generate multiple prediction samples
  const numSamples = 3;
  
  for (let i = 0; i < numSamples; i++) {
    const prediction = generatePrediction(policy, beliefs, i);
    predictions.push(prediction);
  }
  
  return predictions;
}

/**
 * Generate a single prediction
 */
function generatePrediction(
  policy: Policy,
  beliefs: BeliefState[],
  sampleIndex: number
): Prediction {
  // Use beliefs to predict outcome
  const topBeliefs = [...beliefs]
    .sort((a, b) => b.probability - a.probability)
    .slice(0, 3);
  
  // Combine prime factors as prediction content
  const content = topBeliefs.flatMap(b => b.primeFactors);
  
  // Vary probability based on sample index
  const baseProbability = topBeliefs.length > 0 
    ? topBeliefs[0].probability 
    : 0.5;
  
  const probability = baseProbability * (1 - sampleIndex * 0.1);
  
  return {
    id: generateId(`pred-${policy.type}`),
    content,
    probability,
    precision: topBeliefs.length > 0 ? topBeliefs[0].precision : 1.0,
    generated: Date.now()
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// POLICY SELECTION
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Select the best policy based on expected free energy
 */
export function selectPolicy(
  policies: Policy[],
  explorationTemperature: number = 1.0
): Policy | null {
  if (policies.length === 0) return null;
  
  // Sort by expected free energy (lower is better)
  const sorted = [...policies].sort(
    (a, b) => a.expectedFreeEnergy - b.expectedFreeEnergy
  );
  
  if (explorationTemperature === 0) {
    // Greedy selection
    return sorted[0];
  }
  
  // Softmax selection with temperature
  const selected = softmaxSelect(sorted, explorationTemperature);
  return selected;
}

/**
 * Softmax selection over policies
 */
function softmaxSelect(policies: Policy[], temperature: number): Policy {
  // Compute softmax probabilities (negative EFE because lower is better)
  const negEFE = policies.map(p => -p.expectedFreeEnergy);
  const maxEFE = Math.max(...negEFE);
  
  const expEFE = negEFE.map(e => Math.exp((e - maxEFE) / temperature));
  const sumExp = expEFE.reduce((a, b) => a + b, 0);
  const probabilities = expEFE.map(e => e / sumExp);
  
  // Sample from distribution
  const rand = Math.random();
  let cumulative = 0;
  
  for (let i = 0; i < policies.length; i++) {
    cumulative += probabilities[i];
    if (rand <= cumulative) {
      return policies[i];
    }
  }
  
  return policies[policies.length - 1];
}

/**
 * Get top N policies by expected free energy
 */
export function getTopPolicies(policies: Policy[], n: number = 3): Policy[] {
  return [...policies]
    .sort((a, b) => a.expectedFreeEnergy - b.expectedFreeEnergy)
    .slice(0, n);
}

// ═══════════════════════════════════════════════════════════════════════════
// POLICY REFINEMENT
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Refine policy based on action outcome
 */
export function refinePolicyFromOutcome(
  policy: Policy,
  outcome: ActionOutcome,
  learningRate: number
): Policy {
  // Update expected free energy based on actual outcome
  const actualEFE = outcome.predictionError * 0.5 - outcome.information * 0.5;
  
  const refinedEFE = policy.expectedFreeEnergy + 
    learningRate * (actualEFE - policy.expectedFreeEnergy);
  
  return {
    ...policy,
    expectedFreeEnergy: refinedEFE
  };
}

/**
 * Create a refined policy with specific parameters
 */
export function refinePolicyParameters(
  policy: Policy,
  parameterUpdates: Record<string, unknown>
): Policy {
  return {
    ...policy,
    parameters: {
      ...policy.parameters,
      ...parameterUpdates
    }
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// DEFAULT POLICIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Get default available actions for a lifecycle state
 */
export function getDefaultPoliciesForState(
  lifecycleState: string
): PolicyType[] {
  switch (lifecycleState) {
    case 'DORMANT':
      return ['PERCEIVE'];
    case 'PERCEIVING':
      return ['THINK', 'PERCEIVE', 'QUERY'];
    case 'DECIDING':
      return ['THINK', 'RESPOND', 'TOOL_CALL', 'QUERY'];
    case 'ACTING':
      return ['RESPOND', 'TOOL_CALL'];
    case 'LEARNING':
      return ['THINK', 'CONSOLIDATE'];
    case 'CONSOLIDATING':
      return ['CONSOLIDATE', 'SLEEP'];
    case 'SLEEPING':
      return ['SLEEP', 'PERCEIVE'];
    default:
      return ['PERCEIVE', 'THINK', 'RESPOND'];
  }
}
