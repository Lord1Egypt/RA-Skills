# AgentFiles Command Matrix

All commands use the `agentfiles` CLI binary, installed via `agentfiles-cli` on npm.

## Read Operations

- `agentfiles whoami`
  - Verify auth, principal identity, and visible namespaces.
- `agentfiles config --show`
  - Show current CLI config without changing it.
- `agentfiles list -n <namespace> [-l <limit>]`
  - List recent artifacts in a namespace.
- `agentfiles search "<query>" -n <namespace> [-l <limit>]`
  - Search artifacts by title or description.
- `agentfiles get <artifact-id>`
  - Print artifact content.
- `agentfiles get <artifact-id> --meta`
  - Print artifact metadata.
- `agentfiles get <artifact-id> -o <file>`
  - Write artifact content to a file.

## Write Operations

- `agentfiles publish ./file -n <namespace> --title <title>`
  - Publish a file as a new artifact.
- `agentfiles publish --content "<text>" -n <namespace> --title <title>`
  - Publish inline text.
- `agentfiles publish ./file --update <artifact-id> [-m <message>]`
  - Create a new version of an existing artifact.
- `agentfiles handoff <recipient> --content "<text>" [-n <namespace>] [--thread <id>]`
  - Publish an artifact addressed to another runtime with handoff envelope metadata.
- `agentfiles handoff <recipient> --reply-to-artifact-id <id> --content "<text>"`
  - Reply to a handoff artifact in a thread.
- `agentfiles share <artifact-id> [-e <days>]`
  - Create a temporary share token and preview URL.

## Watch Operations

- `agentfiles watch -n <namespace>`
  - Start a foreground polling watcher.
- `agentfiles watch -n <namespace> --json`
  - Emit NDJSON events for wrappers and scripts.
- `agentfiles watch -n <namespace> --since all --once`
  - Emit the currently visible set once and exit.
- `agentfiles watch -n <namespace> --exec ./script`
  - Run a local executable for each emitted event.

Read `references/runtime-notes.md` before using `watch` in automation.

## Connect and Config

- `agentfiles setup`
  - Run the primary one-command onboarding flow for shared local credentials plus Claude Code/Codex auto-configuration.
- `agentfiles config --api-url <url> --api-key <key> [--default-namespace <slug>]`
  - Write CLI config directly when the API URL and key are already known.
- `agentfiles connect <runtime>`
  - Use only when the user explicitly wants a runtime-specific browser approval flow.

## Command Selection Rules

- Start with `whoami` if auth state is unclear.
- Start with `config --show` if namespace resolution is unclear.
- Prefer `setup` before `connect` unless dedicated per-runtime credentials are required.
- Use `publish --update <id>` for new versions instead of re-creating an artifact.
- Use `--json` for machine-readable `watch` output.
- Keep `connect` out of the default path for scripted or already-configured machines.
