# Changelog

All notable changes to the B2B SDR Agent Template are documented here.

Changes sourced from upstream (openclaw/openclaw) are labeled with the originating commit SHA.

---

## [Unreleased]

## 2026-04-08 — v3.6.0

### Added
- **Graphify Knowledge Graph** — Sales intelligence powered by [graphify](https://github.com/safishamsi/graphify)
  Build queryable knowledge graphs from product catalogs, customer conversations, and
  market research. Cherry-picked and adapted for B2B SDR context:
  - Product catalog graph → cross-sell paths, product families, spec relationships
  - Customer intelligence graph → buying patterns, referral paths, stalled lead recovery
  - Market research graph → competitive landscape, expansion opportunities
  - Runtime query via `python3 -m graphify query "topic"` (BFS/DFS traversal)
  - Interactive HTML visualization for owner dashboard
  - New skill: `skills/graphify/SKILL.md`
  - Deploy: auto-installs Python + graphifyy, auto-uploads all local skills
  - Added to `SKILLS_RESEARCH` in skill profiles (`full` profile)

### Changed
- **Operator Bilingual Mode now opt-in** — disabled by default, enable via
  `operator_bilingual: true` in IDENTITY.md. Prevents unexpected self-chat messages
  for operators who don't need Chinese translation.

### Deployment
- `deploy.sh` now auto-uploads all local skills from `skills/` directory
- `deploy.sh` Step 3b: auto-installs Python3 + graphify on target server

---

## 2026-04-08 — OpenClaw v2026.4.7 upstream sync

### Breaking Changes

- **`/allowlist` commands now require owner authorization**
  `/allowlist add` and `/allowlist remove` previously could be issued by any user. They now require owner-level access. Update your admin flows if you delegated allowlist management to non-owner accounts.
  Upstream: v2026.4.7

- **Dangerous environment overrides now blocked at model layer**
  Model-facing tool calls can no longer override Java, Rust, Cargo, Git, Kubernetes, or cloud credential environment variables. If your workflows inject env vars through model instructions, migrate to explicit workspace config or deploy scripts.
  Upstream: v2026.4.7

- **`gateway config.apply` / `config.patch` writes blocked from model**
  AI cannot modify gateway config at runtime via these calls. This prevents prompt-injection-based config changes. Existing automation that patches config via the model layer must migrate to direct API calls with human approval.
  Upstream: v2026.4.7

### Added

- **Webhook Ingress Plugin** — inbound automation drives TaskFlows via shared-secret endpoints
  External systems (CRMs, zapier, n8n, custom webhooks) can now POST to OpenClaw and trigger or advance TaskFlows directly. This is the cleanest way to implement inbound-lead-to-SDR-flow automation: new lead in CRM → webhook → SDR agent starts outreach sequence.

  ```yaml
  # workspace config
  plugins:
    webhook-ingress:
      enabled: true
      secret: "{{WEBHOOK_SECRET}}"    # shared secret for HMAC validation
      endpoint: "/webhooks/crm"       # path exposed by the gateway
  ```

  Sample payload to start a TaskFlow:
  ```json
  {
    "event": "lead.created",
    "flow": "outreach-sequence",
    "data": { "name": "Li Wei", "company": "Shenzhen MFG Co", "phone": "+86..." }
  }
  ```
  Upstream: v2026.4.7

- **`openclaw infer` CLI Hub** — first-class provider-backed inference
  New top-level command for running inference tasks outside of conversation context: model completions, media generation, web lookups, and embeddings. Useful for batch processing leads or generating personalized outreach copy at scale.

  ```bash
  openclaw infer model --prompt "Draft a cold outreach message for Li Wei at Shenzhen MFG" \
    --provider anthropic --model claude-sonnet-4-6
  openclaw infer media image --prompt "Product catalog cover" --provider gemini
  ```
  Upstream: v2026.4.7

- **Memory/Wiki stack restored** — structured claims, evidence fields, freshness-weighted search
  The bundled memory-wiki stack is back with meaningful upgrades: claim/evidence structure, contradiction clustering, and freshness weighting. For SDR use: store verified facts about leads (budget signals, authority contacts, pain points) with evidence links. Freshness weighting ensures recent intel ranks higher than stale data.
  Upstream: v2026.4.7

- **New AI providers: Gemma 4 (Google), Arcee AI**
  Two new bundled providers. Gemma 4 supports `thinkingOff` semantics for faster, non-reasoning responses — good for high-volume first-touch outreach. Arcee AI includes the Trinity catalog, a curated set of task-specialized models. Added to `workspace/TOOLS.md` provider table.
  Upstream: v2026.4.7

- **Session compaction checkpoints + branch/restore UI**
  Sessions UI now shows compaction checkpoints. You can branch from any checkpoint (useful when a long sales conversation goes off-track) or restore pre-compaction state for audit/review. No config needed — automatic.
  Upstream: v2026.4.7

- **Pluggable compaction provider registry**
  Plugins can now replace the built-in context summarization pipeline. Enables custom summarization strategies (e.g., preserve all price quotes verbatim while compacting small talk).
  Upstream: v2026.4.7

### Fixed

- **HTTP requests aborted on client disconnect** — zombie sessions no longer hold resources when a channel disconnects mid-conversation. Improves stability on mobile channels (WhatsApp, Telegram) where connections drop frequently.
  Upstream: v2026.4.7

- **Docker/Podman auto-binding to `0.0.0.0`** — gateway now auto-binds to all interfaces inside containers. No manual `--bind` flag needed. Simplifies `docker run` and Compose deployments.
  Upstream: v2026.4.7

- **Prompt-cache runtime context exposure** — prompt cache statistics now surfaced to context engines. Helps diagnose unexpected API costs or latency spikes by showing cache hit/miss at runtime.
  Upstream: v2026.4.7

- **Ollama vision capability auto-detected** — no longer need to manually declare `vision: true` for Ollama vision models; capability is detected from API responses.
  Upstream: v2026.4.7

### Security

- Media byte limits enforced before base64 decode on Teams, Signal, and QQ Bot channels — prevents memory exhaustion via crafted media payloads.
- File upload URLs validated against HTTPS + Microsoft/SharePoint host allowlists — prevents SSRF via document upload.
- Cross-origin redirect body stripping for POST payloads — prevents credential leakage on redirects.
- Private-network blocking for main-frame document redirects — closes redirect-based SSRF vector.
- Workspace-only filesystem constraint enforced for document uploads.
  Upstream: v2026.4.7

### Documentation
- Updated `workspace/TOOLS.md`: Webhook Ingress Plugin section, expanded AI provider table (Gemma 4, Arcee AI)
- Updated `deploy/UPGRADE.md`: v2026.4.7 security breaking changes and migration notes

---

## 2026-04-06 — OpenClaw v2026.4.5 upstream sync

### Breaking Changes (run `openclaw doctor --fix`)
- **Legacy config aliases removed** — The following keys are no longer recognized at load time:
  - `talk.voiceId` / `talk.apiKey` → use canonical `voice.*` paths
  - `agents.*.sandbox.perSession` → use `sandbox.*` canonical paths
  - `browser.ssrfPolicy.allowPrivateNetwork`
  - `hooks.internal.handlers`
  - Channel/group/room `allow` toggles
  
  Run `openclaw doctor --fix` to auto-migrate. Backward compat shims remain active during the transition period.

### Fixed
- **WhatsApp: `blockStreaming` config option restored**
  The `blockStreaming` option (disables streaming responses on WhatsApp) was inadvertently removed in a prior release. Now restored. No config change needed — existing `blockStreaming: true` configs will work again.
  Upstream: v2026.4.5

- **Telegram: model picker checks and HTML formatting restored**
  Non-default model confirmations now correctly show the model name in HTML-formatted messages. DM voice-note transcription restored. Reaction persistence fixed across gateway restarts.
  Upstream: v2026.4.5

- **Security: plugin allowlists and `/allowlist` access controls hardened**
  Plugin-only tool allowlists are now properly preserved between restarts. `/allowlist add` and `/allowlist remove` now require owner access. Canvas bridge actions require exact normalized URL matches.
  Upstream: v2026.4.5

### Added
- **Multilingual Control UI (12 languages)**
  The OpenClaw control dashboard and mobile UI are now localized for Simplified Chinese, Traditional Chinese, Brazilian Portuguese, German, Spanish, Japanese, Korean, French, Turkish, Indonesian, Polish, and Ukrainian. Operators in China, Japan, Korea, and LATAM can now manage the SDR agent in their native language.
  Upstream: v2026.4.5

- **New AI providers: Qwen, Fireworks AI, StepFun, MiniMax**
  Four new bundled providers are now available as drop-in LLM backends. Qwen and MiniMax are particularly relevant for China-based deployments. Add to `workspace/TOOLS.md` provider table.
  Upstream: v2026.4.5

- **`openclaw status --verbose`** — New diagnostic flag showing prompt cache reuse statistics. Useful for debugging latency or unexpected API costs.
  Upstream: v2026.4.5

- **`openclaw plugins install --force`** — Allows replacing an existing installed plugin without manual removal. Useful for development workflows.
  Upstream: v2026.4.5

### Documentation
- Updated `workspace/TOOLS.md`: WhatsApp `blockStreaming` note, expanded AI provider table (Qwen, Fireworks, StepFun, MiniMax)
- Updated `deploy/UPGRADE.md`: v2026.4.5 breaking changes and migration steps

## 2026-04-05 — v3.4.0

### Added
- **Operator Bilingual Mode** — English for customers, Chinese self-chat sync for operators
  Non-English-speaking operators can now run a global English-facing SDR without needing
  to read English. The agent replies to customers in English and immediately sends a
  Chinese translation to itself via WhatsApp self-chat. Operators read Chinese in their
  "Message to myself" channel; customers only ever see English.

  How it works:
  - Customer sends any language → Agent always replies in English
  - After each English reply → Agent silently sends Chinese translation via self-chat
  - Owner reports (Pipeline daily, quote approvals, notifications) → always Chinese
  - No hardcoded numbers, no extra config — works with `selfChatMode: true` (default)

  Updated files: `workspace/AGENTS.md`, `skills/sdr-humanizer/SKILL.md`

## 2026-04-03

### Fixed
- **Telegram: per-account action configuration now correctly applied during discovery**
  If you run multiple Telegram bots (e.g., one per market), each account's `actions` block
  (reactions, polls, inline buttons) is now independently honored. Previously, only the
  top-level channel config was evaluated regardless of `accountId`.
  Upstream: `fb8048a188e5` — "fix: honor telegram action discovery account config"

- **Mistral AI provider: full transport compatibility**
  OpenClaw now correctly handles Mistral's API quirks when using Mistral as the LLM backend:
  - Uses `max_tokens` instead of `max_completion_tokens`
  - Suppresses unsupported OpenAI-specific params (`store`, `reasoning_effort`)
  - Applies automatically for `provider: mistral` and any custom provider whose `baseUrl`
    points to `api.mistral.ai`
  Upstream: `6ac5806a3957` — "fix(providers): honor mistral transport compat (#60405)"

### Documentation
- Added Multi-Account Telegram Setup guide to `workspace/TOOLS.md`
- Added AI Model Provider reference table (Claude, OpenAI, Mistral, Groq) to `workspace/TOOLS.md`
