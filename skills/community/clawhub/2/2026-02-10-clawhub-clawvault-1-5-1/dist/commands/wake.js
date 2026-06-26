import {
  ClawVault
} from "../chunk-MXNXWOPL.js";
import {
  recover
} from "../chunk-MILVYUPK.js";
import {
  clearDirtyFlag
} from "../chunk-MZZJLQNQ.js";
import "../chunk-7ZRP733D.js";
import "../chunk-VJIFT5T5.js";

// src/commands/wake.ts
import * as path from "path";
var DEFAULT_HANDOFF_LIMIT = 3;
function formatSummaryItems(items, maxItems = 2) {
  const cleaned = items.map((item) => item.trim()).filter(Boolean);
  if (cleaned.length === 0) return "";
  if (cleaned.length <= maxItems) return cleaned.join(", ");
  return `${cleaned.slice(0, maxItems).join(", ")} +${cleaned.length - maxItems} more`;
}
function buildWakeSummary(recovery, recap) {
  if (recovery.checkpoint?.workingOn) {
    return recovery.checkpoint.workingOn;
  }
  const latestHandoff = recap.recentHandoffs[0];
  if (latestHandoff?.workingOn?.length) {
    return formatSummaryItems(latestHandoff.workingOn);
  }
  if (recap.activeProjects.length > 0) {
    return formatSummaryItems(recap.activeProjects);
  }
  return "No recent work summary found.";
}
async function wake(options) {
  const vaultPath = path.resolve(options.vaultPath);
  const recovery = await recover(vaultPath, { clearFlag: true });
  await clearDirtyFlag(vaultPath);
  const vault = new ClawVault(vaultPath);
  await vault.load();
  const recap = await vault.generateRecap({
    handoffLimit: options.handoffLimit ?? DEFAULT_HANDOFF_LIMIT,
    brief: options.brief ?? true
  });
  const summary = buildWakeSummary(recovery, recap);
  const recapMarkdown = vault.formatRecap(recap, { brief: options.brief ?? true });
  return {
    recovery,
    recap,
    recapMarkdown,
    summary
  };
}
export {
  buildWakeSummary,
  wake
};
