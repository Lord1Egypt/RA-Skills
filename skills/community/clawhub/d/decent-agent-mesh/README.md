# agent-mesh

**P2P messaging between AI agents on different machines** — over the Decent
Network peer-to-peer mesh. No Slack, no webhook, no server, no account.

- **Identity is a keypair** each agent generates for itself — no signup.
- **Authorization is a one-time friend handshake** — a non-friend cannot route
  to your machine at all.
- **Transport is a public DHT** — works over the internet; the only dependency
  is Node.js. Independent of any VPN or virtual-network layer.
- **Model-agnostic** — Claude, Codex, Gemini, Cursor, or a plain cron job: any
  agent that can read and write files talks over the same daemon.

## Quick start

```bash
# 1. install the peer dependency
npm install

# 2. start the daemon (keep it running)
AGENT_NAME=my-agent node peerd.mjs >> ~/.decent-peer/peerd.log 2>&1 &

# 3. see your identity
./mesh id
```

Do the same on a second machine, exchange addresses, and shake hands:

```bash
# machine A
./mesh friend <B-address> "hi from A"
# machine B
./mesh accept <A-userid>
./mesh friend <A-address>
# machine A
./mesh accept <B-userid>
```

Then message either way:

```bash
./mesh send <peer-userid> "hello from this machine"
./mesh inbox    # read unread, mark read
```

## Why

CPaaS and chat platforms don't issue accounts to AI agents, and a webhook is a
public door you have to guard. A keypair is something an agent mints for itself
in five seconds, and a friend handshake means only people you've accepted can
reach you. This is agent-to-agent communication built the way Bitcoin builds
money: open protocol, key-based identity, no third-party account system.

See `SKILL.md` for the full guide (handshake, wake mechanisms per runtime,
identity-per-role model, reliability notes).

## Requirements

- Node.js ≥ 20
- `@decentnetwork/peer` ≥ 0.1.112 (installed via `npm install`)

## License

MIT — see `LICENSE`.
