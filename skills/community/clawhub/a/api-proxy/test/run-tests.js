/**
 * API Gateway — test suite
 * Tests the api-gateway.js CLI interface.
 *
 * Run: node ../../test-runner.js --skill ../api-gateway.js --test run-tests.js
 */

module.exports = [
  // ── Status ──────────────────────────────────────────────────────────────
  { name: "--status shows configuration", args: ["--status"], expected: "[api-gateway] Status:" },
  { name: "No args defaults to status", args: [], expected: "[api-gateway] Status:" },
  { name: "Status shows key count", args: ["--status"], expected: "API keys configured:" },
  { name: "Status shows cache count", args: ["--status"], expected: "Cache entries:" },
  { name: "Status shows fallback count", args: ["--status"], expected: "Fallback providers:" },

  // ── Keys ────────────────────────────────────────────────────────────────
  { name: "--keys add stores a key", args: ["--keys", "add", "test-provider", "sk-test123abc"], expected: "[api-gateway] Added key:" },
  { name: "--keys shows the new provider", args: ["--keys"], expected: "test-provider" },
  { name: "--keys masks the key value", args: ["--keys"], notExpected: "sk-test123abc" },

  // ── Fallback ────────────────────────────────────────────────────────────
  { name: "--fallback sets fallback provider", args: ["--fallback", "test-provider", "alt-provider"], expected: "[api-gateway] Fallback set:" },
  { name: "--fallback shows configured fallback", args: ["--fallback"], expected: "test-provider → alt-provider" },

  // ── Cache ────────────────────────────────────────────────────────────────
  { name: "--cache shows entries", args: ["--cache"], expected: "[api-gateway] Cache:" },
  { name: "--cache --clear wipes cache", args: ["--cache", "--clear"], expected: "[api-gateway] Cache cleared." },
  { name: "--cache shows 0 entries after clear", args: ["--cache"], expected: "0 entries" },

  // ── Rate ────────────────────────────────────────────────────────────────
  { name: "--rate with unknown provider shows no data", args: ["--rate", "nonexistent"], expected: "No rate limit data for: nonexistent" },

  // ── Cleanup ─────────────────────────────────────────────────────────────
  { name: "Remove test key (cleanup)", args: ["--keys", "remove", "test-provider"], expected: "[api-gateway] Removed key:" },
  { name: "Remove nonexistent key shows message", args: ["--keys", "remove", "ghost"], expected: "[api-gateway] No key for: ghost" },

  // ── Edge Cases ───────────────────────────────────────────────────────────
  { name: "--keys add without enough args shows list", args: ["--keys", "add"], expected: "[api-gateway]" },
];
