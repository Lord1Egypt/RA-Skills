/**
 * Smoke test: the engine runs the example definition end to end.
 * Regenerate per project: mock LLM/HTTP boundaries, assert the main path
 * reaches the terminal node and produces the DSL-declared outputs.
 *
 * Run: node tests/smoke.test.js   (no test framework needed)
 */
import assert from 'node:assert/strict';
import { DEFINITION, buildHandlers } from '../src/workflow/definition.js';
import { Engine } from '../src/workflow/runner.js';

const engine = new Engine(DEFINITION, buildHandlers());
const outputs = await engine.run({ text: 'hello' });
assert.equal(outputs.result, 'Echo: hello');

// streaming path: example has no answer nodes, so only the final event arrives
const events = [];
for await (const ev of new Engine(DEFINITION, buildHandlers()).runStream({ text: 'hi' })) {
  events.push(ev);
}
assert.equal(events.at(-1)[0], 'final');
assert.equal(events.at(-1)[1].result, 'Echo: hi');

console.log('node-express smoke OK ->', outputs);
