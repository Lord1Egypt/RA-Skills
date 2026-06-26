"use strict";

function normalizeCoverageStatus(value) {
  const raw = String(value || "").trim().toLowerCase();
  if (!raw) return "";
  if (
    ["not_started", "not-started", "todo", "pending", "unmapped", "unassigned", "planned_ready", "phase_1_baseline_captured", "phase_1_placeholder", "present_in_analysis_json"].includes(raw)
    || /^pending_phase_\d+_mapping$/.test(raw)
    || /^planned_phase_\d+$/.test(raw)
    || /^phase_?\d+_planned_ready$/.test(raw)
    || /^phase_\d+_placeholder$/.test(raw)
    || /^phase_\d+_baseline_captured$/.test(raw)
  ) {
    return "planned";
  }
  if (
    [
      "inventory",
      "inventied",
      "inventoried",
      "catalogued",
      "cataloged",
      "baseline_inventory",
      "inventory_only",
      "inventory_ready",
      "source_inventory",
      "inventory_complete",
      "source_inventory_complete",
      "inventory_complete_pending_slides",
      "inventory_ready_pending_slide_mapping",
      "inventory_ready_pending_slides",
      "inventory_ready_pending_mapping",
    ].includes(raw)
    || /^phase_?\d+_inventory$/.test(raw)
    || /^phase_?\d+_inventoried$/.test(raw)
    || /^phase_?\d+_inventied$/.test(raw)
    || /^phase_?\d+_inventory_complete$/.test(raw)
    || /^inventory_complete_pending_(?:slides|mapping|placement)$/.test(raw)
    || /^inventory_ready_pending_(?:slides|mapping|slide_mapping|placement)$/.test(raw)
  ) {
    return "analysis_only";
  }
  if (
    ["mapped", "mapping_complete", "mapping-complete", "fully_mapped", "fully-mapped", "structured_ready"].includes(raw)
    || /^phase_?\d+_structured_ready$/.test(raw)
  ) {
    return "covered";
  }
  return raw;
}

module.exports = {
  normalizeCoverageStatus,
};
