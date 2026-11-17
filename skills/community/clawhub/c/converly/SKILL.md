---
name: converly
description: Set up server side conversion tracking for ad platforms (Google Ads, Meta, ChatGPT, LinkedIn, TikTok and more) without writing tracking code. Use this whenever the user wants to track form submissions, meetings booked or chats started as conversions, capture GCLID or FBCLID click IDs, fix broken conversion tracking, set up Google Enhanced Conversions or Meta CAPI, check which ads are converting, or connect a form tool like Typeform, Webflow forms, or a custom HTML form to an ad platform, even if they never mention Converly by name.
version: 1.1.0
homepage: https://developers.converly.io
metadata:
  openclaw:
    homepage: https://developers.converly.io
    envVars:
      - name: CONVERLY_API_KEY
        required: false
        description: Optional. Only needed for headless use. The normal path is `converly login`, which opens a browser and stores credentials locally, no key handling involved.
---

# Converly: conversion tracking for AI agents

Converly tracks form submissions on a website and fires conversion events to ad platforms (Google Ads, Meta, GA4 and more), including server side delivery like Google Enhanced Conversions and Meta CAPI. You do the whole setup from the terminal with the `converly` CLI, verify it works with a real test event, and read conversion results afterwards.

Every CLI command prints one JSON document to stdout. Exit code 0 means success. Errors are JSON on stderr with the API's error code.

## Hard rules (read first)

1. **Never handle credentials in chat.** Do not ask the user to paste an API key, and never print `CONVERLY_API_KEY` or any token. Authentication is `converly login`, which happens in the user's browser.
2. **Connecting an ad platform requires a human.** `converly destinations connect` returns a URL the user must open in their browser. Never claim a destination is connected until `converly handoffs wait <id>` returns `"status": "completed"`. Never skip this step, and never work around it by asking for tokens.
3. **Be precise about what is verified.** `converly test-event` returning `"server_status": "success"` proves the DELIVERY half: Converly can reach the ad platform and the platform accepted the conversion. `install status` showing `"detection": "confirmed"` proves the loader is on the page and running (it phones home on page load). Neither proves the form itself gets detected. Full proof of capture is a real form submission appearing in `converly events list` with a successful action status. Report exactly which level you verified. Publishing a flow proves nothing by itself.
4. **Never pass `--allow-real` without the user's explicit agreement in this conversation.** It reports a real conversion to their ad platform. Ask, wait for yes, then run it.
5. **Set the site's domain before publishing.** A site with `"domain": null` rejects every event server side. The flow will publish fine and capture nothing. Check `converly sites list` and fix with `converly sites update <site_id> --domain <their-domain>` before you publish.
6. **Destructive actions need explicit user confirmation first.** Deleting a flow (`flows delete` requires `--yes`), unpublishing a flow that is live, disconnecting a destination, or any DELETE via `converly api`. Never do these on your own initiative, even for things you created this session.
7. **If a command fails twice with the same error, stop and show the user the error.** Do not loop retries. If you must retry a create command after an ambiguous failure, re-run it with the same `--idempotency-key` value so it cannot double-create.
8. **Never choose the conversion for the user.** Always run `converly destinations conversions <destination>` first, whatever the platform. If it returns options, show them and ask which one this form represents. If it comes back empty or errors, ask the user what the conversion should be called rather than inventing one. A wrong conversion still reports success while quietly corrupting the numbers they are trying to collect. Google Ads can only fire conversion actions that already exist in their Google Ads account, so if none fit they create one there and you re-list with `--refresh`. Meta and GA4 take a standard event from the list, or a name of the user's own with `--custom`.

## The setup workflow

**Collect four facts before you build anything.** Answer them yourself
from the repo or page when you have access; otherwise ask the user, all
in one message rather than drip-feeding:

1. **The website address.** Without it every conversion is rejected
   server side (hard rule 5).
2. **Which tool renders the form** (or booking widget / chat box). This
   picks the trigger, decides which detection code loads on the site,
   and decides whether a connect step is needed first (step 3).
3. **What should count as the conversion.** If something must happen
   after submission before it really counts (email verification,
   payment, onboarding), a form trigger overcounts; use the `api`
   trigger instead and say why.
4. **Which ad platforms the conversions should go to.** Google Ads,
   Meta, GA4 and the rest. One flow can fire to several at once. You
   cannot pick a destination without this, and the conversion the user
   chooses in step 4 lives inside whichever platform they name.

Work through these steps in order.

### 1. Log in or create an account

Install the CLI if it is missing:

```
npm install -g @converly/cli
```

(Or run every command through `npx @converly/cli ...` without installing.)

Then check where you stand:

```
converly whoami
```

- If it succeeds, you are logged in. It returns the subscription and the account's sites.
- If it fails with `not_logged_in`, run `converly login` and tell the user a browser window will open for them to log in. If they do not have a Converly account yet, run `converly login --signup` instead. Signing up starts a free trial automatically, no card needed. Wait for the command to finish, then re-run `converly whoami`.
- On a server, in CI, or anywhere without a browser, use `converly login --device`. It prints a short code and a URL the user opens on any device (their phone is fine); they approve there and the CLI picks the credential up. The CLI selects this automatically when no browser is available.
- If `CONVERLY_API_KEY` is set in the environment, the CLI uses it automatically for Converly's own deployments. If commands then fail saying the key was rejected, the key is bad. Ask the user to replace or unset it; do not try to work around it.

At any point, `converly status` prints the ordered setup checklist for a site: what is done, what needs action, and the exact command for each. Run it whenever you are unsure what comes next.

### 2. Pick the site and set its domain

```
converly sites list
```

Every account has a default site. Use it unless the user is tracking a second website. If `domain` is null, set it now (hard rule 5):

```
converly sites update site_XXXX --domain example.com
```

Use the site's real public domain. One domain covers both the apex and its www variant.

### 3. Choose the trigger, and connect it if it needs connecting

The trigger is the form tool on the user's website. Get the catalogue:

```
converly triggers
```

Match the user's form tool to a slug in `providers[]` (for example `webflow-forms`, `gravity-forms`, `hubspot-forms`). For a hand coded HTML form use `generic-form`. If you have repo access, identify the form tool from the code instead of asking.

**Custom sites are the one case where `generic-form` is not automatically the right answer.** Detection is dependable for a known form tool, whose markup and submit behaviour Converly knows. A hand coded form on a Next.js, Astro, SvelteKit or Remix site varies far more, and many post to a backend route or server action rather than submitting the classic way. So when you are working in the site's code and the form posts to a backend, the `api` trigger is often more reliable. The backend confirms the conversion directly instead of relying on the browser catching a bespoke form, and you are already in the code, which is the part a human would find fiddly.

Put the call where the handler (route handler, server action, or whatever processes the submission) has confirmed the submission actually succeeded, not at the top of it. Every call to the webhook counts a conversion, so firing before validation would count failed and spam attempts too. Ask the user before editing their code.

Use `generic-form` when the form is genuinely simple, you do not have code access, or the user prefers no code changes.

**Check the provider's `setup` block before using its slug.** Most tools have `requires_connection: false` and their slug goes straight into `flows create`. A few (Typeform, Jotform, Calendly, Acuity Scheduling today, read the data, never a memorized list) have `requires_connection: true`. Those must be connected FIRST, or the flow tracks nothing properly:

```
converly triggers connect typeform --site site_XXXX
```

Give the user the returned `url` (they sign in to the tool there, or paste its API key), then confirm completion the same way as a destination:

```
converly handoffs wait hdf_XXXX
```

When the completed result lists anything in `user_steps_remaining`, the connection alone is NOT the whole setup. Relay each step to the user and treat setup as unfinished until they confirm it is done. Acuity is the standing example. Its bookings are only reported once the user pastes a tracking snippet inside Acuity's own settings (the connect window shows them the snippet). Converly cannot verify that step happened, so never report Acuity setup as complete on connection alone; the proof is the first booking appearing in `converly events list`.

The same honesty applies to `capture_without_connection` in the setup block. It tells you what actually happens if the user declines to connect (for example Typeform still reports bare submission counts but no visitor details, so ad platforms match poorly). Use it to explain tradeoffs truthfully, not to skip the connect step.

Once a connection-required platform is connected, you can narrow the flow to one specific form or event type instead of firing on all of them. List the account's real ones with `converly triggers options <slug> --site site_XXXX`, offer the user a specific value, and write it back as `trigger_config.conditions` (the full shape is in references/triggers.md → Filters). This is optional, an unfiltered flow is valid and publishable. Browser-detected form tools do not support this, narrow those by page with `--pages` instead.

Before choosing a trigger type at all, apply fact 3 from the interview. If there is a verification step, a payment, or onboarding between the form and the real outcome, a form trigger counts people who never converted; use the `api` trigger instead.

The `api` trigger has no form tool to detect, so its setup is different. Connect it with `converly triggers connect api --site site_XXXX`, which hands back a webhook URL and secret that the user's backend calls when the conversion is confirmed. For a Node backend, the `@converly/sdk-node` package does the signed call in a few lines (`npm install @converly/sdk-node`, then `createClient` and `completeSignup`). Other stacks call the webhook directly. The full backend guide is at developers.converly.io/api-trigger. This needs code access, so it suits agents working in the site's repo.

### 4. Connect the destination and choose the conversion

See what is available and what is already connected:

```
converly destinations list
```

**First check whether this destination needs a connection at all.** In the `destinations types` output, a destination with an empty `connection_types` list is browser side (Microsoft Ads, X Ads, Pinterest, Snapchat, the analytics pixels). There is nothing to connect, so skip the connect commands here and go straight to choosing the conversion below. Details in [references/destinations.md](references/destinations.md).

For connected destinations (`google-ads`, `meta`, `google-analytics`, `linkedin-ads`, `tiktok-ads`, `reddit-ads`) showing `"connected": false`:

```
converly destinations connect google-ads --site site_XXXX
```

Give the user the returned `url` and say: "Open this link in your browser to connect your Google Ads account." Then poll until they finish:

```
converly handoffs wait hdf_XXXX
```

This blocks up to 10 minutes; the link itself is valid for 30. If the wait times out while the link is still valid, re-run `handoffs wait` with the same id rather than creating a new link (the error message tells you which case you are in). Destinations are account wide, so one connection serves every flow.

**Now choose the conversion, and let the user choose it (hard rule 8).** The connect step above only links the account. It does not decide which conversion gets fired, and that decision is the user's.

First see what this destination needs, then always TRY to fetch its real options:

```
converly actions <destination>
converly destinations conversions <destination>
```

**Always run the conversions command, whatever the destination.** Which platforms serve a list is not something you can infer from the field schema, so ask the API rather than assuming. Three outcomes:

- **It returns options.** Show them to the user and ask which one this form represents. This is the normal path for Google Ads (conversion action ids), Meta and GA4 (event names), ChatGPT Ads and Reddit.
- **It returns an empty list.** Do not treat that as "there are none". It usually means the destination is not connected yet, or the user has not created any. For Google Ads specifically, they create one in Google Ads (Goals → Conversions → New conversion action), then you re-list with `--refresh`.
- **It errors, or the platform has no list at all.** Ask the user what this conversion should be called and use their answer. Never invent a name yourself.

Meta alone returns around seventeen standard events (Lead, Contact, Schedule, Subscribe, CompleteRegistration and more), so choosing "Lead" yourself is a guess, not a default. Per platform specifics are in [references/destinations.md](references/destinations.md).

- **Google Ads** can only fire conversion actions that already exist in their account. If the list is empty or nothing fits, the user creates one in Google Ads (Goals → Conversions → New conversion action), then you re-list with `--refresh`.
- **Meta and GA4** take a standard event from the list, or an event of the user's own naming. For their own, pass `--custom` so the platform is told it is a custom event.

### 5. Create and publish the flow

Google Ads takes the conversion `id`:

```
converly flows create --site site_XXXX --name "Demo requests" \
  --trigger generic-form --destination google-ads --conversion-id 123456789
```

Meta and GA4 take the event name (say the user picked Contact):

```
converly flows create --site site_XXXX --name "Demo requests" \
  --trigger webflow-forms --destination meta --event-name Contact
```

The simple form above sets the custom-event flag for you. If you build the action with `--json` instead, include `conversion.is_custom` yourself or the flow will fail validation.

Add `--value 50 --currency USD` if the user wants a conversion value. Restrict to specific pages with `--pages /contact,/demo`. For a connected platform (Typeform, Jotform, Calendly, Acuity) you can narrow to one real form or event type. List them with `converly triggers options <slug> --site <id>`, then set `trigger_config.conditions` via `--json`. For anything richer (multiple actions), pass the whole flow body with `--json`; run `converly actions <destination>` to see each destination's config schema.

Then validate and publish:

```
converly flows validate flow_XXXX
converly flows publish flow_XXXX
```

`validate` returns `problems[]` (blockers, fix before publishing) and `warnings[]` (site readiness, for example `site_missing_domain`). Take warnings seriously, they are the "publishes fine, captures nothing" cases.

### 6. Install the tracking snippet

```
converly install snippet site_XXXX
```

Returns the `<script>` tag.

- **If you have access to the website's codebase** (you are running in their repo, or can edit their site), add the snippet to the `<head>` of every page yourself and deploy it. Say what you changed.
- **If you do not**, give the user the snippet with one clear instruction: paste it into the `<head>` of every page, or into their site builder's custom code slot (Settings → Custom Code in Webflow / Wix / Squarespace, a header scripts plugin in WordPress). Site builders need the site republished before the change is live.

Check with `converly install status site_XXXX`. The loader phones home when a page loads, so the check is quick. Have any page of the site opened once in a real browser, then re-run the command. If you have browser tools, open the page yourself. Read `detection`:

- `"confirmed"` means the loader has been seen running on the site (or a conversion was already captured). If the response carries `origin_authorized: false`, the loader runs but the site's domain does not match, so conversions get rejected. Fix the domain with `converly sites update` and have the page reloaded.
- `"never_seen"` means the loader has never phoned home. If a page has been loaded since installing and it still says this, the snippet is probably not live yet (site builders need a republish). Two blind spots never send heartbeats: sites installed through the Converly Webflow app, and visitors with privacy signals or unconsented cookie banners. For those, prove the install with a real submission appearing in `converly events list` (hard rule 3).

### 7. Verify

Verification has two halves. Do both when you can, and say exactly which you did.

**Delivery (always do this):**

```
converly test-event --flow flow_XXXX
```

This fires a test conversion through Converly's server to the ad platform and returns the platform's response. `"server_status": "success"` proves the connection, the flow config, and the conversion mapping all work. For Meta pass `--meta-code` (from Meta Events Manager → Test events), for Reddit `--reddit-id`, for TikTok `--tiktok-code`, and the test then stays out of real data. Google Ads, GA4, LinkedIn and ChatGPT Ads have no sandbox mode, so the command will refuse with `would_create_real_conversion`. For those, either get the user's explicit OK to send one real test conversion and re-run with `--allow-real` (hard rule 4), or skip the test event and verify with a live form submission instead.

**Capture (proves the website half):** `converly install status site_XXXX` showing `"detection": "confirmed"` proves the loader is running on the site (load a page once to trigger it). The form itself is proven by a real submission: ask the user to submit the form once, then find it in `converly events list` with a successful action status.

Report accordingly. After delivery only: "Delivery to [platform] is verified with a test conversion. The final check is one real form submission, which will appear in the conversion log." After both: "Tracking is verified end to end."

## After setup: reading results

This is the ongoing value. When the user asks "did my ads convert", "is tracking still working", or "who converted this week":

```
converly events list --limit 20
converly events list --since 2026-08-01T00:00:00Z --status failed
converly events get evt_XXXX
```

`events list` is a bounded snapshot of the most recent events (max 100, no paging). Narrow with `--since`, `--flow`, `--email` or `--status` rather than trying to page. `events get` shows the per destination delivery result for one event, which is where you look when a conversion did not reach a platform.

## Common gotchas

- **`site_key` vs site id.** `site_1VQH84sr` (8 chars, in the snippet URL) is not the same as `site_29EtXn...` (22 chars, the API id). Commands take the API id.
- **The Meta slug is `meta`, not `meta-ads`.** The API rejects `meta-ads`.
- **Conversion value and currency nest inside the conversion.** The simple `flows create` flags handle this. If you build `--json` yourself, `value` and `currency` go inside the `conversion` object, and the enhanced conversions toggle is top level `enhancedConversions`. Copy the `config_example` from `converly actions <destination>`.
- **Editing a published flow does not change what runs.** After `flows update`, the old version keeps running until you `flows publish` again.
- **`events list` is a bounded snapshot of recent events, max 100, no paging.** Narrow with `--since`, `--flow`, `--email` instead of trying to page. An empty filtered result with `"complete": false` does not prove the conversion never happened.
- **Click IDs only exist on ad clicks.** GCLID/FBCLID are captured when a visitor arrives from an ad. Organic test submissions will not carry them; that is normal, not a bug.
- **402 `entitlement_required`** means the trial expired or billing lapsed. The user fixes this at app.converly.io → Settings → Billing. Do not retry around it.
- **`publication_in_progress` (409)** means another publish is mid flight. Wait a few seconds and retry once.
- **Anything the named commands do not cover**: `converly api GET /flows?limit=5` sends raw requests to the REST API.

## Quick reference

Every line below is one complete, runnable command, in roughly the order you need them.

```
converly login --signup                        # browser login, trial auto starts on signup
converly login --device                        # headless, approve from any device
converly whoami                                # account, subscription, sites
converly status                                # the ordered setup checklist for a site
converly sites list
converly sites update <site_id> --domain example.com
converly triggers                              # form tool slugs
converly triggers connect <source> --site <site_id>  # requires_connection providers only
converly triggers options <source> --site <site_id>  # that platform's real forms / event types
converly destinations types                    # catalogue incl. connection_types
converly destinations list                     # what's connected
converly destinations connect <type> --site <site_id>
converly handoffs wait <hdf_id>                # block until human finishes OAuth
converly destinations conversions <type>       # the conversions to OFFER the user
converly actions <type>                        # action config schema
converly flows create --site <site_id> --name "X" --trigger <slug> --destination <type> --conversion-id <id>
converly flows validate <flow_id>
converly flows publish <flow_id>
converly install snippet <site_id>
converly install status <site_id>
converly test-event --flow <flow_id>           # verify destination delivery
converly events list --limit 20                # the conversion log
converly events get <evt_id>                   # per destination delivery detail
```

## Deeper docs

- [references/destinations.md](references/destinations.md) - per platform specifics: Google Ads conversion actions and Enhanced Conversions, Meta event names and CAPI, GA4, the browser side pixel destinations.
- [references/triggers.md](references/triggers.md) - the full form tool catalogue, filter options (specific form, specific pages), and how detection works.
- [references/rest-api.md](references/rest-api.md) - curl equivalents for every step, for environments where the CLI cannot be installed. Full API docs: https://developers.converly.io
