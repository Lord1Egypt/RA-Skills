---
name: fec-api-integration
description: Use when designing, implementing, or reviewing frontend-to-backend API integration, typed API clients, REST/tRPC/OpenAPI client choices, auth refresh, API error mapping, upload flows, SSE/WebSocket/polling choices, CORS-facing frontend behavior, or cross-boundary loading/error states. Do not use for backend-only service architecture or TanStack Query cache policy alone; Chinese triggers include API integration, front-end and back-end joint debugging, typed API client, Interface error handling, SSE, WebSocket.
---

# API integration

Suitable for front-end and back-end boundary types, errors, authentication, uploads, real-time communication and user status design. Load [integration-patterns.md](references/integration-patterns.md) when specific code patterns are required.

## Purpose

Standardize front-end API integration boundaries to make requests, errors, authentication, and real-time data maintainable.

## Procedure

1. Clarify interface ownership
   - For TypeScript full stack in the same team, tRPC or shared schema can be considered.
   - Multi-language or multi-consumer API preferred OpenAPI/GraphQL codegen.
   - Typed fetch wrapper can be used for small internal applications, but types must be maintained centrally.
   - Do not scatter `fetch`, URL, header, error parsing and token logic in components.
   - Public interfaces need to specify versions, compatibility windows, obsolete field policies, and caller scope.

2. Establish client boundaries
   - Handle base URL, credentials, JSON parsing, timeouts, cancellation and unified errors with an API client.
   - The environment variable only reads the public prefix, and the private token does not enter the client bundle.
   - The component only consumes domain functions or query/mutation hooks, and does not directly splice interface paths.
   - 204, empty response, non-JSON error and network disconnection must have clear behavior.
   - TypeScript contracts must cover request, response, error shapes, and pagination/cursor metadata.

3. Map user-understandable errors
   - 401: Boot login after failed refresh.
   - 403: Indicates insufficient permissions, do not retry.
   - 404: Display missing status or return to the upper level entrance.
   - 409: Prompt for conflict and next step.
   - 422: Mapping field level error.
   - 429/5xx/Network Error: Allow backoff to retry or show try again later.
   - Unrecognized errors should fall into a unified fallback, and the original backend exception should not be exposed to the user.
   - All errors should be attributed to user-recoverable actions: retry, log in again, modify input, return to the previous level, contact support, or try again later.
   - The error object should retain the log-oriented trace id / request id, but the UI should not expose the internal stack, SQL, service name or sensitive fields.

4. Management interface evolution
   - Compatible with new fields; deleting or renaming fields must go through the migration period, adaptation layer or double-write/double-read strategy.
   - Capture breaking changes using schema, type generators or contract tests.
   - Record status codes, error codes, idempotence, retry semantics and time zone/amount/enumeration rules for front-end and back-end collaboration items.

5. Handle authentication refresh
   - Access token has a short life cycle, and refresh is prioritized in httpOnly cookies or server sessions.
   - Only a single refresh of the queue is allowed after 401 to avoid multiple requests being refreshed at the same time.
   - If the refresh fails, you need to clear the local identity status and jump to login.
   - Do not put bearer token in URL, localStorage or logs.

6. Select the upload and real-time plan
   - Multipart is available for small files; large files are given priority for pre-signed direct upload or multipart upload.
   - Only use SSE for server push; use WebSocket for two-way collaboration, chat or multi-person status.
   - Simple status refresh, low-frequency task progress can be polled, and stop conditions can be set.
   - Both uploads and live connections require cancellation, reconnection, timeout and error UI.

7. Verify integration quality
   - Check loading, empty, error, unauthorized, offline, retrying status.
   - Confirm base URL, credentials, CORS, and status code behavior using the browser network panel.
   - Use mock or test services to cover 401, 403, 422, 500, disconnection and cancellation requests.
   - Verify that the client bundle does not contain private environment variables, server keys, or internal addresses.
   - Add minimal testing for key API client behaviors to demonstrate that timeouts, cancellations, error mappings, and flush queues are expected.
   - Verification error boundary cooperates with the request layer: rendering exceptions go to the Error Boundary, and request failures go to the recoverable UI, without swallowing each other.

## Constraints

- Do not manage token refresh, error format parsing, or retry strategies directly in page components.
- No blind automatic retries for 4xx business errors.
- Do not expose backend exception stacks, internal error codes or raw SQL/service names to users.
- Do not use localStorage to store high-value tokens; if legacy systems cannot be avoided, security review must be linked.
- No need to use WebSocket to replace simple polling, and no need to use polling to achieve high-frequency two-way collaboration.
- Do not allow uploads to be forwarded through the API server for large files unless there is an explicit compliance or scanning need.
- Do not directly expose temporary fields, database field names or backend internal error structures in the public interface.

## Expected Output

The output should include API client boundaries, interface type sources, error mappings, authentication refresh policies, upload/real-time schemes, and validation results. After completion, the component will not scatter request details, the user status will be intact, failure scenarios can be recovered, and the client will not leak the server key.
