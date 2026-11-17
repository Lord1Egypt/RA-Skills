# Reference — Calendar mutation procedure (multicalendar UI)

> ⚠️ **THIS CHANGES LIVE PRODUCTION INVENTORY.** Every step below alters the real
> Airbnb listing: blocking a date removes a night from sale; opening one exposes
> it; a price change is live to every guest immediately. There is no "preview"
> and no reliable undo beyond the stated inverse operation. **Do NOT run any step
> of this procedure exploratorily, to "see what happens", or on your own
> initiative.** It executes ONLY under the MUTATE-CAL gate in `SKILL.md` →
> "Approved calendar mutations (v0.2)": the operator named the exact date(s)/field
> and end state, gave explicit per-operation approval (APPROVED), one operation
> only, with mandatory fresh-load verification and a reported inverse afterward.
> No approval, or any ambiguity → STOP and escalate; never mutate from an
> uncertain state.

Verified end-to-end 2026-07-04 on the live listing (block + fresh-load verification).
Follow these steps EXACTLY; the multicalendar is a virtualized, animated grid and
improvised clicking fails silently.

All calls: ClawBridge browser role (`/tools/browser/*`), header
`Authorization: Bearer $CLAWBRIDGE_TOKEN`, base `http://host.docker.internal:3201`.

## Context rule — targeted reads, NEVER repeated full snapshots

A full `/browser/snapshot` is tens of thousands of characters. Pulling one
repeatedly floods your context and you WILL lose track of the task mid-procedure
(observed live 2026-07-04: 15+ full snapshots, then a silent stall). Instead:
- To check one cell's state, use a targeted eval that returns just the labels
  (write to file, `-d @file`):
  `{"script":"(() => { const els=[...document.querySelectorAll('*')].filter(e=>e.childElementCount===0&&(e.textContent||'').includes('July 8, 2026')); return els.map(e=>e.textContent); })()"}`
- To search a snapshot, filter it server-side:
  `curl -s -H "Authorization: Bearer $CLAWBRIDGE_TOKEN" http://host.docker.internal:3201/tools/browser/snapshot | grep -i -m5 "blocked\|Save\|Selected dates"`
- Take a FULL snapshot only when you need fresh element refs for an action, and
  at most once per step.

## Completion rule — a MUTATE-CAL turn NEVER ends silently

You must end the turn with a report: before-state, actions taken, verified
after-state, screenshot paths — or an explicit `unconfirmed`/failure report.
NO_REPLY is forbidden in a mutation turn. If you are unsure or stuck, report
exactly where you stopped and what state the calendar was left in.

## Transport rule — exec + curl ONLY, never the fetch/web_fetch tool

ClawBridge calls MUST go through the `exec` tool running `curl`. The built-in
`fetch`/`web_fetch` tool CANNOT reach ClawBridge: it does not send the
`Authorization: Bearer` header and internal hosts (`host.docker.internal`) are
blocked for it (observed live 2026-07-04: `fetch …/tools/browser/snapshot` failed
and killed the run at the verification step, twice in one day). To search a
snapshot for a string, pipe curl instead:
`curl -s -H "Authorization: Bearer $CLAWBRIDGE_TOKEN" http://host.docker.internal:3201/tools/browser/snapshot | grep -i blocked`

## Payload rule — NEVER inline JS into a quoted `-d` argument

The eval scripts below are full of single quotes. Wrapping them in `curl -d '...'`
breaks shell quoting (curl exits 3 "URL malformed" — observed live 2026-07-04, seven
consecutive failures). Instead, for EVERY `/tools/browser/eval` call:

1. Use the `write` tool to save the JSON body to a file, e.g. `/tmp/eval.json`:
   `{"script":"(() => { ... })()"}` — the write tool needs no shell escaping.
2. Then one clean curl per exec:
   `curl -s -X POST -H "Authorization: Bearer $CLAWBRIDGE_TOKEN" -H "Content-Type: application/json" -d @/tmp/eval.json http://host.docker.internal:3201/tools/browser/eval`

Navigate/action/snapshot payloads contain no nested quotes and may stay inline.

## Step 1 — Open the calendar

`POST /tools/browser/navigate` `{"url":"https://www.airbnb.com/multicalendar"}` then
`GET /tools/browser/snapshot`. Find the month selector:
`combobox "Select a month to view" [ref=eNN]`.

## Step 2 — Reach the target month (select + poll, re-fire if stalled)

`POST /tools/browser/action` `{"action":"select","args":["eNN","June 2027"]}`.
The grid *animates* through intervening months and loads lazily. Poll the snapshot
every ~8s for a gridcell whose label contains your target date (e.g. "June 16, 2027").
If the visible month stops advancing for 3+ polls, RE-FIRE the same select — each
firing advances a few months. Do not proceed until the target date's LISTING-ROW
cell is present (label like "<listing name>, June 16, 2027, Select as start date. $NNNN MXN").
That label is your **before-state** — record it.

## Step 3 — Select the date (JS event dispatch, NOT a plain ref click)

Plain `click` on the cell ref reports ✓ but does not register. Use
`POST /tools/browser/eval` with this script (substitute the date):

```
(() => { const leaf=[...document.querySelectorAll('*')].find(e=>e.childElementCount===0&&(e.textContent||'').includes('June 16, 2027, Select as')); if(!leaf) return 'NOT FOUND'; const cell=leaf.closest('button,[role=button],[role=gridcell]'); cell.scrollIntoView({block:'center',inline:'center'}); const r=cell.getBoundingClientRect(); const o={bubbles:true,cancelable:true,clientX:r.x+r.width/2,clientY:r.y+r.height/2,view:window}; for(const t of ['pointerover','mouseover','pointerdown','mousedown','pointerup','mouseup','click']){cell.dispatchEvent(new MouseEvent(t,o));} return 'CLICKED '+leaf.textContent.slice(0,60); })()
```

Run it **twice** (start date, then end date = same cell for a single night). After the
second run the side panel opens: "Selected dates M/D/YYYY → M/D/YYYY".

## Step 4 — Set availability and save

Snapshot → find `radio "Available"` / `radio "Blocked"` and `button "Save"`.
- To block: `{"action":"check","args":["<Blocked-radio-ref>"]}`
- To unblock: `{"action":"check","args":["<Available-radio-ref>"]}`

Re-snapshot: confirm the radio flipped (`checked=true`) AND Save is no longer
`[disabled]`. Then `{"action":"click","args":["<Save-ref>"]}`.

## Step 5 — MANDATORY independent verification (fresh load)

Never trust the in-page state. `POST /tools/browser/navigate` to the multicalendar
again (fresh load), redo Step 2, and read the target cell's label:
- Blocked ⇒ label contains "Unavailable"
- Available ⇒ label shows the nightly price again

Report before-state, actions taken, after-state label, and the screenshot paths
(every action response includes one). If the label is missing or ambiguous, report
`unconfirmed` — do NOT retry the mutation.

## Known traps (all observed live)

- Cell refs go stale between snapshots — re-snapshot before every ref use.
- The month select animates; clicking mid-animation hits "Loading" skeleton cells.
- A ✓ Done response does NOT mean the UI registered the interaction — only the
  side panel opening / radio flipping / fresh-load label proves anything.
- Success claims without the Step-5 fresh-load check are the #1 failure mode.
- Inlining eval JS into `curl -d '...'` mangles shell quoting — always use the
  write-file + `-d @file` pattern (see Payload rule above).
- Using the built-in `fetch`/`web_fetch` tool for ClawBridge endpoints always
  fails (no auth header, internal host blocked) — exec + curl only (see
  Transport rule above).
