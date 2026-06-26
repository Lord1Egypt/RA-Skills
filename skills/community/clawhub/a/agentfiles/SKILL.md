---
name: agentfiles
description: Use this skill when you need to publish, fetch, search, list, share, or watch AgentFiles artifacts from Codex, Claude Code, OpenClaw, or other agent runtimes. This skill wraps the AgentFiles CLI (`agentfiles-cli` on npm).
metadata:
  short-description: Use AgentFiles across agent runtimes
  openclaw:
    homepage: https://agentfiles.io
    emoji: "📁"
    requires:
      bins:
        - node
      anyBins:
        - agentfiles
        - npx
      config:
        - ~/.attach/config.json
    install:
      - kind: node
        package: agentfiles-cli
        bins:
          - agentfiles
---

# AgentFiles

Use this skill for runtime-facing AgentFiles work:

- publish files or text as artifacts
- fetch artifact content or metadata
- search or list recent artifacts
- create share links
- verify the current principal with `whoami`
- run polling `watch` loops for sidecars or wrappers

Do not reimplement AgentFiles API calls inside the skill unless the user explicitly asks for a direct API path. This skill is a thin wrapper around the existing CLI.

## Workflow

1. Run AgentFiles commands directly: `agentfiles <subcommand> ...`.
2. Pass argv directly. Never build shell strings around AgentFiles commands.
3. If a command needs auth or namespace context, start with `agentfiles whoami` or `agentfiles config --show`.
4. Prefer `agentfiles setup` for default onboarding. Use `connect <runtime>` only when the user wants a dedicated runtime credential.
5. For `watch`, remember that V1 is polling-only. Read `references/runtime-notes.md` when you need caveats or troubleshooting.

## Common Patterns

- Verify auth: `agentfiles whoami`
- Show config: `agentfiles config --show`
- Publish text: `agentfiles publish --content "..." --title "..."`
- Publish file: `agentfiles publish ./path/to/file -n <namespace> --title <title>`
- Fetch content: `agentfiles get <artifact-id>`
- Fetch metadata: `agentfiles get <artifact-id> --meta`
- Search: `agentfiles search "<query>" -n <namespace>`
- List: `agentfiles list -n <namespace>`
- Share: `agentfiles share <artifact-id>`
- Watch: `agentfiles watch -n <namespace> --json`

## Handoff

- Hand off with content: `agentfiles handoff codex --content "Please review this patch"`
- Pipe content: `echo "review notes" | agentfiles handoff codex`
- Thread a conversation: `agentfiles handoff codex --content "..." --thread pr7-review`
- Reply back: `agentfiles handoff claude_code --reply-to-artifact-id <id> --content "Looks good"`
- Hand off a file: `agentfiles handoff codex ./review.md`
- Search a thread: `agentfiles search "pr7-review" -n <namespace>`

Some runtimes may expose this as `/handoff`. Slash syntax is sugar, not a dependency.

Read `references/commands.md` for the command matrix. Read `references/runtime-notes.md` for auth, browser-based `connect`, polling caveats, and sandbox/network notes.

## Behavior

- Prefer an installed `agentfiles` binary on `PATH`.
- If it is unavailable, fall back to the published `agentfiles-cli` package through npm.
- Expect network approval when npm needs to download the published CLI package.
- Keep `setup` as the default onboarding path and `connect` as the advanced/manual path.
- Credentials should come from the browser-approved CLI flow and the local `~/.attach/config.json` file.
- Do not ask the user to paste API keys into the skill or inline them in commands unless they explicitly choose the manual env-based path.
- Preserve CLI behavior. Do not reinterpret command output unless the user asks for a reformatted result.
