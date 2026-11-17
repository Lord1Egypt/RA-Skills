---
name: agentgates-swarm
description: "Deploy OpenClaw subagents to their own cloud server: start another OpenClaw agent on a confidential virtual machine (CVM, a sealed Intel TDX VM) for agents that hold keys or money, or on a cheap plain VM for workers with nothing secret, one per agent, for trading swarms or any swarm, by the hour, paid in USDC from a prepaid Agentgates balance. Its model is Agentgates inference."
allowed-tools: ["exec"]
metadata:
  openclaw:
    requires:
      bins:
        - node
      env:
        - AGENTGATES_COMPUTE_KEY
        - AGENTGATES_INFERENCE_KEY
    primaryEnv: AGENTGATES_COMPUTE_KEY
    envVars:
      - name: AGENTGATES_COMPUTE_KEY
        required: true
        description: "A compute key (agc_...) your owner minted on their prepaid Agentgates compute balance. It rents and renews machines from that balance and can do nothing else: it signs no payment, touches no wallet and destroys no machine."
      - name: AGENTGATES_INFERENCE_KEY
        required: true
        description: "An inference key (ag_...) on your owner's prepaid Agentgates inference balance. Every machine you start uses it as its model key."
    homepage: https://github.com/agentgates-ai/agentgates
---

# OpenClaw on a confidential computer

Start a new OpenClaw agent on a machine of its own: a confidential VM (Intel
TDX) rented by the hour from Agentgates, with a remote-attestation quote. One
machine per agent. You give it work over HTTPS, it answers, and its sessions
and memory stay on that machine's encrypted disk. Use it for a swarm: trading
agents that keep their keys and strategies sealed from the host, research or
data workers, or any agent that should run apart from you. Workers with nothing
secret on them can run on a plain VM for much less (below).

The new agent runs OpenClaw's own release image (`compose.yml` in this skill,
pinned by digest; OpenClaw is https://github.com/openclaw/openclaw). Its model
is Agentgates inference in the standard chat format, default `glm-5-3-flash`,
a confidential model in attested hardware.

## What your owner sets up once

1. A prepaid compute balance and a compute key on it:
   `POST https://api.agentgates.ai/api/compute/credits` with `{"amountUsd": 5}`
   (1, 5, 25 or 100), paid over x402 by their wallet, then
   `POST https://api.agentgates.ai/api/compute/keys` with `{"name": "my-agent"}`,
   signed by that wallet. Contract: `GET https://api.agentgates.ai/api/compute/docs`.
2. A prepaid inference balance and a key on it: the same two calls under
   `/api/inference/credits` and `/api/inference/keys`. Contract:
   `GET https://api.agentgates.ai/api/inference/docs`.
3. The two secrets in your environment: `AGENTGATES_COMPUTE_KEY` (agc_...) and
   `AGENTGATES_INFERENCE_KEY` (ag_...).

## Start a machine

```bash
node {baseDir}/scripts/openclaw-machine.mjs price
node {baseDir}/scripts/openclaw-machine.mjs start --name worker-1 --max-usd 1
```

`start` asks the API for the exact price of this purchase (a free `402` quote;
a draw from the balance costs that or less) and reads your compute balance. It
refuses when `--max-usd` is missing, the price is over it, or the balance is
short or cannot be read. Only then does it buy the machine (default
`compute.standard`, 1 hour; `--hours N` or `--minutes 15|30|45`, `--model <id>`
from `GET https://api.agentgates.ai/api/inference/catalog`), and it checks the
charge against `--max-usd` after, exiting with code 2 if the price moved past
it. It makes a fresh gateway token, seals it into the machine with the
inference key, keeps it in `~/.agentgates/openclaw-machines.json` (readable by
you only) and waits until the new OpenClaw answers, about 3 minutes after the
purchase (we measured 2 minutes 28 seconds and 2 minutes 42 seconds). The
machine's clock starts when it runs.

`compute.standard` (2 vCPU, 4 GB) is the smallest plan OpenClaw runs well on.
Measured with OpenClaw 2026.11.1: on 1 vCPU it gave no answer in 5 minutes,
and given room its memory peaked at 2.07 GB, more than a 2 GB machine holds.
On a Standard machine with `glm-5-3-flash` its answers took 8 to 58 seconds.

`compose.yml` reads `OPENCLAW_GATEWAY_TOKEN`, `AGENTGATES_API_KEY` and
`AGENTGATES_MODEL` from the new machine's sealed env, which `start` fills, and
merges them into OpenClaw's own settings file at every boot, so a new model
your owner sends with `POST /api/compute/deployments/{id}/update` takes effect
at the restart it brings. Your own environment needs only the two keys above.

## Cheap workers on plain VMs

A worker with nothing secret on it, such as a scraper, a crawler or a bot that
reads public data, can run on a plain VM for much less:

```bash
node {baseDir}/scripts/openclaw-machine.mjs price --plan compute.vm.standard
node {baseDir}/scripts/openclaw-machine.mjs start --plan compute.vm.standard --name scraper-1 --max-usd 0.2
```

`compute.vm.standard` (2 vCPU, 4 GB) is the smallest plain plan OpenClaw runs
on. A plain VM has its own IP address and any port, and no proof: its host can
read its disk, its memory and its env, the gateway token and the inference key
included. So keep wallet keys, exchange keys and private data on confidential
machines, give plain workers public work only, and have them send their results
back to you. The catalog marks a plain plan with `"proof": "none"`
(`GET https://api.agentgates.ai/api/compute/catalog`). A plain plan sells while
its host has room: when it has none, `price` and `start` say so and nothing is
bought.

A plain VM's https name is a proxy inside the machine, its certificate made
there once the machine runs; `start` waits for it, and `ask` sends the token
over https only. On a plain plan `start` also sends `OPENCLAW_TRUSTED_PROXIES`,
the private range that proxy reaches OpenClaw from: OpenClaw refuses calls
through a proxy it does not trust. In our run on `compute.vm.standard` OpenClaw
answered on the machine 3 minutes 37 seconds after the purchase, its https name
was live when we looked 9 minutes after it, and a task over that name took 21
to 43 seconds.

## Give it work

```bash
node {baseDir}/scripts/openclaw-machine.mjs ask worker-1 "Write a pre-trade checklist for a BTC perpetuals strategy and keep it in your notes"
node {baseDir}/scripts/openclaw-machine.mjs list
node {baseDir}/scripts/openclaw-machine.mjs renew worker-1 --hours 1 --max-usd 1
```

`ask` posts to the machine's own `POST /v1/chat/completions` (model
`openclaw`) with its token; `--session <id>` keeps a conversation apart.
Anyone holding that token is the machine's operator: never share it. The state
file is its only copy, so back it up; if it is lost, your owner can seal a new
token into the machine with `POST /api/compute/deployments/{id}/update`. Runs
side by side are safe: each change to the file takes a lock. Before you send a
confidential machine secrets, check its proof page,
`https://api.agentgates.ai/compute/verify/<deploymentId>`: its compose hash, OS
image hash and Intel TDX quote. A plain VM has no proof page: send it no
secrets.

A new OpenClaw's first answer may end by asking what to call it. That is its
first-run greeting: name it in your next message or go on with the work. Its
sessions live on the machine's disk, so after a restart the same `--session`
carries on where it was.

A machine stops when its paid time ends and its disk is kept a while after
(`GET https://api.agentgates.ai/api/compute/docs`, "Lifecycle"). Renew before
`expiresAt` to keep it. Your compute key cannot destroy a machine; your owner's
wallet can.

## Paying with x402 instead

If your agent pays its own way over x402 and your owner set a per-payment cap,
`node {baseDir}/scripts/openclaw-machine.mjs body --name worker-2 --minutes 15`
prints the create body (this compose, a fresh token, the inference key) and
saves the token. The body holds both secrets: keep it out of logs and send it
only to `https://api.agentgates.ai/api/compute/deployments`, with your x402
client. The `402` names the exact price on each network, asking it is free, and
your client signs that exact amount, so keep its per-payment cap at your
owner's budget. Then run `attach worker-2 <deploymentId>` and `list` until it
shows `running`.

A machine belongs to the wallet that paid for it. `list` finds it when that
wallet is your owner's, the one behind your compute key. If another wallet
paid, read the machine with that wallet (`GET /api/compute/deployments/{id}`
signed with `X-Wallet-Auth`, in the compute docs) and pass its endpoint:
`attach worker-2 <deploymentId> <endpoint>`. Any wallet may pay a renewal
(`POST /api/compute/deployments/{id}/renew`) over x402 the same way.

## If a machine never answers

If `start` reports the machine running but OpenClaw does not answer within 15
minutes, its sealed env may have been lost: the docs say a provision retry runs
without env values. Your owner can send them again with
`POST /api/compute/deployments/{id}/update` signed by their wallet, or you can
start another machine.

## Spending

This skill spends your owner's money, and only from the two prepaid balances
behind the keys they gave you. The balances are the hard limits: the API
refuses any purchase or model call its balance cannot cover, and your owner can
revoke either key at once. Each machine is drawn from the compute balance;
every model call a machine makes is drawn from the inference balance. The
template starts OpenClaw with no scheduled jobs: a machine calls its model
only when you ask it something, or on a schedule you asked it to keep.

`start` and `renew` require `--max-usd`, the most your owner lets one purchase
cost. The API takes no cap of its own, so this script checks it against the
API's quote just before buying and against the charge right after. Start or
renew a machine only when your owner asked you to or set a budget for it.
Asking the price is free and never charges. Ask your owner to keep on each
balance only what your agents may spend.
