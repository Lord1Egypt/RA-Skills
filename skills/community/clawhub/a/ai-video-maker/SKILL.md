---
name: aivideo-api-executor
description: Executes AIVideoMaker API workflows for text-to-video and image-to-video generation, including task creation, status polling, task details retrieval, and cancellation. Use when users ask to generate videos via API, monitor generation progress, cancel tasks, or automate AIVideoMaker API operations.
version: 1.0.14
requires:
  env:
    - AIVIDEO_API_KEY
  binaries:
    - node
primaryCredential: AIVIDEO_API_KEY
---




# AIVideoMaker API Executor

## Purpose
Provide a production-ready execution workflow for AIVideoMaker API v1:
- Create generation task
- Poll task status safely
- Fetch task details
- Cancel submitted task

## When To Use
- User asks to call `aivideomaker.ai` API directly
- User wants a scriptable generation workflow
- User needs robust retry/429 handling for task queries

## Required Environment
- `AIVIDEO_API_KEY` (required) Get an API Key from [https://aivideomaker.ai](https://aivideomaker.ai) .
- `AIVIDEO_TIMEOUT_MS` (optional, default `30000`) - Request timeout in milliseconds
- `AIVIDEO_MAX_RETRIES` (optional, default `3`) - Max retries for idempotent read requests

## Supported Actions
1. `createGeneration`
2. `getTask`
3. `getStatus`
4. `cancelTask`

## Model Whitelist
- `t2v`
- `i2v`
- `lv`
- `t2v_v3`
- `i2v_v3`

## Image Input Policy
- This skill accepts both public image URLs and `data:image/...;base64,...` for `i2v`, `lv`, and `i2v_v3`.
- Prefer `data:image/...;base64,...` for reliability in OpenClaw environments.

## Standard Workflow
1. Validate model and payload by contract.
2. Call `createGeneration`.
3. Poll `getStatus` with backoff until terminal status.
4. If `COMPLETED`, call `getTask` and return output.
5. If `FAILED`, return failure with actionable next steps.

## Error Policy
- Normalize all responses to:
  - `ok`, `status`, `taskId`, `data`, `errorCode`, `errorMessage`, `retryAfter`
- Map API/runtime errors into stable error codes:
  - `INVALID_MODEL`
  - `INVALID_PAYLOAD`
  - `AUTH_FAILED`
  - `RATE_LIMITED`
  - `INSUFFICIENT_CREDITS`
  - `TASK_NOT_FOUND`
  - `NETWORK_ERROR`
  - `UNKNOWN_ERROR`

## Execution Commands
- Run full workflow:
  - `node scripts/run-workflow.mjs --model <model> --payload '<json_payload>'`
- Query status:
  - `node scripts/run-workflow.mjs --action getStatus --taskId <task_id>`
- Query task details:
  - `node scripts/run-workflow.mjs --action getTask --taskId <task_id>`
- Cancel task:
  - `node scripts/run-workflow.mjs --action cancelTask --taskId <task_id>`

## Security
This skill only performs the following actions:
- Calls the AIVideoMaker API with user-provided parameters
- Validates input payloads against a defined contract
- Reads only payload passed via `--payload`
- Does not read arbitrary host files, credentials, or sensitive system information
- Does not execute arbitrary code or shell commands

All network requests are made to `https://aivideomaker.ai` (or an optional custom base URL configured via client options) and include only the API key for authentication. The API key is sent as an HTTP header named `key` (as required by the AIVideoMaker API). While HTTPS encrypts the transmission, intermediaries may log the `key` header. Users should be aware of privacy implications when sending image data and API keys to upstream services.

**Security Best Practices:**
- Never hardcode API keys in source code, configuration files, or skill archives
- Always pass the `AIVIDEO_API_KEY` as an environment variable
- Use secret management tools or platform-specific credential storage
- Regularly rotate API keys and monitor usage

## Additional Resources
- Full API matrix: [references/api-reference.md](references/api-reference.md)
- Usage and failure scenarios: [references/examples.md](references/examples.md)
