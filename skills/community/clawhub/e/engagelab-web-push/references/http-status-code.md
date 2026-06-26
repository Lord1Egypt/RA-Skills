# HTTP Status Code

HTTP return code specification for the EngageLab Web Push (MTPush) REST API.

## Status code definition

| Code | Description | Explanation |
|------|-------------|-------------|
| 200 | OK | Success. |
| 400 | Incorrect request | The request is invalid. The response body will explain the reason. |
| 401 | Not verified | No verification information or verification failed. |
| 403 | Rejected | The request was understood but not accepted. The response will explain. |
| 404 | Unable to find | The resource does not exist, or the requested format is not supported. |
| 405 | Request method not suitable | The operation does not support the request method. |
| 410 | Offline | The requested resource is offline. |
| 429 | Excessive requests | Rate limit exceeded. The response will explain. |
| 500 | Internal service error | An internal error occurred. Contact support. |
| 502 | Invalid proxy | The service server is offline or being upgraded. Try again later. |
| 503 | Service temporarily invalid | The server could not respond. Try again later. |
| 504 | Agent timeout | The server did not respond in time. Try again later. |

## Compliance

- Use 200 only for success. Do not use 200 for error responses.
- For business logic errors, use 4xx or 400.
- For server internal errors, use 5xx or 500.
- When a business error occurs, the response body must be JSON with error information (e.g. `code`, `message`).
