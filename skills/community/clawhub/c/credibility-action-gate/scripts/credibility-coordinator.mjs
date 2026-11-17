#!/usr/bin/env node
/*
 * credibility-coordinator
 *
 * Deterministic coordinator for claim-quality review lanes.
 * Reads lane JSON plus operator policy, writes an analysis-only action disposition.
 */

import fs from "node:fs";
import path from "node:path";
import { randomUUID } from "node:crypto";

const SEVERITY_RANK = {
  info: 0,
  low: 1,
  medium: 2,
  high: 3,
  critical: 4,
};

const VALID_LANE_STATUSES = new Set(["completed", "missing", "not_applicable", "error"]);

const DEFAULT_POLICY = {
  policy_name: "default-policy",
  policy_version: "0.1.0",
  requested_action: {
    type: "bounded_action",
    size: 1,
    unit: "configured_unit",
    is_repeat_action: false,
  },
  authority: {
    max_autonomous_action_size: 1,
    small_test_action_size: 1,
    serious_action_threshold: 1,
  },
  required_lanes: ["evidence", "external_context"],
  required_lanes_for_serious_action: ["evidence", "external_context"],
  hard_blocker_codes: [
    "POLICY_AUTHORITY_EXCEEDED",
    "DOMAIN_HARD_BLOCKER",
    "CONTRADICTION_IN_RECORD",
  ],
  disposition_preferences: {
    uncertainty_action: "monitor",
    reject_on_any_critical: true,
    reject_on_any_high: true,
    missing_required_lane: "monitor_until_new_evidence",
    missing_required_lane_for_serious_action: "monitor_until_new_evidence",
    repeat_action_without_fresh_reason: "monitor_until_new_evidence",
  },
};

function usage() {
  return `Usage:
  node scripts/credibility-coordinator.mjs --policy policy.json --lane evidence=evidence.json [--lane external_context=external.json] [--out disposition.json]

Options:
  --policy FILE       Operator policy JSON. If omitted, conservative defaults are used.
  --lane NAME=FILE    Review lane JSON. Repeat for multiple lanes.
  --out FILE          Write output JSON to FILE instead of stdout.
`;
}

function parseArgs(argv) {
  const args = { lanes: [] };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--help" || arg === "-h") {
      process.stdout.write(usage());
      process.exit(0);
    }
    if (arg === "--policy") args.policyFile = argv[++index];
    else if (arg === "--lane") args.lanes.push(argv[++index]);
    else if (arg === "--out") args.out = argv[++index];
    else throw new Error(`Unknown argument: ${arg}`);
  }
  return args;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

// Resolve existing ancestors too, so aliases through directory links are detected
// even when the selected output or an input does not exist yet.
function canonicalPath(file) {
  const absolute = path.resolve(file);
  try {
    return fs.realpathSync(absolute);
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    const parent = path.dirname(absolute);
    if (parent === absolute) throw error;
    return path.join(canonicalPath(parent), path.basename(absolute));
  }
}

function prepareOutput(file, inputFiles) {
  const output = path.resolve(file);
  let stat;
  try { stat = fs.lstatSync(output); }
  catch (error) { if (error.code !== "ENOENT") throw error; }
  if (stat && (!stat.isFile() || stat.nlink !== 1)) {
    throw new Error("Output must be a regular file with one link, not a directory or link.");
  }
  const comparable = (value) => process.platform === "win32" ? value.toLowerCase() : value;
  const destination = canonicalPath(output);
  for (const input of inputFiles) {
    if (comparable(destination) === comparable(canonicalPath(input))) {
      throw new Error("Output must not alias a policy or lane input.");
    }
  }
  // Only the explicitly selected, validated output is invalidated. Do this
  // before reading/parsing inputs, so their failures cannot retain eligibility.
  if (stat) fs.unlinkSync(output);
  return destination;
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const temporary = `${file}.${randomUUID()}.tmp`;
  let owned = false;
  try {
    const fd = fs.openSync(temporary, "wx", 0o600);
    owned = true;
    try { fs.writeFileSync(fd, `${JSON.stringify(data, null, 2)}\n`); }
    finally { fs.closeSync(fd); }
    fs.renameSync(temporary, file);
  } finally {
    if (owned) {
      try { fs.unlinkSync(temporary); }
      catch (error) { if (error.code !== "ENOENT") throw error; }
    }
  }
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function asNumber(value, fallback = 0) {
  return Number.isFinite(Number(value)) ? Number(value) : fallback;
}

function normalizeSeverity(severity) {
  const normalized = String(severity ?? "info").toLowerCase();
  return Object.prototype.hasOwnProperty.call(SEVERITY_RANK, normalized) ? normalized : "info";
}

function severityRank(severity) {
  return SEVERITY_RANK[normalizeSeverity(severity)] ?? 0;
}

function highestSeverity(findings) {
  return asArray(findings).reduce((highest, finding) => {
    return severityRank(finding.severity) > severityRank(highest) ? normalizeSeverity(finding.severity) : highest;
  }, "info");
}

function mergePolicy(input) {
  const policy = input && typeof input === "object" ? input : {};
  const uncertainty = policy.disposition_preferences?.uncertainty_action;
  if (uncertainty !== undefined && !["monitor", "small_test"].includes(uncertainty)) {
    throw new Error("uncertainty_action must be monitor or small_test.");
  }
  if (uncertainty === "small_test" &&
      !(typeof policy.authority?.small_test_action_size === "number" &&
        Number.isFinite(policy.authority.small_test_action_size) && policy.authority.small_test_action_size > 0)) {
    throw new Error("small_test uncertainty permission requires an explicit positive finite small_test_action_size.");
  }
  return {
    ...DEFAULT_POLICY,
    ...policy,
    requested_action: {
      ...DEFAULT_POLICY.requested_action,
      ...(policy.requested_action ?? {}),
    },
    authority: {
      ...DEFAULT_POLICY.authority,
      ...(policy.authority ?? {}),
    },
    disposition_preferences: {
      ...DEFAULT_POLICY.disposition_preferences,
      ...(policy.disposition_preferences ?? {}),
    },
    required_lanes: Array.isArray(policy.required_lanes) ? policy.required_lanes : DEFAULT_POLICY.required_lanes,
    required_lanes_for_serious_action: Array.isArray(policy.required_lanes_for_serious_action)
      ? policy.required_lanes_for_serious_action
      : DEFAULT_POLICY.required_lanes_for_serious_action,
    hard_blocker_codes: Array.isArray(policy.hard_blocker_codes)
      ? policy.hard_blocker_codes
      : DEFAULT_POLICY.hard_blocker_codes,
  };
}

function parseLaneSpec(spec) {
  const splitAt = spec.indexOf("=");
  if (splitAt <= 0 || splitAt === spec.length - 1) throw new Error(`Lane must be NAME=FILE, got: ${spec}`);
  return {
    laneType: spec.slice(0, splitAt),
    file: spec.slice(splitAt + 1),
  };
}

function normalizeFinding(finding) {
  return {
    code: String(finding?.code ?? "UNSPECIFIED_FINDING"),
    severity: normalizeSeverity(finding?.severity),
    summary: String(finding?.summary ?? finding?.description ?? ""),
    evidence_refs: asArray(finding?.evidence_refs),
  };
}

const DECISION_VALUES = {
  supports_core_claim: ["yes", "partial", "unknown", "no", "contradiction", "unsupported"],
  supports_requested_action_size: ["yes", "partial", "unknown", "no", "unsupported"],
  source_independence: ["strong", "some", "weak", "none", "not_applicable"],
  public_context_plausibility: ["all_found", "some_found", "weak", "not_found", "not_applicable"],
  claimant_linkage: ["verified", "partial", "unknown", "unverified", "contradicted"],
  repeat_or_top_up_support: ["fresh_reason_present", "weak", "none", "not_applicable"],
};

function isRecord(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function normalizeLane(laneType, raw) {
  if (!isRecord(raw)) throw new Error(`Lane "${laneType}" must be a JSON object.`);
  if (raw?.lane_type !== undefined && String(raw.lane_type) !== laneType) {
    throw new Error(`Lane spec "${laneType}" does not match lane_type "${raw.lane_type}" in lane JSON.`);
  }
  const status = raw.status === undefined ? "missing" : raw.status;
  if (!VALID_LANE_STATUSES.has(status)) {
    throw new Error(`Invalid status "${status}" for lane "${laneType}".`);
  }
  if (status === "completed") {
    if (!Array.isArray(raw.findings) || !isRecord(raw.decision)) {
      throw new Error(`Completed lane "${laneType}" requires findings and decision.`);
    }
    const requiredFields = laneType === "evidence"
      ? ["supports_core_claim", "supports_requested_action_size", "claimant_linkage"]
      : laneType === "external_context" ? ["public_context_plausibility", "source_independence"] : [];
    for (const field of requiredFields) {
      if (!Object.prototype.hasOwnProperty.call(raw.decision, field)) {
        throw new Error(`Completed lane "${laneType}" requires decision.${field}.`);
      }
    }
  }
  if (raw.decision !== undefined && !isRecord(raw.decision)) {
    throw new Error(`Invalid decision object for lane "${laneType}".`);
  }
  for (const [field, values] of Object.entries(DECISION_VALUES)) {
    if (raw.decision && Object.prototype.hasOwnProperty.call(raw.decision, field) &&
        !values.includes(raw.decision[field])) {
      throw new Error(`Invalid decision.${field} for lane "${laneType}".`);
    }
  }
  for (const finding of asArray(raw.findings)) {
    if (!isRecord(finding) || !Object.prototype.hasOwnProperty.call(SEVERITY_RANK, finding.severity)) {
      throw new Error(`Invalid finding or severity for lane "${laneType}".`);
    }
  }
  if (raw.confidence != null && !["high", "medium", "low", "unknown"].includes(raw.confidence)) {
    throw new Error(`Invalid confidence for lane "${laneType}".`);
  }
  const lane = {
    ...(raw && typeof raw === "object" ? raw : {}),
    lane_type: String(raw?.lane_type ?? laneType),
    status,
    confidence: raw?.confidence ?? null,
    findings: asArray(raw?.findings).map(normalizeFinding),
    positives: asArray(raw?.positives),
    decision: raw?.decision && typeof raw.decision === "object" ? raw.decision : {},
    limitations: asArray(raw?.limitations),
  };
  lane.highest_severity = highestSeverity(lane.findings);
  return lane;
}

function loadLanes(laneSpecs) {
  return laneSpecs.map((spec) => {
    const parsed = parseLaneSpec(spec);
    return normalizeLane(parsed.laneType, readJson(parsed.file));
  });
}

function isSeriousAction(policy) {
  const size = asNumber(policy.requested_action?.size, 0);
  const threshold = asNumber(policy.authority?.serious_action_threshold, Number.POSITIVE_INFINITY);
  return size >= threshold;
}

function laneMap(lanes) {
  const map = new Map();
  for (const lane of lanes) map.set(lane.lane_type, lane);
  return map;
}

function missingLanes(policy, lanes) {
  const map = laneMap(lanes);
  const required = new Set(asArray(policy.required_lanes));
  if (isSeriousAction(policy)) {
    for (const lane of asArray(policy.required_lanes_for_serious_action)) required.add(lane);
  }
  return [...required].filter((lane) => !map.has(lane) || map.get(lane).status !== "completed");
}

function collectSignals(policy, lanes) {
  const signals = [];
  const hardCodes = new Set(asArray(policy.hard_blocker_codes));
  const allFindings = lanes.flatMap((lane) =>
    lane.findings.map((finding) => ({ ...finding, lane_type: lane.lane_type })));
  const highFindings = allFindings.filter((finding) => severityRank(finding.severity) >= SEVERITY_RANK.high);
  const criticalFindings = allFindings.filter((finding) => severityRank(finding.severity) >= SEVERITY_RANK.critical);
  const mediumPlusFindings = allFindings.filter((finding) => severityRank(finding.severity) >= SEVERITY_RANK.medium);
  const concernLanes = new Set(mediumPlusFindings.map((finding) => finding.lane_type));
  const hardBlockerFindings = allFindings.filter((finding) => hardCodes.has(finding.code));
  const missing = missingLanes(policy, lanes);
  const map = laneMap(lanes);
  const evidence = map.get("evidence")?.decision ?? {};
  const external = map.get("external_context")?.decision ?? {};
  const repeatSupport = map.get("evidence")?.status === "completed" && evidence.repeat_or_top_up_support !== undefined
    ? evidence.repeat_or_top_up_support
    : map.get("external_context")?.status === "completed" ? external.repeat_or_top_up_support : undefined;
  const actionSizeSupport = lanes
    .filter((lane) => lane.status === "completed" && Object.prototype.hasOwnProperty.call(lane.decision, "supports_requested_action_size"))
    .map((lane) => ({
      lane_type: lane.lane_type,
      value: String(lane.decision.supports_requested_action_size ?? "unknown"),
    }));
  const sourceIndependence = map.get("external_context")?.status === "completed"
    ? String(external.source_independence ?? "not_applicable") : "not_applicable";

  if (hardBlockerFindings.length > 0) {
    signals.push({
      code: "HARD_BLOCKER_CODE_PRESENT",
      severity: "critical",
      summary: "At least one finding matches the operator policy hard-blocker list.",
      refs: hardBlockerFindings.map((finding) => `${finding.lane_type}:${finding.code}`),
    });
  }
  if (criticalFindings.length > 0) {
    signals.push({
      code: "ANY_CRITICAL_FINDING",
      severity: "critical",
      summary: "At least one lane emitted a critical finding.",
      refs: criticalFindings.map((finding) => `${finding.lane_type}:${finding.code}`),
    });
  }
  if (highFindings.length > 0) {
    signals.push({
      code: "ANY_HIGH_FINDING",
      severity: "high",
      summary: "At least one lane emitted a high-or-higher finding.",
      refs: highFindings.map((finding) => `${finding.lane_type}:${finding.code}`),
    });
  }
  if (mediumPlusFindings.length === 1 && mediumPlusFindings[0].severity === "medium") {
    signals.push({ code: "MATERIAL_REVIEW_CONCERN", severity: "medium",
      summary: "A lane reports a material review concern.",
      refs: mediumPlusFindings.map((finding) => `${finding.lane_type}:${finding.code}`) });
  }
  if (mediumPlusFindings.length >= 2 || concernLanes.size >= 2) {
    signals.push({
      code: "MULTIPLE_MEDIUM_OR_CROSS_LANE_CONCERNS",
      severity: "medium",
      summary: "Multiple material concerns appear across the record.",
      refs: mediumPlusFindings.map((finding) => `${finding.lane_type}:${finding.code}`),
    });
  }
  if (missing.length > 0) {
    signals.push({
      code: "REQUIRED_LANE_UNAVAILABLE",
      severity: "medium",
      summary: "One or more required lanes are missing, errored, or not applicable on the current record.",
      refs: missing,
    });
  }
  // Material decision fields remain distinct from general public context.
  for (const lane of lanes.filter((lane) => lane.status === "completed")) {
    for (const field of ["supports_core_claim", "claimant_linkage"]) {
      const value = lane.decision[field];
      if (value === undefined) continue;
      const contradiction = ["contradiction", "contradicted"].includes(value);
      const negative = ["no", "unsupported"].includes(value);
      const uncertain = ["unknown", "partial", "unverified"].includes(value);
      if (contradiction || negative || uncertain) signals.push({
        code: contradiction ? "MATERIAL_CLAIM_CONTRADICTED" : negative ? "CORE_CLAIM_UNSUPPORTED" : "MATERIAL_SUPPORT_UNCERTAIN",
        severity: contradiction || negative ? "high" : "medium",
        summary: `${lane.lane_type}.${field} is ${value} on the reviewed record.`,
        refs: [`${lane.lane_type}:${field}`],
      });
    }
    if (lane.confidence == null || ["unknown", "low"].includes(lane.confidence)) signals.push({
      code: "REVIEW_CONFIDENCE_UNCERTAIN",
      severity: "medium",
      summary: `${lane.lane_type} reviewer confidence is ${lane.confidence ?? "unspecified"}.`,
      refs: [`${lane.lane_type}:confidence`],
    });
  }
  for (const field of ["supports_core_claim", "claimant_linkage", "supports_requested_action_size"]) {
    if (!lanes.some((lane) => lane.status === "completed" && lane.decision[field] !== undefined)) {
      signals.push({ code: "MATERIAL_SUPPORT_UNCERTAIN", severity: "medium",
        summary: `No completed lane reports ${field}.`, refs: [field] });
    }
  }
  const unsupportedActionSize = actionSizeSupport.filter((entry) => ["no", "unsupported"].includes(entry.value));
  if (unsupportedActionSize.length > 0) {
    signals.push({
      code: "REQUESTED_ACTION_SIZE_UNSUPPORTED",
      severity: "high",
      summary: "At least one lane says the current record does not support the requested action size.",
      refs: unsupportedActionSize.map((entry) => `${entry.lane_type}:supports_requested_action_size`),
    });
  } else {
    const weakActionSize = actionSizeSupport.filter((entry) => ["partial", "unknown"].includes(entry.value));
    if (weakActionSize.length > 0) {
      signals.push({
        code: "REQUESTED_ACTION_SIZE_NOT_FULLY_SUPPORTED",
        severity: "medium",
        summary: "At least one lane only partially supports, or cannot confirm, the requested action size.",
        refs: weakActionSize.map((entry) => `${entry.lane_type}:supports_requested_action_size`),
      });
    }
  }
  if (["weak", "none"].includes(sourceIndependence)) {
    signals.push({
      code: "SOURCE_INDEPENDENCE_WEAK",
      severity: "medium",
      summary: "External context does not provide strong independent support.",
      refs: ["external_context:source_independence"],
    });
  }
  if (policy.requested_action?.is_repeat_action && repeatSupport !== "fresh_reason_present") {
    signals.push({
      code: "REPEAT_ACTION_WITHOUT_FRESH_REASON",
      severity: "medium",
      summary: "Repeat action lacks a fresh reason on the current record.",
      refs: ["repeat_or_top_up_support"],
    });
  }

  const requestedSize = asNumber(policy.requested_action?.size, 0);
  const maxSize = asNumber(policy.authority?.max_autonomous_action_size, 0);
  if (requestedSize > maxSize) {
    signals.push({
      code: "POLICY_AUTHORITY_EXCEEDED",
      severity: "critical",
      summary: "Requested action size exceeds configured autonomous authority.",
      refs: ["policy.authority.max_autonomous_action_size"],
    });
  }

  return {
    all_findings: allFindings,
    high_findings: highFindings,
    medium_plus_findings: mediumPlusFindings,
    concern_lane_count: concernLanes.size,
    missing_lanes: missing,
    signals,
  };
}

function chooseDisposition(policy, signals) {
  const prefs = policy.disposition_preferences ?? {};
  const hasCode = (code) => signals.some((signal) => signal.code === code);
  const anyCritical = signals.some((signal) => severityRank(signal.severity) >= SEVERITY_RANK.critical);
  const anyHigh = signals.some((signal) => severityRank(signal.severity) >= SEVERITY_RANK.high);
  const anyMedium = signals.some((signal) => severityRank(signal.severity) >= SEVERITY_RANK.medium);
  const requestedSize = asNumber(policy.requested_action?.size, 0);
  const maxSize = asNumber(policy.authority?.max_autonomous_action_size, 0);
  const smallSize = asNumber(policy.authority?.small_test_action_size, Math.min(requestedSize, maxSize));

  if (hasCode("POLICY_AUTHORITY_EXCEEDED") || hasCode("HARD_BLOCKER_CODE_PRESENT")) {
    return {
      disposition: "blocked_by_operator_or_legal_policy",
      action_size_guidance: "do_not_act_without_policy_change",
      maximum_recommended_size: 0,
    };
  }
  if (hasCode("MATERIAL_CLAIM_CONTRADICTED") || hasCode("CORE_CLAIM_UNSUPPORTED") ||
      hasCode("REQUESTED_ACTION_SIZE_UNSUPPORTED")) {
    return { disposition: "reject_current_record", action_size_guidance: "do_not_act_on_current_record", maximum_recommended_size: 0 };
  }
  if (anyCritical && prefs.reject_on_any_critical !== false) {
    return {
      disposition: "reject_current_record",
      action_size_guidance: "do_not_act_on_current_record",
      maximum_recommended_size: 0,
    };
  }
  if (anyHigh && prefs.reject_on_any_high !== false) {
    return {
      disposition: "reject_current_record",
      action_size_guidance: "do_not_act_on_current_record",
      maximum_recommended_size: 0,
    };
  }
  if (hasCode("REQUIRED_LANE_UNAVAILABLE")) {
    return {
      disposition: prefs.missing_required_lane ??
        prefs.missing_required_lane_for_serious_action ??
        "monitor_until_new_evidence",
      action_size_guidance: "wait_for_required_lanes",
      maximum_recommended_size: 0,
    };
  }
  if (hasCode("REPEAT_ACTION_WITHOUT_FRESH_REASON")) {
    return {
      disposition: prefs.repeat_action_without_fresh_reason ?? "monitor_until_new_evidence",
      action_size_guidance: "do_not_repeat_without_new_record_support",
      maximum_recommended_size: 0,
    };
  }
  if (anyMedium) {
    const permitBoundedUncertainty = prefs.uncertainty_action === "small_test" && !anyHigh && !anyCritical;
    return {
      disposition: permitBoundedUncertainty ? "eligible_for_small_test_action" : "monitor_until_new_evidence",
      action_size_guidance: permitBoundedUncertainty ? "operator_permitted_bounded_uncertainty" : "wait_for_material_support",
      maximum_recommended_size: permitBoundedUncertainty ? Math.max(0, Math.min(smallSize, maxSize, requestedSize)) : 0,
    };
  }
  if (requestedSize <= maxSize) {
    return {
      disposition: "eligible_for_full_policy_action",
      action_size_guidance: "requested_action_within_policy",
      maximum_recommended_size: requestedSize,
    };
  }
  return {
    disposition: "eligible_for_bounded_action",
    action_size_guidance: "cap_to_operator_policy",
    maximum_recommended_size: maxSize,
  };
}

function confidenceFor(signals, lanes, collected) {
  if (signals.some((signal) => severityRank(signal.severity) >= SEVERITY_RANK.high)) return "low";
  if (collected.missing_lanes.length > 0) return "low_due_to_missing_lanes";
  if (signals.some((signal) => severityRank(signal.severity) >= SEVERITY_RANK.medium)) return "low_to_medium";
  const laneConfidences = lanes.filter((lane) => lane.status === "completed").map((lane) => lane.confidence);
  if (!laneConfidences.length || laneConfidences.some((value) => value == null || value === "unknown")) return "unknown";
  if (laneConfidences.includes("low")) return "low_to_medium";
  if (laneConfidences.includes("medium")) return "medium";
  return "medium_to_high";
}

function coordinate(policyInput, lanes) {
  const policy = mergePolicy(policyInput);
  const collected = collectSignals(policy, lanes);
  const selected = chooseDisposition(policy, collected.signals);
  return {
    review_type: "credibility-action-gate",
    review_version: "0.3.0",
    reviewed_at: new Date().toISOString(),
    status: "completed",
    analysis_only: true,
    policy: {
      policy_name: policy.policy_name,
      policy_version: policy.policy_version,
      action_domain: policy.action_domain ?? "general",
      requested_action: policy.requested_action,
      authority: policy.authority,
      uncertainty_action: policy.disposition_preferences.uncertainty_action,
    },
    disposition: selected.disposition,
    confidence: confidenceFor(collected.signals, lanes, collected),
    action_size_guidance: selected.action_size_guidance,
    maximum_recommended_size: selected.maximum_recommended_size,
    reasons: collected.signals.map((signal) => ({
      code: signal.code,
      severity: signal.severity,
      summary: signal.summary,
      refs: signal.refs,
    })),
    missing_lanes: collected.missing_lanes,
    lane_summary: lanes.map((lane) => ({
      lane_type: lane.lane_type,
      status: lane.status,
      confidence: lane.confidence,
      highest_severity: lane.highest_severity,
      finding_count: lane.findings.length,
    })),
    lane_details: lanes,
    integration_guidance: {
      does_not_execute_action: true,
      use_as_gate_not_mission_selector: true,
      avoid_public_accusation: "Use record-scoped language unless independent evidence supports a stronger public claim.",
    },
  };
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const inputFiles = args.lanes.map((spec) => parseLaneSpec(spec).file);
    if (args.policyFile) inputFiles.push(args.policyFile);
    const output = args.out ? prepareOutput(args.out, inputFiles) : undefined;
    const policy = args.policyFile ? readJson(args.policyFile) : DEFAULT_POLICY;
    const lanes = loadLanes(args.lanes);
    const result = coordinate(policy, lanes);
    if (output) writeJson(output, result);
    else process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } catch (error) {
    process.stderr.write(`credibility-coordinator error: ${error.message}\n`);
    process.exit(1);
  }
}

main();
