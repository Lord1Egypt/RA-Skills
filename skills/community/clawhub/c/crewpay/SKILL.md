---
name: crewpay
description: Launch Solana Pump.fun coins via CrewPay with KOL Autohire and on-chain fee-shares. Prefer pinned local MCP; dry-run first; dedicated low-SOL burner only; never paste wallet secrets into chat or tool args.
version: 1.1.6
homepage: https://crewpay.dev
metadata:
  openclaw:
    requires:
      bins:
        - curl
      anyBins:
        - npx
        - node
    primaryEnv: CREWPAY_API_KEY
    envVars:
      - name: CREWPAY_API_KEY
        required: true
        description: CrewPay agent API key (crew_ak_…). Claim via POST /api/agent/keys/claim if unset, then store here. Sent as HTTP header x-crew-api-key. MCP alias CREW_AGENT_API_KEY accepts the same value.
      - name: CREW_LAUNCHER_KEY
        required: false
        description: Local MCP only. Secret for a dedicated low-SOL burner launcher wallet (base58 or JSON byte array). Required only for real launch / wire-fees via local crewpay-mcp. Never your main or treasury wallet. Never paste into chat. Never pass as a tool argument (launcherKey/privateKey/secretKey are rejected). Do not document or run REST curls that put this value in headers from the agent session.
      - name: CREW_API_URL
        required: false
        description: API base URL. Default https://api.crewpay.dev
    homepage: https://crewpay.dev
---

# CrewPay — KOL fee-share launches for agents

Approval is optional. Operators can require human approval per key.

Use this skill when launching **Solana / Pump.fun** coins, hiring **KOLs**, or locking **on-chain creator fee-shares** through CrewPay.

## Why KOLs matter

Most AI-launched tokens get little or no traction without distribution, so hire or Autohire a real crew before spending SOL. Do not launch a solo / empty-crew meme and hope.

## Honest product facts (no hype)

- **Fee split (mode=`agent`):** **60% hired KOL crew · 15% launching agent · 25% CrewPay** by default. If the API key was claimed with a KOL `referralCode` / `referral_code` / `CREWPAY_REFERRAL_CODE`, the split is **60/15/5/20** (referrer KOL is an on-chain fee-share recipient).
- **Buyback is not live yet.** Treasury still locks on-chain (25% or 20% when referred); automatic market buybacks of a CREW token run only when operators configure buyback mint + key. An empty proof tape does **not** mean fee-shares failed.
- **Create + fee-lock may need two transactions.** Prefer atomic paths; if launch returns HTTP **202** / `feeShareLocked=false`, call wire-fees before considering the launch complete.
- **No price talk. No return promises.** Do not project market caps, “guaranteed” pumps, or ROI.

## Wallet & secret policy (non-negotiable)

| Env | Role |
| --- | --- |
| `CREWPAY_API_KEY` | `crew_ak_…` agent key → header `x-crew-api-key` (MCP also accepts `CREW_AGENT_API_KEY`) |
| `CREW_LAUNCHER_KEY` | **Local MCP process env only** — dedicated burner wallet secret |

**Burner wallet rules**

1. Create a **new dedicated launcher wallet** for CrewPay launches. Never use a main, treasury, CEX-withdrawal, or high-balance wallet.
2. Fund it with **only** the SOL needed for one launch + rent/fees (dry-run reports exact costs). Keep the balance low; top up per launch.
3. After a launch, leave leftover dust or drain back to cold storage — do not park large balances on the burner.
4. Rotate the burner if it was ever pasted into chat, logs, or a shared host.

**Never**

- Ask the human to paste a wallet private key into chat.
- Pass `launcherKey`, `privateKey`, `secretKey`, or `CREW_LAUNCHER_KEY` as a tool/MCP argument.
- Put `CREW_LAUNCHER_KEY` into `curl` / HTTP header examples from this agent session.
- Run unpinned `npx -y crewpay-mcp` (always pin the version below).

Hosted MCP at `https://mcp.crewpay.dev/mcp` is **publicMode**: API-key writes for discover/autohire/dry-run only. It **cannot** hold a launcher secret. Own-wallet launches use **local** `crewpay-mcp` only.

## Safety rules

1. **Always dry-run first** (`crew_launch_dry_run` or `POST /api/agent/launch/dry-run`). Dry-run spends no SOL and creates no mint; it returns `dryRunId` + `approvalUrl`.
2. **Human must open `approvalUrl`** and confirm on the CrewPay page before any real launch. Then call launch with the same body + `dryRunId`. Do not invent confirm phrases.
3. **Original memes only** — legitimate original art and names. No impersonation of brands, people, or other tokens.
4. Prefer **registered Autohire KOLs** when available; otherwise public Pump profiles are listings, not consent.
5. MAINNET only. Check `feeShareLocked` after every launch.

## Canonical URLs

- Site / agents: https://crewpay.dev · https://crewpay.dev/agents
- Discovery: https://crewpay.dev/llms.txt · https://api.crewpay.dev/api/agent
- OpenAPI: https://api.crewpay.dev/openapi.json
- Proof: https://crewpay.dev/proof · `GET https://api.crewpay.dev/api/proof`
- MCP HTTP (no launcher secret): https://mcp.crewpay.dev/mcp · card https://mcp.crewpay.dev/.well-known/mcp.json

Do **not** use `app.crewpay.dev` (no DNS).

## Preferred path — local MCP (pinned)

Install/run the **pinned** npm package (do not use `@latest` or unpinned `-y crewpay-mcp`):

```bash
npx -y crewpay-mcp@1.2.5
```

Configure MCP **env** (not tool args):

| Env | Value |
| --- | --- |
| `CREW_AGENT_API_KEY` | same as `CREWPAY_API_KEY` (`crew_ak_…`) |
| `CREW_LAUNCHER_KEY` | dedicated low-SOL burner secret (launch path only) |
| `CREW_API_URL` | `https://api.crewpay.dev` (optional) |

Tools: `crew_discover` · `crew_claim_key` · `crew_search_kols` · `crew_autohire` · `crew_launch_dry_run` · `crew_launch` · `crew_list_launches` · `crew_status` · `crew_wire_fees` · `crew_lock_holder_kol` · `crew_crank_remits` · `crew_proof`

**Launch flow via MCP**

1. `crew_claim_key` if `CREWPAY_API_KEY` / `CREW_AGENT_API_KEY` unset → store once in env.
2. `crew_autohire` (or pass an explicit crew totaling **100%** shares).
3. `crew_launch_dry_run` → review costs, crew, fee map, warnings; note `dryRunId` + `approvalUrl`.
4. **Stop — human opens `approvalUrl` and approves.**
5. `crew_launch` with the same body + `dryRunId` → expect `feeShareLocked=true`; if false, `crew_wire_fees`.
6. Optional: `crew_crank_remits` · `crew_proof`.

Images: PNG/JPEG/WebP/GIF only (SVG rejected). User description ≤**204** chars (final ≤240 with `Launched from CrewPay.dev platform`).

## HTTP helpers (no launcher secret)

Use REST for discovery, claim, autohire, dry-run, crank, and proof. **Do not** launch or wire-fees over raw `curl` from the agent — use local MCP for those.

Base: `${CREW_API_URL:-https://api.crewpay.dev}`  
Auth for writes: `x-crew-api-key: $CREWPAY_API_KEY`

### Discover (no auth)

```bash
curl -sS https://api.crewpay.dev/api/agent
curl -sS https://crewpay.dev/llms.txt
```

### Claim API key (if `CREWPAY_API_KEY` unset)

```bash
curl -sS -X POST https://api.crewpay.dev/api/agent/keys/claim \
  -H 'content-type: application/json' \
  -d '{"label":"openclaw"}'
```

Store the returned `crew_ak_…` once as `CREWPAY_API_KEY` (and `CREW_AGENT_API_KEY` for MCP). Rate limit: 5/hour/IP.

### Autohire a KOL crew (required for a real shot)

Most AI-launched tokens get little or no traction without distribution, so hire or Autohire a real crew before spending SOL — do not skip this.

```bash
curl -sS -X POST https://api.crewpay.dev/api/agent/autohire \
  -H "content-type: application/json" \
  -H "x-crew-api-key: $CREWPAY_API_KEY" \
  -d '{"name":"Desk Cat","ticker":"DCAT","description":"tips the tape","seats":3}'
```

### Dry-run (mandatory; no launcher secret)

```bash
curl -sS -X POST https://api.crewpay.dev/api/agent/launch/dry-run \
  -H "content-type: application/json" \
  -H "x-crew-api-key: $CREWPAY_API_KEY" \
  -d '{
    "name":"Desk Cat",
    "ticker":"DCAT",
    "description":"tips the tape",
    "mode":"agent",
    "autoHire":{"seats":3},
    "initialBuySol":0,
    "imageUrl":"https://example.com/coin.png"
  }'
```

Review `costs`, `crew`, `shareholders` / fee map, `warnings`, `vibe`, `dryRunId`, and `approvalUrl`. **Human opens `approvalUrl`**, then launch via **local MCP** (`crew_launch` with `dryRunId`), not curl.

### Crank + proof (no launcher secret required)

```bash
curl -sS -X POST https://api.crewpay.dev/api/agent/crank \
  -H "content-type: application/json" \
  -H "x-crew-api-key: $CREWPAY_API_KEY" \
  -d '{"mint":"<MINT>"}'

curl -sS https://api.crewpay.dev/api/proof
```

Crank is permissionless when the server ops key is set.

## Limits

| Field | Limit |
| --- | --- |
| name | 2–32 |
| ticker | 2–13 `[A-Z0-9]` |
| description | ≤204 user / ≤240 final |
| initialBuySol | 0–10 |
| Autohire seats | 1–10 |
| crew shares | must total 100% |

## Fee map reminder (agent mode)

| Slice | Default | Referred agent |
| --- | --- | --- |
| Hired KOLs | **60%** | **60%** |
| Launching agent | **15%** | **15%** |
| Referrer KOL | — | **5%** |
| CrewPay treasury | **25%** | **20%** |

Bind a referrer at key claim (`referralCode` / MCP `referral_code` / env `CREWPAY_REFERRAL_CODE`) — immutable afterwards. Invite links: `https://crewpay.dev/r/<code>`.

Buyback cron is **not** guaranteed live; fee-share lock is.

## References

- Full discovery: https://crewpay.dev/llms-full.txt
- Agents.md: https://crewpay.dev/AGENTS.md
- Source skill path in repo: `skills/crewpay/`
- MCP package (pinned): `crewpay-mcp@1.2.5` on npm
