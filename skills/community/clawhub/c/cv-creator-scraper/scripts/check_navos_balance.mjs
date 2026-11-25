#!/usr/bin/env node
// Check Navos credit balance for the current desktop user.
// Usage: node check_navos_balance.mjs [--uid <uid>]

import { checkNavosBalance } from './_navos_balance.mjs';
import { loadNavosIdentity } from './_navos_identity.mjs';

async function main() {
  const args = process.argv.slice(2);
  const uidIdx = args.indexOf('--uid');
  const uid = uidIdx !== -1 ? args[uidIdx + 1] : null;

  // If no uid flag, try to load from Navos identity (may throw if not logged in).
  const effectiveUid = uid || (() => {
    try { return loadNavosIdentity().uid; } catch { return null; }
  })();

  if (!effectiveUid) {
    console.error(JSON.stringify({
      error: 'uid not provided and Navos identity not found',
      hint: 'Pass --uid <uid> or ensure ~/.navos/identity/navos-userinfo.json exists',
    }));
    process.exit(1);
  }

  try {
    const balance = await checkNavosBalance({ uid: effectiveUid });
    console.log(JSON.stringify({
      uid: effectiveUid,
      total_balance: balance.total_balance,
      available_balance: balance.available_balance,
    }, null, 2));
  } catch (err) {
    console.error(JSON.stringify({
      error: err.message,
      ...(err.ret !== undefined && { ret: err.ret }),
      hint: 'Set NAVOS_BASE_URL to switch between staging/production.',
    }));
    process.exit(1);
  }
}

main();
