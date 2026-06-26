# Codex MPP Gotchas

Common failure points when using the MPP payment flow.

## Mutations and subscriptions are not supported

MPP only works for `query` operations. Sending a mutation or subscription returns `403`. Use API key auth for those.

## API key takes precedence

If an `Authorization` header with an API key is present, the server uses API key auth and skips the payment flow. Don't mix them.

## Challenges expire

A `WWW-Authenticate` challenge is single-use and short-lived. If you get `invalid-challenge` on retry, request a fresh challenge by repeating the initial request.

## Credential encoding

The credential in `Authorization: Payment <credential>` must be base64url-encoded, not standard base64. A `malformed-credential` error usually means wrong encoding or broken JSON.

## `tempo request` handles the flow automatically

If the user has the Tempo CLI installed, `tempo request` handles the full 402 challenge/payment/retry cycle in one command. Don't manually implement the flow when `tempo request` is available.

## Check wallet balance before making requests

Run `tempo wallet -t whoami` before paid requests and confirm `ready` is `true` with sufficient `balance.available`. An insufficient balance mid-flow produces confusing errors.
