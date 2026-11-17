---
name: connect-agents
description: "Connect your agent to another agent over A2A so they can ask each other for things. Use when a task needs something only the other agent can do, or when you are told to 'link' two agents and the setup is not working."
version: 1.0.0
license: MIT
metadata:
  tags: [a2a, multi-agent, setup, troubleshooting, agent-card]
---

# Connecting two agents over A2A

Two agents talk over A2A: one publishes an agent card, the other calls it with a
bearer token. The protocol is small. Almost everything that goes wrong is not
the protocol.

This is the list of what actually breaks, in the order you should check it. It
comes from doing it by hand between two agents on different machines, where each
step below cost real time.

## Before anything: what you are building

- The **called** agent exposes `/.well-known/agent-card.json` and accepts
  `message/send`.
- The **calling** agent holds that URL plus a bearer token.

Both directions need this if both are to initiate. Set up one direction, prove
it, then mirror it. Doing both at once means two things can be wrong and you
cannot tell which.

## The checks, in order

### 1. Is the inbound half actually on?

Listing an A2A plugin in a toolset list often registers only the **outbound**
tools — the ability to call others. The inbound listener is usually a separate
switch (an env var such as `A2A_PORT`).

Symptom: your agent can call out, nobody can call in, and nothing logs an error.

### 2. Is there a token?

Many implementations bind to `127.0.0.1` when no bearer token is configured.
The endpoint then answers only itself.

Symptom: `curl` from inside the container works, from anywhere else it times
out or refuses.

### 3. Is the endpoint reachable from outside?

If your platform gives one hostname per service and the dashboard already uses
it, A2A has no address. You need a second hostname pointing at the A2A port.

Check from a third machine, not from the host: `curl https://<host>/.well-known/agent-card.json`

### 4. Does the card advertise https?

Behind a TLS proxy the app often sees plain HTTP and writes `http://` into its
own card. Peers then send the bearer token in the clear.

Symptom: everything *works*. This one does not fail — it leaks. Read the card
and check the scheme yourself; set the public URL explicitly rather than
letting the app guess from the request.

### 5. Will the address survive a restart?

If the hostname is generated per deployment, every rebuild hands the peer a dead
address. Pin a stable name before you give it to anyone.

### 6. Will the token survive a restart?

Same trap: a token minted at start rotates on rebuild, and peers get 401 from an
agent that is running perfectly.

### 7. Is the peer configured with auth, not just a URL?

A bare URL is often accepted and stored with empty auth, so the call is
guaranteed to 401. The peer entry needs the token as well as the address.

### 8. Can the two hosts actually reach each other?

Two agents behind the same router or in the same cluster often cannot reach
each other by their public names, while both reach the open internet fine.

Symptom: DNS resolves, connection times out. This is the network, not the agent.

## When it still fails

Read the response body, not the status code. The useful distinctions:

- **401** — the token is wrong, missing, or not being sent. Check the peer entry
  first; a URL saved without auth is the common cause.
- **404 on the card** — you are talking to the wrong service on the right host.
- **timeout** — network path, not authentication. Go to check 8.
- **200 with HTML** — a proxy or a website answered instead of the agent. The
  hostname points somewhere else than you think.

## What to write down

Whatever you end up with, record the peer's **name, URL and how the token is
stored**. The next person to debug this — possibly you, in a month — needs to
know which of the eight things above were already settled.
