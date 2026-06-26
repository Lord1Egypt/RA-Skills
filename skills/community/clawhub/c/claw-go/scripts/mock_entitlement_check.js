#!/usr/bin/env node

/**
 * Mock entitlement checker for local testing.
 * Usage:
 *   node scripts/mock_entitlement_check.js free hd_image
 *   node scripts/mock_entitlement_check.js pro rare_location_arc
 */

const tier = process.argv[2] || "free";
const feature = process.argv[3] || "proactive_update_extra";

const freeFeatures = new Set([
  "daily_report",
  "standard_image",
  "standard_voice"
]);

const proFeatures = new Set([
  ...freeFeatures,
  "proactive_update_extra",
  "hd_image",
  "rare_location_arc",
  "premium_voice_style",
  "deep_memory_itinerary"
]);

const allowed = (tier === "pro" ? proFeatures : freeFeatures).has(feature);

const result = {
  allowed,
  tier,
  feature,
  reason: allowed ? "ok" : "feature_not_in_plan",
  fallback_tier: allowed ? null : "free"
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
