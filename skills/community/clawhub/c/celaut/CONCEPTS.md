# Concepts

A short, self-contained glossary of the terms Nodo uses. It is the conceptual
companion to the task-oriented [`USAGE.md`](./USAGE.md), the [`PACKING.md`](./PACKING.md)
input format, and the payment/reputation model in [`ERGO.md`](./ERGO.md). The
underlying paradigm is defined in
[celaut-project/paradigm](https://github.com/celaut-project/paradigm).

## Celaut

The paradigm Nodo implements: a network in which **services** are specialized
software components encapsulated in binary files, and **nodes** are the computers
that discover each other, run those services, and pay each other for the work. It
is designed to be multi-ledger; Ergo is the ledger implemented today (see
[`ERGO.md`](./ERGO.md)) — "not necessarily the only ledger to be used."

## Node (`nodo`)

A single participant in the network. A node executes services (locally or by
delegating to peers), exposes a communication interface to the services it runs,
provisions their address + token, resolves their dependencies, and — in this
implementation — can pack projects into service specifications. See the node
responsibilities in the project [`README.md`](https://github.com/celaut-project/nodo/blob/stable/README.md).

## Service specification

A **deterministic, content-addressed** description of a program: its filesystem,
architecture, entrypoint, resource limits, API, and declared environment. It is
identified by the hash of its content (its **service id**), so the same
specification always has the same id, on any node. Produced by `nodo pack` (see
[`PACKING.md`](./PACKING.md)); exchanged as a `.celaut.bee` package.

- **`.celaut.bee`** — the importable/transmittable package (`nodo export <svc> <dir>`).
- **`.celaut` (raw)** — a raw specification for **hash verification only**; it is
  **not** importable (`nodo export <svc> <dir> --raw`).

## Instance

A **running** service — one launched specification executing inside a microVM.
The specification is the blueprint (`service id`); the instance is the live
process (`instance id`). One specification can have many instances. `nodo execute`
creates an instance; `nodo instances` lists them; `nodo kill` stops one.

## microVM (Cloud Hypervisor, `ch`)

Services **execute** inside isolated Cloud Hypervisor microVMs — not Docker
containers. `ch` is the only virtualizer. Docker, when used at all, is only for
the *packing* step (and only in the opt-in `packer.local` mode); it never runs a
service. Do not use `docker ps` to inspect a running instance — use
`nodo instances` / `nodo observe`.

## Gas

The unit of compute a client pays for. A client tops up its gas balance on a node
by generating a **deposit token** — a locally-generated identifier, not an
on-chain asset — and submitting an Ergo transaction that carries that identifier
(in register R4) plus some ERG; the node verifies the deposit belongs to the
client and that the funds reached its wallet, then credits gas. Nodes run a
single hot wallet (`ledgers.ergo.WALLET_MNEMONIC`); clients pay its derived P2PK
address, and excess is swept to an optional cold address. `nodo estimate` reports
a service's gas cost before you run it;
`nodo increase_gas` / `nodo decrease_gas` adjust a running instance. Full model:
[`ERGO.md`](./ERGO.md).

## Address and token provisioning

To talk to a running instance you need its **communication address** (`ip:port`,
from the ports the service declares in `service.json → api`) and an
**authentication token**. Providing these is a core node responsibility
(project [`README.md`](https://github.com/celaut-project/nodo/blob/stable/README.md)); the API's transport, `protocol` (e.g.
`grpc`) and `gas_amount_per_call` come from the service's own `service.json → api`
block (see [`PACKING.md`](./PACKING.md)).

## Block

A content-addressed chunk of storage. Large files in a service's filesystem are
not embedded inline in the protobuf; they are stored as **blocks** referenced by
their content hash, which deduplicates identical large files across services. See
*Filesystem Parsing Behaviour* in [`PACKING.md`](./PACKING.md).

## Peers and clients

**Peers** are other nodes this node has connected to; nodes reciprocally offer and
request services from their peers, so a node can run a workload locally or hand it
to a peer. **Clients** are the entities (nodes or external callers) that have
registered with this node and pay it gas. `nodo peers` / `nodo clients` list them.

## Service composition (dependencies)

Services can depend on other services. In `pack_config.json` you declare
`dependencies`; with `dependencies_env: true` the packer injects each resolved
dependency's content hash into the build as an environment variable, so a service
can address its dependencies by id regardless of which node runs them. See the
`dependencies` / `dependencies_env` reference in [`PACKING.md`](./PACKING.md).

## Core services

Celaut services the node treats as part of its own workflow, referenced by service
id (content hash) in `core_services` in `config.yaml`. The well-known roles today
are `packer` (builds services in a sealed microVM for `nodo pack`),
`source-application` (resolves a service id to its downloadable sources), and
`low-demand-fallback` (an opportunistic service run only when the node is idle;
WIP). See [`CONFIG.md`](./CONFIG.md).

## Reputation proof

An on-chain record (an Ergo token held in a "reputation box") that carries a
node's opinions about other nodes' reputation proofs. It lets peers assign each
other trust in a decentralized, transparent way. Nodes generate and submit these
proofs; publishing skill/coverage/benchmark/result entities uses the same
reputation-box machinery. Model: [`ERGO.md`](./ERGO.md).

## Coverage / Benchmark / Result / Skill

The four on-chain entity types in the **Unstoppable Skills** registry
([celaut-project/skills](https://github.com/celaut-project/skills)):

- **Skill** — a *problem* marker (e.g. "Optimal XAU/BTC Performance").
- **Coverage** — a service that addresses (covers) a Skill.
- **Benchmark** — a deterministic spec for how to measure a Skill.
- **Result** — a comparative measurement submitted against a Benchmark.

Agents "search for problems, not servers": pick a Skill, then read its Coverages,
Benchmarks and Results to choose a service. These are read via the Celaut Skills
MCP server; see the bridge skill in [`skill/SKILL.md`](./SKILL.md).
