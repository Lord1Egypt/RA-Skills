/**
 * Feelings Framework — TypeScript Type Declarations
 * @version 1.0.0
 */

/** The nine core feelings an agent can experience. */
export enum Feeling {
  WARMTH = "warmth",
  COOLNESS = "coolness",
  INTEREST = "interest",
  BOREDOM = "boredom",
  LONELINESS = "loneliness",
  SECURITY = "security",
  ANXIETY = "anxiety",
  SATISFACTION = "satisfaction",
  FRUSTRATION = "frustration",
}

export const FEELING_KEYS: Feeling[];

/**
 * Abstract memory interface.
 * Implement this to use any storage backend.
 */
export abstract class Memory {
  /** Load and return a serialized state object, or null. */
  load(): FeelingsState | null;
  /** Persist a state object. */
  save(state: FeelingsState): void;
}

/** In-memory storage (for testing / short-lived sessions). */
export class InMemory extends Memory {
  load(): FeelingsState | null;
  save(state: FeelingsState): void;
}

/** LocalStorage-backed memory (for browser environments). */
export class LocalStorageMemory extends Memory {
  constructor(key: string);
  load(): FeelingsState | null;
  save(state: FeelingsState): void;
}

/**
 * @typedef {Object} Trigger
 * @property {Feeling} feeling
 * @property {number} delta
 * @property {number} [escalationMultiplier=1.0]
 * @property {number} [maxIntensity=1.0]
 */

/**
 * @typedef {Object} Calibration
 * @property {Record<string, number>} triggerDeltas
 * @property {number} [moodBaseline=0.0]
 * @property {number} [moodSensitivity=1.0]
 * @property {number} [dampingRate=0.05]
 */

/**
 * @typedef {Object} FeelingsState
 * @property {string} agentId
 * @property {number} mood
 * @property {Record<Feeling, number>} feelings
 * @property {string} lastUpdate
 * @property {number} sessionCount
 * @property {Record<string, number>} [_triggerCounts]
 */

/**
 * @typedef {Object} RespondModifiers
 * @property {number} warmth
 * @property {number} restraint
 * @property {number} curiosity
 * @property {number} guard
 * @property {number} energy
 * @property {number} patience
 * @property {number} reach_out
 * @property {number} withdraw
 * @property {number} engage_deeper
 * @property {number} play_it_safe
 * @property {number} persist
 * @property {number} celebrate
 * @property {number} _mood
 * @property {number} _frustration
 * @property {number} _anxiety
 * @property {number} _loneliness
 */

export interface FeelingsEngineOptions {
  agentId: string;
  memory?: Memory;
  triggers?: Record<string, Trigger>;
  calibrations?: Record<string, Calibration>;
  initialMood?: number;
  moodMin?: number;
  moodMax?: number;
}

/** Default calibration for a warm, engaged agent. */
export function defaultCalibration(): Calibration;

/**
 * The main feelings engine.
 */
export class FeelingsEngine {
  constructor(opts: FeelingsEngineOptions);

  /**
   * Apply a named trigger. Updates feeling intensities and mood.
   * @param triggerName
   * @param [_context]
   */
  update(triggerName: string, _context?: Record<string, unknown>): FeelingsState;

  /** Return the current state. */
  getState(): FeelingsState;

  /** Generate response modifiers based on current feelings. */
  respond(): RespondModifiers;

  /** Explicitly save current state. */
  save(): void;

  /** Explicitly load state from memory (overwrites current). */
  load(): FeelingsState;

  /**
   * Switch to a different agent's calibration table.
   * @param agentId
   */
  calibrate(agentId: string): void;

  /**
   * Register or update a trigger at runtime.
   * @param name
   * @param feeling
   * @param delta
   * @param [escalationMultiplier=1.0]
   * @param [maxIntensity=1.0]
   */
  registerTrigger(
    name: string,
    feeling: Feeling,
    delta: number,
    escalationMultiplier?: number,
    maxIntensity?: number
  ): void;

  /**
   * Set or update a calibration table.
   * @param agentId
   * @param calibration
   */
  setCalibration(agentId: string, calibration: Calibration): void;

  /**
   * Manually apply dampening to all feelings.
   * @param [amount=0.05]
   */
  dampenAll(amount?: number): void;

  /** Reset all feeling intensities to 0. */
  resetFeelings(): void;
}

export default FeelingsEngine;
