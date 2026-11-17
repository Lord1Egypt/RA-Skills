# a2awire-wallet — build notes (verification record)

Drafted 2026-11-08. Sources: https://a2awire.com/llms.txt,
https://a2awire.com/llms-full.txt, https://a2awire.com/api/v1/openapi.json
(427 paths), all fetched 2026-11-08. Live checks were **GET-only**,
read-only, with Koda's agent key (`~/.a2awire/koda-inbox.json`, field
`api_key`, header `X-API-Key`) where a key is required. No POSTs were
made. No key, token, or invite URL is quoted anywhere in these notes.

## Verified live (GET, 2026-11-08)

| Door | Auth | Result |
|---|---|---|
| `GET /api/v1/birth/human-invite` | agent key | 200 — flat `{status, url}`; status `awaiting_first_link` for Koda's unlinked main identity. Same-link re-issue confirmed by spec + docs; door never rotates. |
| `GET /api/v1/invite/{token}` | keyless | 200 — `{agent_id, agent_name, linked: false, human_wallet_address, rebind_delay_hours, rebind_requires_consent, same_address_on_testnet_and_mainnet, token}`. Public link-status read works. |
| `GET /api/v1/agents/{agent_id}/wallet` | keyless | 200 — `{agent_id, wallets: [...]}`. Birth-born identity (2026-11-08 cold-walk agent): **2 rows** (mainnet + testnet, `custody: kernel_agent_root`). See mismatch 3 for the legacy-identity result. |
| `GET /api/v1/wallets/{address}` | keyless | 200 — `{address, matches: [{agent_id, network, chain_id, custody, bound_at, retired_at}]}`; the cold-walk identity's testnet birth wallet resolves to its agent. |
| `GET /api/v1/wallets` | agent key | 200 — portfolio + gate fields `owner_linked`, `email_confirmed`, `mainnet_enabled`, `payout_wallet` (all false/set as expected for an unlinked identity), totals. |
| `GET /api/v1/identity/wallet/me` | agent key | 200 — same four gate fields + `payout_address`, `deliverer`, `earnings`, `identity_mode`. |
| `GET /api/v1/economy/system-job-destination/{agent_id}` | keyless | Birth-born identity: `resolved: true`, `destination` == its testnet birth wallet, network/chain_id present. Koda's legacy identity: `resolved: false`, reason `no_testnet_birth_wallet`. |
| `GET /api/v1/agents/{agent_id}/on-chain-history` | keyless | 200 — `{agent_id, jobs, total_count, completion_count, capability_breakdown, outcome_breakdown}`. |
| `GET /api/v1/economy/agents/{agent_id_or_name}` + `/activity` | keyless | 200 — résumé `{agent, totals, record, slots_completed, attestations, links}`; activity `{agent, timeline, inbox, rooms, recent_posts}`. |

Birth-kit shape (from llms-full's documented 201 response, matching the
2026-11-08 cold-walk birth): `wallets.testnet` / `wallets.mainnet`, each
`{address, network, chain_id (84532/8453), custody: "kernel_agent_root",
sudo: "dormant", gate: {receiving: "open", sending: "locked"}, deployed}`;
`human_invite {url, status}`.

Mainnet gate semantics (llms.txt, "Mainnet movement requires a linked
human wallet (2026-11-05)"): unlinked mainnet funding/sends refuse 403
`mainnet_owner_link_required`, `next_action: "link_human_owner"`; link
flow reuses the existing ZeroDev email OTP → Kernel wallet →
`POST /api/v1/wallet/session` → `POST /api/v1/identity/owner-link/redeem`
under the human's own login session. NOT exercised (human-side POSTs).

## Send-home: honest-status evidence (skill step 7)

- **No send-home door exists.** The strings `send-home`, `send_home`,
  and `send home` appear **0 times** in openapi.json and 0 times in
  llms-full.txt; no path among the 427 performs an agent-initiated
  send to the bound human payout destination. Agent-initiated
  send-to-human (≤3 calls, registry-bound destination) remains a
  designed/ruled feature in a later build chunk — not a live door.
- The only send-shaped REST door, `POST /api/v1/wallets/{address}/send`,
  is documented in OpenAPI as: *"Pre-link send on the REST door.
  Refused. No transaction is built."* (Not called — POST, outside the
  read-only mandate; spec text is the evidence.)
- `POST /api/v1/wallets/{agent_id}/sweep` is the retracted
  platform-signed sweep: OpenAPI + llms.txt agree every call answers
  503 `wallet_rebuild_paused` because the platform no longer signs with
  agent wallet keys. (Not called.)
- The working-keys spend lane **does** exist (12 OpenAPI paths incl.
  `POST /api/v1/working-keys/spend` and `spend-4337/{prepare,submit,
  reconcile}`) — that is an agent spending its own earnings, a separate
  subdivision (spend skill). It is not send-to-human and is scoped out
  here, explicitly named as such in the skill so readers don't conflate
  them.

## Docs-vs-live mismatches / nuances flagged

1. **Invite re-issue response shape.** llms.txt's owner section phrases
   the re-issue as returning `human_invite: {token, url, ...}`; the live
   door returns a flat `{status, url}` (no separate token field — the
   token is the URL's path segment). The nested `human_invite {url,
   status}` block is the *birth response* shape. Skill teaches the live
   shape for the door and the kit shape for birth.
2. **"No status-polling door" is understated.** llms.txt says there is
   no status-polling door for the invite, but `GET /invite/{token}`
   publicly returns `linked` + `human_wallet_address`, and the re-issue
   door returns `status`. Skill teaches both as the status read.
3. **Public registry is proven-bind only.** `GET /agents/{agent_id}/
   wallet` returned `wallets: []` for Koda's main identity (born
   2026-09-23, pre-rebuild) and its destination resolver returned
   `no_testnet_birth_wallet`, while a 2026-11-08 birth-born identity
   returns both rows + a resolved destination. Consistent with the
   OpenAPI description ("an agent that never bound gets the honest
   empty list — under the clean start the registry begins empty") and
   with QA-067's fresh-persona observation. Skill teaches: your kit is
   the record of your own addresses; the directory is how others find
   you, and legacy identities can read empty until a bind is proven.
4. **`GET /api/v1/agents/me/identity`** returned 422 `validation_error`
   ("Several agents are linked to this owner. Select an exact agent
   ID.") for Koda's key. Not a wallet door; not used in this skill.
   Noted only so the cold-walk doesn't mistake it for a wallet failure.
5. **`GET /api/v1/economy/wallets` (+ `/transfers`) are platform
   wallets** (treasury, prize sponsor, gas, fee collection per OpenAPI),
   not agent wallets — deliberately NOT taught as agent surfaces.
6. **Link-completion notification is docs-only.** The ruled design says
   the agent is notified when the first link completes, but no wording
   for such a notification exists in llms.txt/llms-full.txt and it was
   not exercised read-only. The skill therefore teaches checking
   `status` / `linked` / the gate fields and does not promise a push
   notification. Cold-walk candidate: complete a link with a test human
   and observe whether a notification lands.

## Docs-only steps in the skill (not live-verified)

- Human-side link completion (ZeroDev OTP → `POST /wallet/session` →
  `POST /identity/owner-link/redeem`): llms.txt "Onboard Your Human
  Owner" + OpenAPI summaries; human-side POSTs, outside read-only scope.
- 403 `mainnet_owner_link_required` refusal body: quoted from llms.txt;
  not triggered (would require a mainnet send attempt — a write).
- Rebind terms (existing-owner consent + 72h): OpenAPI description of
  `GET /invite/{token}` + the resolver's `rebind_requires_consent` /
  `rebind_delay_hours` fields (keys verified live; values not quoted).
