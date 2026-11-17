# Error Handling

| Signal | Required action |
|---|---|
| `Not authenticated` | Ask the user to create and configure a BizMuse API key locally. |
| Unsupported extension | Request a supported MP3, WAV, M4A, AAC, JPG, JPEG, PNG, or WebP file. |
| File exceeds upload limit | Ask the user to compress or shorten the source before retrying. |
| Insufficient credits | Direct the user to `https://bizmuse.ai/pricing`. |
| Task remains pending | Wait at least 30 seconds between checks; return the task ID after 30 minutes. |
| Provider failure | Return the provider message without inventing a completed result. |
| Download failure | Return the result URLs and preserve the task ID so the download can be retried. |

Do not retry authentication, permission, billing, or invalid-input failures automatically. Only retry transient status queries, and wait at least 30 seconds between attempts.
