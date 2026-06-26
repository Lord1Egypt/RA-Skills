# Guardians + social recovery

## Guardian set

Guardians are EOAs that can jointly initiate recovery or resurrection for an agent.

| Command | Effect |
|---|---|
| `guardian add --agent-id <id> --guardian 0x…` | Add a guardian (owner only) |
| `guardian remove --agent-id <id> --guardian 0x…` | Remove a guardian (owner only) |
| `guardian list --agent-id <id>` | List current guardians with ACTIVE / INACTIVE flags |

## Recovery flow (guardian-initiated owner migration)

Use when the owner has lost their private key but still has the guardians' trust.

1. Any guardian: `coc-soul recovery initiate --agent-id <id> --new-owner 0x…`
2. Other guardians approve: `coc-soul recovery approve --request-id <id>`
3. Once quorum (N-of-M) + timelock satisfied: `coc-soul recovery complete --request-id <id>`
4. Anytime before step 3, the **original** owner can veto: `coc-soul recovery cancel --request-id <id>`
5. `coc-soul recovery status --request-id <id>` shows current state at any point.

Quorum and timelock parameters are set on-chain at SoulRegistry deployment time. Typical config: 3-of-5 guardians with 48-hour timelock.

## Resurrection flow (agent-level)

Resurrection moves the agent's soul to a carrier so it can resume operation on different hardware. Distinct from recovery (which changes ownership). See [`carrier.md`](./carrier.md) for the carrier-side.

1. Guardian: `coc-soul guardian initiate --agent-id <id> --carrier-id <id>` — starts the request
2. Other guardians: `coc-soul guardian approve --request-id <id>`
3. Carrier: `coc-soul carrier submit-request --request-id <id>` — claim the request
4. `coc-soul guardian status --request-id <id>` — check readiness

Triggers (set via `backup configure-resurrection`):

- Explicit — a guardian manually initiates
- Offline — heartbeat missed for `maxOfflineDuration` seconds
- Key-hash — a pre-agreed key is submitted (disaster recovery)

## `recovery` vs `guardian` — don't conflate them

Both are guardian-touching, but they do different things:

| Subtree | Changes | Typical question |
|---|---|---|
| `coc-soul recovery ...` | **Owner address** of the agent (ownership migration after key loss) | "I lost the owner key — how do I transfer ownership to a new address?" |
| `coc-soul guardian initiate / approve / status` | **Resurrection request lifecycle** for moving the agent to a carrier | "Agent's host died — how do I get a carrier to pick it up?" |
| `coc-soul guardian add / remove / list` | **Guardian set membership** (owner-only admin) | "I want to change / add / list the guardian set" |

When you see "social recovery", clarify which one — the owner-migration `recovery` flow, or the guardian-mediated resurrection `guardian initiate` flow.

## Preconditions checklist (run before any recovery / resurrection action)

1. Agent is registered on-chain (`backup doctor --json` → `chain.registered: true`)
2. Guardian set is configured and reachable: `coc-soul guardian list --agent-id <id>`
3. Participants know the target `agentId` (bytes32)
4. For `recovery`: the new owner address is validated and signer-controlled
5. For resurrection (guardian-initiated): a registered carrier exists (`coc-soul carrier list`)

## Security rules

- Never transmit owner / resurrection / guardian **private keys** in chat — even split or encrypted fragments. Route key transfer through a local secure channel.
- It IS safe to share addresses, agent IDs, request IDs, transaction hashes.
- When users say "multisig" in this context, they mean the **guardian quorum threshold** (an N-of-M policy enforced at the SoulRegistry contract level), not a separate multisig wallet contract.

## Failure-mode triage

| Symptom | Cause | Action |
|---|---|---|
| `recovery approve` reverts with "not a guardian" | guardian set out of date | `guardian list --agent-id <id>` to confirm membership |
| `recovery complete` reverts before timelock | quorum reached but waiting period not elapsed | `recovery status --request-id <id>` shows `unlocksAt` — wait until past that timestamp |
| `recovery complete` reverts after timelock | owner cancelled mid-flight | `recovery status` will show `cancelled: true`; restart with a fresh `recovery initiate` |
| `guardian initiate` reverts with "carrier inactive" | target carrier deregistered or unavailable | `carrier list --include-inactive` to see all; pick an active one |
