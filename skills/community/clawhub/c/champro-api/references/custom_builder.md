# CHAMPRO Custom Builder

The Custom Builder is CHAMPRO's web-to-print configurator. A shopper embeds it
in an iframe, designs a uniform and enters a roster; saving produces a **Design
Session ID**, which is then the handle for everything else — the roster data,
the proof PDF, the four view renders, and placing the order.

Nothing in PromoStandards describes any of this.

## Two tiers

CHAMPRO documents two embed tiers:

| | Basic | Advanced |
| --- | --- | --- |
| Authentication | not required | required |
| Product customization | yes | yes |
| Order methods (`GetOrderInfo`, `GetFile`) | **no** | yes |
| `PlaceOrder` from a design | **no** | yes |

Advanced is marked "Coming Soon" in the published document. The endpoints are
live — `cb.champrosports.com/api/Order/*` all respond — but entitlement is per
account, so a correctly-keyed call may still be refused. If the `cb-*` actions
return nothing for a session you know exists, ask CHAMPRO whether the account
is provisioned for advanced embedding before debugging the call.

## Embedding

```bash
echo '{"category":"FOOTBALL"}' | python3 scripts/champro.py cb-embed-url
```

Returns the `src` and a ready-made `<iframe>` tag. Twenty-six categories are
bundled in `assets/cb_categories.json`; omit `category` for all of them.

The URL shape is `https://cb.champrosports.com/V2/Index/<id>?Name=<name>&lic=<embed key>`,
with the name percent-encoded (`MEN%27S%20SOCCER`) — the generator reproduces
CHAMPRO's published table exactly, including parameter order.

The embed key travels to the browser in that URL by design. It is a licence
identifier rather than a secret in the way the API Customer Key is, but it does
identify your account, so treat any page carrying it as account-scoped.

### Catching the saved design

The advanced embed posts a message to the parent page when a design is saved.
Listen for it, and keep the session id — it is the only handle to the design:

```html
<script>
window.addEventListener("message", (event) => {
  if (event.data && event.data.sender === "CustomBuilder") {
    // event.data.action === "ProcessDesign" on save
    // event.data.message is the Design Session ID
    cb_callback(event.data.action, event.data.message);
  }
});
</script>
```

Verify `event.origin` against `https://cb.champrosports.com` before trusting
the payload; any page can post a message to yours.

## The session lifecycle

```
design in the iframe
        │  save  →  "ProcessDesign" + Design Session ID
        ▼
  cb-get-design      roster, product, fabric, lead times
        │
        ├─ cb-get-file ProofPdf     → the proof the order needs
        │
        ├─ cb-place-order           → order the design directly
        │
        └─ or: host the proof, then place a REST CUSTOM order
                                      with proof_file_url + the roster
```

Both ordering routes are real. `cb-place-order` is fewer moving parts;
the REST route gives you `validate-order`'s pre-flight, multi-order envelopes
and the sandbox host.

## `cb-get-design`

```bash
echo '{"session_id":"…"}' | python3 scripts/champro.py cb-get-design
```

Returns each cart item with its product, design name, fabric, selected and
available lead times, and the teams/players roster — plus a flattened
`players` list, which is usually what you want when building order lines.

**An empty result is ambiguous.** Verified live: CHAMPRO returns a bare `[]`
with HTTP 200 for an unknown session id, a wrong embed key, *and* a design that
genuinely has no items. There is no error field to distinguish them. The action
reports `resolved: false` with an explicit note rather than "0 items", because
reporting an auth failure as an empty design is how you end up ordering
nothing and thinking it worked.

## `cb-get-file`

```bash
echo '{"session_id":"…","file_type":"ProofPdf"}' | python3 scripts/champro.py cb-get-file
```

| `file_type` | Extension |
| --- | --- |
| `ProofPdf` | pdf |
| `FrontImage` | png |
| `BackImage` | png |
| `LeftImage` | png |
| `RightImage` | png |

(CHAMPRO's own example labels the `FrontImage` button `'pdf'`; the renders are
images. The extensions above are what this skill writes.)

An unknown session id and a wrong embed key both produce a 404 — the action
says so rather than guessing which.

**The download URL is not a `ProofFileURL`.** A REST CUSTOM order's
`proof_file_url` is fetched by CHAMPRO server-side, and the `GetFile` URL
carries your embed key. Download the proof, host it somewhere publicly
reachable, and pass that URL.

## `cb-place-order`

```bash
echo '{
  "session_id": "…",
  "po_number": "PO-1234",
  "lead_time_id": "EX",
  "ship_to": {
    "first_name": "…", "last_name": "…",
    "address1": "…", "city": "…", "state": "IL", "zip": "60007",
    "phone": "…", "is_residential": true
  },
  "confirm": true
}' | python3 scripts/champro.py cb-place-order
```

Same two gates as `place-order`: `confirm` decides whether anything is sent,
`production` whether it is real. Unlike the REST API, the Custom Builder picks
its environment with an `IsSandBox` boolean on the same URL, so `production:
false` (the default) sets `IsSandBox: true`.

`lead_time_id` is the `LeadTimeId` from `cb-get-design`
(`selected_lead_time.lead_time_id`, e.g. `"EX"`) — **not** the `LeadTimeName`
that a REST CUSTOM order takes. Different field, different vocabulary.

The ship-to uses the Custom Builder's own spelling — `Address1`, `Zip`, `State`,
and `IsResidential` as the *string* `"true"`/`"false"` — which differs from the
REST order's `Address`, `ZIPCode`, `StateCode` and integer flag. `schemas.py`
keeps the two types apart so neither leaks into the other.

On success: `Result: "OK"`, an `Order` number, and a
`ValidatedShippingAddress`. On failure: `Result: "Error"` with a `Message` and
a two-digit `MessageCode` — run it through
`echo '{"code":"06"}' | python3 scripts/champro.py explain-error`.

CHAMPRO does not verify the address itself and requires it to satisfy UPS
address rules; failing that is error 06 or 24.
