# adidas Click "place a purchase order" — reverse-engineered flow (working notes)

> Captured interactively from the live adidas Click B2B portal. These notes
> back the Playwright-driven `create-purchase-order` action. Selectors are what
> the driver targets; anything dynamic is parameterized from stdin JSON.
>
> **Surface:** the adidas Click B2B ordering portal
> (`https://b2bportal.adidas-group.com`). Driver creds:
> `ADIDAS_CLICK_USERNAME` / `ADIDAS_CLICK_PASSWORD` (base URL override
> `ADIDAS_CLICK_BASE_URL`).

---

## ⏯️ RESUME HERE (read this first)

**Status:** ✅ Complete. All steps and sub-paths are implemented — the skill
drives a purchase order end to end: login → add line quantities to the active
cart → set Customer PO / delivery location (default, saved, or one-time dropship
with State dropdown) / shipping method (code or label) → Next → Calc. Net Price
(wait for "Done!") → Order Now → parse the confirmation number from the redirect
URL. `confirm: false` is a full dry run; `confirm: true` **places a real order**
(no sandbox).

**Validated:** a real order has been placed end to end against the live site
(cart dedup → product → size qty → checkout → Calc Net Price → Order Now →
confirmation number; net `order_total` confirmed). Several live-only issues were
fixed along the way: login tell (Logout hidden in a dropdown), cart-name
uniqueness + can't-delete-active-cart, lazy-rendered size tiles, and the cart
"Next" button inactive until scrolled.

**Method (progressive HTML capture — same as SanMar's `process-return`):** we
build one step at a time. For each step the user pastes the page **URL** and the
relevant **HTML** (the form / table / controls), Claude extracts the selectors,
implements the driver method, and flips that step's `*_IMPLEMENTED` flag.

**Build complete** — nothing left to capture for ordering. A second action,
`check-inventory-pricing`, was added on top of these steps (inventory read /
wholesale-pricing lookup that never orders) — see "Inventory / pricing checks"
below. It captured **no new selectors**; it reuses steps 1–4.

A third action, `get-order-tracking`, drives a **different, read-only surface**
(order book → order detail → delivery tracking) and *did* capture new selectors
— see "Delivery tracking" at the end of this file. It shares only Step 1
(login) with the ordering flow.

### Step map / gates (`scripts/adidas_browser.py`)

| Step | Gate flag | Driver method | Status |
| --- | --- | --- | --- |
| 1. Login | `LOGIN_IMPLEMENTED` | `login()` | ✅ implemented |
| 2. Add lines (product nav, size map, inventory, qty input) | `ADD_LINES_IMPLEMENTED` | `add_lines()` | ✅ implemented |
| 3. Checkout (PO + delivery + shipping) | `CHECKOUT_IMPLEMENTED` | `fill_checkout()` | ✅ implemented (incl. dropship + shipping) |
| 4. Checkout → calc net price → order now | `FINAL_SUBMIT_IMPLEMENTED` | `price_cart()` + `complete_submission()` | ✅ implemented |
| Check. Inventory / pricing (no order) | — (reuses 1–4) | `read_inventory()` / `price_cart()` / `delete_cart()` / `check_inventory_pricing()` | ✅ implemented |
| Track. Delivery tracking (read-only) | — (reuses 1 only) | `find_orders_for_po()` / `open_order()` / `read_delivery_tracking()` / `read_expected_ship_dates()` / `get_order_tracking()` | ✅ implemented (live run pending) |

### Insufficient-availability decision point ✅ IMPLEMENTED

`add_lines` reads availability for **every** line first (`_prepare_lines` opens
each product once and reads the size-tile inventory indicator; `_parse_available`
treats `"300+"`/blank as sufficient, exact numbers as the count). A line is
**short** when its exact available count < requested. Then per
`OrderRequest.on_insufficient_stock`:

- **`pause`** (default) + any shortfall → raise `_OrderPause`; the
  entry point returns `status="needs_confirmation"` with `out_of_stock`
  (`[{style, size, requested, available}]`) and a `message` listing the choices,
  and places **nothing** (even with `confirm: true`, because this happens before
  the submit gate). The cart may hold nothing (short found in the read pass) — a
  re-run's `new_cart` dedup cleans up regardless.
- **`order`** → enter the short line anyway with the spread accepted (delayed
  delivery); line note records it.
- **`skip`** → do not enter the short line (quantity 0, "removed" note); order the
  rest. If **all** lines are skipped → error ("nothing to order").

The **agent** turns a `needs_confirmation` result into a user message, then
re-runs with `on_insufficient_stock: "order"` / `"skip"`, or **substitutes** by
editing `lines` and re-running. Pre-authorizing phrases in the user's prompt
("order anything out of stock" / "remove out-of-stock items") let the agent set
the flag up front and skip the pause. See SKILL.md "Out-of-stock handling".

### Missing-product decision point ✅ IMPLEMENTED

Same shape, second axis: a style adidas serves **no product page** for is a
decision for the caller, not a crash. `_open_product(style, missing_ok=True)`
returns False and records the style in `driver.missing_products`
(`[{style, sizes, requested, reason, detail}]`); `_prepare_lines` marks that
style's lines `not_found`. Then per `OrderRequest.on_missing_product`:

- **`pause`** (default) → the same `_OrderPause` (it carries both
  `out_of_stock` and `missing_products`), so the entry point returns
  `status="needs_confirmation"` and places **nothing**.
- **`skip`** → drop those lines (quantity 0, `not offered …` note), order the
  rest. All lines missing → the "No lines could be ordered" error names the
  styles.
- **`error`** → `missing_ok=False`, so `_open_product` raises `AdidasAPIError`
  (the pre-0.7 behavior).

`check_inventory_pricing` forces `skip` internally (a check reports what it can
read and never aborts mid-run) and then re-escalates itself: if anything landed
in `missing_products`, the result flips to `status="needs_confirmation"` unless
the caller asked for `skip`. Its `add_lines` fallback also catches
`AdidasAPIError` now, so a line that fails to resolve can never strand the
throwaway `DO NOT BUY` cart.

Detection details and the still-uncaptured not-found markup: see "Style adidas
does not carry" under Step 2. See SKILL.md "Missing / unlisted product
handling".

---

## Step 1 — Login (`/login`)  ✅ IMPLEMENTED

Standard username/password form at `https://b2bportal.adidas-group.com/login`.
Title "Welcome to Click". Implemented in `AdidasClickDriver.login()`.

| Element | Selector | Notes |
| --- | --- | --- |
| Form | `#loginFormDsk` | POSTs to `/login` (`method=post`) |
| Hidden | `input#queryString` (`name=queryString`) | dynamic; filling the live form carries it — never hardcode |
| Username | `#usernameField` (`name=username`) | ← `ADIDAS_CLICK_USERNAME` |
| Password | `#passwordField` (`name=password`) | ← `ADIDAS_CLICK_PASSWORD` |
| Remember me | `#form-reminder` (checkbox) | left unchecked |
| Submit | `#send2Dsk` ("Login", `type=submit`) | the real button — fill + click so JS validation/CSRF come along |
| Bad-creds alert | `#login-error-alert` ("Invalid username or password.") | starts `display:none`; JS flips it visible **without navigation** |
| SSO error alert | `#sso-login-error-alert` | SSO-only; also checked |
| SSO button | `#send2SSO` ("Single Sign On for Sales Managers", `type=button`) | **separate IdP flow — not used by this skill** |
| Forgot links | `#forgot-password-link` (`/forgotPassword`), `#forgot-username-link` (`/forgotUsername`) | not used |

**Driver behavior:**
- Fill visible fields → click `#send2Dsk` → `wait_for_load_state("networkidle")`.
- **Bad-credentials tell:** `#login-error-alert` (or `#sso-login-error-alert`)
  becomes visible in place → raise `config_error`.
- **Success tell (provisional):** a valid login **navigates away from `/login`**.
  If `#loginFormDsk` is still present at a `/login` URL with no error → raise
  `config_error` (possible SSO-only account or blocking interstitial).

**Confirmed post-login (from the landing-page header capture):**
- **Landing URL:** `/adidas/reorder/home`. No cookie / T&C interstitial appears.
- **Logged-in tell:** wait for an always-visible authenticated shell control —
  `_LOGGED_IN_MARKER` = `#ReorderNavLink, #CartOverviewNavLink,
  #HeaderSearchButtonButton, #PersonalNavigationDropdownLabel` (any visible).
  ⚠️ **Do NOT use `#LogoutNavLink`** — it lives inside the collapsed account
  dropdown (`#PersonalNavigationDropdownList`), so it is present but *hidden*;
  a visibility wait on it times out even though login succeeded (observed as a
  false "login did not complete" on a real run).

## Step 2 — Add product lines  *(IN PROGRESS)*

### Step 2a — Header search (✅ wired in `_search_style`)

Global site header `.o-siteHeader`. The search box lives in
`section.o-siteHeader__searchBox` and is **collapsed by default** — click the
magnifier to reveal the input; the submit button is `disabled` until text is
entered.

| Element | Selector | Notes |
| --- | --- | --- |
| Open (magnifier) | `#HeaderSearchButtonButton` | expands the collapsed search |
| Input | `#HeaderSearchSearchInput` (`name=search`) | placeholder "Search for Article Numbers, Colors, Brand types" — the **style / article number** goes here |
| Submit | `#HeaderSearchSubmitButton` (`type=submit`) | starts `disabled`; enables once the input has text |
| Close | `#HeaderSearchCloseButton` | not used |

Other useful header nav (for later steps / fallbacks):
`#CatalogNavLink` → `/adidas/reorder/catalog`,
`#CartOverviewNavLink` → `/adidas/reorder/cart-overview`,
`#OrderBookNavLink` → `/adidas/reorder/my/order-book`,
`#QuickAddTileButton` (a "Quick Add" side panel — a possible bulk-entry
alternative to search),
`#HeaderCartsTileButton` (cart side panel).

### Navigation — direct product URL (✅ preferred, `_open_product`)

- **Search** lands on a results page regardless of exact match:
  `/adidas/reorder/catalog?searchTerm={style}`.
- **Recommended:** navigate straight to the product —
  `/adidas/reorder/product/{STYLE}` (e.g. `/adidas/reorder/product/JW4306`).
  **adidas article numbers encode the color** (JW4306 = "M FLEECE CREW BLACK"),
  so there is **no color picker** — landing on the URL is landing on the color.
  `_open_product` uses this and waits for `#CartModule-SizeTable`.

#### Style adidas does not carry (⚠️ tell NOT captured — text-matched)

A style this account isn't offered (or a wrong article number) has **no size
table to wait for**. The portal's empty/not-found product markup has **not been
captured**, so — deliberately, rather than inventing a selector — `_open_product`
decides with two signals it can trust:

1. **URL**: after `goto`, the page is no longer under `/reorder/product/`
   (the portal bounced it) → `reason: "not_found"`.
2. **Text**: the visible body matches `_PRODUCT_MISSING_TELL_RE` ("no results",
   "not found", "no longer available", …) once `_LOGGED_IN_MARKER` has painted
   → `reason: "not_found"`.

Neither firing within `_PRODUCT_WAIT_MS` (15s, polled every 400ms rather than
one blocking `wait_for_selector`, so a bad style doesn't burn the full 30s
timeout) gives `reason: "unresolved"` — reported as *unconfirmed*, never as
"this style doesn't exist". A false positive is safe by construction: it can
only route the style into the `on_missing_product` escalation, which places
nothing and asks the user.

**Next capture:** open a style the account isn't offered and record the real
not-found page's id/markup, then swap the text match for that selector (keeping
the text match as a fallback).

### Step 2a — Availability date gate (✅ wired)

Above the size table sits a draggable date-tab strip
(`#DateTabs-DraggableTable`); the active tab is `#DateTabButton` and its inner
text is a formatted date (e.g. `"Jul 31, 2026"`). This is the **earliest date
the product can ship**, and the size-tile inventory numbers refer to _that_
date. If it isn't today, the size table is describing future stock —
**nothing is orderable now** regardless of what the tiles show.

`_product_available_today()` reads `#DateTabButton`, parses `%b %d, %Y`, and
compares to today's date. Both the order flow (`_prepare_lines`) and the
inventory read (`read_inventory`) call it right after `_open_product` and
before touching any tile; when it returns False, every requested line for that
style is classified `unavailable` with a `"not available until {date}"` note
and the size-tile read is skipped. Fail-open on a missing/unparseable date
(logs a warning) so a portal shape change doesn't silently block every order.

### Step 2b — Size table (✅ mapping + inventory wired)

Container `#CartModule-SizeTable`. ⚠️ **The grid sits below the fold and
lazy-renders its per-size tiles only when scrolled into view** — the size
*labels* (SizeTranslation cells) render eagerly, but the
`#CartModule-SizeTile-{style}-{code}` tiles do not attach until the table enters
the viewport. `_open_product` calls `_ensure_size_tiles_rendered(style)`
(scrollIntoView center → wait for `[id^="CartModule-SizeTile-{style}-"]`, with a
nudge-scroll fallback) before any tile interaction, so a headless run (or an
unscrolled headed run) doesn't time out on a not-yet-rendered tile.

A horizontally-scrolling **size-run grid**: one column per size, a per-size cell
per article row.

⚠️ **Off-screen sizes lazy-load** — only the visible sizes' cells are in the DOM;
the rest render when the row's **arrow buttons** are clicked
(`#CartModuleSizeBarNavigationForward{group}Button` /
`…Back{group}Button`, `{group}` dynamic — targeted by id-prefix). `_ensure_size_
in_view(style, code)` resets to the leftmost then scans forward (clicking the
forward arrow, polling) until the size's wrapper cell
(`#CartModule-SizeRow-SizeTile-Wrapper-{style}-{code}`) attaches. Called before
classifying a size and before entering its quantity.

**Per-size cell shapes** (`_classify_size` → `ok` | `short` | `unavailable`):
- **Orderable:** wrapper contains `#CartModule-SizeTile-{style}-{code}` (the
  quantities div) + `#CartModule-SizeTile-InventoryIndicator-{style}-{code}`.
  Stock `0` **with a restock date** still lives here — it's backorderable
  (`short` when available < requested).
- **Not available:** wrapper contains `#CartModule-SizeTile-Status-NotAvailable-
  {style}-{code}` (the "X" cell, hashed class `notAvailable--…`) and **no**
  quantity input — it will never be restocked and **cannot be ordered**
  (`unavailable`). Dropped under every policy with a "not available" note; under
  `order` it still can't be placed (only remove/substitute).

> ⚠️ **Use stable ids, not classes.** The `*--xxxxx` classes (`sizeTile--jfyHK`,
> `sizeTranslation--xFkgj`, …) are hashed CSS-module names that change on every
> build. All selectors below use the semantic `id` prefixes.

**Size label → numeric code** (from the size-bar header cells):
`#CartModule-SizeBar-SizeTranslation-{group}-{code}` with the label in an
`<ins>`. `{group}` is a conversion-group id (`51` in the sample). Observed map:

| Label | Code | | Label | Code | | Label | Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| XS | 210 | | 3XL | 320 | | 3XLT | 410 |
| S | 230 | | 4XL | 330 | | 4XLT | 420 |
| M | 250 | | 5XL | 340 | | 5XLT | 430 |
| L | 270 | | LT | 380 | | LT2 | 450 |
| XL | 290 | | XLT | 390 | | XLT2 | 460 |
| 2XL | 310 | | 2XLT | 400 | | 2XT2 | 470 |

`_size_code_map()` reads these live (never hardcodes) into `{label: code}` and
resolves the requested size label to its code.

**Per-style, per-size tile** (`{style}` = article number, `{code}` = size code):

| Element | Selector |
| --- | --- |
| Quantities cell | `#CartModule-SizeTile-{style}-{code}` |
| Inventory text | `#CartModule-SizeTile-InventoryIndicator-{style}-{code}` (`300+`, `160`, `0`, …) — in-stock tiles also carry a `hasInventory--…` class (hashed; not used) |
| Restock icon | `#CartModule-SizeTile-RestockIndicator-{style}-{code}` |
| Article total qty | `#CartModule-MaterialRow-Summary-TotalQuantity-{style}` |
| Article total price | `#CartModuleMaterialRowSummaryTotalPrice{style}Price` |
| Product name | `#CartModule-TinyProduct-{style}-ProductName` (e.g. "M FLEECE CREW BLACK") |
| Wholesale price | `#CartModuleTinyProductPrice{style}Price` ("Wholesale Price from $22.50") |

`_read_inventory()` surfaces the availability text; `add_lines()` groups lines
by style, opens each product once, and fills all its sizes.

### Step 2b-2 — Re-stock date (✅ IMPLEMENTED, hover-read)

A size that adidas will replenish carries a small calendar icon in the tile's
top-right corner. Captured markup:

```html
<div class="restockIcon--O65EH " id="CartModule-SizeTile-RestockIndicator-KD5434-240">
  <div class="m-restockWeekIndicator">
    <svg viewBox="0 0 24 24" class="a-icon -calendarInactive">…</svg></div></div>
```

The id follows the same `{style}-{code}` convention as the other tile ids
(`_SIZE_TILE_RESTOCK_ID`), so its **presence** is a reliable "this size gets
restocked" tell. The **date is not in that markup** — the portal renders it only
in a tooltip on hover (*"Re-stock in Nov 8, 2026"*).

`_read_restock_date` therefore:

1. checks `title` / `aria-label` / `data-tooltip` / `data-title` on the icon and
   its descendants first (free, in case a build exposes it as an attribute);
2. otherwise hovers the icon, waits 400 ms, and matches the page text against
   `_RESTOCK_TOOLTIP_RE` — anchored on the word "re-stock" so an unrelated date
   elsewhere on the page can never be picked up. The **tooltip's own markup is
   not captured**, so no selector is invented for it;
3. moves the mouse to (0, 0) in a `finally` so the tooltip closes and the next
   size reads its own date, not this one fading out.

Called **only for a `short` size** (`_classify_size`), so an in-stock check
costs no hovers, and never for the `X` cell — a flatly unavailable size has no
restock date by definition.

Surfaced as `restock_date` (as shown) + `restock_date_iso` (via `_iso_date`,
which reuses the tracking flow's `%b %d, %Y` parser) on `OrderLineResult`,
`CheckLineResult`, and each `out_of_stock` entry, and woven into the per-line
`note` and the `needs_confirmation` message — including the explicit "no restock
date posted" wording when adidas showed none.

### Step 2c — Quantity input (✅ IMPLEMENTED)

Clicking a size tile opens a **single shared floating overlay** `#quantityInput`
(absolutely positioned via inline `left`/`top` over the active cell). Typing a
value + **Enter** commits it; the overlay closes and the ordered qty renders in
the cell. Entering a quantity **is** adding to the working cart — everything is
under the `CartModule` namespace, and there is **no separate add-to-cart button**
on the product page.

| Element | Selector | Notes |
| --- | --- | --- |
| Overlay | `#quantityInput` | shared; repositions over the clicked tile |
| Quantity field | `#quantityInput input` | react-numeric-input, **no id of its own**; `.fill()` + `press("Enter")` to commit |
| Decrease / increase | `#QuantityInputDecreaseButton` / `#QuantityInputIncreaseButton` | not used (we type the value) |
| **Committed qty readback** | `#CartModule-SizeTile-OrderedInDate-{style}-{code}` | appears in the cell after commit (e.g. "10") — the driver reads this to confirm |
| Committed cell state | tile gains hashed class `orderedInThisDate--…` | hashed; not used |

**Insufficient availability** → dialog `#CartModule-SizeItemProposals`
("Insufficient availability — Do you want to spread your quantity over the
following dates?"):

| Button | Selector |
| --- | --- |
| Yes, spread delivery | `#CartModuleSpreadAcceptButton` |
| No, just one delivery | `#CartModuleSpreadDeclineButton` |
| Close | `#CartModuleSizeItemProposalsOverlayCloseButton` |

Driver policy (`OrderRequest.spread_delivery`, default **false**): declines the
spread (single delivery). `true` accepts it. `_handle_availability_proposal`
short-waits (2s) for the dialog after each commit and clicks accordingly;
`_read_ordered_quantity` then reports what actually committed, and `add_lines`
notes any shortfall on the line result.

> **Cart behavior (confirmed):** adidas Click supports **multiple carts**.
> Quantities entered on the product page land in the **active** cart.
> `/adidas/reorder/cart` opens that active cart. When a size's requested qty
> exceeds availability **and the spread is declined**, adidas moves the overflow
> into a **new, inactive cart** ("A new cart with the additional quantities has
> been created") — it defaults to inactive, so it does not interfere with
> checking out the active cart.

Implemented in `_set_size_quantity` / `_handle_availability_proposal` /
`_read_ordered_quantity`; `ADD_LINES_IMPLEMENTED = True`.

## Step 2.5 — Fresh cart per run  ✅ IMPLEMENTED (`create_new_cart`)

adidas Click supports **multiple carts**, and on a **shared account** entering
quantities on a product page adds to whatever cart is *active* — which risks
piling onto (and checking out) a teammate's cart. So by default
(`new_cart: true`) the driver creates its own cart first, right after login.

Open the carts side panel with `#HeaderCartsTileButton`, then:

| Element | Selector | Notes |
| --- | --- | --- |
| New Cart | `#CreateNewCartButton` | opens the name form |
| Name field | `form.o-editCartForm input.m-input__field` | no own id; `maxlength=25`; same charset as the PO (`/ _ . ? &`) |
| Save | `#EditCartSaveButton` (`type=submit`) | creates the cart **and switches the active cart to it** |
| Cancel | `#EditCartCancelButton` | not used |

The cart **name is the personalReference — i.e. the Customer PO** (the carts
list column `personalReference` is headed "Cart Name"). The driver names the new
cart with the (sanitized) PO. Pass `new_cart: false` to reuse the active cart.

**Delete-first, then create.** Two hard rules interact: (a) **cart names must be
unique** — the New-Cart **Save button stays `disabled`** if a cart with that name
already exists (so you can't create-then-delete); and (b) **the active cart
can't be deleted.** So the driver deletes any same-named leftover *first*, and if
that leftover is the active cart, activates a different cart before deleting it.

Flow (`create_new_cart` → `_delete_carts_named`):
1. `_cart_rows()` snapshots the carts **ag-grid** (`.o-headerCartsList`): per row
   the `row-id`, name (`a.a-link[title=…]`, title = cart name = PO), active flag
   (`.o-activeBadge` present), and activate-toggle id
   (`div.a-toggle[id$="ToggleActiveCartToggle"]`).
2. `old_ids` = rows whose title == PO. If none, skip to create.
3. If a same-named cart **is active**, click another cart's toggle
   (`[id="{cartId}ToggleActiveCartToggle"]`) to make it active — the active row
   has no toggle. (If the leftover is the *only* cart → clear error; empty/rename
   manually or `new_cart:false`.)
4. `_delete_cart_rows(old_ids)` — tick each `div[role=row][row-id=…]
   input.ag-checkbox-input` → mass-actions bar (`.o-agGridHeader.-massActions`)
   appears → trash `#DeleteAllCartsButton` → confirm `#DeleteCartConfirmButton`
   ("Yes").
5. Now the name is free: click `#CreateNewCartButton`, fill the name, and — after
   waiting for `#EditCartSaveButton:not([disabled])` (fails fast + clear if it
   stays disabled) — Save. Saving activates the new cart.

Only carts with this **exact** PO name are matched — never a teammate's
differently-named cart. Deletions are reported in the result `warnings`. (ag-grid
virtualizes rows, so this covers same-PO dups in the rendered set — normally one.)

> Carts panel also exposes each cart's list price via `.o-cartPanelPriceRenderer`
> and an active badge (`.o-activeBadge`) / activate toggle
> (`#{cartId}ToggleActiveCartToggleInput`); the mass-actions bar also has
> `#CartSubmissionButton` / `#DuplicateAllCartsButton` / `#CopyAllCartsToButton` /
> `#DownloadAllCartsButton` / `#AnalyticsOfCartsButton` — not used here.

## Step 3 — Checkout: PO + delivery + shipping  ✅ IMPLEMENTED

Navigate to `/adidas/reorder/cart` (opens the **active** cart) and wait for the
header `#CartModule-CartHeader`. The three order settings sit in a row
(`ul.orderSettings--…`). Heading `#CartHeaderHeading` = "My Cart"; the
"This is not a confirmed order" note (`#CartModule-CartHeader-notConfirmedOrder`)
confirms nothing is placed yet.

### Customer PO # (✅ `_set_customer_po`)

| Element | Selector | Notes |
| --- | --- | --- |
| Field | `#CartModule-PersonalReference-InputField input` | **no own id**; `maxlength=18`; **defaults to a random string** that must be cleared + replaced each time |

Driver validates length ≤ 18, `fill()`s the PO (replacing the default), presses
Enter + blurs, then reads `input_value()` back to confirm it stuck.

### Delivery Location (✅ default / saved / one-time)

Dropdown label `#DeliveryAddressOptionsDropdownLabel` shows the current location
(id `6017069000` + name). Defaults to the account preset — **left untouched
unless** a different location or a dropship is requested. Precedence:
`delivery_location_id` > `ship_to` > default.

- **Open** → `#DeliveryAddressOptionsDropdownContent`, containing:
  - a search input (`input[type=search]`; note its id is a dynamic
    `{number}SearchInput`, so target by type within the content),
  - **Add one-time delivery location** button `#DeliveryAddressAddOneTimeShipToButton`,
  - saved options `#Option{locId}` with button `#OptionButton{locId}Button`
    (e.g. `#OptionButton6017069000Button`).
- **Saved** (`_select_saved_location`): open → click `#OptionButton{id}Button`.
- **One-time / dropship** (`_add_one_time_location`): open → click add button →
  modal form `#CartModule-DeliveryAddress-OneTimeShipToAddressForm`:

  | Field | Selector | Maps from `ship_to` |
  | --- | --- | --- |
  | Attention 1* | `#Attention1InputField` | `name` |
  | Attention 2 | `#Attention2InputField` | `attention` |
  | Street Address* | `#StreetInputField` | `address1` (+ `, address2`) |
  | City/Town* | `#CityTownInputField` | `city` |
  | State* (dropdown) | `#StateInputFieldDropdownLabel` | `state` — ⚠️ option markup **not captured** (see below) |
  | ZIP code* | `#ZipcodeInputField` | `zip` |
  | Country | *(static "UNITED STATES")* | fixed US |
  | Submit | `#DeliveryAddressFormSubmitButton` ("USE THIS ADDRESS") | |

  Rules from the form: mandatory fields marked `*`; Latin characters only;
  **PO-Box addresses are cancelled**.

### Shipping Method (✅ `_select_shipping_method`)

Dropdown label `#ShippingMethodsOptionsDropdownLabel` (defaults "Default"). Open →
`#ShippingMethodsOptionsDropdownContent`. Each option is
`<div class="option {CODE}" id="Option{CODE}"><button id="OptionButton{CODE}Button"><span>{label}</span></button>`.
`ship_method` accepts the **4-letter code** (stable id) or the **exact label**:

| Code | Label | | Code | Label |
| --- | --- | --- | --- | --- |
| `DFLT` | Default | | `FED4` | FedEx 3 Day |
| `FDGP` | FedEx Ground | | `FESO` | FedEx Next Business Day |
| `FDGR` | FedEx Ground Residential Only | | `FEDN` | FedEx Next Business Day 10:30 |
| `FEDE` | FedEx 2 Day | | `FEDY` | FedEx Next Business Day Residential Only |
| `FEDZ` | FedEx 2 Day Residential Only | | `FEDB` | FedEx Saturday Delivery |

### State dropdown (✅ `_select_state`)

Inside the one-time-address modal. Label `#StateInputFieldDropdownLabel`; open →
`#StateInputFieldDropdownContent`. Options are
`<button class="m-button -dropdown" id="OptionButton{NameNoSpaces}Button"><span>{Full State Name}</span></button>`
— **full names** ("Tennessee", "New York", "District of Columbia"), plus
territories and Armed Forces entries. `_resolve_state_name` maps a 2-letter
abbreviation (`OR`→Oregon, `TN`→Tennessee, …) to the full name; a full name
passes through. Matched by **exact** text (so "Virginia" ≠ "West Virginia").

Both dropdowns: options are `button.m-button` elements; clicking one selects and
closes. A search input is present but not needed (all options are in the DOM).
`_click_option_by_exact_text` iterates the option buttons and clicks the exact
(case-insensitive whole-string) text match.

## Step 4 — Checkout → calc net price → place order  ✅ IMPLEMENTED

⚠️ Real submit — **no sandbox**; `confirm: true` places a real PO.
`complete_submission()` runs the full sequence and `FINAL_SUBMIT_IMPLEMENTED` is
**True**.

**Sequence (captured controls):**

| # | Action | Selector | Notes |
| --- | --- | --- | --- |
| 4a | **Next** (cart → checkout) | `#CartModuleCheckoutProgressNPCButton` | navigates to `/adidas/reorder/checkout`; **stays inactive until the cart body is scrolled into view** — the driver `_activate_by_scroll`s it (scroll-into-view + nudge + wait-for-enabled) before clicking |
| 4b | **Calc. Net Price** | `#NPCCartSimulation` (`<a role=button>` in the summary-table header; also per row) | **applies our wholesale discounts — MUST run every time and finish before ordering; it is slow** |
| 4c | **Order Now** | `#CartModuleCheckoutProgressBarSubmitOrderButton` | final submit |

**Totals (✅ `_read_checkout_totals`):** after Calc, each order row on the review
page has a net-price cell `#OrderReviewShardTotalsNetPrice{N}` (N = 1-based row
index) whose **first `<span>` is the net price** (e.g. `$35.08`) and second is
the retail comparison (`$45.00`). The driver collects the per-row nets, assigns
each to its result line (`line_total`, positional — review rows follow entry
order), derives `unit_price` = `line_total` ÷ quantity (`_unit_price`), and sums
the nets into `order_total` (`_sum_currency`). Best-effort; never
blocks the order. `total_quantity` is computed from the committed line
quantities (available on dry runs too). `order_total` / per-line `line_total`
only populate on `confirm: true` (they require the Calc step).

**Calc-complete tell (✅ captured, `_await_net_price_calc`):** when 4b finishes,
`#NPCCartSimulation` is replaced by a **"Done!"** message in the summary-table
header cell (`<span class="OrderConfirmationOrderSummaryRunNPCMessageDone--…">Done!</span>`
— class hashed, so match the **text**). The driver waits for the button to
detach and for "Done!" to appear (120s timeout) and **raises without ordering**
if "Done!" never shows — so 4c never fires at list price. The same summary header
also carries TOTAL ORDER PROPOSALS / TOTAL ARTICLES / TOTAL RETAIL PRICE
($45.00) / TOTAL PRICE ($17.54 net) — useful to scrape onto the result later.

**Confirmation (✅ captured):** Order Now **auto-redirects** to
`/adidas/reorder/order/{orderNumber}/confirmation` (e.g. order `25709165`) — no
intermediate confirm dialog. `_read_confirmation_number` parses the number
straight from that URL (`_CONFIRMATION_URL_RE`); `complete_submission` waits for
`**/adidas/reorder/order/*/confirmation` after Order Now. A **Qualtrics feedback
popup** ("rate your experience", NPS 0–10) opens afterward — it is **ignored**
(reading the main page URL is unaffected; no interaction needed).

### Design decisions (locked in the scaffolding)

- Final submit gated behind `confirm: true` (mirrors SanMar's
  `create-purchase-order`) **and** `FINAL_SUBMIT_IMPLEMENTED`.
- `confirm: false` → fill + validate + `dry_run` preview (nothing placed).
- Credentials never hardcoded; env (`ADIDAS_CLICK_*`) or inline stdin JSON.
- Input model: `{po_number (≤18 chars), lines: [{style, size, quantity, color?}],
  ship_to?: {...}, delivery_location_id?, ship_method?, spread_delivery?,
  requested_ship_date?, notes?}` (see `scripts/schemas.py`). `color` is optional
  (the article number encodes it); `spread_delivery` (default false) declines the
  over-availability spread; delivery precedence is
  `delivery_location_id` > `ship_to` > default.

## Inventory / pricing checks (`check-inventory-pricing`)  ✅ IMPLEMENTED

A **read-only lookup** that reuses the ordering steps above and **never places
an order** (there is no `confirm` path). Entry point:
`adidas_browser.check_inventory_pricing()`; tool `adidas_check_inventory_pricing`;
result models `CheckResult` / `CheckLineResult` in `scripts/schemas.py`. **No new
selectors were captured** — it composes the same live-validated steps, so it
inherits their capture. The one refactor: the order flow's `complete_submission`
was split so its cart→checkout→**Calc. Net Price**→read-totals half is a reusable
`price_cart()` that both the order flow (before Order Now) and the pricing check
(before deleting the cart) call.

**Modes (`check` arg):**

| Mode | Path | Cart |
| --- | --- | --- |
| `inventory` | `read_inventory()` — open each product (`_open_product`), read the size-tile inventory indicator via `_classify_size` (the same read the order flow does in `_prepare_lines`), classify `in_stock` / `backorder` / `unavailable`. A blank `size` (or `"*"`/`"all"`) expands to **every** size of the style (iterate `_size_code_map()`). | **None** — reads product pages only. |
| `pricing` | `create_new_cart(po)` → `add_lines(req)` → `fill_checkout(req)` (sets the DO-NOT-BUY Customer PO) → `price_cart()` (Next → Calc. Net Price → `_read_checkout_totals`) → `delete_cart(po)`. Stops **before** `#CartModuleCheckoutProgressBarSubmitOrderButton` (Order Now). | Throwaway; created, priced, deleted. |
| `both` | Same as `pricing`; the per-line inventory indicators read during `add_lines` are surfaced alongside the prices. | Same as `pricing`. |

**Cart cleanup (`delete_cart` → `_delete_carts_named`):** reuses the exact
delete path that `create_new_cart` uses for dedup — it activates a *different*
cart first if the check cart is active (the active cart can't be deleted), then
ticks + trashes + confirms. If the check cart is the account's **only** cart,
the delete can't proceed (nothing to switch to) → `_safe_delete_cart` downgrades
that to a `warning` and sets `cart_deleted=false`; the scary cart name is the
mitigation. Note this leaves the *other* cart active as a mild side effect (the
order flow's dedup already does the same).

**"DO NOT BUY" marker (`_generate_check_po`):** the throwaway cart name **and**
Customer PO get `DO NOT BUY {rand5}` (5 chars from an unambiguous alnum
alphabet, e.g. `DO NOT BUY 7F3K9`, 16 chars). The fuller "AUTOMATED CHECK - DO
NOT PURCHASE - …" can't fit the **18-char** Customer PO limit + the restricted
charset (`_PO_ALLOWED_RE`), so this is the clearest imperative that still leaves
room for the uniqueness suffix. Passes the sanitizer unchanged. Caller may
override via `po_number` (re-sanitized + length-checked).

**Never pauses:** a check deletes its cart and never buys, so `pause` is upgraded
to `order` before `add_lines` — every orderable (incl. backorderable) line gets
a price; flatly `unavailable` sizes are reported price-less. If **all** requested
sizes are unavailable, `add_lines` raises `AdidasConfigError`, which the check
catches and falls back to an inventory-only report (then still deletes the cart).

**Net-price mapping:** `_checkline_results` assigns the review-page nets
(`line_net_prices`, positional over the lines actually entered, i.e. committed
qty > 0) to those lines and derives `unit_price` = net ÷ qty; `order_total` is
their sum. Same positional assumption as the order flow, but filtered to entered
lines so dropped/unavailable lines don't shift the alignment.

---

## Delivery tracking (`get-order-tracking`)  ✅ IMPLEMENTED (live run pending)

A **read-only** walk over a different part of the portal: the order book, an
order's detail page, and its Delivery Tracking table. Shares only **Step 1
(login)** with the ordering flow — no cart, no checkout, no writes. Entry point:
`adidas_browser.get_order_tracking()`; tool `adidas_get_order_tracking`; result
models `TrackingResult` / `TrackingPO` / `TrackingOrder` / `TrackingShipment` in
`scripts/schemas.py`.

**Status:** selectors captured from pasted HTML (order-book row, tracking-link
button, delivery table, article week toggle/header) and the whole flow exercised
end to end against a **local replica** of those pages (multi-order PO, multi-
delivery order, unshipped order, unknown PO, unreadable order). **Not yet run
against the live portal** — watch the first real run, especially the order-book
grid (virtualized rows) and the article toggle's expand/collapse semantics.

### T1 — Order book search (per PO, one PO at a time)

`GET /adidas/reorder/my/order-book?searchText={PO}&page={n}&size=20&filterByRDD=false`

Searching and paging are done **through the URL**, so no search-form or pager
selectors were needed. Pages are walked (`page` 0,1,2…, cap `_ORDER_BOOK_MAX_PAGES`
= 10) until a page returns fewer than `size` rows or adds nothing new.

Captured row (inside an ag-grid cell — the wrapping `id="cell-id-30"` is
positional and **not** used):

```html
<div class="m-orderHeaderData -overview">
  <h2 class="a-heading -s -regular" id="OrderHeaderRow6279266468Heading">6279266468</h2>
  <ul class="m-orderHeaderData__items">
    <li class="m-orderHeaderData__item"><span>P13433</span></li>
    <li class="m-orderHeaderData__item"><div class="a-orderType -reorder">Re-Order</div></li>
  </ul>
</div>
```

| What | Selector |
| --- | --- |
| Row | `div.m-orderHeaderData` (`_ORDER_ROW`) |
| Order number | `h2[id^="OrderHeaderRow"]` text; the id (`OrderHeaderRow{order}Heading`) is the fallback |
| Customer PO | `.m-orderHeaderData__item span` (first) |
| Order type | `.m-orderHeaderData__item .a-orderType` ("Re-Order") |

Two live-site behaviours are handled up front:

- **Virtualized rows** — `_collect_order_rows` scrolls and re-scans, deduping by
  order number, until two consecutive passes add nothing. A PO's *later* orders
  are exactly the ones a tracking lookup must not silently drop.
- **Prefix matches** — adidas's `searchText` also matches PO prefixes (searching
  `P1343` surfaces `P13433` **and** `P13434`). Rows are flagged `exact` on the
  PO cell; only exact ones are tracked, and the rest are reported in a
  `warning` so nobody gets tracking for a PO they did not ask about.

### T2 — Order detail → "has it shipped?"

`GET /adidas/reorder/my/order-book/{order}` (derived from the tracking link's
captured href, which is that path + `/deliveries`).

The **presence** of the Delivery Tracking link is the portal's own "this order
has shipments" tell:

```html
<a class="m-button -tertiary -backButton" id="OrderTrackingButtonLink"
   href="/adidas/reorder/my/order-book/6279266468/deliveries">
  <svg class="a-icon -delivery">…</svg><span class="a-label -large -bold">Delivery Tracking</span></a>
```

`open_order()` polls (`_ORDER_DETAIL_WAIT_MS` 20s) for **either**
`#OrderTrackingButtonLink` (→ shipped) **or** the article rows
(`.o-orderDetailArticle__weekToggle button` → page is up); once the article rows
are up the link still gets a 2s grace window, so a slow render is never read as
"not shipped". If neither appears the order is reported `unreadable` (never
"not shipped") and the run continues with the other orders.

### T3a — Shipped: the Delivery Tracking table

Click the link (falls back to navigating its href /
`/adidas/reorder/my/order-book/{order}/deliveries`), then read one row per
`.o-deliveryTrackingOverview__item`:

| Field | Selector (scoped to the item) |
| --- | --- |
| Delivery note | `a[id^="DownloadPdfCtaLink"]` text (the id repeats across rows — always scope to the item) |
| Ship date | `.o-deliveryTrackingOverview__shipDate` ("Aug 3, 2026") |
| Carrier code | `.o-deliveryTrackingOverview__carrier` ("UPSN") |
| Tracking number + URL | `.m-trackingNumber__trackingNumber a` (text + `href`) |

`carrier_name` is derived from the tracking URL's host (`ups.com` → UPS,
`fedex.com` → FedEx, …) since adidas shows only its own code. One order can have
several deliveries, and **one delivery note can appear on more than one row**
(multiple parcels) — every row is returned, nothing is deduped.

> ⚠️ **The delivery-note PDF link carries a bearer token** in its href
> (`…/download?access_token=Bearer 00D58…`). It is deliberately **not** read or
> returned — only the note number is taken from the link's text.

### T3b — Not shipped: expected ship dates

No tracking link ⇒ nothing has shipped. Each article row has a chevron toggle
that reveals its week list, whose header is the expected ship date:

```html
<div class="o-orderDetailArticle__weekToggle"><button class="m-toggleLabel -isActive">…</button></div>
<header class="o-orderDetailArticle__weekItemHeader">
  <span class="o-orderDetailArticle__weekItemHeaderName">Feb 4, 2027</span></header>
```

`read_expected_ship_dates()` clicks every toggle **that is not already
expanded** — expansion is decided by whether that article already shows a
`…__weekItemHeaderName`, not by the `-isActive` class, whose polarity is not
captured — so the pass is idempotent and cannot collapse an already-open row.

The article **container** (`.o-orderDetailArticle`) is *inferred* from the BEM
block of the two captured elements; it is used only to group dates per article
(and to label them from the block's first `h2, h3, .a-heading`). If it does not
match the live markup, every date found is still returned as one order-level
entry — the dates are never lost, only their per-article grouping.

`expected_ship_date` is the earliest date parsed with `%b %d, %Y` / `%B %d, %Y`,
falling back to the first date shown if the format ever changes.

### Design decisions

- **Read-only, and shaped like the other actions' escalations.** A PO with no
  orders (`not_found`) or an order whose page would not load (`unreadable`)
  flips the result to `needs_confirmation` with the details in `warnings` —
  the same "hand the gap back to the user" contract as `missing_products`.
- **One login, POs looped one at a time** (`po_numbers` is a list, a
  comma/whitespace string, or a single `po_number`; duplicates collapse).
- **A `table` field** (Markdown, PO → order → tracking rows, unshipped rows
  annotated `*(expected)*`) is built server-side so the calling agent hands back
  one consistent table instead of re-deriving one per call.
- **Never guess a shipment.** Expected ship dates are labelled expected in the
  data *and* in the table, and an unreadable order is never reported as "not
  shipped".
