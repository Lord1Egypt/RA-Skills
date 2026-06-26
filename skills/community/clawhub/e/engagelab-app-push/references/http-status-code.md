# HTTP Status Code

HTTP return code specification for the EngageLab App Push (MTPush) REST API.

## Status code definition

| Code | Description | Explanation |
|------|-------------|-------------|
| 200 | OK | Success. |
| 400 | Bad request | The request is invalid. The response body will explain the reason. |
| 401 | Not verified | No verification information or verification failed. |
| 403 | Rejected | The request was understood but not accepted. The response will explain. |
| 404 | Not found | The resource does not exist, or the requested format is not supported. |
| 405 | Method not allowed | The interface does not support the request method. |
| 410 | Gone | The requested resource is no longer available. |
| 429 | Too many requests | Rate limit exceeded. The response will explain. |
| 500 | Internal server error | An internal error occurred. Contact support. |
| 502 | Bad gateway | The service server is offline or being upgraded. Try again later. |
| 503 | Service unavailable | The server could not respond. Try again later. |
| 504 | Gateway timeout | The server did not respond in time. Try again later. |

## Specifications

- Use 200 only for success. Do not use 200 for error responses.
- For business logic errors, use 4xx with appropriate error codes; otherwise use 400.
- For server internal errors without a specific code, use 500.
- When a business error occurs, the response body must be JSON with error information (e.g. `code`, `message`).
