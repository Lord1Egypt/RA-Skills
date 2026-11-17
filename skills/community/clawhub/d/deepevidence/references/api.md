# DeepEvidence Public API Reference

This reference follows the public DeepEvidence Open Platform docs at:

<https://deepevid.medsci.cn/platform/docs>

Use this file for endpoint, request schema, image content parts, streaming behavior, and public API limits.

## Base URL

```text
https://deepevid.medsci.cn/api/v1
```

Append endpoint paths to this base URL.

## Authentication

Pass the API key in the request header:

```http
Authorization: Bearer <api_key>
```

Do not log, print, commit, screenshot, or package API keys.

## Chat Completions

### POST /chat/completions

Full URL:

```text
https://deepevid.medsci.cn/api/v1/chat/completions
```

DeepEvidence is compatible with the OpenAI Chat Completions request shape. The public model is `DeepEvidence-V1`.

### Request Parameters

| Parameter | Type | Required | Public-doc description |
|---|---|---:|---|
| `model` | `string` | Yes | Model name. Current public model: `DeepEvidence-V1`. Enterprise custom models may be available when authorized. |
| `messages` | `array` | Yes | Message list. Supports `system`, `developer`, `user`, and `assistant` roles. User message `content` can be a string or an array of `text` / `image_url` parts. |
| `stream` | `boolean` | No | Whether to stream output. Default is `true`. |
| `stream_options` | `object` | No | When `{ "include_usage": true }`, usage is returned before the stream ends. |
| `user` | `string` | No | End-user identifier for multi-tenant scenarios. Prefer stable opaque non-PII IDs. |

### Image Input

`messages[].content` supports OpenAI standard content parts with `text` and `image_url`.

`image_url` accepts:

- HTTPS image URLs
- base64 data URLs, such as `data:image/jpeg;base64,...`

Content part shape:

```json
{
  "type": "image_url",
  "image_url": {
    "url": "https://example.com/medical-image.jpg",
    "detail": "auto"
  }
}
```

### Non-Streaming Calls

The public docs show streaming examples and state that `stream` defaults to `true`. For direct HTTP or script usage where a standard JSON response is easier to handle, set:

```json
{ "stream": false }
```

### Streaming Usage

To request usage in streaming mode:

```json
{
  "stream": true,
  "stream_options": {
    "include_usage": true
  }
}
```

## Integration Examples

For curl, Python, and Node examples, read [integration.md](integration.md).

## Error Handling

For status-code handling, stable user-facing failure messages, and troubleshooting, read [errors.md](errors.md) only when an API call fails.

## Public vs Internal Extensions

The current server code may include additional unpublished extension endpoints and fields, such as conversations, project attachments, QA records, feedback, `metadata`, `store`, and code-level model aliases. These are not shown in the public docs above.

For public distribution, demos, and general developer documentation:

- Document only `POST /chat/completions` unless another endpoint is published in the public docs.
- Use `https://deepevid.medsci.cn/api/v1` as the base URL.
- Use `DeepEvidence-V1` as the public model name.
- Treat any project, conversation, QA, feedback, `metadata`, `store`, or private/custom model behavior as an internal or explicitly authorized extension.

For internal validation against source code, verify behavior directly in the server repository before documenting an extension publicly.

## Safety

For emergency, patient-data, PII, and citation-integrity rules, read [safety.md](safety.md) only when the request touches those concerns.
