# Publishing the 2Chat skill to ClawHub — step by step

This publishes the `2chat-whatsapp` skill folder to OpenClaw's ClawHub marketplace under the
official **2chat** owner. Run these from the folder that contains `2chat-whatsapp/`.

## 0. Before you start (namespace claim)

You chose to publish under the official **2Chat** brand. ClawHub gates brand/org owner handles.
If the `2chat` owner handle isn't already linked to your account, request it first at:

- https://docs.openclaw.ai/clawhub/namespace-claims

Publishing to a scope you don't own will be rejected ("Package scope must match selected owner").
If the claim is still pending, you can publish under your personal handle now and migrate later
with `--migrate-owner` (shown below).

## 1. Install the CLI

```bash
npm i -g clawhub
# or: pnpm add -g clawhub
```

## 2. Sign in

```bash
clawhub login          # opens the browser
clawhub whoami         # confirm you're authenticated
```

Headless/remote instead? Use `clawhub login --device` or `clawhub login --token clh_...`.

## 3. Dry run (validate without uploading)

```bash
clawhub skill publish ./2chat-whatsapp \
  --owner 2chat \
  --version 1.0.0 \
  --dry-run
```

Fix anything the validator flags. Common ones: frontmatter fields, disallowed file types,
metadata that doesn't match what the skill actually does.

## 4. Publish

```bash
clawhub skill publish ./2chat-whatsapp \
  --owner 2chat \
  --version 1.0.0 \
  --changelog "Initial release: connects OpenClaw to the 2Chat remote MCP server (WhatsApp Web + WABA, SMS, contacts, groups, statuses, calls)." \
  --clawscan-note "This skill registers the official remote MCP server https://mcp.2chat.io/mcp (Streamable HTTP, OAuth 2.1 / PKCE). Network access to mcp.2chat.io and OAuth credentials are expected and intentional; the skill stores no API keys locally."
```

The `--clawscan-note` matters here: ClawScan flags network access and provider credentials, and
this skill legitimately does both. The note gives the reviewer that context up front.

## 5. After publishing

- The listing is **hidden from install surfaces until the automated review completes** — this is
  normal. Check status with `clawhub whoami` / your ClawHub dashboard.
- To ship a fix or update, bump the version and re-run step 4 (e.g. `--version 1.0.1`).
- Verify a real install once it's live:

  ```bash
  clawhub skill install 2chat/2chat-whatsapp
  ```

## Publishing under your personal handle instead

Drop `--owner 2chat` (it defaults to your handle), or set `--owner <your-handle>`. To later move
it to the official `2chat` owner once the namespace claim clears:

```bash
clawhub skill publish ./2chat-whatsapp --owner 2chat --migrate-owner --version 1.0.1
```

## Notes

- ClawHub licenses all published skills under **MIT-0** and does not support paid skills.
- Everything the skill needs is documented in `2chat-whatsapp/SKILL.md`; `mcp-server.json` is a
  convenience config block for users who prefer editing `mcp.servers` by hand.
