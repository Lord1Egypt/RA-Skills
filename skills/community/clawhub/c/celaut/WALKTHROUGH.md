# End-to-End Walkthrough

A single worked path from a project directory to a running, reachable service:
**pack → estimate → execute → get address + token → call → observe → kill.** It
also serves as the example-output reference for the commands in
[`USAGE.md`](./USAGE.md) (which documents every flag but shows no output).

> The output blocks below are **illustrative**. Hashes, ids, ports, and exact
> formatting will differ on your node and between versions; treat them as shape,
> not literal contract. The authoritative field lists live in
> [`USAGE.md`](./USAGE.md) and [`PACKING.md`](./PACKING.md).

Prerequisites: Nodo installed ([`INSTALL.md`](./INSTALL.md)), the KyA accepted, and
— for default-mode packing — a packer core service configured and running
([`CONFIG.md`](./CONFIG.md)).

## 1. Pack the project

Author the project per [`PACKING.md`](./PACKING.md) (a `Dockerfile` with **no**
`CMD`/`ENTRYPOINT`/`EXPOSE`, a `service.json` declaring `architecture`, `init`,
`api`, and any `envs`), then:

```bash
nodo pack ./my-solver
```

```
Preparing ./my-solver …
Building filesystem via packer-service (instance 9f2c… @ 192.168.200.7:8080) …
Parsed filesystem → celaut.Service specification
Imported service.
service id: 7b8f4e2a9c1d6f03a5e8b7c4d2f1a0e9b6c3d8f5a2e1b4c7d0f9a6e3b8c5d2f1
tags: my-solver
```

Keep the printed **service id** (or the `my-solver` tag) — it identifies the
specification for every command below.

## 2. Inspect what it declares

Never guess environment variables or ports — read them from the service.

```bash
nodo inspect my-solver
```

```
Service 7b8f4e2a…d2f1  (tag: my-solver)
architecture:      linux/amd64
init.entry_path:   /app/start.sh
resources:
  at_init:  mem_limit=104857600 (100 MB)  disk_space=2147483648 (2 GB)
  at_most:  mem_limit=524288000 (500 MB)  disk_space=10737418240 (10 GB)
api:
  - port 50051  transport=tcp  protocol=[grpc]
    gas_amount_per_call: { Solve: 100 }
envs (declared):   WORKERS, TIMEOUT
network:           [ipv4, public]
```

The `-e` values you may pass to `execute` are exactly the declared `envs`
(`WORKERS`, `TIMEOUT` here). The reachable port/protocol come from the `api`
block. See [Concepts → Address and token provisioning](./CONCEPTS.md).

## 3. Estimate feasibility and cost

```bash
nodo estimate my-solver
```

```
Execution feasibility: YES
Estimated gas:
  initial:      1.20e+08
  maintenance:  3.00e+06 / iteration
```

If it prints `Execution feasibility: NO`, the `reason` line names the failing guard
(usually `resources.at_most.mem_limit` vs the node's memory pool). Fix the service
or free resources before executing.

## 4. Execute — creates a running instance

```bash
# Pass only declared envs; --remote advertises the host-facing IP.
nodo execute --remote -e WORKERS 8 -e TIMEOUT 20 my-solver
```

`execute` prints the full `nodo inspect` dump of the launched service, then a
launch confirmation and the reachable endpoints:

```
🚀 Service launched successfully!
🌐 Endpoints available:
   http://203.0.113.10:50051
```

If the service declares no `http` slots (e.g. a `grpc/tcp` API like this one),
it prints `No endpoints available` instead — the endpoint list only enumerates
`http`-labelled slots. `execute` does **not** print the instance id, a status, a
virtualizer, or a token, and nodo emits no JWT anywhere.

To get the instance id and its API address, list the running instances:

```bash
nodo instances
```

```
ID                 SERVICE (TAG)   API                  VIRTUALIZER   GAS
c92ae2ff1b7d4a0e…  my-solver       203.0.113.10:50051   ch            1.20e+08
```

The instance **id is also its token** — the same hex value. There is no separate
authentication token to look up; use the id shown here both to address the
instance (`nodo observe`, `nodo kill`, …) and as the token on service calls.

## 5. Call the service

Use the address + token with the protocol the service declares (`grpc` here). The
token is the instance id from `nodo instances`. For example, with `grpcurl` and
the token as metadata:

```bash
grpcurl -H "authorization: <instance id>" -d '{"input": "..."}' \
  203.0.113.10:50051 my.solver.Solver/Solve
```

Each call is metered per `service.json → api.gas_amount_per_call` (here `Solve`
costs 100 gas). Top up a running instance with
`nodo increase_gas c92ae2ff1b7d4a0e… 100` (use the full instance id).

## 6. Observe live metrics and network activity

```bash
nodo observe c92ae2ff1b7d4a0e… --save ./captures
```

```
my-solver  c92ae2ff1b7d4a0e…   [ch]                CPU 12.4% (peak 41.0%)   MEM 88.2 MB (peak 130.1 MB)
Network (newest first):
17:15:41  OUT → instance c92ae2ff1b7d4a0e… [gateway] (parent)   TCP   142 pkts   38.4 KB
17:15:41  IN  ← 203.0.113.55:54210                              TCP    37 pkts    9.1 KB
… writing ./captures/my-solver_c92ae2ff1b7d4a0e…/{metrics.jsonl,capture.pcap}
```

`observe` answers "what is my instance doing right now." With `--save` it writes
`metrics.jsonl` (one CPU/memory sample per second) and, on a Linux/KVM host with
`CAP_NET_RAW`, `capture.pcap` (every frame, openable in Wireshark). `Ctrl-C`
exits. Full behaviour: [`USAGE.md`](./USAGE.md) → `observe`.

## 7. Kill the instance

`kill` requires root:

```bash
sudo nodo kill c92ae2ff1b7d4a0e…
```

```
Stopping instance c92ae2ff1b7d4a0e… … stopped.
```

The specification stays in the local registry (`nodo services`); only the running
instance is gone. To remove the specification too (also root):
`sudo nodo remove my-solver`.
