/**
 * Free Energy Calculations
 * 
 * Implements variational free energy and expected free energy calculations
 * for the Active Inference framework.
 */

import { BeliefState, Prediction, GenerativeModelParams } from './types';

// ═══════════════════════════════════════════════════════════════════════════
// VARIATIONAL FREE ENERGY
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Calculate variational free energy F = E_q[log q(s) - log p(o,s)]
 * 
 * This is the core quantity minimized in Active Inference.
 * F = complexity - accuracy
 * F = KL[q||p] - E_q[log p(o|s)]
 * 
 * @param beliefs Current belief states
 * @param observation Current observation (encoded)
 * @param modelParams Generative model parameters
 */
export function calculateVariationalFreeEnergy(
  beliefs: BeliefState[],
  observation: number[],
  modelParams: GenerativeModelParams
): number {
  if (beliefs.length === 0) {
    return 1.0; // Maximum uncertainty
  }
  
  // Calculate complexity: KL divergence from prior
  const complexity = calculateKLDivergence(beliefs, modelParams.priorPrecision);
  
  // Calculate negative log-likelihood (accuracy term)
  const accuracy = calculateAccuracy(beliefs, observation, modelParams.likelihoodPrecision);
  
  // F = complexity - accuracy
  return complexity - accuracy;
}

/**
 * Calculate KL divergence from prior beliefs
 */
export function calculateKLDivergence(
  beliefs: BeliefState[],
  priorPrecision: number
): number {
  let kl = 0;
  
  for (const belief of beliefs) {
    // Assume uniform prior
    const priorProb = 1 / beliefs.length;
    
    if (belief.probability > 0 && priorProb > 0) {
      kl += belief.probability * Math.log(belief.probability / priorProb);
    }
  }
  
  // Weight by precision
  return kl * priorPrecision;
}

/**
 * Calculate accuracy (negative log-likelihood of observation given beliefs)
 */
export function calculateAccuracy(
  beliefs: BeliefState[],
  observation: number[],
  likelihoodPrecision: number
): number {
  // Calculate weighted prediction based on beliefs
  const prediction = predictObservation(beliefs);
  
  // Calculate squared error
  const squaredError = observation.reduce((acc, obs, i) => {
    const pred = prediction[i] || 0;
    return acc + Math.pow(obs - pred, 2);
  }, 0);
  
  // Precision-weighted negative log likelihood
  // Higher precision = smaller errors matter more
  return -0.5 * likelihoodPrecision * squaredError;
}

/**
 * Generate predicted observation from beliefs
 */
export function predictObservation(beliefs: BeliefState[]): number[] {
  if (beliefs.length === 0) return [];
  
  // Combine belief primes weighted by probability
  const maxPrimes = Math.max(...beliefs.map(b => b.primeFactors.length));
  const prediction = new Array(maxPrimes).fill(0);
  
  for (const belief of beliefs) {
    for (let i = 0; i < belief.primeFactors.length; i++) {
      prediction[i] += belief.probability * belief.primeFactors[i];
    }
  }
  
  return prediction;
}

// ═══════════════════════════════════════════════════════════════════════════
// EXPECTED FREE ENERGY
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Calculate expected free energy G(π) for policy selection
 * 
 * G(π) = epistemic_value + pragmatic_value + risk
 * 
 * This is used to evaluate and compare policies.
 */
export function calculateExpectedFreeEnergy(
  beliefs: BeliefState[],
  goalState: number[],
  policyPredictions: Prediction[],
  modelParams: GenerativeModelParams
): { epistemic: number; pragmatic: number; risk: number; total: number } {
  // Epistemic value: expected information gain
  const epistemic = calculateEpistemicValue(beliefs, policyPredictions);
  
  // Pragmatic value: expected goal achievement
  const pragmatic = calculatePragmaticValue(policyPredictions, goalState);
  
  // Risk: ambiguity in predictions
  const risk = calculateRisk(policyPredictions);
  
  // Combine with weights
  const total = 
    modelParams.explorationBonus * epistemic +
    modelParams.goalWeight * pragmatic +
    risk;
  
  return { epistemic, pragmatic, risk, total };
}

/**
 * Calculate epistemic value (expected information gain)
 */
export function calculateEpistemicValue(
  beliefs: BeliefState[],
  predictions: Prediction[]
): number {
  if (predictions.length === 0) return 0;
  
  // Current entropy
  const currentEntropy = calculateBeliefEntropy(beliefs);
  
  // Expected entropy after observations
  let expectedEntropyAfter = 0;
  for (const pred of predictions) {
    // Assume each prediction leads to some belief update
    // This is simplified - real calculation would be more complex
    expectedEntropyAfter += pred.probability * (currentEntropy * 0.9);
  }
  
  // Information gain = current entropy - expected entropy after
  return currentEntropy - expectedEntropyAfter;
}

/**
 * Calculate pragmatic value (expected goal achievement)
 */
export function calculatePragmaticValue(
  predictions: Prediction[],
  goalState: number[]
): number {
  if (predictions.length === 0 || goalState.length === 0) return 0;
  
  let value = 0;
  
  for (const pred of predictions) {
    // Calculate distance to goal
    const predArray = Array.isArray(pred.content) ? pred.content as number[] : [];
    const distance = goalState.reduce((acc, goal, i) => {
      const predVal = predArray[i] || 0;
      return acc + Math.pow(goal - predVal, 2);
    }, 0);
    
    // Negative distance weighted by probability
    value -= pred.probability * Math.sqrt(distance);
  }
  
  return value;
}

/**
 * Calculate risk/ambiguity in predictions
 */
export function calculateRisk(predictions: Prediction[]): number {
  if (predictions.length === 0) return 0;
  
  // Risk as variance in predictions
  const mean = predictions.reduce((acc, p) => acc + p.probability, 0) / predictions.length;
  const variance = predictions.reduce((acc, p) => 
    acc + Math.pow(p.probability - mean, 2), 0) / predictions.length;
  
  return variance;
}

// ═══════════════════════════════════════════════════════════════════════════
// BELIEF UPDATES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Calculate belief entropy
 */
export function calculateBeliefEntropy(beliefs: BeliefState[]): number {
  if (beliefs.length === 0) return 0;
  
  let entropy = 0;
  for (const belief of beliefs) {
    if (belief.probability > 0) {
      entropy -= belief.probability * Math.log2(belief.probability);
    }
  }
  
  return entropy;
}

/**
 * Calculate prediction error
 */
export function calculatePredictionError(
  predicted: number[],
  actual: number[],
  precision: number
): number {
  const maxLen = Math.max(predicted.length, actual.length);
  let squaredError = 0;
  
  for (let i = 0; i < maxLen; i++) {
    const p = predicted[i] || 0;
    const a = actual[i] || 0;
    squaredError += Math.pow(a - p, 2);
  }
  
  // Precision-weighted error
  return precision * Math.sqrt(squaredError);
}

/**
 * Update beliefs based on prediction error (Bayesian update)
 */
export function updateBeliefs(
  beliefs: BeliefState[],
  observation: number[],
  learningRate: number
): BeliefState[] {
  if (beliefs.length === 0) return [];
  
  // Calculate likelihood of observation under each belief
  const likelihoods = beliefs.map(belief => {
    const prediction = belief.primeFactors;
    const error = calculatePredictionError(prediction, observation, belief.precision);
    return Math.exp(-0.5 * error * error);
  });
  
  // Normalize likelihoods
  const totalLikelihood = likelihoods.reduce((a, b) => a + b, 0);
  
  // Update probabilities using Bayes rule with learning rate
  return beliefs.map((belief, i) => {
    const posterior = totalLikelihood > 0 
      ? likelihoods[i] / totalLikelihood 
      : 1 / beliefs.length;
    
    const newProbability = belief.probability + 
      learningRate * (posterior - belief.probability);
    
    return {
      ...belief,
      probability: newProbability,
      entropy: -newProbability * Math.log2(Math.max(newProbability, 1e-10)),
      lastUpdated: Date.now()
    };
  });
}

/**
 * Normalize belief probabilities to sum to 1
 */
export function normalizeBeliefs(beliefs: BeliefState[]): BeliefState[] {
  const total = beliefs.reduce((acc, b) => acc + b.probability, 0);
  if (total === 0) return beliefs;
  
  return beliefs.map(b => ({
    ...b,
    probability: b.probability / total
  }));
}

// ═══════════════════════════════════════════════════════════════════════════
// SURPRISAL
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Calculate surprisal (negative log probability) of an observation
 */
export function calculateSurprisal(
  observation: number[],
  beliefs: BeliefState[]
): number {
  if (beliefs.length === 0) return Infinity;
  
  // Calculate probability of observation under belief model
  let logProb = 0;
  
  for (const belief of beliefs) {
    const prediction = belief.primeFactors;
    const error = calculatePredictionError(prediction, observation, belief.precision);
    
    // Gaussian likelihood
    const likelihood = Math.exp(-0.5 * error * error);
    logProb += belief.probability * Math.log(Math.max(likelihood, 1e-10));
  }
  
  return -logProb; // Surprisal is negative log probability
}
