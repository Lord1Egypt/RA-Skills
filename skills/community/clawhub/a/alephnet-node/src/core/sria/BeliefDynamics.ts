/**
 * Belief Dynamics with Quaternion Representation
 * 
 * Implements quaternion-based belief state dynamics for smooth
 * transitions in the belief space.
 */

import { BeliefState, AttentionState } from './types';
import { Quaternion } from '../../common/math';

// ═══════════════════════════════════════════════════════════════════════════
// QUATERNION OPERATIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create an identity quaternion (no rotation)
 */
export function identityQuaternion(): Quaternion {
  return { w: 1, x: 0, y: 0, z: 0 };
}

/**
 * Normalize a quaternion to unit length
 */
export function normalizeQuaternion(q: Quaternion): Quaternion {
  const mag = Math.sqrt(q.w * q.w + q.x * q.x + q.y * q.y + q.z * q.z);
  if (mag === 0) return identityQuaternion();
  
  return {
    w: q.w / mag,
    x: q.x / mag,
    y: q.y / mag,
    z: q.z / mag
  };
}

/**
 * Multiply two quaternions (Hamilton product)
 */
export function multiplyQuaternions(a: Quaternion, b: Quaternion): Quaternion {
  return normalizeQuaternion({
    w: a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
    x: a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
    y: a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
    z: a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w
  });
}

/**
 * Conjugate of a quaternion
 */
export function conjugateQuaternion(q: Quaternion): Quaternion {
  return { w: q.w, x: -q.x, y: -q.y, z: -q.z };
}

/**
 * Spherical linear interpolation between quaternions
 */
export function slerpQuaternion(a: Quaternion, b: Quaternion, t: number): Quaternion {
  // Calculate cosine of angle between quaternions
  let cosHalfTheta = a.w * b.w + a.x * b.x + a.y * b.y + a.z * b.z;
  
  // If quaternions are opposite, flip one
  let bNorm = { ...b };
  if (cosHalfTheta < 0) {
    bNorm = { w: -b.w, x: -b.x, y: -b.y, z: -b.z };
    cosHalfTheta = -cosHalfTheta;
  }
  
  // If very close, use linear interpolation
  if (cosHalfTheta > 0.9999) {
    return normalizeQuaternion({
      w: a.w + t * (bNorm.w - a.w),
      x: a.x + t * (bNorm.x - a.x),
      y: a.y + t * (bNorm.y - a.y),
      z: a.z + t * (bNorm.z - a.z)
    });
  }
  
  const halfTheta = Math.acos(cosHalfTheta);
  const sinHalfTheta = Math.sqrt(1 - cosHalfTheta * cosHalfTheta);
  
  const ratioA = Math.sin((1 - t) * halfTheta) / sinHalfTheta;
  const ratioB = Math.sin(t * halfTheta) / sinHalfTheta;
  
  return normalizeQuaternion({
    w: a.w * ratioA + bNorm.w * ratioB,
    x: a.x * ratioA + bNorm.x * ratioB,
    y: a.y * ratioA + bNorm.y * ratioB,
    z: a.z * ratioA + bNorm.z * ratioB
  });
}

/**
 * Create rotation quaternion from axis-angle
 */
export function quaternionFromAxisAngle(
  axis: { x: number; y: number; z: number },
  angle: number
): Quaternion {
  const halfAngle = angle / 2;
  const sinHalfAngle = Math.sin(halfAngle);
  
  // Normalize axis
  const mag = Math.sqrt(axis.x * axis.x + axis.y * axis.y + axis.z * axis.z);
  const normAxis = mag > 0 ? {
    x: axis.x / mag,
    y: axis.y / mag,
    z: axis.z / mag
  } : { x: 0, y: 0, z: 1 };
  
  return normalizeQuaternion({
    w: Math.cos(halfAngle),
    x: normAxis.x * sinHalfAngle,
    y: normAxis.y * sinHalfAngle,
    z: normAxis.z * sinHalfAngle
  });
}

/**
 * Get rotation angle from quaternion
 */
export function quaternionToAngle(q: Quaternion): number {
  return 2 * Math.acos(Math.min(1, Math.abs(q.w)));
}

/**
 * Compute angular distance between two quaternions
 */
export function quaternionDistance(a: Quaternion, b: Quaternion): number {
  const dot = a.w * b.w + a.x * b.x + a.y * b.y + a.z * b.z;
  return Math.acos(Math.min(1, Math.abs(dot))) * 2;
}

// ═══════════════════════════════════════════════════════════════════════════
// BELIEF STATE DYNAMICS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Map belief probabilities to quaternion space
 * 
 * Maps a probability distribution to a point on the 3-sphere (quaternion space)
 */
export function beliefsToQuaternion(beliefs: BeliefState[]): Quaternion {
  if (beliefs.length === 0) return identityQuaternion();
  
  // Use first 4 belief probabilities as quaternion components
  // Normalize to ensure unit quaternion
  const probs = beliefs.slice(0, 4).map(b => b.probability);
  while (probs.length < 4) probs.push(0);
  
  return normalizeQuaternion({
    w: probs[0],
    x: probs[1],
    y: probs[2],
    z: probs[3]
  });
}

/**
 * Update quaternion based on prediction error
 * 
 * Large prediction errors cause larger rotations in belief space
 */
export function updateQuaternionFromError(
  current: Quaternion,
  predictionError: number,
  learningRate: number
): Quaternion {
  // Error magnitude determines rotation amount
  const errorMag = Math.min(Math.abs(predictionError), 1.0);
  const angle = errorMag * learningRate * Math.PI / 4; // Max 45 degrees
  
  // Error direction determines axis (using error as seed for reproducibility)
  const seed = Math.abs(predictionError * 1000) % 360;
  const axis = {
    x: Math.cos(seed * Math.PI / 180),
    y: Math.sin(seed * Math.PI / 180),
    z: Math.cos((seed + 90) * Math.PI / 180)
  };
  
  const rotation = quaternionFromAxisAngle(axis, angle);
  return multiplyQuaternions(current, rotation);
}

/**
 * Smooth belief transition using quaternion interpolation
 */
export function smoothBeliefTransition(
  currentBeliefs: BeliefState[],
  targetBeliefs: BeliefState[],
  transitionRate: number
): BeliefState[] {
  const currentQ = beliefsToQuaternion(currentBeliefs);
  const targetQ = beliefsToQuaternion(targetBeliefs);
  
  const interpolatedQ = slerpQuaternion(currentQ, targetQ, transitionRate);
  
  // Map back to beliefs
  const components = [interpolatedQ.w, interpolatedQ.x, interpolatedQ.y, interpolatedQ.z];
  
  // Ensure all positive and normalized
  const absComponents = components.map(c => Math.abs(c));
  const total = absComponents.reduce((a, b) => a + b, 0);
  const normalizedComponents = absComponents.map(c => c / total);
  
  return currentBeliefs.map((belief, i) => ({
    ...belief,
    probability: i < 4 ? normalizedComponents[i] : belief.probability * (1 - transitionRate),
    lastUpdated: Date.now()
  }));
}

// ═══════════════════════════════════════════════════════════════════════════
// ATTENTION DYNAMICS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Update attention based on beliefs and predictions
 */
export function updateAttention(
  attention: AttentionState,
  beliefs: BeliefState[],
  predictionError: number,
  learningRate: number
): AttentionState {
  // Higher prediction error increases precision (sharpen attention)
  const newPrecision = attention.precision * 
    (1 + learningRate * Math.abs(predictionError));
  
  // Update prime alignments based on strongest beliefs
  const sortedBeliefs = [...beliefs].sort((a, b) => b.probability - a.probability);
  const topBeliefs = sortedBeliefs.slice(0, 4);
  
  const newPrimeAlignments = topBeliefs.flatMap(b => b.primeFactors.slice(0, 2));
  
  return {
    ...attention,
    precision: Math.min(newPrecision, 10.0), // Cap precision
    primeAlignments: newPrimeAlignments.slice(0, 8) // Keep top 8 primes
  };
}

/**
 * Apply attention to beliefs (precision-weighted)
 */
export function applyAttention(
  beliefs: BeliefState[],
  attention: AttentionState
): BeliefState[] {
  // Calculate attention weights based on prime alignment
  const attentionWeights = beliefs.map(belief => {
    const primeOverlap = belief.primeFactors.filter(
      p => attention.primeAlignments.includes(p)
    ).length;
    
    return 1 + attention.precision * primeOverlap / 10;
  });
  
  // Apply weights
  const totalWeight = attentionWeights.reduce((a, b) => a + b, 0);
  
  return beliefs.map((belief, i) => ({
    ...belief,
    probability: (belief.probability * attentionWeights[i]) / totalWeight
  }));
}

// ═══════════════════════════════════════════════════════════════════════════
// BELIEF MANAGEMENT
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Create a new belief state
 */
export function createBelief(
  id: string,
  content: string,
  probability: number,
  primeFactors: number[]
): BeliefState {
  return {
    id,
    content,
    probability: Math.max(0, Math.min(1, probability)),
    entropy: probability > 0 ? -probability * Math.log2(probability) : 0,
    precision: 1.0,
    primeFactors,
    lastUpdated: Date.now()
  };
}

/**
 * Prune beliefs with very low probability
 */
export function pruneBeliefs(
  beliefs: BeliefState[],
  threshold: number = 0.01,
  maxBeliefs: number = 20
): BeliefState[] {
  // Filter out low probability beliefs
  const filtered = beliefs.filter(b => b.probability >= threshold);
  
  // Sort by probability and take top N
  const sorted = filtered.sort((a, b) => b.probability - a.probability);
  const pruned = sorted.slice(0, maxBeliefs);
  
  // Renormalize
  const total = pruned.reduce((acc, b) => acc + b.probability, 0);
  return pruned.map(b => ({
    ...b,
    probability: b.probability / total
  }));
}

/**
 * Merge similar beliefs
 */
export function mergeBeliefs(
  beliefs: BeliefState[],
  similarityThreshold: number = 0.9
): BeliefState[] {
  const merged: BeliefState[] = [];
  const used = new Set<string>();
  
  for (const belief of beliefs) {
    if (used.has(belief.id)) continue;
    
    // Find similar beliefs
    const similar = beliefs.filter(b => 
      !used.has(b.id) && 
      b.id !== belief.id && 
      calculateBeliefSimilarity(belief, b) >= similarityThreshold
    );
    
    if (similar.length === 0) {
      merged.push(belief);
      used.add(belief.id);
    } else {
      // Merge all similar beliefs
      const allSimilar = [belief, ...similar];
      const totalProb = allSimilar.reduce((acc, b) => acc + b.probability, 0);
      
      // Combine prime factors
      const allPrimes = new Set<number>();
      allSimilar.forEach(b => b.primeFactors.forEach(p => allPrimes.add(p)));
      
      merged.push({
        ...belief,
        probability: totalProb,
        primeFactors: Array.from(allPrimes),
        lastUpdated: Date.now()
      });
      
      allSimilar.forEach(b => used.add(b.id));
    }
  }
  
  return merged;
}

/**
 * Calculate similarity between two beliefs
 */
export function calculateBeliefSimilarity(a: BeliefState, b: BeliefState): number {
  // Prime factor overlap (Jaccard similarity)
  const aPrimes = new Set(a.primeFactors);
  const bPrimes = new Set(b.primeFactors);
  
  const intersection = new Set([...aPrimes].filter(p => bPrimes.has(p)));
  const union = new Set([...aPrimes, ...bPrimes]);
  
  if (union.size === 0) return 0;
  return intersection.size / union.size;
}
