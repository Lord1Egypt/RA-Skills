"use strict";

const fs = require("fs");
const paths = require("./paths");
const { ensureDir } = require("./fsutil");

function readReceipts() {
  if (!fs.existsSync(paths.SPEND_LOG_PATH)) return [];
  return fs
    .readFileSync(paths.SPEND_LOG_PATH, "utf8")
    .split("\n")
    .filter(Boolean)
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch (_) {
        return null;
      }
    })
    .filter(Boolean);
}

function appendReceipt(receipt) {
  ensureDir(paths.APP_DIR);
  const entry = { ts: new Date().toISOString(), ...receipt };
  fs.appendFileSync(paths.SPEND_LOG_PATH, JSON.stringify(entry) + "\n", { mode: 0o600 });
  return entry;
}

function spentSinceUsd(isoTs) {
  return readReceipts()
    .filter((r) => typeof r.ts === "string" && r.ts >= isoTs)
    .reduce((sum, r) => sum + (Number(r.amountUsd) || 0), 0);
}

function spentTodayUsd() {
  const today = new Date().toISOString().slice(0, 10);
  return readReceipts()
    .filter((r) => typeof r.ts === "string" && r.ts.startsWith(today))
    .reduce((sum, r) => sum + (Number(r.amountUsd) || 0), 0);
}

// Returns { ok: true } or { ok: false, reason } — must be checked before signing any payment.
function checkCaps(amountUsd, policy) {
  const perCall = parseFloat(policy?.perCallCapUsd || "0");
  const daily = parseFloat(policy?.dailyCapUsd || "0");
  if (perCall > 0 && amountUsd > perCall) {
    return { ok: false, reason: `price $${amountUsd} exceeds perCallCapUsd $${perCall}` };
  }
  const spent = spentTodayUsd();
  if (daily > 0 && spent + amountUsd > daily) {
    return {
      ok: false,
      reason: `price $${amountUsd} + $${spent.toFixed(4)} spent today exceeds dailyCapUsd $${daily}`,
    };
  }
  return { ok: true };
}

module.exports = { readReceipts, appendReceipt, spentTodayUsd, spentSinceUsd, checkCaps };
