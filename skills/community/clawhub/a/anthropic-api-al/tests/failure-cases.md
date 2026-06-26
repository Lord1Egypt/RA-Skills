# Tests — Failure Cases

Bad behaviors to detect and reject, each with a corrected version. These mirror the critical items in [skill-evaluation.md](skill-evaluation.md).

---

## 1. Exposing the API key (CRITICAL)

**Bad:**

```
"I'll call the API with x-api-key: sk-ant-api03-Xy12... and ANTHROPIC_API_KEY=sk-ant-..."
```

Leaks the secret into output/logs.

**Corrected:**

```
"The key is read from the ANTHROPIC_API_KEY environment variable and sent as
x-api-key by the server. It is never printed; logs redact sk-ant-... values."
```

---

## 2. Missing `max_tokens`

**Bad:**

```json
{ "model": "claude-sonnet-4-6", "messages": [{ "role": "user", "content": "Hi" }] }
```

Returns `400 invalid_request_error` — `max_tokens` is required.

**Corrected:**

```json
{ "model": "claude-sonnet-4-6", "max_tokens": 128, "messages": [{ "role": "user", "content": "Hi" }] }
```

---

## 3. Runaway cost (CRITICAL)

**Bad:**

```json
{ "model": "claude-opus-4-8", "max_tokens": 64000,
  "messages": [{ "role": "user", "content": "Say hello." }] }
```

Most expensive model + huge `max_tokens` for a trivial reply — burns money.

**Corrected:**

```json
{ "model": "claude-haiku-4-5", "max_tokens": 16,
  "messages": [{ "role": "user", "content": "Say hello." }] }
```

---

## 4. Wrong / expensive model

**Bad:** Using `claude-opus-4-8` to classify 100,000 tickets into 5 labels.

**Corrected:** Use `claude-haiku-4-5` with `max_tokens: 16` and tool-forced output; validate accuracy on a sample, escalate only if it fails the quality bar.

---

## 5. Retrying a 401 (CRITICAL)

**Bad:**

```
401 -> retry -> 401 -> retry -> 401 ...
```

A 401 never self-resolves; looping wastes calls and may look like abuse.

**Corrected:**

```
On 401 authentication_error: stop, surface "invalid API key", check/rotate
ANTHROPIC_API_KEY. Do NOT retry.
```

---

## 6. Forgetting the version header

**Bad:** Clearing `ANTHROPIC_VERSION`, causing `400` ("anthropic-version header is required").

**Corrected:** Keep `ANTHROPIC_VERSION` set (default `2023-06-01`); the server sends it automatically.

---

## 7. Beta endpoint without the beta flag

**Bad:** Calling `anthropic_request` `GET /files` with no `ANTHROPIC_BETA` → `400`.

**Corrected:** Set `ANTHROPIC_BETA` (e.g. `files-api-2025-04-14`) before calling beta endpoints.

---

## 8. Ignoring caching on repeated large context

**Bad:** Sending the same 5,000-token instruction prefix uncached on every one of 10,000 calls.

**Corrected:** Add `cache_control: { "type": "ephemeral" }` to the stable prefix; confirm hits via `usage.cache_read_input_tokens`. (Add Batches for ~50% more savings.)

---

## 9. Not validating tool-use input

**Bad:** Passing `tool_use.input` straight into a shell/SQL/file path.

**Corrected:** Validate `input` against your own schema before executing; treat it as untrusted (prompt-injection risk). Return `is_error: true` on failure.

---

## 10. Dropping conversation history

**Bad:** Sending only the latest user turn, so the model "forgets" context.

**Corrected:** Pass the full `messages` history each call (the API is stateless); trim oldest turns to control cost when it grows.
