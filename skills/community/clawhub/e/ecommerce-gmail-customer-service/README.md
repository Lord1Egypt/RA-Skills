# E-commerce Gmail Customer Service

An OpenClaw Skill for handling e-commerce customer-service email safely in Gmail.

It turns incoming customer threads into auditable reply drafts: it separates multiple requests, classifies each one with a three-level intent taxonomy, matches the request to products and complete orders, checks current campaigns and policies, and writes one clear reply for the thread.

## What it does

- Handles pre-sale questions, order changes, shipping, damaged or missing items, returns, refunds, warranties, subscriptions, privacy requests, complaints, and more.
- Matches each request to the relevant product and complete order instead of guessing.
- Uses merchant policies and current campaign information when preparing a response.
- Lets the merchant enter one public storefront URL during setup, then safely discovers public product data, likely campaign pages, and policy sources with timestamps and provenance; when direct fetching fails, a guarded OpenClaw browser/browse fallback can produce the same validated snapshot.
- Creates Gmail drafts by default; sending is disabled until explicitly configured and tested.
- Escalates high-risk cases such as safety incidents, legal complaints, chargebacks, privacy requests, fraud, and requests containing `requires manual processing`.
- Can optionally learn approved writing preferences and reusable handling patterns from the previous 30 days of a dedicated support mailbox. This requires explicit user consent and stores only redacted summaries in `user_memory.md`.

## Prerequisites

- OpenClaw installed and working.
- A dedicated Gmail support inbox.
- Google Cloud OAuth credentials with the Gmail API enabled.
- `gogcli` installed for Gmail access.
- A public storefront URL, when the merchant has one.
- Read-only authenticated connections to the store or OMS for customer purchases, complete orders, private inventory, and customer-specific eligibility.

## Install

### Registry installation

After v1.2.8 is published, install the versioned registry release into the current Agent workspace:

```bash
openclaw skills install @ecomagenttools/ecommerce-gmail-customer-service --version 1.2.8
openclaw skills info ecommerce-gmail-customer-service
```

Do not use `--acknowledge-clawhub-risk` as a substitute for reviewing a release. Confirm that `openclaw skills info` reports the expected Agent-workspace path before completing OAuth or setup.

### Local checkout installation

For development or a reviewed local checkout, install into the current Agent workspace rather than the shared global skills directory:

```bash
git clone https://github.com/Ecom-Agent-Tools/Ecom-Agent-Tools.git
cd Ecom-Agent-Tools
openclaw skills install ./awesome-skills-for-ecommerce/ecommerce-gmail-customer-service
openclaw skills info ecommerce-gmail-customer-service
```

If OpenClaw is not configured yet, run `openclaw onboard` first. Do not place OAuth client files, tokens, or other secrets in this repository.

## Source, publisher, and release evidence

- Canonical public source: <https://github.com/Ecom-Agent-Tools/Ecom-Agent-Tools/tree/ecommerce-gmail-customer-service-v1.2.6/awesome-skills-for-ecommerce/ecommerce-gmail-customer-service>. The release tag and immutable commit are both part of the verification record; the tag alone is not the security boundary.
- The release owner is the `@ecomagenttools` organization publisher (display name: `EcomAgentTools`), not an individual persona. Inspect the registered files and the source release before granting Gmail access:

  ```bash
  clawhub skill verify @ecomagenttools/ecommerce-gmail-customer-service --version 1.2.6
  clawhub inspect @ecomagenttools/ecommerce-gmail-customer-service --version 1.2.6 --files
  ```

  **Current registry limitation:** the ordinary ClawHub CLI publish endpoint accepts `--source-*` fields but does not persist them as `server-resolved-github-import` provenance. Therefore v1.2.6 correctly reports `provenance.source=unavailable`; do not claim that it has registry-resolved GitHub provenance. The stricter source binding is only produced by ClawHub's authenticated **Import from GitHub** workflow, which re-fetches a public repository and records the resolved commit and path. Until that import has been completed for a later release, verify the public GitHub tag and signed release asset below rather than treating a README link as provenance.

- The GitHub Release attaches a deterministic ZIP with `release-manifest.json` listing the SHA-256 of every included file. The tag workflow signs the ZIP with a short-lived GitHub Actions OIDC/Sigstore certificate. Download the release asset and verify both the signer workflow and tag:

  ```bash
  gh release download ecommerce-gmail-customer-service-v1.2.6 \
    --repo Ecom-Agent-Tools/Ecom-Agent-Tools \
    --pattern 'ecommerce-gmail-customer-service-1.2.6.zip'
  gh attestation verify ecommerce-gmail-customer-service-1.2.6.zip \
    --repo Ecom-Agent-Tools/Ecom-Agent-Tools \
    --signer-workflow Ecom-Agent-Tools/Ecom-Agent-Tools/.github/workflows/ecommerce-gmail-customer-service-release.yml \
    --source-ref refs/tags/ecommerce-gmail-customer-service-v1.2.6
  ```

- ClawHub currently reports `signature.status=unsigned` for Skill versions. Do not represent that field as a cryptographic signature. The GitHub-attested release ZIP is the cryptographic publication proof. Once a later release is published through ClawHub's GitHub Import workflow, its server-resolved provenance can additionally bind registry files to the reviewed public source.

## First-time setup

Start the guided setup by asking your OpenClaw agent to configure the e-commerce Gmail customer-service Skill. The complete walkthrough is in [references/onboarding.md](references/onboarding.md).

The setup guides you through:

1. Creating the runtime configuration.
2. Entering the storefront URL and reviewing automatically discovered public products, campaigns, and policy sources.
3. Enabling the Gmail API and completing Gmail OAuth.
4. Connecting authenticated read-only order and private merchant data sources.
5. Naming the customer-service Agent and setting its persona.
6. Reviewing the system prompt, workflow, and optional AI disclosure.
7. Optionally approving a one-time 30-day onboarding history import, then separately choosing ongoing Draft-edit learning, existing-memory use for Drafts, and the global/category automatic-send controls.
8. Creating a disabled scheduled task and running end-to-end draft-only tests.

From the Skill directory, initialize and inspect the runtime files:

```bash
python3 scripts/configure.py init
python3 scripts/discover_store.py --url https://store.example --confirm-owner-request
python3 scripts/configure.py storefront confirmed --confirm-owner-request
python3 scripts/configure.py status
python3 scripts/configure.py verify
```

## Everyday use

Label customer email threads with `ECS/ToProcess`, then ask the Agent to process them with this Skill. The default result is a Gmail draft in the original thread.

Useful commands:

```bash
python3 scripts/configure.py show system-prompt
python3 scripts/configure.py show workflow
python3 scripts/configure.py show persona
python3 scripts/configure.py show config
python3 scripts/configure.py path persona
python3 scripts/configure.py path user-memory
python3 scripts/configure.py show auto-reply-permissions
python3 scripts/configure.py set disclosure on --confirm-owner-request
python3 scripts/configure.py set learning on --confirm-owner-request
python3 scripts/configure.py set memory-usage on --confirm-owner-request
python3 scripts/configure.py set auto-send on --confirm-owner-request
python3 scripts/user_memory.py clear --confirm-owner-request --confirm-delete-all
python3 scripts/auto_reply_permissions.py status
python3 scripts/auto_reply_permissions.py disable-all --confirm-owner-request
python3 scripts/configure.py schedule --timezone '<USER_CONFIRMED_IANA_TIMEZONE>' --quiet-hours '<USER_CONFIRMED_QUIET_HOURS_OR_NONE>' --confirm-owner-request
```

`show` is read-only and redacts configuration secrets. `path` prints the local file location; an owner may open that location with their own desktop tools, but this Skill never launches an editor, `open`, or another external program.

The optional AI disclosure is:

> This email is automatically processed by AI. If manual processing is required, please include the words "requires manual processing" in your reply.

Customers can request escalation by including `requires manual processing` anywhere in their reply.

## Safety model

This Skill starts in `draft_only` mode. Existing approved long-term memory participates in Draft generation by default once it exists, but it never replaces current order data, policies, platform rules, or applicable law. The owner can turn memory use off without disabling normal Draft generation.

Runtime prompt, workflow, persona, configuration, restore, schedule, browser-import, storefront confirmation, and whole-memory clearing changes are administrator actions. A one-time history import is allowed only during onboarding after explicit user consent and uses the owner-confirmed `--source onboarding` merge path. Ongoing Draft-edit snapshots and `--source draft-edit` merges require `learning.enabled=true` with recorded consent; that setting does not control history import or whether existing memory guides a Draft. `memory.usage_enabled` controls Draft-generation context only. Automatic sending is separate: the owner may change the global setting at any time, and every exact category is stored in independent permission state. A known sent AI Draft creates a pending confirmation event; only the owner's later confirmation enables that category. Clearing `user_memory.md` does not change category switches, and disabling one or all category switches does not change long-term memory. A first or changed storefront URL requires a current owner request and `--confirm-owner-request`; after review, `storefront confirmed` or `storefront none` requires the flag too. Only the exact URL with `storefront.status=confirmed` and a recorded `owner_confirmed_at` can refresh without a new request. Normal email processing must not make administrator changes. Before any cron task, record the owner-confirmed IANA timezone and quiet-hours policy, then run `python3 scripts/configure.py verify --require-schedule`.

Storefront discovery reads only public pages, respects `robots.txt`, rejects private-network and cross-host access, and uses strict page and response limits. If direct discovery cannot fetch or render the confirmed site, the documented browser/browse fallback remains read-only and its structured output must pass `scripts/import_browser_discovery.py --confirm-owner-request` before use. Public storefront content is candidate evidence only; complete orders and customer-specific decisions still require an authorized commerce connector.

Review the generated drafts before sending, especially during initial deployment and after changing a connector, system prompt, or workflow.

## Project files

- [SKILL.md](SKILL.md) — operational instructions and guardrails.
- [references/onboarding.md](references/onboarding.md) — guided setup.
- [references/storefront-discovery.md](references/storefront-discovery.md) — safe public storefront discovery and evidence rules.
- [references/intent-taxonomy.csv](references/intent-taxonomy.csv) — three-level customer-intent taxonomy.
- [references/reply-playbooks.md](references/reply-playbooks.md) — reusable reply approaches.
- [assets/default-system-prompt.md](assets/default-system-prompt.md) — immutable baseline safety prompt.
- [scripts/configure.py](scripts/configure.py) — runtime configuration and confirmed scheduling safeguards.
- [scripts/discover_store.py](scripts/discover_store.py) and [scripts/import_browser_discovery.py](scripts/import_browser_discovery.py) — guarded public-storefront discovery and validation.
- [scripts/draft_learning.py](scripts/draft_learning.py) and [scripts/user_memory.py](scripts/user_memory.py) — optional redacted long-term learning helpers.
- [scripts/auto_reply_permissions.py](scripts/auto_reply_permissions.py) — independent category automatic-reply switches and sent-Draft confirmation events.
- [scripts/validate_skill.py](scripts/validate_skill.py) and [tests/test_runtime.py](tests/test_runtime.py) — offline package validation and runtime smoke tests.
