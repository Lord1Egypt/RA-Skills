'use strict';

// Phase C of the EvoX multi-tier router. The authoritative algorithm
// lives in Rust at
//   evox/crates/evox-agent-core/src/model_router.rs
// and ships a generated JSON fixture at
//   evox/crates/evox-agent-core/tests/fixtures/model_router_cases.json
// A vendored copy of that fixture (test/fixtures/model_router_cases.json)
// pins this port byte-for-byte; CI diffs against a regenerated copy so
// silent drift turns red.
//
// Why a fresh module under src/proxy/router/ and not a fold into an
// existing router-ish helper: src/proxy/ has no prior router/classifier
// concept (mailbox/, sync/, task/, extensions/, lifecycle/ all sit at a
// different layer). A first-class subdir is the cheapest place to grow
// the Phase C pieces (cache_passthrough, anthropic egress) without
// muddying the proxy core.

const REASONS = Object.freeze({
  ROUTER_DISABLED: 'router_disabled',
  HARD_PINNED: 'hard_pinned',
  GENE_HINT: 'gene_hint',
  POST_TOOL_RESULT_SYNTHESIS: 'post_tool_result_synthesis',
  USER_REQUESTED_PLANNING: 'user_requested_planning',
  HIGH_TOOL_USE_DENSITY: 'high_tool_use_density',
  TRIVIAL_LOOKUP: 'trivial_lookup',
  DEFAULT_TIER: 'default_tier',
  ESCALATED_FROM_HISTORY: 'escalated_from_history',
});

const TIER_ORDER = Object.freeze({ cheap: 0, mid: 1, expensive: 2 });

function tierStepUp(tier) {
  if (tier === 'cheap') return 'mid';
  if (tier === 'mid') return 'expensive';
  return 'expensive';
}

function classify(features, config) {
  // Parity invariant with model_router.rs:340 — branch order matters.
  // post_tool_result_synthesis must win over high_tool_use_density when
  // both signal: the synthesis turn is just summarising tool output.
  if (
    features.last_user_is_tool_result_only &&
    features.last_assistant_stop_reason === 'ToolUse'
  ) {
    return ['cheap', REASONS.POST_TOOL_RESULT_SYNTHESIS];
  }
  if (features.user_requested_planning) {
    return ['expensive', REASONS.USER_REQUESTED_PLANNING];
  }
  if (features.last_assistant_tool_call_count > 3) {
    return ['expensive', REASONS.HIGH_TOOL_USE_DENSITY];
  }
  if (features.user_simple_lookup) {
    return ['cheap', REASONS.TRIVIAL_LOOKUP];
  }
  return [config.default_tier, REASONS.DEFAULT_TIER];
}

function maybeEscalate(base, history) {
  // Stalled-turn signal from model_router.rs:373: the last decision
  // produced <50 output tokens with no tool call. Bump one tier up,
  // never above expensive, and never weaker than what classify chose.
  if (!history || history.length === 0) return [base, null];
  const last = history[history.length - 1];
  const stalled = last.output_tokens < 50 && !last.had_tool_call;
  if (!stalled) return [base, null];
  if (last.tier === 'expensive') return [base, null];
  const target = tierStepUp(last.tier);
  if (TIER_ORDER[target] > TIER_ORDER[base]) {
    return [target, last.tier];
  }
  return [base, null];
}

function pickForTurn(input) {
  const { features, router_state, config } = input;
  const geneHint = input.gene_hint;

  if (config.disable) {
    return {
      tier: config.default_tier,
      reason: REASONS.ROUTER_DISABLED,
      escalated_from: null,
    };
  }
  if (config.hard_pin_after_plan && router_state && router_state.pinned) {
    return {
      tier: router_state.pinned,
      reason: REASONS.HARD_PINNED,
      escalated_from: null,
    };
  }
  if (geneHint) {
    return {
      tier: geneHint,
      reason: REASONS.GENE_HINT,
      escalated_from: null,
    };
  }
  const [baseTier, baseReason] = classify(features, config);
  const history = router_state ? router_state.history : [];
  const [escalatedTier, escalatedFrom] = maybeEscalate(baseTier, history);
  const reason = escalatedFrom !== null ? REASONS.ESCALATED_FROM_HISTORY : baseReason;
  return {
    tier: escalatedTier,
    reason,
    escalated_from: escalatedFrom,
  };
}

module.exports = { pickForTurn, REASONS };
