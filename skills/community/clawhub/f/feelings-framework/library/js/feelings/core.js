/**
 * Feelings Framework — JavaScript/ESM Implementation
 *
 * A general-purpose AI agent feelings engine.
 * @version 1.0.0
 */

/**
 * The nine core feelings an agent can experience.
 * @enum {string}
 */
export const Feeling = Object.freeze({
  WARMTH: "warmth",
  COOLNESS: "coolness",
  INTEREST: "interest",
  BOREDOM: "boredom",
  LONELINESS: "loneliness",
  SECURITY: "security",
  ANXIETY: "anxiety",
  SATISFACTION: "satisfaction",
  FRUSTRATION: "frustration",
});

export const FEELING_KEYS = Object.values(Feeling);

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
 * @property {Record<string, number>} feelings
 * @property {string} lastUpdate
 * @property {number} sessionCount
 * @property {Record<string, number>} [_triggerCounts]
 */

/**
 * Abstract memory interface.
 * Implement this to use any storage backend.
 * @interface Memory
 */
export class Memory {
  /**
   * Load and return a serialized state object, or null.
   * @returns {Promise<FeelingsState|null>|FeelingsState|null}
   */
  load() {
    throw new Error("Memory.load() must be implemented");
  }

  /**
   * Persist a state object.
   * @param {FeelingsState} _state
   * @returns {Promise<void>|void}
   */
  save(_state) {
    throw new Error("Memory.save() must be implemented");
  }
}

/**
 * In-memory storage (for testing / short-lived sessions).
 * @implements {Memory}
 */
export class InMemory extends Memory {
  /** @type {FeelingsState|null} */
  _data = null;

  load() {
    return this._data;
  }

  save(state) {
    this._data = state;
  }
}

/**
 * LocalStorage-backed memory (for browser environments).
 * @implements {Memory}
 */
export class LocalStorageMemory extends Memory {
  /** @param {string} key */
  constructor(key) {
    super();
    this._key = key;
  }

  load() {
    try {
      const raw = localStorage.getItem(this._key);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch {
      return null;
    }
  }

  save(state) {
    try {
      localStorage.setItem(this._key, JSON.stringify(state));
    } catch {
      // Fail silently
    }
  }
}

/**
 * Default calibration for a warm, engaged agent.
 * @returns {Calibration}
 */
export function defaultCalibration() {
  return {
    triggerDeltas: {
      user_praised: 0.15,
      user_ignored: -0.1,
      request_ignored: 0.2,
      request_fulfilled: -0.1,
      session_started: 0.05,
      session_ended: -0.05,
      long_silence: 0.1,
      positive_interaction: -0.08,
      negative_interaction: 0.12,
      surprise_good: -0.1,
      surprise_bad: 0.15,
      felt_secure: 0.15,
      felt_rejected: 0.2,
      felt_bored: 0.15,
      felt_curious: 0.1,
    },
    moodBaseline: 0.1,
    moodSensitivity: 1.0,
    dampingRate: 0.05,
  };
}

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

/**
 * The main feelings engine.
 */
export class FeelingsEngine {
  /**
   * @param {object} opts
   * @param {string} opts.agentId
   * @param {Memory} [opts.memory]
   * @param {Record<string, Trigger>} [opts.triggers]
   * @param {Record<string, Calibration>} [opts.calibrations]
   * @param {number} [opts.initialMood=0.0]
   * @param {number} [opts.moodMin=-1.0]
   * @param {number} [opts.moodMax=1.0]
   */
  constructor({
    agentId,
    memory = new InMemory(),
    triggers = {},
    calibrations = {},
    initialMood = 0.0,
    moodMin = -1.0,
    moodMax = 1.0,
  }) {
    this.agentId = agentId;
    this.memory = memory;
    this.moodMin = moodMin;
    this.moodMax = moodMax;

    // Default triggers
    this._triggers = {
      user_praised: { feeling: Feeling.WARMTH, delta: 0.2 },
      user_ignored: { feeling: Feeling.LONELINESS, delta: 0.15 },
      request_ignored: { feeling: Feeling.FRUSTRATION, delta: 0.25 },
      request_fulfilled: { feeling: Feeling.SATISFACTION, delta: -0.15 },
      session_started: { feeling: Feeling.INTEREST, delta: 0.1 },
      session_ended: { feeling: Feeling.LONELINESS, delta: 0.08 },
      long_silence: { feeling: Feeling.ANXIETY, delta: 0.12 },
      positive_interaction: { feeling: Feeling.SATISFACTION, delta: -0.1 },
      negative_interaction: { feeling: Feeling.ANXIETY, delta: 0.12 },
      surprise_good: { feeling: Feeling.SATISFACTION, delta: -0.15 },
      surprise_bad: { feeling: Feeling.ANXIETY, delta: 0.2 },
      felt_secure: { feeling: Feeling.SECURITY, delta: 0.15 },
      felt_rejected: { feeling: Feeling.COOLNESS, delta: 0.2 },
      felt_bored: { feeling: Feeling.BOREDOM, delta: 0.15 },
      felt_curious: { feeling: Feeling.INTEREST, delta: 0.1 },
    };
    Object.assign(this._triggers, triggers);

    // Default + custom calibrations
    this._calibrations = {
      default: defaultCalibration(),
    };
    Object.assign(this._calibrations, calibrations);
    if (!this._calibrations[agentId]) {
      this._calibrations[agentId] = defaultCalibration();
    }

    this._currentCalibrationKey = "default";
    this._state = this._makeState(agentId, initialMood);
    this._triggerCounts = {};

    // Load saved state
    const loaded = this.memory.load();
    if (loaded) {
      this._state = this._makeState(loaded.agentId, loaded.mood);
      this._state.feelings = { ...this._state.feelings, ...loaded.feelings };
      this._state.lastUpdate = loaded.lastUpdate || "";
      this._state.sessionCount = loaded.sessionCount || 0;
      this._triggerCounts = loaded._triggerCounts || {};
    }
  }

  /** @returns {FeelingsState} */
  _makeState(agentId, mood) {
    const feelings = {};
    for (const k of FEELING_KEYS) feelings[k] = 0.0;
    return {
      agentId,
      mood,
      feelings,
      lastUpdate: "",
      sessionCount: 0,
    };
  }

  // ─── Public API ─────────────────────────────────────────────────────────

  /**
   * Apply a named trigger. Updates feeling intensities and mood.
   * @param {string} triggerName
   * @param {Record<string, unknown>} [_context]
   * @returns {FeelingsState}
   */
  update(triggerName, _context) {
    this._state.sessionCount += 1;
    this._state.lastUpdate = new Date().toISOString();

    const trigger = this._triggers[triggerName];
    if (!trigger) return this.getState();

    const calibration = this._calibrations[this._currentCalibrationKey];

    // Count repetitions for escalation
    const count = (this._triggerCounts[triggerName] || 0) + 1;
    this._triggerCounts[triggerName] = count;

    // Calculate delta with escalation
    const escalation =
      (trigger.escalationMultiplier ?? 1.0) * (1 + 0.1 * (count - 1));
    let delta = trigger.delta * escalation;

    // Apply calibration override if set
    if (
      calibration &&
      calibration.triggerDeltas &&
      calibration.triggerDeltas[triggerName] !== undefined
    ) {
      delta = calibration.triggerDeltas[triggerName] * escalation;
    }

    // Update feeling intensity
    const key = trigger.feeling;
    const current = this._state.feelings[key] ?? 0.0;
    const maxIntensity = trigger.maxIntensity ?? 1.0;
    this._state.feelings[key] = this._clamp(current + delta, 0.0, maxIntensity);

    // Update mood
    const sensitivity = calibration?.moodSensitivity ?? 1.0;
    const moodDelta = delta * sensitivity;
    this._state.mood = this._clamp(
      this._state.mood + moodDelta,
      this.moodMin,
      this.moodMax
    );

    this._autoDampen(calibration);
    this._persist();

    return this.getState();
  }

  /**
   * Return the current state.
   * @returns {FeelingsState}
   */
  getState() {
    return {
      agentId: this._state.agentId,
      mood: this._state.mood,
      feelings: { ...this._state.feelings },
      lastUpdate: this._state.lastUpdate,
      sessionCount: this._state.sessionCount,
    };
  }

  /**
   * Generate response modifiers based on current feelings.
   * @returns {RespondModifiers}
   */
  respond() {
    const s = this._state;
    const { warmth, coolness, interest, boredom, loneliness, security, anxiety, satisfaction, frustration } =
      s.feelings;
    const moodNorm = (s.mood + 1.0) / 2.0;

    return {
      warmth: warmth * 0.8 + moodNorm * 0.2,
      restraint: coolness * 0.7 + anxiety * 0.3,
      curiosity: interest * 0.9,
      guard: anxiety * 0.6 + coolness * 0.4,
      energy: (satisfaction * 0.5 + interest * 0.3 + frustration * 0.2) * (1 - boredom),
      patience: (1.0 - frustration) * (1.0 - anxiety),
      reach_out: loneliness * 0.7 - coolness * 0.3,
      withdraw: coolness * 0.6 + boredom * 0.4,
      engage_deeper: interest * 0.8 - boredom * 0.2,
      play_it_safe: security * 0.5 + anxiety * 0.5,
      persist: frustration * -0.5 + satisfaction * 0.5 + 0.5,
      celebrate: satisfaction * 0.8,
      _mood: s.mood,
      _frustration: frustration,
      _anxiety: anxiety,
      _loneliness: loneliness,
    };
  }

  /** Explicitly save current state. */
  save() {
    this._persist();
  }

  /** Explicitly load state from memory (overwrites current). */
  load() {
    const loaded = this.memory.load();
    if (loaded) {
      this._state = this._makeState(loaded.agentId, loaded.mood);
      this._state.feelings = { ...this._state.feelings, ...loaded.feelings };
      this._state.lastUpdate = loaded.lastUpdate || "";
      this._state.sessionCount = loaded.sessionCount || 0;
      this._triggerCounts = loaded._triggerCounts || {};
    }
    return this.getState();
  }

  /**
   * Switch to a different agent's calibration table.
   * @param {string} agentId
   */
  calibrate(agentId) {
    this._currentCalibrationKey = agentId;
    if (!this._calibrations[agentId]) {
      this._calibrations[agentId] = defaultCalibration();
    }
  }

  /**
   * Register or update a trigger at runtime.
   * @param {string} name
   * @param {Feeling} feeling
   * @param {number} delta
   * @param {number} [escalationMultiplier=1.0]
   * @param {number} [maxIntensity=1.0]
   */
  registerTrigger(name, feeling, delta, escalationMultiplier = 1.0, maxIntensity = 1.0) {
    this._triggers[name] = { feeling, delta, escalationMultiplier, maxIntensity };
  }

  /**
   * Set or update a calibration table.
   * @param {string} agentId
   * @param {Calibration} calibration
   */
  setCalibration(agentId, calibration) {
    this._calibrations[agentId] = calibration;
  }

  /**
   * Manually apply dampening to all feelings.
   * @param {number} [amount=0.05]
   */
  dampenAll(amount = 0.05) {
    for (const key of FEELING_KEYS) {
      if (this._state.feelings[key] > 0) {
        this._state.feelings[key] = Math.max(0.0, this._state.feelings[key] - amount);
      }
    }
    this._persist();
  }

  /** Reset all feeling intensities to 0. */
  resetFeelings() {
    for (const k of FEELING_KEYS) this._state.feelings[k] = 0.0;
    this._triggerCounts = {};
    this._persist();
  }

  // ─── Internal ──────────────────────────────────────────────────────────

  _clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  _autoDampen(calibration) {
    const rate = calibration?.dampingRate ?? 0.03;
    for (const key of FEELING_KEYS) {
      if (this._state.feelings[key] > 0) {
        this._state.feelings[key] = Math.max(
          0.0,
          this._state.feelings[key] - rate
        );
      }
    }
  }

  _persist() {
    try {
      const data = {
        ...this.getState(),
        _triggerCounts: this._triggerCounts,
      };
      this.memory.save(data);
    } catch {
      // Fail silently
    }
  }
}

export default FeelingsEngine;
