# Digitize outsourcing — routine details

The full detail behind the six steps in `SKILL.md`. Read this when the happy
path isn't enough.

## The `digitize.demand` workflow

```
not_ready → ready → outsource → sew_out → done
```

* **not_ready ⇄ ready** flips automatically in Odoo from the decoration's
  readiness (production PNG, thread colours, non-zero size) plus a linked sale
  order. You never write these — you read `state=ready`.
* **ready → outsource** is the only transition you make, via
  `digitize_demand_outsource`. Once a demand is at `outsource` (or beyond) Odoo
  freezes the readiness recheck, so it can't be dragged back to Ready.
* **sew_out / done** happen when the digitized file comes back and is uploaded
  in Odoo — not your concern.

So the queue you work is exactly `state=ready`, and marking a demand
`outsource` is what removes it from that queue.

## Reading a row

`digitize_demand_search` enriches every row from the linked decoration. The
fields that matter to the routine:

- `id` — the **digitize.demand** id (what you pass to `digitize_demand_outsource`).
- `decoration.id` — the **decoration** id (the `job_reference`, and the
  `record_id` you download files from).
- `outsource_ready` (bool) + `blockers` (list) — send only when true; otherwise
  report the blockers. Common blocker: `no AI source file on the decoration`
  (the AI is not part of Odoo's Ready predicate but the digitizer needs it, so a
  demand can be Ready yet not sendable).
- `decoration_method` (`{id, name}`) — **process only when it is exactly
  "Embroidery"**; skip Tackle Twill, Puff, and any other variant (they aren't
  outsourced to Artwork Lady). Applies to both legs.
- `shopworks_design_number` — when set, the decoration is **already digitized in
  Shopworks** and only needs its file uploaded. **Skip it on the send leg** (never
  outsource it); report it so a human can upload.
- `art.embroidery_png` / `art.ai_file` — each `{present, cdn_url, web_url}`.
- `art.height_in`, `art.width_in`, `art.color_names` (list of thread-colour
  names) — the brief.
- `earliest_ship_date`, `days_until_ship`, `is_rush`, `rush_threshold_days`.

## Downloading the PNG + AI

Use `digitize_demand_files` — one call returns both files, already fetched:

```bash
python3 scripts/odoo_mcp.py call digitize_demand_files '{"demand_id": <DEMAND_ID>}'
```

It returns a `files` list; by default the embroidery PNG + AI (pass `fields` to
choose from `embroidery_production_png`, `decoration_ai_file`,
`embroidery_production_dst`, `decoration_pdf_file`). Each entry is either
`{field, filename, mimetype, size_bytes, source, data_base64}` or
`{field, error}`.

- **Decode `data_base64` to disk** for each file. `source` is `binary` (stored
  inline) or `cdn` (fetched from the CDN server-side).
- **Why not fetch the CDN yourself:** on production these binaries are offloaded
  to `api.baconco.com`, which is firewalled to Odoo's IP — an agent elsewhere
  gets a connection timeout. `digitize_demand_files` runs inside Odoo, so it can
  reach the CDN and hands you the bytes. Don't try the row's `art.*.cdn_url`
  directly; it will time out.
- **An `error` entry** (missing file, or over the 20 MB guard) → that demand
  isn't sendable. Report and skip; don't submit a half job.

Suggested local names, so a crash leaves obvious artefacts:
`emb_<demand_id>.png`, `emb_<demand_id>.ai`. Use absolute paths in the submit
call. Verify each file is non-empty before submitting.

## Rush is informational (current policy)

A row is rush when `is_rush` is true — the ship date is within
`rush_threshold_days` (5 by default; Odoo env `DRIVETHRU_DIGITIZE_RUSH_DAYS`).
It is **surfaced but not acted on**: the routine submits every `outsource_ready`,
non-custom demand regardless of `is_rush`, and always at the standard `nextday`
turnaround (below). The current backlog trips `is_rush` on old ship dates that
aren't true rushes, so neither a hold nor a rush turnaround is warranted. Report
the rush rows for visibility; revisit if genuine rush handling is wanted later.

## Turnaround

The digitizer's `turnaround` is `sameday | nextday | rushorder`. **For now,
always send `nextday`** — the standard turnaround — and do not select `rushorder`
or `sameday`. The backlog trips `is_rush` on stale ship dates that aren't true
rushes, so a rush turnaround would be wrong (and can cost more). If genuine rush
handling is turned on later, map an approved rush to `rushorder` (and an
immediate ship date to `sameday`); until then, `nextday` for everything.

## The brief (`message`)

State the size and colours plainly — **each colour with its Odoo code** (from
`art.colors[].color_code`), so the digitizer uses the exact thread and can't
substitute a different code than the shop picked:

```
Embroidery digitizing. Size: <width>in W × <height>in H.
Thread colours — use these exact codes: <code> <name>, <code> <name>, …
Digitize to DST.
```

Format each colour as `<color_code> <name>` (e.g. `1801 White`), pulling from
`art.colors` (not `art.color_names`). A colour with no `color_code` falls back to
the name alone — flag it, since the digitizer will then choose a code that the
return leg records. Add placement/garment context from the row when present.
`file_types` defaults to `["dst"]` (the stitch file we want back).

## Exactly-once

The portal returns HTTP 200 with an **empty body** — no id — so nothing can
correlate a resubmission. The discipline that makes this safe:

1. Work only `state=ready`. A sent demand is at `outsource` and gone from the queue.
2. Per demand: submit (`confirm:true`) → on `status:"submitted"` immediately call
   `digitize_demand_outsource`. Don't batch the sends and mark them all at the end.
3. If `digitize_demand_outsource` fails right after a confirmed submit, **stop and
   report** — the job was sent; a human must reconcile it. Do not resend.
4. A crash *before* the submit returns leaves the demand Ready — correct, since it
   was never sent — and it's retried next pass.

`digitize_demand_outsource` is idempotent (already-sent → `already_outsourced`),
and its `note` records the job reference + submitted-at in the demand's chatter
for the audit trail.

## Worked example (one demand)

```bash
# 1. queue
python3 scripts/odoo_mcp.py call digitize_demand_search '{}'
#   → row: id=812, decoration.id=4590, outsource_ready=true, is_rush=false,
#          art.width_in=3.5, art.height_in=2.0,
#          art.colors=[{name:White,color_code:1801},{name:Tennessee Orange,color_code:1765}]

# 2. files (both in one call, fetched server-side)
python3 scripts/odoo_mcp.py call digitize_demand_files '{"demand_id":812}'
#   → files:[{field:embroidery_production_png, data_base64:…}, {field:decoration_ai_file, data_base64:…}]
#   → decode each data_base64 → write emb_812.png, emb_812.ai

# 3. submit at standard nextday turnaround (is_rush not acted on). 4. brief from the art fields.

# 5. dry run, then confirm (artworklady-digitizing skill)
python3 <artworklady-digitizing>/scripts/artworklady_digitizing.py submit '{
  "job_reference":"4590","turnaround":"nextday","file_types":["dst"],
  "files":["/abs/emb_812.png","/abs/emb_812.ai"],
  "message":"Embroidery digitizing. Size: 3.5in W × 2.0in H. Thread colours — use these exact codes: 1801 White, 1765 Tennessee Orange. Digitize to DST."}'   # confirm:false → dry_run
#   …then the same with "confirm":true → status:"submitted"

# 6. mark outsourced (only on submitted)
python3 scripts/odoo_mcp.py call digitize_demand_outsource \
  '{"demand_id":812,"note":"Artwork Lady — job_reference 4590, submitted 2026-09-18T14:03Z"}'
```

## Return leg — receiving the digitized file

When the digitizer finishes, complete the demand (`outsource → sew_out`).

- **Find the work:** `digitize_demand_search {"state":["outsource"]}`. Process only
  demands whose `decoration_method` is exactly "Embroidery" (skip Tackle Twill /
  Puff / other variants); work at most ~20 per run.
- **Get the files:** use the `artworklady-digitizing` skill's `fetch` command with
  `{"job_reference":"<deco_id>", "out_dir":"/home/agent/.openclaw/jobs/<deco_id>"}`.
  It logs in, finds our order row on `/orders` by job reference, and downloads
  that row's **own** download links — returning the saved files and the `dst`
  path. Fetch straight into the job's archive folder (next bullet).
  `status:"pending"` means it isn't finished yet (skip and retry);
  `status:"not_found"` means no such order. **Don't guess the file URL:** the
  vendor's store is shared across customers, so a job-number collision can rename
  the file (`8524_2.DST`); the order row links the right one.
- **File the package:** keep what the vendor returned on the agent's own
  persistent storage, with a `manifest.json` (below). Not Odoo.
- **Upload it:** base64 the archived DST and call `digitize_demand_upload
  {"demand_id":…, "dst_base64":…, "pdf_base64":…}`. Odoo writes them to the
  decoration's `embroidery_production_dst` / `decoration_pdf_file` and advances
  the demand to Sew Out. Leave `stitch_count` off here — the worksheet apply
  (below) owns it.
- **Apply the worksheet:** parse the job's Production Worksheet PDF and push its
  numbers onto the decoration (below).

## Filing the vendor's files (the job archive)

The vendor's returned files are the shop's own paperwork — kept on the agent's
machine like job folders on an employee's workstation, retrievable on request,
and deliberately **not** stored in Odoo.

- **Where:** one folder per job on **persistent** storage. For this agent that's
  the mounted volume: `/home/agent/.openclaw/jobs/<decoration_id>/`. Anything
  under `/tmp` is wiped on redeploy, so never archive there — fetch's `out_dir`
  points straight at the job folder so the files land where they're kept. (If a
  different agent's persistent workspace is elsewhere, use that; if `jobs/` is
  taken under `.openclaw`, use `vendor-files/<decoration_id>/`.)
- **What:** the whole vendor **return package** — typically the worksheet PDF,
  the DST stitch file, the native `.EMB` design (the editable source — worth
  keeping), and a `.TBF`. Keep everything the order returned; you don't archive
  the PNG/AI we sent out (those are the shop's, already in Odoo).
- **Manifest:** drop a `manifest.json` in each folder so it's self-describing:
  ```json
  {"decoration_id": 8524, "job_reference": "8524",
   "customer": "UT Center for Global Engagement",
   "job_name": "UT Global Engage International House",
   "digitize_demand_id": 1982, "artwork_lady_order_id": "68217",
   "date_filed_utc": "2026-09-22T17:55:44Z",
   "files": [{"filename": "8524.pdf", "bytes": 367769}, {"filename": "8524.DST", "bytes": 16878}]}
  ```
- **Footprint:** a package is well under 1 MB, so the 5 GB volume holds thousands
  of jobs — no pruning needed for a long time. Re-filing a job overwrites its
  folder, so a re-run is safe.
- **Retrieval:** when someone asks for a job's files, look under the archive by
  decoration id and hand them over.

## Worksheet → decoration (the digitizer's PDF)

Every finished job has a **Production Worksheet PDF** (Wilcom
EmbroideryStudio). It carries the truth about the stitched design — the stitch
count, the sewn size, and the thread colours in stitch order — so after the DST
is uploaded, parse it and write it onto the decoration.

### Parsing — `scripts/parse_worksheet.py`

```bash
python3 scripts/parse_worksheet.py /home/agent/.openclaw/jobs/8524/8524.pdf --pretty
```

Returns:

```json
{ "stitch_count": 5455, "height_in": 2.08, "width_in": 4.01,
  "colors_declared": 2,
  "colors": [
    {"sequence": 1, "n_number": 1, "code": "1765", "name": "Tiger",
     "chart": "Madeira PolyNeon 40", "stitches": 816},
    {"sequence": 2, "n_number": 2, "code": "1801", "name": "Super White",
     "chart": "Madeira PolyNeon 40", "stitches": 4637} ],
  "raw": {"stitches": "5,455", "height": "2.08 in", …}, "warnings": [] }
```

- The **labelled scalars** (`Stitches:`, `Height:`, `Width:`, `Colors:`) are read
  from each label word's own line — the value words to its right — not from
  `get_text()` order, which linearises the two-column layout misleadingly.
- The **Stop Sequence** table is parsed by column *geometry*: each data word is
  assigned to the header column it physically overlaps (nearest-centre when it
  overlaps none). That's what makes the right-aligned stitch column and the empty
  colour-swatch column land in the right fields. It needs `pymupdf` (declared in
  the skill's `install.uv`), which is self-contained — unlike pdfplumber/pypdf,
  whose cffi/cryptography deps are flaky in the agent container.
- `sequence` is the running stitch order (1..N) — exactly the order the colours
  are sewn, which is what the decoration's thread-colour lines want.
- Always read `warnings`: a `colors_declared` ≠ parsed-rows mismatch, a
  millimetre size, or a row missing a `code` means look at the PDF before
  applying. `raw` shows what each label literally said, for auditing a bad parse.

### Applying — `digitize_demand_apply_worksheet`

```bash
python3 scripts/odoo_mcp.py call digitize_demand_apply_worksheet '{
  "demand_id": 1982,
  "stitch_count": 5455, "height_in": 2.08, "width_in": 4.01,
  "colors": [{"sequence":1,"code":"1765","name":"Tiger"},
             {"sequence":2,"code":"1801","name":"Super White"}]}'
```

- Writes `number_of_stitches`, `size_height`, `size_width` on the decoration
  (only the fields you pass), and rebuilds `embroidery_thread_color_lines` in
  `sequence` order.
- **Thread colours are matched by `code`** against `embroidery_thread_color`
  (exact on the code). A code not on file is **created** (worksheet `name` +
  `code`) and, so someone buys the thread or fixes the decoration's colour, a
  note is posted on the demand's **batch** @mentioning the thread buyer — default
  *Laura McCarter*, env `DRIVETHRU_DIGITIZE_THREAD_BUYER`, or `notify_partner_name`
  to override. No batch on the demand → the note lands on the demand's own chatter.
- **Gated to a sent demand** (`outsource`/`sew_out`/`done`). Past Ready the
  readiness recheck is frozen, so rewriting the colour lines can't bounce the
  state — this is why you apply the worksheet *after* `digitize_demand_upload`,
  not before. Custom-text demands are refused.
- **Exactly-once note:** re-running matches the colour created last time, so the
  “new thread colour” note fires only on the pass that actually created it.
  `dry_run:true` previews `colors.matched` / `colors.created` and the note target
  without writing anything.
- The result's `colors.created` is the follow-up list — **surface it** to the
  human; `colors.matched` is what resolved cleanly; `note` says where it posted
  and to whom (`partner_resolved:false` means the buyer name didn't resolve, so
  the note went out un-tagged — flag that).

### Exactly-once (return leg)

`digitize_demand_upload` is idempotent: a demand already at Sew Out/Done returns
`already_uploaded` and nothing is re-written. So the safe order is fetch → file →
upload → apply-worksheet per demand; a crash before the upload just leaves the
demand at Outsource and it is retried next pass. Custom-text demands are refused
(they use the per-value digitizing flow), and a demand not yet at Outsource is
refused. `digitize_demand_apply_worksheet` is safe to re-run after the upload (it
rewrites the same numbers/colours and only notes a *newly* created colour), so
re-running a partially-completed demand converges.

```bash
# receive one finished demand (demand 812 / decoration 4590)
JOB=/home/agent/.openclaw/jobs/4590          # persistent volume, NOT /tmp
python3 <artworklady-digitizing>/scripts/artworklady_digitizing.py fetch \
  "{\"job_reference\":\"4590\",\"out_dir\":\"$JOB\"}"
#   → status:"fetched", dst:"$JOB/4590.DST", files:[…, {ext:"pdf", path:"$JOB/4590.pdf"}, {ext:"emb",…}]

# file the vendor package: fetch already dropped the files in $JOB — add a manifest
cat > "$JOB/manifest.json" <<JSON
{"decoration_id":4590,"job_reference":"4590","customer":"…","job_name":"…",
 "digitize_demand_id":812,"artwork_lady_order_id":"…","date_filed_utc":"$(date -u +%FT%TZ)",
 "files":[{"filename":"4590.DST","bytes":0},{"filename":"4590.pdf","bytes":0}]}
JSON

DST_B64=$(base64 -w0 "$JOB"/*.DST)
PDF_B64=$(base64 -w0 "$JOB"/*.pdf)
python3 scripts/odoo_mcp.py call digitize_demand_upload \
  "{\"demand_id\":812,\"dst_base64\":\"$DST_B64\",\"pdf_base64\":\"$PDF_B64\"}"
#   → state: "sew_out", uploaded: true

# then push the worksheet numbers onto the decoration
python3 scripts/parse_worksheet.py "$JOB"/*.pdf --pretty
#   → {stitch_count:5455, height_in:2.08, width_in:4.01, colors:[{sequence,code,name,…}], warnings:[]}
# read that output, then call apply_worksheet with the same numbers + colours
# (colors needs only sequence/code/name per row):
python3 scripts/odoo_mcp.py call digitize_demand_apply_worksheet '{
  "demand_id":812, "stitch_count":5455, "height_in":2.08, "width_in":4.01,
  "colors":[{"sequence":1,"code":"1765","name":"Tiger"},
            {"sequence":2,"code":"1801","name":"Super White"}]}'
#   → applied:{number_of_stitches,size_height,size_width}, colors:{matched:[…],created:[…]}, note:{…}
```
