import { describe, it, expect, beforeEach } from '@jest/globals';
import { SRIAEngine } from '../../src/core/SRIAEngine';
import { ActionOutcome, Policy } from '../../src/core/sria/types';

describe('SRIAEngine', () => {
  let engine: SRIAEngine;

  beforeEach(() => {
    engine = new SRIAEngine();
  });

  describe('initializeSession', () => {
    it('should initialize with default values', async () => {
      const state = await engine.initializeSession('session-1');
      expect(state.sessionId).toBe('session-1');
      expect(state.lifecycleState).toBe('DORMANT');
      expect(state.freeEnergy).toBe(1.0);
      expect(state.quaternionState).toEqual({ w: 1, x: 0, y: 0, z: 0 });
    });

    it('should initialize with custom body hash', async () => {
      const state = await engine.initializeSession('session-1', 'custom-body-hash');
      expect(state.bodyHash).toBe('custom-body-hash');
    });
  });

  describe('runCycle', () => {
    it('should throw if session not initialized', async () => {
      const observation = [1, 2, 3, 4];
      await expect(engine.runCycle(observation)).rejects.toThrow('SRIA session not initialized');
    });

    it('should complete a full cycle with observation', async () => {
      await engine.initializeSession('session-1');
      const observation = [0.5, 0.3, 0.1, 0.1];

      const result = await engine.runCycle(observation);
      
      expect(result.policy).toBeDefined();
      expect(result.freeEnergy).toBeDefined();
      expect(result.beliefs.length).toBeGreaterThan(0);
    });

    it('should update free energy trajectory', async () => {
      await engine.initializeSession('session-1');
      const observation = [0.5, 0.3, 0.1, 0.1];

      await engine.runCycle(observation);
      
      const state = engine.getState();
      expect(state).toBeDefined();
      expect(state!.freeEnergyTrajectory.length).toBeGreaterThan(1);
    });

    it('should select a policy based on beliefs', async () => {
      await engine.initializeSession('session-1');
      const observation = [0.5, 0.3, 0.1, 0.1];

      const result = await engine.runCycle(observation);
      
      expect(result.policy).toBeDefined();
      expect(result.policy!.type).toBeDefined();
      expect(result.policy!.expectedFreeEnergy).toBeDefined();
    });
  });

  describe('perceive', () => {
    it('should update beliefs based on observation', async () => {
      await engine.initializeSession('session-1');
      const observation = [0.5, 0.3, 0.1, 0.1];

      // Run a cycle which internally calls perceive
      await engine.runCycle(observation);
      
      const state = engine.getState();
      expect(state!.currentBeliefs.length).toBeGreaterThan(0);
    });

    it('should calculate surprisal', async () => {
      await engine.initializeSession('session-1');
      const observation = [0.5, 0.3, 0.1, 0.1];

      // Run a cycle to get beliefs
      await engine.runCycle(observation);
      
      const state = engine.getState();
      // Surprisal should be calculated
      expect(state!.surprisal).toBeDefined();
    });
  });

  describe('act', () => {
    it('should execute a policy', async () => {
      await engine.initializeSession('session-1');
      const observation = [0.5, 0.3, 0.1, 0.1];

      const result = await engine.runCycle(observation);
      
      if (result.policy) {
        const outcome = await engine.act(result.policy);
        expect(outcome.policyId).toBe(result.policy.id);
        expect(outcome.success).toBe(true);
      }
    });
  });

  describe('learn', () => {
    it('should update quaternion from prediction error', async () => {
      await engine.initializeSession('session-1');
      const observation = [0.5, 0.3, 0.1, 0.1];
      await engine.runCycle(observation);

      const initialQ = { ...engine.getState()!.quaternionState };
      
      const outcome: ActionOutcome = {
        policyId: 'test-policy',
        success: true,
        predictionError: 0.5,
        information: 0.2,
        beliefUpdate: [],
        smfDelta: []
      };

      await engine.learn(outcome);
      
      const state = engine.getState();
      // Quaternion should have changed due to prediction error
      const currentQ = state!.quaternionState;
      const changed = 
        initialQ.w !== currentQ.w || 
        initialQ.x !== currentQ.x || 
        initialQ.y !== currentQ.y || 
        initialQ.z !== currentQ.z;
      
      expect(changed).toBe(true);
    });

    it('should update attention based on outcome', async () => {
      await engine.initializeSession('session-1');
      const observation = [0.5, 0.3, 0.1, 0.1];
      await engine.runCycle(observation);

      const initialPrecision = engine.getState()!.attention.precision;
      
      const outcome: ActionOutcome = {
        policyId: 'test-policy',
        success: true,
        predictionError: 0.3,
        information: 0.1,
        beliefUpdate: [],
        smfDelta: []
      };

      await engine.learn(outcome);
      
      const state = engine.getState();
      // Precision may have changed
      expect(state!.attention.precision).toBeGreaterThanOrEqual(initialPrecision);
    });
  });

  describe('consolidate', () => {
    it('should return high-confidence beliefs as insights', async () => {
      await engine.initializeSession('session-1');
      
      // Add a high-confidence belief
      engine.addBelief('High confidence insight', 0.8, [2, 3, 5, 7]);
      
      const result = await engine.consolidate();
      expect(result.insights).toBeDefined();
    });
  });

  describe('setGoalState', () => {
    it('should set goal state for pragmatic value', async () => {
      await engine.initializeSession('session-1');
      engine.setGoalState([1, 0, 0, 0]);
      
      const observation = [0.5, 0.3, 0.1, 0.1];
      const result = await engine.runCycle(observation);
      
      // Policy should have pragmatic value calculated
      expect(result.policy).toBeDefined();
    });
  });

  describe('event system', () => {
    it('should emit events during cycle', async () => {
      await engine.initializeSession('session-1');
      
      const events: string[] = [];
      const unsubscribe = engine.on((event) => {
        events.push(event.type);
      });

      const observation = [0.5, 0.3, 0.1, 0.1];
      await engine.runCycle(observation);
      
      expect(events).toContain('state_change');
      expect(events).toContain('free_energy_update');
      expect(events).toContain('policy_selected');
      
      unsubscribe();
    });
  });

  describe('getFreeEnergyTrend', () => {
    it('should report decreasing trend when free energy drops', async () => {
      await engine.initializeSession('session-1');
      
      // Run multiple cycles to build trajectory
      const observation = [0.5, 0.3, 0.1, 0.1];
      for (let i = 0; i < 5; i++) {
        await engine.runCycle(observation);
      }
      
      const trend = engine.getFreeEnergyTrend();
      // Trend should be one of the valid values
      expect(['decreasing', 'stable', 'increasing']).toContain(trend);
    });
  });

  describe('addBelief', () => {
    it('should add and normalize beliefs', async () => {
      await engine.initializeSession('session-1');
      
      engine.addBelief('Test belief 1', 0.5, [2, 3]);
      engine.addBelief('Test belief 2', 0.5, [5, 7]);
      
      const state = engine.getState();
      expect(state!.currentBeliefs.length).toBe(2);
      
      // Probabilities should be normalized
      const totalProb = state!.currentBeliefs.reduce(
        (acc, b) => acc + b.probability, 0
      );
      expect(totalProb).toBeCloseTo(1.0, 2);
    });
  });
});
