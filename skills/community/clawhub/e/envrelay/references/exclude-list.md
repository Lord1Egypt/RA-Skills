# What to leave behind

The principle, in one line:

> **Configuration travels. Caches and dependencies stay and get rebuilt.**

A `node_modules` directory is not data. It is a deterministic function of
`package.json` and a lockfile, both of which are three kilobytes and both of
which are travelling. Carrying the output instead of the input turns a 2 GB
backup into a 60 GB one, takes an hour longer to encrypt, and produces a
`node_modules` built for the wrong architecture on the other end.

The same is true of `target/`, `~/.m2/repository`, `~/.gradle/caches`,
`~/.cargo/registry`, and every Docker layer on the machine.

Apply this list while sizing candidates in step 1, so the numbers you show the
user in step 2 are the real ones.

## Config that travels, next to the cache that does not

This is the part that is easy to get backwards. Each of these directories
contains both.

| Carry | Leave |
|---|---|
| `~/.npmrc` | `~/.npm/_cacache`, `node_modules/`, `~/.pnpm-store/`, `~/Library/pnpm/store` |
| `~/.cargo/config.toml`, `~/.cargo/credentials.toml` | `~/.cargo/registry`, `~/.cargo/git`, `target/` |
| `~/.m2/settings.xml`, `~/.m2/settings-security.xml` | `~/.m2/repository` |
| `~/.gradle/gradle.properties`, `~/.gradle/init.d/` | `~/.gradle/caches`, `~/.gradle/wrapper/dists`, `~/.gradle/daemon` |
| `~/.pypirc`, `~/.config/pip/pip.conf`, `~/.condarc` | `~/.cache/pip`, `~/Library/Caches/pip`, `.venv/`, `venv/`, `__pycache__/` |
| `~/.yarnrc`, `~/.yarnrc.yml` | `~/.cache/yarn`, `~/Library/Caches/Yarn` |
| `~/.gemrc`, `~/.bundle/config` | `~/.gem`, `vendor/bundle/` |
| `~/.docker/config.json` (auth), `~/.docker/daemon.json` | `~/Library/Containers/com.docker.docker`, `~/.docker/desktop`, image and volume data |
| `~/.rustup/settings.toml` | `~/.rustup/toolchains`, `~/.rustup/downloads`, `~/.rustup/tmp` |
| `.nvmrc` files in projects | `~/.nvm/versions`, `~/.nvm/.cache` |
| `~/.tool-versions` (asdf/mise) | `~/.asdf/installs`, `~/.local/share/mise/installs` |

The pattern: a small text file the user or their team wrote by hand goes; a
directory a tool filled in on its own stays.

## The full leave-behind list

### JavaScript / TypeScript

```
node_modules/
.pnpm-store/
~/.npm/_cacache
~/.cache/yarn          ~/Library/Caches/Yarn
~/Library/pnpm/store
.next/  .nuxt/  .svelte-kit/  .parcel-cache/  .turbo/
dist/  build/          # only when generated; check for a .gitignore entry
bower_components/
```

### Rust

```
target/                # every one, at every depth
~/.cargo/registry
~/.cargo/git
~/.rustup/toolchains   # reinstall with rustup, it is one command
~/.rustup/downloads
```

### Java / JVM

```
~/.m2/repository
~/.gradle/caches
~/.gradle/wrapper/dists
~/.gradle/daemon
~/.gradle/native
build/  out/  .gradle/  # per-project
```

### Python

```
.venv/  venv/  env/  .virtualenvs/
__pycache__/  *.pyc
.pytest_cache/  .mypy_cache/  .ruff_cache/  .tox/
~/.cache/pip           ~/Library/Caches/pip
~/.cache/uv            ~/Library/Caches/uv
~/miniconda3/pkgs  ~/anaconda3/pkgs
```

Note that a `.venv` often contains absolute paths baked into its scripts, so it
would not work on the new machine even if you did carry it.

### Go

```
~/go/pkg/mod
~/go/pkg/sumdb
~/.cache/go-build      ~/Library/Caches/go-build
```

### Ruby

```
~/.gem
vendor/bundle/
~/.rbenv/versions
```

### Containers and VMs

```
~/Library/Containers/com.docker.docker
~/.docker/desktop
~/.colima
~/.lima
~/.orbstack/data
~/.vagrant.d/boxes
~/VirtualBox VMs
*.vmdk  *.qcow2  *.vdi
```

Docker images are rebuilt from Dockerfiles and pulled from registries. A
machine's worth of layers is often 30–60 GB.

### Editors and IDEs

```
~/Library/Caches/JetBrains
~/.cache/JetBrains
<project>/.idea/       # workspace state; keep .idea/ only if it is committed
~/Library/Application Support/Code/Cache
~/Library/Application Support/Code/CachedData
~/Library/Application Support/Code/logs
~/.vscode/extensions   # reinstall from the extension list instead
~/Library/Caches/com.apple.dt.Xcode
~/Library/Developer/Xcode/DerivedData
~/Library/Developer/CoreSimulator     # tens of GB of simulator runtimes
```

VS Code extensions travel as a *list* (`code --list-extensions`), not as a
directory. See `software-inventory.md`.

### System and browser

```
~/Library/Caches/               # macOS, the whole tree
~/.cache/                       # Linux, the whole tree — but see the exceptions above
~/Library/Logs
~/.Trash  ~/.local/share/Trash
.DS_Store                       # every one
~/Library/Application Support/Google/Chrome/*/Cache
~/Library/Application Support/Firefox/Profiles/*/cache2
~/Library/Application Support/Slack/Cache
~/Library/Application Support/Spotify/PersistentCache
```

### Package managers themselves

```
~/Library/Caches/Homebrew
/opt/homebrew            # reinstall Homebrew, then the package list
/usr/local/Cellar
~/.local/pipx/venvs      # pipx reinstalls from the app list
```

### AI coding agents

Their state is the biggest surprise in a modern home directory — on the
machine this was written on, Codex held 59.6 GB and Claude Code 5.9 GB. What is
mechanical to leave behind:

```
~/.ollama/models                # re-pull; tens of GB of re-downloadable weights
~/.config/opencode/node_modules # reinstalled by the agent
~/.claude/plugins/marketplaces  # git checkouts, re-cloned from the plugin list
~/.claude/plugins/cache  ~/.claude/cache
~/.cursor/extensions            # replay the extension list instead
~/.codex/.tmp  ~/.codex/log     # scratch and logs
~/.claude/shell-snapshots       # per-session shell captures
~/.claude/paste-cache  ~/.claude/telemetry  ~/.claude/debug
~/.gemini/tmp
<repo>/.aider.tags.cache.v*     # per-repo, rebuilt on demand
```

Session transcripts — `~/.claude/projects/*/**.jsonl`, `~/.codex/sessions`,
`~/.gemini/config/projects`, `~/.local/share/opencode/storage` — are **not** on this
list, because they are a judgement call, not a default: see `ai-agents.md` for
the `none` / `recent` / `all` decision. Two things about them are not
judgement. Agent *memory* files never go in the leave pile even when every
transcript does; and a live SQLite database (`~/.codex/sqlite`, Cursor's
`state.vscdb`) is either copied with its `-wal`/`-shm` siblings while the
agent is closed, or not copied at all.

## Judgement calls

The list above is mechanical. These are not:

- **`~/Downloads`** — usually noise, occasionally the only copy of an installer
  or a licence file. Show the size and the ten largest items, and let the user
  decide.
- **`~/Library/Application Support/<app>`** — some apps keep real data here
  (Obsidian vaults, database GUIs' saved connections), some keep only cache.
  Check size, name the apps you find, ask.
- **`dist/` and `build/` inside a project** — regenerable in a build system,
  but sometimes checked in on purpose. If the project's `.gitignore` lists it,
  exclude it.
- **Datasets, model weights, media** — enormous and often irreplaceable. Never
  silently exclude these on size alone. Surface them individually.
- **`.git/`** — always carried when a repository is carried at all. It is the
  history; never treat it as regenerable.
- **Agent session transcripts** — the gigabytes, and the one pile that can
  contain a secret the user pasted a year ago. Size them per agent, offer the
  three tiers from `ai-agents.md`, and never search them to find out what is
  inside.

When in doubt, carrying something costs disk. Leaving out something
irreplaceable costs the user their work. Ask.

## Using the list

Pass the names that sit inside a carried directory to `scripts/stage_copy.py`,
one `--exclude` each, without the trailing slash:

```sh
python3 scripts/stage_copy.py ~/dev/site staging/files/home/dev/site \
    --exclude node_modules --exclude target --exclude .venv \
    --exclude __pycache__ --exclude .DS_Store \
    --hash --hash-prefix files/home/dev/site
```

Record what you excluded in the manifest entry's `excluded` field, so the
restoring side knows a `npm install` is waiting for it.

Never *delete* a build directory to make a backup smaller. Excluding is a
decision about the copy; deleting is a decision about the user's machine, and
it is not yours to make.
