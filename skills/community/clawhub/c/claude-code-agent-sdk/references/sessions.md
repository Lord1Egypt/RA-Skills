# Using Sessions

Sessions are the conversation history (prompts, tool calls, results, responses) the SDK accumulates as your agent works. The SDK automatically writes them to disk, allowing you to resume or fork them.

## Choosing an Approach

| Scenario | What to Use |
|----------|--------------|
| One-off task | No extra effort, single `query()` call |
| Multi-turn chat within a single process | `ClaudeSDKClient` (Python) or `continue: true` (TypeScript) |
| Continue after process restart | `continue_conversation=True` / `continue: true` |
| Resume a specific past session | Capture session_id, pass to `resume` |
| Try an alternative approach | Fork the session |
| Stateless tasks | TypeScript: `persistSession: false` |

## Continue vs Resume vs Fork

- **Continue** — Finds most recent session in current directory, no tracking ID needed
- **Resume** — Takes a specific session ID, manual tracking
- **Fork** — Creates new session, starts with copy of original history, original unchanged

## Python: ClaudeSDKClient

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("Analyze the auth module")
    async for message in client.receive_response():
        print(message)
    # Second query automatically continues same session
    await client.query("Now refactor it to use JWT")
    async for message in client.receive_response():
        print(message)
```

## TypeScript: continue: true

```typescript
// First query creates new session
for await (const message of query({ prompt: "...", options: {...} })) { ... }
// Second query automatically resumes most recent session
for await (const message of query({
    prompt: "...",
    options: { continue: true, ... }
})) { ... }
```

## Capturing Session ID

```python
async for message in query(prompt="...", options=...):
    if isinstance(message, ResultMessage):
        session_id = message.session_id
```

## Resuming by ID

```python
async for message in query(
    prompt="Now implement the refactoring",
    options=ClaudeAgentOptions(resume=session_id, ...)
): ...
```

> If resume returns a new session, the most common cause is cwd mismatch. Sessions are stored at `~/.claude/projects/<encoded-cwd>/*.jsonl`.

## Forking to Explore Alternatives

```python
# Fork: branch from session_id into a new session
async for message in query(
    prompt="Instead of JWT, implement OAuth2",
    options=ClaudeAgentOptions(resume=session_id, fork_session=True),
):
    if isinstance(message, ResultMessage):
        forked_id = message.session_id

# Original session unchanged, resume continues JWT thread
async for message in query(
    prompt="Continue with the JWT approach",
    options=ClaudeAgentOptions(resume=session_id),
): ...
```

## Resuming Across Hosts

Move `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` to the same path on the new host, or capture the result as application state to pass into a new session's prompt.

**Session utility functions:** `list_sessions()`, `get_session_messages()`, `get_session_info()`, `rename_session()`, `tag_session()`