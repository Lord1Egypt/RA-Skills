# SanMar portal "process a return" — reverse-engineered flow (working notes)

> Captured interactively from the live sanmar.com portal (Vue-rendered, Bootstrap 5).
> These notes back the Playwright-driven `process-return` action. Selectors are
> what the driver targets; anything dynamic is parameterized from stdin JSON.
>
> **Surface:** the sanmar.com customer *portal* (separate login from the SOAP
> web-services creds). Driver creds: `SANMAR_PORTAL_USERNAME` /
> `SANMAR_PORTAL_PASSWORD`.

---

## ⏯️ RESUME HERE (read this first)

**Status:** Steps 1–4 are implemented and shipped in `scripts/sanmar_browser.py`
(action `process-return`). The driver logs in, resolves the order, opens the
initiate page, matches lines, and fills quantity + reason + reason-specific
fields. It then **stops before submitting**:
- `confirm: false` → returns a `dry_run` preview (nothing filed).
- `confirm: true` → returns `not_implemented` (guarded by
  `FINAL_SUBMIT_IMPLEMENTED = False` in `sanmar_browser.py`).

**What's missing:** Step 5 — the **Continue → review → confirm** submission and
the success page. It was deliberately left untested because there's no return
sandbox; it must be captured during a *real* return the user intends to file.

**Exactly what to ask the user (progressive-HTML method, same as before):**
The user performs one real return in the browser and pastes, at each click:

1. **After clicking "Continue"** on the initiate page — the **URL** and the
   **HTML** of the review/confirmation page. Specifically:
   - Is there a final **"Submit"/"Place Return"/"Confirm"** button? Capture its
     selector (id/class/text) and whether it's a normal submit or JS-driven.
   - Any **required fields on the review page** not present on the initiate page
     (e.g. a contact-preference radio that must be chosen, a terms checkbox)?
   - Whether the **contact-preference checkboxes** (`#email` / `#telephone`,
     seen on the initiate page) are required before Continue enables.
2. **After final submit** — the **URL** and **HTML** of the **success page**,
   especially the **RMA / return-confirmation number** and where it appears
   (selector + example value/format). Also whether a printable label / PDF link
   is shown (capture that link's selector if so).
3. Any **error states** they hit (validation messages, ineligible warnings) —
   selector + text — so the driver can surface them cleanly.

**Then, to finish the code:**
- Implement `SanMarReturnsDriver.complete_submission()` in `sanmar_browser.py`
  (click Continue, handle the review page, click final submit, wait for success,
  scrape the RMA number → return it).
- Flip `FINAL_SUBMIT_IMPLEMENTED = True`.
- The `process_return()` entry point already wires `confirm: true` →
  `complete_submission()` → `status="submitted"` + `rma_number`; no other
  changes needed there.
- Add a realistic end-to-end example to `references/examples.md`.
- ⚠️ Test only with a return the user actually wants to file — there is no
  sandbox and `confirm: true` will create a real RMA.

See **Step 5** below for the detailed capture checklist.

---

## Step 1 — Login (`https://www.sanmar.com/`)

Standard Spring Security form embedded in the homepage header.

| Element | Selector | Notes |
| --- | --- | --- |
| Form | `#login-header-form` | POSTs to `/j_spring_security_check` |
| Username | `#username` (`name=j_username`) | ← `SANMAR_PORTAL_USERNAME` |
| Password | `#password` (`name=j_password`) | ← `SANMAR_PORTAL_PASSWORD` |
| Submit | `#login-header-form button.btn-primary-df[type=submit]` ("Log In") | avoid the hidden `.fv-hidden-submit` |
| CSRF | `input[name=CSRFToken]` | dynamic per page — never hardcode; filling the live form carries it |

- Fill visible fields + click the real "Log In" button (don't POST directly) so
  CSRF + JS validation come along.
- **Login does not redirect** — the header just reloads the homepage. Success tell:
  header flips from `.logged-out` to a logged-in state. Guard: if a later
  authenticated nav bounces back to a login form → raise `config_error`.
- Leave "Stay Logged In" (`_spring_security_remember_me`) unchecked.

## Step 2 — Reach order history

No post-login redirect. **Explicitly navigate** to:

```
https://www.sanmar.com/mysanmar/order-history
```

## Step 3 — Order history (`/mysanmar/order-history`)

Table `#sales-order-table`, one `tr.orders-separator` per order. Per row (desktop cells):

| Field | Selector (within row) | Example |
| --- | --- | --- |
| Status | status `<img>` tooltip text | `Sanmar Shipped`, `In Progress`, `Complete`, `Return Processing` |
| Order # | `td.col-order-number strong` | `SO-162275814` |
| PO # | `td.col-purchase-order span` | `P12146` |
| Date placed | `td.col-order-date` | `06/17/26` |
| Return control | `a[id^="returnLinkId-"]` (e.g. `#returnLinkId-1`) | JS-driven |

**Key facts:**
- **Order # (`SO-…`) is the unique key. PO # is NOT unique** — e.g. `P12119`
  appears on 3 rows, `P12037` on 2. Action keys on `SO-…`; accepts a PO but
  errors (listing candidate `SO-…`) if the PO maps to >1 row.
- **Eligibility is encoded in the return icon:**
  - Eligible: link has `href="#"`, img `Return.svg`, popover "Return Items".
  - Ineligible: **no `href`**, img `Return-Disabled.svg`, popover
    "Returns are available for 30 days from purchase and after they have been
    shipped. This item is not eligible for return. Please call (800) 426-6399…"
- List is paginated (15/page default, items-per-page up to 250, "Previous 30
  days" window). Clicking the icon is equivalent to navigating directly (Step 4),
  so the driver can skip the table entirely when given an `SO-…`.

## Step 4 — Initiate return (`/mysanmar/returns/initiate?salesOrderNumber=SO-…`)

**Clicking the return icon = navigating to this URL.** Driver `page.goto()` with
the `salesOrderNumber` query param; no need to click through the table.

Container: `#initiate-return` (Vue, `data-v-app`).
Header: `h1` → "Initiate Return - Order #SO-162275814".
Summary table `#table-history-summary`: PO, Sales Order, Ordered date.

### Line items — `table.table-initiate-returns` (rows `tr.order-history-details-items`)

Per row (0-based index `N`):

| Field | Selector (within row) | Example |
| --- | --- | --- |
| Select item | `input#select-item-{N}` (+ `label[for=select-item-{N}]`) | checkbox |
| Style | `td.column-style .style-number` | `ST405` |
| Color | `td.column-color .name` (also swatch img `alt`) | `White` |
| Size | `td.column-size` | `L` |
| Description | `td.column-description span` | `ST PosiCharge Tri-Blend Wicking Polo` |
| Warehouse | `td.column-warehouse span` | `Cincinnati, OH` |
| Pieces (orig qty) | `td.column-pieces` | `1` |
| Price | `td.column-price` | `$11.17` |
| Amount | `td.column-amount span` | `$11.17` |
| Return qty input | `td.column-quantity input[type=number]` (`min=1`, `max=`pieces) | hidden until selected |
| Reason select | `td.column-select-reason select` | hidden until selected |

Select-all: `#select-all-returns`.

**Critical interaction:** the return-qty input and reason `<select>` are
`display:none` until the row's `#select-item-{N}` checkbox is checked. Flow per
line: check item → fill qty (1..pieces) → choose reason.

### Reason codes (canonical `<option>` values)

| Value | Label | Note |
| --- | --- | --- |
| `SAMPLES` | Samples | 1–2 pcs/size (≤4/SKU) |
| `UNWANTED` | Unwanted | **20% restock fee** deducted from credit |
| `ORDER_INCORRECT` | Order incorrect | |
| `DEFECTIVE_DAMAGED` | Defective/Damaged | |
| `INCORRECT_PRODUCT` | Received Incorrect Product | |

### Reason-conditional sub-row (`tr.return-info-row`, appears after a reason is picked)

Selecting a reason injects a sibling row with reason-specific **required** fields,
suffixed by the row index `{N}`:

- **`ORDER_INCORRECT`**
  - `textarea#incorrect-details-{N}` (name `incorrect-details-{N}`, required, maxlength 4000)
    — "Please provide information of the incorrect products"
  - radio `incorrect-replacement-{N}` (required): `#incorrect-replacement-yes-{N}`
    (value `true`) / `#incorrect-replacement-no-{N}` (value `false`)
- **`DEFECTIVE_DAMAGED`**
  - `textarea#defective-details-{N}` (name `defective-details-{N}`, required, maxlength 4000)
    — "Please provide details of the issues with the items"
  - radio `defective-replacement-{N}` (required): `#defective-replacement-yes-{N}` /
    `#defective-replacement-no-{N}`
  - **optional** image upload `#file{N}` (jpg/jpeg/png/gif, ≤2MB)
- **`INCORRECT_PRODUCT`** — **reuses the `ORDER_INCORRECT` field group** (same ids/names):
  `textarea#incorrect-details-{N}` + radio `incorrect-replacement-{N}`
  (`-yes-{N}`/`-no-{N}`). (Observed without the `required` attr on the textarea —
  likely a Vue timing quirk; it's visually required, so fill it anyway.)
- **`SAMPLES`** — no sub-row (qty + reason only).
- **`UNWANTED`** — no sub-row (qty + reason only); 20% restock fee applies.

Complete reason → extra-fields matrix:

| Reason | details textarea | replacement radio | image upload |
| --- | --- | --- | --- |
| `SAMPLES` | — | — | — |
| `UNWANTED` | — | — | — |
| `ORDER_INCORRECT` | `#incorrect-details-{N}` (req) | `incorrect-replacement-{N}` (req) | — |
| `INCORRECT_PRODUCT` | `#incorrect-details-{N}` (req) | `incorrect-replacement-{N}` (req) | — |
| `DEFECTIVE_DAMAGED` | `#defective-details-{N}` (req) | `defective-replacement-{N}` (req) | `#file{N}` (optional) |

Implication for input schema — per return line:
`{style, color, size, quantity, reason, details?, replacement?, image_path?}`
where `details` + `replacement` are required iff reason ∈
{`ORDER_INCORRECT`, `INCORRECT_PRODUCT`, `DEFECTIVE_DAMAGED`}; `image_path`
only meaningful for `DEFECTIVE_DAMAGED`.

### Contact / summary (revealed after a line is selected)

- Contact Information block: shows email + telephone; "Update Contact Details"
  → modal `#update-contact-modal`. Contact-preference checkboxes `#email`,
  `#telephone`.
- Summary: Total Merchandise Amount, Estimated Restock Fee, Estimated Credit.
- **Continue** button (`button.btn-primary`, text "Continue") starts `disabled`;
  enables once a valid line (item+qty+reason) is present.
- Cancel → `../order-history`.

Ignored on this page (global site chrome, not part of returns): the
"Email this page" modal, all inventory/backorder modals, warehouse-details modal.

## Step 5 — Review / confirm  *(NOT YET CAPTURED — implement here)*

This is the only remaining piece. Capture it from a **real** return (no sandbox
exists). Checklist of HTML/URLs to get from the user, in order:

- [ ] **Initiate page, pre-Continue:** are the contact-preference checkboxes
      (`#email` / `#telephone`) or the "Update Contact Details" modal required
      before `Continue` enables? (The driver currently does not touch them.)
- [ ] **Click "Continue" →** record the resulting **URL** (new route, or same
      page with a revealed review section?).
- [ ] **Review page HTML:** the summary of lines being returned, the
      estimated-credit block, and **the final submit control**
      (id/class/text; submit-button vs JS handler).
- [ ] **Any new required fields** on the review page (terms checkbox, contact
      method, shipping/label choice) — selector + values.
- [ ] **Click final submit →** the **success page URL + HTML**, with the
      **RMA / return-confirmation number** (selector + example + format) and any
      printable label / PDF link (selector).
- [ ] **Error/validation states** encountered — selectors + messages.

### Design decisions already made (Steps 1–4)

- Lines matched to rows by `style`+`color`+`size`; ambiguous (identical SKU on
  >1 row) → error, not a guess. Resolved in `match_lines()`.
- Default return qty = original `pieces` when `quantity` omitted; qty > pieces
  → error.
- Order keyed on `SO-…` (unique); `po_number` resolved via order history,
  errors if it maps to >1 order.
- Final-submit gated behind `confirm: true` (mirrors `create-purchase-order`)
  **and** `FINAL_SUBMIT_IMPLEMENTED` until Step 5 lands.

### Code touchpoints to finish (all in `scripts/sanmar_browser.py`)

1. Implement `SanMarReturnsDriver.complete_submission()` → returns the RMA number.
2. Set `FINAL_SUBMIT_IMPLEMENTED = True`.
3. (Optional) capture the label/PDF URL onto `ReturnResult` (add a field in
   `schemas.py` if desired).
4. Add an end-to-end example to `references/examples.md` and update the
   "Status" note in `SKILL.md`'s Processing-returns section.
