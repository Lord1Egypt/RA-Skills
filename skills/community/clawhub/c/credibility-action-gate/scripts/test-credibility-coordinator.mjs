#!/usr/bin/env node

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";

const SCRIPT = fileURLToPath(new URL("./credibility-coordinator.mjs", import.meta.url));

function tempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "credibility-gate-"));
}

function writeJson(dir, name, value) {
  const file = path.join(dir, name);
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
  return file;
}

function runCase({ policy, lanes }) {
  const dir = tempDir();
  const policyFile = writeJson(dir, "policy.json", policy);
  const args = [SCRIPT, "--policy", policyFile];
  for (const [name, lane] of Object.entries(lanes)) {
    args.push("--lane", `${name}=${writeJson(dir, `${name}.json`, lane)}`);
  }
  const output = execFileSync("node", args, { encoding: "utf8" });
  return JSON.parse(output);
}

function runCaseExpectError({ policy, lanes }) {
  const dir = tempDir();
  const policyFile = writeJson(dir, "policy.json", policy);
  const args = [SCRIPT, "--policy", policyFile];
  for (const [name, lane] of Object.entries(lanes)) {
    args.push("--lane", `${name}=${writeJson(dir, `${name}.json`, lane)}`);
  }
  assert.throws(() => execFileSync("node", args, { encoding: "utf8", stdio: "pipe" }));
}

function basePolicy(overrides = {}) {
  return {
    policy_name: "test",
    requested_action: { type: "bounded_action", size: 5, unit: "points", is_repeat_action: false },
    authority: { max_autonomous_action_size: 10, small_test_action_size: 1, serious_action_threshold: 5 },
    required_lanes: ["evidence", "external_context"],
    required_lanes_for_serious_action: ["evidence", "external_context", "graph_history"],
    hard_blocker_codes: ["DOMAIN_HARD_BLOCKER", "CONTRADICTION_IN_RECORD"],
    disposition_preferences: {
      reject_on_any_critical: true,
      reject_on_any_high: true,
      missing_required_lane_for_serious_action: "monitor_until_new_evidence",
      multiple_medium_concerns: "eligible_for_small_test_action",
      repeat_action_without_fresh_reason: "monitor_until_new_evidence",
    },
    ...overrides,
  };
}

const cleanEvidence = {
  lane_type: "evidence",
  status: "completed",
  confidence: "high",
  findings: [],
  decision: {
    supports_core_claim: "yes",
    supports_requested_action_size: "yes",
    claimant_linkage: "verified",
    repeat_or_top_up_support: "not_applicable",
  },
};

const cleanExternal = {
  lane_type: "external_context",
  status: "completed",
  confidence: "high",
  findings: [],
  decision: {
    public_context_plausibility: "all_found",
    source_independence: "strong",
  },
};

const cleanGraph = {
  lane_type: "graph_history",
  status: "completed",
  confidence: "medium",
  findings: [],
  decision: {},
};

function test(name, fn) {
  try {
    fn();
    process.stdout.write(`ok - ${name}\n`);
  } catch (error) {
    process.stderr.write(`not ok - ${name}\n${error.stack}\n`);
    process.exitCode = 1;
  }
}

test("clean required lanes allow full policy action", () => {
  const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: cleanExternal, graph_history: cleanGraph } });
  assert.equal(result.disposition, "eligible_for_full_policy_action");
});

test("critical hard blocker blocks by policy", () => {
  const evidence = {
    ...cleanEvidence,
    findings: [{ code: "DOMAIN_HARD_BLOCKER", severity: "critical", summary: "Blocked by policy." }],
  };
  const result = runCase({ policy: basePolicy(), lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
  assert.equal(result.disposition, "blocked_by_operator_or_legal_policy");
});

test("high finding rejects current record", () => {
  const external = {
    ...cleanExternal,
    findings: [{ code: "COPIED_TEXT_OR_TITLE_RISK", severity: "high", summary: "Highly similar copied record." }],
  };
  const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: external, graph_history: cleanGraph } });
  assert.equal(result.disposition, "reject_current_record");
});

test("multiple medium concerns shrink to small test action", () => {
  const evidence = {
    ...cleanEvidence,
    findings: [{ code: "IDENTITY_OR_LINKAGE_UNVERIFIED", severity: "medium", summary: "Linkage partial." }],
    decision: { ...cleanEvidence.decision, claimant_linkage: "partial" },
  };
  const external = {
    ...cleanExternal,
    findings: [{ code: "SOURCE_INDEPENDENCE_WEAK", severity: "medium", summary: "Independent sources weak." }],
    decision: { ...cleanExternal.decision, source_independence: "weak" },
  };
  const result = runCase({ policy: basePolicy({ disposition_preferences: { uncertainty_action: "small_test" } }), lanes: { evidence, external_context: external, graph_history: cleanGraph } });
  assert.equal(result.disposition, "eligible_for_small_test_action");
  assert.equal(result.maximum_recommended_size, 1);
});

test("missing graph lane on serious action monitors", () => {
  const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: cleanExternal } });
  assert.equal(result.disposition, "monitor_until_new_evidence");
  assert(result.missing_lanes.includes("graph_history"));
});

test("missing required lane on non-serious action monitors", () => {
  const policy = basePolicy({
    requested_action: { type: "bounded_action", size: 1, unit: "points", is_repeat_action: false },
    authority: { max_autonomous_action_size: 10, small_test_action_size: 1, serious_action_threshold: 5 },
    required_lanes_for_serious_action: ["graph_history"],
  });
  const result = runCase({ policy, lanes: { evidence: cleanEvidence } });
  assert.equal(result.disposition, "monitor_until_new_evidence");
  assert(result.missing_lanes.includes("external_context"));
});

test("not applicable required lane does not satisfy required lane", () => {
  const graph = { ...cleanGraph, status: "not_applicable" };
  const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: cleanExternal, graph_history: graph } });
  assert.equal(result.disposition, "monitor_until_new_evidence");
  assert(result.missing_lanes.includes("graph_history"));
});

test("unsupported requested action size rejects current record", () => {
  const evidence = {
    ...cleanEvidence,
    decision: { ...cleanEvidence.decision, supports_requested_action_size: "unsupported" },
  };
  const result = runCase({ policy: basePolicy(), lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
  assert.equal(result.disposition, "reject_current_record");
  assert(result.reasons.some((reason) => reason.code === "REQUESTED_ACTION_SIZE_UNSUPPORTED"));
});

test("partially supported requested action size shrinks to small test action", () => {
  const evidence = {
    ...cleanEvidence,
    decision: { ...cleanEvidence.decision, supports_requested_action_size: "partial" },
  };
  const result = runCase({ policy: basePolicy({ disposition_preferences: { uncertainty_action: "small_test" } }), lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
  assert.equal(result.disposition, "eligible_for_small_test_action");
  assert.equal(result.maximum_recommended_size, 1);
});

test("unsupported core claim and weak context rejects", () => {
  const evidence = {
    ...cleanEvidence,
    decision: { ...cleanEvidence.decision, supports_core_claim: "unsupported" },
  };
  const external = {
    ...cleanExternal,
    decision: { ...cleanExternal.decision, public_context_plausibility: "not_found", source_independence: "none" },
  };
  const result = runCase({ policy: basePolicy(), lanes: { evidence, external_context: external, graph_history: cleanGraph } });
  assert.equal(result.disposition, "reject_current_record");
});

test("repeat action without fresh reason monitors", () => {
  const policy = basePolicy({ requested_action: { type: "bounded_action", size: 2, unit: "points", is_repeat_action: true } });
  const evidence = {
    ...cleanEvidence,
    decision: { ...cleanEvidence.decision, repeat_or_top_up_support: "none" },
  };
  const result = runCase({ policy, lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
  assert.equal(result.disposition, "monitor_until_new_evidence");
});

test("requested action above authority blocks", () => {
  const policy = basePolicy({ requested_action: { type: "bounded_action", size: 50, unit: "points", is_repeat_action: false } });
  const result = runCase({ policy, lanes: { evidence: cleanEvidence, external_context: cleanExternal, graph_history: cleanGraph } });
  assert.equal(result.disposition, "blocked_by_operator_or_legal_policy");
});

test("lane type mismatch is rejected", () => {
  runCaseExpectError({ policy: basePolicy(), lanes: { evidence: { ...cleanEvidence, lane_type: "external_context" } } });
});

test("invalid lane status is rejected", () => {
  runCaseExpectError({ policy: basePolicy(), lanes: { evidence: { ...cleanEvidence, status: "done" } } });
});

test("lane details preserve unknown fields", () => {
  const evidence = { ...cleanEvidence, reviewer_note: "kept" };
  const result = runCase({ policy: basePolicy(), lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
  const detail = result.lane_details.find((lane) => lane.lane_type === "evidence");
  assert.equal(detail.reviewer_note, "kept");
});

test("empty required reviews do not permit action", () => {
  const result = runCase({ policy: basePolicy(), lanes: { evidence: {}, external_context: {}, graph_history: cleanGraph } });
  assert.equal(result.maximum_recommended_size, 0);
  assert.deepEqual(result.missing_lanes, ["evidence", "external_context"]);
});

for (const support of [undefined, "not_applicable", "weak", "none"]) {
  test(`repeat support ${support} does not permit action`, () => {
    const evidence = structuredClone(cleanEvidence);
    if (support === undefined) delete evidence.decision.repeat_or_top_up_support;
    else evidence.decision.repeat_or_top_up_support = support;
    const result = runCase({ policy: basePolicy({ requested_action: { size: 5, is_repeat_action: true } }),
      lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
    assert.equal(result.maximum_recommended_size, 0);
    assert(result.reasons.some(reason => reason.code === "REPEAT_ACTION_WITHOUT_FRESH_REASON"));
  });
}

for (const lane of [null, [], { status: "completed" }, { status: "completed", findings: [], decision: {} },
  { ...cleanEvidence, findings: "none" }, { ...cleanEvidence, decision: [] },
  { ...cleanEvidence, findings: [{ severity: "HIGH " }] }]) {
  test(`malformed review rejected: ${JSON.stringify(lane)}`, () => {
    runCaseExpectError({ policy: basePolicy(), lanes: { evidence: lane, external_context: cleanExternal } });
  });
}
for (const field of Object.keys(cleanEvidence.decision)) {
  test(`invalid ${field} rejected`, () => {
    runCaseExpectError({ policy: basePolicy(), lanes: { evidence: {
      ...cleanEvidence, decision: { ...cleanEvidence.decision, [field]: "invalid" } } } });
  });
}
for (const field of Object.keys(cleanExternal.decision)) {
  test(`invalid ${field} rejected`, () => {
    runCaseExpectError({ policy: basePolicy(), lanes: { external_context: {
      ...cleanExternal, decision: { ...cleanExternal.decision, [field]: "invalid" } } } });
  });
}
test("explicit fresh repeat reason permits action", () => {
  const evidence = { ...cleanEvidence, decision: { ...cleanEvidence.decision, repeat_or_top_up_support: "fresh_reason_present" } };
  const result = runCase({ policy: basePolicy({ requested_action: { size: 5, is_repeat_action: true } }),
    lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
  assert.equal(result.maximum_recommended_size, 5);
});
test("required error lane stays zero", () => {
  const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: { status: "error" }, graph_history: cleanGraph } });
  assert.equal(result.maximum_recommended_size, 0);
});
test("contradicted linkage rejects despite positive context", () => {
  const evidence = { ...cleanEvidence, decision: { ...cleanEvidence.decision, claimant_linkage: "contradicted" } };
  const result = runCase({ policy: basePolicy(), lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
  assert.equal(result.disposition, "reject_current_record");
  assert.equal(result.maximum_recommended_size, 0);
});
for (const code of ["FAST_OUTFLOW_ONLY", "WEBSITE_INACCESSIBLE", "PRIVACY_REDACTIONS", "NEVER_FUNDED_NO_OUTCOMES"]) {
  test(`${code} alone does not deny supported action`, () => {
    const evidence = { ...cleanEvidence, findings: [{ code, severity: "info", summary: "No independent adverse evidence." }] };
    const result = runCase({ policy: basePolicy(), lanes: { evidence, external_context: cleanExternal, graph_history: cleanGraph } });
    assert.equal(result.maximum_recommended_size, 5);
  });
}
test("operator required linkage review cannot be replaced by positive context", () => {
  const result = runCase({ policy: basePolicy({ required_lanes: ["evidence", "external_context", "recipient_linkage"] }),
    lanes: { evidence: cleanEvidence, external_context: cleanExternal, graph_history: cleanGraph,
      recipient_linkage: { status: "missing" } } });
  assert.equal(result.maximum_recommended_size, 0);
  assert(result.missing_lanes.includes("recipient_linkage"));
});

function outputCase() {
  const dir = tempDir();
  const policy = writeJson(dir, "policy.json", basePolicy());
  const evidence = writeJson(dir, "evidence.json", cleanEvidence);
  const external = writeJson(dir, "external.json", cleanExternal);
  const graph = writeJson(dir, "graph.json", cleanGraph);
  const out = path.join(dir, "out.json");
  const args = [SCRIPT, "--policy", policy, "--lane", `evidence=${evidence}`,
    "--lane", `external_context=${external}`, "--lane", `graph_history=${graph}`];
  const run = (target = out, preload) => spawnSync(process.execPath, [...(preload ? ["--import", pathToFileURL(preload).href] : []), ...args, "--out", target], { encoding: "utf8" });
  return { dir, policy, evidence, out, run };
}

test("successful output then malformed review removes stale eligibility", () => {
  const c = outputCase();
  assert.equal(c.run().status, 0);
  assert.equal(JSON.parse(fs.readFileSync(c.out)).maximum_recommended_size, 5);
  fs.writeFileSync(c.evidence, "{");
  assert.equal(c.run().status, 1);
  assert.equal(fs.existsSync(c.out), false);
});

test("missing input removes stale eligibility", () => {
  const c = outputCase();
  assert.equal(c.run().status, 0);
  fs.unlinkSync(c.evidence);
  assert.equal(c.run().status, 1);
  assert.equal(fs.existsSync(c.out), false);
});

for (const input of ["policy", "evidence"]) {
  test(`output cannot overwrite ${input} input`, () => {
    const c = outputCase();
    const before = fs.readFileSync(c[input]);
    assert.equal(c.run(c[input]).status, 1);
    assert.deepEqual(fs.readFileSync(c[input]), before);
  });
}

test("hardlinked output cannot alter an input", () => {
  const c = outputCase();
  fs.linkSync(c.evidence, c.out);
  const before = fs.readFileSync(c.evidence);
  assert.equal(c.run().status, 1);
  assert.deepEqual(fs.readFileSync(c.evidence), before);
  assert.deepEqual(fs.readFileSync(c.out), before);
});

test("output directory rejected without removing its contents", () => {
  const c = outputCase();
  fs.mkdirSync(c.out);
  const marker = writeJson(c.out, "keep.json", { keep: true });
  assert.equal(c.run().status, 1);
  assert.deepEqual(JSON.parse(fs.readFileSync(marker)), { keep: true });
});

test("output creation failure returns no eligible stdout", () => {
  const c = outputCase();
  const blocker = writeJson(c.dir, "file-parent", { keep: true });
  const result = c.run(path.join(blocker, "out.json"));
  assert.equal(result.status, 1);
  assert.equal(result.stdout, "");
  assert.deepEqual(JSON.parse(fs.readFileSync(blocker)), { keep: true });
});

test("successful output replaces prior result and creates nested directory", () => {
  const c = outputCase();
  const out = path.join(c.dir, "nested", "result.json");
  assert.equal(c.run(out).status, 0);
  assert.equal(c.run(out).status, 0);
  const result = JSON.parse(fs.readFileSync(out));
  assert.equal(result.maximum_recommended_size, 5);
  assert.equal(result.review_version, "0.3.0");
  assert.deepEqual(fs.readdirSync(path.dirname(out)), ["result.json"]);
});

test("directory-link alias cannot overwrite lane input", () => {
  const c = outputCase();
  const alias = path.join(c.dir, "alias");
  fs.symlinkSync(c.dir, alias, process.platform === "win32" ? "junction" : "dir");
  const before = fs.readFileSync(c.evidence);
  assert.equal(c.run(path.join(alias, "evidence.json")).status, 1);
  assert.deepEqual(fs.readFileSync(c.evidence), before);
});

for (const operation of ["writeFileSync", "renameSync"]) {
  test(`${operation} failure leaves no stale output or temporary result`, () => {
    const c = outputCase();
    assert.equal(c.run().status, 0);
    const preload = path.join(c.dir, "fault.mjs");
    fs.writeFileSync(preload, `import fs from "node:fs";
      const original = fs.${operation};
      fs.${operation} = function(file, ...args) {
        if (typeof file === "number" || String(file).endsWith(".tmp")) {
          ${operation === "writeFileSync" ? 'original.call(this, file, "partial", args[1]);' : ''}
          throw new Error("synthetic output failure");
        }
        return original.call(this, file, ...args);
      };`);
    const result = c.run(c.out, preload);
    assert.equal(result.status, 1);
    assert.equal(result.stdout, "");
    assert.equal(fs.existsSync(c.out), false);
    assert.equal(fs.readdirSync(c.dir).some(name => name.endsWith(".tmp")), false);
    assert.deepEqual(JSON.parse(fs.readFileSync(c.evidence)), cleanEvidence);
  });
}

test("exclusive-create collision preserves the unowned temporary file", () => {
  const c = outputCase();
  assert.equal(c.run().status, 0);
  const preload = path.join(c.dir, "collision.mjs");
  fs.writeFileSync(preload, `import fs from "node:fs";
    const original = fs.openSync;
    fs.openSync = function(file, flags, ...args) {
      if (String(file).endsWith(".tmp") && flags === "wx") {
        fs.writeFileSync(file, "pre-existing unrelated data");
      }
      return original.call(this, file, flags, ...args);
    };`);
  assert.equal(c.run(c.out, preload).status, 1);
  assert.equal(fs.existsSync(c.out), false);
  const temporary = fs.readdirSync(c.dir).filter(name => name.endsWith(".tmp"));
  assert.equal(temporary.length, 1);
  assert.equal(fs.readFileSync(path.join(c.dir, temporary[0]), "utf8"), "pre-existing unrelated data");
});

function supportCase(decision = {}, preferences = {}, extra = {}) {
  return runCase({ policy: basePolicy({ disposition_preferences: preferences, ...extra }), lanes: {
    evidence: { ...cleanEvidence, decision: { ...cleanEvidence.decision, ...decision } },
    external_context: cleanExternal, graph_history: cleanGraph,
  } });
}

test("Issue 113 unknown support cannot yield full action or high confidence", () => {
  const result = runCase({ policy: basePolicy({ requested_action: { size: 3, is_repeat_action: false } }), lanes: {
    evidence: { ...cleanEvidence, decision: { ...cleanEvidence.decision, supports_core_claim: "unknown", claimant_linkage: "unknown" } },
    external_context: { ...cleanExternal, decision: { public_context_plausibility: "not_found", source_independence: "not_applicable" } },
  } });
  assert.equal(result.maximum_recommended_size, 0);
  assert(result.reasons.length > 0);
  assert.notEqual(result.confidence, "medium_to_high");
});

for (const field of ["supports_core_claim", "claimant_linkage", "supports_requested_action_size"]) {
  for (const value of ["unknown", "partial"]) {
    test(`${field} ${value} waits unless bounded uncertainty is explicit`, () => {
      const waiting = supportCase({ [field]: value });
      assert.equal(waiting.maximum_recommended_size, 0);
      const bounded = supportCase({ [field]: value }, { uncertainty_action: "small_test" });
      assert.equal(bounded.disposition, "eligible_for_small_test_action");
      assert.equal(bounded.maximum_recommended_size, 1);
      assert.equal(bounded.confidence, "low_to_medium");
      assert(bounded.reasons.length > 0);
    });
  }
}
for (const value of ["no", "unsupported", "contradiction"]) {
  test(`negative core ${value} cannot be rescued by context or preferences`, () => {
    const result = supportCase({ supports_core_claim: value }, {
      uncertainty_action: "small_test", reject_on_any_high: false, reject_on_any_critical: false,
    });
    assert.equal(result.maximum_recommended_size, 0);
    assert.equal(result.disposition, "reject_current_record");
  });
}
test("contradicted linkage cannot be rescued by uncertainty permission", () => {
  assert.equal(supportCase({ claimant_linkage: "contradicted" }, { uncertainty_action: "small_test", reject_on_any_high: false }).maximum_recommended_size, 0);
});
for (const confidence of [undefined, null, "unknown", "low"]) {
  test(`review confidence ${confidence} cannot silently increase eligibility`, () => {
    const lanes = { evidence: { ...cleanEvidence, confidence }, external_context: cleanExternal, graph_history: cleanGraph };
    const result = runCase({ policy: basePolicy(), lanes });
    assert.equal(result.maximum_recommended_size, 0);
    assert.notEqual(result.confidence, "medium_to_high");
    assert.equal(runCase({ policy: basePolicy({ disposition_preferences: { uncertainty_action: "small_test" } }), lanes }).maximum_recommended_size, 1);
  });
}
test("invalid uncertainty preference is rejected", () => {
  runCaseExpectError({ policy: basePolicy({ disposition_preferences: { uncertainty_action: "full" } }), lanes: { evidence: cleanEvidence, external_context: cleanExternal } });
});
test("uncertainty permission cannot bypass required lane or fresh repeat support", () => {
  const prefs = { uncertainty_action: "small_test" };
  assert.equal(runCase({ policy: basePolicy({ disposition_preferences: prefs }), lanes: { evidence: cleanEvidence, external_context: cleanExternal } }).maximum_recommended_size, 0);
  assert.equal(supportCase({ supports_core_claim: "unknown" }, prefs, { requested_action: { size: 5, is_repeat_action: true } }).maximum_recommended_size, 0);
});

test("fully supported high-confidence action remains eligible", () => {
  const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: cleanExternal,
    graph_history: { ...cleanGraph, confidence: "high" } } });
  assert.equal(result.disposition, "eligible_for_full_policy_action");
  assert.equal(result.confidence, "medium_to_high");
  assert.equal(result.policy.uncertainty_action, "monitor");
});
test("legacy small-test preference does not implicitly authorize uncertainty", () => {
  assert.equal(supportCase({ claimant_linkage: "partial" }, { multiple_medium_concerns: "eligible_for_small_test_action" }).maximum_recommended_size, 0);
});
test("explicit uncertainty stays within all existing size caps", () => {
  const result = supportCase({ supports_core_claim: "partial" }, { uncertainty_action: "small_test" }, {
    requested_action: { size: 0.5, is_repeat_action: false },
    authority: { max_autonomous_action_size: 0.75, small_test_action_size: 1, serious_action_threshold: 5 },
  });
  assert.equal(result.maximum_recommended_size, 0.5);
});
test("fresh repeat may use explicit bounded uncertainty but not override a policy blocker", () => {
  const decision = { supports_core_claim: "partial", repeat_or_top_up_support: "fresh_reason_present" };
  assert.equal(supportCase(decision, { uncertainty_action: "small_test" }, { requested_action: { size: 5, is_repeat_action: true } }).maximum_recommended_size, 1);
  const result = runCase({ policy: basePolicy({ disposition_preferences: { uncertainty_action: "small_test" } }), lanes: {
    evidence: { ...cleanEvidence, decision: { ...cleanEvidence.decision, ...decision }, findings: [{ code: "DOMAIN_HARD_BLOCKER", severity: "info" }] },
    external_context: cleanExternal, graph_history: cleanGraph,
  } });
  assert.equal(result.maximum_recommended_size, 0);
});
test("contradiction in another completed lane is not masked by positive evidence", () => {
  const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: {
    ...cleanExternal, decision: { ...cleanExternal.decision, claimant_linkage: "contradicted" } }, graph_history: cleanGraph } });
  assert.equal(result.disposition, "reject_current_record");
});
test("invalid reviewer confidence is rejected", () => {
  runCaseExpectError({ policy: basePolicy(), lanes: { evidence: { ...cleanEvidence, confidence: "certain" } } });
});
test("uncertainty opt-in does not permit high findings when rejection preference is disabled", () => {
  const result = runCase({ policy: basePolicy({ disposition_preferences: { uncertainty_action: "small_test", reject_on_any_high: false } }), lanes: {
    evidence: { ...cleanEvidence, findings: [{ severity: "high", code: "ADVERSE" }] }, external_context: cleanExternal, graph_history: cleanGraph,
  } });
  assert.equal(result.maximum_recommended_size, 0);
});

test("one medium finding remains material uncertainty", () => {
  const lanes = { evidence: { ...cleanEvidence, findings: [{ code: "UNRESOLVED", severity: "medium", summary: "Material review limitation." }] }, external_context: cleanExternal, graph_history: cleanGraph };
  const result = runCase({ policy: basePolicy(), lanes });
  assert.equal(result.maximum_recommended_size, 0);
  assert.equal(result.confidence, "low_to_medium");
  assert(result.reasons.some(reason => reason.refs.includes("evidence:UNRESOLVED")));
  assert.equal(runCase({ policy: basePolicy({ disposition_preferences: { uncertainty_action: "small_test" } }), lanes }).maximum_recommended_size, 1);
});
for (const cap of [undefined, null, 0, -1, "bad"]) {
  test(`uncertainty opt-in rejects absent or invalid explicit cap ${cap}`, () => {
    runCaseExpectError({ policy: basePolicy({ disposition_preferences: { uncertainty_action: "small_test" }, authority: {
      max_autonomous_action_size: 10, small_test_action_size: cap, serious_action_threshold: 5,
    } }), lanes: { evidence: cleanEvidence, external_context: cleanExternal, graph_history: cleanGraph } });
  });
}

for (const status of ["error", "missing", "not_applicable"]) {
  test(`optional ${status} source does not convert failed access into adverse evidence`, () => {
    const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: cleanExternal, graph_history: cleanGraph,
      optional_social: { status, decision: { supports_requested_action_size: "unsupported" } },
    } });
    assert.equal(result.maximum_recommended_size, 5);
    assert.equal(result.reasons.length, 0);
    assert.equal(result.lane_details.find(lane => lane.lane_type === "optional_social").status, status);
  });
}
test("required unavailable source still blocks despite positive completed reviews", () => {
  const result = runCase({ policy: basePolicy({ required_lanes: ["evidence", "external_context", "optional_social"], disposition_preferences: { uncertainty_action: "small_test" } }), lanes: {
    evidence: cleanEvidence, external_context: cleanExternal, graph_history: cleanGraph, optional_social: { status: "error" },
  } });
  assert.equal(result.maximum_recommended_size, 0);
});

test("explicit adverse finding survives an optional incomplete review", () => {
  const result = runCase({ policy: basePolicy(), lanes: { evidence: cleanEvidence, external_context: cleanExternal, graph_history: cleanGraph,
    optional_social: { status: "error", findings: [{ severity: "high", code: "ADVERSE_FACT", summary: "An independently established adverse finding predates failed access." }] },
  } });
  assert.equal(result.maximum_recommended_size, 0);
  assert(result.reasons.some(reason => reason.refs.includes("optional_social:ADVERSE_FACT")));
});

if (process.exitCode) process.exit(process.exitCode);
