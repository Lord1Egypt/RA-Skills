# Rewind File Changes with Checkpointing

> Track file changes during agent sessions and restore files to any previous state.

File checkpointing tracks file modifications made through Write, Edit, and NotebookEdit tools. Changes via Bash commands (like `echo > file.txt` or `sed -i`) are NOT captured.

## Key Options

| Option | Python | TypeScript | Description |
|:---|:---|:---|:---|
| Enable checkpointing | `enable_file_checkpointing=True` | `enableFileCheckpointing: true` | Tracks file changes for rewinding |
| Receive checkpoint UUIDs | `extra_args={"replay-user-messages": None}` | `extraArgs: { 'replay-user-messages': null }` | Required to get user message UUIDs |

## Complete Flow

### TypeScript

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  const opts = {
    enableFileCheckpointing: true,
    permissionMode: "acceptEdits" as const,
    extraArgs: { "replay-user-messages": null }
  };

  const response = query({ prompt: "Refactor the authentication module", options: opts });

  let checkpointId: string | undefined;
  let sessionId: string | undefined;

  for await (const message of response) {
    if (message.type === "user" && message.uuid && !checkpointId) {
      checkpointId = message.uuid;
    }
    if ("session_id" in message && !sessionId) {
      sessionId = message.session_id;
    }
  }

  // Rewind later
  if (checkpointId && sessionId) {
    const rewindQuery = query({
      prompt: "",
      options: { ...opts, resume: sessionId }
    });
    for await (const msg of rewindQuery) {
      await rewindQuery.rewindFiles(checkpointId);
      break;
    }
    console.log(`Rewound to checkpoint: ${checkpointId}`);
  }
}
main();
```

### Python

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, UserMessage, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        enable_file_checkpointing=True,
        permission_mode="acceptEdits",
        extra_args={"replay-user-messages": None},
    )
    checkpoint_id = None
    session_id = None

    async with ClaudeSDKClient(options) as client:
        await client.query("Refactor the authentication module")
        async for message in client.receive_response():
            if isinstance(message, UserMessage) and message.uuid and not checkpoint_id:
                checkpoint_id = message.uuid
            if isinstance(message, ResultMessage) and not session_id:
                session_id = message.session_id

    if checkpoint_id and session_id:
        async with ClaudeSDKClient(
            ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
        ) as client:
            await client.query("")
            async for message in client.receive_response():
                await client.rewind_files(checkpoint_id)
                break
        print(f"Rewound to checkpoint: {checkpoint_id}")
```

## Patterns

### Checkpoint Before Risky Operations

Keep only the latest checkpoint UUID. If something goes wrong, immediately rewind:

```typescript
let safeCheckpoint: string | undefined;
for await (const message of response) {
  if (message.type === "user" && message.uuid) safeCheckpoint = message.uuid;
  if (yourRevertCondition && safeCheckpoint) {
    await response.rewindFiles(safeCheckpoint);
    break;
  }
}
```

### Multiple Restore Points

Store all checkpoint UUIDs with metadata (description, timestamp) in an array. After session completes, rewind to any specific point.

## CLI Rewind

```bash
claude -p --resume <session-id> --rewind-files <checkpoint-uuid>
```

## Notes

- Only Write/Edit/NotebookEdit changes are tracked; Bash changes are not
- Rewinding restores files on disk but does NOT rewind the conversation
- Created files are deleted, modified files restored to content at checkpoint
- This doc is from English version (Chinese URL returned 404)
