---
name: Finix JS
description: |
  Finix.js integration for accepting card and ACH bank payments on the web. Embed the hosted payment form, tokenize card/bank data in the browser, and claim tokens server-side to create Buyer Identities, Payment Instruments, and Transfers/Authorizations via the Finix Payments API.
  Use this skill when users want to accept payments on their website with Finix, set up a Finix checkout, tokenize card/bank details, or wire up the server-side token-exchange and charge flow.
metadata:
  author: finix
  version: "1.0"
  clawdbot:
    emoji: 💳
    homepage: "https://finix.com"
    requires:
      env:
        - FINIX_USERNAME
        - FINIX_PASSWORD
        - FINIX_APPLICATION_ID
        - FINIX_MERCHANT_ID
---

# Finix.js Integration Skill

This document teaches how to integrate **Finix.js** into a customer website to accept card and bank (ACH) payments via Finix. It covers the Finix APIs involved, the account/application setup required, and the steps to embed and use the library.

---

## 1. What Finix.js Is

Finix.js is a client-side, hosted payment form. It injects an iframe into the merchant's page that collects sensitive PCI/NACHA data (card number, expiration, security code, bank account/routing numbers) and exchanges it directly with the Finix Payments API for a single-use **token**. The merchant's backend then uses that token to create a reusable **Payment Instrument** and charge the customer via **Transfer** or **Authorization** API calls. Because raw card/bank data never hits the merchant's servers, this flow keeps cards in SAQ-A PCI scope, and is the only supported pattern for Finix web integrations.

---

## 2. Prerequisites: Finix Account Setup

Before writing any code, the merchant must have:

1. **A Finix account** (Dashboard access at `https://finix.payments-dashboard.com/`).
2. **An Application ID** (`APxxxxxxxxxxxxxxxxxxxxxx`). This identifies the platform/application that owns the tokens. It is passed to `Finix.PaymentForm(...)`. Application IDs are **environment-scoped** — sandbox and production IDs are different.
3. **A Merchant ID** (`MUxxxxxxxxxxxxxxxxxxxxxx`). This represents the entity being paid. Needed server-side when creating Authorizations/Transfers, and client-side if using `Finix.Auth` for fraud session tracking.
4. **API credentials** (username + password used as HTTP Basic Auth). These are **server-side only** — never ship them to the browser.

### Environments

| Environment string | Payments API host |
|---|---|
| `prod` / `production` / `live` | `https://finix.live-payments-api.com` |
| `sandbox` / `sb` | `https://finix.sandbox-payments-api.com` |

Always build/test in sandbox first. Switching to prod is a one-line change (environment string + Application ID).

---

## 3. The End-to-End Payment Flow

1. The merchant page loads `finix.js` and calls `Finix.PaymentForm(...)`, which mounts an iframe into a container `<div>`.
2. The buyer enters card or bank data into the iframe's inputs.
3. On submit, the iframe POSTs the sensitive data directly to the Finix Payments API at `/applications/:app_id/tokens` and receives a single-use token (`TKxxxx...`).
4. The token (plus a `fraud_session_id` from `Finix.Auth` and any checkout context) is POSTed to the **merchant's backend**.
5. The backend uses server-side API credentials to create a Buyer Identity, exchange the token for a Payment Instrument, and create a Transfer or Authorization (see "Server-Side: Claiming the Token" below).

Finix.js handles steps 1–3. Steps 4–5 are the merchant's responsibility.

---

## 4. Embedding Finix.js

### 4a. Minimal integration

```html
<div id="finix-form"></div>
<script src="https://js.finix.com/v/2/finix.js"></script>
<script>
  const form = Finix.PaymentForm(
    "finix-form",                 // container: id string OR an HTMLElement
    "sandbox",                    // environment
    "APgPDQrLD52TYvqazjHJJchM",   // Application ID
    {
      onSubmit: (error, response) => {
        if (error) {
          console.error(error);
          return;
        }
        const token = response.data.id; // "TKxxxx..."
        // POST token to your backend to finish the charge.
        fetch("/api/charge", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ...paymentData, token }), // include other checkout data (amount, currency, buyer info, cart id, etc.)
        });
      },
    }
  );
</script>
```

The library attaches `window.Finix` on load and exposes:

- `Finix.PaymentForm(element, env, applicationId, options)` — renders card + bank form (default is cards only; enable bank via `paymentMethods: ['card', 'bank']`).
- `Finix.Auth(env, merchantId, callback)` — initializes Sift fraud session tracking (see "Fraud Session" below).
- Aliases: `Finix.TokenForm`, `Finix.CardTokenForm`, `Finix.BankTokenForm` all delegate to `PaymentForm`.

`element` may be either an element ID (string) or an `HTMLElement` — the latter is required when mounting inside a Shadow DOM / web component.

### 4b. The form instance

`PaymentForm` returns an instance with:

- `form.submit((error, response) => {...})` — trigger tokenization from a custom button. See "Custom submit button" below.
- `form.theme(themeName)` — swap theme at runtime.

---

### 4c. Options Reference

Pass as the 4th argument to `PaymentForm`. All are optional. This section is the longest because options are where most integrations get stuck — read carefully before customizing.

#### 4c.1 Quick index

| Option | Type | Default | Purpose |
|---|---|---|---|
| `paymentMethods` | `('card' \| 'bank')[]` | `['card']` | Which payment method tabs to render. |
| `showAddress` | `boolean` | `false` | Show the billing address section. |
| `showLabels` | `boolean` | `true` | Render field `<label>` elements above inputs. |
| `labels` | `Record<field, string>` | `{}` | Override default label text per field. |
| `showPlaceholders` | `boolean` | `true` | Render input placeholders. |
| `placeholders` | `Record<field, string>` | `{}` | Override placeholder text per field. |
| `hideFields` | `string[]` | `[]` | Hide specific fields (deep dive below). |
| `requiredFields` | `string[]` | `[]` | Force normally-optional fields to be required (deep dive below). |
| `requireSecurityCode` | `boolean` | `true` | Require CVV/CVC on cards. |
| `confirmAccountNumber` | `boolean` | `true` | Require bank account number to be typed twice. |
| `hideErrorMessages` | `boolean` | `false` | Suppress inline error text (fields still validate). |
| `errorMessages` | `Record<field, string>` | `{}` | Custom inline error copy per field. |
| `hidePotentialIssueMessages` | `boolean` | `false` | Hide soft "are you sure?" warnings (e.g. unusual card length). |
| `defaultValues` | `Record<field, string>` | `{}` | Prefill non-sensitive fields (deep dive below). |
| `enableDarkMode` | `boolean` | `false` | Respect `prefers-color-scheme: dark`. |
| `theme` | `string` | `'finix'` | Brand preset (deep dive below). |
| `styles` | `StylesCfg` | `{}` | Per-state CSS overrides (deep dive below). |
| `fonts` | `Array<{fontFamily,url,format}>` | `[]` | Inject custom `@font-face` rules (deep dive below). |
| `submitLabel` | `string` | `'Submit'` | Built-in submit button label. |
| `plaidLinkSettings` | `{ displayName, language, countries }` | — | Enable Plaid embedded bank linking (see "Plaid Bank Linking" below). |
| `onLoad` | `() => void` | — | Fires when the iframe has mounted and initialized. |
| `onUpdate` | `(state, binInfo, hasErrors) => void` | — | Fires on every field change. |
| `onSubmit` | `(error, response) => void` | — | Fires after tokenization completes. |

#### 4c.2 The complete field name list

Every option that takes a field-keyed record (`labels`, `placeholders`, `hideFields`, `requiredFields`, `errorMessages`, `defaultValues`) uses the same set of canonical field names. Use these **exactly** — arbitrary keys are silently ignored.

| Section | Field name | Notes |
|---|---|---|
| Card | `card_holder_name` | Cardholder name. Optional by default. |
| Card | `number` | Card number. Always required when card is active. |
| Card | `expiration_date` | MM/YY. Always required when card is active. |
| Card | `security_code` | CVV/CVC. Required unless `requireSecurityCode: false` or `hideFields: ['security_code']`. |
| Bank (USA + CAN) | `account_holder_name` | Account holder name. **Required by default when bank is active.** |
| Bank (USA + CAN) | `account_number` | Account number. Required when bank is active. |
| Bank (USA + CAN) | `account_type` | `PERSONAL_CHECKING \| PERSONAL_SAVINGS \| BUSINESS_CHECKING \| BUSINESS_SAVINGS`. Required when bank is active. |
| Bank (USA) | `bank_code` | US ABA routing number (9 digits). Required when country is `USA`. |
| Bank (CAN) | `transit_number` | 5-digit transit. Required when country is `CAN`; replaces `bank_code`. |
| Bank (CAN) | `institution_number` | 3-digit institution. Required when country is `CAN`; replaces `bank_code`. |
| Address | `address_line1` | Street. |
| Address | `address_line2` | Apt/suite. |
| Address | `address_city` | City. |
| Address | `address_region` | State/province. Dropdown is auto-populated for USA/CAN. |
| Address | `address_country` | Dropdown; dictates bank field set and postal-code format. |
| Address | `address_postal_code` | ZIP (US: `12345` or `12345-6789`) / postal code (CAN: `A1A 1A1`). |

#### 4c.3 `paymentMethods`

```js
paymentMethods: ['card']            // card only (default)
paymentMethods: ['bank']            // ACH/bank only
paymentMethods: ['card', 'bank']    // tabs for both
```

When both are present, a tab bar appears and the user chooses. The active method determines which required fields are enforced. Bank fields **vary by `address_country`** — selecting `CAN` swaps `bank_code` for `transit_number` + `institution_number`.

#### 4c.4 `hideFields` (deep dive)

Removes a field from the DOM and from validation. The tokenization payload simply omits it.

**Fields that are safe to hide:**

- `card_holder_name` — optional for cards.
- `account_holder_name` — hideable for bank; if hidden the default-required check is skipped for it.
- `security_code` — equivalent to setting `requireSecurityCode: false`; produces a token without CVV, but many issuers will decline the downstream charge. Only hide if your Finix account/use-case permits card-on-file without CVV.
- Any `address_*` field — all address fields are optional at the tokenization layer. To hide the entire address section at once, prefer `showAddress: false` (or simply omit it — `false` is the default).

**Fields you should NOT hide** (will break tokenization):

- `number`, `expiration_date` — required to mint a card token.
- `account_number`, `account_type`, and `bank_code` (USA) / `transit_number`+`institution_number` (CAN) — required to mint a bank token.

**Common hide patterns:**

```js
// Show address but skip the optional second line
hideFields: ['address_line2'],

// CVV-less card-on-file
hideFields: ['security_code'],

// Drop name fields (name captured elsewhere in your checkout)
hideFields: ['card_holder_name', 'account_holder_name'],
```

If the user hides a field that was also listed in `requiredFields`, the hide wins — the field does not render and is not validated.

#### 4c.5 `requiredFields` (deep dive)

**What it does:** promotes a normally-optional field to required. It does **not** add fields that aren't already rendering — you still need `showAddress: true` (or no matching `hideFields` entry) for address fields to appear.

**Fields that are already required by default** (no need to list them):

- Card: `number`, `expiration_date`, `security_code` (unless `requireSecurityCode: false`).
- Bank (USA): `account_holder_name`, `account_number`, `bank_code`, `account_type`.
- Bank (CAN): `account_holder_name`, `account_number`, `transit_number`, `institution_number`, `account_type`.

**Fields you can add to `requiredFields`:**

- `card_holder_name`
- `account_holder_name` (redundant for bank — already required by default)
- `name` — legacy alias that maps to `card_holder_name` or `account_holder_name` depending on the active payment method. Prefer the explicit names in new code.
- `address_line1`, `address_line2`, `address_city`, `address_region`, `address_country`, `address_postal_code`

Anything else is silently dropped (only the list above is honored).

**Interactions to be aware of:**

- `requireSecurityCode: false` + `requiredFields: ['security_code']` — the `requiredFields` entry is **not** honored for `security_code`. Use `requireSecurityCode` as the switch.
- `hideFields` + `requiredFields` for the same field — hide wins.
- `confirmAccountNumber: true` (default) implicitly requires `account_number_confirmation` when bank is active; you don't list it manually.

**Typical billing-address collection for AVS/fraud checks:**

AVS itself only evaluates `address_line1` + `address_postal_code`, but most merchants collect the full address for records and fraud scoring:

```js
showAddress: true,
requiredFields: [
  'address_line1',
  'address_city',
  'address_region',
  'address_postal_code',
  // address_country is a dropdown with a default, so it's not strictly needed here
],
```

For a minimal AVS-only setup:

```js
showAddress: true,
hideFields: ['address_line2', 'address_city', 'address_region', 'address_country'],
requiredFields: ['address_line1', 'address_postal_code'],
```

#### 4c.6 `defaultValues` (deep dive)

Prefills non-sensitive fields so the buyer doesn't retype data your checkout already has.

**Allowed fields:**

- `card_holder_name`, `account_holder_name`
- `address_line1`, `address_line2`, `address_city`, `address_region`, `address_country`, `address_postal_code`

**Never prefill** (the iframe ignores these even if passed):

- `number`, `expiration_date`, `security_code` — would break PCI scope.
- `account_number`, `bank_code`, `transit_number`, `institution_number` — would break NACHA scope.

**Format requirements:**

- `address_country` → ISO-3 alpha codes (`'USA'`, `'CAN'`, `'GBR'`, …). The dropdown's list comes from `countryNamesOptions` and is ACH-restricted to `USA`/`CAN` when bank is the active method.
- `address_region` → two-letter state/province abbreviation for US (`'CA'`, `'NY'`) and CAN (`'ON'`, `'BC'`). Other countries: free text.
- `address_postal_code` → already-formatted string (`'94105'`, `'94105-1234'`, `'M5V 3L9'`). The formatter will re-normalize input, but passing the canonical form avoids confusing the buyer.

**Example:**

```js
defaultValues: {
  card_holder_name: 'Ada Lovelace',
  address_line1: '50 Beale St',
  address_line2: 'Suite 600',
  address_city: 'San Francisco',
  address_region: 'CA',
  address_country: 'USA',
  address_postal_code: '94105',
},
```

#### 4c.7 `theme` vs `styles`

`theme` is a preset that changes the whole form's look (colors, borders, button). `styles` is a targeted override on top of whichever theme is active. Use `theme` for brand-alignment, then nudge with `styles`.

Built-in themes: `finix` (default), `amethyst`, `sapphire`, `topaz`, `ruby`, `emerald`, `midnight`, `elevated`. Switch at runtime via `form.theme('ruby')`.

#### 4c.8 `styles` (deep dive)

`styles` is an object with two top-level branches — `default` (always applied) and `dark` (applied only when `enableDarkMode` is on **and** the user/browser is in dark mode; merged *over* `default`).

Under each branch, each target element exposes a set of **states**. States are also applied additively in this order: `default` → `success` (if valid) → `error` (if invalid & errors shown) → `focused` (if focused).

**Full shape:**

```js
styles: {
  default: {
    form: {
      default: { /* container around entire form */ },
    },
    section: {
      default: { /* each section wrapper (card/bank/address) */ },
    },
    sectionHeader: {
      default: { /* section heading text */ },
      focused: { /* when a field inside is focused */ },
    },
    input: {
      default: { /* all inputs */ },
      success: { /* input with valid value */ },
      error:   { /* input with validation error and showErrors=true */ },
      focused: { /* input while focused */ },
    },
    submitButton: {
      default:  { /* built-in submit button */ },
      disabled: { /* when the form has errors */ },
    },
  },
  dark: {
    // same tree — these get merged on top of `default` when dark is active
    input: { default: { /* ... */ } },
    // ...
  },
},
```

**Values are camelCased CSS strings** (same as React/inline style objects), not CSS declarations. Use string values everywhere, including numeric-looking ones:

```js
input: {
  default: {
    border: '1px solid #7D90A5',
    borderRadius: '12px',
    padding: '12px 14px',
    fontSize: '16px',
    fontFamily: '"Effra", sans-serif',
  },
  focused: {
    border: '1px solid #3B82F6',
    boxShadow: '0 0 0 3px rgba(59,130,246,0.2)',
  },
  error: {
    border: '1px solid #DC2626',
    color: '#DC2626',
  },
  success: {
    border: '1px solid #16A34A',
  },
},
```

**State precedence example.** An input that is both focused and in error ends up with the merge `default → error → focused`. So if both define `border`, `focused` wins. To force error styling to trump focus, re-declare `border` inside the error block of the `dark`/`default` tree, or move the style onto `outline` so they don't collide.

**Dark mode notes.** `dark` only applies when you set `enableDarkMode: true`. Everything inside `dark` is a **patch** over `default` — you don't have to redeclare unchanged rules.

**What you can't do.** You can't inject arbitrary CSS, pseudo-classes (`:hover`), or selectors. If you need hover styles or animation, do it by adjusting `default`/`focused` or filing a feature request.

#### 4c.9 `fonts`

Injects `@font-face` rules into the iframe so the CSS `fontFamily` values in `styles` actually resolve. Each font object:

```js
fonts: [
  {
    fontFamily: 'Effra',
    url: 'https://cdn.example.com/fonts/effra.woff2',
    format: 'woff2',
  },
],
```

**Constraints enforced by the iframe:**

- `url` **must** be served over `https://` — anything else is rejected with a console warning.
- `format` must be one of `woff`, `woff2`, `truetype`, `opentype`, `embedded-opentype`, `svg`.
- `fontFamily` is sanitized (strips anything that isn't word/space/comma/hyphen) to prevent CSS injection.

After the font is loaded, reference it in `styles` via the sanitized family name: `fontFamily: '"Effra", sans-serif'`.

#### 4c.10 Error messages

Two independent switches:

- `hideErrorMessages: true` — hides inline error text. Fields still validate and the form still blocks submission; you just don't show the red copy.
- `errorMessages: { field: 'custom string' }` — per-field override. Still only shown when `hideErrorMessages` is false. The keys match the canonical field names listed in "The complete field name list" above.

`hidePotentialIssueMessages: true` suppresses the soft warnings like "This Visa number is valid, but Visa typically issues 13 or 16 digit cards…" without affecting hard validation.

#### 4c.11 Callbacks

```js
onLoad: () => { /* iframe mounted & initialized */ },

onUpdate: (state, binInfo, hasErrors) => {
  // state     — { [fieldName]: { value, errors, isDirty, isFocused, ... } }
  // binInfo   — { cardBrand, bin } once enough digits are entered
  // hasErrors — true while any required/invalid field blocks submission
  // Typical use: enable/disable your custom submit button.
},

onSubmit: (error, response) => { /* see "The onSubmit Response" below for shape */ },
```

Callbacks live on the parent and are invoked in response to iframe messages — they are stripped from the options object before it crosses the postMessage boundary.

### 4d. Custom submit button

Omit the built-in button by providing your own and calling `form.submit`:

```html
<div id="finix-form"></div>
<button id="pay-btn" disabled>Pay</button>
<script>
  const form = Finix.PaymentForm("finix-form", "sandbox", "APxxx...", {
    onUpdate: (_state, _bin, hasErrors) => {
      document.getElementById("pay-btn").disabled = hasErrors;
    },
  });

  document.getElementById("pay-btn").addEventListener("click", () => {
    form.submit((error, response) => {
      if (error) return handleError(error);
      sendTokenToBackend(response.data.id);
    });
  });
</script>
```

Note: do **not** wrap `#finix-form` in a `<form>` element whose submit you also handle — the library manages its own submission via postMessage to the iframe.

---

## 5. The onSubmit Response

```js
onSubmit: (error, response) => {
  if (error) {
    // error.data?.message — human-readable
    // error.data?._embedded?.errors — per-field validation errors from Finix
    return;
  }
  const tokenData = response.data;
  // tokenData.id          → "TKxxxxxxxxxxxxxxxxxxxxxx" (single-use, 30 days)
  // tokenData.fingerprint → stable hash of the payment method
  // tokenData.instrument  → "PAYMENT_CARD" | "BANK_ACCOUNT"
  // tokenData.expires_at  → ISO timestamp
  const token = tokenData.id; // what you forward to your backend
};
```

**Tokens are single-use and expire in ~30 days.** The merchant's server should exchange the token for a persistent Payment Instrument immediately after receiving it (see "Server-Side: Claiming the Token" below).

---

## 6. Plaid Bank Linking (optional)

Instead of (or in addition to) manual routing + account entry, merchants can enable Plaid Link for ACH. Add `plaidLinkSettings` to options and make sure `paymentMethods` includes `'bank'`:

```js
Finix.PaymentForm("finix-form", "sandbox", "APxxx...", {
  paymentMethods: ['card', 'bank'],
  plaidLinkSettings: {
    displayName: 'Acme Corp',
    language: 'en',
    countries: ['USA', 'CAN'],
  },
  onSubmit: (err, res) => { /* ... */ },
});
```

When the user successfully links an account via Plaid, the library posts a `third_party_token` payload instead of raw bank fields. The returned token is used exactly like a normal token on the server side.

---

## 7. Fraud Session (Finix.Auth)

For card and bank payments Finix recommends initializing a Sift fraud session tied to the Merchant ID. This produces a `sessionKey` (`fraud_session_id`) that must be forwarded to the backend and attached to the Authorization/Transfer request.

```js
const auth = Finix.Auth("sandbox", "MUxxxxxxxxxxxxxxxxxxxxxx", (sessionKey) => {
  // Stash it; attach to the payload when creating an Authorization/Transfer server-side.
  window.__finixFraudSessionId = sessionKey;
});
```

Important: `Finix.Auth` takes the **Merchant ID**, not the Application ID. The supported environment strings are the same ones in the prerequisites table above (`sandbox`/`sb` and `prod`/`production`/`live`).

---

## 8. Server-Side: Claiming the Token and Charging the Customer

Everything above this section happens in the browser. Once the merchant's backend receives the token (`TKxxxx...`), it has **30 days** to claim it. The backend does this in three steps:

1. **Create (or reuse) a Buyer Identity** → `IDxxxx...`
2. **Create a Payment Instrument** from the token + Identity → `PIxxxx...` (this *claims* the token)
3. **Create a Transfer** (a sale/debit) — or an Authorization if you want to capture later — using the Payment Instrument as the `source` and the Merchant ID as `merchant`.

Transfers are the most common path (one-step sale). Authorizations follow the same pattern but require a separate capture call afterwards.

All requests use HTTP Basic Auth with a server-side API key pair and must include the `Finix-Version` header.

### 8a. (Optional) Create a Buyer Identity

Skip this step if you already have an Identity for this buyer — Identities are reusable and can be updated later via `PUT`.

You can create a fully-populated Identity, or an empty one with just `identity_roles` and `type` — both are valid. Populating it up front avoids asking the buyer for the same info later.

```bash
curl -i -X POST \
  -u USfdccsr1Z5iVbXDyYt7hjZZ:313636f3-fac2-45a7-bff7-a334b93e7bda \
  https://finix.sandbox-payments-api.com/identities \
  -H 'Content-Type: application/json' \
  -H 'Finix-Version: 2022-02-01' \
  -d '{
    "entity": {
      "phone": "7145677613",
      "first_name": "John",
      "last_name": "Smith",
      "email": "finix_example@finix.com",
      "personal_address": {
        "line1": "741 Douglass St",
        "line2": "Apartment 7",
        "city": "San Mateo",
        "region": "CA",
        "postal_code": "94114",
        "country": "USA"
      }
    },
    "identity_roles": ["BUYER"],
    "tags": { "key": "value" },
    "type": "PERSONAL"
  }'
```

Response contains `"id": "IDxxxx..."` — keep it for step 8b.

### 8b. Create a Payment Instrument (claims the token)

This is the step that **claims the token**. The token becomes a persistent, reusable Payment Instrument tied to the buyer's Identity. Once claimed, the original `TK...` is consumed; future charges use the returned `PI...`.

```bash
curl -i -X POST \
  -u USfdccsr1Z5iVbXDyYt7hjZZ:313636f3-fac2-45a7-bff7-a334b93e7bda \
  https://finix.sandbox-payments-api.com/payment_instruments \
  -H 'Content-Type: application/json' \
  -H 'Finix-Version: 2022-02-01' \
  -d '{
    "token": "TKiMxe323RE5Dq3wLVtG8kSW",
    "type": "TOKEN",
    "identity": "IDjvxGeXBLKH1V9YnWm1CS4n"
  }'
```

Example response (card):

```json
{
  "id": "PImmCg3Po7oNi7jaZcXhfkEu",
  "application": "APgPDQrLD52TYvqazjHJJchM",
  "identity": "IDgWxBhfGYLLdkhxx2ddYf9K",
  "instrument_type": "PAYMENT_CARD",
  "brand": "MASTERCARD",
  "card_type": "DEBIT",
  "last_four": "8210",
  "expiration_month": 12,
  "expiration_year": 2029,
  "fingerprint": "FPRiCenDk2SoRng7WjQTr7RJY",
  "enabled": true,
  "currency": "USD",
  "address": { "line1": "900 Metro Center Blv", "city": "San Francisco", "region": "CA", "postal_code": "94404", "country": "USA" }
}
```

The `id` (`PImmCg3Po7oNi7jaZcXhfkEu`) is the `source` you'll use in step 8c.

### 8c. Create a Transfer (most common: one-step sale)

This actually moves the money. `amount` is in the currency's minor units (cents for USD).

```bash
curl -i -X POST \
  -u USfdccsr1Z5iVbXDyYt7hjZZ:313636f3-fac2-45a7-bff7-a334b93e7bda \
  https://finix.sandbox-payments-api.com/transfers \
  -H 'Content-Type: application/json' \
  -H 'Finix-Version: 2022-02-01' \
  -d '{
    "amount": 662154,
    "currency": "USD",
    "merchant": "MUmfEGv5bMpSJ9k5TFRUjkmm",
    "source": "PI6iQcTtJNCS8GZAVKYi5Ueb",
    "tags": { "test": "Sale" }
  }'
```

Fields:

- `merchant` — the Merchant ID being paid (the same `MU...` used in `Finix.Auth`).
- `source` — the Payment Instrument ID from step 8b.
- `amount` — integer in minor units. `662154` = `$6,621.54`.
- `fraud_session_id` — (recommended) the `sessionKey` returned by `Finix.Auth` in the browser (see "Fraud Session" above).
- `tags` — arbitrary metadata for your own reporting.

### 8d. Authorizations (when you need to capture later)

Identical structure to Transfers, but posted to `/authorizations`. They place a hold on funds without capturing. Call `POST /authorizations/:id/capture` (or `void`) to finish. Use this for workflows like "authorize at checkout, capture on ship." For most use cases — e-commerce sales, one-click pay — **a Transfer is what you want**.

### 8e. What lives where

| Concern | Location | Credential |
|---|---|---|
| Collect card/bank | Browser (iframe) | Application ID (public) |
| Tokenize (`TK...`) | Browser → Finix | Application ID |
| Create Identity, Payment Instrument, Transfer/Authorization | **Server only** | API username + password |
| Webhooks (dispute, settlement, etc.) | Server | Verify signature |

**Never** put the API username/password into `finix.js` or any browser-delivered bundle. The `US...:...` credentials shown above are public Finix sandbox test keys — safe to copy for local experiments, but replace with your own for live traffic.

---

## 9. Integration Checklist

- [ ] Sandbox Application ID and Merchant ID obtained from Finix Dashboard.
- [ ] `finix.js` script tag added; container `<div>` present in the DOM before the script runs.
- [ ] `PaymentForm` called with correct environment + Application ID.
- [ ] `onSubmit` (or custom-button `form.submit`) wired to a backend endpoint.
- [ ] Backend exchanges token → Payment Instrument → Authorization/Transfer using server-side API credentials.
- [ ] `Finix.Auth` initialized with the Merchant ID; `sessionKey` forwarded to backend and included as `fraud_session_id`.
- [ ] Tested in sandbox with Finix test cards (e.g. `4111 1111 1111 1111`) and test bank routing numbers before swapping to live environment + live Application ID.
- [ ] Merchant page served over HTTPS in production (Finix enforces this for the iframe).

---

## 10. References

- Finix.js tokenization guide: https://docs.finix.com/guides/online-payments/payment-tokenization/tokenization-forms
- Create an Identity (Buyer): https://docs.finix.com/api/identities/createidentity
- Create a Payment Instrument (claims the token): https://docs.finix.com/api/payment-instruments/createpaymentinstrument
- Create a Transfer (one-step sale): https://docs.finix.com/api/transfers/createtransfer
- Create an Authorization (auth + later capture): https://docs.finix.com/api/authorizations/createauthorization
