#!/usr/bin/env bash
# where-am-i — one call an agent asks constantly: which org, which identities with which accounts,
# what can I spend, and does a shortfall stop me. Prints one JSON object. Needs the CERTEN CLI on
# PATH and a key in ~/.certen/config.json (see SKILL.md, "One-time setup").
set -uo pipefail
command -v certen >/dev/null 2>&1 || { echo '{"error":"certen CLI not on PATH — npm i -g @certen.io/cli"}'; exit 2; }
who=$(certen whoami --json 2>/dev/null || echo '{"ok":false,"error":{"message":"no credential — run: certen signup --with-key agent --org-name <owner>-<handle> --no-keyring"}}')
ids=$(certen identity list --json 2>/dev/null || echo '{"ok":true,"data":[]}')
bal=$(certen balance --json 2>/dev/null || echo '{"ok":false}')
# Accounts live on `identity get`, not on the list; one call per identity, capped so a large org
# does not turn a status check into a rate-limit event.
details="["
for id in $(node -e 'const j=JSON.parse(process.argv[1]); for (const i of (j.data||[]).slice(0,8)) console.log(i.id)' "$ids"); do
  d=$(certen identity get "$id" --json 2>/dev/null || echo '{}')
  details="$details$d,"
done
details="${details%,}]"
node -e '
const [who, ids, bal, details] = process.argv.slice(1).map((s) => { try { return JSON.parse(s); } catch { return {}; } });
const w = who.data ?? {}; const b = bal.data ?? {};
const byId = Object.fromEntries((details || []).map((d) => [d.data?.id ?? d.id, d.data ?? d]));
const identities = (ids.data ?? []).map((i) => {
  const full = byId[i.id] ?? {};
  return { id: i.id, adi: i.adi_url, status: i.status, key_page: full.key_page_url ?? null,
    accounts: Object.fromEntries((full.chain_accounts ?? []).map((a) => [a.chain_id ?? a.chain, a.address])) };
});
console.log(JSON.stringify({
  org: w.organization?.name ?? null,
  org_id: w.organization?.id ?? null,
  key_prefix: w.key_prefix ?? null,
  gateway: w.api_url ?? null,
  standing: w.account_status ?? null,
  identities,
  spendable_usd: b.spendable_usd ?? null,
  enforcing: b.enforcing ?? null,
  meaning: b.enforcing === false ? "metered: shortfalls are recorded, nothing is refused"
         : b.enforcing === true ? "enforced: a run short of funds stops with a 402" : "unknown",
  error: who.ok === false ? (who.error?.message ?? "no credential") : null,
}, null, 2));
' "$who" "$ids" "$bal" "$details"
