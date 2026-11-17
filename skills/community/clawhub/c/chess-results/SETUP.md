# chess-results — Setup

## Prerequisites

- **Python 3.11+**
- Packages: `pip install -r requirements.txt`
  (`requests`, `beautifulsoup4`, and `mcp` for the MCP server; `keyring` is needed on Linux and
  Windows for the login store — macOS uses the Keychain directly)

## Login (only for result entry)

Run once, in your own terminal:

```bash
python3 scripts/cli.py login
```

It asks for your Chess-Results personal number and password (hidden), stores them and
tries the login. The command line and the MCP server then find it by themselves, in
this order:

1. **Environment** — `CHESS_RESULTS_PNO` and `CHESS_RESULTS_PASSWORD`.
2. **System credential store** — where `cli.py login` writes:
   - **macOS**: the login keychain, generic password with service `chess-results`,
     written and read by `/usr/bin/security`. That program is on the entry's access
     list, so it is read without an authorization dialog while you are logged in.
     Passwords saved by Safari live in iCloud Keychain / the Passwords app, which no
     command-line tool can read — copy yours from there once into `cli.py login`.
   - **Windows / Linux desktop**: Credential Manager / Secret Service, through `keyring`.
3. **A private file** — for machines without a credential store (a headless server, a
   container): `python3 scripts/cli.py login --file` writes
   `~/.config/chess-results/credentials.json` with mode 600 (another path:
   `--file PATH`, and `CHESS_RESULTS_CREDENTIALS=PATH` for reading). A file that others
   can read is refused.

`python3 scripts/cli.py status` shows whether a login is found and where (never the
password); `python3 scripts/cli.py logout` removes the stored one.

## Club settings (only for match reports)

Copy `examples/chess-results.example.json` to `chess-results.json` in your project
folder (or any parent folder, `~/.config/chess-results/chess-results.json`, or a
path in `CHESS_RESULTS_CONFIG`) and adapt it:

| Key | Meaning |
|---|---|
| `club` | the word that marks your teams in Chess-Results team names |
| `club_name` | your club's full name |
| `user_agent` | how the client names itself; sent as `Mozilla/5.0 (compatible; …)`, which the result editor requires |
| `ignore_words` | sponsor or other words in team names that say nothing about a club |
| `tournaments.championship.prefix` | search every league starting with this on Chess-Results' AUT championship overview (e.g. `Bgld`, `Wien`) |
| `tournaments.numbers` | or list tournament numbers directly — works for any country |
| `board_order_tolerance` | rating points within which boards may be swapped (national rating); `null` to skip |
| `deadline` | online entry closes at this time on the first working day after the match; `null` for none |

The queries work without a settings file.

## Claude Code

This folder is a Claude Code plugin (`.claude-plugin/plugin.json`) and its own
marketplace (`.claude-plugin/marketplace.json`): it starts the MCP server and adds this
skill.

```text
/plugin marketplace add odrobnik/chess-results-skill
/plugin install chess-results@chess-results-skill
```

For development: `claude --plugin-dir /path/to/chess-results`.

## Codex

Add the server to `~/.codex/config.toml`:

```toml
[mcp_servers.chess-results]
command = "python3"
args = ["/path/to/chess-results/scripts/server.py"]
```

The login comes from the same credential-store entry; nothing secret goes into the
Codex config.

## OpenClaw

Two ways in:

- **As a plugin** — OpenClaw reads this folder as a Claude bundle: it loads
  `skills/chess-results` and starts the MCP server from `.mcp.json`
  (`${CLAUDE_PLUGIN_ROOT}` is expanded). The tools then appear as
  `chess-results__search_players` and so on.

  ```bash
  openclaw plugins install git:github.com/odrobnik/chess-results-skill@v0.1.0
  openclaw plugins install ./chess-results      # or from a local folder
  ```

- **As a skill** — from ClawHub or a folder. The agent uses the command line,
  `{baseDir}/scripts/cli.py`.

  ```bash
  openclaw skills install @odrobnik/chess-results
  ```

**macOS: pin the Python for the MCP server.** The OpenClaw Gateway puts `/usr/bin`
ahead of Homebrew on the `PATH` it gives MCP servers, so `python3` there is Apple's
Python 3.9 without these packages. The server then exits at once, and the Gateway
logs only `MCP error -32000: Connection closed`
([openclaw/openclaw#165642](https://github.com/openclaw/openclaw/issues/165642)).
Until that is fixed, override the bundle's server with an absolute interpreter. A
configured server of the same name takes precedence:

```bash
openclaw mcp set chess-results '{"command": "/opt/homebrew/bin/python3",
  "args": ["/path/to/chess-results/scripts/server.py"], "cwd": "/path/to/chess-results"}'
```

Use the folder the plugin was installed to (`openclaw plugins inspect chess-results`
shows it) and the Python that has the packages from `requirements.txt`.

**The login.** Use `cli.py login` as above — the Keychain/credential store on a
desktop, `cli.py login --file` on a headless gateway. Both reach the command line and
the MCP server alike, with nothing to configure in OpenClaw.

Through OpenClaw's own settings, a login reaches **only the command line**:

```json5
{
  skills: { entries: { "chess-results": {
    apiKey: { source: "exec", provider: "…", id: "chess-results" },  // a SecretRef: env, file, exec
    env: { CHESS_RESULTS_PNO: "your-personal-number" }
  } } }
}
```

The skill declares `CHESS_RESULTS_PASSWORD` as its `primaryEnv`, so `apiKey` becomes
that variable for commands the agent runs. MCP servers don't get it: OpenClaw starts
them with only a few inherited variables, and `plugins.entries.<id>` has no `apiKey`
or `env` (only `enabled`, `hooks`, `subagent`, `llm`, `config`). For the MCP tools,
use the credential store or the file. An `exec` SecretRef provider must be a script
you own; OpenClaw does not run root-owned binaries such as `/usr/bin/security`
directly.

## Tests

```bash
python3 -m unittest discover -s tests
```
