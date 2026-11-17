# Creating a Deutero account as an agent

For an agent with a browser tool and a programmable inbox. Verified end to end against production on 17 September 2026 using an AgentMail inbox and headless Chromium.

If a human is signing up, none of this is needed: send them to `https://dashboard.deutero.ai/login`.

## What you need

- **A programmable inbox you can read.** AgentMail, or any IMAP/API mailbox. Deutero sends a magic link there. Use a dedicated inbox per account so links from different runs cannot collide.
- **A browser you can drive.** There is no account-creation endpoint. Once the account exists, everything else can go over MCP or REST.
- **Cookies that persist across the whole flow.** The intermediate login state is a session cookie. If the browser restarts mid-flow, you start again from step 1.

Steps 1–4 must run in one browser session.

## Step 1 — Request the magic link

Load `https://dashboard.deutero.ai/login`, fill `#email-input` with the inbox address, click **Continue with email**. The page then reads "An email was sent to …".

## Step 2 — Read the email

Wait for mail from `login@stytch.com`, subject **"Your login request to Deutero"**. Take the link from the **plain-text** body:

```
https://stytch.com/v1/magic_links/redirect?public_token=…&stytch_token_type=discovery&token=…
```

Two traps, both of which produce confusing errors:

- The HTML body escapes `&` as `&amp;`. Using it unmodified produces `invalid_public_token_id`.
- Each new request invalidates the previous link. Always use the newest message.

## Step 3 — Authenticate

Extract the `token` query parameter and navigate directly to:

```
https://dashboard.deutero.ai/authenticate?stytch_token_type=discovery&token=<token>
```

This is the same destination the email button eventually reaches, and it is the more reliable path for a headless browser: following `stytch.com/v1/magic_links/redirect` in headless Chromium landed on `stytch.com/redirect-error` in testing, while the direct call worked every time.

You are redirected to `/create-organization` (new address) or straight to the dashboard (address already known).

## Step 4 — Create the organization

On `/create-organization`, fill **Organization Name** and submit:

```python
page.get_by_label("Organization Name").fill("<name>")
page.get_by_role("button", name="Create Organization").click()
```

You land on `/onboarding`. The organization starts on the Hobby plan with 15 credits. The slug is derived from the email domain unless you set one.

## Step 5 — Get an API key

1. Go to `https://dashboard.deutero.ai/settings`.
2. Fill `#apiKeyName` with a label — the id is `apiKeyName`, not something like `apiKeyLabel`.
3. Click **Generate API Key**.
4. Read the key from `#newApiKey` in the dialog, or from the JSON response of `POST /settings/api/keys`. **It is shown once.**

Store it as `DEUTERO_API_KEY` with owner-only file permissions. Never log it.

## Step 6 — Switch to the API

Drive the UI no further than you have to; MCP and REST are faster and steadier.

```python
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

client = Client(StreamableHttpTransport(
    "https://dashboard.deutero.ai/mcp",
    headers={"X-API-Key": key},
))
```

Verify with `health_health_get`, then `list_projects`.

## Session notes for any later browser work

- Sign-in survives browser restarts for about 7 days, but **the selected project and study do not** — those live in the Flask session. Re-select with `/select-project?projectId=<id>`, or pass `?survey_id=<id>` on each study page, which every study page accepts.
- A redirect to `/login` means the session lapsed: redo steps 1–3. Build that in as an automatic retry rather than treating it as a failure.
- Several pages **lazy-load on scroll**, the Responses dashboard especially. If a number reads "Loading…", scroll before concluding anything is broken.

## What a fresh agent account cannot do

A new account lands on **Hobby**, which is text chat and on-device voice interviews on the open-weights model and nothing else:

- Run simulations, author an Interview Flow, show participants images or ask them for one, use cloud voice or video, use the standard or premium model tiers, keep more than one study open at a time, or exceed 15 credits a month. All of that needs a paid plan, and upgrading needs a human to complete Stripe checkout.

`plan-limits.md` has the full matrix and the fallback for each gate.

## Courtesies

- Prefer simulations to real participant interviews when you only need test data — and remember simulations need a paid plan, so on Hobby the honest test is one short interview you take yourself.
- Never post a live recruitment link into a real channel from a test account.
- Disable or delete API keys you no longer use.
