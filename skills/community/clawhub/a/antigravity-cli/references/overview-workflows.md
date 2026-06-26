# Overview and Workflows

## Positioning

Use Antigravity CLI when the user wants a lightweight, terminal-native agent workflow with minimal overhead, keyboard navigation, shell pipeline integration, SSH/tmux friendliness, and fast local iteration.

Use Antigravity 2.0 when the user needs visual orchestration, broader project management, richer multi-panel review, or desktop IDE workflows.

Both surfaces share the same agent harness and synchronize core preferences, permissions, and security configuration.

## Platform comparison

| Need | Prefer |
| --- | --- |
| Fast local terminal iteration | CLI |
| SSH, headless, tmux, terminal multiplexers | CLI |
| Scriptable one-shot prompts | CLI |
| Visual project management | Antigravity 2.0 |
| Rich desktop artifact review | Antigravity 2.0 |
| Continue a complex terminal session visually | Export/continue in Antigravity 2.0 |

## Reliable agent workflow

For complex changes:

1. Ask the agent to explore the codebase and identify constraints.
2. Ask for a plan or use `/planning`.
3. Review artifacts before approving multi-file edits.
4. Provide a local verification command, such as `npm test`, `pytest`, `go test ./...`, or a project build command.
5. Let the agent iterate on test/build output.

For small changes:

1. Use a direct prompt or `agy -p`.
2. Keep the requested scope narrow.
3. Ask for a summary plus verification result.

## Session control patterns

- Press `Esc` early when the agent goes down the wrong path.
- Use `/rewind` to recover from a bad turn without throwing away the whole conversation.
- Use `/fork` for uncertain implementation experiments.
- Use `/resume` to return to a stable thread.
- Use background subagents for broad searches, independent investigations, or parallel cleanup tasks.

## Automation pattern

For shell pipelines, use non-interactive print mode and include the required output contract:

```bash
agy -p "Review this git diff and produce a conventional commit message. Output only the commit title and body."
```

When automating code changes, include a verification loop in the prompt:

```bash
agy -p "Implement the requested refactor, then run npm test and summarize the result."
```
