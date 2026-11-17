// crypto-alerts trigger gate: fire only when `check` prints alerts.
// Runs every schedule tick BEFORE the agent turn (no model call when silent).
const res = await exec({ command: "python3 __WORKSPACE__/skills/crypto-alerts-kalkulasi/scripts/alert_cli.py check" });
const out = String((res && res.aggregated) ?? "").trim();
if (out.indexOf("CRYPTO ALERTS") !== -1) {
  return { fire: true, message: "---\n" + out, state: { t: Date.now(), fired: true } };
}
return { fire: false, state: { t: Date.now() } };
