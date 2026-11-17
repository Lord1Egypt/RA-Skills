# Destination specifics

Per platform details for building a flow's action config. Always confirm the current schema with `converly actions <destination_type>`, it returns the field list plus a copy ready `config_example`.

Two families of destination:

- **Connected destinations** fire server side (and browser side) and need the connect handoff first: `google-ads`, `meta`, `google-analytics`, `linkedin-ads`, `tiktok-ads`, `reddit-ads`. These are the high value ones (Enhanced Conversions, CAPI).
- **Browser side destinations** need NO connection at all. The visitor's browser fires the platform's own pixel, which must already be installed on the site: `microsoft-ads`, `x-ads`, `pinterest-ads`, `snapchat-ads`, `adroll`, `taboola`, `plausible-analytics`, `fathom-analytics`, `gosquared`, `simple-analytics`, `pirsch-analytics`. Skip the connect step entirely for these.

## Google Ads (`google-ads`)

- Connect via handoff (OAuth in the user's browser).
- The flow action fires a specific **conversion action** that must already exist in the Google Ads account. Pick it from `converly destinations conversions google-ads` and put its `id` in the config (`--conversion-id`).
- If the list is empty, the user creates one in Google Ads (Goals → Conversions → New conversion action → Website, then "conversion created manually with code"), then re-list with `--refresh`.
- `enhancedConversions` defaults to true. It sends hashed first party data (email) alongside the conversion, which improves match rates. Leave it on unless the user objects.
- Google requires the account to have accepted the Customer Data Terms for Enhanced Conversions to work. If test events succeed but Google reports no enhanced data, that acceptance (in Google Ads settings) is the usual culprit.
- Conversions attribute via the GCLID captured when the visitor clicked the ad. Organic visits carry no GCLID, so a form fill without an ad click still records in Converly but cannot attribute in Google Ads. Expected behaviour, not a bug.

Config shape:

```json
{
  "conversion": { "id": "7083752309", "name": "Signed Up", "value": 50, "currency": "USD" },
  "enhancedConversions": true
}
```

## Meta Ads (`meta`)

- Connect via handoff. The popup offers both OAuth and a paste token path; the user picks inside the popup.
- The action fires a **pixel event by name**. Standard events: `Lead`, `CompleteRegistration`, `Purchase`, `Contact`, `SubmitApplication`, `Schedule`, `StartTrial`, `Subscribe`. Use `--event-name Lead` with `is_custom: false` (the CLI default). For a custom named event pass `--event-name MyEvent --custom`.
- Delivery is dual: browser pixel plus server side CAPI with event deduplication. That is why connecting matters even though Meta has a browser pixel.
- Testing: get a test code from Meta Events Manager → Test events, pass it as `--meta-code TEST12345`. The test conversion then appears in that tab instantly instead of mixing with real data.

Config shape:

```json
{
  "conversion": { "event_name": "Lead", "is_custom": false, "value": 100, "currency": "USD" }
}
```

## Google Analytics 4 (`google-analytics`)

- Connect via handoff (OAuth, or paste a Measurement ID `G-XXXX` plus API secret inside the popup).
- The action fires a GA4 event by name (`generate_lead` is the conventional one for form fills). Use `--event-name generate_lead`.
- To make it count as a conversion in GA4 reports, the user marks that event as a key event in GA4 Admin. Mention this.

## LinkedIn Ads (`linkedin-ads`)

- Connect via handoff (paste token path inside the popup).
- Fires a specific conversion rule, picked exactly like Google Ads conversions:

```
converly destinations conversions linkedin-ads
converly flows create --site site_XXXX --name "Leads to LinkedIn" \
  --trigger generic-form --destination linkedin-ads --conversion-id <id from the list>
```

## TikTok Ads (`tiktok-ads`) and Reddit Ads (`reddit-ads`)

- Connect via handoff first.
- Then run `converly actions tiktok-ads` (or `reddit-ads`) and build the flow from its `config_example`. The pattern is always the same, only the config differs:

```
converly actions tiktok-ads
converly flows create --json '{
  "site_id": "site_XXXX",
  "name": "Leads to TikTok",
  "trigger_config": { "integrationId": "generic-form", "pageFilter": "all" },
  "actions_config": [{ "id": "act-1", "integrationId": "tiktok-ads",
    "config": <the config_example from converly actions, with your values> }]
}'
```

Do not guess config field names for these destinations. Copy `config_example` and substitute values.

## Browser side pixels (no connection)

For `microsoft-ads`, `x-ads`, `pinterest-ads`, `snapchat-ads`, `adroll`, `taboola`, `plausible-analytics`, `fathom-analytics`, `gosquared`, `simple-analytics`, `pirsch-analytics`:

- No connect step (`converly destinations connect` will refuse and tell you so). Run `converly actions <type>`, build the flow with its `config_example` via `--json` exactly as in the TikTok example above, publish, done.
- The platform's own base pixel must already be installed on the site. Converly tells the pixel to fire the conversion; it does not install the pixel. If you have page access, verify the pixel script is present before promising anything.
- Delivery is browser side only, so ad blockers can suppress these. Note `converly test-event` exercises server side delivery and does NOT apply to browser side destinations; verification here is a real form submission appearing in `converly events list`.

## ChatGPT Ads (`chatgpt-ads`)

- Connect via handoff. Inside the popup the user pastes an Ads API key and picks a data source (never take that key yourself). Then run `converly actions chatgpt-ads` and build the flow from its `config_example` via `--json`.
