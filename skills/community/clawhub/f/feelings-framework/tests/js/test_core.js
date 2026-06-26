/**
 * Feelings Framework — JavaScript Tests
 */

import {
  FeelingsEngine,
  InMemory,
  Feeling,
  FEELING_KEYS,
  defaultCalibration,
} from "../../library/js/feelings/core.js";

// ─── Helpers ────────────────────────────────────────────────────────────────

class DummyMemory extends InMemory {
  /** @type {import('../../library/js/feelings/core.js').FeelingsState|null} */
  _data = null;
  load() { return this._data; }
  save(state) { this._data = state; }
}

// ─── Tests ──────────────────────────────────────────────────────────────────

const tests = [];

function assert(condition, message) {
  if (!condition) throw new Error(`FAIL: ${message}`);
}

function test(name, fn) {
  tests.push({ name, fn });
}

// ─── Test Suites ─────────────────────────────────────────────────────────────

test("initial_state", () => {
  const engine = new FeelingsEngine({ agentId: "test_agent" });
  const state = engine.getState();

  assert(state.agentId === "test_agent", "agent_id matches");
  assert(state.mood === 0.0, "initial mood is 0");
  assert(Object.keys(state.feelings).length === 9, "has 9 feelings");
  assert(Object.values(state.feelings).every(v => v >= 0 && v <= 1), "all feelings in 0..1");
});

test("update_trigger_increases_feeling", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });
  const state = engine.update("user_praised");

  assert(state.feelings.warmth > 0, "warmth increased after praise");
  assert(state.mood > 0, "mood increased after positive trigger");
});

test("frustration_escalates_with_repetition", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });

  const s1 = engine.update("request_ignored");
  const s2 = engine.update("request_ignored");
  const s3 = engine.update("request_ignored");

  assert(
    s3.feelings.frustration >= s2.feelings.frustration,
    "frustration escalates with repeated triggers"
  );
});

test("dampening_reduces_feelings_over_time", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });
  engine.update("user_praised");
  const warmAfterPraise = engine.getState().feelings.warmth;

  // Many neutral updates
  for (let i = 0; i < 15; i++) engine.update("session_started");

  const warmAfterNeutral = engine.getState().feelings.warmth;
  assert(warmAfterNeutral < warmAfterPraise, "warmth dampens with neutral updates");
});

test("calibrate_switch_changes_response", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });

  // Default agent response
  engine.calibrate("default");
  engine._state.feelings.frustration = 0;
  engine.update("request_ignored");
  const frustrationDefault = engine.getState().feelings.frustration;

  // Calm agent calibration
  const calmCal = defaultCalibration();
  calmCal.triggerDeltas.request_ignored = 0.05;
  engine.setCalibration("calm_agent", calmCal);
  engine.calibrate("calm_agent");
  engine._state.feelings.frustration = 0;
  engine.update("request_ignored");
  const frustrationCalm = engine.getState().feelings.frustration;

  assert(frustrationCalm < frustrationDefault, "calm agent reacts less to same trigger");
});

test("respond_returns_all_modifiers", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });
  const mods = engine.respond();

  assert(typeof mods.warmth === "number", "has warmth modifier");
  assert(typeof mods.restraint === "number", "has restraint modifier");
  assert(typeof mods.curiosity === "number", "has curiosity modifier");
  assert(typeof mods.guard === "number", "has guard modifier");
  assert(typeof mods.energy === "number", "has energy modifier");
  assert(typeof mods.patience === "number", "has patience modifier");
  assert(typeof mods.reach_out === "number", "has reach_out modifier");
  assert(typeof mods.withdraw === "number", "has withdraw modifier");
  assert(typeof mods.engage_deeper === "number", "has engage_deeper modifier");
  assert(typeof mods.play_it_safe === "number", "has play_it_safe modifier");
  assert(typeof mods.persist === "number", "has persist modifier");
  assert(typeof mods.celebrate === "number", "has celebrate modifier");
  assert(typeof mods._mood === "number", "has _mood context");
  assert(typeof mods._frustration === "number", "has _frustration context");
});

test("register_trigger_runtime", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });
  engine.registerTrigger("custom_event", Feeling.COOLNESS, 0.5);
  engine.update("custom_event");

  assert(engine.getState().feelings.coolness > 0, "custom trigger applied");
});

test("dampen_all", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });
  engine.update("user_praised");
  engine.update("surprise_bad");
  const warmBefore = engine.getState().feelings.warmth;
  const anxBefore = engine.getState().feelings.anxiety;

  engine.dampenAll(0.1);

  assert(engine.getState().feelings.warmth < warmBefore, "warmth reduced by dampenAll");
  assert(engine.getState().feelings.anxiety < anxBefore, "anxiety reduced by dampenAll");
});

test("reset_feelings", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });
  engine.update("user_praised");
  engine.update("surprise_bad");

  const anyPositive = Object.values(engine.getState().feelings).some(v => v > 0);
  assert(anyPositive, "has positive feelings before reset");

  engine.resetFeelings();
  const allZero = Object.values(engine.getState().feelings).every(v => v === 0);
  assert(allZero, "all feelings zero after reset");
});

test("save_and_load_persists_state", () => {
  const mem = new DummyMemory();
  const engine = new FeelingsEngine({ agentId: "test_save", memory: mem });

  engine.update("user_praised");
  engine.update("session_started");
  engine.save();

  const engine2 = new FeelingsEngine({ agentId: "test_save", memory: mem });
  const state2 = engine2.getState();

  assert(state2.feelings.warmth > 0, "warmth persisted across load");
  assert(state2.sessionCount === 2, "session count persisted");
});

test("feeling_keys_is_nine", () => {
  assert(FEELING_KEYS.length === 9, "FEELING_KEYS has 9 entries");
});

test("mood_clamps_to_range", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory(), moodMin: -1, moodMax: 1 });
  // Apply many negative triggers
  for (let i = 0; i < 20; i++) engine.update("surprise_bad");
  const mood = engine.getState().mood;
  assert(mood >= -1 && mood <= 1, `mood clamped to range: ${mood}`);
});

test("unknown_trigger_noops", () => {
  const engine = new FeelingsEngine({ agentId: "test", memory: new DummyMemory() });
  const before = engine.getState();
  engine.update("this_trigger_does_not_exist");
  const after = engine.getState();

  assert(
    before.feelings.warmth === after.feelings.warmth &&
    before.mood === after.mood,
    "unknown trigger doesn't change state"
  );
});

// ─── Run ─────────────────────────────────────────────────────────────────────

let passed = 0;
let failed = 0;

for (const { name, fn } of tests) {
  try {
    fn();
    console.log(`  ✓ ${name}`);
    passed++;
  } catch (err) {
    console.error(`  ✗ ${name}`);
    console.error(`    ${err.message}`);
    failed++;
  }
}

console.log(`\n${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
