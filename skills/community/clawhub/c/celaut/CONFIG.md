# Configuration Reference (`config.yaml`)

Nodo reads a single `config.yaml`, created from
[`config.example.yaml`](https://github.com/celaut-project/nodo/blob/stable/config.example.yaml) at install time. It lives in the
installation root (`TARGET_DIR`, default `/nodo`), i.e. `/nodo/config.yaml`. The
`main.MAIN_DIR` value inside it is the same root. Edit it directly, or use
`nodo config` (`bash/reconfig.sh` — edits in place with `yq -i`, preserving
comments, but writes **no** backup) or the `nodo tui` Config page (which also
preserves comments and additionally writes a `config.yaml.tui.bak` backup on each
change).

> ⚠️ nodo **rewrites** `config.yaml` on its first load: `auto` values such as
> `network.GATEWAY_PORT` and `ledgers.ergo.WALLET_MNEMONIC` are resolved to
> concrete values, and the file is re-dumped with `yaml.safe_dump`. This **strips
> all comments**, alphabetizes keys, and persists already-interpolated paths. So a
> live `config.yaml` is uncommented and reordered; `config.example.yaml` remains
> the commented reference.

This page documents the load-bearing keys. `config.example.yaml` is the most
complete reference — when in doubt, read it (though at least one live key,
`packer.PACKER_HEALTH_TIMEOUT`, is read by code but absent from the example).
Values below are the shipped defaults.

> Paths in `config.yaml` may reference other fully-qualified keys such as
> `${main.STORAGE}`; nodo expands them (see the `main` note below). After moving any
> runtime/binary, update the matching `dependencies.*` key and restart
> `nodo.service`.

## `main` — paths

| Key | Default | Meaning |
|---|---|---|
| `main.MAIN_DIR` | `/nodo` | Installation root. |
| `main.STORAGE` | `/nodo/storage` | Node storage root. |
| `main.CACHE` | `${main.STORAGE}/__cache__/` | Build/scratch cache. |
| `main.REGISTRY` | `${main.STORAGE}/__registry__/` | Service specification registry. |
| `main.METADATA_REGISTRY` | `${main.STORAGE}/__metadata__/` | Service metadata. |
| `main.BLOCKDIR` | `${main.STORAGE}/__block__/` | Content-addressed blocks (large files). |
| `main.DATABASE_FILE` | `${main.STORAGE}/database.sqlite` | SQLite database. |

> Interpolation only expands the **fully-qualified**, dot-flattened form
> `${main.STORAGE}` — a bare `${STORAGE}` is left literal. `install.sh`
> (`sync_config_main_paths`) rewrites these `main.*` keys to absolute paths at
> install time, so an installed `config.yaml` contains no placeholders.

The KyA acceptance marker is `${main.MAIN_DIR}/storage/.acceptedkya` — it derives
from `MAIN_DIR`, **not** from `main.STORAGE`, so relocating `STORAGE` does not move
it (see
[`USAGE.md`](./USAGE.md#non-interactive-use-automation--agents-️)).

## `dependencies` — local runtimes

Portable runtimes installed under `MAIN_DIR` (not system-wide): `python`, `java`,
`yq`, and `docker`. Override only to relocate the toolchain.

`dependencies.docker.*` (`BIN`, `DAEMON_BIN`, `BUILDX_BIN`, `DOCKER_SOCKET`) is an
**optional, node-local** toolchain used **only** by the local packer
(`packer.local: true`). It is **not** installed at node-install time — nodo runs
`bash/install_docker.sh` on demand and drives an **isolated** daemon under
`MAIN_DIR`, never the host's Docker.

## `virtualizers` — execution runtime

Cloud Hypervisor (`ch`) is the only virtualizer; the Docker virtualizer was
removed, so the node needs no local Docker install to *run* services.

| Key | Default | Meaning |
|---|---|---|
| `virtualizers.DEFAULT_VIRTUALIZER` | `ch` | Only `ch` is supported. |
| `virtualizers.ch.BINARY_PATH` | (set at install) | Cloud Hypervisor binary. |
| `virtualizers.ch.KERNEL_PATHS` / `INITRAMFS_PATHS` | per-arch | Guest kernel/initramfs per `linux/amd64` \| `linux/arm64`. |
| `virtualizers.ch.NETWORK_MODE` | `tap_bridge` | Guest networking mode. |
| `virtualizers.ch.MIN_MEM_MIB` / `DEFAULT_MEM_MIB` | `128` / `256` | Boot memory floor / default. |
| `virtualizers.ch.SECURITY.*` | — | rootfs path confinement, device-node policy, trusted-service allowlists. |

## `builder` — architectures the node can *execute*

These keys govern **which architectures the node can EXECUTE** — they drive
`SUPPORTED_ARCHITECTURES` (`src/utils/architectures.py`). Setting **both** to
`false` means the node executes nothing. Do **not** confuse them with the
packer-side pair below (`packer.ARM_PACKER_SUPPORT` / `X86_PACKER_SUPPORT`), which
only affect what `nodo pack` builds/announces: to limit *execution* architectures,
edit these `builder.*` keys, not the packer pair.

| Key | Default | Meaning |
|---|---|---|
| `builder.ARM_SUPPORT` | `true` | Node can execute `linux/arm64` services. |
| `builder.X86_SUPPORT` | `true` | Node can execute `linux/amd64` services. |
| `builder.WAIT_FOR_UNLOCK_MEMORY` | `60` | Seconds to wait for a memory lock to release during a build (`src/utils/utils.py`). |

## `communication` — peer messaging policy

`communication.*` tunes peer-to-peer messaging behaviour —
`SELF_ANNOUNCE_TO_CONNECTING_PEERS`, `SEND_ONLY_HASHES_ASKING_COST`, and
`DENEGATE_COST_REQUEST_IF_DONT_VE_THE_HASH` (read by `src/commands/connect.py` and
the execution balancer).

## `packer` — how `nodo pack` builds

The most important choice for anyone packing services. Full authoring format:
[`PACKING.md`](./PACKING.md).

| Key | Default | Meaning |
|---|---|---|
| `packer.local` | `false` | `false` → delegate the build to a **packer-service** microVM (no Docker on this host). `true` → build **locally** with nodo's isolated Docker toolchain (provisioned on demand). |
| `packer.PACKER_SOURCE_URL` | `""` | Manifest URL nodo downloads the packer service from directly when it needs to acquire it. Empty → resolve via the `source-application` core service. |
| `packer.PACKER_SERVICE_URL` | `""` | Override: `ip:port` base URL of an out-of-band packer-service. Used only when no packer id is set / no running instance is found. |
| `packer.ARM_PACKER_SUPPORT` / `X86_PACKER_SUPPORT` | `true` | Architectures `nodo pack` accepts/announces (**packer-side** — to limit what the node can *execute*, use `builder.*` instead). |
| `packer.PACKER_MEMORY_SIZE_FACTOR` | `2.0` | Local-packer only: RAM to lock as a factor of the exported filesystem size. |
| `packer.docker.BUILDX_NETWORK` / `BUILDX_BUILDER` | `host` / `nodo-hostnet` | Local-packer buildx settings. |

The **default-mode** packer is *not* configured here by URL — it is referenced by
its published content hash (service id) in the `core_services` list (below), which
is the single source of truth. nodo resolves a running instance of that id and
packs against its `ip:port`.

## `core_services` — bootstrap services (by id)

An array of `{name, id}` entries mapping a well-known role to a published service
hash. The node will only auto-resolve/run a missing service if it is reachable
through one of these configured core services; an empty list or a `"<SET_ME>"`
placeholder fails closed ("Service not allowed.").

| `name` | Role |
|---|---|
| `source-application` | Maps a service id → its downloadable sources (manifest URLs). |
| `packer` | The packer-service used by `nodo pack` (default mode). |
| `low-demand-fallback` | Opportunistic service run only when the node is idle (WIP). |

## `hashing`

| Key | Default | Meaning |
|---|---|---|
| `hashing.HASH` | `sha3_256` | Service/file identification hash. Accepts `sha3_256`, `sha256`, `shake_256`, `blake2b`, or a hex hash-id. |
| `hashing.CHECK_INTEGRITY_ON_SERVE` | `false` | Run integrity/migration automatically on `nodo serve`. |

## `network`

Controls exposure and remote execution. Key entries: `GATEWAY_PORT` (`auto`),
`PUBLIC_IP` / `EXTERNAL_INTERFACE` (what `nodo execute --remote` advertises),
`FREE_PORTS_RANGE` (ports used to expose services — match your router forwarding),
`DISABLE_EXPOSE_OUTSIDE`, `ISOLATE_INTERNAL_CHILDREN`, and `DEFAULT_EXECUTE_REMOTE`
(default remote for NAT/WSL2 nodes). See also [`NETWORKS.md`](https://github.com/celaut-project/nodo/blob/stable/docs/NETWORKS.md).

## `costs`, `timing`, `client`

Gas/cost economics (`EXECUTION_COST`, `BUILD_COST`, deposit factors, gas
thresholds), maintenance-loop timing, and client slot/expiration policy. Defaults
are sensible for a single dev node; change only with the economics in mind.

## `ledgers.ergo` — payments & reputation

There is a **single** Ergo wallet. Clients pay its derived P2PK address; excess is
swept to a cold wallet once thresholds are met. Payments/reputation require Java
(see [`INSTALL.md`](./INSTALL.md)).

| Key | Default | Meaning |
|---|---|---|
| `ledgers.ergo.WALLET_MNEMONIC` | `""` | The one wallet the node controls. Empty disables payments/reputation; `"auto"` generates a fresh mnemonic on first load. **Secret.** |
| `ledgers.ergo.NODE_URL` | `https://node.sigmaspace.io` | Ergo node used for chain access. |
| `ledgers.ergo.GAS_PER_ERG` | `1.0e+58` | Gas-to-ERG conversion. |
| `ledgers.ergo.reputation.REPUTATION_PROOF_ID` | `""` | This node's reputation proof id (reconciled by `nodo sync_reputation_proof`). |
| `ledgers.ergo.payments.HOT_WALLET_LIMITS` | `100` | Max ERG kept in the operational wallet before sweeping. |
| `ledgers.ergo.payments.COLD_WALLET` | `""` | Public address to sweep excess to. Empty disables sweeping. Never a mnemonic. |
| `ledgers.ergo.payments.DONATION_WALLET` / `DONATION_PERCENTAGE` | addr / `0.00` | Optional donation of a share of earnings. |

> ⚠️ `WALLET_MNEMONIC` is a secret. The `nodo tui` Config editor masks secret
> values; keep backups off-repo. Ergo transactions are **final and irreversible**
> (see [`KyA.md`](./KyA.md)).

## `general_flags`, `misc`, `logs`, `low_demand`, `publisher`

- `general_flags.SIMULATE_PAYMENTS` — dry-run payments (dev).
- `misc.MIN_BUFFER_BLOCK_SIZE` (`1.0e+7` = 10 MB) — inline/block threshold: files
  at or above this size are stored as content-addressed blocks (`main.BLOCKDIR`),
  smaller ones inline.
- `misc.VALIDATE_ON_IMPORT` (`true`), `misc.CONFIGURATION_REQUIRED`.
- `logs.DEBUG_MODE`, `logs.MEMORY_LOGS`.
- `low_demand.*` — opportunistic idle scheduler (off by default; WIP).
- `publisher.*` — how `nodo publish` uploads a service and how a freshly-published
  source gets registered (GitHub repo, chunking, auto-publish-tx settings).
