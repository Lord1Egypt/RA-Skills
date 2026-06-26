/**
 * SRIA Engine - Self-Reflective Intelligence Architecture
 * 
 * Main orchestrator for Active Inference-based agent cognition.
 * Coordinates perception, belief updates, policy selection, and action.
 */

import {
  SRIASessionState,
  BeliefState,
  Policy,
  ActionOutcome,
  GenerativeModelParams,
  SRIAEvent,
  SRIAEventHandler,
  AttentionState
} from './types';
import { SRIALifecycleState } from '../../common/types';
import { Quaternion } from '../../common/math';
import {
  calculateVariationalFreeEnergy,
  calculateSurprisal,
  updateBeliefs,
  normalizeBeliefs,
  calculateBeliefEntropy
} from './FreeEnergy';
import {
  identityQuaternion,
  updateQuaternionFromError,
  smoothBeliefTransition,
  updateAttention,
  applyAttention,
  createBelief,
  pruneBeliefs,
  mergeBeliefs
} from './BeliefDynamics';
import {
  generatePolicies,
  evaluatePolicies,
  selectPolicy,
  getDefaultPoliciesForState,
  refinePolicyFromOutcome
} from './PolicySelection';
import { generateId } from '../../common/hash';
import { createLogger } from '../../common/logging';

const logger = createLogger('SRIAEngine');

// ═══════════════════════════════════════════════════════════════════════════
// DEFAULT PARAMETERS
// ═══════════════════════════════════════════════════════════════════════════

const DEFAULT_MODEL_PARAMS: GenerativeModelParams = {
  priorPrecision: 1.0,
  likelihoodPrecision: 2.0,
  learningRate: 0.1,
  explorationBonus: 0.3,
  goalWeight: 0.7
};

// ═══════════════════════════════════════════════════════════════════════════
// SRIA ENGINE CLASS
// ═══════════════════════════════════════════════════════════════════════════

export class SRIAEngine {
  private state: SRIASessionState | null = null;
  private eventHandlers: Set<SRIAEventHandler> = new Set();
  private goalState: number[] = [];
  private policyHistory: Policy[] = [];
  private maxHistoryLength = 100;
  
  constructor(private modelParams: GenerativeModelParams = DEFAULT_MODEL_PARAMS) {}
  
  // ═══════════════════════════════════════════════════════════════════════
  // SESSION MANAGEMENT
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Initialize a new SRIA session
   */
  async initializeSession(
    sessionId: string,
    bodyHash?: string
  ): Promise<SRIASessionState> {
    logger.info('Initializing SRIA session', { sessionId });
    
    this.state = {
      sessionId,
      lifecycleState: 'DORMANT',
      bodyHash: bodyHash || generateId('body'),
      quaternionState: identityQuaternion(),
      currentBeliefs: [],
      freeEnergy: 1.0,
      surprisal: 0,
      entropy: 0,
      currentEpoch: 0,
      entropyTrajectory: [],
      freeEnergyTrajectory: [1.0],
      attention: {
        focusLayer: 'input',
        layerWeights: {},
        primeAlignments: [],
        precision: 1.0
      },
      modelParams: { ...this.modelParams },
      predictions: []
    };
    
    this.emitEvent('state_change', { newState: 'DORMANT' });
    return this.state;
  }
  
  /**
   * Get current session state
   */
  getState(): SRIASessionState | null {
    return this.state;
  }
  
  /**
   * Set the goal state for pragmatic value calculation
   */
  setGoalState(goal: number[]): void {
    this.goalState = goal;
    logger.debug('Goal state updated', { dimensions: goal.length });
  }
  
  /**
   * Update model parameters
   */
  setModelParams(params: Partial<GenerativeModelParams>): void {
    if (this.state) {
      this.state.modelParams = { ...this.state.modelParams, ...params };
    }
    this.modelParams = { ...this.modelParams, ...params };
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // LIFECYCLE STATE MACHINE
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Transition to a new lifecycle state
   */
  private transitionTo(newState: SRIALifecycleState): void {
    if (!this.state) return;
    
    const oldState = this.state.lifecycleState;
    this.state.lifecycleState = newState;
    
    logger.debug('State transition', { from: oldState, to: newState });
    this.emitEvent('state_change', { oldState, newState });
  }
  
  /**
   * Check if transition is valid
   */
  private canTransition(from: SRIALifecycleState, to: SRIALifecycleState): boolean {
    const validTransitions: Record<SRIALifecycleState, SRIALifecycleState[]> = {
      DORMANT: ['PERCEIVING'],
      PERCEIVING: ['DECIDING', 'CONSOLIDATING'],
      DECIDING: ['ACTING', 'PERCEIVING'],
      ACTING: ['LEARNING'],
      LEARNING: ['PERCEIVING', 'CONSOLIDATING', 'DECIDING'],
      CONSOLIDATING: ['SLEEPING', 'DORMANT'],
      SLEEPING: ['DORMANT', 'PERCEIVING']
    };
    
    return validTransitions[from]?.includes(to) ?? false;
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // ACTIVE INFERENCE CYCLE
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Run a complete Active Inference cycle
   */
  async runCycle(observation: number[]): Promise<{
    policy: Policy | null;
    freeEnergy: number;
    beliefs: BeliefState[];
  }> {
    if (!this.state) {
      throw new Error('SRIA session not initialized');
    }
    
    logger.debug('Running SRIA cycle', { epoch: this.state.currentEpoch });
    
    // 1. Perception Phase
    this.transitionTo('PERCEIVING');
    await this.perceive(observation);
    
    // 2. Decision Phase
    this.transitionTo('DECIDING');
    const policy = await this.decide();
    
    // Store result before potential action
    const result = {
      policy,
      freeEnergy: this.state.freeEnergy,
      beliefs: [...this.state.currentBeliefs]
    };
    
    // Update epoch
    this.state.currentEpoch++;
    
    return result;
  }
  
  /**
   * Perception phase: update beliefs based on observation
   */
  async perceive(observation: number[]): Promise<void> {
    if (!this.state) return;
    
    logger.debug('Perceiving', { observationDims: observation.length });
    
    // Calculate surprisal of observation
    this.state.surprisal = calculateSurprisal(
      observation, 
      this.state.currentBeliefs
    );
    
    // Update beliefs based on observation
    if (this.state.currentBeliefs.length > 0) {
      this.state.currentBeliefs = updateBeliefs(
        this.state.currentBeliefs,
        observation,
        this.state.modelParams.learningRate
      );
    } else {
      // Initialize beliefs from observation
      this.state.currentBeliefs = this.initializeBeliefsFromObservation(observation);
    }
    
    // Apply attention weighting
    this.state.currentBeliefs = applyAttention(
      this.state.currentBeliefs,
      this.state.attention
    );
    
    // Normalize and prune
    this.state.currentBeliefs = normalizeBeliefs(this.state.currentBeliefs);
    this.state.currentBeliefs = pruneBeliefs(this.state.currentBeliefs);
    
    // Calculate new free energy
    const newFreeEnergy = calculateVariationalFreeEnergy(
      this.state.currentBeliefs,
      observation,
      this.state.modelParams
    );
    
    // Update trajectories
    this.state.freeEnergy = newFreeEnergy;
    this.state.freeEnergyTrajectory.push(newFreeEnergy);
    
    this.state.entropy = calculateBeliefEntropy(this.state.currentBeliefs);
    this.state.entropyTrajectory.push(this.state.entropy);
    
    // Keep trajectories bounded
    if (this.state.freeEnergyTrajectory.length > this.maxHistoryLength) {
      this.state.freeEnergyTrajectory.shift();
    }
    if (this.state.entropyTrajectory.length > this.maxHistoryLength) {
      this.state.entropyTrajectory.shift();
    }
    
    this.emitEvent('free_energy_update', { freeEnergy: newFreeEnergy });
  }
  
  /**
   * Decision phase: select policy based on expected free energy
   */
  async decide(): Promise<Policy | null> {
    if (!this.state) return null;
    
    // Get available actions for current state
    const availableActions = getDefaultPoliciesForState(this.state.lifecycleState);
    
    // Generate candidate policies
    const policies = generatePolicies(
      this.state.currentBeliefs,
      this.state.freeEnergy,
      availableActions
    );
    
    // Evaluate policies
    const evaluatedPolicies = evaluatePolicies(
      policies,
      this.state.currentBeliefs,
      this.goalState,
      this.state.modelParams
    );
    
    // Select best policy
    const explorationTemp = this.calculateExplorationTemperature();
    const selectedPolicy = selectPolicy(evaluatedPolicies, explorationTemp);
    
    if (selectedPolicy) {
      logger.debug('Policy selected', { 
        type: selectedPolicy.type, 
        efe: selectedPolicy.expectedFreeEnergy 
      });
      
      this.policyHistory.push(selectedPolicy);
      if (this.policyHistory.length > this.maxHistoryLength) {
        this.policyHistory.shift();
      }
      
      this.emitEvent('policy_selected', { policy: selectedPolicy });
    }
    
    return selectedPolicy;
  }
  
  /**
   * Action phase: execute the selected policy
   */
  async act(policy: Policy): Promise<ActionOutcome> {
    if (!this.state) {
      throw new Error('SRIA session not initialized');
    }
    
    this.transitionTo('ACTING');
    logger.debug('Executing policy', { type: policy.type });
    
    // Generate predictions for this action
    const prediction = this.state.currentBeliefs.flatMap(b => b.primeFactors);
    this.state.predictions.push({
      id: generateId('pred'),
      content: prediction,
      probability: 0.5,
      precision: 1.0,
      generated: Date.now()
    });
    
    // Return placeholder outcome - actual execution handled externally
    return {
      policyId: policy.id,
      success: true,
      predictionError: 0,
      information: 0,
      beliefUpdate: [],
      smfDelta: []
    };
  }
  
  /**
   * Learning phase: update beliefs based on action outcome
   */
  async learn(outcome: ActionOutcome): Promise<void> {
    if (!this.state) return;
    
    this.transitionTo('LEARNING');
    logger.debug('Learning from outcome', { 
      policyId: outcome.policyId, 
      error: outcome.predictionError 
    });
    
    // Update quaternion based on prediction error
    this.state.quaternionState = updateQuaternionFromError(
      this.state.quaternionState,
      outcome.predictionError,
      this.state.modelParams.learningRate
    );
    
    // Update attention based on outcome
    this.state.attention = updateAttention(
      this.state.attention,
      this.state.currentBeliefs,
      outcome.predictionError,
      this.state.modelParams.learningRate
    );
    
    // Merge similar beliefs
    this.state.currentBeliefs = mergeBeliefs(this.state.currentBeliefs);
    
    // Apply belief updates from outcome
    if (outcome.beliefUpdate.length > 0) {
      for (const update of outcome.beliefUpdate) {
        const existing = this.state.currentBeliefs.find(b => b.id === update.id);
        if (existing) {
          Object.assign(existing, update);
        } else {
          this.state.currentBeliefs.push(update);
        }
      }
      this.state.currentBeliefs = normalizeBeliefs(this.state.currentBeliefs);
    }
    
    // Update policy based on outcome
    const lastPolicy = this.policyHistory[this.policyHistory.length - 1];
    if (lastPolicy) {
      const refinedPolicy = refinePolicyFromOutcome(
        lastPolicy,
        outcome,
        this.state.modelParams.learningRate
      );
      this.policyHistory[this.policyHistory.length - 1] = refinedPolicy;
    }
    
    this.emitEvent('action_complete', { outcome });
    
    if (outcome.predictionError > 0.1) {
      this.emitEvent('prediction_error', { 
        error: outcome.predictionError,
        policyId: outcome.policyId
      });
    }
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // CONSOLIDATION & SLEEP
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Consolidation phase: sync insights to long-term memory
   */
  async consolidate(): Promise<{ insights: BeliefState[] }> {
    if (!this.state) {
      throw new Error('SRIA session not initialized');
    }
    
    this.transitionTo('CONSOLIDATING');
    logger.debug('Consolidating beliefs');
    
    // Get high-confidence beliefs for GMF contribution
    const insights = this.state.currentBeliefs
      .filter(b => b.probability > 0.7 && b.entropy < 0.3)
      .map(b => ({ ...b }));
    
    // Prune old predictions
    const now = Date.now();
    this.state.predictions = this.state.predictions.filter(
      p => now - p.generated < 60000 // Keep last minute
    );
    
    this.emitEvent('consolidation_complete', { insights });
    return { insights };
  }
  
  /**
   * Sleep phase: background processing and memory consolidation
   */
  async sleep(duration: number = 1): Promise<void> {
    if (!this.state) return;
    
    this.transitionTo('SLEEPING');
    logger.debug('Entering sleep phase', { duration });
    
    // Simulate sleep processing
    await new Promise(resolve => setTimeout(resolve, duration));
    
    // Reset some state
    this.state.freeEnergy = Math.max(0.5, this.state.freeEnergy * 0.9);
    this.state.attention.precision = 1.0;
    
    // Wake up
    this.transitionTo('DORMANT');
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // HELPER METHODS
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Initialize beliefs from observation
   */
  private initializeBeliefsFromObservation(observation: number[]): BeliefState[] {
    // Create initial beliefs based on observation structure
    const numBeliefs = Math.min(8, Math.ceil(observation.length / 4));
    const beliefs: BeliefState[] = [];
    
    for (let i = 0; i < numBeliefs; i++) {
      const startIdx = i * 4;
      const primes = observation.slice(startIdx, startIdx + 4);
      
      beliefs.push(createBelief(
        generateId(`belief-${i}`),
        `Initial belief ${i}`,
        1 / numBeliefs,
        primes.length > 0 ? primes : [2, 3, 5, 7]
      ));
    }
    
    return beliefs;
  }
  
  /**
   * Calculate exploration temperature based on trajectory
   */
  private calculateExplorationTemperature(): number {
    if (!this.state) return 1.0;
    
    // High free energy = more exploration
    // Low free energy = more exploitation
    const fe = this.state.freeEnergy;
    
    // Also consider trajectory - if stuck, increase exploration
    const trajectory = this.state.freeEnergyTrajectory.slice(-5);
    const isStuck = trajectory.length >= 5 && 
      Math.max(...trajectory) - Math.min(...trajectory) < 0.05;
    
    let temp = 0.5 + fe * 0.5; // Base temperature
    
    if (isStuck) {
      temp *= 1.5; // Increase exploration if stuck
    }
    
    return Math.max(0.1, Math.min(2.0, temp));
  }
  
  /**
   * Add a belief to the current state
   */
  addBelief(
    content: string,
    probability: number,
    primeFactors: number[]
  ): BeliefState | null {
    if (!this.state) return null;
    
    const belief = createBelief(
      generateId('belief'),
      content,
      probability,
      primeFactors
    );
    
    this.state.currentBeliefs.push(belief);
    this.state.currentBeliefs = normalizeBeliefs(this.state.currentBeliefs);
    
    this.emitEvent('belief_update', { belief });
    return belief;
  }
  
  /**
   * Get free energy trend
   */
  getFreeEnergyTrend(): 'decreasing' | 'stable' | 'increasing' {
    if (!this.state) return 'stable';
    
    const trajectory = this.state.freeEnergyTrajectory.slice(-5);
    if (trajectory.length < 2) return 'stable';
    
    const first = trajectory[0];
    const last = trajectory[trajectory.length - 1];
    const diff = last - first;
    
    if (diff < -0.1) return 'decreasing';
    if (diff > 0.1) return 'increasing';
    return 'stable';
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // EVENT SYSTEM
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Subscribe to SRIA events
   */
  on(handler: SRIAEventHandler): () => void {
    this.eventHandlers.add(handler);
    return () => this.eventHandlers.delete(handler);
  }
  
  /**
   * Emit an event
   */
  private emitEvent(type: SRIAEvent['type'], data: unknown): void {
    if (!this.state) return;
    
    const event: SRIAEvent = {
      type,
      timestamp: Date.now(),
      sessionId: this.state.sessionId,
      data
    };
    
    for (const handler of this.eventHandlers) {
      try {
        handler(event);
      } catch (error) {
        logger.error('Event handler error', error as Error);
      }
    }
  }
}
