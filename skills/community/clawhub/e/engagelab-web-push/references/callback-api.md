# Callback API

Message status callbacks are sent to your business server so you can perform analytics and react to delivery/click events.

## Callback address

- There is no web UI for setting the callback URL. Contact EngageLab support to configure the callback address for your application.

## Address validity verification

When the callback URL is configured, the backend sends a **POST** request with a randomly generated 8-character string in the request body as `echostr`.

**Request body:**

```json
{
  "echostr": "12345678"
}
```

**Required response:** Return the value of `echostr` in the response **body** (plain text), e.g.:

```
12345678
```

Your server must respond with this value so the callback address is validated.

## Security (optional)

To verify that the callback is from EngageLab, configure a **callback username** and **callback secret** in the console. Then verify the `X-CALLBACK-ID` header.

**Header example:**

```
X-CALLBACK-ID: timestamp=1681991058;nonce=123123123123;username=test;signature=59682d71e2aa2747252e4e62c15f6f241ddecc8ff08999eda7e0c4451207a16b
```

- `timestamp` — Callback message timestamp.
- `nonce` — Random number.
- `username` — Callback username you configured.
- `signature` — Signature to verify.

**Signature algorithm:**

```
signature = HMAC-SHA256(secret, timestamp + nonce + username)
```

Use your configured **callback secret** as the HMAC key, and the string `timestamp + nonce + username` (concatenated) as the message. Compare the computed signature with the `signature` in the header.

## Response requirements

Your server must respond **within 3 seconds**:

- **Success:** HTTP status **200** or **204**. Response body can be empty.
- **Failure:** HTTP status **4xx** or **5xx**. You may return a JSON body, e.g.:

```json
{
  "code": 2002,
  "message": "error"
}
```

If you do not return 200/204 in time, EngageLab may retry; ensure your endpoint is idempotent.

## Callback payload (message body)

The callback POST body contains message status data (e.g. total, rows with message_id, from, to, server, channel, custom_args, itime, status). For full field definitions and status values, see `doc/webpush/REST API/Callback API.md`.

## Summary

1. Provide EngageLab with your callback URL.
2. Implement the echostr validation (return `echostr` in body).
3. Optionally verify `X-CALLBACK-ID` with HMAC-SHA256(secret, timestamp+nonce+username).
4. Respond with 200 or 204 within 3 seconds for success.
