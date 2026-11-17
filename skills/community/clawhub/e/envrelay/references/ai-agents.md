# AI coding agents

A machine that runs Claude Code, Codex, Cursor or their kin carries a second
environment inside the first one: the agents' configuration, the skills and
MCP servers they are wired to, and every conversation they have ever had.

It is worth treating as its own category for three reasons, and each one is a
way this step goes wrong if you treat agent directories as ordinary dotfiles:

- **It is where the disk went.** Session transcripts are the largest thing in
  a developer's home directory on a machine like this. Measured by this
  reference's own script on one real machine: Codex 59.6 GB (49.9 GB of it
  the sessions plane, 7.7 GB more of working state), Claude Code 5.9 GB
  (5.7 GB of it sessions), Ollama 9.0 GB of model weights. Carried blindly,
  the agents alone are a 75 GB backup — and the part of it worth having is
  measured in megabytes.
- **It is where the secrets are.** Not only the obvious `auth.json`: every MCP
  server definition can carry an API key in an `env` block, in a file that
  otherwise looks like ordinary config.
- **It is executable.** Restoring hooks, MCP servers and skills onto the new
  machine arms commands that run the next time the agent starts — before the
  user has typed anything. See rule 4 in `SKILL.md`.

## The five planes

Every agent splits the same five ways. Decide plane by plane, not directory by
directory.

| Plane | What it is | Default |
|---|---|---|
| **The agent itself** | the `claude` / `codex` / `gemini` binary, the IDE | not here — it is a package, see `software-inventory.md` |
| **Configuration** | `settings.json`, `config.toml`, `mcp.json`, hooks, the agent's own instruction file (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) | carry — small, hand-written, irreplaceable |
| **Extensions** | skills, plugins, subagents, slash commands, marketplaces, IDE extensions | split: hand-written travels as files, marketplace-installed replays as a list |
| **Working state** | session transcripts, project state, agent memory | judgement — this is where the gigabytes are, and memory is not transcripts |
| **Credentials** | `auth.json`, `oauth_creds.json`, Keychain items, MCP `env` blocks | credential rules, and most are better re-authenticated than carried |

## Enumerating

```sh
python3 scripts/agent_inventory.py
```

One pass over every agent layout the script knows, reporting for each: whether
the CLI is on `PATH` and its version, every config/extension/session/credential
path that actually exists with its size, the extensions by name, and the MCP
servers with **key names only, never values**. It reads no session file and no
credential file.

Sizes are measured by default because they are the whole point of the session
decision; `--no-sizes` skips the walk when you only need the shape (a second
rather than a few). `--recent-days N` adds, per path, the bytes touched in the
last N days — the number the three-tier session decision below actually turns
on. `--agents claude-code,codex` narrows the pass. `--diff MANIFEST.json`
compares a backup's `agents` array against this machine and is the first thing
to run on the new one.

Two parts of its output deserve reading rather than skimming:

- **`unclassified`** — files and directories under an agent's root that the
  script has no rule for. Agent layouts change with every release; an
  unclassified 900 MB directory is a decision you have to make, not something
  to let the default swallow.
- **`likely_secret_keys`** on an MCP server — the subset of `env_keys` (the
  names of environment variables set inline in the config) whose names look
  like secrets. Those values are live API keys sitting in a plaintext file.
  `env_keys` is the full list: read it too, because a secret can be named
  anything.

The tables below are what the script probes. They stay here because layouts
move and because a machine will always have an agent the script does not know.
**Check that a path exists before claiming it is in the backup** — an agent
you did not find is not an agent that is not there.

## Where the planes live

### Claude Code (`claude`)

| Path | Plane | Note |
|---|---|---|
| `~/.claude/settings.json`, `settings.local.json` | config | permissions, hooks, model, statusline |
| `~/.claude/CLAUDE.md` | config | the user's global instructions; usually the single most valuable file here |
| `~/.claude.json` | config **and** credential | one JSON holding `mcpServers` (with their `env`), `oauthAccount`, and a per-project history blob for every directory ever opened. Carry the parts that matter; do not carry it whole without looking at what it grew into |
| `~/.claude/skills/`, `agents/`, `commands/`, `hooks/` | extensions | hand-written. Carry as files |
| `~/.claude/plugins/installed_plugins.json`, `known_marketplaces.json` | extensions | the replayable list — carry these two files |
| `~/.claude/plugins/cache/`, `marketplaces/` | extensions | git clones of the above. Leave; `claude plugin install` re-creates them |
| `~/.claude/projects/<path-slug>/*.jsonl` | sessions | the 5.7 GB. Path-keyed — see the traps below |
| `~/.claude/memory/` | **memory** | the global memory directory, beside the per-project ones below |
| `~/.claude/projects/<path-slug>/memory/` | **memory** | file-based memory, inside the transcript directory. Small, hand-curated, and the thing a user would actually miss |
| `~/.claude/history.jsonl`, `sessions/`, `tasks/`, `file-history/` | sessions | working state, safe to leave |
| `~/.claude/backups/`, `cache/`, `downloads/`, `debug/`, `telemetry/`, `paste-cache/`, `shell-snapshots/` | cache | leave |
| macOS login Keychain | credential | the OAuth token is in the Keychain, not in a file — it cannot travel. On Linux it is `~/.claude/.credentials.json` |

### Codex CLI (`codex`)

| Path | Plane | Note |
|---|---|---|
| `~/.codex/config.toml` | config **and** credential | `[mcp_servers.*]` sections, including `env` and `env_http_headers` |
| `~/.codex/AGENTS.md` | config | global instructions |
| `~/.codex/hooks.json`, `hooks/` | config | executable — see rule 4 |
| `~/.codex/skills/`, `prompts/`, `plugins/`, `local-marketplaces/` | extensions | `skills/` and `prompts/` are hand-written; `plugins/` (hundreds of MB here) is installed, and `[plugins.*]` in `config.toml` is the replayable list |
| `~/.codex/memories/`, `memories_*.sqlite` | memory | the Markdown under `memories/` carries; the SQLite files are live databases (see the WAL trap) |
| `~/.codex/sessions/`, `archived_sessions/`, `thread_history_*.sqlite`, `rollout-migrations/` | sessions | the 49.9 GB |
| `~/.codex/generated_images/`, `creative-production/`, `computer-use/` | working state | output, often large. Ask; some of it is work the user wants |
| `~/.codex/auth.json` | credential | `codex login` on the new machine is cleaner |
| `~/.codex/cache/`, `log/`, `logs_*.sqlite`, `tmp/`, `ipc/` | cache | leave |

### Gemini CLI (`gemini`)

| Path | Plane | Note |
|---|---|---|
| `~/.gemini/settings.json`, `GEMINI.md` | config | |
| `~/.gemini/config/mcp_config.json` | config | MCP servers |
| `~/.gemini/config/skills/`, `~/.gemini/extensions/`, `commands/` | extensions | `gemini extensions list` / `gemini skills list` name what is installed |
| `~/.gemini/oauth_creds.json`, `google_accounts.json` | credential | `gemini` re-authenticates in a browser; carrying these is rarely worth it |
| `~/.gemini/tmp/`, `antigravity*/` | cache / IDE payload | leave; the `antigravity` trees are a downloaded IDE, ~230 MB |

### Cursor (`cursor`)

| Path | Plane | Note |
|---|---|---|
| `~/.cursor/mcp.json` | config **and** credential | |
| `~/.cursor/rules/`, `skills-cursor/` | extensions | hand-written rules and skills |
| `~/.cursor/extensions/` | extensions | replay as a list: `cursor --list-extensions` (the `vscode-ext` manager in `software-inventory.md`) |
| `~/Library/Application Support/Cursor/User/settings.json`, `keybindings.json` | config | the editor half |
| `~/Library/Application Support/Cursor/User/globalStorage/`, `workspaceStorage/` | sessions | chat history and per-workspace state; large, and full of absolute paths |
| `~/.cursor/projects/`, `ai-tracking/` | sessions | |

### The rest

Probe before you propose; these are the layouts the script knows, and they are
the ones that move most often between releases.

| Agent | Config | Extensions | Sessions / memory | Credential |
|---|---|---|---|---|
| **GitHub Copilot CLI** | `~/.copilot/config.json` | — | `~/.copilot/history`, `logs/` | `gh auth` / Copilot login |
| **Copilot in VS Code** | `~/Library/Application Support/Code/User/settings.json`, repo `.github/copilot-instructions.md` | `code --list-extensions` | — | GitHub login |
| **opencode** | `~/.config/opencode/opencode.json` | `~/.config/opencode/{agent,command,plugin}/` | `~/.local/share/opencode/storage/` | `~/.local/share/opencode/auth.json` |
| **Windsurf** | `~/.codeium/windsurf/mcp_config.json` | `~/Library/Application Support/Windsurf/User/` | same | Codeium login |
| **Continue** | `~/.continue/config.yaml` (or `config.json`) | `~/.continue/{assistants,rules}/` | `~/.continue/sessions/`, `index/` | inside the config |
| **Aider** | `~/.aider.conf.yml`, repo `.aider.conf.yml` | — | repo `.aider.chat.history.md`, `.aider.tags.cache.v*/` | `~/.aider/` / env vars |
| **Cline / Roo Code** | VS Code `globalStorage/<publisher>.<ext>/settings/` | — | same `globalStorage` tree | inside VS Code secret storage |
| **Zed** | `~/.config/zed/settings.json` | `~/.config/zed/extensions/` | `~/Library/Application Support/Zed/`, `~/.local/share/zed/` | Zed login |
| **Goose** | `~/.config/goose/config.yaml` | `~/.config/goose/` | `~/.local/share/goose/sessions/` | keyring |
| **Qwen Code** | `~/.qwen/settings.json` | `~/.qwen/` | `~/.qwen/tmp/` | `~/.qwen/oauth_creds.json` |
| **Ollama / local models** | `~/.ollama/` | — | — | — |

`~/.ollama/models` is weights: gigabytes, re-pullable, and the same bytes
every machine downloads. Record `ollama list` in `notes` and leave the blobs.

### In the repositories

Agent configuration also lives inside projects, and it travels with the
repository rather than with this step:

```
CLAUDE.md  AGENTS.md  GEMINI.md  .cursorrules
.claude/{settings.json,settings.local.json,skills,agents,commands,hooks}
.cursor/rules/  .github/copilot-instructions.md  .mcp.json  .aider.conf.yml
```

Two consequences. First, `.gitignore`d ones (`settings.local.json` is the
common case) are local-only state: a repo carrying them is a repo where
`"strategy": "clone"` silently loses something, so `git_classify.py`'s
untracked count is the signal to check. Second, a repo's `.mcp.json` and
`.claude/hooks/` are code that runs when the agent opens that directory on the
new machine — rule 4 applies to restored repositories, not only to `~`.

## The traps

**MCP server definitions are credential files.** An `env` block holds the key
inline:

```jsonc
"mcpServers": { "corp": { "command": "npx", "args": ["-y", "corp-mcp"],
                          "env": { "CORP_API_KEY": "sk-live-…" } } }
```

`~/.claude.json`, `~/.codex/config.toml`, `~/.cursor/mcp.json`,
`~/.gemini/config/mcp_config.json` and every repo `.mcp.json` can all be in
this state. `agent_inventory.py` reports the *names* of inline env keys, which
is all you need: a config with any of them goes to `credentials/` under the
credential rules, not to `files/`. You do not need to read the value to know a
key is there, and you should not.

HTTP-transport servers hide the same thing in a URL or a header. The script
reports the host and flags a query string rather than printing the URL.

**Restored agent config runs code.** Hooks fire on session start; MCP servers
launch a process the first time the agent connects; a skill is instructions the
agent will follow. Restoring these wholesale gives the new machine a set of
commands the user has not looked at since they wrote them — and, if the backup
ever left their hands, ones they did not write. Restore them in review: name
every MCP server's command, every hook's script, and let the user strike any of
them. This is rule 4, and it is the whole reason agent state gets its own
reference.

**Sessions are the gigabytes, and the transcript is not the memory.** Offer
three tiers and let the user pick per agent:

| Tier | What travels | Who it is for |
|---|---|---|
| `none` | config, extensions and memory only | most people — the default |
| `recent` | transcripts newer than N days (30 is a reasonable default) | "I want to resume what I was in the middle of" |
| `all` | everything | someone who mines their own history, and knows the size |

Memory is never in the `none` tier's leave pile: `~/.claude/projects/*/memory/`,
`~/.codex/memories/`, an agent's `MEMORY.md`. It is kilobytes, it is curated by
hand, and it is the one part of working state that cannot be regenerated by
using the machine again.

**Sessions are also the leak.** A transcript contains whatever crossed the
terminal — printed env vars, a pasted token, a customer's data, the contents of
files the agent read. Three things follow. Do not grep them, ever: decide from
metadata (size, mtime, count) alone, and if one may hold a secret, the fix is
to rotate the secret, not to search for it. Tell the user plainly what
carrying them means before they pick the `all` tier. And remember that
staging and the restore directory are both plaintext on disk — the encryption
only covers the `.envrelay` file between them.

**Project keys are derived from paths.** Claude Code's
`~/.claude/projects/-Users-dylan-dev-app` is the absolute project path with the
separators flattened. A new machine with a different username, or the same
project checked out at a different root, produces a different key — so the
carried history and, worse, the carried `memory/` are on disk but invisible to
the agent. The manifest already records the old home in `machine.home`; mark
the entry's `memory`/`sessions` with `"project_keys": "path-slug"` so the
restore knows to rename the directories to the new machine's slugs instead of
copying them verbatim. Cursor's `workspaceStorage` and opencode's `storage`
are path-keyed the same way.

**A live SQLite database cannot be copied file by file.** Codex keeps
`thread_history_1.sqlite` next to `thread_history_1.sqlite-wal` and `-shm`;
copying the first without the other two produces a database missing its most
recent writes, and copying all three while the agent is running produces a torn
snapshot. Ask the user to quit the agent before staging, carry the `.sqlite`,
`-wal` and `-shm` files as one unit, or leave the database behind and say so.
Never carry a `.sqlite` alone when a `-wal` sits beside it.

**Marketplace extensions replay; hand-written ones must travel.** A skill the
user wrote in `~/.claude/skills/` exists nowhere else in the world. A plugin
installed from a marketplace is a git clone with a name and a version, and the
list is three lines of JSON against hundreds of megabytes of checkout. Carry
the first, list the second — and when a marketplace is a private or internal
URL, that is a `source` worth recording, because the new machine may not reach
it.

**An agent's own import command may beat all of this.** `claude import` reads
configuration out of another agent on the same machine. It is not a migration
path between machines, but if the user is switching agents as well as machines,
mention it rather than hand-assembling the translation.

## Restoring

Per agent in the manifest's `agents` array, in this order — each step is only
safe once the one before it is done:

1. **Install the agent first.** It comes from the `software` array (`npm-g`,
   `brew`, a native installer), under the same rules, name verification
   included. An agent that is not installed has nowhere to put configuration,
   and several of them rewrite their config directory on first run.
2. **Authenticate by logging in, not by restoring a token.** `claude`, `codex
   login`, `gemini`, `opencode auth` — seconds each, and the result is a token
   that belongs to this machine. Carry `auth.json`-shaped files only when the
   user asked for them, and restore a carried one only where no login exists —
   under rule 2, `0600`, never overwriting one that is already there.
   Anything the entry lists under `machine_bound` — a macOS Keychain token, a
   device-bound session — has no file to restore at all: say so and let the
   user redo it.
3. **Config in review.** This is rule 4's moment. One line per MCP server (name
   and the command it runs), one line per hook (the script it calls), and the
   user strikes what they do not want. Then write the files, merging rather
   than overwriting where the new machine already has a config — a fresh
   `~/.claude/settings.json` that an install wrote is not worth losing.
4. **Extensions.** Hand-written skills and subagents are file restores.
   Marketplace plugins replay through the agent's own installer, item by item
   with confirmation, exactly like `software` —
   `claude plugin install <name>@<marketplace>` after
   `claude plugin marketplace add`, `gemini extensions install`. Verify
   against the recorded list afterwards. A plugin whose marketplace is
   unreachable is `extensions-partial`, not a failure to hide.
5. **Sessions and memory last**, and only the tiers the user chose. Path-keyed
   directories get the path-slug rewrite from the traps above: from the
   manifest's `machine.home` to this machine's home, done explicitly, and the
   user told it happened — a silently un-rewritten memory directory is memory
   that is simply gone. Never open a transcript to check.

Then confirm with the agent's own eyes rather than by looking at the files you
just wrote:

```sh
claude mcp list          # and: claude plugin list, claude doctor
codex mcp list           # and: codex doctor
gemini mcp list          # and: gemini extensions list, gemini skills list
opencode mcp list        # and: opencode auth list
```

A server that shows up in `mcp list` but fails to connect is usually the
missing half of a credential: the config travelled, the API key in its `env`
did not. That is `needs-login` in the ledger, with the variable's name in
`reason` — the name, not a guess at the value.

Ledger every agent as its own `agent` item, using the statuses in
`references/manifest.md`: `restored`, `config-restored`, `extensions-partial`,
`needs-login`, `not-installed`, `skipped`.
