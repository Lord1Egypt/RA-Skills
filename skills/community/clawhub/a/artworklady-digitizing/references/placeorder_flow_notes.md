# Artwork Lady `/placeorder` — Embroidery Digitizing intake flow

The reverse-engineered flow behind `scripts/artworklady_digitizing.py`, captured
from the live portal. Art work Lady is a **Wix-hosted** marketing site with a
custom PHP app under `/placeorder`; the intake form is plain HTML + jQuery, so
selectors are authored ids/names and are stable.

**Status: confirmed live, end to end** — login (employee) → `/placeorder` →
Embroidery tab → all fields filled + validated → **real Send** → `order_form_submit`
returned **HTTP 200** → redirect to `/placeorder/thanks`, ~11s, headless. (The
one exercised submission used a throwaway reference and a "please ignore" message.)

## Waiting — never on `networkidle`

The home page (`https://www.artworklady.com/`) is a hydrating Wix marketing page
that holds connections open; `networkidle` may never arrive. Every wait targets a
concrete element or the form's own hidden state (`#form_type === '1'`), and each
step is recorded with elapsed ms in the `trace` the tool returns.

## The flow

```
https://www.artworklady.com/            ← home (Wix marketing page)
  → click  button.ip2026-get-started    ("Register / Login") → opens the popup
  → click  span[onclick="switchForm('login')"]   ("Sign in")  → login form (no URL change)
  → (optional) click #popup-company-login-btn     to switch employee→company
  → fill #popupLoginForm email/password, submit
  → redirect to  /placeorder            ← the order form (login success signal)
  → click  button[onclick="change_form('embroidery')"]   → Embroidery tab (no URL change)
  → fill #contactform, attach files
  → click  input[name="submit"]  (Send) → XHR POST /placeorder/order_form_submit → /placeorder/thanks
```

## Step 1 — Login popup

The public nav has **no** Login link; the entry is a button.

| Element | Selector |
|---|---|
| Open popup | `button.ip2026-get-started` (`onclick="openAuth('register')"`) — popup opens on the **Register** form |
| Switch to sign-in | `span[onclick="switchForm('login')"]` ("Sign in" at the popup foot). Fallback: `page.evaluate("switchForm('login')")` |
| Employee toggle (default) | `#popup-employee-login-btn` (`data-login-type="employee"`, class `active_login`) |
| Company toggle | `#popup-company-login-btn` (`data-login-type="company"`) |
| Hidden login type (posted) | `#popup_login_type` (name `login_type`, default `employee`) |
| Email | `#popupLoginForm input[name="email"]` |
| Password | `#popupLoginForm input[name="password"]` |
| Submit | `#popupLoginForm button[type="submit"]` ("Sign In") |
| Error message | `#popupLoginMessage` |

The login form posts to `https://www.artworklady.com/unifiedlogin/doLogin`. On
success the app **redirects to `/placeorder`** — that URL (plus the presence of
`#contactform`) is the definitive "we are in" signal, not a load state. The
confirmed account logs in as **employee** (the default).

## Step 2 — The Embroidery Digitizing tab

`/placeorder` renders **one** form, `#contactform` (name `orderForm`,
`enctype=multipart/form-data`), containing all three tabs' fields. The tab
buttons just show/hide sections and set a hidden type:

| Tab | Button | `#form_type` |
|---|---|---|
| Artwork | `button[onclick="change_form('artwork')"]` | 0 |
| **Embroidery Digitizing** | `button[onclick="change_form('embroidery')"]` | **1** |
| Product Visual | `button[onclick="change_form('visual')"]` | 2 |

> The three tab **buttons** share the class `digitize_btn` (a copy-paste bug — the
> Product Visual button also carries it), so match on the `onclick`, not the class.
> The driver clicks the embroidery button and then asserts `#form_type === '1'`
> and `#file1` visible before filling.

## Step 3 — Embroidery form fields

All under `#contactform`, all visible only after the Embroidery tab is active.

| Field | Selector | Values / notes |
|---|---|---|
| Job reference | `#jobref` (name `jobref`) | text; placeholder "Enter Job Referer". **Required** (JS). |
| Required Turnaround | `input[name="radio"][value="…"]` | `sameday` (default checked) \| `nextday` \| `rushorder`. `id="radio"` is duplicated on all three — **target by value**. A radio must be checked or `uploadfile()` throws. |
| Required File Type | `input[name="fileType"][value="…"]` | `dst` \| `emb` \| `exp` \| `other`. ≥1 required (JS). `other` → `#otherCheckbox`, and reveals `#otherTextbox` with a free-text `#otherText`. |
| Color Scheme | `#contactform select.color_scheme` | options `CMYK` \| `RGB`. **Target by class**, not `#colorScheme` — see the id-swap gotcha below. |
| Upload File Here | `#file1` (name `file1`) | **Mandatory** (JS: "image is required"). |
| Upload File | `#file2` (name `file2`) | optional |
| Upload File | `#file3` (name `file3`) | optional |
| Required proof template | `#proof_template` (value `1`) | checkbox |
| (hidden) admin note | `#admin_note` (name `admin_note`) | set via JS if needed |
| Your Message | `#msg` (name `msg`) | textarea |
| Send | `#contactform input[name="submit"]` | `type=button`, `onclick="uploadfile()"` — **not** a native submit |
| (hidden) form type | `#form_type` | `1` for embroidery |
| Error/status spans | `#jobrefError`, `#checkboxError`, `#imgError`, `#status`, `#progressBar` | JS writes validation + upload status here |

### Gotchas that a screenshot cannot reveal

1. **Color-scheme id swap.** `change_form()` reassigns the `id` `colorScheme`
   between the CMYK/RGB `<select class="color_scheme">` and the printing-method
   `<select class="color_scheme_printing">` depending on the tab. `uploadfile()`
   posts `document.getElementById('colorScheme').value`. For the embroidery/artwork
   tabs the CMYK/RGB select holds the id; for Product Visual it moves. Bind to the
   **class** `select.color_scheme` (always the CMYK/RGB one) so it survives the swap.
2. **Repeated `fileType` values.** Across the hidden Artwork/Visual sections there
   are other `name="fileType"` checkboxes (`ai`, `eps`, `hpdf`, `pdf`, `jpg`).
   `dst/emb/exp/other` are unique to the embroidery section and the only visible
   ones after the tab switch, so `input[name="fileType"][value="dst"]` is safe.
3. **Duplicated ids.** All three turnaround radios share `id="radio"`; target by
   `value`. The tab buttons share `digitize_btn`; target by `onclick`.

## Step 4 — Send + the success signal

`uploadfile()` (inline on the page) does, in order:

1. require `#jobref` (else `#jobrefError` = "job reference is required..!"),
2. read `input[name="radio"]:checked` (throws if none),
3. require ≥1 checkbox checked (else `#checkboxError`),
4. require `#file1` (else `#imgError` = "image is required..!"),
5. build a `FormData` (`file1..3`, `jobref`, `radio`, `fileType` (comma-joined),
   `colorScheme`, `msg`, `form_type`, `otherText`, `proof_template`, `admin_note`),
6. `XMLHttpRequest` **POST** to `https://www.artworklady.com/placeorder/order_form_submit`,
7. on the XHR `load` event → `#status` = `responseText`, then
   `document.location.href = 'https://www.artworklady.com/placeorder/thanks'`.

**The redirect is not a success check** — `completeHandler` fires on `load`
regardless of HTTP status and never inspects it, so a server-side failure still
lands on `/thanks`. The driver therefore waits for the **actual
`order_form_submit` response** and treats the job as posted only on **HTTP 200**,
capturing the response body (wire the routine's Odoo update to that). The
`/thanks` navigation is captured too, but only as corroboration.

> **Recorded from a live run:** on success `order_form_submit` returns **HTTP
> 200 with an empty body** — there is **no confirmation/ticket id** anywhere in
> the response, and `/placeorder/thanks` is a static page with none either. So
> the portal gives the caller nothing to correlate a submission back to. The
> success signal is therefore "HTTP 200 + `/thanks`", and **dedupe must live on
> the Odoo side** (stamp the demand with the `job_reference` + a submitted-at
> time and skip demands already stamped) — the portal itself does not dedupe.

## Environment / TLS

- **Browser proxy.** Reads `ARTWORKLADY_PROXY` else `HTTPS_PROXY`; unset on a
  normal network.
- **CA pinning.** Behind a TLS-terminating egress proxy, set
  `ARTWORKLADY_TLS_SPKI_PINS` to the proxy CA's base64 SPKI hash(es); the driver
  passes them to Chromium's `--ignore-certificate-errors-spki-list`, which
  whitelists exactly those keys instead of disabling verification. Compute a pin
  with:
  ```bash
  openssl x509 -in ca.crt -pubkey -noout \
    | openssl pkey -pubin -outform der \
    | openssl dgst -sha256 -binary | openssl enc -base64
  ```
- **Headless.** Confirmed working headless at 1440×900 with a desktop UA and
  `--disable-blink-features=AutomationControlled`. No CAPTCHA / MFA / device check
  appeared on login from this environment. (Untested: login from a datacenter IP
  over a long period, and whether the vendor ever adds a bot check.)

## Failure artefacts

On `config_error` / `portal_error` the driver writes `artworklady_failure.png`
and `artworklady_failure.html` to `ARTWORKLADY_ARTIFACT_DIR` (default cwd), so the
first failing run is the diagnostic one.
