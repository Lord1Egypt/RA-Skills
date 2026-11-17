---
name: ai-quota-dashboard
description: "лимиты нейросетей, quota dashboard, остатки токенов, подписки и куки. Real-time multi-provider AI quota dashboard with secure token management and telemetry guide."
---

# AI Quotas & Subscription Limits Dashboard

Real-time telemetry, monitoring, and automated tracking for AI model quotas, subscription reset times, and API token balances across cloud and self-hosted providers (Google Antigravity, ElevenLabs, OpenRouter, xAI/Grok, Anthropic, OpenAI, Perplexity, LiteLLM, Ollama, and custom gateways).

---

## 1. Zero-Leakage Credential Standard (Mandatory Security)

To pass automated security audits (`skillspector`, `llm`, `vt`) and safeguard user privacy, all credential operations must strictly follow these rules:

1. **Zero Process Argument Leakage (`[TT5]`):**
   - Never pass API keys, tokens, or headers via command-line arguments (`argv`). CLI arguments are visible to `ps aux`, process accounting daemons, and system audit logs.
   - Credentials must be read strictly from isolated configuration files or environment variables.

2. **Strict Filesystem Isolation (`[PE3]`):**
   - All credentials files must reside in dedicated directories with restrictive permissions (`chmod 700 ~/.config/ai-quota-dashboard` and `chmod 600 config.json`).
   - Collector scripts must audit permissions and refuse execution if files are world-readable.

3. **Strict Origin Domain Pinning (`[SQP-2]`, `[E1]`):**
   - Outbound HTTP requests bearing authorization headers must enforce strict HTTPS and validate that the request target matches the pinned official provider domain. Requests to mismatched hosts or unverified proxies are rejected.

4. **Official Developer Credentials & Service Tokens:**
   - Always prioritize official developer API keys or read-only service tokens configured in your provider/gateway dashboard.
   - Do not scrape or extract third-party browser session cookies.

For complete specifications and audit scripts, see [references/security-cookie-guide.md](references/security-cookie-guide.md).

---

## 2. Telemetry Ingestion & No-Limit Fallback Strategies

When integrating an AI provider without public quota countdown documentation:

1. **Standard Telemetry Ingestion:**
   - Query documented developer endpoints (e.g., OpenRouter `/api/v1/credits`, ElevenLabs `/v1/user/subscription`, Ollama `/api/tags`).
   - Map response fields to standard telemetry: `used`, `limit`, `percent_used`, `unit`, and `resets_at` (ISO 8601 UTC).

2. **When Endpoints Lack Explicit Limit Numbers:**
   - **Unit Economics (Reverse Calculation):** When only account balance is returned (e.g. pay-as-you-go APIs), calculate remaining capacity by dividing balance by unit request price (`remaining = balance / unit_price`).
   - **Rolling Window Timers:** When limits operate on rolling intervals (e.g. 50 requests per 3 hours), track the cycle start timestamp locally and display an active countdown timer to reset.
   - **Local Usage Telemetry:** For self-hosted gateways without billing endpoints, aggregate runtime token usage statistics locally.
   - **Session Validity Heartbeat:** For flat-rate or unlimited tiers, verify endpoint availability via lightweight status ping (200 OK) and display an active pulse badge.

3. **Pick the window that actually consumes (multi-bucket providers):**
   - Some providers return several quota windows for the same model. Google Antigravity's `fetchAvailableModels` returns only the **5-hour** `quotaInfo` — short and self-resetting, so it reads ~100% even under heavy use, and a dashboard built on it looks frozen at full while usage is real.
   - The real consumption lives in a **separate endpoint**: `POST /v1internal:retrieveUserQuotaSummary` returns `groups[].buckets[]` with `bucketId` `gemini-weekly` (the weekly limit — the one that moves) and `gemini-5h`. Collect both and render them as two labelled bars, so a full short window and a draining weekly window are not confused.
   - Treat a never-moving percentage as a wrong-source symptom before suspecting the provider. Verify by reading the raw bucket values, not the rendered card.
   - Network hiccups on the quota call must **retry** (3 attempts) before falling back to cache: a silent cache fallback reproduces the same frozen 100% and hides the real value.

For full architecture details, see [references/api-reverse-engineering.md](references/api-reverse-engineering.md).

---

## 3. Collector Scalability & Zero-Flapping Standards

When monitoring expanding multi-account pools (e.g. 6+ Google accounts, multiple ElevenLabs keys) through outbound proxies:

1. **Subprocess Lifetime Budget:**
   - Sequential proxy handshakes scale with pool size. Set daemon runner timeout (`subprocess.run(timeout=...)`) to at least **60–75s** (not 25s) to prevent SIGKILL interruptions mid-poll.

2. **Proactive Pre-emptive Token Refresh (Zero Flapping):**
   - Never wait for a provider to return `401 Unauthorized` before attempting a refresh. Check stored `expires` timestamps. If `now > expires - 300s`, proactively request a fresh access token via `refresh_token` and persist it to disk before querying quota endpoints.

3. **Graceful Cache Fallback:**
   - Transient network timeouts (`URLError`, handshake lag, HTTP 502/503) must not wipe account telemetry or flag status as error. Retain the previous successful quota readings (`prev_cache`). An account is only truly in error if the token endpoint returns an unrecoverable revocation (`invalid_grant`) or credentials are missing.

4. **Dynamic Usability Badges & Display Focus:**
   - Capacity badges must compute active availability by filtering for usable quota (`remaining > 0%` and no auth error), not raw registered credential counts.
   - Filter auxiliary, legacy, or preview endpoints in the rendering layer so cards focus strictly on the active operational model (e.g., Gemini 3.8 Flash).
   - When a card must show more than one scale, render **one entry per bucket from a single list** — drawing a headline bar *and* a bucket list repeats the same value twice. Give every bar the same height and the same glow/animation class, or the un-animated one reads as "disabled".

5. **Pool edits fight the collector:**
   - The collector reads the credential file, refreshes tokens, and **writes the whole file back** on every cycle. Editing that file (adding/removing an account, replacing a token) while the collector runs is silently reverted.
   - Stop the collector service, make the edit, restart it, then confirm after a full cycle. See `antigravity-pool-diagnose` → `pool-management.md`.

---

## 4. Deployment & Networking Scenarios

The dashboard supports three operational modes:

1. **Strictly Local LAN (Home / Office Wi-Fi):**
   - Bind server to `0.0.0.0:8885` and restrict firewall to local subnet. Access via `http://<LAN_IP>:8885`.
2. **Remote Access Without Domain (External IP / VPN):**
   - Use encrypted WireGuard/Tailscale mesh VPN (zero router ports exposed) or router Port Forwarding with IP restrictions. Alternatively, use secure Cloudflare Tunnels.
3. **Custom Domain with HTTPS & Password Protection:**
   - Nginx reverse proxy with Certbot Let's Encrypt SSL. Enforce Basic Auth (`htpasswd`) so public bots cannot scrape private quota telemetry.

For complete Nginx blocks, firewall rules, and VPN instructions, see [references/networking-deployment.md](references/networking-deployment.md).

---

## 5. Mobile Standalone App (PWA Shortcut)

The dashboard includes full Progressive Web App support to run as a standalone fullscreen app on iOS and Android:
- **iPhone / iPad (Safari):** Tap the **Share** button (box with upward arrow) -> select **"Add to Home Screen"** -> Tap **"Add"**.
- **Android (Chrome):** Tap **Menu** (three dots) -> select **"Install app"** or **"Add to Home screen"**.

Launches in fullscreen mode with an app icon and dark theme status bar.

---

## 6. Verification Checklist

- [ ] `config.json` has permissions `0600` (`ls -l ~/.config/ai-quota-dashboard/config.json`).
- [ ] No tokens or keys appear in `ps aux` or shell history.
- [ ] Provider endpoints match pinned domain verification checks.
- [ ] Dashboard is accessible via LAN IP, VPN, or reverse proxy.
- [ ] PWA manifest loads cleanly and installs to mobile home screen.
