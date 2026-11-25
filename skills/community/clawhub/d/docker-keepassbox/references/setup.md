# Connect to KeePassBox

Connect to the instance's Streamable HTTP endpoint at `/mcp` with a bearer token. The token returned by `keepassbox token` can manage its owner's vaults, reveal passwords, and generate TOTP codes. Custom tokens can have [restricted scopes](https://psyb0t.github.io/docker-keepassbox/api/#access). The REST API under `/v1` uses the same credentials and permissions.

OpenClaw's bridge reads the instance's base URL from `KEEPASSBOX_URL` and the token from `KEEPASSBOX_TOKEN`.
