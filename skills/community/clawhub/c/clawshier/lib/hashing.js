const crypto = require("crypto");

function normalizeTotal(total) {
  const parsed = parseFloat(total);
  if (Number.isFinite(parsed)) return parsed.toFixed(2);
  return String(total).trim().toLowerCase();
}

function fingerprint(vendor, date, total) {
  const input = [
    String(vendor).trim().toLowerCase(),
    String(date).trim().toLowerCase(),
    normalizeTotal(total),
  ].join("|");

  return crypto.createHash("sha256").update(input).digest("hex");
}

module.exports = { fingerprint };
