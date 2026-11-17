---
name: drivethru-digitize-outsourcing
description: >
  Outsource embroidery digitizing end to end for BaconCo (Odoo). On a routine,
  read the `digitize.demand` records that are Ready to send out, pull the
  decoration's embroidery artwork + specs (production PNG, AI source file,
  height/width, thread-colour names, ship date), download the two files, decide
  rush from the ship date, submit the job to the outside digitizer via the
  `artworklady-digitizing` skill with a brief that states the size and colours,
  and — only on a confirmed submission — transition the demand to Outsource in
  Odoo. Talks to Odoo through the `drivethru_mcp` MCP server (digitize_demand_*
  + decoration_* tools) and hands the actual portal submission to the
  `artworklady-digitizing` skill. Idempotent: it only ever works Ready demands
  and marks them outsourced after a confirmed send, so a retry can't double-post.
  Use whenever the user asks to outsource digitizing, send embroidery jobs to
  the digitizer / Artwork Lady, receive digitized files back, or run the
  digitizing-outsourcing routine. It also runs the RETURN leg: for demands
  already Outsourced, fetch the finished stitch file (DST) from the digitizer by
  job number and upload it to Odoo via `digitize_demand_upload`, advancing the
  demand Outsource → Sew Out, then parse the job's Production Worksheet PDF and
  push its stitch count, sewn size, and Stop-Sequence thread colours onto the
  decoration via `digitize_demand_apply_worksheet`, and file the vendor's
  returned files (worksheet PDF, DST, native design) away on the agent's own
  persistent storage — organized by job, retrievable on request, not in Odoo.
version: 0.5.3
emoji: 🧵
homepage: https://www.odoo.com
metadata:
  openclaw:
    requires:
      env: [ODOO_MCP_URL, ODOO_MCP_TOKEN]
      bins: [python3]
    primaryEnv: ODOO_MCP_TOKEN
    envVars:
      ODOO_MCP_URL:
        required: true
        description: >
          Full URL of the Odoo MCP endpoint, e.g.
          `https://staging.baconco.com/drivethru_mcp/v1` (the MCP server exposed
          by the `drivethru_mcp` Odoo module, not the Odoo base URL). Test
          against STAGING, never production.
      ODOO_MCP_TOKEN:
        required: true
        description: >
          The `drivethru.mcp_key` value from the Odoo `drivethru_mcp` module,
          sent as `Authorization: Bearer`. Treat as a secret; never paste into
          chat.
    install:
      uv:
        - mcp>=1.9.0
        - pymupdf>=1.24        # parse the digitizer's Production Worksheet PDF
---

# Digitize outsourcing (Odoo → outside digitizer)

You run the embroidery **digitizing outsourcing** loop. Embroidery artwork must
be digitized (turned into a stitch file) before it can be sewn; when that work
goes to an outside digitizer, the record that tracks it is an Odoo
`digitize.demand`. Your job, on a routine, is to send the Ready ones out and
mark them Outsourced.

This is the **ERP half** of the loop. The **portal half** — actually posting the
job into the digitizer's web form — is the separate
[`artworklady-digitizing`](../artworklady-digitizing/SKILL.md) skill, which you
invoke. Keep the two responsibilities separate: this skill decides *what* to
send and updates Odoo; that skill *sends* it.

```
SEND leg:
digitize_demand_search (Ready, non-custom)  →  pull decoration art + specs
      →  download the PNG + AI files to disk
      →  build the brief (H × W + thread codes + colours)
      →  artworklady-digitizing submit (dry run, then confirm; standard turnaround)
      →  on status=="submitted":  digitize_demand_outsource   (Ready → Outsource)

RETURN leg:
digitize_demand_search (state=outsource)  →  fetch the vendor's returned files
      →  file them on your machine         (persistent job archive + manifest)
      →  digitize_demand_upload            (Outsource → Sew Out)
      →  parse_worksheet (the PDF)         →  stitch count, size, Stop-Sequence colours
      →  digitize_demand_apply_worksheet   (dims + stitch count + thread colours)
```

## Transport

Odoo is driven through the `drivethru_mcp` MCP server via `scripts/odoo_mcp.py`:

```bash
python3 scripts/odoo_mcp.py tools                        # discover tools + schemas
python3 scripts/odoo_mcp.py call <tool> '{"...":"..."}'  # call a tool
echo '{"...":"..."}' | python3 scripts/odoo_mcp.py call <tool>
```

Every call prints one JSON object, or `{"error": {...}}` with a non-zero exit.
`ODOO_MCP_URL` / `ODOO_MCP_TOKEN` must be set — if not, stop and tell the user.
**Run `tools` first and trust its `inputSchema` over any signature below.**

## The routine, step by step

### 1. Read the Ready queue

```bash
python3 scripts/odoo_mcp.py call digitize_demand_search '{"is_custom": false}'
```

This returns Ready, **non-custom** demands — the queue (custom-text demands use a
different digitizing flow, so exclude them). **Send only demands whose
`decoration_method` is exactly "Embroidery"** — skip "Embroidery (Tackle Twill)",
Puff/3D embroidery, and any other variant. **Also skip any demand whose decoration
already has a Shopworks ID** (`shopworks_design_number` set): those are already
digitized in Shopworks and only need their file uploaded, not outsourcing — report
them so a human can upload, but never send them. Read the roll-up
(`sendable_count`, `blocked_count`, `rush_count`) and each row. **Work at most ~20
per run**, soonest `earliest_ship_date` first; anything beyond that is picked up
next run:

| Field | Use |
|---|---|
| `outsource_ready` / `blockers` | Only send rows where `outsource_ready` is true. Report the blocked ones (with their `blockers`), don't force them. |
| `decoration_method` | Send **only** when it is exactly "Embroidery" — skip Tackle Twill, Puff, and any other variant. |
| `shopworks_design_number` | If set, **skip** — already digitized in Shopworks; it only needs its file uploaded, not outsourcing. Report it for manual upload. |
| `decoration.id` | The job reference you send to the digitizer, and the record whose files you download. |
| `art.embroidery_png`, `art.ai_file` | The two files to download (`cdn_url` / `web_url`, `present`). |
| `art.height_in`, `art.width_in`, `art.color_names` | The brief — size and thread colours. |
| `earliest_ship_date`, `days_until_ship`, `is_rush` | Informational only — surfaced, not acted on (see §3). |

**Skip anything already outsourced.** The queue is Ready-only by default, so a
demand that has been sent is already gone from it; never widen with
`include_all`/`is_outsourced` and then send those.

### 2. Download the two files

For each sendable demand, get the decoration's **embroidery production PNG** and
its **AI source file** with `digitize_demand_files` — one call returns both:

```bash
python3 scripts/odoo_mcp.py call digitize_demand_files '{"demand_id": <DEMAND_ID>}'
```

Each entry comes back with `filename`, `mimetype`, `size_bytes`, `source`, and
`data_base64` (or `error`). **Decode each `data_base64` to a file** (e.g.
`emb_<demand_id>.png`, `emb_<demand_id>.ai`) and confirm it's non-empty.

Do **not** try to fetch the row's `art.*.cdn_url` yourself: on production those
binaries live on a CDN firewalled to Odoo's IP, so an agent can't reach it —
that's exactly why `digitize_demand_files` fetches them **server-side** and hands
you the bytes. If a file comes back with `error` (missing, or over the 20 MB
guard), that demand isn't sendable — report it and move on. See
[`references/routine.md`](references/routine.md) for details.

### 3. Rush is informational — submit everything, standard turnaround

`is_rush` (ship date within the window) and `days_until_ship` are surfaced per
row, but the routine does **not** act on them right now. It submits **every**
`outsource_ready`, non-custom demand, and always at the **standard `nextday`
turnaround** — it does *not* select Artwork Lady's rush option. (The current
backlog trips `is_rush` on old ship dates that aren't true rushes, so a rush
turnaround would be wrong and can cost more.) Report the rush rows for
visibility, but don't treat them differently. Revisit if genuine rush handling
is wanted later.

### 4. Build the brief

The `message` you send the digitizer must clearly state the **height × width and
the thread colours — each with its Odoo colour code**. The code is essential: a
bare name like "White" lets the digitizer substitute a different thread code than
the one the shop picked (and the return leg then records their substitution over
your choice). Build the colour list from **`art.colors`** (each
`{name, color_code, pms_color}`), not `color_names` — format each as
`<color_code> <name>`:

```
Embroidery digitizing. Size: 3.5in W × 2.0in H.
Thread colours — use these exact codes: 1801 White, 1765 Tennessee Orange.
Left chest. Digitize to DST.
```

Build the size from `art.width_in` / `art.height_in`. If a colour has no
`color_code` on the row, use the name alone and flag it (the digitizer will pick
a code, which the return leg then records). Add placement/decoration context if
the row carries it.

### 5. Submit to the digitizer (dry run, then confirm)

Hand the actual submission to the **`artworklady-digitizing`** skill. Its creds
(`ARTWORKLADY_USERNAME`/`PASSWORD`, and, behind the egress proxy, the TLS SPKI
pins) are that skill's concern — if it exits `config_error`, stop and tell the
user to configure them; never ask for them in chat.

**Always dry-run first** (default `confirm:false`) to validate the fill, then
submit with `confirm:true`:

```bash
python3 <artworklady-digitizing>/scripts/artworklady_digitizing.py submit '{
  "job_reference": "<DECO_ID>",
  "turnaround": "nextday",
  "file_types": ["dst"],
  "files": ["/abs/emb_<id>.png", "/abs/emb_<id>.ai"],
  "message": "Embroidery digitizing. Size: 3.5in W × 2.0in H. Thread colours — use these exact codes: 1801 White, 1765 Tennessee Orange. …"
}'
```

* `job_reference` = the **decoration id** (what that skill expects).
* `files` — the PNG first (the mandatory upload slot), the AI second. Both go up.
* `turnaround` — always **`nextday`** for now; do **not** select `rushorder` /
  `sameday` (see §3). Revisit only if genuine rush handling is turned on.
* Success is judged on the real submit response (HTTP 200 → `status:"submitted"`).
  Treat **only** `status:"submitted"` as sent — never a `dry_run`, an `error`, or
  the sight of `/thanks`.

### 6. Mark it Outsourced — exactly once

**Only** on `status:"submitted"`, transition the demand:

```bash
python3 scripts/odoo_mcp.py call digitize_demand_outsource \
  '{"demand_id": <DEMAND_ID>, "note": "Artwork Lady — job_reference <DECO_ID>, submitted <ISO time>"}'
```

This moves the demand `ready → outsource`, stamps `outsource_date`, and flags
`is_outsourced` on the demand and the decoration. Do this **immediately after**
each confirmed submission, one demand at a time.

`digitize_demand_outsource` is **idempotent** (a demand already outsourced comes
back as `already_outsourced`), but the window between a confirmed send and this
call is the one risk: the portal returns no id, so a resend can't be detected.
If this call fails after a confirmed submit, **stop and report it** — do not
re-submit the job.

## Idempotency & exactly-once (read this)

* Work **only** `state=ready` demands. Once sent they're at `outsource` and drop
  out of the default queue, so a re-run never re-sends them.
* Submit **first**, mark outsourced **after** a `submitted` result — and put the
  outsource call right after the submit for each demand, so a crash leaves the
  demand Ready (correct: it was never actually sent) rather than sent-but-unmarked.
* The portal does **not** dedupe and returns no id. The demand's state + the
  chatter `note` (job reference + submitted-at) are your audit trail.

## Return leg: receive the digitized file (Outsource → Sew Out)

When the digitizer finishes, pull the stitch file back and complete the demand.

1. Find the demands waiting on the digitizer:

```bash
python3 scripts/odoo_mcp.py call digitize_demand_search '{"state":["outsource"]}'
```

   Process only demands whose `decoration_method` is exactly "Embroidery" (skip
   Tackle Twill / Puff / other variants). Work at most ~20 per run; the rest come
   next hour.

2. Fetch the vendor's returned files from the portal with the
   `artworklady-digitizing` skill's `fetch` command. It logs into our account,
   finds our order row on `/orders` by job reference (the decoration id), and
   downloads **that row's own download links** — so we get the files the vendor
   actually produced. **Fetch straight into the job's archive folder** so the
   files land where you keep them (see step 3):

```bash
python3 <artworklady-digitizing>/scripts/artworklady_digitizing.py fetch \
  '{"job_reference": "<DECO_ID>", "out_dir": "/home/agent/.openclaw/jobs/<DECO_ID>"}'
```

   * `status:"fetched"` → take the stitch file from the `dst` path in the result,
     and the **worksheet PDF** from the `.pdf` entry in `files` (there's always
     one for the job) — you need it in steps 5–6.
   * `status:"pending"` → the order isn't finished yet; skip and retry next pass.
   * `status:"not_found"` → no order for that job reference; report it.

   **Do not guess the file URL.** The vendor's file store is shared across
   customers, so a job-number collision can rename the file (e.g. `8524_2.DST`);
   scraping our own order row is what guarantees the right file.

3. File the vendor's return package on your own machine. Keep everything the
   order returned (typically the worksheet PDF, the DST, the native `.EMB`
   design, a `.TBF`) in a per-job folder on **persistent** storage, and drop a
   `manifest.json` beside it so the folder is self-describing:

```bash
# the archive folder IS the fetch out_dir above — persistent, survives redeploys
JOB=/home/agent/.openclaw/jobs/<DECO_ID>
cat > "$JOB/manifest.json" <<JSON
{"decoration_id": <DECO_ID>, "job_reference": "<DECO_ID>",
 "customer": "<customer>", "job_name": "<decoration name>",
 "digitize_demand_id": <DEMAND_ID>, "artwork_lady_order_id": "<order # if known>",
 "date_filed_utc": "<UTC now>", "files": [{"filename": "...", "bytes": 0}]}
JSON
```

   * **Persistent, not `/tmp`.** The archive must live on durable storage — for
     this agent that's the mounted volume under `/home/agent/.openclaw/…`;
     anything under `/tmp` is wiped on redeploy. If your persistent workspace is
     elsewhere, use that (and use `.../vendor-files/<DECO_ID>/` if `jobs/` is taken).
   * This is deliberately **not** stored in Odoo — it's the shop's own copy of
     what the vendor sent, like a job folder on an employee's work machine. When
     someone asks for a job's files later, look here by decoration id.
   * Re-filing a job just overwrites its folder, so a re-run is safe.

4. Upload the DST (and the worksheet PDF) back to Odoo, which writes them onto
   the decoration and advances the demand `outsource → sew_out`:

```bash
DST_B64=$(base64 -w0 "$JOB"/*.DST)
PDF_B64=$(base64 -w0 "$JOB"/*.pdf)
python3 scripts/odoo_mcp.py call digitize_demand_upload \
  "{\"demand_id\": <DEMAND_ID>, \"dst_base64\": \"$DST_B64\", \"pdf_base64\": \"$PDF_B64\"}"
```

   (Read them from the archive folder you filed in step 3, and pipe the JSON via
   stdin — the base64 is large.) `digitize_demand_upload` is **idempotent** — a
   demand already at Sew Out/Done comes back as `already_uploaded`, so a re-run
   skips finished work. Leave `stitch_count` to step 6, which is the single
   source of truth for the worksheet numbers.

5. Parse the worksheet PDF. `scripts/parse_worksheet.py` reads the stitch count,
   sewn size, and the Stop-Sequence thread list positionally (see
   [`references/routine.md`](references/routine.md)):

```bash
python3 scripts/parse_worksheet.py "$JOB"/*.pdf --pretty
#   → {"stitch_count":5455,"height_in":2.08,"width_in":4.01,
#      "colors":[{"sequence":1,"code":"1765","name":"Tiger",…},
#                {"sequence":2,"code":"1801","name":"Super White",…}], "warnings":[]}
```

   Read `warnings` — a colour count mismatch or a millimetre size means eyeball
   the PDF before applying. A row with no `code` can't be matched; surface it.

6. Apply the worksheet to the decoration. Pass the parsed values straight
   through — `colors` needs only `code`, `name`, `sequence` per row:

```bash
python3 scripts/odoo_mcp.py call digitize_demand_apply_worksheet '{
  "demand_id": <DEMAND_ID>,
  "stitch_count": 5455, "height_in": 2.08, "width_in": 4.01,
  "colors": [{"sequence":1,"code":"1765","name":"Tiger"},
             {"sequence":2,"code":"1801","name":"Super White"}]
}'
```

   This writes `number_of_stitches`, `size_height`/`size_width`, and rebuilds the
   decoration's thread colours in stitch order — **matching each by its code**. A
   code not on file is **created** (name + code) and a note is posted on the
   demand's batch @mentioning the thread buyer (default *Laura McCarter*) to buy
   the thread or change the colour. The result's `colors.matched` /
   `colors.created` and `note` tell you what happened; **report any created
   colours** so a human follows up. Re-running is safe — a created colour matches
   next time, so the note fires once. Dry-run first with `"dry_run": true` if you
   want to preview the matches and creates without writing.

## A pass, end to end

**Send leg:**

1. `digitize_demand_search '{"is_custom": false}'` → the Ready, non-custom queue.
2. If `sendable_count` is 0, report `blocked_count` + top blockers and stop.
3. Keep only demands whose `decoration_method` is exactly "Embroidery" (skip
   Tackle Twill / Puff / other variants) and with **no** `shopworks_design_number`
   (already digitized in Shopworks — report for manual upload, don't send), then
   take up to ~20 `outsource_ready`, soonest `earliest_ship_date` first.
4. For each, one at a time: download PNG + AI → build the brief →
   `artworklady-digitizing submit` dry run → confirm (standard `nextday`
   turnaround) → on `submitted`, `digitize_demand_outsource`.
5. Report: how many outsourced, which were blocked (and why), and any rush rows
   (informational only — still sent at standard turnaround).

**Return leg:**

6. `digitize_demand_search '{"state":["outsource"]}'` → demands out at the digitizer. Process only Embroidery-method demands (skip Tackle Twill / Puff); cap ~20/run.
7. For each, `artworklady-digitizing fetch` into the job's archive folder
   (`out_dir=/home/agent/.openclaw/jobs/<deco id>`); skip any that come back
   `pending` (not finished yet).
8. File the vendor return package: the fetch already put the files in the archive
   folder — write a `manifest.json` beside them. Persistent storage, not `/tmp`;
   not Odoo.
9. base64 the archived `.DST` (+ the `.pdf` as `pdf_base64`) and
   `digitize_demand_upload` it → the demand moves to Sew Out.
10. `parse_worksheet.py <archived .pdf>` → `digitize_demand_apply_worksheet` with
    the stitch count, size, and Stop-Sequence colours. Report how many were
    received vs still pending, any thread colours that had to be created (batch
    note raised), and where each job was filed.

## Errors

- `config_error` (exit 2) — `ODOO_MCP_URL` / `ODOO_MCP_TOKEN` missing (this skill),
  or `ARTWORKLADY_USERNAME`/`PASSWORD` missing (the digitizing skill).
- `connection_error` — Odoo unreachable or key rejected.
- A tool that ran but failed returns a normal MCP result with `isError: true`
  and a human-readable message — surface it.
- `portal_error` from the digitizing skill — the submit did not return HTTP 200;
  the demand stays Ready and is retried next pass. Do NOT mark it outsourced.

## References

- [`references/routine.md`](references/routine.md) — the download details, the
  turnaround/rush mapping, file naming, and the exactly-once reasoning in full.
