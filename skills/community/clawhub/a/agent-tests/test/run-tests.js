module.exports = [
  // ── Status ──────────────────────────────────────────────────────────────
  { name: "no args shows status", args: [], expected: "[agent-tests] Status:" },
  { name: "--status shows status", args: ["--status"], expected: "[agent-tests] Status:" },
  { name: "status shows counters", args: ["--status"], expected: "Tests defined:" },

  // ── Test (correct usage: --test --run) ──────────────────────────────────
  { name: "--test --run nonexistent test", args: ["--test", "--run", "nonexistent"], expected: "Test not found:" },

  // ── List ─────────────────────────────────────────────────────────────────
  { name: "--test --list shows tests", args: ["--test", "--list"], expected: "[agent-tests]" },

  // ── Regression ──────────────────────────────────────────────────────────
  { name: "--regression shows status", args: ["--regression"], expected: "[agent-tests]" },

  // ── Benchmark ───────────────────────────────────────────────────────────
  { name: "--benchmark without test shows usage", args: ["--benchmark"], expected: "Usage:" },
];
