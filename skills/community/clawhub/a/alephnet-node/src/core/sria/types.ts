/**
 * SRIA (Self-Reflective Intelligence Architecture) Types
 * 
 * Core type definitions for the Active Inference engine.
 */

import { SRIALifecycleState, SMFVector } from '../../common/types';
import { Quaternion } from '../../common/math';

// ═══════════════════════════════════════════════════════════════════════════
// LIFECYCLE
// ═══════════════════════════════════════════════════════════════════════════

// SRIALifecycleState imported from common

// ═══════════════════════════════════════════════════════════════════════════
// QUATERNION & BELIEF STATE
// ═══════════════════════════════════════════════════════════════════════════

// Quaternion imported from common

export interface BeliefState {
  id: string;
  content: string;
  probability: number;        // P(belief | evidence)
  entropy: number;            // -sum(p * log(p)) for sub-beliefs
  precision: number;          // Inverse variance (confidence)
  primeFactors: number[];     // Semantic prime encoding
  lastUpdated: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// ATTENTION
// ═══════════════════════════════════════════════════════════════════════════

export interface AttentionState {
  focusLayer: string;                    // Current focus of attention
  layerWeights: Record<string, number>;  // Attention weights per layer
  primeAlignments: number[];             // Prime-aligned attention vector
  precision: number;                     // Precision of attention
}

// ═══════════════════════════════════════════════════════════════════════════
// POLICY & ACTION
// ═══════════════════════════════════════════════════════════════════════════

export type PolicyType = 
  | 'PERCEIVE'      // Gather more information
  | 'THINK'         // Internal reasoning
  | 'RESPOND'       // Generate response
  | 'TOOL_CALL'     // Invoke a tool
  | 'QUERY'         // Ask clarifying question
  | 'CONSOLIDATE'   // Sync to memory
  | 'SLEEP';        // Enter sleep state

export interface Policy {
  id: string;
  type: PolicyType;
  parameters: Record<string, unknown>;
  expectedFreeEnergy: number;  // G(π) - lower is better
  epistemic: number;           // Information gain component
  pragmatic: number;           // Goal-directed component
  risk: number;                // Risk/ambiguity component
}

export interface ActionOutcome {
  policyId: string;
  success: boolean;
  predictionError: number;     // Difference between expected and actual
  information: number;         // Bits of information gained
  beliefUpdate: BeliefState[]; // Updated beliefs
  smfDelta: number[];          // Change in SMF vector
}

// ═══════════════════════════════════════════════════════════════════════════
// GENERATIVE MODEL
// ═══════════════════════════════════════════════════════════════════════════

export interface GenerativeModelParams {
  priorPrecision: number;      // Precision of prior beliefs
  likelihoodPrecision: number; // Precision of sensory data
  learningRate: number;        // Rate of belief updates
  explorationBonus: number;    // Bonus for epistemic value
  goalWeight: number;          // Weight for pragmatic value
}

export interface Prediction {
  id: string;
  content: unknown;
  probability: number;
  precision: number;
  generated: number;
}

// ═══════════════════════════════════════════════════════════════════════════
// SESSION STATE
// ═══════════════════════════════════════════════════════════════════════════

export interface SRIASessionState {
  sessionId: string;
  lifecycleState: SRIALifecycleState;
  
  // Identity
  bodyHash: string;              // Hash of agent embodiment
  
  // Belief dynamics
  quaternionState: Quaternion;   // Rotation in belief space
  currentBeliefs: BeliefState[];
  
  // Free energy
  freeEnergy: number;            // Current variational free energy
  surprisal: number;             // -log P(observation)
  entropy: number;               // Belief entropy
  
  // History
  currentEpoch: number;
  entropyTrajectory: number[];   // History of entropy values
  freeEnergyTrajectory: number[];// History of free energy
  
  // Attention
  attention: AttentionState;
  
  // Model parameters
  modelParams: GenerativeModelParams;
  
  // Predictions
  predictions: Prediction[];
}

// ═══════════════════════════════════════════════════════════════════════════
// EVENTS
// ═══════════════════════════════════════════════════════════════════════════

export type SRIAEventType = 
  | 'state_change'
  | 'belief_update'
  | 'policy_selected'
  | 'action_complete'
  | 'prediction_error'
  | 'free_energy_update'
  | 'consolidation_complete';

export interface SRIAEvent {
  type: SRIAEventType;
  timestamp: number;
  sessionId: string;
  data: unknown;
}

export type SRIAEventHandler = (event: SRIAEvent) => void;
