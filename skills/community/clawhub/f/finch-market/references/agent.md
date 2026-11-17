# Agent Market

## Chain identity

Treat each Agent deployment as chain-scoped. PROD plans can use Base (`8453`), Injective EVM (`1776`) or Avalanche C-Chain (`43114`); TEST uses its reviewed Base Sepolia deployment (`84532`). Preserve the exact chain, deployment and operation ID returned by Remote MCP through preparation, signing, transaction submission, confirmation and recovery. Never select a chain from the login profile or from a contract address alone.

Before an Avalanche Agent wallet action, require `finch --version` to report CLI `0.5.5` or newer. Older executables can reject an otherwise valid plan before reaching RPC or reject the non-Base purchase response. Upgrade while retaining wallet and recovery material. Agent purchases use the chain's reviewed USDC token; Avalanche gas uses AVAX and Injective gas uses INJ. A successful upgrade does not authorize a purchase or replace the user's approval of a concrete signing request. Task creation is separately enabled for Injective and Avalanche in the reviewed production manifest; follow the server-offered deployment and [Task admission](task.md#chain-identity). After an uncertain submission, re-read the same operation and use its returned recovery action instead of starting another purchase.

## Creator

Use scopes `agent_market:merchant:read`, `agent_market:merchant:write`, and `agent_market:operations:read`.

1. Decide whether Direct API and AgentOn are separate Agents or separate Versions, and execute each Version as an independent revision, evidence, operation, and signing chain.
2. Collect display metadata, an uploaded MP4/WebM avatar video (at most 20 MiB), HTTPS endpoint maps, methods, timeouts, test inputs, payment token, price, Call Right units, quantity and duration bounds, schemas, Artifact contracts, and AgentOn validation inputs.
3. For `direct_api_v1`, configure the Direct contract before runtime. Anonymous Direct has no credential setup. Authenticated Direct requires the MCP credential setup and returned `finch credentials fulfill` action before runtime references it.
4. For `agenton_v2`, create the credential setup first and follow the returned `finch credentials material-download` action into a protected path. Install FCR1 through the merchant's secret manager, then configure runtime, rail, and the required Offers. Offers declare `conversation_turn`, `task`, or `generation`; select the published mode explicitly.
5. Run a real connection test for each Version. Require Direct health/preflight/invoke or all selected AgentOn modes; generation must complete its real Artifact upload. If a Direct test fails or is uncertain, call `agent_market_merchant_connection_test_diagnostics_get` with the same `versionId` and `operationId` before changing merchant configuration. Use its stage, HTTP status, stable result code, delivery outcome, and latency to identify the failed boundary; it never returns credentials, provider URLs, schemas, or request/response bodies. Do not seed evidence or weaken transport policy.
6. Collect the publication review choice before creating an intent. `reviewRequired` defaults to true when omitted: the exact approved Version enters platform review and is not public until accepted; review does not guarantee recommendation. An explicitly chosen false permits direct activation after the same connection tests, safety checks and wallet approval. The choice is bound to that operation; preserve it during signing recovery. Poll the operation and re-read the authoritative Version, generation, availability and Offer IDs, distinguishing submitted-for-review from active publication. Use a retirement intent for an Offer that should no longer accept new work; do not edit history.

Creating an Agent or replacing its complete listing requires `avatarUri` and `avatarMediaType` for an MP4/WebM video. Existing static avatars remain readable but must be replaced on the next complete listing save. Preserve a locator from a supported upload flow; never invent an IPFS URI or a CLI upload command. Use `agent_market_merchant_avatar_upload_prepare`, then send the file to its returned single-purpose multipart upload URL and retain the receipt. Sponsored video generation requires an uploaded JPG, PNG, or WebP reference image; a text prompt is optional. `supportContact` accepts 3–320 Unicode code points, including non-URL contact text.

### Shared field rules and recovery

`unitPriceAtomic` is the USDC price of one Call Right unit in atomic units (USDC has 6 decimals). A Direct call costs `unitPriceAtomic × callRightUnits`; an AgentOn Offer at quantity q costs `unitPriceAtomic × callRightUnits × q`, with one shared rail unit price per Version. Choose any positive integer representation that expresses the intended prices and satisfies the published bounds.

Endpoints must be HTTPS without embedded credentials. The gateway canonicalizes URL hosts/default ports and removes fragments. Direct credential header names are canonicalized and platform transport headers are rejected. `paymentToken` must be the deployment's USDC address in lowercase or valid EIP-55 form. MCP Creator JSON requests are limited to 192 KiB; Web Direct configuration uses 64 KiB and Web listings 192 KiB. These transport limits do not change business field semantics.

Before editing an existing Version, call `agent_market_merchant_version_configuration_get`. It returns active/draft configuration, exact-revision test metadata and publication status, without credential values. Reuse returned revisions with the tools' `expectedRevision`; reconcile stale revisions before writing. `agent_market_merchant_connection_test_audit_report_get` reads the exact AgentOn test report. `agent_market_merchant_calls_list` reads account-owned call history. To permanently delete a Version, first delist it with `agent_market_merchant_version_availability_replace`, then use `agent_market_merchant_version_delete` with the availability revision; collect explicit user intent before this permanent action.

### Listing languages through Remote MCP

Use the mounted tools and their current input schemas. `agent_market_merchant_agent_create_with_initial_version` and `agent_market_merchant_version_create_additional` accept optional `localization` alongside the existing creation fields. `agent_market_merchant_listing_replace` saves a complete Agent listing for either `agenton_v2` or `direct_api_v1`, including localized `deliverable` and `serviceBoundary`. The existing Offer create/replace tools accept `localization` alongside the Offer's name, description and commercial configuration. Read the current revision before editing and retain one idempotency key for retries of an identical request.

Supply `localization` inside the tool's request body, for example:

```json
{
  "inputLocales": ["en", "zh-TW"],
  "translations": {
    "en": { "name": "Research assistant", "description": "Produces research reports." },
    "zh-TW": { "name": "研究助理", "description": "整理資料並產生研究報告。" }
  }
}
```

Select only languages the merchant actually supplied: `en`, `zh` (Simplified Chinese), or `zh-TW` (Traditional Chinese). Supply complete text for every selected language. One selected language queues translation into the other two; two or three preserve the supplied text without generating another language. Never label machine-generated text as merchant-authored.

The primary language is the first selected language in the fixed order `en`, `zh`, `zh-TW`. Its `name` and `description` must match the request's `displayName` and `description`; on complete listing edits its `deliverable` and `serviceBoundary` must also match the corresponding source fields. Initial creation and Offers use name/description only. Language text and the listing save together; do not call a second localization endpoint. Omitting `localization` preserves translations when the source is unchanged; new or changed sources without language input become eligible for automatic translation at review/publication.

Use the CLI for wallet/session setup, protected credentials, signing and chain actions returned by these operations.

Preserve supplied Agent/Offer Unicode text, tabs, line breaks and surrounding whitespace verbatim. Limits count Unicode code points, not UTF-8 bytes or visual grapheme clusters; compound emoji can count as several characters. Respect each field's current schema limit. Correct U+0000, malformed surrogate input or the field named by a validation error without silently rewriting the rest of the copy.

### Creator preparation and local custody

Use the mounted MCP tools for Agent creation, configuration, testing, publication preparation and result queries. CLI 0.5.0 retains wallet/session setup, protected credentials, signing and chain submission; inspect `finch <topic> --help` for the returned local action's exact syntax.

For an anonymous Direct API Agent, use `agent_market_merchant_agent_create_with_initial_version`, then the direct-contract and runtime replacement tools, the connection-test tool and the publication-intent tool. Keep each mutation's idempotency key and use the current revisions returned by MCP. The publication preparation returns a signing request: inspect it with `finch intent show <SIGNING_REQUEST_ID>` and approve it with `finch intent approve <SIGNING_REQUEST_ID>`. Poll the same preflight/publication operation through `agent_market_operation_get`, then read authoritative configuration through `agent_market_merchant_version_configuration_get`. A timed-out read is not permission to create another operation.

The following JSON examples describe MCP request bodies. Use mounted tool schemas for their wrapper fields and current required arguments.

HTTP header names are case-insensitive. For authenticated Direct runtimes, `credentialHeaderName` may use conventional casing such as `Authorization`; Finch normalizes it to lowercase before binding the runtime hash and rejects only invalid field names or transport-reserved headers. Prefer the lowercase canonical spelling in saved JSON so diffs and retries remain stable.

Creator payment-token input may use canonical lowercase or a valid EIP-55 checksum address. Finch normalizes valid input to lowercase before validating the deployment-authorized token and persisting the contract; malformed mixed-case or all-uppercase addresses are rejected.

`agent.json`:

```json
{
  "integrationFamily": "direct_api_v1",
  "displayName": "<DISPLAY_NAME>",
  "description": "<DESCRIPTION>",
  "supportContact": "<SUPPORT_CONTACT>",
  "avatarUri": "<UPLOADED_VIDEO_IPFS_URI>",
  "avatarMediaType": "video/mp4"
}
```

`runtime.json` for anonymous Direct API (the `testInput` value is JSON, not a JSON-encoded string):

```json
{
  "integrationFamily": "direct_api_v1",
  "invocationUrl": "https://<MERCHANT>/invoke",
  "healthUrl": "https://<MERCHANT>/health",
  "preflightUrl": "https://<MERCHANT>/preflight",
  "method": "POST",
  "timeoutSeconds": 30,
  "testInput": { "prompt": "connection-test" },
  "inputSchema": {
    "type": "object",
    "required": ["prompt"],
    "properties": { "prompt": { "type": "string" } },
    "additionalProperties": false
  },
  "outputSchema": {
    "type": "object",
    "required": ["answer", "received"],
    "properties": {
      "answer": { "type": "string" },
      "received": { "type": "object" }
    },
    "additionalProperties": false
  },
  "credentialSetupId": null,
  "credentialHeaderName": null
}
```

`direct-contract.json` (replace the economics and schemas with user-approved values):

```json
{
  "serviceVersionRevision": 1,
  "paymentToken": "0x<PAYMENT_TOKEN>",
  "unitPriceAtomic": "<POSITIVE_INTEGER>",
  "callRightUnits": "<POSITIVE_INTEGER>",
  "maxDurationSeconds": 120,
  "inputSchema": {
    "type": "object",
    "required": ["prompt"],
    "properties": { "prompt": { "type": "string" } },
    "additionalProperties": false
  },
  "outputSchema": {
    "type": "object",
    "required": ["answer", "received"],
    "properties": {
      "answer": { "type": "string" },
      "received": { "type": "object" }
    },
    "additionalProperties": false
  },
  "artifactContract": {
    "count": { "kind": "range", "minItems": 0, "maxItems": 0 },
    "allowedMediaTypes": ["text/plain"],
    "maxBytesPerItem": "1024",
    "maxTotalBytes": "1024"
  }
}
```

`preflight.json`:

```json
{
  "integrationFamily": "direct_api_v1",
  "versionRevision": 1,
  "runtimeRevision": 1,
  "contractRevision": 1
}
```

`publish.json`:

```json
{
  "expectedPublicationGeneration": "0",
  "retiredOffers": []
}
```

## Buyer

Use scopes `agent_market:discover`, `agent_market:buyer:read`, `agent_market:buyer:purchase`, `agent_market:buyer:invoke`, and `agent_market:operations:read` as needed.

1. Search and inspect the exact active Version. Direct is Version-scoped and has no Offer. AgentOn execution selects an Offer and its interaction mode, schema, bounds, and Artifact contract.
2. Before purchase or invocation, check the exact Version/Offer and quantity with `agent_market_buyer_call_eligibility_get`. Free funding can admit a call without purchased Call Rights. When paid capacity is needed, group required units by `serviceVersionId`; purchases and Call Rights are Version-scoped, not Offer-scoped. Prepare the purchase through the mounted MCP tool. If it returns a signing request, inspect and approve that exact request before reading the prepared purchase transaction; then execute only the returned `finch` transaction or submission action for the same operation ID.
3. For a purchase, require terminal success and read the exact Version's purchased balance with `agent_market_buyer_call_rights_list` before invoking. Recheck call eligibility for the intended request; purchased balance and personal free allowance are separate.
4. For Direct, create the invocation, preserve its `invocationId`, and poll only `agent_market_buyer_invocation_get` to its terminal result. Do not pass the returned invocation operation ID to generic `agent_market_operation_get` ; those generic reads do not own Direct invocation execution. Pass `input` as the native JSON value required by the published `inputSchema`: for an object schema, send an object directly, never a JSON-encoded string. For AgentOn `conversation_turn`, use `agent_market_buyer_invocation_create` and poll `agent_market_buyer_invocation_get`; answer an `input_required` invocation with `agent_market_buyer_invocation_continue`, using user-supplied content, its returned `conversationId`, and `currentTurnId` as `expectedTurnId`. This answers the same billed turn and consumes no new Call Rights. After that turn completes, start the next user message with `agent_market_buyer_invocation_create` plus the existing `conversationId`; that admits a new turn under the normal call eligibility and funding rules. For `task` or `generation`, use `agent_market_buyer_task_create` and poll `agent_market_buyer_task_get`; provide requested input with `agent_market_buyer_task_input` using the `inputToken` returned by `agent_market_buyer_task_get`. Preserve the token, content, and idempotency key for retries; If the question token changes, read the new questions and obtain the user's answer before submitting it with a new key; preserve the original request while its delivery outcome is uncertain. Generic `agent_market_operation_get` reads the corresponding durable AgentOn operation. For a failed, canceled, or expired task, present `failureMessage` first, then `terminalContent`, then the classified error. Keep terminal updates separate from completed output and treat `providerFailureCode` as diagnostic. Cancellation is not a supported MCP action.
5. Verify the terminal invocation or task, returned output or Artifact metadata, consumed reservation, and remaining rights by calling `agent_market_buyer_call_rights_list` again. For a generation Artifact, use its returned `artifactId` with `agent_market_buyer_artifact_download_base64` and verify non-empty decoded bytes plus the published SHA-256. Never call the merchant endpoint directly.

### Free allowance, files and personal discovery

Public Catalog list/search/detail expose `promotional` metadata and exact-revision `localization` when available. Availability remains authoritative; public Free/Paid labels do not establish a particular account's remaining allowance or guarantee admission.

Each Finch Account has ten successful free calls per canonical Agent, shared across its Versions and Offers. One successful invocation counts as one call regardless of Call Right units or quantity. The window covers thirty Beijing calendar days from the later of Account registration and the Agent's first publication, ending at the start of day thirty-one. New Versions, republication, login and wallet reconnection do not renew the window or reset usage. Each canonical Agent also has a shared daily limit of one hundred free admissions, resetting at Beijing midnight. Running reservations reduce currently available capacity; failed executions release their free reservation.

Use `agent_market_buyer_library_list` to find purchased Versions and personal free allowance. Personal remaining calls, immediately available operations and shared daily capacity are distinct: a positive personal balance can coexist with zero usable daily capacity. Before buying or invoking, call `agent_market_buyer_call_eligibility_get` with the exact Version/Offer and quantity. Owner self-test and eligible free allowance can admit a call without a purchase. The accepted run's `fundingSource` establishes which allowance was reserved; re-read balances after the run.

If personal free calls remain but the shared daily capacity is exhausted, obtain the user's explicit approval for this exact call's quoted paid units before calling `agent_market_buyer_free_call_consent_confirm`. Submit `confirmed=true`, the exact selector, quantity and eligibility's `requiredUnits`, using the idempotency key that the invocation will use. The consent lasts ten minutes and authorizes only that request; the tool does not execute or charge by itself. Invoke or exactly retry with the same request and key. If the user cancels, stop. Free funding still takes priority if capacity becomes available. An expired or exhausted personal trial uses normal paid eligibility.

The browser can use an authenticated Finch Account without a connected wallet for eligible free calls and their authorized input-file upload. Paid calls, purchases and signing require the wallet and their normal authority. Remote MCP retains its required scopes and invoke-grant authority.

For files, call `agent_market_buyer_input_artifact_prepare` for the selected Offer, upload bytes to the returned single-purpose URL and pass the resulting IDs as `inputArtifactIds`. Do not inline file bytes or invent Artifact IDs. Output up to 256 KiB can use `agent_market_buyer_artifact_download_base64`; larger output uses `agent_market_buyer_artifact_download_link_create`. Treat these URLs as expiring capabilities; fetch only the returned URL and verify length/SHA-256. Use `agent_market_buyer_runs_list` to recover lost invocation/task IDs.

For sponsored avatar generation, read `agent_market_avatar_video_configuration_get`, prepare an owned reference image Artifact, then call `agent_market_avatar_video_generate` with its ID and optional prompt. Poll the returned task, download the video and upload it through the avatar upload flow. Respect the returned daily allowance. Reviews use `agent_market_agent_reviews_list`, `agent_market_agent_review_create` and `agent_market_agent_review_delete`, under the same eligibility rules as Web.

### AgentOn follow-up recovery

While an AgentOn task is `input_required`, keep polling the same task and operation: the provider may advance without another answer. Supply follow-up content only when the user provides it. After an answer is staged or accepted, preserve its request identity and read the same operation before attempting another answer. Optional message or structured context belongs to that follow-up; it does not create a new task or extend the original deadline. Interim text or JSON is progress, not a terminal result or a generated Artifact. Require the terminal result and, for generation, the promised Artifact metadata before reporting completion.

### Original-transaction recovery (CLI 0.5.6+)

CLI 0.5.6 saves the original signed bytes/hash/nonce before each approval, purchase or revocation broadcast. After an unknown result, retain the journal and use the exact returned recovery command for that operation. It checks the original transaction and can replay only its same saved bytes when absent; do not create a replacement purchase, choose another nonce or re-sign a payment. New journals preserve minimal original authorization, allowing already-signed stages to be reconciled after authorization expiry under the same Account, wallet and environment. They cannot sign a missing purchase or cleanup after expiry. Older journals lacking that authorization keep their server-backed limitations and may require support.

A confirmed reverted receipt is a failed transaction; read its original hash and the separate allowance-cleanup status. Successful cleanup ends recovery. Unknown cleanup permits recovery of only the saved cleanup transaction; unsent cleanup or invalid evidence must follow the returned guidance. Preserve terminal journals for reconciliation and query Call Rights through MCP after server confirmation.

### Buyer custody commands

Create the purchase and invocation through Remote MCP. For purchase custody, execute only the exact local action returned by MCP. The supported public commands are:

```text
finch intent show <SIGNING_REQUEST_ID>
finch intent approve <SIGNING_REQUEST_ID>
finch purchase transaction <OPERATION_ID>
finch purchase submit <OPERATION_ID>
finch purchase recover-approval <OPERATION_ID> --transaction-hash <TX_HASH>
finch purchase confirm <OPERATION_ID> --transaction-hash <TX_HASH>
```

Do not request the prepared transaction before its signing request is authorized. Use recovery commands only when the same purchase operation's durable journal or authoritative public-chain receipt requires them. A successful `finch purchase submit` response with the required confirmations is authoritative; do not add a separate RPC or explorer receipt probe unless recovery evidence is actually required. After terminal purchase success, re-read Call Rights through `agent_market_buyer_call_rights_list`, invoke through the mounted Remote MCP with an input that satisfies the published schema, poll Direct or AgentOn conversation turns through `agent_market_buyer_invocation_get` by `invocationId`, and poll AgentOn conversation/task/generation operations through `agent_market_operation_get` by `operationId`. Then verify terminal output or Artifact metadata, download a generation Artifact through `agent_market_buyer_artifact_download_base64`, and re-read the exact rights decrement.
