# Troubleshooting

## `ERROR: GMAIL_RAG_REPO is not set`

- Export `GMAIL_RAG_REPO` to your local `ClawInboxRAG` path.

## `ERROR: GMAIL_RAG_REPO does not exist`

- Verify the path is correct and readable.

## `ERROR: runner not found in PATH`

- Install `uv` or set `GMAIL_RAG_UV_BIN` to the correct executable.

## `ModuleNotFoundError: gmail_rag`

- Check repository path and environment setup.
- Confirm CLI runs in the configured `ClawInboxRAG` checkout.

## OAuth/auth failures

- Confirm token exists and has Gmail read-only scope.
- Re-authenticate if token is expired or revoked.

## Empty semantic/hybrid results

- Run maintenance (`mail sync`) and retry.
- Fall back to `keyword` mode for exact-match validation.

## Slow responses

- Lower `max/top/limit` values.
- Prefer keyword mode for narrow exact-match searches.
