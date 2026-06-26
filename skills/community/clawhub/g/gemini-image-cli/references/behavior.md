# Gemini Image CLI Behavior

Read this reference only when choosing models, explaining endpoint/security tradeoffs, debugging latency or failures, or modifying the CLI. For exact flags, accepted values, and defaults, run:

```bash
./scripts/gemini-image.sh --help
```

Do not duplicate the full option table here; `--help` is the CLI parameter authority.

## Provider Selection

The script supports two Gemini-compatible providers:

- `local`: a local proxy endpoint, preferred for stronger key isolation.
- `google`: the official Google Gemini endpoint, used as fallback or when explicitly requested.

Default auto-selection:

1. Check whether `GEMINI_LOCAL_ENDPOINT` is reachable.
2. If local is reachable, use local and do not require `GEMINI_API_KEY`.
3. If local is unreachable, fall back to Google.
4. Require `GEMINI_API_KEY` only when using Google.

Explicit provider behavior:

- `--provider local`: use only local; fail if local health check fails; never fall back to Google.
- `--provider google`: use only Google; do not check local; require `GEMINI_API_KEY`.

Only local health-check failure can trigger fallback. If local is reachable but `generateContent` fails, report that failure directly.

## Environment

Endpoint environment variables are base origins. Do not include `/v1beta`.

```bash
GEMINI_LOCAL_ENDPOINT=${GEMINI_LOCAL_ENDPOINT:-http://127.0.0.1:8000}
GEMINI_LOCAL_API_KEY=${GEMINI_LOCAL_API_KEY:-sk-123456}
GEMINI_GOOGLE_ENDPOINT=${GEMINI_GOOGLE_ENDPOINT:-https://generativelanguage.googleapis.com}
```

`GEMINI_API_KEY` is required only for the Google provider.

The local endpoint must expose a Gemini-compatible API so the script can call:

```text
{endpoint}/v1beta/models/{model}:generateContent
```

`gemini-balance` is one compatible local proxy option: <https://github.com/snailyp/gemini-balance>

## Security Model

Environment variables avoid storing keys in code or command history, but they are not a hard boundary against a runtime that can execute arbitrary shell commands in the same environment.

Use local proxy mode when the runtime should not have direct access to the real Google Gemini API key. In local mode, the script sends only `GEMINI_LOCAL_API_KEY`, a lower-risk proxy key, to the localhost service. The real Google key stays inside the local proxy.

A local proxy still grants image-generation capability, so the proxy should:

- Bind to `127.0.0.1`, not `0.0.0.0`.
- Avoid arbitrary URL forwarding.
- Enforce model, request size, rate, and quota limits as needed.
- Avoid logging real upstream credentials.

## Model Choice

Use defaults for ordinary single-image generation.

Use `gemini-2.5-flash-image` when speed and stability matter. Local tests observed about 8-13 seconds for simple prompts.

Use `gemini-3.1-flash-image-preview` for the default newer Flash image path. Local tests observed about 11-17 seconds at `--size 512`, but larger sizes can have long-tail latency.

Use `gemini-3-pro-image-preview` for stronger instruction following, text rendering, or professional-quality output.

These timings are observations, not guarantees.

## Logs

The script prints human-readable logs to stderr and machine-readable result lines to stdout.

Stderr sections:

- `Request`: selected provider, endpoint, model, size, aspect, output, and raw JSON path.
- `Curl`: a copyable curl command wrapped in a Markdown `bash` code fence.
- `Generating`: response timing and image count.
- `Done`: final duration.

The printed curl command masks both Google and local proxy keys. If input images are present, base64 data is printed as:

```json
"data": "<base64:redacted>"
```

Use `--quiet` to suppress stderr logs.

## Output Files

The script reads each returned `inlineData.mimeType` and selects the image extension from the MIME type:

- `image/png` -> `.png`
- `image/jpeg` -> `.jpg`
- `image/webp` -> `.webp`

Do not assume Gemini always returns PNG. If `--output` has a known image extension, the script treats it as a prefix and replaces the extension when needed.

## Failure Handling

Common curl failures:

- `curl: (56) Failure when receiving data from the peer`: connection closed during response. Try `--http1.1`, `--retry 1`, a smaller size, or a faster model.
- `curl: (92) HTTP/2 stream error`: try `--http1.1`.
- `curl: (28) Operation timed out`: increase `--max-time` or leave it as `0` for no total timeout.

Do not enable retries automatically for ambiguous user requests. Retries can submit additional generation requests and may consume extra quota.
