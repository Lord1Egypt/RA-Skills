# cli-butler

> An agent skill that gives any AI coding agent the ability to manage local CLI tools: inventory, install, upgrade, uninstall, reference-chain tracing, and capability enumeration.

## Why

Agents are great at installing tools and terrible at cleaning up after themselves. cli-butler makes provenance a first-class concept: every CLI belongs to exactly one **channel** (brew / npm / pipx / uv / cargo / gem / apt / manual / system), and the channel decides how it is installed, upgraded, and — critically — uninstalled. No more `rm`-ing brew-owned binaries or leaving launchd services half-disabled.

## Status

✅ **v0.1.1** — all six commands implemented, POSIX bash, zero third-party dependencies, 184 tests green, shellcheck clean. macOS first (SIP-aware system detection); apt supported on Linux.

- [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) — requirements (source of truth)
- [docs/provenance.md](docs/provenance.md) — channel model & ownership resolution
- [docs/design.md](docs/design.md) — architecture

## Install

```
npx skills add kelegele/cli-butler
```

## Usage

```
bin/list.sh                 # inventory all CLIs, grouped by channel with descriptions
bin/list.sh --by-function   # same inventory, grouped by purpose (AI agents, mobile, containers...)
bin/manage.sh info docker   # real path, symlink chain, owner, size, references
bin/manage.sh outdated      # what's stale, per channel with native outdated support
bin/manage.sh upgrade fd    # dry-run plan first; add --yes to execute
bin/install.sh cowsay       # routed to brew/npm/... by OS; journal writeback on success
bin/uninstall.sh cowsay     # dry-run plan; --yes runs the channel's uninstall
bin/refchain.sh docker      # where does this come from, what references it
bin/cap.sh git              # what can this CLI do
```

### What `list` looks like (real output, macOS)

```
== brew (706) - Homebrew-managed tools
NAME        VERSION   SIZE    DESC
docker      29.8.1    70.6M   Pack, ship and run any application as a lightweight container
...
== system (1198) - system-bundled (SIP-protected, NOT uninstallable)
...
```

### What `refchain` looks like (real output)

```
$ bin/refchain.sh docker
name=docker
path=/usr/local/bin/docker
chain=/usr/local/bin/docker -> /Applications/OrbStack.app/Contents/MacOS/xbin/docker -> /Applications/OrbStack.app/Contents/MacOS/xbin/docker-tools
realpath=/Applications/OrbStack.app/Contents/MacOS/xbin/docker-tools
owner=brew|managed
last-used=1790066193 (2026-09-22 16:36)
```

## License

MIT
