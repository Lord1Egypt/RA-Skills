# Troubleshooting — Fastmail API

## 401 Unauthorized

Likely causes:
- Invalid or expired token
- Token missing required scope
- Authorization header formatting issues

Actions:
1. Re-issue or verify token.
2. Re-test with `jmap/session`.
3. Confirm token is passed as `Authorization: Bearer ...`.

## Capability Errors

If methods fail due to unsupported capability:
- Read capabilities from session response.
- Add required capability URNs to `using`.
- Remove calls that are not supported for the token.

## Partial Write Failures

When `notUpdated` or `notCreated` is present:
- Summarize failed IDs and reasons.
- Re-run only failed items after payload correction.
- Verify final state with read calls before closing.

## Large Batch Timeouts

- Reduce batch size.
- Add incremental checkpoints in `request-log.md`.
- Prefer pagination windows over monolithic requests.
