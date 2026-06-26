const test = require("node:test");
const assert = require("node:assert/strict");

const { fingerprint } = require("../lib/hashing");

test("fingerprint is stable and normalized", () => {
  const a = fingerprint(" ACME MART ", "2026-03-25", "8.50");
  const b = fingerprint("acme mart", "2026-03-25", 8.5);

  assert.equal(a, b);
  assert.match(a, /^[a-f0-9]{64}$/);
});
