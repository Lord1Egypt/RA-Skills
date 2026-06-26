#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cd "$TMP"

node "$ROOT/scripts/ber.js" init >/tmp/ber-init.out
node "$ROOT/scripts/ber.js" capture --type correction --note "Use a durable session manager for long jobs." --scope workspace --expires never --tags remote,ops >/tmp/ber-capture.out
node "$ROOT/scripts/ber.js" list --today >/tmp/ber-list.out
node "$ROOT/scripts/ber.js" propose --today >/tmp/ber-propose.out
node "$ROOT/scripts/ber.js" report --today >/tmp/ber-report.out

test -s .better-every-run/events.jsonl
test -s .better-every-run/lessons.jsonl
grep -q "durable session manager" /tmp/ber-list.out
grep -q "scope=workspace" /tmp/ber-list.out
grep -q "Proposed lessons" /tmp/ber-propose.out
grep -q "Promote:" /tmp/ber-propose.out
grep -q "Better Every Run report" /tmp/ber-report.out
grep -q "Promotion suggestions" /tmp/ber-report.out

LESSON_ID="$(node -e 'const fs=require("fs"); const row=JSON.parse(fs.readFileSync(".better-every-run/lessons.jsonl","utf8").trim().split(/\n+/)[0]); console.log(row.id)')"
node "$ROOT/scripts/ber.js" accept "$LESSON_ID" >/tmp/ber-accept.out
grep -q '"status":"accepted"' .better-every-run/lessons.jsonl
node "$ROOT/scripts/ber.js" export-memory-patch >/tmp/ber-export.out
grep -q "Better Every Run accepted lessons" /tmp/ber-export.out
printf "# Test Memory\n" > memory.md
if node "$ROOT/scripts/ber.js" apply-memory-patch --target memory.md >/tmp/ber-apply.out 2>&1; then
  echo "expected apply-memory-patch to be retired" >&2
  exit 1
fi
grep -q "apply-memory-patch is retired" /tmp/ber-apply.out
if grep -q "durable session manager" memory.md; then
  echo "apply-memory-patch changed memory.md" >&2
  exit 1
fi

printf "# One Step Memory\n" > one-step.md
if node "$ROOT/scripts/ber.js" remember --note "Keep human usage to one command." --scope skill --target one-step.md --tags ux >/tmp/ber-remember-direct.out 2>&1; then
  echo "expected remember --target to fail" >&2
  exit 1
fi
grep -q "remember no longer writes directly" /tmp/ber-remember-direct.out
if grep -q "Keep human usage" one-step.md; then
  echo "remember --target changed one-step.md" >&2
  exit 1
fi

node "$ROOT/scripts/ber.js" remember --note "Keep human usage to one command." --scope skill --tags ux >/tmp/ber-remember.out
grep -q "Durable file changed: none" /tmp/ber-remember.out
PROMOTE_ID="$(node -e 'const fs=require("fs"); const rows=fs.readFileSync(".better-every-run/lessons.jsonl","utf8").trim().split(/\n+/).map(JSON.parse); console.log(rows.find((r)=>r.text.includes("Keep human usage")).id)')"
printf "# Skill Notes\n" > SKILL.md
if node "$ROOT/scripts/ber.js" promote "$PROMOTE_ID" --to skill --target SKILL.md >/tmp/ber-promote-no-card.out 2>&1; then
  echo "expected promotion without card to fail" >&2
  exit 1
fi
grep -q "Promotion requires a lesson card" /tmp/ber-promote-no-card.out
node "$ROOT/scripts/ber.js" card "$PROMOTE_ID" --to skill --target SKILL.md --note "promote into skill behavior" >/tmp/ber-card.out
grep -q "Lesson card written" /tmp/ber-card.out
grep -q "Target SHA-256" /tmp/ber-card.out
grep -q "Verdict: clean" /tmp/ber-card.out
test -s ".better-every-run/cards/$PROMOTE_ID.md"
grep -q "Better Every Run lesson card" ".better-every-run/cards/$PROMOTE_ID.md"
node "$ROOT/scripts/ber.js" promote "$PROMOTE_ID" --to skill --target SKILL.md --note "promote into skill behavior" >/tmp/ber-promote.out
grep -q "Lesson promoted" /tmp/ber-promote.out
grep -q "Skill behavior to preserve" SKILL.md
grep -q '"status":"promoted"' .better-every-run/lessons.jsonl

MEM_ID="$(node "$ROOT/scripts/ber.js" remember --note "Use concise status updates for recurring weekly reports." --scope memory --tags preference | awk '/Lesson:/ {print $3}')"
mkdir -p memory
printf "# Decisions\n" > memory/decisions.md
node "$ROOT/scripts/ber.js" card "$MEM_ID" --to memory --target memory/decisions.md >/tmp/ber-memory-card.out
node "$ROOT/scripts/ber.js" promote "$MEM_ID" --to memory --target memory/decisions.md >/tmp/ber-memory-promote.out
grep -q "Lesson promoted" /tmp/ber-memory-promote.out
grep -q "Use concise status updates" memory/decisions.md
printf "# Bad Memory\n" > decisions.md
if node "$ROOT/scripts/ber.js" card "$MEM_ID" --to memory --target decisions.md >/tmp/ber-bad-memory-target.out 2>&1; then
  echo "expected memory target outside memory/ to fail" >&2
  exit 1
fi
grep -q "memory/\*.md" /tmp/ber-bad-memory-target.out
printf "# Other Skill\n" > OTHER.md
if node "$ROOT/scripts/ber.js" card "$PROMOTE_ID" --to skill --target OTHER.md >/tmp/ber-bad-skill-target.out 2>&1; then
  echo "expected non-SKILL.md skill target to fail" >&2
  exit 1
fi
grep -q "SKILL.md" /tmp/ber-bad-skill-target.out

STALE_ID="$(node "$ROOT/scripts/ber.js" remember --note "Promote stale-card checks into skill coverage." --scope skill --tags regression | awk '/Lesson:/ {print $3}')"
node "$ROOT/scripts/ber.js" card "$STALE_ID" --to skill --target SKILL.md >/tmp/ber-stale-card.out
printf "changed\n" >> SKILL.md
if node "$ROOT/scripts/ber.js" promote "$STALE_ID" --to skill --target SKILL.md >/tmp/ber-stale-promote.out 2>&1; then
  echo "expected stale card promotion to fail" >&2
  exit 1
fi
grep -q "Target changed since lesson card was written" /tmp/ber-stale-promote.out

BAD_NOTE="Store api_""key: REDACTED in durable lessons."
SCAN_ID="$(node "$ROOT/scripts/ber.js" remember --note "$BAD_NOTE" --scope memory --tags scan | awk '/Lesson:/ {print $3}')"
if node "$ROOT/scripts/ber.js" card "$SCAN_ID" --to memory --target memory/decisions.md >/tmp/ber-scan-card.out 2>&1; then
  true
fi
if node "$ROOT/scripts/ber.js" promote "$SCAN_ID" --to memory --target memory/decisions.md >/tmp/ber-scan-promote.out 2>&1; then
  echo "expected scanner to block credential-looking lesson" >&2
  exit 1
fi
grep -q "Promotion blocked by BER scanner" /tmp/ber-scan-promote.out
WARN_ID="$(node "$ROOT/scripts/ber.js" remember --note "Always prefer the deployment checklist." --scope skill --tags scan | awk '/Lesson:/ {print $3}')"
node "$ROOT/scripts/ber.js" card "$WARN_ID" --to skill --target SKILL.md >/tmp/ber-warn-card.out || true
if node "$ROOT/scripts/ber.js" promote "$WARN_ID" --to skill --target SKILL.md >/tmp/ber-warn-promote.out 2>&1; then
  echo "expected scanner warning to block promotion" >&2
  exit 1
fi
grep -q "Promotion needs review" /tmp/ber-warn-promote.out

printf "# Fix Memory\n" > fix.md
if node "$ROOT/scripts/ber.js" fix "agent exposes ledger workflow -> agent gives one human command" --scope skill --target fix.md --tags ux >/tmp/ber-fix-direct.out 2>&1; then
  echo "expected fix --target to fail" >&2
  exit 1
fi
grep -q "fix no longer writes directly" /tmp/ber-fix-direct.out
if grep -q "agent exposes ledger workflow" fix.md; then
  echo "fix --target changed fix.md" >&2
  exit 1
fi
node "$ROOT/scripts/ber.js" fix "agent exposes ledger workflow -> agent gives one human command" --scope skill --tags ux >/tmp/ber-fix.out
grep -q "Durable file changed: none" /tmp/ber-fix.out

printf "# Facade Memory\n" > facade.md
if node "$ROOT/scripts/ber" fix "human sees helper internals -> human sees /ber fix" --target facade.md --tags ux >/tmp/ber-facade-fix.out 2>&1; then
  echo "expected facade fix --target to fail" >&2
  exit 1
fi
grep -q "fix no longer writes directly" /tmp/ber-facade-fix.out
if node "$ROOT/scripts/ber" remember "Human command hides the ledger machinery." --target facade.md --tags ux >/tmp/ber-facade-remember.out 2>&1; then
  echo "expected facade remember --target to fail" >&2
  exit 1
fi
grep -q "remember no longer writes directly" /tmp/ber-facade-remember.out
if grep -q "Human command hides" facade.md; then
  echo "facade remember --target changed facade.md" >&2
  exit 1
fi
node "$ROOT/scripts/ber" fix "human sees helper internals -> human sees /ber fix" --tags ux >/tmp/ber-facade-fix-ok.out
grep -q "Durable file changed: none" /tmp/ber-facade-fix-ok.out
node "$ROOT/scripts/ber" remember "Human command hides the ledger machinery." --tags ux >/tmp/ber-facade-remember-ok.out
grep -q "Durable file changed: none" /tmp/ber-facade-remember-ok.out
node "$ROOT/scripts/ber" report --today >/tmp/ber-facade-report.out
grep -q "Better Every Run report" /tmp/ber-facade-report.out

QUAR_ID="$(node "$ROOT/scripts/ber.js" remember --note "This one-off correction should not become durable policy." --scope project --tags lifecycle | awk '/Lesson:/ {print $3}')"
node "$ROOT/scripts/ber.js" quarantine "$QUAR_ID" --reason "one-off" >/tmp/ber-quarantine.out
grep -q "Lesson quarantined" /tmp/ber-quarantine.out
grep -q '"status":"quarantined"' .better-every-run/lessons.jsonl
OLD_ID="$(node "$ROOT/scripts/ber.js" remember --note "Use the old deployment checklist." --scope skill --tags lifecycle | awk '/Lesson:/ {print $3}')"
NEW_ID="$(node "$ROOT/scripts/ber.js" remember --note "Use the new deployment checklist with verification proof." --scope skill --tags lifecycle | awk '/Lesson:/ {print $3}')"
node "$ROOT/scripts/ber.js" supersede "$OLD_ID" --by "$NEW_ID" --reason "new checklist has proof" >/tmp/ber-supersede.out
grep -q "Lesson superseded" /tmp/ber-supersede.out
grep -q '"status":"superseded"' .better-every-run/lessons.jsonl
node "$ROOT/scripts/ber.js" report --today >/tmp/ber-lifecycle-report.out
grep -q "Quarantined:" /tmp/ber-lifecycle-report.out
grep -q "Superseded:" /tmp/ber-lifecycle-report.out

FIXTURE_ID="$(node "$ROOT/scripts/ber.js" fix "agent claims done without proof -> agent includes verification output" --scope eval --tags regression | awk '/Lesson:/ {print $3}')"
node "$ROOT/scripts/ber.js" eval-fixture "$FIXTURE_ID" --target evals/ber-regressions.json --name "requires verification proof" >/tmp/ber-eval-fixture.out
grep -q "Eval fixture written" /tmp/ber-eval-fixture.out
test -s evals/ber-regressions.json
node -e 'const fs=require("fs"); const rows=JSON.parse(fs.readFileSync("evals/ber-regressions.json","utf8")); if(rows.length!==1) process.exit(1); if(!rows[0].prompt.includes("claims done")) process.exit(1); if(!rows[0].expected.includes("verification output")) process.exit(1);'
grep -q '"evalFixture":"evals/ber-regressions.json"' .better-every-run/lessons.jsonl
if node "$ROOT/scripts/ber.js" eval-fixture "$FIXTURE_ID" --target tmp/ber-regressions.json >/tmp/ber-bad-eval-target.out 2>&1; then
  echo "expected eval target outside tests/evals to fail" >&2
  exit 1
fi
grep -q "Eval fixtures must target" /tmp/ber-bad-eval-target.out

echo "smoke ok"
