# Trigger specifics

The trigger is what Converly's loader watches for on the user's website. Get the live catalogue with `converly triggers`; use a slug from `providers[]` as the flow's trigger.

## How detection works

The Converly snippet loads a per site config and watches the page for the configured form tool's submission signals (native events, embedded iframe messages, DOM signals, depending on the tool). No code changes to the form itself, no webhooks to set up for the browser detected tools. That means:

- The snippet MUST be on the page where the form lives.
- The flow must be PUBLISHED before anything is captured.
- Detection is per tool. Picking the right provider slug matters. `generic-form` covers hand coded `<form>` elements.

## Picking the right slug

Match what actually renders the form, not the brand of the website builder:

- A Typeform embedded on a Webflow site is `typeform`, not `webflow-forms`.
- A HubSpot form embedded anywhere is `hubspot-forms`.
- Webflow's own native form blocks are `webflow-forms`.
- A React app's hand rolled form is `generic-form`.

If you have repo or page access, inspect the form markup and decide yourself. Embed scripts (`js.hsforms.net`, `embed.typeform.com`) are the giveaway.

## Trigger types

- `form_submission` - about 80 providers: Gravity Forms, Contact Form 7, WPForms, Elementor, Typeform, Jotform, Webflow, Wix, Squarespace, Framer, Unbounce, HubSpot, Mailchimp, Marketo, Tally, Fillout, ClickFunnels, and more. No filter is required. A flow with no `--pages` fires for every form of that type anywhere on the site, so offer page narrowing when the site has more than one form.
- `chat_started` - LiveChat, Intercom, Drift, Tawk.to, HubSpot Chat and similar. Fires when a visitor starts a conversation.
- `meeting_booked` - Calendly, Acuity, Cal.com, OnceHub, SavvyCal style booking tools.
- Connection-required providers. Read each provider's `setup` block in the catalogue. `requires_connection: true` (Typeform, Jotform, Calendly, Acuity today) means the tool must be connected with `converly triggers connect <slug> --site <id>` BEFORE its flow properly works. `capture_without_connection` tells you honestly what happens if the user declines (for example count-only capture with no visitor details). `post_connect_user_steps` lists steps the USER must still do outside Converly (Acuity's pasted snippet); Converly cannot verify those, so setup is only proven when the first event arrives.
- `custom_event` - cannot be set up through this surface. Never offer it, and never improvise a custom-event workaround for an unsupported tool. If no listed provider fits, say so plainly.

## Filters

The simple CLI form defaults to all pages (`pageFilter: "all"`), and that is a valid, publishable flow. Narrowing options, honestly stated:

- **By page** (works for every browser-detected tool): `--pages /contact,/demo`. This is the only per-form narrowing that works for browser-detected tools. When the site has more than one form, ask which page the form the user cares about lives on and narrow to it, otherwise a contact form and a newsletter box report as the same conversion.
- **By specific form or event type** (connection-required providers only: Typeform, Jotform, Calendly, Acuity). Once the platform is connected, list its real forms or event types with `converly triggers options <slug> --site <site_id>`. Each field in the result carries the account's actual values with their `id` and `name`. Offer the user a specific one, then narrow the flow by writing `trigger_config.conditions` keyed by that field, for example `converly flows update <flow_id> --json '{"trigger_config": {"conditions": {"form": {"ids": ["abc123"], "names": ["Demo Request"]}}}}'`. The values come live from the platform, so never invent condition values that `triggers options` did not return. Respect its `notes` too: a field marked `available: false` means the values could not be fetched, not that the account has none.

There is no `formId`, `formSelector`, or CSS-selector filter on any surface. The only two filters the loader actually honours are the page path (above) and, for connected platforms, the `conditions` shape from `triggers options`. Any other field you put on the trigger is silently dropped at publish and the flow fires on every form of that type, so do not guess a filter field.

To adjust an existing flow, pass just the changed field to `converly flows update <flow_id> --json '{"trigger_config": {...}}'`.

## When nothing fires

Work through, in order:

1. `converly install status <site>`. The loader phones home on page load, so have any page of the site opened once, then re-run. Read `detection` precisely: `"confirmed"` means the loader runs on the site, look further down this list (and if `origin_authorized` is false, the domain is wrong, fix it with `sites update`). `"never_seen"` after a fresh page load means the snippet is probably not live (site builders need a republish), except for two heartbeat blind spots: Converly Webflow app installs and privacy-signal visitors, where only a real submission in `events list` proves the install. `"pending"` means the check itself couldn't run right now, try again shortly.
2. Site domain set and matching the real origin? `converly sites list` → `domain`. A staging URL or a different subdomain will be rejected.
3. Flow published? `converly flows get <id>` → `status` must be `published`, `publication_state` should be `in_sync`.
4. Right provider slug for what actually renders the form? (See "Picking the right slug".)
5. Internal traffic rule swallowing your tests? `converly rules list`.
6. Still nothing: `converly events list --status failed` and `converly events get` on anything that appears; the event detail carries per destination errors and user facing notices.
