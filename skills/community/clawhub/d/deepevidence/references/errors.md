# DeepEvidence Error Handling

Use this reference only after an API call fails or returns insufficient content. Keep logs minimal because prompts, responses, and error bodies may contain sensitive clinical information.

## Stable User-Facing Messages

Missing API key:

```text
DE_CONFIG_ERROR: DEEPEVIDENCE_API_KEY is not set. Apply for an API key at: https://deepevid.medsci.cn/platform/api-keys
```

Temporary retrieval failure:

```text
Temporarily unable to retrieve evidence-based results. Please try again later or consult a licensed clinician.
```

Do not interpret empty, timed-out, or failed retrieval as "no risk" or "no evidence".

## Output Contract

- `stdout`: medical answer content only.
- `stderr`: stable error code, status, request ID, latency, token usage, and debug class when enabled.
- Exit code `0`: success.
- Exit code `1`: API, network, timeout, or response error.
- Exit code `2`: local configuration error.

Stable error codes:

```text
DE_CONFIG_ERROR
DE_BAD_REQUEST
DE_AUTH_ERROR
DE_PERMISSION_ERROR
DE_RATE_LIMIT
DE_TIMEOUT
DE_UPSTREAM_ERROR
DE_INVALID_RESPONSE
```

## Status Codes

| Status | Meaning | Handling |
|---:|---|---|
| `400` | `DE_BAD_REQUEST` | Check `model`, `messages`, `stream`, `stream_options`, and `image_url` content parts against `references/api.md`. |
| `401` | `DE_AUTH_ERROR` | Check that `DEEPEVIDENCE_API_KEY` is set, valid, and not expired. Do not print the key. |
| `403` | `DE_PERMISSION_ERROR` | Confirm the key is authorized for the requested product or resource. Do not bypass boundaries. |
| `404` | `DE_UPSTREAM_ERROR` | For public packages, confirm the URL is `https://deepevid.medsci.cn/api/v1/chat/completions`. |
| `429` | `DE_RATE_LIMIT` | Reduce call frequency, retry later, or contact the administrator. |
| `5xx` | `DE_UPSTREAM_ERROR` | Use bounded retries; if still failing, present the temporary retrieval failure message. |

## Observability

Log only operational metadata such as status code, latency, model, token usage, request ID if returned, and redacted error class. Do not log full prompts, full responses, API keys, patient identifiers, image data URLs, or raw stack traces in normal mode.

Use `DEEPEVIDENCE_DEBUG=1` only in controlled local debugging. Debug output must still avoid full request and response bodies.
