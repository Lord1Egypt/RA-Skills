# Security model

This document is the threat model + data-flow + guardrail reference for the
Buck Mason Stylist Skill. It exists so reviewers (humans and automated
scanners like ClawScan / VirusTotal Code Insight) can verify what this skill
does, what it can't do, and what the operator is on the hook for.

If you find a vulnerability, email **security@pima.io** — do not file a public
GitHub issue.

## TL;DR

- **No bundled binaries, no native modules, no install-time scripts.** The
  skill is markdown + JSON + Python sample code. Tools that get invoked are
  invoked through the *agent's* shell (`curl`, `jq`, `python3`,
  `python-pptx`, `Pillow`, optionally `magick` and `@stripe/link-cli`) — all
  under the operator's existing trust boundary.
- **No persistent server.** Everything runs as in-conversation tool calls
  from whatever agent loaded `SKILL.md`.
- **The MPP payment path** never sees a card number; it only
  ever holds a one-time, short-lived **Stripe Shared Payment Token** minted
  by the customer push-approving the spend in their own Link wallet. The
  push-approval IS the consent. SPTs are never written to disk.
- **The OpenAI key is required only for the default Premium lookbook workflow.**
  All other workflows (stock check, recommend, MPP checkout, order
  tracking, returns) and fallback lookbook tiers work with no OpenAI key at all.

## Data flow

| Source | Sink | Trigger | What goes |
|---|---|---|---|
| `profile.md` (sizes, build, face, photos) | OpenAI `/v1/images/edits` | Workflow #3 (default Premium lookbook / explicit try-on) | Reference photos + structured garment + setting prompt. Photos are sent only when the customer asks for a lookbook/try-on and Premium prerequisites are present. |
| `profile.md` (size, zip) | `pima.io/mcp/buckmason/*` | Workflows #1, #2, #4 | Just the size + zip — no photos, no contact info, no shipping address. |
| `profile.md` (shipping, name, email, phone) | `pima.io/mcp/buckmason/checkout` | Workflow #4 step 3 (MPP only, opt-in) | Buyer block sent to Pima for the payment intent. |
| `profile.md` (Link card labels, last4, purpose preferences) | Local agent + `link-cli payment-methods list` | Workflow #4 step 3 (MPP only, opt-in) | Used to choose the live Link payment method for a purchase purpose such as clothing or business. The profile stores only labels/brand/last4/purpose; Link internal payment-method ids are resolved live and not persisted. |
| `profile.md` (email) | Customer's own inbox via Pima | Workflow #5c (magic-link, opt-in only) | Email is delivered by Pima to the customer; the agent never sees it unless an explicit email-MCP is authorized in the same turn. |
| `wardrobe.md`, `events.md` | Local filesystem only | All workflows that read them | Never sent to any external service. |
| Generated HTML lookbook | Cloudflare Pages (`*.pages.dev`) via the operator's `wrangler` | `scripts/deploy-lookbook.sh` (opt-in; the operator runs it) | The HTML file + assets. Includes generated try-on imagery if Premium-tier ran and the default voting UI/Pages Functions unless `--no-voting` is explicit. The skill shells out to `wrangler` which uses the operator's pre-existing Cloudflare credentials. **Customer should treat the resulting URL as semi-public** — it is not access-controlled. |
| Partner/stakeholder vote form | Cloudflare KV (`LOOKBOOK_VOTES`) via Pages Functions | Default Cloudflare Pages lookbook deploy after the customer/operator provides `lookbook_votes_kv_id` or `$LOOKBOOK_VOTES_KV_ID` | Voter-entered name, thumbs up/down per look/item, free-text comment, timestamp, IP, user agent, and lookbook id. No account login or payment data. |
| Generated HTML lookbook | Other hosts (Surge, Netlify, Vercel, Gist, S3, 0x0.st, …) | Operator manually runs the alternate CLI per `references/hosting-options.md` | Same payload as above. The skill **does not bundle, install, or invoke** those CLIs — listed in `clawhub.json#permissions.network_alternatives_documented_only` for full disclosure. Same trust model as `@stripe/link-cli`. |
| `html-cart` selection block (slug + size + qty + lookbook_id) | `~/.buck-mason-stylist/wishlist.jsonl` (local filesystem) | Workflow #4 path B on handoff paste-back and on successful MPP order | Append-only JSONL. Contains slug, size, qty, `lookbook_id`, `price_cents_at_pick`, and (after settlement) `order_id` + `purchased_at`. No card data, no shipping address, no email, no full name. Lives outside the workspace so it persists across agent sessions on the same machine — declared in `clawhub.json#permissions.filesystem`. |

Nothing in this skill writes to anywhere outside the operator's workspace
or the wishlist path declared in `clawhub.json#permissions.filesystem`,
and never to any host outside the four listed in
`clawhub.json#permissions.network`.

## Threat model

### What the skill DOES NOT do (deliberately)

- It does **not** ask for, store, or transmit raw card numbers, CVVs,
  routing numbers, or bank credentials. Stripe SPTs are the only payment
  artifact the agent ever holds.
- It does **not** persist Link internal payment-method ids. A profile may store
  customer-readable card labels, last4s, and purpose preferences (for example
  "clothing -> 0896"), but the agent resolves the live `--payment-method-id`
  through `link-cli payment-methods list` immediately before checkout.
- It does **not** read the customer's email automatically. The magic-link
  flow (workflow #5c) is opt-in; default is the guest `?order_code=` path.
  When email is read, it requires an explicitly authorized email MCP and
  the agent restates the authorization in the same turn.
- It does **not** auto-checkout. Even on the MPP path, the agent must read
  back items + total + shipping + return policy in plain English in the same
  turn and wait for an unambiguous "yes, go ahead" before invoking
  `link-cli spend-request create --request-approval`.
- It does **not** install or fetch code at runtime. Optional dependencies
  (`@stripe/link-cli`, `magick`) are operator-installed.
- It does **not** include or vendor third-party CLIs. The skill references
  `@stripe/link-cli` by its npm scope (verified Stripe publisher) and links
  to the source repo. If you don't want it, leave it uninstalled — MPP
  checkout will be unavailable.
- It does **not** keep a long-lived server-side session. Outside the optional
  Cloudflare KV voting namespace, there's no database, no queue, and no
  server-side session. Each commerce/image tool call is a stateless HTTP
  request to `pima.io` or `api.openai.com`.

### What an operator opts into

| Capability | Default | Opt-in |
|---|---|---|
| Stock check, recommend | ✅ on | — |
| Order tracking via guest order-code | ✅ on | — |
| AI try-on (sends photos to OpenAI) | ❌ off in default install; when `OPENAI_API_KEY` is configured, it is the default for unqualified lookbook requests | per-lookbook |
| MPP fully-agent-driven checkout | ❌ off (requires `@stripe/link-cli` and an explicit user opt-in to agent-driven payment) | per-purchase |
| Email magic-link account linking | ❌ off | per-conversation, with retrieval method confirmed before sending the email |
| HTML lookbook deploy to Cloudflare Pages + default voting | ❌ off (requires the operator-installed `wrangler` CLI, Cloudflare auth, and a KV namespace id unless `--no-voting` is explicit) | per-deploy, by running `scripts/deploy-lookbook.sh` or headless auto-publish |
| HTML lookbook deploy to alternate hosts (Surge, Netlify, Vercel, Gist, S3, 0x0.st) | ❌ off (skill never invokes these — operator runs the host's CLI manually) | per-deploy, fully operator-driven |

If the operator wires the skill into an agent without `OPENAI_API_KEY` and
without `@stripe/link-cli`, all the high-risk capabilities are unreachable
by construction.

### Risks the skill cannot mitigate

These are the operator's responsibility:

- **Workspace integrity.** `profile.md` lives in the agent's workspace. If
  the workspace is shared (a shared box, a CI runner, a multi-tenant
  filesystem) the operator must restrict it. Recommendations:
  - Keep `profile.md` minimal — the skill only needs sizes + zip for stock
    checks. Shipping, photos, full address are required only for the
    workflows that explicitly need them.
  - Don't check `profile.md` into git. The skill's `templates/profile.example.md`
    is committed; the filled-in version should not be.
- **Agent host trust.** The skill assumes the agent host can keep
  `OPENAI_API_KEY` out of public conversation logs and out of LLM context
  it doesn't need. The skill itself never echoes the key.
- **Email MCP scope.** If the operator wires a Gmail/IMAP MCP with broad
  read scope solely for the magic-link flow, that's a much larger blast
  radius than the magic-link workflow itself. Prefer the customer pasting
  the link back, or scope the MCP to just the inbox tied to the Buck Mason
  email.
- **Network-level interception.** The skill talks to `pima.io` and
  `api.openai.com` over TLS. The operator is responsible for the host's
  CA store.
- **Lookbook hosting destination.** When the operator runs
  `scripts/deploy-lookbook.sh` or one of the alternates in
  `references/hosting-options.md`, the resulting URL is hosted on the
  *operator-chosen* third party (Cloudflare Pages, Surge, etc.) under the
  operator's own account. The skill does not configure access control on
  those hosts — the URL is treated as semi-public. If the lookbook contains
  generated try-on imagery, the operator must decide whether the chosen
  host's default privacy posture is acceptable. Cloudflare Pages and Vercel
  give a stable subdomain; Gist + 0x0.st are anonymous-public; S3 depends
  on bucket ACLs the operator owns.

## Permission breadth (what to expect on install)

Network egress (declared in `clawhub.json#permissions.network`):

**Always-on (default workflows):**
- `pima.io` — MCP catalog, stock, locations, MPP checkout
- `www.buckmason.com` — public storefront aliases for the same MCP
- `cdn.shopify.com` — product imagery for lookbook generation

**Opt-in (only when the operator wires the dependency):**
- `api.openai.com` — image generation (`gpt-image-2`), try-on workflow only; requires `OPENAI_API_KEY`
- `api.cloudflare.com` + `*.pages.dev` — HTML lookbook deploy and default voting Pages Functions/KV via the operator-installed `wrangler` CLI; requires running `scripts/deploy-lookbook.sh`
- `api.stripe.com` — fully-agent-driven MPP checkout; reached only by `@stripe/link-cli`, never by the skill itself

**Documented alternatives (operator's own CLIs, the skill never invokes them):**
Listed in `clawhub.json#permissions.network_alternatives_documented_only` for full disclosure: Surge, Netlify, Vercel, Gist, S3, 0x0.st. Same trust model as `@stripe/link-cli` — operator-driven via tools the skill neither bundles nor calls.

Filesystem (declared in `clawhub.json#permissions.filesystem`):
- `<workspace>/profile.md` — read
- `<workspace>/wardrobe.md` — read (optional)
- `<workspace>/events.md` — read (optional)
- `<workspace>/lookbook/` — write (generated PNG/PPTX/HTML output, only on
  workflows that produce them)
- `~/.buck-mason-stylist/wishlist.jsonl` — read-write (cross-session
  wishlist + purchase history; slug + size + qty + lookbook_id + order_id +
  timestamps; no card data, no shipping address, no email)

## Reporting

- **Vulnerabilities**: security@pima.io
- **Spec questions**: open an issue at
  https://github.com/pima-io/buck-mason-stylist-skill
- **General docs**: see `SKILL.md`, `references/mcp-api.md`, `references/mpp.md`,
  `references/image-generation.md`

## Versioning

This security model applies to the current major version (0.x). Material
changes — new capabilities, new permissions, new outbound network hosts —
will trigger a minor version bump and a `CHANGELOG.md` entry calling out
the security delta.
