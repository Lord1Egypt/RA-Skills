# Web-image routine — per-color storefront mockups (blank + decorations)

This is what the **Mockup Artist Agent** runs for the routine **"General Purpose
Web image generation routine."** When a storefront site is built, products are
created in bulk from blanks + decorations and arrive with **no image**. This
routine gives every colour of every such product a mockup: the product's
decoration(s) composited onto that colour's blank photo, written to the colour's
`product.product` records (every size) and, if missing, the template.

**The whole routine is one script: `scripts/web_mockup_job.py`.** It plans,
fetches, preps art, composites, checks, gets an independent vision verdict, and
uploads — and it prints only JSON. Your job is to run it, read its JSON, act on
`needs_adjustment` verdicts with one command, and report.

## Hard rules — read these first

These exist because each one was broken in a past run.

1. **Never let image bytes into your context.** Do not `Read`/open/view any
   image file. Do not call `decoration_get_image`, `decoration_list_attachments`
   with `include_data`, or `product_read`/`ops_search` with `include_binary`.
   Do not `cat`/`base64` an image. The vision review runs *inside* the script
   and hands you a yes/no verdict. (A few images in context balloons the session.)
2. **Never write an image yourself.** No `product_write`/`product_create` with an
   image field (the server refuses it anyway), no `decoration_set_image`, **no
   chunking bytes into a field** — it never works. The script uploads
   byte-exact through `POST <ODOO_MCP_URL>/upload` and verifies the write.
3. **Never decide whether a blank "has an image" by fetching it.** Odoo serves a
   *placeholder* for an empty image field. `web_mockup_plan` checks the actual
   field server-side; an empty blank is a `skip_reason`, not a picture.
4. **Left/right are the WEARER'S.** "Left chest" is over the wearer's left pec,
   which in a flat front photo is on the **image's RIGHT** half. You never have
   to work this out: `scripts/locations.py` maps each raw location name to a
   `placement` (wearer frame) *and* `image_side` (image frame) — "Left Leg" is
   the front of the wearer's left leg, image right — the rules are
   orientation-guarded, the script
   checks the side geometrically, and the reviewer is told both frames. If you
   ever pass a manual `--offset-x-pct`, **positive moves toward the image's
   right**.
5. **Never composite a background.** Art is taken best-first: embroidery PNG /
   DTF production PNG before the decoration thumbnail. Every source is checked
   for a plate — including production PNGs that have transparent padding around
   a solid swatch (an embroidery preview on fabric colour): a one-colour plate is
   keyed out (`art_sources`… `plate_keyed`), and if the art's edge is still a
   solid block that source is rejected and the next is tried. Don't work around a `background_not_removed` / `art_unusable`
   failure; report it.
6. **Only a "yes" is written.** Up to 3 attempts per colour. After that it is
   `rejected` and left for a human. Never force it.
7. **Unattended.** No questions to a human mid-run. Skip with a reason instead.

## Setup (once per environment)

The script reads `ODOO_MCP_URL` (`…/drivethru_mcp/v1`) and `ODOO_MCP_TOKEN` —
the same Odoo credentials the MCP uses, **pointing at the environment you are
writing to** — plus a vision key: `MOCKUP_VISION_API_KEY` (or
`OPENROUTER_API_KEY`), optional `MOCKUP_VISION_MODEL` (default
`anthropic/claude-sonnet-5`) and `MOCKUP_VISION_BASE_URL` (default OpenRouter).
If a required var is missing, the script exits with a clear error — report it;
do not try another path.

## Each fire

### 1. Pick scope

```jsonc
storefront_list_sites { "state": "draft" }     // stores being built
```

Work one site at a time, newest first. (Optionally peek with
`web_mockup_plan { "site_id": <id>, "limit": 10 }` — it is metadata only and
shows `colors_needing_image`. `0` → nothing to do for that site.)

### 2. Run — in the background, and report progress while it goes

A run takes about a minute per colour, so a store can take 15–30 minutes. If
you run it as one blocking command, you (and whoever is watching the task) see
nothing until it ends. So **start it in the background and poll it**:

```bash
nohup python3 scripts/web_mockup_job.py run --site-id <id> --limit 10 \
    > /dev/null 2>&1 &
# or specific products:  … run --product-tmpl-ids 24921,24920 …
```

Then, **about once a minute**, until the run is finished:

```bash
python3 scripts/web_mockup_job.py status --brief
```

```json
{"active_run": {"pid": 4121, "done": 5, "total": 16, "alive": true,
                "latest": "21:24:10 [5/16]  24941-black  needs_adjustment  too_high(+6y)  a1  $0.013"},
 "last_run_finished": "2026-09-22 21:10:02",
 "recent": ["…", "…", "…"]}
```

- **Each poll, post a progress update quoting `active_run.latest`** and
  `done/total` (e.g. `5/16 — 24941-black needs_adjustment too_high(+6y)`), with
  progress ≈ `done/total`. Don't repeat identical updates; post when it changes.
- **Finished** = `active_run` is `null` and `last_run_finished` is newer than when
  you started. Then read the result: `python3 scripts/web_mockup_job.py status --last-run`
  (the same JSON a foreground run prints).
- **`alive: false`** while `active_run` is still present = the process died
  without finishing. Report the `recent` lines; don't restart it more than once.
- Don't poll faster than every ~45 s, and don't open or read the progress log or
  any image yourself — `status` is the only thing you need.

`adjust` commands (step 3) take a minute or two each; run those in the
foreground and post a progress update after each.

**Missing blank photos are filled first, automatically.** Before planning, `run`
calls `web_mockup_refresh_blanks`: every blank colour with no photo (or only an
on-model one) whose blank comes from an **integrated vendor** gets its
`vendor_image_url` set from that vendor — SanMar's SDL flat front, S&S's
`colorFrontImage` — so it gets a mockup in the same run. Only that URL is
written, never downgraded. The result is under `blank_refresh` in the summary
(`updated`, `kept_existing`, `vendor_has_no_image`, `colour_not_on_blank`,
`not_integrated`, `vendor_error`); report its counts. Non-integrated blanks
(house brands, other vendors) stay `not_integrated` → the colour is still skipped
`blank_color_has_no_image` for a human. A `--dry-run` only reports what it would
fill. `--no-refresh-blanks` turns it off.

`--include-imaged` also redoes colours (and the template) that already carry an
image — use it **only when told to**, e.g. when the store-build wizard copied the
blank's photo onto the end items. Without it, existing images are never touched.

Output (abridged):

```json
{"counts": {"image_written": 5, "needs_adjustment": 1, "failed": 1},
 "skipped": {"blank_color_has_no_image": 2, "already_imaged": 7, "unmapped_location": 1},
 "not_imaged": [{"product_tmpl_id": 25016, "name": "…", "reason": "unmapped_location",
   "decorations": [{"decoration_id": 143, "location_name": "Left Hip", "reason": "unmapped_location"}]}],
 "remaining_unscanned": 0,
 "jobs": [
  {"job": "24921-black", "status": "image_written", "art_sources": {"8934": "dtf_png"}},
  {"job": "24921-orange", "status": "needs_adjustment", "attempts": 1,
   "issues": [{"decoration_id": 8934, "code": "too_high", "detail": "…"}],
   "suggested": {"8934": {"offset_y_pct": 5}},
   "next": "python3 scripts/web_mockup_job.py adjust --job 24921-orange --apply-suggested"},
  {"job": "24920-navy", "status": "failed", "error": {"code": "art_unusable", "detail": "…"}}
 ]}
```

Each progress line is one finished colour:
`[i/N] <job> <status> <reason or size> a<attempt> $<vision cost>`.
The final JSON also carries:

- `cost` — vision spend for this invocation: `vision_usd`, `vision_calls`,
  `per_written_colour_usd` (OpenRouter's exact per-call cost). Your own model's
  spend is not included — it's on the OpenRouter dashboard.
- `tuning` — per (category, placement): how many approved mockups needed a
  nudge, the deltas they needed, and — when ≥ 2 agree — a suggested
  `edit_placement_rule.py update …` command. **Report it; never run it** — a
  default change affects every future mockup and is a human decision.

### 3. Act on each `needs_adjustment`

Run the job's `next` command — that's the "easy fix" path:

```bash
python3 scripts/web_mockup_job.py adjust --job 24921-orange --apply-suggested
```

It layers the reviewer's deltas onto the previous attempt (halving any that flip
sign — overshoot guard), re-composes, re-reviews, and writes on "yes". Repeat
while it returns `needs_adjustment`; the script stops at 3 attempts
(`rejected`). If `next` says the issue is not fixable by moving
(`background_visible`, `bad_blank`, `art_damaged`), leave it.

Before the vision check, a geometry check also rejects a chest print whose
centre is outside its zone (left chest 60–72% of the garment width, right chest
28–40%) with `outside_chest_zone` and a fix back toward the middle of the zone.

Manual nudge (only if you have a specific reason beyond the suggestion):

```bash
python3 scripts/web_mockup_job.py adjust --job <job> --decoration-id <id> \
    --offset-y-pct 4 --offset-x-pct -3 --width-delta-pct 10
# offset-x: + = toward the IMAGE's right. offset-y: + = down. width: + = bigger.
```

`review_error` (the vision call failed) → `adjust --job <job>` with no deltas
re-reviews once. Still failing → report it.

**A person sent a written image back** (a `get_feedback` redo, or a review
verdict with a correction): turn their words into deltas and rewrite it —

```bash
python3 scripts/web_mockup_job.py adjust --job <job> --redo --offset-x-pct -3   # "move it toward the zipper"
```

`--redo` needs at least one of `--offset-x-pct` / `--offset-y-pct` /
`--width-delta-pct` (image coordinates: + x = image right, + y = down,
+ width = bigger). The person is the reviewer, so there is no vision call and
no adjustment cap; the geometry checks still apply. It rewrites every size of
the colour (and the template image if this colour supplied it). Then
`submit_for_review` again with `revision_of` set to the review id.

### 4. Report

One outcome per job plus a run summary. Use the script's statuses verbatim:

| Status / skip | Meaning |
|---|---|
| `image_written` | Reviewed "yes", uploaded to every size variant (and the template if it had no image), verified byte-exact. |
| `needs_adjustment` | Reviewer said no with a fix — run `next`. |
| `rejected` | 3 attempts, still no — left for a human. Include the last issues. Also `error.code: adjustment_limit` when the reviewer's fixes would move a print further from its measured rule than allowed (±4 across, ±5 down, ±15% size, in total) — the rule and the reviewer disagree, so a human decides. Never work around it with manual deltas. |
| `failed` | `error.code` says why (`art_unusable`, `background_not_removed`, `blank_looks_like_placeholder`, `source_empty`, `upload_truncated`, …). A Python error code (`TypeError`, `KeyError`, …) is a bug in the script — report `error.where` verbatim. |
| `review_error` | Vision call failed — re-review once, then report. |
| `blank_rejected` | The reviewer rejected the **blank photo itself** (`bad_blank`: an "image not available" graphic stored on the variant, an on-model shot, a different product). No nudge fixes that, so it is never `needs_adjustment`. The run automatically asks the vendor for that exact colour (`blank_refetch` in the result) and re-images it on the new photo; `blank_rejected` in the final result means the vendor had nothing better — a human must add a flat front photo. |
| skipped `already_imaged` | Colour already has its own image. Never overwritten. |
| skipped `blank_color_has_no_image` / `no_blank_for_color` / `blank_needs_flatfront` | The blank has no usable photo for that colour, and the automatic vendor refresh couldn't supply one (see `blank_refresh`: not integrated, or the vendor has no image) — a human needs to add it. |
| skipped `back_only_no_back_blank` | Only back prints; blanks carry front photos only. |
| skipped `unmapped_location` / `no_art` / `no_usable_decoration` | Nothing on the product can go on the front photo: a location name `locations.py` doesn't recognise, or no art. The product and each decoration's `location_name` + reason are listed in `not_imaged` — report them. A new location name is a skill change (`scripts/locations.py`), not an Odoo change. |

Summary line: `site=<id> written=<w> adjusted=<a> rejected=<r> failed=<f> skipped=<s> remaining=<remaining_unscanned> vision=$<cost.vision_usd>`.
Then list any `tuning` rows with `needed_adjustment > 0` (and their `suggest`).
Nothing to do is a `nothing_to_do` verdict — the steady state.

### 5. Escalate what needs a person — do not just report it

The result (and `status`) carries **`needs_human`**: every job that ended
`rejected`, `blank_rejected`, `failed`, `review_error` or `unreviewed`, any
`needs_adjustment` with no automatic fix, and every product in `not_imaged`,
each with `why` and the `action` a person has to take. After step 3's
follow-ups, re-read `python3 scripts/web_mockup_job.py status` and, if
`needs_human` is non-empty, **call `escalate_to_human` once for the run**
(kind `blocker`) before you finish:

- `title`: `Store <site_id> mockups: <n> need a person`
- `context`: one lead sentence, then a table — product, colour, status, why,
  action — one row per `needs_human` item.
- one question: "What should I do with these?" — options
  `Retry after I fix them (Recommended)` (you then run
  `run --product-tmpl-ids <ids> --retry-stuck` for those products) and
  `Leave them parked`.

Then end your turn; the answer wakes you. A run whose only open items are
people's work is **not** complete until it is escalated — a line in the
summary is not an escalation. Never escalate mid-run, and never for items
the script is still handling (`needs_adjustment` with a `next` command).

`python3 scripts/web_mockup_job.py status` shows everything waiting on you,
all-time vision spend (`cost_all_time`), the cumulative `tuning` table, and the
last 20 progress lines (`--tail N`).

Jobs that ended `rejected`, or `failed` on bad source data (`art_unusable`,
`background_not_removed`, `blank_looks_like_placeholder`, `source_empty`, …), are
**parked**: later fires report them but don't re-run them. Once a human fixes
the art or blank, `run … --retry-stuck` restarts them.

## What the pipeline does (for debugging, not for you to redo by hand)

- **Plan** (`web_mockup_plan`, server-side): per colour the size variants to
  write, whether they already carry their *own* image (`vendor_image_url` →
  `image_url` → `image_variant_1920`; never `image_1920`, which falls back to the
  template), and the matching blank photo — matched by colour **name**, on-model
  vendor shots rejected. Per decoration: the raw `location_name`, method, size
  and art sources best-first. Odoo makes no placement decision.
- **Placement** (`scripts/locations.py`, in the skill): location name →
  `placement` / `view` / `image_side`; front decorations become layers, back
  prints and unrecognised names are omitted (the blank photo is a front), and a
  product with no front layer lands in `not_imaged` with the reason.
- **Fetch**: everything with a `fetch` ref goes through `GET <ODOO_MCP_URL>/image`,
  which 404s on an empty field instead of returning a placeholder — including
  the embroidery/DTF production PNGs, which Odoo pulls from the CDN (the agent
  host cannot reach the CDN; a direct download times out and the run falls back
  to the thumbnail). Vendor blank URLs are fetched directly. Blanks are also
  rejected locally if tiny or near-uniform.
- **Art prep**: transparent production PNG → trimmed and used; opaque art →
  plate colour-keyed (or segmented with rembg), then verified: a surviving
  opaque border = rejected, next source.
- **Compose**: all front layers onto one garment bbox via `compose_mockup.compose`
  with the orientation-guarded rules; category inferred from the blank name.
- **Checks**: geometry (image side, inside garment) → vision review
  (`vision_review.py`, JSON only). Geometry failures never spend a vision call.
- **Write**: 1200 px JPEG → `POST <ODOO_MCP_URL>/upload` with
  `record_ids=<all sizes of the colour>`; `bytes_received` must equal the file
  size and every record must report `bytes_stored`.

State lives in `$MOCKUP_DATA_DIR/web_jobs/` (per-job folder + `state.json`).

## The routine prompt (paste into the Mockup Artist Agent's Routines page)

- **Name:** `General Purpose Web image generation routine`
- **Schedule:** hourly during business hours (or as configured)
- **Prompt:**

  ```
  Image new storefront products. Follow references/web_image_routine.md in the
  drivethru-graphic-artist skill exactly — especially its Hard rules.

  1. storefront_list_sites state=draft. For each site (newest first), start
     the run IN THE BACKGROUND (see "2. Run" in the doc):
       nohup python3 scripts/web_mockup_job.py run --site-id <id> --limit 10 > /dev/null 2>&1 &
     then poll `python3 scripts/web_mockup_job.py status --brief` about once a
     minute, posting a progress update with active_run.done/total and
     active_run.latest each time it changes. When finished, read
     `status --last-run`. Stop starting new sites once 30 colour jobs have run
     this fire.
  2. For every job with status needs_adjustment, run its "next" command
     (adjust --job <job> --apply-suggested) until it is image_written or
     rejected. For review_error, re-run `adjust --job <job>` once.
  3. Report one line per job (status + reason), the summary line with the
     vision cost, and any tuning rows that needed adjustment.
  4. Re-read `status`. If `needs_human` is non-empty, call escalate_to_human
     once (kind blocker) with a table of those items (product, colour,
     status, why, action) — see "5. Escalate" in the doc. Do not finish the
     run with them only in the summary.

  Never open, Read, or view an image. Never call decoration_get_image,
  decoration_set_image, or product_write/product_create with an image field,
  and never pass include_binary. Never write image bytes yourself or in chunks —
  the script does the upload. Never ask a human mid-run — escalate once, at
  the end (step 4).
  ```
