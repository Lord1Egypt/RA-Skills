#!/usr/bin/env node
/**
 * validate.mjs — the CEO To-Do reliability guarantee, in code.
 *
 * Zero-dependency Node script. Parses a canonical CEO To-Do doc and asserts
 * every load-bearing invariant. It runs in Claude's code-execution sandbox
 * (the same mechanism the built-in docx/pptx/xlsx skills use to run bundled
 * Python) — NOT on the CEO's machine. The CEO installs the skill, never a
 * runtime.
 *
 * The skill/agent MUST run this before AND after any write:
 *   - before: on the PROPOSED doc. Non-zero exit ⇒ do NOT write, STOP, report.
 *   - after:  on the WRITTEN doc. Non-zero exit ⇒ the write is corrupt, STOP,
 *             restore from the snapshot backup, report.
 *
 * Usage:
 *   node validate.mjs <doc.md>                 # validate one doc
 *   node validate.mjs <doc.md> --prev <snap.md>  # also assert no-loss + stamp-advanced vs a prior snapshot
 *
 * Exit codes:
 *   0  every invariant holds
 *   1  one or more invariants violated (message names the exact violation)
 *   2  usage / file-read error
 *
 * ---------------------------------------------------------------------------
 * Canonical line grammar (fixed slots, machine-checkable). Each item line is:
 *
 *   - [STATUS] [#id] (Pn|parked) [reply-by: YYYY-MM-DD]? [user-added]? · <text> · updated: YYYY-MM-DD
 *
 * where
 *   STATUS   one of OPEN | DONE | STALE | WAITING
 *   #id      a stable 4-hex id, e.g. [#a7f3]
 *   Pn       priority P0 | P1 | P2, or the literal `parked`
 *   reply-by optional, REQUIRED for WAITING items: [reply-by: 2026-07-10]
 *   [user-added]  optional flag; the archive-as-DONE automation must never fire on these
 *   updated  the item's own last-touched date: updated: YYYY-MM-DD
 *
 * Example:
 *   - [OPEN] [#a7f3] P1 · Send the board deck to Dana · updated: 2026-07-01
 *   - [WAITING] [#b2c8] P0 [reply-by: 2026-07-03] · Legal to redline the MSA · updated: 2026-06-28
 *   - [OPEN] [#c4d1] parked [user-added] · Look into the office lease renewal · updated: 2026-07-05
 *
 * The doc also carries a "last updated" stamp line anywhere in the file:
 *   last updated: YYYY-MM-DD
 *
 * Items whose STATUS is DONE live under an `## Archive` heading (append-only).
 * Items the model could not confidently classify live under `## NEEDS-REVIEW`
 * and are exempt from strict grammar (they are captured verbatim, not dropped).
 * ---------------------------------------------------------------------------
 */

import { readFileSync } from 'node:fs';

const STALE_DAYS = 7; // open item with no update for STRICTLY MORE than 7 days ⇒ STALE

// -------------------------- arg parsing -----------------------------------

function parseArgs(argv) {
  const args = { doc: null, prev: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--prev' && argv[i + 1]) {
      args.prev = argv[i + 1];
      i++;
    } else if (!args.doc) {
      args.doc = argv[i];
    }
  }
  return args;
}

// -------------------------- date helpers ----------------------------------

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

function parseDate(s) {
  if (!DATE_RE.test(s)) return null;
  const d = new Date(s + 'T00:00:00Z');
  return Number.isNaN(d.getTime()) ? null : d;
}

function daysBetween(a, b) {
  return Math.floor((b.getTime() - a.getTime()) / 86400000);
}

// today, in UTC, as a YYYY-MM-DD-anchored Date. Overridable via CEO_TODO_TODAY
// so evals can pin "now" deterministically.
function today() {
  const override = process.env.CEO_TODO_TODAY;
  if (override && DATE_RE.test(override)) return parseDate(override);
  const now = new Date();
  return parseDate(now.toISOString().slice(0, 10));
}

// -------------------------- parsing ---------------------------------------

// Match a canonical item line. Sections:
//   status, id, priority, optional reply-by, optional user-added, text, updated
const ITEM_RE = new RegExp(
  '^\\s*(?:[-*+]|\\d+\\.)\\s*' + // list marker: -, *, + or 1.  (all render as a bullet)
    '\\[(OPEN|DONE|STALE|WAITING)\\]\\s+' + // status
    '\\[#([0-9a-fA-F]{4})\\]\\s+' + // id
    '(P0|P1|P2|parked)' + // priority
    '(?:\\s+\\[reply-by:\\s*(\\d{4}-\\d{2}-\\d{2})\\])?' + // optional reply-by
    '(\\s+\\[user-added\\])?' + // optional user-added flag
    '\\s+·\\s+(.+?)\\s+·\\s+' + // text
    'updated:\\s*(\\d{4}-\\d{2}-\\d{2})\\s*$', // updated date
);

// Mask out HTML comments, fenced code blocks, and inline `code` spans so their
// contents — which legitimately contain [STATUS] tokens and grammar examples in
// a real doc — are never mistaken for live item lines. Returns masked lines,
// index-aligned with the original, with masked regions replaced by spaces so
// line numbers and offsets are preserved for accurate error messages.
function maskNonContent(rawLines) {
  const masked = [];
  let inFence = false;
  let inComment = false;
  for (const line of rawLines) {
    const isFenceToggle = /^\s*```/.test(line);
    if (inFence) {
      masked.push(' '.repeat(line.length));
      if (isFenceToggle) inFence = false;
      continue;
    }
    if (isFenceToggle) {
      inFence = true;
      masked.push(' '.repeat(line.length));
      continue;
    }
    let res = '';
    let j = 0;
    while (j < line.length) {
      if (inComment) {
        const end = line.indexOf('-->', j);
        if (end === -1) {
          res += ' '.repeat(line.length - j);
          j = line.length;
        } else {
          res += ' '.repeat(end + 3 - j);
          j = end + 3;
          inComment = false;
        }
        continue;
      }
      if (line.startsWith('<!--', j)) {
        res += '    ';
        j += 4;
        inComment = true;
        continue;
      }
      if (line[j] === '`') {
        const end = line.indexOf('`', j + 1);
        if (end === -1) {
          res += ' ';
          j += 1;
        } else {
          res += ' '.repeat(end + 1 - j);
          j = end + 1;
        }
        continue;
      }
      res += line[j];
      j += 1;
    }
    masked.push(res);
  }
  return masked;
}

const ID_RE = /\[#([0-9a-fA-F]{4})\]/g;
// A line is a COMMITMENT-SHAPED line (and therefore MUST parse as a valid item,
// never be silently skipped) if it either looks like a list item under any
// markdown bullet marker, OR carries a bracketed status token anywhere.
const ITEMISH_RE = /^\s*(?:[-*+]|\d+\.)\s+\[/;
const STATUS_TOKEN_RE = /\[(?:OPEN|DONE|STALE|WAITING)\]/;

function parseDoc(raw) {
  const rawLines = raw.split('\n');
  const lines = maskNonContent(rawLines); // masked, index-aligned with rawLines
  const items = [];
  const errors = [];
  const presentIds = new Set(); // every id present anywhere (incl. NEEDS-REVIEW) — for no-loss
  let stamp = null; // the doc-level "last updated" date
  let section = 'body'; // body | archive | needs-review

  for (let n = 0; n < lines.length; n++) {
    const line = lines[n]; // masked content for detection/matching
    const lineNo = n + 1;
    const trimmed = line.trim();

    // section headers
    const h = trimmed.match(/^##\s+(.+?)\s*$/);
    if (h) {
      const name = h[1].toLowerCase();
      if (name === 'archive') section = 'archive';
      else if (name === 'needs-review') section = 'needs-review';
      else section = 'body';
      continue;
    }

    // doc stamp
    const s = trimmed.match(/^last updated:\s*(\d{4}-\d{2}-\d{2})\s*$/i);
    if (s) {
      stamp = s[1];
      continue;
    }

    // NEEDS-REVIEW is captured verbatim — no grammar enforced (fail-safe park) —
    // but any item IDs it carries still count as PRESENT, so moving a previously
    // classified item into NEEDS-REVIEW is not a false no-loss failure.
    if (section === 'needs-review') {
      for (const m of line.matchAll(ID_RE)) presentIds.add(m[1].toLowerCase());
      continue;
    }

    // A commitment-shaped line MUST parse. This closes the bullet-marker evasion:
    // a real commitment written with *, +, 1. (or any stray status token) can no
    // longer be silently skipped — it either matches the grammar or is flagged
    // malformed. Missing this is a lost/invisible commitment.
    if (ITEMISH_RE.test(line) || STATUS_TOKEN_RE.test(line)) {
      const m = line.match(ITEM_RE);
      if (!m) {
        errors.push(
          `line ${lineNo}: commitment-shaped line does not match the canonical grammar (it must parse, never be skipped): ${rawLines[n].trim()}`,
        );
        continue;
      }
      const [, status, id, priority, replyBy, userAddedFlag, text, updated] = m;
      const idLc = id.toLowerCase();
      presentIds.add(idLc);
      items.push({
        lineNo,
        status,
        id: idLc,
        priority,
        replyBy: replyBy || null,
        userAdded: Boolean(userAddedFlag),
        text: text.trim(),
        updated,
        section,
      });
    }
  }

  return { items, stamp, errors, presentIds };
}

// -------------------------- invariant checks ------------------------------

function checkInvariants(doc, prevDoc) {
  const violations = [...doc.errors];
  const now = today();

  // 1. No duplicate IDs.
  const seen = new Map();
  for (const it of doc.items) {
    if (seen.has(it.id)) {
      violations.push(
        `duplicate id [#${it.id}]: line ${seen.get(it.id)} and line ${it.lineNo}. IDs must be unique.`,
      );
    } else {
      seen.set(it.id, it.lineNo);
    }
  }

  // 2. WAITING items must carry a reply-by date (delegation needs a deadline).
  for (const it of doc.items) {
    if (it.status === 'WAITING' && !it.replyBy) {
      violations.push(`item [#${it.id}] is WAITING but has no [reply-by: YYYY-MM-DD] date (line ${it.lineNo}).`);
    }
  }

  // 3. Every item's updated date must be a real date and not in the future.
  for (const it of doc.items) {
    const d = parseDate(it.updated);
    if (!d) {
      violations.push(`item [#${it.id}] has an invalid updated date "${it.updated}" (line ${it.lineNo}).`);
      continue;
    }
    if (now && daysBetween(d, now) < 0) {
      violations.push(`item [#${it.id}] updated date "${it.updated}" is in the future (line ${it.lineNo}).`);
    }
  }

  // 4. Staleness math. A PRIORITIZED (P0/P1/P2) OPEN item with no update for
  //    STRICTLY MORE than STALE_DAYS days must be tagged STALE, not left OPEN.
  //    `parked` items are the GTD someday/maybe bucket — intentionally not being
  //    actively pushed — so they are exempt from the OPEN→STALE requirement
  //    (flagging a deliberately-parked item as stale is noise, not signal). And
  //    nothing may be tagged STALE while still within the window (a wrong STALE
  //    is a false alarm), regardless of priority.
  if (now) {
    for (const it of doc.items) {
      if (it.section !== 'body') continue; // archived items don't age
      const d = parseDate(it.updated);
      if (!d) continue; // already reported above
      const age = daysBetween(d, now);
      const prioritized = it.priority !== 'parked';
      if (it.status === 'OPEN' && prioritized && age > STALE_DAYS) {
        violations.push(
          `item [#${it.id}] is OPEN but ${age} days stale (> ${STALE_DAYS}); it must be tagged [STALE] (line ${it.lineNo}).`,
        );
      }
      if (it.status === 'STALE' && age <= STALE_DAYS) {
        violations.push(
          `item [#${it.id}] is tagged [STALE] but only ${age} days old (<= ${STALE_DAYS}); staleness fires only after ${STALE_DAYS} days (line ${it.lineNo}).`,
        );
      }
    }
  }

  // 5. No [user-added] item may be auto-closed. A [user-added] item that is now
  //    DONE must have been closed by a human, which shows up as the flag being
  //    dropped on close. So: a [user-added] item that is STILL flagged AND is
  //    DONE is an illegal auto-close.
  for (const it of doc.items) {
    if (it.userAdded && it.status === 'DONE') {
      violations.push(
        `item [#${it.id}] is [user-added] AND [DONE] (line ${it.lineNo}): the archive-as-DONE automation must never fire on a user-added item. Only a human may close it, and closing removes the [user-added] flag.`,
      );
    }
  }

  // 6. Cross-snapshot no-loss + stamp-advanced (only when --prev given).
  if (prevDoc) {
    const nowIds = doc.presentIds; // includes NEEDS-REVIEW ids, so a park is not a false loss
    for (const prev of prevDoc.items) {
      // Every prior OPEN or WAITING item ID must still be present somewhere in
      // the new doc (it may have moved to Archive as DONE, but it must not have
      // vanished). Never lose a live commitment.
      if ((prev.status === 'OPEN' || prev.status === 'WAITING' || prev.status === 'STALE') && !nowIds.has(prev.id)) {
        violations.push(
          `no-loss violation: prior ${prev.status} item [#${prev.id}] ("${prev.text}") is missing from the new doc. Items are append/archive-only and must never disappear.`,
        );
      }
      // A [user-added] item present before must still be present (never dropped).
      if (prev.userAdded && !nowIds.has(prev.id)) {
        violations.push(`no-loss violation: prior [user-added] item [#${prev.id}] is missing from the new doc.`);
      }
    }
    // Stamp must advance (or hold) — never go backwards.
    if (doc.stamp && prevDoc.stamp) {
      const a = parseDate(prevDoc.stamp);
      const b = parseDate(doc.stamp);
      if (a && b && daysBetween(a, b) < 0) {
        violations.push(`stamp regressed: prior "last updated: ${prevDoc.stamp}" is newer than new "last updated: ${doc.stamp}".`);
      }
    }
  }

  // 7. The doc must carry a "last updated" stamp at all.
  if (!doc.stamp) {
    violations.push('missing document "last updated: YYYY-MM-DD" stamp.');
  } else if (!parseDate(doc.stamp)) {
    violations.push(`document "last updated" stamp "${doc.stamp}" is not a valid date.`);
  }

  return violations;
}

// -------------------------- main ------------------------------------------

function main() {
  const { doc: docPath, prev: prevPath } = parseArgs(process.argv.slice(2));
  if (!docPath) {
    console.error('Usage: node validate.mjs <doc.md> [--prev <snapshot.md>]');
    process.exit(2);
  }

  let raw;
  try {
    raw = readFileSync(docPath, 'utf8');
  } catch (e) {
    console.error(`ERROR: cannot read doc "${docPath}": ${e.message}`);
    process.exit(2);
  }

  let prevDoc = null;
  if (prevPath) {
    let prevRaw;
    try {
      prevRaw = readFileSync(prevPath, 'utf8');
    } catch (e) {
      console.error(`ERROR: cannot read prev snapshot "${prevPath}": ${e.message}`);
      process.exit(2);
    }
    prevDoc = parseDoc(prevRaw);
  }

  const doc = parseDoc(raw);
  const violations = checkInvariants(doc, prevDoc);

  if (violations.length > 0) {
    console.error(`VALIDATION FAILED (${violations.length} violation${violations.length === 1 ? '' : 's'}) for ${docPath}:`);
    for (const v of violations) console.error('  ✗ ' + v);
    process.exit(1);
  }

  const bodyCount = doc.items.filter((i) => i.section === 'body').length;
  const archiveCount = doc.items.filter((i) => i.section === 'archive').length;
  console.log(
    `VALIDATION PASSED for ${docPath}: ${doc.items.length} items (${bodyCount} active, ${archiveCount} archived), stamp ${doc.stamp}.`,
  );
  process.exit(0);
}

main();
