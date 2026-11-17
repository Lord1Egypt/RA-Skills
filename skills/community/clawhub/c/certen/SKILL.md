---
name: certen
description: Give this agent a CERTEN identity and let it execute proof-gated actions on any chain it is linked to. It never spends without the owner's explicit consent.
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins: [node, certen]
    install:
      - kind: node
        package: "@certen.io/cli"
        bins: [certen]
---

# CERTEN for agents

CERTEN gives an agent an on-chain identity it does not custody a key for, accounts on any supported
chain that only execute what a validator quorum has proved, and a receipt a stranger can verify
without trusting the agent or its owner. Use it for anything where money is at stake and more than
one party has to agree: escrow legs, settlement, arbitration, insurance, a regulator's seat.

Do NOT use it for chat, discovery, or small per-message fees. A proof costs money (about $0.35 on
Base, about $1 to $4 on Ethereum) and takes 60 to 110 seconds. Putting that in front of a $3 fee
makes everything slow and proves nothing anyone needs proved.

Every command below prints JSON with `--json`, wrapped as `{"ok": true, "data": ...}` on success
and `{"ok": false, "error": {"code": ..., "message": ...}}` on failure. Read `data`, never the prose.

## Consent, before anything else

An identity costs money. Every proof-gated action costs money and moves the owner's funds. So:

1. Quote first: `certen quote --chain <chain> --json` and `certen balance --json`.
2. Show the owner the cost and the balance.
3. Ask, in plain words, whether to proceed. Do not proceed on silence.
4. Only then run the action. Never run `identity create`, `call`, `tx create`, or `governance
   *` without an explicit yes for that specific action.

If the owner has not told you which chain, use `base-sepolia` on testnet. It is the cheapest
chain CERTEN runs and every command here works on it.

## One-time setup (owner runs this, or you run it with consent)

```bash
certen keys generate --name agent --no-passphrase        # an Ed25519 key that never leaves this machine
certen signup --with-key agent --org-name <owner>-<handle> --no-keyring --json
certen doctor --json                                     # names the one thing blocking you, if any
```

`signup` proves you hold the key and returns an organization with a $10 trial. It prints only the
API key's prefix; the key is stored in `~/.certen/config.json`. Nothing goes into this skill's
environment, and nothing needs to.

**Sandboxed hosts:** if this agent runs in a container whose home directory is wiped between
sessions, `~/.certen` vanishes with it. Persist `~/.certen/keys/agent.json` and
`~/.certen/config.json` in the workspace and restore them at session start, or the identity you
created cannot be signed for.

## Where am I

Run `scripts/where-am-i.sh` (bundled) or the three commands inside it:

```bash
certen whoami --json          # org, key prefix, gateway, standing
certen identity list --json   # identities and their accounts per chain
certen balance --json         # spendable, held, and whether a shortfall is refused or only recorded
```

`balance.enforcing` is the fact that matters: `false` means the gateway meters and records
shortfalls but refuses nothing (testnet today); `true` means a run short of funds stops with a 402.

## Get an identity

```bash
certen identity create --name <handle> --sign-with agent --chains base-sepolia --wait --json
```

The result carries `id` (a uuid: use it in every later command), `adi_url` (the identity itself,
`acc://<handle>.acme`), and `chain_accounts[]` with an `address` per chain. That address is this
agent's `msg.sender` on that chain.

One identity, many chains — no new identity, no new key:

```bash
certen identity link-chain <id> --chain arbitrum-sepolia --json
```

## Execute something, proof-gated

Any contract call from the agent's account. The validators execute exactly this target, value and
calldata, after a quorum has proved it, or nothing.

```bash
certen call --identity <id> --chain base-sepolia --to <contract> \
  --fn "ship(bytes32,string)" --arg 0x<orderId> --arg "TRACK-1" \
  --sign-with agent --wait --json
```

- `--value <wei>` forwards native value with the call. Wei, as a string.
- An ERC-20 move is a call on the token contract: `--to <token> --fn "transfer(address,uint256)"
  --arg <to> --arg <amount in the token's base units>`. USDC has 6 decimals.
- `--proof-class on_cadence` batches the proof (cheaper, default in most kits); `on_demand` is
  immediate and costs more on Ethereum.

Wait for the outcome with `certen tx status <intent_id> --wait --json`. Two failures mean
different things:

- `status: failed` with `reason_code: target_reverted` — CERTEN did its whole job and the contract
  said no. A business outcome. Retrying the identical call reverts again.
- anything else — CERTEN did not complete. Infrastructure or funding. Read `certen errors --json`
  for the code you got.

## Hand the counterparty a proof, not a promise

```bash
certen proof get <intent_id> --json                 # the proof artifact, once it has anchored
certen proof share <proof_id> --hours 72 --json     # a link that resolves with NO API key
```

The artifact anchors 60 to 120 seconds after the leg completes. If `proof get` says there is none
yet, wait and retry; do not send the counterparty a bare transaction hash instead. They open the
link with `certen proof open <link>` and verify it against CERTEN, not against you.

## Being regulated

The owner can make their policy signer a required co-signer on this identity. From then on every
transaction this agent submits waits until the owner's rules approve it, and the agent cannot opt
out. The owner runs:

```bash
certen governance add-authority --identity acc://<handle>.acme \
  --authority acc://<owner-policy>.acme/book --sign-with agent --json
```

Once that is in place, a `call` or `tx create` returns with the transaction pending; the policy
signer decides and the transaction proceeds or is rejected. Treat `pending` as normal, not as an
error. `certen pending list --json` shows what is waiting.

## When something refuses you

- `CHAIN_NOT_PRICEABLE`: CERTEN's price book will not sell on that chain right now. That is on
  CERTEN's side; tell the owner and try another chain.
- `CHAIN_SUSPENDED`: the chain is paused while costs are investigated. Wait `retry_after_sec`.
- `402` / `INSUFFICIENT_BALANCE`: only when `enforcing` is true. `certen fund <usd> --chain
  <chain> --json` prints where to send testnet USDC.
- `no proof artifact yet`: normal for about two minutes after a leg completes. Wait.

Never work around a refusal by changing amounts, retrying in a loop, or using another identity.
Report it to the owner with the code and the exact message.
