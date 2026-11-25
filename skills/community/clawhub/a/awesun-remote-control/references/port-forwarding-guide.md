# Port Forwarding Guide

Detailed configuration schema, usage examples, and troubleshooting pitfalls for `awesun-cli forward`.

## 1. Channels JSON Schema

The `--channels` argument accepts a JSON array of channel objects defining remote forwarding targets:

```json
[
    {
        "channel_id": "ch1",
        "address": "127.0.0.1",
        "port": 8080
    }
]
```

### Field Definitions

| Key          | Required | Description                                                   |
| ------------ | -------- | ------------------------------------------------------------- |
| `channel_id` | **yes**  | Unique identifier for the channel (e.g. `ch1`, `ssh`, `web`). |
| `address`    | **yes**  | Remote-side target IP address (e.g. `127.0.0.1`).             |
| `port`       | **yes**  | Remote-side target port (e.g. `8080`, `22`).                  |

> [!IMPORTANT]
> There is **NO `local_port` or `remote_port` parameter** in the input configuration. The CLI / daemon automatically binds an available local port and prints it in the output table. Passing unsupported keys causes execution failure.

## 2. Typical Flow

```bash
# 1. Connect forward session (session_id is an integer: 1, 2, 3...)
awesun-cli session connect --type forward --remote-id <remote-id>
# Returns session_id, e.g. 1

# 2. Configure port forwarding
awesun-cli forward config 1 --channels '[{"channel_id":"ch1","address":"127.0.0.1","port":8080}]'
# Output prints the channel table: CHANNEL_ID / LOCAL_ADDRESS / LOCAL_PORT / REMOTE_ADDRESS / REMOTE_PORT

# 3. Access the service using the assigned LOCAL_PORT from the returned table
curl -i http://127.0.0.1:<LOCAL_PORT_FROM_TABLE>/
```

## 3. Known Pitfalls & Troubleshooting

- **Local port is dynamically assigned**: Do not attempt to specify `local_port`. Always read the assigned port from the returned table (or inspect via `lsof -nP -iTCP -sTCP:LISTEN | grep awesun`).
- **No channel delete/clear**: `--channels '[]'` fails, and re-configuring an existing channel also fails. To reset, disconnect via `awesun-cli session disconnect <session_id>` and reconnect to obtain a new session ID.
- **Stale session ID**: After disconnect/reconnect, referencing the old session ID returns `cannot find session with id "<n>"`. Query active sessions using `awesun-cli session ls`.
- **Exit code 0 on failure**: The command may return exit code 0 even on failure. Always parse stderr for `Error:` instead of relying solely on `$?`.
- **No `--help` for forward**: Running `forward config <id> --help` is parsed as a session ID; avoid passing `--help` or `--verbose` to the `forward config` subcommand.
