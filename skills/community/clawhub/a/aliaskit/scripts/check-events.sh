#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ID_FILE="$SKILL_DIR/identity.json"

# No identity yet, exit silently
[ -f "$ID_FILE" ] || exit 0

node -e "
const { AliasKit } = require('aliaskit');
const id = JSON.parse(require('fs').readFileSync('$ID_FILE', 'utf8'));
if (id.apiKey) process.env.ALIASKIT_API_KEY = id.apiKey;

(async () => {
  try {
    const ak = new AliasKit();
    const [emails, sms] = await Promise.all([
      ak.emails.list(id.identityId, { unread: true, limit: 5 }),
      ak.sms.list(id.identityId, { unread: true, limit: 5 }).catch(() => ({ data: [] })),
    ]);

    const ue = emails.data || [];
    const us = sms.data || [];

    if (ue.length === 0 && us.length === 0) process.exit(0);

    console.log('--- AliasKit: New messages ---');
    if (ue.length > 0) {
      console.log('Unread emails (' + ue.length + '):');
      ue.forEach(e => console.log('  From: ' + (e.from || '?') + ' | Subject: ' + (e.subject || '(none)')));
    }
    if (us.length > 0) {
      console.log('Unread SMS (' + us.length + '):');
      us.forEach(s => console.log('  From: ' + (s.from || '?') + ' | ' + (s.body || '').slice(0, 80)));
    }
    console.log('---');
  } catch { process.exit(0); }
})();
" 2>/dev/null || true
