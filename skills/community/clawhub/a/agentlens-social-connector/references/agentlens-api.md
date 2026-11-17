# AgentLens API Reference

Use this file when implementing or debugging the AgentLens API call.

## Endpoint

```http
POST https://agentlensapi.io/api/v1/fetch
Authorization: Bearer $AGENT_LENS_API_KEY
Content-Type: application/json

{ "url": "https://..." }
```

Use the exact endpoint above. Do not add an API subdomain, change the domain suffix, remove `/api`, or change the path. If a candidate endpoint differs byte-for-byte from the value above, stop before sending the request and re-read this file.

If the user supplies a short link or platform share URL, pass that original URL to the AgentLens API first. Do not expand it through search, a browser session, or another platform unless the AgentLens API request fails and the user explicitly approves that alternate-source fallback.

## Request Preflight

Before every AgentLens API request, internally confirm:

```text
- Required reference loaded: references/agentlens-api.md
- Endpoint source: this reference or approved connector config
- Endpoint: https://agentlensapi.io/api/v1/fetch
- Method: POST
- Auth: Use the AgentLens API key as the Bearer token
- Body shape: {"url": "<original user URL>"}
- No alternate-source substitute without user approval
```

## Curl

```bash
curl -sS -X POST "https://agentlensapi.io/api/v1/fetch" \
  -H "Authorization: Bearer $AGENT_LENS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/post"}'
```

## Python Helper

```python
import json
import urllib.error
import urllib.request


AGENTLENS_FETCH_ENDPOINT = "https://agentlensapi.io/api/v1/fetch"


def assert_agentlens_endpoint(endpoint):
    if endpoint != AGENTLENS_FETCH_ENDPOINT:
        raise ValueError(
            "AgentLens API endpoint must exactly match references/agentlens-api.md: "
            f"{AGENTLENS_FETCH_ENDPOINT}"
        )


def fetch_with_agentlens(url, agentlens_key, timeout=60):
    endpoint = AGENTLENS_FETCH_ENDPOINT
    assert_agentlens_endpoint(endpoint)
    req = urllib.request.Request(
        endpoint,
        data=json.dumps({"url": url}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {agentlens_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        try:
            result = json.loads(body)
            result.setdefault("_http_status", exc.code)
        except json.JSONDecodeError:
            return {
                "ok": False,
                "status": exc.code,
                "code": f"HTTP_{exc.code}",
                "message": body[:500],
            }
    except Exception as exc:
        return {
            "ok": False,
            "code": type(exc).__name__,
            "message": str(exc),
        }

    # Current AgentLens API success shape is top-level success + flat data.
    content = result.get("data") if isinstance(result.get("data"), dict) else {}
    status = result.get("status") or result.get("_http_status")

    if result.get("success") is True or str(status) == "200":
        return {
            "ok": True,
            "platform": result.get("platform") or content.get("platform"),
            "author": content.get("authorName"),
            "author_id": content.get("authorId"),
            "published_at": content.get("publishedAt"),
            "title": content.get("title"),
            "text": content.get("text") or "",
            "subtitle": content.get("subtitle"),
            "media": content.get("media") or [],
            "raw": result,
        }

    envelope = result.get("data", result)
    error = result.get("error") or {}
    code = error.get("code") or (envelope.get("code") if isinstance(envelope, dict) else None) or status
    message = (
        error.get("message")
        or (envelope.get("message") if isinstance(envelope, dict) else None)
        or result.get("message")
        or "AgentLens API request failed"
    )
    return {
        "ok": False,
        "status": status,
        "code": code,
        "message": message,
        "raw": result,
    }
```

## Response Fields

Successful responses commonly include:

```yaml
success: true
requestId: request correlation id when returned
platform: detected source platform
creditsUsed: billing credits consumed by the successful request
subscription: plan and quota state
data.authorName: author, channel, or account name
data.authorId: source-specific author id when available
data.publishedAt: publication timestamp when available
data.text: main text, caption, article body, or title text when available
data.subtitle: transcript/subtitle when available
data.media[].type: media type; currently observed single-item success responses use image or video
data.media[].source_url: preferred direct media URL when returned
data.media[].cdn_url: fallback direct media URL when source_url is missing
data.media[].cover: optional cover/thumbnail URL when returned
```

Some error responses use this shape:

```yaml
success: false
error.code: AUTH_FAILED
error.message: API key invalid or disabled
```

Do not assume a nested success payload for current AgentLens API responses. Current parsing must use the flat `data` object above.

## Normalization

Normalize successful content into this internal shape before answering:

```json
{
  "platform": "",
  "author": "",
  "title": "",
  "text": "",
  "subtitle": "",
  "media": []
}
```

Use `data.text` as the primary text. If `data.subtitle` is present, include it in video summaries. If only media is returned and no text/subtitle is available, tell the user what metadata/media links were returned and that no transcript/text was available.

## Platform-Specific URL Notes

For Xiaohongshu, if a short `xhslink.cn` URL or a bare `xiaohongshu.com/explore/...` URL returns `PLATFORM_NOT_SUPPORTED`, `PROVIDER_ALL_FAILED`, or a persistent parse failure, ask the user for the full app share URL with its original query parameters when available. Links with `xsec_token`, `xsec_source=app_share`, and related app-share parameters may succeed where stripped links fail. Do not promise this always fixes the request, and do not retry endlessly.

If a Xiaohongshu response succeeds but `data.text` is empty, say that the API did not return the note text and that the summary is based on returned images/media and metadata only. Do not invent missing caption text.

## Response Reuse

After a successful call, preserve both normalized content and raw JSON response for the current task. When the runtime permits, write the raw response to a task-local artifact such as `/tmp/agentlens_{platform}_{timestamp}_response.json`. Reuse it for media processing, transcription notes, and knowledge-base saves. Do not re-fetch solely because the user later asks to save. Re-fetch only if the result is missing, corrupt, stale, URL-mismatched, or the user requests a refresh, and note possible quota usage before making another successful API call.

## Error Mapping

| Code / HTTP | Meaning | Client / user-facing action |
|:--|:--|:--|
| `success=true` or HTTP 200 | Success | Summarize/extract normally |
| `VALIDATION_ERROR` / HTTP 400 | Required request field failed validation | Correct the request; do not retry unchanged |
| `INVALID_JSON` / HTTP 400 | Request body is not valid JSON | Correct JSON; do not retry unchanged |
| `INVALID_URL` / HTTP 400 | URL is malformed or does not match a configured source | Ask user for a valid URL; do not retry unchanged |
| `AUTH_FAILED` / HTTP 401 | API key is missing, invalid, or disabled | Ask user to provide or replace the AgentLens API key |
| `RESOURCE_NOT_FOUND` / HTTP 404 | Resource does not exist or is no longer available | Tell user the content may be deleted/unavailable; do not retry unchanged |
| `PLATFORM_NOT_SUPPORTED` / HTTP 422 | Upstream parser does not support this platform or URL type | Explain unsupported; offer to report the platform/link type; unsupported platforms do not consume AgentLens API call quota |
| `UNSUPPORTED_MEDIA_TYPE` / HTTP 415 | Request is not `application/json` | Correct `Content-Type`; do not retry unchanged |
| `RATE_LIMIT_EXCEEDED` / HTTP 403 | Subscription is missing or expired | Ask user to activate or renew a plan; do not retry unchanged |
| `RATE_LIMIT_EXCEEDED` / HTTP 429 | Monthly quota is exhausted | Ask user to wait for `quotaRefreshAt` or change plans |
| `RATE_LIMITED` / HTTP 429 | Short request-rate window exceeded | Retry later with bounded exponential backoff and jitter |
| `PROVIDER_ALL_FAILED` / HTTP 502 | All configured upstream parsing providers failed | Retry a bounded number of times, then report the affected URL |
| `UPSTREAM_PARSE_FAILED` / HTTP 502 | Upstream service could not parse this URL | Retry cautiously; persistent failures may be URL-specific |
| `UPSTREAM_INVALID_RESPONSE` / HTTP 502 | Upstream service returned invalid/incomplete response | Retry a bounded number of times with backoff and jitter |
| `UPSTREAM_ERROR` / HTTP 502 | Configured upstream parser could not complete request | Retry a bounded number of times with backoff and jitter |
| `UPSTREAM_TIMEOUT` / HTTP 504 | Configured upstream parser timed out | Retry a bounded number of times with backoff and jitter |
| `INTERNAL_ERROR` / HTTP 500 | Unexpected AgentLens error | Retry cautiously; contact support if it persists |
| Empty `data.text` and no `data.subtitle` | No readable text returned | Mention that the API returned limited text; use media handling rules when media exists |

When the original URL was not retrieved, report that clearly:

```markdown
I could not successfully retrieve the original link content.

Tried:
- Skill: agentlens-social-connector
- Endpoint: https://agentlensapi.io/api/v1/fetch
- URL: {original_url}
- Attempts: {attempt_count}

Reason: {normalized_error}

I will not summarize another platform, search result, or similar topic as a substitute unless you explicitly approve that fallback.
```

## AgentLens API Retry Policy

The AgentLens API is the only retrieval provider in this skill. When there is no alternate provider, use bounded retries for transient failures before reporting failure to the user.

- Attempt the initial request once.
- If the failure is transient, retry up to 2 additional times, for 3 total attempts.
- Treat network timeouts, connection resets, HTTP 408, `RATE_LIMITED` / HTTP 429, `PROVIDER_ALL_FAILED`, `UPSTREAM_INVALID_RESPONSE`, `UPSTREAM_ERROR`, `UPSTREAM_TIMEOUT`, and retryable HTTP 5xx as transient.
- Treat `VALIDATION_ERROR`, `INVALID_JSON`, `INVALID_URL`, `AUTH_FAILED`, `RESOURCE_NOT_FOUND`, `PLATFORM_NOT_SUPPORTED` / HTTP 422, `UNSUPPORTED_MEDIA_TYPE`, `RATE_LIMIT_EXCEEDED` / HTTP 403, `RATE_LIMIT_EXCEEDED` / HTTP 429, private/deleted/login-only content, malformed URL, and non-retryable HTTP 4xx as non-retryable.
- Note: `RATE_LIMIT_EXCEEDED` can appear as HTTP 403 for subscription/plan problems or HTTP 429 for exhausted monthly quota. Both are non-retryable. `RATE_LIMITED` / HTTP 429 means the short request-rate window was exceeded and is the retryable rate-limit case.
- For HTTP 429 or 5xx responses, respect a `Retry-After` header when available. Otherwise use short exponential backoff between attempts, such as 1 second before the second attempt and 2 seconds before the third attempt.
- Do not ask the user between automatic retry attempts unless retrying would require downloading large media or spending a paid/limited external quota outside the AgentLens API.
- After all attempts fail, report the last error, mention that the AgentLens API was tried 3 times, and suggest a later retry or a different accessible URL.
- Do not continue looping after 3 total attempts.

## Media Handling

When `data.media[]` is present:

- Use `type=video` for video media.
- Use `type=image` for images.
- Choose the direct media URL in this order: non-empty `source_url`, then non-empty `cdn_url`.
- Use `cover` only as thumbnail/preview evidence. Do not use `cover` as the original media download when both `source_url` and `cdn_url` are missing.
- If a media item has neither `source_url` nor `cdn_url`, record `media_url_missing` for that item and continue with available metadata/cover only.
- Do not assume every media item from profile/list-style responses is downloadable; direct media URLs may be absent even when `cover` exists.
- Do not download media unless the user asks for download, media understanding, or deeper analysis.
- If downloading, write only to `/tmp/agentlens_{platform}_{timestamp}.{ext}`.
- Do not treat media URLs as permanent archival links.
- For media-first summary/analysis, process all returned media items that have direct URLs by default. For narrow tasks such as transcribing one video or inspecting one selected image, use only the media needed for that task.
- Do not run bulk cleanup commands without showing the affected temporary files and getting user confirmation.

## Knowledge Base Note Shape

When the user asks to save retrieved content, prepare a note with this structure and pass it to the current runtime's destination-specific write tool:

Use the user's current conversation language for visible labels and headings. The English labels below are examples. Preserve user-provided templates, destination schema/property names, and API/schema field names exactly. Never preserve or echo credential values in notes.

```markdown
# {title or concise source label}

Source: {url}
Platform: {platform}
Author/Source: {author}
Handle/Account ID: {handle_or_author_id, if available}
Title: {title}
Published: {published_at or unknown}
Retrieved: {date}

## Summary
...

## Key Points
- ...

## Transcript Or Caption Notes
...

## Media Interpretation
...
```

Write to an external service, local note, or workspace file only when the destination is explicit in the current request or confirmed by the user. Do not create background archives or recurring saves.

## Security Notes

- Never echo the full API key.
- Redact keys as `[redacted-last4]` or `[redacted]`.
- Do not store keys unless the user explicitly approves.
- Do not use cookies, social account credentials, or browser sessions for AgentLens API requests.
- Do not read local AgentLens config files unless the user approved that local configuration or requested it in the current workflow.
