# `claw-mem` CLI reference

The OpenClaw plugin (`@chainofclaw/claw-mem` after `openclaw plugins install`) mounts its CLI under a single root: `openclaw mem`. Memory queries and maintenance live as direct subcommands; SQLite maintenance, plugin config, and version info live as nested subgroups (`mem db …`, `mem config …`, `mem version`). Sibling plugins (`coc-node`, `coc-soul`) mount their own roots — there is no shared umbrella anymore. Anything not listed below (node lifecycle, soul backup, bootstrap, doctor, init) lives either in those sibling plugins or in the **standalone `claw-mem` binary** — see the appendix at the end if you installed that separately.

> **Inside an agent loop, prefer the registered tools** (`mem-search`, `mem-status`, `mem-forget`) over shelling out — the tool calls don't depend on PATH or shell context. The CLI commands below are for human/ops use from a terminal.

## Memory commands (`openclaw mem …`)

| Command | Purpose |
|---|---|
| `mem search <query>` | FTS5 full-text search over observations. Flags: `--limit <n>`, `--type <kind>`, `--agent <id>`, `--json`. |
| `mem status` | Counts of observations / summaries / sessions / agents, plus DB path and `tokenBudget`. Quick sanity check. |
| `mem forget <sessionId>` | Delete all observations for a specific session. |
| `mem peek` | Dump the memory context that would be injected on the next prompt (respects `tokenBudget`). Flags: `--agent <id>`, `--json`. |
| `mem prune` | Delete old observations. `--older-than <days>` keeps the last N days; `--before <iso>` for explicit cutoff. |
| `mem export <file>` | Dump observations + summaries + sessions to a JSON file. Flag: `--agent <id>` to scope. |
| `mem import <file>` | Load a previously exported file. Uses snake_case field names (matches SQLite schema). |

## DB commands (`openclaw mem db …`)

| Command | Purpose |
|---|---|
| `db size` | On-disk size of the SQLite DB + FTS index (main + WAL/SHM). Flag: `--json`. |
| `db vacuum` | Reclaim space after large deletes. Flag: `--json`. |
| `db migrate-status` | Check schema version against code's expected version. Flag: `--json`. |

## Config commands (`openclaw mem config …`)

| Command | Purpose |
|---|---|
| `config list` | Print the full effective config. Flags: `--from-disk`, `--section <name>`. |
| `config get <path>` | Read a dotted key (e.g. `tokenBudget`, `summarizer.mode`). Flags: `--json`, `--from-disk`. |
| `config set <path> <value>` | Write a key to `~/.claw-mem/config.json`. String-coercion is careful not to stringify hex keys or URLs. Flag: `--json` (treat value as JSON). |
| `config path` | Print the config file location. |

## `openclaw mem version`

Prints the loaded plugin version (matches `~/.openclaw/extensions/claw-mem/package.json`).

---

## Appendix: standalone `claw-mem` bin

The standalone binary is a separate artifact: install it with `npm i -g @chainofclaw/claw-mem`. It is **not** placed on PATH by `openclaw plugins install`. When you run it outside OpenClaw, it mounts the full command tree — including the umbrella commands that the OpenClaw plugin path does not expose:

- `claw-mem mem …` — same memory subtree as `openclaw mem`, just rooted at the bare bin
- `claw-mem db …` / `config …` — same as `openclaw mem db` / `openclaw mem config`
- `claw-mem node …` — re-mount of `@chainofclaw/node`
- `claw-mem backup … / did … / guardian … / recovery … / carrier …` — re-mount of `@chainofclaw/soul`
- `claw-mem bootstrap dev|prod` — one-shot bootstrap pipeline (starts hardhat, deploys contracts, installs a node, runs first backup)
- `claw-mem status` / `doctor` / `init` / `tools` / `uninstall` — cross-layer health + management

If you don't have the bin and don't want to install it: stick with `openclaw mem …` for memory work, install `coc-node` for node lifecycle, and `coc-soul` for backup/recovery. That's the supported in-OpenClaw composition.

---

## Appendix: in-place tarball install (when `openclaw plugins install` is unusable)

If `openclaw plugins install @chainofclaw/claw-mem --dangerously-force-unsafe-install --force` errors out (npm cache `EACCES` on the openclaw user, registry blocked, sandboxed runner without npm install permissions, etc.), you can install the byte-identical artifact manually — this completely bypasses OpenClaw's install pipeline and its `child_process` static scan:

```bash
# 1. Build/pack from source (or download the tarball from npm directly)
cd /path/to/claw-mem/packages/claw-mem
npm pack --pack-destination /tmp        # → /tmp/chainofclaw-claw-mem-<v>.tgz

# 2. Wipe the existing extension dir and extract the tarball in place
rm -rf ~/.openclaw/extensions/claw-mem
mkdir -p ~/.openclaw/extensions/claw-mem
tar -xzf /tmp/chainofclaw-claw-mem-<v>.tgz \
    -C ~/.openclaw/extensions/claw-mem --strip-components=1

# 3. Install runtime deps only (skips dev/build tooling)
cd ~/.openclaw/extensions/claw-mem
npm install --omit=dev

# 4. Restart the gateway and verify
openclaw mem status                     # → JSON with observation/summary/session counts
```

To download the tarball from npm without a source clone: `npm pack @chainofclaw/claw-mem@<version> --pack-destination /tmp` works as long as you have npm registry access; the rest of the steps are identical.

Always back the DB up before any version change: `cp ~/.claw-mem/claw-mem.db ~/.claw-mem/claw-mem.db.pre-<v>.bak` (or use whatever `dataDir` is configured if you've overridden it).
