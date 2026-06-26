# aicade SDK Capabilities

Use this reference when deciding which SDK modules to mention in the final prompt and what constraints the prompt should add.

This file is adapted from the SDK reference and rewritten for skill usage. It is not a full API manual. It focuses on:

- what each module is for
- which methods and events matter in prompt writing
- how to translate SDK details into implementation constraints

## Integration Order

Always preserve this order in prompts when the app uses the SDK:

1. Create an `AicadeSDK` instance
2. Call `init(...)` once
3. Call `waitForReady()` before business calls
4. Get modules with `getModule(...)`
5. Reuse module instances instead of recreating them
6. Subscribe to events when UI needs to follow account, score, currency, or stream changes
7. Call `destroy()` on teardown when appropriate

## Core SDK Surface

These SDK-level methods are safe to reference in prompts:

- `init(options: InitOptions): Promise<void>`
- `waitForReady(): Promise<void>`
- `destroy(): Promise<void>`
- `getModule<T extends IModule>(name: ModuleType): T`
- `Login(): Promise<AccountInfo>`
- `GetAccountInfo(): AccountInfo | null`
- `on(eventType, callback): RemoveListener`
- `off(eventType, callback?): boolean`

Advanced bridge-style methods also exist, but should only be mentioned when clearly needed:

- `post(namespace, method, ...args)`
- `tryPost(namespace, method, ...args)`
- `fetchObject(namespace, method, ...args)`
- `tryFetchObject(namespace, method, ...args)`

Do not instruct the model to call unsupported or undocumented runtime methods. For example, `execute(...)` is explicitly not supported.

## SDK-Level Events

These top-level events are useful when the app must stay in sync with account or point changes:

- `AccountChanges` -> payload: `AccountInfo`
- `PointCurrencyChange` -> payload: `number`

Prompt implication:

- if the UI shows wallet/account state, ask for event-driven UI updates
- if the UI shows platform point balance, ask for event subscriptions rather than one-time reads only

## iframe Sandbox Constraints

Apps integrated with this SDK are ultimately rendered inside an iframe with:

```html
sandbox="allow-scripts allow-modals"
```

Because `allow-same-origin` is not enabled, the iframe is treated as an opaque origin. Prompts should assume these restrictions by default.

### Browser capabilities that may fail or be blocked

- `cookie`
- `localStorage`
- `sessionStorage`
- `IndexedDB`
- `document.domain`
- direct parent/child DOM access
- `window.parent.xxx`
- `top.location`
- `window.open`
- form submission flows
- file downloads
- `ServiceWorker`

### Network-side risks

Requests may carry `Origin: null`, which can cause:

- login state failures
- CORS rejection
- CSRF validation failure

### Required replacement strategies

When prompts describe cross-frame or storage behavior, prefer these replacements:

- use `ajax` requests or SDK modules for business data access and interaction
- use token injection instead of cookie-based login assumptions
- use URL parameters when the host injects context safely
- use a server-side proxy when direct cross-origin requests are not reliable
- use `LocalStorageTools` instead of browser `localStorage` and `cookie`

### Error compatibility

Prompt constraints should explicitly ask the implementation to tolerate and handle errors such as:

- `SecurityError`
- `Blocked a frame with origin ...`
- `Failed to read 'localStorage' ...`

### Prompt implication

When the app depends on embedding behavior, the final prompt should state that:

- the app runs inside a sandboxed iframe
- same-origin assumptions are unsafe
- browser storage, parent DOM access, popup flows, and Service Worker assumptions must be avoided
- business data access should prefer `ajax` or SDK modules instead of parent frame object access
- browser `cookie` and `localStorage` assumptions must be replaced

## Upload Script Rule

When a new project needs upload support:

- copy `upload.js` directly from `https://github.com/aicade-galaxy/aicade-ts-bootstrap/blob/main/upload.js`
- do not rewrite the upload script
- do not ask the model to infer or rebuild upload behavior from scratch
- treat the upstream `upload.js` as the source of truth unless the user explicitly asks to refresh it from the official repository

If the user decides to use AI to reimplement the project in the required stack, start from the official scaffold repository:

- `https://github.com/aicade-galaxy/aicade-ts-bootstrap`

That scaffold already includes the official upload script and upload command, so do not rebuild those pieces manually.

The scaffold upload flow reads these environment variables:

- `AICADE_API_KEY` / `VITE_AICADE_API_KEY` / `DAPP_KEY`
- `AICADE_API_SECRET_KEY` / `VITE_AICADE_API_SECRET_KEY` / `DAPP_SECRET_KEY`

Optional overrides:

- `VITE_AICADE_API_UPLOAD` or `UPLOAD_URL` only when the default upload URL must be replaced
- `AICADE_API_URL` / `VITE_AICADE_API_URL` only when the default base `https://aicadegalaxy.com/v1` must be customized

Do not ask twice for key/secret values when the access variables have already been saved locally, because `AICADE_API_KEY = VITE_AICADE_API_KEY` and `AICADE_API_SECRET_KEY = VITE_AICADE_API_SECRET_KEY` for this skill workflow.
Use the default `AICADE_API_URL = VITE_AICADE_API_URL = https://aicadegalaxy.com/v1` unless the user explicitly overrides it.

## Module Selection Guide

Choose only the modules the app actually needs. Do not ask the model to integrate every SDK module by default.

## Integration Layers For This Skill

When this skill confirms integration scope with the user, split it into 3 layers:

### 1. Base requirements

These are mandatory:

- SDK initialization flow (`AicadeSDK`, `init(...)`, `waitForReady()`, `getModule(...)`)
- app lifecycle level integration when the app is built on the aicade runtime

### 2. Compatibility requirements

These are also mandatory when relevant compatibility risks exist:

- `LocalStorageTools` as the replacement for browser `localStorage`
- iframe sandbox compatibility constraints
- opaque-origin safe networking and error handling

### 3. SDK modules

Treat real SDK modules separately from non-module requirements.

Real modules include:

- `Application`
- `LocalStorageTools`
- `Ticket`
- `AppScore`
- `AicadeCurrency`
- `AIChat`
- `AICoinMarket`
- `Token`
- `NftOwner`

Do not describe non-module requirements such as SDK init order, iframe compatibility, wallet display, or point-balance display as if they were SDK modules.

### 4. Extension modules

These require explicit user confirmation before inclusion:

- `Ticket`
- `AppScore`
- `AicadeCurrency`
- `AIChat`
- `AICoinMarket`
- `Token`
- `NftOwner`

Do not auto-enable extension modules just because they exist.

If an extension module has business parameters, confirm them explicitly. Example:

- `AicadeCurrency` exchange ratio
- daily exchange cap
- exchange trigger timing
- `Ticket` payment mode expectations
- `Token` swap-related display or action requirements

### `Application`

Primary use:

- app metadata
- application lifecycle

Key methods:

- `GetInfo(): Promise<ApplicationInfo>`
- `Exit(): void`

Prompt hints:

- include when the app needs app metadata, title, identifiers, or explicit exit behavior
- avoid mentioning if the app has no lifecycle-specific behavior beyond normal rendering

### `Ticket`

Primary use:

- access gate
- purchase / subscription / play eligibility

Key properties:

- `CurPaymentMethod`: `"free" | "one" | "subscribe"`
- `CanPlay`: `boolean`

Key methods:

- `refresh(): Promise<boolean>`
- `buy(): Promise<boolean>`
- `play(): Promise<boolean>`

Events:

- `TicketChanges` -> payload: `boolean`

Prompt hints:

- include when the app has gated access, paid unlock, subscription flow, or play permission checks
- ask the implementation to refresh ticket state before access-sensitive actions
- if the UI reflects access state, ask for `TicketChanges` subscriptions

### `AppScore`

Primary use:

- score persistence
- leaderboard

Key property:

- `CurScore: number`

Key methods:

- `refresh(): Promise<number>`
- `getRanks(): Promise<AppScoreRank[]>`
- `setScore(score: number): Promise<number>`

Events:

- `AppScoreChanges` -> payload: `number`

Prompt hints:

- include only when the app actually has score semantics or leaderboard requirements
- ask for score refresh before score display if stale state matters
- if the score UI updates live, ask for `AppScoreChanges` subscriptions

### `AicadeCurrency`

Primary use:

- platform point and token balance
- point consumption
- app-to-platform point exchange

Key property:

- `CurrencyBlanaces: { token: BN; point: number; pointOfChain: BN }`

Key methods:

- `refreshPoint(): Promise<void>`
- `refresh(): Promise<void>`
- `consume(num: number, scene: string, message?: string): Promise<number>`
- `obtain(scene: string, expendNum: number, rewardAicadeScore: number): Promise<number>`

Related global event:

- `sdk.on("PointCurrencyChange", cb)`

Prompt hints:

- include when the app needs to show platform point balance, consume points, or exchange app rewards into platform points
- if exchange is enabled, specify:
  - exchange trigger
  - exchange ratio
  - daily cap if the business requires it
- if balance appears in the UI, ask for refresh plus event-driven sync

### `AIChat`

Primary use:

- chat sessions
- chat history
- sending user messages

Key methods:

- `getSessionList(): Promise<AIChatSession[]>`
- `createSession(firstMessage: string): Promise<AIChatSession>`
- `getMessages(sessionId: string): Promise<AIChatMessage[]>`
- `createMessage(sessionId: string, message: string): Promise<AIChatMessage>`

Prompt hints:

- include when the app contains an AI assistant, Q&A area, or conversational workflow
- ask for a clear session list, message list, input box, loading state, and error state
- do not invent streaming behavior here unless another module provides it

### `AICoinMarket`

Primary use:

- market assistant integration
- streaming messages
- MCP-related message workflows

Key methods:

- `bindApiKey(apiKey: string, secretKey: string): Promise<boolean>`
- `getApiKey(): Promise<string>`
- `unbindApiKey(): Promise<boolean>`
- `createEventSource(): Promise<boolean>`
- `sendMessage(content: string): Promise<boolean>`
- `getMessages(): Promise<AICoinMarketMessageResponse[]>`

Event:

- `OnReciveMessage(cb)` -> payload: `AICoinMarketMessageResponse`

Prompt hints:

- include only when the app needs market-assistant messaging or stream updates
- if used, ask for stream lifecycle handling, message history, and reconnect/error UI
- mention event-driven message updates instead of polling-only designs when real-time behavior matters

### `Token`

Primary use:

- token balance
- token swap flow

Key methods:

- `balanceOf(address: string): Promise<BN>`
- `swap(request: TokenSwapInfo): Promise<void>`

Prompt hints:

- include when the app needs token balance display or swap actions
- ask for numeric formatting and transaction-state feedback
- if balance is shown, ask for proper BN formatting rather than raw values

### `NftOwner`

Primary use:

- NFT ownership
- NFT avatar

Key methods:

- `GetAllContracts(): Promise<NftContractInfo[]>`
- `GetNftTokenList(nftContract: string, forceRefresh?: boolean): Promise<NftTokenInfo[]>`
- `GetAvatar(): Promise<NftAvatarInfo>`
- `SetUpUserAvatar(contractAddress: string, token: string): Promise<NftAvatarInfo>`

Prompt hints:

- include when the app shows owned NFTs, contract lists, or avatar setup
- if avatar setup is present, ask for preview, selection state, and update feedback

### `LocalStorageTools`

Primary use:

- app-scoped storage instead of browser storage

Key methods:

- `setItem(key: string, value: string): Promise<void>`
- `getItem(key: string): Promise<string | null>`
- `removeItem(key: string): Promise<void>`
- `clear(): Promise<void>`

Prompt hints:

- include whenever the app would otherwise use `localStorage`
- explicitly tell the model to replace browser `localStorage` with `LocalStorageTools`
- ask for serialization discipline if complex objects are stored

## Utilities Worth Mentioning

These helpers exist and can be referenced when the app handles token-style numbers or polling:

### Number and Web3 helpers

- `Web3Utils.parseUnits`
- `Web3Utils.parseEther`
- `Web3Utils.format`
- `bigNumber`
- `bigNumberToInt`
- `formatBN`

Use them when:

- the app shows token balances
- the app converts between human-readable and on-chain units
- the app must avoid raw BN display in the UI

### Runtime helpers

- `detectPlatform()`
- `waitUntil(onCheck, checkInterval?)`

Use them sparingly. In prompts, it is usually enough to ask for platform-aware initialization or guarded async readiness.

## Prompt Assembly Rules

When this skill assembles the final prompt:

1. Mention only the selected SDK modules
2. Always include mandatory base integration and mandatory compatibility integration
3. Add extension-module constraints only if the user confirmed that module
4. Keep initialization order explicit: `init(...)` -> `waitForReady()` -> module usage
5. Ask for event-driven UI sync when events exist and the UI depends on live state
6. Ask for `LocalStorageTools` whenever persistent local state is needed
7. Add exchange rules only if exchange capability is explicitly enabled and its parameters were confirmed
8. Add iframe sandbox constraints because the final app runs inside a sandboxed iframe
9. Do not promise unsupported APIs or private internals

## Error Handling Guidance

These constraints are worth carrying into prompts:

- wrap async SDK calls in `try/catch`
- validate required params before calling SDK APIs
- provide fallback UI for network, auth, or signature failures
- store and release listener remove functions
- do not assume balances, scores, or chat history are immediately available before refresh/ready steps

## Good Prompt Fragments

Use phrasing like:

- "Initialize the SDK with `init(...)`, then call `waitForReady()` before any business module usage."
- "Use `LocalStorageTools` instead of browser `localStorage`."
- "Subscribe to account, score, point, or stream events when the UI depends on live updates."
- "Only integrate the selected SDK modules; do not add unused platform capabilities."

Avoid phrasing like:

- "Use all available SDK modules."
- "Call undocumented runtime methods."
- "Use `localStorage` for convenience."
