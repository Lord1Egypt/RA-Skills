# Cross-Device Portability

**Protocol 3.3+**

A guild directory rarely stays on one machine forever. People carry it between
a laptop and a desktop, across Windows / macOS / Linux, and increasingly onto
phones and tablets. Some of what a guild stores is universally true; some of it
is only true for one operating system; some of it is only true for one specific
machine.

Agent Guild **does not move your files**. It has no sync command, no network
calls, no remote state. Carrying the directory is the user's choice of
mechanism — a folder-sync utility, a cloud drive, a private VCS checkout, a USB
disk. What the protocol guarantees is the part that actually breaks in
practice: **after the directory lands on a second device, every device can tell
"this applies to me" apart from "this belongs to another device".**

## 1. The three scopes

| Scope | Test | Where it lives |
|---|---|---|
| **shared** | Still true on any other device | Normal guild paths: `identity/`, `rules/`, `projects/`, `memory/`, `learnings/`, `skills/` |
| **platform** | True for one OS + architecture | Declared per platform: `tools/<name>/tool.json`, payloads under `tools/<name>/bin/<os>-<arch>/` |
| **host** | True for this one machine | `hosts/<host-id>/` |

One question decides the scope: **would this still be true on another device?**

- Yes → shared. "The user prefers conclusions first" is true everywhere.
- Only on the same OS → platform. A prebuilt `arm64` binary is one example.
- Only here → host. An absolute path like `/Users/alice/.my-agent/` is one.

## 2. Device identity

```
host-id = <os>-<arch>-<hostname>        e.g. macos-arm64-studio, windows-x64-desk
platform tag = <os>-<arch>              e.g. linux-x64, android-arm64
os ∈ { macos, windows, linux, android, ios }
```

The id is **computed at runtime, never read back from a stored file**. That is
deliberate: a copy of the guild arriving on a second device must not inherit
the first device's identity. `ag platform` prints what the current device
resolved to.

Two escape hatches, both honest:

| Variable | Use |
|---|---|
| `AG_HOST_ID` | Hostname is unstable, sensitive, or two devices should deliberately share one id |
| `AG_PLATFORM` | Probes are wrong (exotic shell, emulated arch), or you want to dry-run how another platform would resolve |

### `hosts/<host-id>/`

| File | Content | Written by |
|---|---|---|
| `host.json` | os / arch / link capability / python / first seen | `ag init` |
| `host-notes.md` | User-owned: facts true on THIS device only | User / agents |
| `VERSION` | Skill + protocol version installed here | `ag init`, `ag upgrade` |
| `groom.json` | Last data-hygiene run on this device | `ag groom` |

Every device gets its own directory, so several of them coexist in one guild
without ever overwriting each other.

## 3. Platform assets: declare, don't hardcode

A prebuilt binary is the classic portability trap: it works perfectly on the
machine that installed it and is dead weight everywhere else.

```
tools/doxygen/
├── tool.json
└── bin/
    ├── macos-arm64/doxygen
    └── linux-x64/doxygen
```

```json
{
  "name": "doxygen",
  "platforms": {
    "macos-arm64": { "exec": "bin/macos-arm64/doxygen" },
    "linux-x64":   { "exec": "bin/linux-x64/doxygen" },
    "windows-x64": { "install": "winget install -e --id DimitriVanHeesch.Doxygen" },
    "linux":       { "exec_on_path": "doxygen", "install": "sudo apt install doxygen" }
  },
  "any": { "exec_on_path": "doxygen" }
}
```

Resolution order for `ag tool doxygen`:

1. `platforms["<os>-<arch>"].exec` — a file inside the guild, if it exists
2. `platforms["<os>-<arch>"].exec_on_path` — on PATH
3. `platforms["<os>"]` — same two keys, arch-independent
4. `any.exec_on_path`, then plain PATH lookup
5. otherwise: **exit 3**, with the install hint for this platform

```bash
BIN="$(ag tool doxygen)" || { echo "not available here"; exit 0; }
"$BIN" Doxyfile
```

Agents **MUST** resolve platform assets this way instead of hardcoding a path
under `tools/`. An honest "not available on windows-x64 — install with …" is
useful on every device; a hardcoded macOS path is useful on exactly one.

A tool with no manifest is not an error — `ag port --apply` generates one that
declares the platform it can currently see, which is enough for other devices
to stop guessing.

## 4. Link direction invariant

**The guild owns its payloads. Links point inward, never outward.**

```
✗ ~/.agent-guild/skills/my-skill  ->  ~/projects/my-skill      (dead elsewhere)
✓ ~/projects/my-skill             ->  ~/.agent-guild/skills/my-skill
```

A link from the guild to an external path means the real files exist on exactly
one device; every other device sees a dangling link. `ag doctor` reports this
as a problem and `ag port --apply` fixes it by moving the payload into the
guild and linking the old external path back in.

Links that stay **inside** the guild must be relative
(`../skills/agent-guild/scripts/ag.py`), not absolute — an absolute link breaks
as soon as the user name, home directory, or drive letter differs.

## 5. Platform-scoped skills

A skill that only runs on one OS declares it:

```json
{ "name": "windows-console-encoding", "platforms": ["windows"] }
```

Absent declaration means portable, which is the common case. `ag port` points
out skills whose payload looks single-platform (only `.ps1`/`.bat`, only
`.command`) while declaring nothing.

## 6. Logs and ledgers across devices

| Artifact | Multi-device behaviour |
|---|---|
| `log/daily/<date>-<agent>.md` | Gains a `.<host-id>` suffix once more than one device is known, so two machines appending on the same day cannot collide |
| `current-focus.md` blocks | Header carries `@<host-id>` |
| Learning ledger entries | Carry a `**Host**:` field |
| `registry.json` | Device facts live in `agents.<name>.hosts.<host-id>`; flat fields remain as a compatibility mirror |

`ag status` shows only the agents installed on the current device and marks the
rest as living elsewhere; `ag status --all` shows every device. `ag doctor`
validates paths for the current device only — another machine's install is not
a defect here.

## 7. What not to carry between devices

Anything rebuildable, secret, or strictly local:

```
.trash/                 recoverable deletions, per machine
connectors/             credentials — keep them out of any shared carrier
**/.ag-lock             append-serialization locks, empty and per machine
**/__pycache__/         rebuildable
**/.venv/               rebuildable, platform-specific
**/node_modules/        rebuildable, platform-specific
.DS_Store, Thumbs.db    OS noise
```

`hosts/*/` is safe (and useful) to carry: it is how each device advertises what
it has. Nothing in it is ever interpreted as belonging to another device.

## 8. Moving to a new device

```bash
# 1. the directory arrives by whatever means you use
# 2. claim the device (idempotent, never touches existing data)
python3 <skill>/scripts/ag.py init <agent>

# 3. see what differs here
python3 <skill>/scripts/ag.py port

# 4. install what this platform is missing, using the printed hints
```

Existing devices need no changes. Their host directories, tool declarations and
registry blocks stay exactly as they were.

## 9. Audit and repair

```bash
ag platform        # device identity + link capability
ag port            # DRY-RUN report of everything non-portable
ag port --apply    # mechanical fixes only
ag doctor          # includes a portability section
```

`ag port --apply` performs only reversible, mechanical work:

- moves pre-3.3 host state into `hosts/<host-id>/`
- folds flat registry paths into the current device's block
- internalizes outbound links, then links the old path back in
- rewrites absolute intra-guild links as relative
- generates a missing `tool.json` declaring the platform it can see

It never rewrites user-written text. Machine paths found inside shared files
are reported with `file:line` for a human to fix, because only a human knows
whether the fact belongs in `hosts/<host-id>/host-notes.md` or should be
generalised.
