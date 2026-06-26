# OpenClaw Boot Camp

**Agent CLI Training** — auto-generates a CLI reference doc so your agent stops guessing and starts working.

Every OpenClaw agent wastes tokens fumbling with CLI syntax. The `--help` command is broken on most subcommands. Flags get guessed wrong. Commands that don't exist get tried. Boot Camp fixes that by discovering your actual CLI commands and generating a clean reference your agent can read.

## Quick Start

```bash
bash bootcamp.sh
```

That's it. Follow the wizard. Your agent gets a cheat sheet.

## What It Does

1. Reads your OpenClaw **bash completion file** (the authoritative source of all commands/flags)
2. Extracts **command descriptions** from `openclaw --help`
3. Generates a **structured markdown reference** and drops it in your agent's workspace

The output includes every command, subcommand, and flag for your installed version — no internet required.

## Modes

### Local Only (Recommended)
```bash
bash bootcamp.sh
# Select [1] in the wizard
```
- Discovers commands directly from your CLI
- No internet, no API calls, no token cost
- Produces a solid reference from what's installed

### Local + Enrich
```bash
bash bootcamp.sh --enrich
# Or select [2] in the wizard
```
- Runs local discovery first
- Then asks your agent to search docs.openclaw.ai for your version
- Agent fills in flag descriptions, usage examples, gotchas
- **Requires:** Agent with web search capability
- **Cost:** ~1 agent turn (varies by model/provider)

## Options

| Flag | Description |
|------|-------------|
| `--enrich` | Enable Phase 2 agent enrichment |
| `--yes`, `-y` | Non-interactive mode (overwrite existing, skip prompts) |
| `--output=PATH` | Custom output directory (default: `~/.openclaw/workspace/notes`) |
| `--help`, `-h` | Show help |

## Version Management

If Boot Camp finds an existing reference doc, it asks:
- **Overwrite** — replace with current version
- **Keep both** — saves as `openclaw-cli-reference-v2026.4.8.md`
- **Cancel** — do nothing

## Requirements

- OpenClaw installed and in PATH
- Bash 4+ (for associative arrays)
- No other dependencies — pure bash, grep, awk, sed

## Output

The reference lands at:
```
~/.openclaw/workspace/notes/openclaw-cli-reference.md
```

Your agent can read it anytime. Run Boot Camp again after updating OpenClaw to regenerate for the new version.

## Example Output

```markdown
# OpenClaw CLI Reference (v2026.4.8)

## Commands

### `agent`
Run one agent turn via the Gateway
**Flags:** `-m`, `-t`, `--session-id`, `--agent`, `--thinking`, ...

### `gateway`
Run, inspect, and query the WebSocket Gateway
**Subcommands:** `run`, `status`, `install`, `restart`, `call`, ...
**Flags:** `--port`, `--bind`, `--token`, `--auth`, `--force`, ...
```

## Why

Because `openclaw <command> --help` is broken on 90% of subcommands and every agent on the planet rediscovers this the hard way.

## License

MIT
