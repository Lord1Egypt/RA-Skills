# Software inventory

Two jobs: enumerate what is installed on the old machine, and install what is
missing on the new one. The commands below cover both directions.

The `manager` strings in the left column are the exact values that go into the
manifest's `software` array. The restore side dispatches on them, so spell them
this way.

## Enumerating

Run the batch script once instead of improvising twenty shell commands:

```sh
python3 scripts/sw_inventory.py --apps
```

One invocation per present manager, everything in one JSON: `software`,
`apps` (GUI applications — macOS via `system_profiler`, Linux via `.desktop`
files), `absent_managers`, and `errors` for any manager that was present but
failed to answer. A manager that errors does not sink the inventory; it lands
in `errors` and you tell the user about that one manager.

The table below is what the script runs under the hood. It stays here because
it is the spelling authority for `manager` strings, and the fallback when a
machine has a manager the script does not know.

Check that the manager exists before running it (`command -v brew`). A manager
that is not installed is not an error — it is just not part of this machine.

| `manager` | List installed | Notes |
|---|---|---|
| `brew` | `brew list --formula --versions` | One `name version` pair per line |
| `brew-cask` | `brew list --cask --versions` | GUI apps. macOS only |
| `brew-tap` | `brew tap` | Record these too — a formula from a third-party tap will not install without its tap |
| `npm-g` | `npm ls -g --depth=0 --json` | Parse `.dependencies`; drop `npm` itself. An entry may lack a `version` key (linked or unusually published packages) — omit the field, do not crash on it |
| `pnpm-g` | `pnpm ls -g --depth=0 --json` | |
| `yarn-g` | `yarn global list --json` | Yarn 1 only; Yarn 2+ has no global installs |
| `cargo` | `cargo install --list` | `name vX.Y.Z:` header lines, then indented binaries. Take the header lines |
| `pipx` | `pipx list --json` | Parse `.venvs`; the key is the package name |
| `pip-user` | `pip list --user --format=json` | Only if the user installs outside virtualenvs |
| `uv-tool` | `uv tool list` | |
| `gem` | `gem list --local` | Skip default gems (`gem list --local --no-details` still includes them; filter names marked `default:`) |
| `go` | `ls $(go env GOPATH)/bin` | Go records no install manifest; the binary names are the best available signal. Note this in `notes` |
| `mas` | `mas list` | macOS App Store. `id name (version)` per line — keep the id, it is what installs |
| `vscode-ext` | `code --list-extensions --show-versions` | `publisher.name@version`. Also `cursor`, `code-insiders`, `codium` if present |
| `jetbrains-plugin` | Read `~/Library/Application Support/JetBrains/<IDE>/plugins/` | Directory names. Best-effort; note it |
| `apt` | `apt-mark showmanual` | Debian/Ubuntu. Manually-installed only — the full list is thousands of dependencies |
| `dnf` | `dnf repoquery --userinstalled --qf '%{name} %{version}'` | Fedora/RHEL |
| `pacman` | `pacman -Qqe` | Arch, explicitly-installed only |
| `snap` | `snap list` | |
| `flatpak` | `flatpak list --app --columns=application,version` | |
| `asdf` / `mise` | `asdf current` / `mise ls --current` | Language runtime versions. Also carry `~/.tool-versions` as a file |

AI coding agents come through these same managers — `claude`, `codex`,
`@google/gemini-cli` and `opencode` under `npm-g`, Cursor and Windsurf as
casks, Copilot Chat under `vscode-ext`. The package is all this page covers.
What makes one of them *the user's* agent — config, MCP servers, skills and
plugins, sessions and memory — is `ai-agents.md`, and it is a separate,
larger job than reinstalling the binary.

A useful sweep for the tail end, before you decide the inventory is complete:

```sh
ls ~/.local/bin /usr/local/bin 2>/dev/null
```

Anything there that no manager claimed came from a tarball, a curl-pipe
installer, or a `go install`. Those cannot be replayed automatically — list
them in the manifest's `notes` so the user gets told rather than surprised.

## Versions

Record the version the manager reports. On restore it is **context, not a
constraint**:

- Newer on the new machine → normal. Say so and move on.
- Missing entirely → install at whatever the manager offers now.
- Pinning to the old version → only when the user asks, or when something in
  the restored config clearly depends on it (a lockfile, a `.tool-versions`, a
  CI config). Chasing exact versions across a machine migration produces a
  long tail of failures for very little benefit.

Language runtimes are the exception worth caring about. If `~/.tool-versions`
or `.nvmrc` files travelled, install those exact versions — projects will fail
to build otherwise.

The manifest records this distinction as `restore_mode`: absent or
`"compatible"` means whatever the manager offers now; `"exact"` means the
recorded version matters. Set `"exact"` only where something on disk pins it —
a `.tool-versions`, a lockfile, a CI config — or where the user says so. When
an `"exact"` version is no longer offered, that is `version-unavailable`:
report it and let the user decide, do not silently take the nearest.

Two more optional fields from v2 worth writing when you know them:

- **`source`** — where the package came from when it is not the manager's
  default registry: the tap name for a tapped formula (`brew tap-info
  --installed` says which formulae came from where), the registry URL for a
  scoped npm package. On restore this is the difference between "install"
  and "first decide whether to trust that source".
- **`runtime`** — for packages installed *into* a runtime (`npm-g`,
  `pip-user`, `gem`), the runtime and version they were installed against,
  e.g. `"node 22.11.0"`. Restore order depends on it: the runtime lands
  first, then the packages.

## Installing on the new machine

### The order

1. Get the package manager itself installed first (Homebrew, then everything
   else). Nothing below works without it.
2. `brew-tap` before `brew` — a formula from an untapped source will not
   resolve.
3. Language runtimes (`asdf`/`mise`/`nvm`) before the packages that need them.
   A `npm -g` install against the system Node will land in the wrong place.
4. Everything else.

### The diff, then the confirmation

Enumerate what is already installed and diff against the manifest in one shot:

```sh
python3 scripts/sw_inventory.py --diff <restore-dir>/manifest.json
```

**Batch first, single queries second.** The one-shot inventory answers "what
is already here" for every package at once; per-item commands (`brew info`,
`npm view`) are for the follow-up questions on the items that turned out to
need one. Running a query per manifest entry is how a 200-package restore
turns into 200 network round-trips and twenty minutes of nothing.

Present the groups the diff hands back:

- **Missing** — the actual proposal.
- **Already installed** — skip silently in the report, do not re-install.
- **Version differs** — usually leave alone; say what the difference is.
  For a `restore_mode: "exact"` entry the difference is actionable, not
  cosmetic.
- **Manager missing** — the manager itself is not on this machine yet;
  install it first, then re-run the diff for its packages.
- **Manager errored** — the manager is present but its enumeration failed
  (the error is in the JSON's `errors`). These packages are *unknown*, not
  missing: report the breakage, do not propose installs from a blind spot.

Then, for every package you are about to install, **verify the name resolves
through the manager itself** before proposing it:

| `manager` | Verify | Install |
|---|---|---|
| `brew` | `brew info <name>` | `brew install <name>` |
| `brew-cask` | `brew info --cask <name>` | `brew install --cask <name>` |
| `brew-tap` | `brew tap-info <user/repo>`, then show the user the repository URL it resolves to (`https://github.com/<user>/homebrew-<repo>` by default) | `brew tap <user/repo>` — per-item confirmation, never in a batch |
| `npm-g` | `npm view <name> version` | `npm install -g <name>` |
| `pnpm-g` | `pnpm view <name> version` | `pnpm add -g <name>` |
| `yarn-g` | `yarn info <name> version` | `yarn global add <name>` |
| `cargo` | `cargo search <name> --limit 1` | `cargo install <name>` |
| `pipx` | `pip index versions <name>` | `pipx install <name>` |
| `gem` | `gem list -r -e <name>` | `gem install <name>` |
| `mas` | `mas info <id>` | `mas install <id>` — by id, never by name |
| `vscode-ext` | Show the user the marketplace page for the exact id (`https://marketplace.visualstudio.com/items?itemName=<publisher.name>`) before installing; `code --list-extensions --show-versions` after, to confirm what landed | `code --install-extension <publisher.name>` — the id verbatim from the manifest, never a near-match |
| `apt` | `apt-cache policy <name>` | `sudo apt install <name>` — the user runs anything with sudo |
| `dnf` | `dnf info <name>` | `sudo dnf install <name>` |
| `pacman` | `pacman -Si <name>` | `sudo pacman -S <name>` |
| `snap` | `snap info <name>` | `sudo snap install <name>` |
| `flatpak` | `flatpak search <name>` | `flatpak install <name>` |

Two of these rows install more than a package and deserve the extra sentence
when you ask:

- A **tap** adds a third-party repository whose formulae run arbitrary code on
  every future `brew install` from it. Name the tap's full repository URL when
  asking, and confirm each tap on its own line — a tap is trust, not software.
- A **VS Code extension** runs inside the editor with the user's file access.
  The marketplace link above lets the user see the publisher before agreeing.

A name that does not resolve gets **reported, not guessed at**. Do not
substitute a similarly-spelled package: `brew install ripgrep` and `brew
install rg` are not the same decision, and a display-name resemblance is not
evidence.

The sharpest case of that rule: a package whose `source` is a private
registry, an internal tap, or anything with the company's name in it. **Never
look it up on a public registry, and never install what a public registry
offers under that name** — a same-named public package is the textbook
dependency-confusion attack. Ledger it `unknown-source` and hand it to the
user; they know where their internal registry lives.

Record every package's outcome in the restore ledger as you go, using the
`software` statuses from `references/manifest.md` — `installed`,
`already-present`, `compatible-alias`, `not-found`, `version-unavailable`,
`blocked-by-trust`, `blocked-by-tls`, `unknown-source`,
`requires-user-action`. The report at the end is then a query, not a memory
exercise.

Get the user's confirmation before installing. Per manager as a reviewed batch
is fine — one line per package, and they can strike any of them. Per item is
better when the list is short or anything on it is surprising.

Install with the manager's own command and nothing clever: one package name per
argument, no shell metacharacters, no interpolation of anything that came out
of the manifest into a shell string. The manifest crossed a machine boundary;
treat every string in it as untrusted input, because that is what it is.

### When the network says no

A batch of installs failing with the same error is one problem, not N
problems. Before retrying anything, classify the source once:

| Classification | The signature | What to do |
|---|---|---|
| `blocked-by-tls` | certificate errors, `SSL: CERTIFICATE_VERIFY_FAILED`, `unable to get local issuer` — corporate TLS interception, usually | Tell the user their machine needs the corporate CA installed. **Never** disable TLS verification, set `NODE_TLS_REJECT_UNAUTHORIZED=0`, pass `-k`/`--insecure`, or point at an http mirror — not to "just check", not once |
| `blocked-by-authentication` | 401/403 from a registry | The registry wants credentials the machine does not have yet. Point at the credential step or the user's login, do not guess tokens |
| `network-timeout` | timeouts, DNS failures | Say so; retry later is the user's call |
| `source-unavailable` | 404s or the whole registry unreachable while other sources work | That source is gone or renamed; report it |

One `curl -sI https://registry.npmjs.org` per suspect source tells you which
row you are in. Classify once, mark every affected ledger item with the same
status, and move to the managers that work.

### GUI applications

An application's identity is its **bundle id**, not its path. The same app
lives in `/Applications` on one machine and `~/Applications` on another;
`com.knollsoft.Rectangle` is the fact that survives the move. The inventory
script fills the manifest's `apps` array with name, version, bundle id, path
and (when `system_profiler` knows) the install source.

On restore, for each app in the manifest:

1. Is the bundle id already on this machine? (`sw_inventory.py --diff` checks
   this; a single lookup is `mdfind "kMDItemCFBundleIdentifier == '<id>'"`.)
   Found at a different path → `alternate-path`, which is *installed*, not a
   problem to fix.
2. Not found → route by `source`: `brew-cask` → the normal cask flow above;
   `app-store` → `requires-app-store`, the user signs in and installs, you do
   not; an MDM/enterprise install → `requires-enterprise-enrollment`;
   `dmg`/`unknown` → `unknown-source`, name it in the report with wherever the
   `notes` say it came from.

Do not install a GUI app from a source the manifest does not name. A cask that
happens to share the app's display name is a guess, and rule 3 applies.

### What does not replay

Say this out loud at the end rather than letting the user discover it:

- Apps installed from a `.dmg` or `.pkg` that Homebrew does not carry.
- Anything behind a licence key or a login (JetBrains, Adobe, Setapp…).
- `go install`ed binaries, unless the module paths were recorded in `notes`.
- Global npm packages installed against a Node version that is no longer here.
- macOS system settings, Dock layout, keyboard shortcuts — not software, and
  not in scope for this tool.

## Between two Macs

If both machines are Macs and the old one still exists, Apple's Migration
Assistant moves applications, the Keychain, and system settings in one step —
things this tool deliberately does not touch. It is worth mentioning: use
Migration Assistant for the machine, EnvRelay for the development environment.
They complement each other, and neither is a substitute for the other.
