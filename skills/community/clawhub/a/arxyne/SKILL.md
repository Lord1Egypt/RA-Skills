---
name: arxyne
description: Run engineering simulations on your own machine and read each result with its provenance, across aerodynamics, vehicle dynamics, structures, thermal, acoustics, crash and electromagnetics. It lists the solvers and products this machine can run, records each case, reads past results back, and registers a solver image you built. Use when a CFD, structural, crash, thermal, acoustic or electromagnetic case is asked for, or when the numbers and provenance of a past run are needed.
---

# Arxyne

Arxyne runs an engineering simulation on this machine with Docker, and keeps the result in a
product record that other runs read. The tools come from the local `arxyne` MCP server.

## First, check that the tools exist

Look for `list_solvers` and `simulate` in your tool list before anything else.

**If they are there**, use them as this file describes.

**If they are not**, check the CLI first: `arxyne --version`. If that fails, Arxyne is not on this
machine — install it (below) and do not describe it as a registration problem. If the command
works, the CLI is installed but its server is not registered with this client. That is a setup
gap, not a broken install. Say so once, then carry on with the CLI, which reaches the same
server and prints the same answers. Do not retry the tools, and do not tell the user that
Arxyne is missing.

Registering the server is a choice of two transports:

- **HTTP**: start it with `arxyne mcp start`, then add `http://localhost:8100/mcp` to the client.
- **stdio**: add a server whose command is `arxyne mcp stdio`. Some clients want the full path
  to the binary.

In OpenClaw, one command does it, and one proves it:

```bash
openclaw mcp add arxyne --command arxyne --arg mcp --arg stdio
openclaw mcp doctor arxyne --probe
```

`arxyne: ok` means the server started and its tools were listed. Ask before you run these,
because they change the user's config.

The same work, either way:

| Task | MCP tool | CLI |
|---|---|---|
| List solvers | `list_solvers` | `arxyne solver list` |
| List products | `list_products` | `arxyne products` |
| Run a case | `simulate` | `arxyne run --domain <domain> --product <name>` |
| Read a result | `get_product_results` | `arxyne results --product <name>` |
| Record a value | `set_product_value` | `arxyne case set KEY=VALUE --source '<source>'` |

## Before the first run

1. Install the CLI if `arxyne` is missing: `pipx install arxyne` on Linux or macOS, `pip install
   arxyne` on Windows. Keep it current with `pipx upgrade arxyne`. Show the install guide at
   https://docs.arxyne.com/getting-started/installation/ when the user wants the other options.
2. What the install cannot supply: Python 3.11 to 3.14, since the wheels stop there, and Docker
   24+ installed and running (Docker Desktop on macOS and Windows). An NVIDIA GPU is needed only
   by the GPU solvers, XLB and DoMINO.
3. Run `arxyne doctor`. It checks Python, Docker, GPU, the solver images and the workspace.
   Report what it says. If Docker is missing or not running, stop there: nothing else works.
4. `arxyne onboard` walks the same checks, pulls images, and starts the MCP server, if the user
   would rather be guided.

A solver image is pulled on its first use, which takes minutes and a lot of disk. `arxyne pull
<name>` does it up front.

Products, layers and run output live in Arxyne's own data root, `~/.arxyne/` on Linux, not in the
working directory. Look there for a product's files.

## Find out what can run

1. Call `list_solvers`. It gives the solvers this install can dispatch, the domains they cover,
   and the products each declares.
2. Call `list_products`. It gives the products, and which solvers can run each.

Choose a product and a solver that declares it. If the user named neither, ask: a run pulls a
large image and takes real time. `arxyne solver coverage` shows the product x solver matrix when
the user wants to see the choice.

A product that does not exist yet is scaffolded on its first use, out of the solver's own scope
declarations. There is no create step, and no product to invent.

## Run a case

Call `simulate` with the product, the solver, and only the settings the user asked to change.
Omit the rest and the product's own defaults apply. The product's recorded values are seeded
into the case, so say where a number came from if the user asks.

On the CLI the same run is `arxyne run --domain aero --product ahmed --solver openfoam`.
`--domain` is required there, and `--solver` picks one; omit it and the domain's default solver
is used.

Useful shapes:

- One domain: `simulate` with the product and the solver for that domain.
- Every domain a product supports: `--domain all` on the CLI.
- A named scenario a solver declares: `--test <name>`, or `--all` for every one. `arxyne tests
  list` shows them.
- A one-run change: `--override key=value`. It changes that run only and writes nothing.
- `--set-targets` forces a refresh of the targets a run fills in (see below).

Report the KPIs the run returned, and the gate verdict if the product declares a target. A gate
that misses is a result, not a failed run: say which number missed and by how much.

## Read a past run

Call `get_product_results` for the product. It gives the recorded KPIs and the provenance of each
run, including the fingerprint that links image, case, and parameters.

Quote values as recorded. Do not recompute, round differently, or describe a number the record
does not carry.

## Targets, and what a run learns

A target the solver image declares is used as it is. A KPI with no target takes a band around
the value the first run measured, and the band width comes from the solver's own tolerance, or
ten percent when it declares none. Existing targets are never overwritten, whether the user set
them or a run learned them.

`--set-targets` is the explicit way to refresh them. Do not pass it unless the user asks.

To set a target by hand: `arxyne case set target_cd=0.30 --source 'agreed with aero' --product
ahmed`. A target needs a source like a value does. A bare key records the band its direction
implies.

## Record a value the user supplies

A value's identity is the source plus the name that source used. Nothing is renamed on arrival
and nothing is reconciled:

```bash
arxyne case set mass=1800 --source 'kerb weight' --unit kg --product ahmed
arxyne case values --product ahmed
```

A value with no source is refused, and two sources may state one name: both records are kept. A
case that needs one number for such a name refuses until it is told which source to build from,
`--from '<source>'`. A key no solver declares is stored and reported, never dropped.

Use `--override` for a number that belongs to one run. Use `case set` for a number that belongs
to the product.

## Run a solver image the user built

The built-in solvers are not a gate. Any image that satisfies the solver contract can be
registered, and it then runs exactly like a built-in one: same contract, same fingerprint, same
gate.

```bash
arxyne solver add --image ghcr.io/you/my-solver:1.0
```

- Conformance runs against the image before it is registered. A conformance failure is a
  statement about the image's `/solver/solver.yaml`, not about this install: report the failing
  rule as the tool gives it. `--no-conformance` exists and is not recommended.
- A private registry only needs `docker login` first. Registering is local: it writes one file,
  `~/.arxyne/solvers-registry.yaml`, contacts no Arxyne service, and needs no account.
- An air-gapped machine works: `docker load` the image, then add it by its local tag.
- After it registers, `list_solvers` shows it and `simulate` can dispatch it.

To build one, the image carries `/solver/solver.yaml` and a server that speaks the contract.
Point the user at the recipe for writing it:
https://docs.arxyne.com/guide/copy-for-llm/ and
https://docs.arxyne.com/guide/community-solvers/

Manage what is registered with `arxyne solver list`, `arxyne solver info --alias <name>` (the
full manifest: inputs, KPIs, compute), and `arxyne solver remove --alias <name>`. Publishing a
solver for other people is a separate step and never required.

## Say what happened

If a dispatch fails, report the error the tool returned and stop. Do not retry with a different
solver or product unless the user asks: the error is usually about the machine (Docker not
running, image not pulled, no GPU for a GPU solver) or about a setting the product does not
declare.

Never state a number, a gate verdict, or a provenance that the record did not give you.
