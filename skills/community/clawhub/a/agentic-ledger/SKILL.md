---
name: agentic-ledger
description: 'Track every token and dollar your OpenClaw agent spends, set budget walls that actually refuse calls, and replay runs on free local models. Local-first: all data stays on this machine. Use when the user asks about cost, spend, tokens, budgets, usage reports, or what the agent has been doing.'
---

# Agentic Ledger

## What this is

Agentic Ledger is a small local proxy that sits between OpenClaw and the
model provider. Every call is recorded on this machine: the prompt, the
response, tokens, cost, latency, and errors. It can also refuse calls once a
budget line is crossed, which a dashboard alone cannot do. No account, no
cloud, no telemetry.

## Setup (one time)

Run these on the host machine (not inside the OpenClaw container):

```bash
pip install agentic-ledger
agenticledger start
agenticledger connect openclaw
```

If `agenticledger` is not on PATH after the install, it lives inside the
virtualenv you installed into: run it as `<venv>/bin/agenticledger`.

`connect openclaw` finds the OpenClaw config, backs it up, and points the
model provider's base URL at the proxy. It detects Docker installs and uses
`host.docker.internal` automatically, because `localhost` inside a container
is the container itself. Restart the OpenClaw gateway afterwards so the new
config loads.

No upstream configuration is needed: the ledger (0.8.1 and later) routes
each call to the provider matching its wire format, so Anthropic and
OpenAI agents both work out of the box. Only for a custom gateway or a
pre-0.8.1 ledger, set it explicitly and restart:

```bash
agenticledger config set proxy.upstream_url <your provider or gateway URL>
agenticledger stop && agenticledger start
```

Optional but recommended so cost questions run without an approval prompt
each time (this is what the ledger reads need; it pre-approves only curl):

```bash
openclaw approvals allowlist add --agent main "/usr/bin/curl"
```

Verify: the ledger's `/health` should answer (see "Finding the ledger's
address" below), and after the agent's next message `$LEDGER/api/sessions`
should show a session. The dashboard lives at http://localhost:8000 in the
host's browser.

The ledger never stores the provider API key. OpenClaw keeps its own
credentials; the proxy forwards them per call.

## Finding the ledger's address

On a bare install the ledger is at `http://localhost:8000`. Inside Docker,
`localhost` is the container itself, so the ledger is at
`http://host.docker.internal:8000`. Test with `/health` and use whichever
answers:

```bash
curl -s -m 3 http://localhost:8000/health || curl -s -m 3 http://host.docker.internal:8000/health
```

Use the address that worked as LEDGER in everything below.

## Answering cost questions

When the user asks what things cost or what the agent did, read from the
ledger, never estimate:

```bash
curl -s "$LEDGER/api/reports?days=7"
curl -s "$LEDGER/api/runs"
curl -s "$LEDGER/api/sessions"
```

If an access key is configured, add
`-H 'x-agenticledger-api-key: <key>'`.

Report in plain words: total spend for the window, the per-model breakdown
largest first, error counts (amber "blocked" calls are the budget wall
working, not failures), and cache savings when notable. For loops, give
iterations so far and the spend rate.

When an exec approval prompt appears for one of these reads, ask the user
to approve it, and in the same breath tell them the one-liner that stops
the asking permanently (it pre-approves only curl, nothing else):

```bash
openclaw approvals allowlist add --agent main "/usr/bin/curl"
```

If exec approval is unavailable or misbehaving (approvals loop without
executing), do not guess numbers. Either use a web fetch tool on the same
URLs (they are plain GET endpoints returning JSON) or hand the user this one
command to run on the host and paste back:

```bash
curl -s "http://localhost:8000/api/reports?days=7"
```

## Budget walls

To cap spending, set budgets in the ledger config and restart it:

```bash
agenticledger config set budgets.daily 5.00
agenticledger config set budgets.session 1.00
```

On OpenClaw setups, also set the refusal status to 402. OpenClaw reads a
429 as a rate limit and retries it over and over (observed live: one
question became twelve wall-hits); 402 is a final no that nothing retries:

```bash
agenticledger config set budgets.status 402
```

Once a wall is hit, the proxy answers the call with a clear refusal instead
of forwarding it, and the dashboard shows the blocked calls in amber. This
is a hard stop, not an alert.

## Replay: try a cheaper model on a real run

The dashboard can re-run a captured session or a whole run on another model,
including a free local one (LM Studio or any OpenAI-style server), and grade
the result: how many moments matched, which fumbled, and cost totalled both
ways. Point the user at http://localhost:8000 in their browser, pick the
run, choose Replay.
Useful before switching models: see whether the cheap model would have
survived the actual workload, not a benchmark.
