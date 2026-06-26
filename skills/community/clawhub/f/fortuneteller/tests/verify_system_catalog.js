#!/usr/bin/env node
const assert = require("node:assert/strict");
const systems = require("../data/system-catalog.js");

assert.ok(systems.length >= 10, "catalog should feel encyclopedic");

for (const item of systems) {
  assert.ok(item.id, "system id required");
  assert.ok(item.name, `${item.id} name required`);
  assert.ok(["S", "B", "C"].includes(item.grade), `${item.id} invalid grade`);
  assert.ok(item.status, `${item.id} status required`);
  assert.ok(item.basis, `${item.id} basis required`);
  assert.ok(item.capability, `${item.id} capability required`);
  assert.ok(item.guardrail, `${item.id} guardrail required`);
  assert.ok(Array.isArray(item.bestFor) && item.bestFor.length > 0, `${item.id} bestFor required`);
  assert.ok(Array.isArray(item.inputs) && item.inputs.length > 0, `${item.id} inputs required`);
}

const active = systems.filter((item) => item.status === "已启用").map((item) => item.id).sort();
assert.deepEqual(active, ["routing", "yijing-library", "zhouyi-benjing"].sort());

const zhouyi = systems.find((item) => item.id === "zhouyi-benjing");
assert.equal(zhouyi.grade, "S");
assert.match(zhouyi.basis, /周易/);

const qimen = systems.find((item) => item.id === "qimen");
assert.equal(qimen.status, "待校验");
assert.match(qimen.guardrail, /基准盘/);

console.log("system catalog verification passed");
