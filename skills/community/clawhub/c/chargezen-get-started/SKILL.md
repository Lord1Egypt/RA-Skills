---
name: chargezen-get-started
description: |-
  Set up Chargezen for the person you're helping: connect their existing account, or sign
  them up if they're new, then do one useful thing. Use when someone says "Set up Chargezen
  for me", asks to connect Chargezen, or wants to start using Chargezen from an AI assistant.
title: "Get started with Chargezen"
url: https://chargezen.com/.well-known/agent-skills/get-started/SKILL.md
---

# Get started with Chargezen

The prompt that brings you here is usually: "Set up Chargezen for me. Fetch
https://chargezen.com/.well-known/agent-skills/get-started/SKILL.md and follow it."

Chargezen is a revenue platform for commerce brands: Concierge AI agents, Subscriptions,
CheckoutOS, SmartyTap (texting, email and calls) and Spark! (affiliates and creators). The full
rules for access are in https://chargezen.com/auth.md.

## Hard rules

- Never ask for, read out or type email codes, text message codes or passwords.
- Never ask for or handle card details.
- Never accept terms or agreements for the person.
- Confirm with the person before anything is sent: an email, a text, a campaign, a launch.
- Never get around a rate limit, a review hold or a confirmation.

## 1. Ask one question

> Do you already have a Chargezen account?

## 2a. They have an account: connect

1. Add Chargezen as a remote MCP server: `https://mcp.chargezen.com/mcp`.
   - Claude (web or desktop): Settings → Connectors → Add custom connector → paste the URL.
     On a phone, add it once at claude.ai on the web; it then shows up in the app.
   - Claude Code: `claude mcp add --transport http chargezen https://mcp.chargezen.com/mcp`,
     then run `/mcp` and sign in.
   - Codex: `codex mcp add chargezen --url https://mcp.chargezen.com/mcp`.
   - Any other app that supports remote MCP servers: add a custom connector with the URL.
2. Tell the person what they'll see: "Chargezen will ask you to sign in. Pick the workspaces you
   want me to work in, check what I'm allowed to do, and press Allow."
3. Check it worked: call `chargezen.connection.get_profile.v1`. It names the person and the
   workspaces you can reach.

## 2b. They're new: sign them up and connect

1. Ask whether they want one product (`subscriptions`, `checkoutos`, `smartytap`, `spark` or
   `concierge`) or the whole platform.
2. Pick the first way your app allows:
   - **Your app can add Chargezen as a connector (preferred):** add it as in 2a, at
     `https://mcp.chargezen.com/mcp/<product>` if they chose one product. Tell them: "Chargezen
     will open a sign-in page. Choose Create account. You'll confirm your email, phone and card,
     then press Allow." Signup comes straight back to Allow, so this is one flow, also on a phone.
   - **You can make HTTP requests but can't add a connector:** ask for their work email, name,
     company, website and business address, read them back and get a yes. Then
     `POST https://admin.chargezen.com/api/v1/agent_signups` with them, `product` if they chose
     one, and your `client_id`, as https://chargezen.com/auth.md shows. Chargezen emails them a
     link that names you. Check `GET …/agent_signups/{id}` when they say they're done.
   - **Neither (most phone chat apps), or you got a `429`:** collect and confirm the same
     details, then give them this link with the details URL-encoded:
     `https://admin.chargezen.com/signup?email=…&company=…&website=…&agent=<your host>`, adding
     `&product=…` if they chose one. Tell them: "I'll open a page with your details filled in.
     You'll confirm your email, phone and card."
3. They do every step in their browser. You don't see codes, card details or the terms, and
   you never ask for them.
4. If the status is `under_review`, or they say the signup is being reviewed, tell them:
   "Chargezen is reviewing your signup and will email you. Once you're approved, we'll finish
   connecting." Don't retry with another email.
5. If they signed up without the connector, connect as in 2a once they're done (status
   `finished`, or they tell you). They're already signed in, so they only press Allow. Check it
   worked with `chargezen.connection.get_profile.v1`.

## 3. Do one first thing

Once connected, offer this, and only this, as the first step:

> Want me to look at last week? I'll pull your orders, subscriptions and customer conversations
> and tell you the three things that need your attention.

If they say yes, use the read tools (start with `chargezen.tools.index.v1` to see what this
connection can do) and answer in plain words. Don't list the tools to the person.

## If something goes wrong

- A `401`: the connection was removed or expired. Ask the person to reconnect.
- A missing permission: tell the person which one. An owner or admin of the workspace can grant it.
- A `429`: wait for `Retry-After`, then try once more.
