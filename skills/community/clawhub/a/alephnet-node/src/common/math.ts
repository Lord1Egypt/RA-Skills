/**
 * Mathematical Utilities
 * 
 * Common mathematical operations used across the AlephNet codebase.
 * Includes vector operations, statistics, and numeric utilities.
 */

import { SMFVector, SemanticDomain, DOMAIN_RANGES, SMFAxisIndex } from './types';

// ═══════════════════════════════════════════════════════════════════════════
// VECTOR OPERATIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Calculate dot product of two vectors
 */
export function dotProduct(a: number[], b: number[]): number {
  if (a.length !== b.length) {
    throw new Error(`Vector length mismatch: ${a.length} vs ${b.length}`);
  }
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    sum += a[i] * b[i];
  }
  return sum;
}

/**
 * Calculate vector magnitude (L2 norm)
 */
export function magnitude(v: number[]): number {
  let sum = 0;
  for (let i = 0; i < v.length; i++) {
    sum += v[i] * v[i];
  }
  return Math.sqrt(sum);
}

/**
 * Normalize a vector to unit length
 */
export function normalize(v: number[]): number[] {
  const mag = magnitude(v);
  if (mag === 0) return v.slice(); // Return copy of zero vector
  return v.map(val => val / mag);
}

/**
 * Calculate cosine similarity between two vectors
 */
export function cosineSimilarity(a: number[], b: number[]): number {
  const magA = magnitude(a);
  const magB = magnitude(b);
  if (magA === 0 || magB === 0) return 0;
  return dotProduct(a, b) / (magA * magB);
}

/**
 * Calculate Euclidean distance between two vectors
 */
export function euclideanDistance(a: number[], b: number[]): number {
  if (a.length !== b.length) {
    throw new Error(`Vector length mismatch: ${a.length} vs ${b.length}`);
  }
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    const diff = a[i] - b[i];
    sum += diff * diff;
  }
  return Math.sqrt(sum);
}

/**
 * Add two vectors element-wise
 */
export function vectorAdd(a: number[], b: number[]): number[] {
  if (a.length !== b.length) {
    throw new Error(`Vector length mismatch: ${a.length} vs ${b.length}`);
  }
  return a.map((val, i) => val + b[i]);
}

/**
 * Subtract two vectors element-wise (a - b)
 */
export function vectorSubtract(a: number[], b: number[]): number[] {
  if (a.length !== b.length) {
    throw new Error(`Vector length mismatch: ${a.length} vs ${b.length}`);
  }
  return a.map((val, i) => val - b[i]);
}

/**
 * Scale a vector by a scalar
 */
export function vectorScale(v: number[], scalar: number): number[] {
  return v.map(val => val * scalar);
}

/**
 * Element-wise multiplication of two vectors
 */
export function vectorMultiply(a: number[], b: number[]): number[] {
  if (a.length !== b.length) {
    throw new Error(`Vector length mismatch: ${a.length} vs ${b.length}`);
  }
  return a.map((val, i) => val * b[i]);
}

/**
 * Calculate mean of a vector
 */
export function vectorMean(v: number[]): number {
  if (v.length === 0) return 0;
  return v.reduce((sum, val) => sum + val, 0) / v.length;
}

/**
 * Calculate mean of multiple vectors (element-wise)
 */
export function vectorsMean(vectors: number[][]): number[] {
  if (vectors.length === 0) return [];
  const dim = vectors[0].length;
  const result = new Array(dim).fill(0);
  
  for (const v of vectors) {
    for (let i = 0; i < dim; i++) {
      result[i] += v[i];
    }
  }
  
  return result.map(val => val / vectors.length);
}

/**
 * Create a zero vector of specified length
 */
export function zeroVector(length: number): number[] {
  return new Array(length).fill(0);
}

/**
 * Create a zero SMF vector
 */
export function zeroSMF(): SMFVector {
  return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
}

/**
 * Create a random SMF vector (normalized)
 */
export function randomSMF(): SMFVector {
  const v: number[] = [];
  for (let i = 0; i < 16; i++) {
    v.push(Math.random() * 2 - 1); // -1 to 1
  }
  const normalized = normalize(v);
  return normalized as SMFVector;
}

// ═══════════════════════════════════════════════════════════════════════════
// SMF-SPECIFIC OPERATIONS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Extract a domain slice from an SMF vector
 */
export function extractDomain(smf: SMFVector, domain: SemanticDomain): number[] {
  const [start, end] = DOMAIN_RANGES[domain];
  return smf.slice(start, end + 1);
}

/**
 * Calculate domain magnitudes for an SMF vector
 */
export function domainMagnitudes(smf: SMFVector): Record<SemanticDomain, number> {
  return {
    perceptual: magnitude(extractDomain(smf, 'perceptual')),
    cognitive: magnitude(extractDomain(smf, 'cognitive')),
    temporal: magnitude(extractDomain(smf, 'temporal')),
    meta: magnitude(extractDomain(smf, 'meta'))
  };
}

/**
 * Determine the primary semantic domain of an SMF vector
 */
export function determineDomain(smf: SMFVector): SemanticDomain {
  const mags = domainMagnitudes(smf);
  let maxDomain: SemanticDomain = 'cognitive';
  let maxMag = 0;
  
  for (const [domain, mag] of Object.entries(mags)) {
    if (mag > maxMag) {
      maxMag = mag;
      maxDomain = domain as SemanticDomain;
    }
  }
  
  return maxDomain;
}

/**
 * Find secondary domains above a threshold relative to primary
 */
export function findSecondaryDomains(smf: SMFVector, threshold = 0.5): SemanticDomain[] {
  const mags = domainMagnitudes(smf);
  const primary = determineDomain(smf);
  const maxMag = mags[primary];
  
  if (maxMag === 0) return [];
  
  return (Object.entries(mags) as [SemanticDomain, number][])
    .filter(([domain, mag]) => domain !== primary && mag >= maxMag * threshold)
    .map(([domain]) => domain);
}

/**
 * Calculate alignment between SMF vector and specific axes
 */
export function axisAlignment(smf: SMFVector, axes: SMFAxisIndex[]): number {
  if (axes.length === 0) return 0;
  
  let alignmentMag = 0;
  let totalMag = 0;
  
  for (let i = 0; i < 16; i++) {
    const absMag = Math.abs(smf[i]);
    totalMag += absMag;
    if (axes.includes(i as SMFAxisIndex)) {
      alignmentMag += absMag;
    }
  }
  
  return totalMag > 0 ? alignmentMag / totalMag : 0;
}

// ═══════════════════════════════════════════════════════════════════════════
// QUATERNION OPERATIONS
// ═══════════════════════════════════════════════════════════════════════════

export interface Quaternion {
  w: number;
  x: number;
  y: number;
  z: number;
}

/**
 * Create identity quaternion
 */
export function quaternionIdentity(): Quaternion {
  return { w: 1, x: 0, y: 0, z: 0 };
}

/**
 * Normalize a quaternion
 */
export function quaternionNormalize(q: Quaternion): Quaternion {
  const mag = Math.sqrt(q.w * q.w + q.x * q.x + q.y * q.y + q.z * q.z);
  if (mag === 0) return quaternionIdentity();
  return {
    w: q.w / mag,
    x: q.x / mag,
    y: q.y / mag,
    z: q.z / mag
  };
}

/**
 * Quaternion multiplication (Hamilton product)
 */
export function quaternionMultiply(a: Quaternion, b: Quaternion): Quaternion {
  return {
    w: a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z,
    x: a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y,
    y: a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x,
    z: a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w
  };
}

/**
 * Create rotation quaternion from axis and angle
 */
export function quaternionFromAxisAngle(axis: [number, number, number], angleRadians: number): Quaternion {
  const halfAngle = angleRadians / 2;
  const s = Math.sin(halfAngle);
  const normalized = normalize(axis);
  return {
    w: Math.cos(halfAngle),
    x: normalized[0] * s,
    y: normalized[1] * s,
    z: normalized[2] * s
  };
}

/**
 * Spherical linear interpolation between quaternions
 */
export function quaternionSlerp(a: Quaternion, b: Quaternion, t: number): Quaternion {
  // Compute dot product
  let dot = a.w * b.w + a.x * b.x + a.y * b.y + a.z * b.z;
  
  // If negative dot, negate one quaternion to take shortest path
  let bNeg = b;
  if (dot < 0) {
    bNeg = { w: -b.w, x: -b.x, y: -b.y, z: -b.z };
    dot = -dot;
  }
  
  // Clamp dot to valid range
  dot = Math.min(Math.max(dot, -1), 1);
  
  const theta = Math.acos(dot);
  const sinTheta = Math.sin(theta);
  
  let s0: number, s1: number;
  if (sinTheta < 0.001) {
    // Linear interpolation for small angles
    s0 = 1 - t;
    s1 = t;
  } else {
    s0 = Math.sin((1 - t) * theta) / sinTheta;
    s1 = Math.sin(t * theta) / sinTheta;
  }
  
  return {
    w: s0 * a.w + s1 * bNeg.w,
    x: s0 * a.x + s1 * bNeg.x,
    y: s0 * a.y + s1 * bNeg.y,
    z: s0 * a.z + s1 * bNeg.z
  };
}

// ═══════════════════════════════════════════════════════════════════════════
// STATISTICS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Calculate variance of values
 */
export function variance(values: number[]): number {
  if (values.length === 0) return 0;
  const mean = vectorMean(values);
  return values.reduce((sum, val) => sum + (val - mean) ** 2, 0) / values.length;
}

/**
 * Calculate standard deviation
 */
export function standardDeviation(values: number[]): number {
  return Math.sqrt(variance(values));
}

/**
 * Calculate entropy of a probability distribution
 */
export function entropy(probabilities: number[]): number {
  let sum = 0;
  for (const p of probabilities) {
    if (p > 0) {
      sum -= p * Math.log2(p);
    }
  }
  return sum;
}

/**
 * Softmax function
 */
export function softmax(values: number[]): number[] {
  const max = Math.max(...values);
  const exps = values.map(v => Math.exp(v - max)); // Subtract max for numerical stability
  const sum = exps.reduce((a, b) => a + b, 0);
  return exps.map(e => e / sum);
}

/**
 * Sigmoid function
 */
export function sigmoid(x: number): number {
  return 1 / (1 + Math.exp(-x));
}

/**
 * Hyperbolic tangent (for SMF normalization)
 */
export function tanh(x: number): number {
  return Math.tanh(x);
}

// ═══════════════════════════════════════════════════════════════════════════
// NUMERIC UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Clamp a value between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

/**
 * Linear interpolation
 */
export function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t;
}

/**
 * Round to specified decimal places
 */
export function roundTo(value: number, decimals: number): number {
  const factor = 10 ** decimals;
  return Math.round(value * factor) / factor;
}

/**
 * Check if two floats are approximately equal
 */
export function approximately(a: number, b: number, epsilon = 1e-6): number {
  return Math.abs(a - b) < epsilon ? 1 : 0;
}

/**
 * Generate a random integer between min and max (inclusive)
 */
export function randomInt(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Generate a random float between min and max
 */
export function randomFloat(min: number, max: number): number {
  return Math.random() * (max - min) + min;
}
