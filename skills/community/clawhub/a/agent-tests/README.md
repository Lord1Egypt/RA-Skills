# Agent Tests 🧪

**Define, run, and track tests for agent behavior. Test cases, assertions, regression tracking, and performance benchmarking.**

## Why Agent Tests?

Testing agents is different from testing code. Agents produce complex, varied outputs — structured tool calls, free-form text, conditional logic. Agent Tests gives you:

- **Behavioral assertions** — Test what the agent *does*, not just what it returns
- **Self-testing framework** — 27 built-in tests covering all assertion types
- **Fixture-based testing** — Reusable test fixtures for multi-agent scenarios
- **Performance benchmarking** — Track response times, token usage, iteration counts
- **Regression tracking** — Record and compare behavior across agent versions
- **Zero dependencies** — Pure Node.js, no npm install needed

---

## Installation

```bash
# Already included in OpenClaw workspace at skills/agent-tests/
# No npm install needed — pure Node.js
```

---

## Quick Start

```bash
# Run the full self-test suite
node skills/agent-tests/tests/run-self-tests.js

# Expected output: 27/27 tests passing
```

---

## Core Concepts

### Assertions

Agent Tests provides a full set of behavioral assertions:

| Assertion | What It Checks |
|-----------|----------------|
| `assertEqual(actual, expected)` | Strict equality |
| `assertNotEqual(a, b)` | Inequality |
| `assert(condition)` | Truthy value |
| `assertDeepEqual(actual, expected)` | Deep object equality |
| `assertMatch(str, regex)` | Regex match in string |
| `assertNotMatch(str, regex)` | No regex match |
| `assertThrows(fn)` | Function throws |
| `assertNotThrows(fn)` | No exception |
| `assertType(value, type)` | typeof check |
| `assertDefined(value)` | Not undefined |
| `assertGreaterThan(a, b)` | a > b |
| `assertLessThan(a, b)` | a < b |
| `assertInRange(val, min, max)` | min ≤ val ≤ max |
| `assertProperty(obj, key)` | Key exists in object |
| `assertCallCount(spy, count)` | Function called N times |
| `assertSpyWithArg(spy, arg)` | Function called with specific arg |
| `assertOrdered(actual, expected)` | Array order match |

### Test Groups

```javascript
group('Feature name — N cases', () => {
  assert(something, 'should work');
  assertEqual(a, b, 'equality check');
});
```

Test groups provide:
- Auto-numbered test cases
- Clear pass/fail indicators
- Summary output with totals
- Exit code on failure

---

## Test Writing Guide

### Basic Structure

```javascript
// test/my-agent-test.js
const { group, assert, assertEqual } = require('./path/to/test-framework');

group('Auth flow — 3 cases', () => {
  assert(authenticate('valid-token'), 'Valid token passes');
  assert(!authenticate(''), 'Empty token rejected');
  assertThrows(() => authenticate(null), 'Null throws error');
});
```

### Fixture Usage

```javascript
const { loadFixture } = require('./fixtures/test-fixtures');
const fixture = loadFixture('auth-scenario');

group('Auth fixture — 2 cases', () => {
  assert(fixture.token, 'Fixture has token');
  assert(fixture.expectedRole === 'admin', 'Expected role is admin');
});
```

### Performance Benchmarking

```javascript
group('Response time — 1 case', () => {
  const start = Date.now();
  runAgentTask();
  const elapsed = Date.now() - start;
  assertLessThan(elapsed, 5000, 'Response under 5s');
});
```

---

## API Reference

### Functions

```javascript
// Core assertions
assert(condition, description)
assertEqual(actual, expected, description)
assertNotEqual(a, b, description)
assertDeepEqual(actual, expected, description)
assertMatch(str, regex, description)
assertNotMatch(str, regex, description)
assertThrows(fn, description)
assertNotThrows(fn, description)
assertType(value, type, description)
assertDefined(value, description)
assertGreaterThan(a, b, description)
assertLessThan(a, b, description)
assertInRange(val, min, max, description)

// Object assertions
assertProperty(obj, key, description)

// Spy/mock assertions
assertCallCount(spy, count, description)
assertSpyWithArg(spy, arg, description)

// Array assertions
assertOrdered(actual, expected, description)

// Test organization
group(name, fn)
```

### Configuration

```javascript
// Set test mode (empty-strings is default)
process.env.EMPTY_STRINGS = '1';

// Verbose output
process.env.VERBOSE = '1';
```

---

## Test Fixtures

Located in `tests/fixtures/`:

| Fixture | Purpose |
|---------|---------|
| `test-fixtures.js` | Load test scenarios with expected inputs/outputs |
| `empty-strings.js` | Tests for empty/whitespace string handling |

Fixtures provide reusable test scenarios with:
- Pre-defined inputs
- Expected outputs
- Edge case coverage
- Multiple agent interaction patterns

---

## Running Tests

```bash
# Full suite (27 tests)
node skills/agent-tests/tests/run-self-tests.js

# Legacy tests
node skills/agent-tests/test/run-tests.js

# Single group (via direct require)
node -e "require('./tests/run-self-tests.js')"
```

### Expected Output

```
📋 Basic assertions — 4 cases
  ✅ truthy value passes
  ✅ strict equality
  ✅ deep equality
  ✅ string match

...

═══════════════════════════════════════
  Agent Tests Self-Test Results
  27/27 tests passing
═══════════════════════════════════════

✅ All self-tests passed
```

---

## Security

Agent Tests is **pure Node.js** — no shell execution, no network access, no external dependencies. All assertions run in-memory.

| Protection | Status |
|------------|--------|
| Shell injection | ✅ No exec/system calls |
| Network access | ✅ None |
| File system writes | ✅ JSON test files + results (local workspace only) |
| eval/Function | ✅ Not used |
| External deps | ✅ Zero |

---

## Examples

### Test Async Agent Behavior
```javascript
group('Async agent — 2 cases', () => {
  const result = await runAgent('deploy weather skill');
  assert(result.success, 'Agent completes task');
  assertProperty(result, 'output', 'Agent produces output');
});
```

### Test Error Handling
```javascript
group('Error handling — 2 cases', () => {
  assertThrows(() => runAgent(null), 'Null input throws');
  assertThrows(() => runAgent({}), 'Empty object throws');
});
```

### Test Regression
```javascript
group('Regression: config parsing — 1 case', () => {
  const config = parseConfig('key=value\nport=8080');
  assertEqual(config.port, '8080', 'Config port matches');
});
```

---

## Publishing to ClawHub

```bash
# Via skill_workshop (after review)
skill_workshop action=create name=agent-tests ...
```

---

## License

MIT — Part of the OpenClaw skill ecosystem.

---

## Related Skills

- **Environment Manager** — Manage dev environments
- **API Gateway** — Test external API integrations
- **Smart Files** — Test file operations
