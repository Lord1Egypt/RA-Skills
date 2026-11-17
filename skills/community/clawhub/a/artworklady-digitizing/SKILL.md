---
name: artworklady-digitizing
description: >
  Artwork Lady embroidery-digitizing intake adapter — post a digitizing job
  into the Art work Lady portal (https://www.artworklady.com), which has no
  API. A Playwright driver logs in, opens the "Embroidery Digitizing" tab on
  the /placeorder form, fills the fields (job reference, turnaround, file
  type, color scheme, message), attaches 1–3 files, and — only when told to —
  clicks Send and confirms the job posted by watching the real
  order_form_submit response. Use when a decoration needs to be sent out for
  digitizing: "send this decoration to Artwork Lady", "post the digitizing
  job", "submit to the digitizer". It is a THIN PORTAL ADAPTER and touches no
  ERP: give it a job reference, the field values, and local file paths, and it
  returns a structured result. Pair it with a routine that polls Odoo
  `digitize.demand` (or `decoration`), downloads the attachments to disk,
  calls this skill, and updates the record on success. Submitting is gated
  behind `confirm: true`; the default is a dry run that fills and validates
  the form but posts nothing. A `fetch` command also downloads the FINISHED files
  back from `/orders` by job reference (the return leg), returning the DST path —
  by scraping our own order row so a job-number collision can't fetch the wrong file.
version: 0.2.0
emoji: 🧵
homepage: https://www.artworklady.com
metadata:
  openclaw:
    requires:
      bins: [python3]
    primaryEnv: ARTWORKLADY_USERNAME
    envVars:
      ARTWORKLADY_USERNAME:
        required: false
        description: >
          Artwork Lady portal login (the agent's bound account). Optional at
          boot — may instead be passed inline as `username` in the tool JSON —
          but one of the two is required at call time or the tool exits
          `config_error`. Treat as a secret; never ask for it in chat.
      ARTWORKLADY_PASSWORD:
        required: false
        description: Portal password. Treat as a secret; never paste into chat.
      ARTWORKLADY_LOGIN_TYPE:
        required: false
        description: >
          `employee` (default) or `company` — the login popup's toggle. The
          confirmed account logs in as `employee`; only change this if the
          bound account is a company-level login.
      ARTWORKLADY_BASE_URL:
        required: false
        description: Portal base URL. Defaults to `https://www.artworklady.com`.
      ARTWORKLADY_HEADLESS:
        required: false
        description: Default `true`. Set falsy to run the browser headed.
      ARTWORKLADY_TIMEOUT_MS:
        required: false
        description: >
          Per-step wait, default 30000. Every wait targets a concrete element
          or the form's own hidden state — nothing waits on `networkidle`
          (the home page is a hydrating marketing page that may never reach it).
      ARTWORKLADY_STATE_PATH:
        required: false
        description: >
          File path for a persisted logged-in session (Playwright
          storage_state). Set it to skip the login round trip on later runs; a
          stale session falls back to a fresh login automatically.
      ARTWORKLADY_ARTIFACT_DIR:
        required: false
        description: >
          Where screenshots (and, on failure, the page HTML) are written.
          Defaults to the current working directory.
      ARTWORKLADY_PROXY:
        required: false
        description: >
          Explicit browser proxy (`server` passed to Playwright). Falls back
          to HTTPS_PROXY when unset. Only needed behind an egress proxy.
      ARTWORKLADY_TLS_SPKI_PINS:
        required: false
        description: >
          Comma-separated base64 SPKI pins passed to Chromium's
          --ignore-certificate-errors-spki-list. Needed ONLY behind a
          TLS-terminating egress proxy whose CA the browser does not otherwise
          trust; it whitelists exactly those keys rather than disabling
          verification. Leave unset on a normal network.
    install:
      uv:
        # Browser automation for the intake form. Installs the Playwright
        # package; the Chromium binary is a separate `python -m playwright
        # install chromium` (or a preinstalled build via PLAYWRIGHT_BROWSERS_PATH).
        - playwright>=1.40
---

# Artwork Lady — Embroidery Digitizing intake

Art work Lady digitizes embroidery artwork, and the only way in is a web
**intake form** on `https://www.artworklady.com/placeorder` — there is no API.
This skill drives that form with Playwright. It is the *portal adapter* half of
the digitizing loop; the ERP half (poll `digitize.demand`, download the files,
update the record) lives in the routine that calls it.

The single helper is `scripts/artworklady_digitizing.py`:

```bash
# Read-only diagnostic: log in, open the Embroidery tab, dump the live field
# map + a screenshot. Nothing is submitted. Run this first if the form changed.
python3 scripts/artworklady_digitizing.py capture '{}'

# Fill the form — DRY RUN by default (fills + validates, does NOT click Send).
python3 scripts/artworklady_digitizing.py submit '{
  "job_reference": "12345",
  "turnaround": "sameday",
  "file_types": ["dst"],
  "color_scheme": "CMYK",
  "files": ["/path/artwork.png", "/path/spec.pdf"],
  "message": "Left chest, 3.5in wide. Threads: white + navy. Digitize to DST."
}'

# Actually post the job — clicks Send and confirms via the submit response.
python3 scripts/artworklady_digitizing.py submit '{ … , "confirm": true }'

# Fetch the FINISHED files for a completed job (the return leg). Logs in,
# opens /orders, finds our row by job reference, and downloads that row's own
# download links — so the file is whatever the vendor named it, never a guess.
python3 scripts/artworklady_digitizing.py fetch '{"job_reference": "8524", "out_dir": "/tmp/dl"}'
```

Each command prints one JSON object, or `{"error": {...}}` with a non-zero
exit. Credentials come from `ARTWORKLADY_USERNAME` / `ARTWORKLADY_PASSWORD`
(or inline `username`/`password`); if missing it exits `config_error` — stop
and tell the user to configure them, never ask for them in chat.

## `submit` input

| Key | Required | Default | Notes |
|---|---|---|---|
| `job_reference` | ✅ | — | The intake "Job reference". Set it to the `digitize.demand` / decoration id. |
| `files` | ✅ | — | 1–3 local paths. **The first fills the mandatory "Upload File Here"**; the rest are optional. |
| `turnaround` | ✅ | — | `sameday` \| `nextday` \| `rushorder`. Required — the caller supplies it per demand (no baked-in default). |
| `file_types` | | `["dst"]` | Any of `dst` \| `emb` \| `exp` \| `other` (≥1). For `other`, also pass `other_text`. |
| `color_scheme` | | `CMYK` | `CMYK` \| `RGB`. (Present on the form though embroidery is thread-based.) |
| `message` | | `""` | Free text — the digitizing brief (dimensions, placement, thread colors, garment…). |
| `proof_template` | | `false` | Ticks "Required proof template". |
| `other_text` | | — | Required when `file_types` includes `other`. |
| `admin_note` | | — | Optional hidden note posted with the job. |
| `confirm` | | `false` | **`false` = dry run** (fill + validate, no Send). `true` = post the job. |
| `login_type` | | env/`employee` | `employee` \| `company`. |
| `headless`, `base_url`, `state_path`, `timeout_ms`, `artifact_dir` | | env | Overrides for the env vars above. |

The value mapping (which turnaround, which file type, what the message says,
which two Odoo attachments to send) is the **routine's** decision — this skill
just takes the values. The defaults above are placeholders to confirm.

## `fetch` input / output — the return leg

`fetch` downloads a **completed** order's files from `/orders` by job reference,
using that order row's **own** download links (never a guessed URL).

| Key | Required | Default | Notes |
|---|---|---|---|
| `job_reference` | ✅ | — | The job reference to find (the decoration id). |
| `order_id` | | — | Disambiguates when a job reference repeats across your orders (the Artwork Lady Order Id). |
| `out_dir` | | cwd / artifact_dir | Where the files are written. |
| `exts` | | all | Restrict to these extensions, e.g. `["dst","pdf"]`. |
| `require_completed` | | `true` | Only pull a row marked Completed. |

```json
{ "status": "fetched", "job_reference": "8524", "order_id": "68217",
  "files": [ {"name":"8524.DST","path":"…","size":16878,"ext":"dst","url":"…"}, … ],
  "dst": "/abs/path/8524.DST" }
{ "status": "pending",   "job_reference": "8524", "message": "…not ready yet" }
{ "status": "not_found", "job_reference": "8524" }
```

Take the finished stitch file from `dst`. **Why scrape rather than guess the
URL:** the vendor's file store is shared across customers, so a job-number
collision can make it rename the file (e.g. `8524_2.DST`). The `/orders` row
always links to the right file for **your** order, whatever it is named.

## What "success" means — read before wiring the status update

The Send button (`input[name=submit]`, `onclick="uploadfile()"`) is **not** a
native form submit. `uploadfile()` validates, then POSTs a `multipart/form-data`
XHR to `https://www.artworklady.com/placeorder/order_form_submit`, and on the
XHR's `load` event it writes the response into `#status` and **redirects to
`/placeorder/thanks`** — *without checking the HTTP status*. So the redirect
alone is **not** proof of success.

This skill therefore judges success on the **actual `order_form_submit`
response**: it waits for that POST, and treats the job as posted only on
**HTTP 200**, returning `status: "submitted"` with the response body and the
`/thanks` URL. A non-200 raises `portal_error`. The routine must update
`digitize.demand` **only** on `status: "submitted"` — never on a `dry_run`, an
`error`, or the mere sight of `/thanks`.

A live run confirmed the endpoint returns **HTTP 200 with an empty body** — no
confirmation/ticket id comes back (and `/thanks` is static), so there is nothing
to correlate a submission to. **De-duplication is the caller's job:** stamp the
demand with its `job_reference` + a submitted-at time on `submitted`, and skip
demands that already carry one, so a routine retry after a crash can't double-post.

Result shapes:

```json
{ "status": "dry_run",   "filled": { … }, "screenshot": "…", "trace": [ … ] }
{ "status": "submitted", "filled": { … }, "response": {"status":200,"body":"…"}, "thanks_url": "…/placeorder/thanks" }
{ "error": { "type": "config_error|portal_error|unexpected", "message": "…" } }
```

## Where this fits

```
routine: poll Odoo digitize.demand  →  download attachments to disk
      →  THIS SKILL: submit {job_reference, values, files, confirm:true}
      →  on status=="submitted": update the digitize.demand record in Odoo
```

Keep the exactly-once discipline the same way the payables skills do: submit
first, update Odoo **after** a `submitted` result. If the routine crashes
between the two, the demand is still "to digitize" and will be retried — so
decide up front how to avoid a double-post (e.g. store the returned
confirmation / a submitted-at stamp on the demand, and skip demands that
already carry one). The portal itself does **not** dedupe.

## Notes / gotchas (see references for the full map)

- **Employee vs Company login.** The popup opens on Register; the driver clicks
  "Sign in" (`switchForm('login')`) and logs in as `employee` (the confirmed
  default). `company` is the other toggle.
- **One shared form, three tabs.** All three tabs are the same `#contactform`;
  `change_form('embroidery')` just unhides the digitizing section and sets the
  hidden `#form_type=1`. The driver asserts that before filling.
- **Color scheme id is swapped between tabs.** `change_form` moves the id
  `colorScheme` between the CMYK/RGB select and the printing-method select, so
  the driver targets the CMYK/RGB one by its stable **class** `select.color_scheme`,
  never the id.
- **`fileType` values repeat across the hidden tabs**, but `dst/emb/exp/other`
  are unique to the embroidery section and the only visible ones after the tab
  switch.
- **`file1` is mandatory**; a turnaround radio must be checked (the page throws
  otherwise). The driver mirrors these preconditions in `validate_ready()` and
  refuses to Send until they hold.

## Build status

Confirmed live **end to end**, including a real Send: `capture`, `submit` (dry
run), and one `confirm: true` submission have all run against the live portal
from this environment — login (employee) → `/placeorder` → Embroidery tab →
every field filled and validated → Send → `order_form_submit` **HTTP 200** →
`/placeorder/thanks`, in ~11s headless. The one real submission used a throwaway
`job_reference` ("AUTOMATION-TEST-PLEASE-IGNORE") and a "please ignore" message,
and should be deleted from the Artwork Lady account. Untested: login from a
long-lived datacenter IP, and whether the vendor ever adds a bot/MFA check.

## References

- [`references/placeorder_flow_notes.md`](references/placeorder_flow_notes.md) —
  the reverse-engineered flow: every selector, the `uploadfile()` submit
  mechanism, the success signal, and the gotchas. Start here if the form changes.
