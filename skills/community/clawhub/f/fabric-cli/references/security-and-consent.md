# Security and consent guide for Fabric.so CLI workflows

Fabric CLI operations can read from and write to a remote workspace. Use the following consent boundaries and safety habits.

## Operation categories

| Category | Examples | Default behaviour |
| --- | --- | --- |
| Local read-only | `command -v fabric`, `fabric --version`, `fabric --help` | Safe to run when relevant. |
| Remote read-only | `search`, `path`, `inbox`, `bin`, `workspace current`, `workspace list`, `task list`, `subscription` | Safe to run when user context implies Fabric access. |
| Non-destructive remote write | `note`, `link`, `file`, `save`, `create folder`, `task add`, `task done`, `task edit`, `workspace select` | Run only when the user clearly asks for the change or it is necessary for the requested workflow. |
| Destructive or hard-to-reverse | `task rm`, `logout`, deletion, bulk edits, broad moves, any deletion command found in help | Ask for explicit confirmation immediately before running. |
| Installation/authentication | installer, `login`, `auth API_KEY` | Do not run without explicit request and safe handling of credentials. |

## Installation

The official installer is a remote shell script. That is normal for this CLI, but it still deserves care.

```bash
tmp_script="$(mktemp)"
curl -fsSL https://fabric.so/cli/install.sh -o "$tmp_script"
sed -n '1,200p' "$tmp_script"
# After approval:
sh "$tmp_script"
```

Never run installer commands hidden inside another script or without telling the user what will happen.

## Authentication

Preferred for humans: `fabric login`.

Non-interactive environments may need `fabric auth "$FABRIC_API_KEY"`.

Rules: do not ask the user to paste API keys into ordinary chat unless there is no safer route; prefer environment variables, secret stores, or interactive login; never echo a key; never save keys to Fabric memory; redact tokens in command output before summarising.

## Shell quoting and command history

User-provided content can contain spaces, quotes, command substitutions, shell metacharacters, or newlines. Avoid interpolating it directly into shell commands. For long generated text, write to a temp file and pipe stdin:

```bash
cat /tmp/note.md | fabric --json note --tag agent-memory
```

## File uploads

Before uploading a local path, run `test -f "$PATH"`. Reject or ask before uploading credential files such as `.env`, SSH keys, API-token files, browser profile directories, password databases, private key material, large logs that may contain secrets, or broad user-home globs.

## Workspace selection

Changing workspace changes where subsequent commands operate. Before write operations: `fabric --json workspace current`. When switching, list if needed, select, then re-check current workspace and report it in the final answer.

## Memory persistence privacy

Fabric memory is persistent and searchable. Do not save secrets, unrelated sensitive personal data, private user preferences unless the user asked for persistent memory, raw transcripts, or uncertainty-free claims when evidence is weak.
