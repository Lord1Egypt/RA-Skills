# AI Orchestrator — Phase 1: Network-First Pipeline

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    ask-puppeteer.js                         │
│                                                              │
│  sendPrompt()  →  prepareForRequest()                       │
│     │                  │                                    │
│     │            windowOpen = true                          │
│     │            expectedRequestIds prepared                │
│     │                                                        │
│     ↓                                                        │
│  Page: вставляем текст → Enter                                │
│                                                              │
│  CDP: Network.requestWillBeSent                              │
│    → filter: /completion, POST, postData > 10 chars          │
│    → window = false (caught first only)                      │
│    → expectedRequestIds.add(requestId)                       │
│                                                              │
│  CDP: Network.loadingFinished                                │
│    → if expectedRequestIds.has(requestId) && !resolved:      │
│      → getResponseBody(requestId)                            │
│      → parseDeepSeekBody(raw)                                │
│        └─ DeepSeek custom event-stream:                      │
│           data: {"v":{"response":{"fragments":[{"content":"X"}]}}}
│           data: {"p":"response/fragments/...","o":"APPEND","v":"text"}
│           data: {"v":"char"}                                 │
│         └─ Standard JSON fallback:                            │
│           choices[0].message.content                          │
│         └─ SSE fallback:                                     │
│           data: {"choices":[{"delta":{"content":"X"}}]}       │
│      → resolved = true, result = {text, format}             │
│                                                              │
│  waitForAnswer():                                            │
│    STAGE 1: cdpInterceptor.waitForResponse()                 │
│      → if text >= 2 chars: return immediately               │
│      → else: cleanupState() → STAGE 2                        │
│    STAGE 2: _waitForAnswerDOM() — DOM polling fallback       │
│                                                              │
│  handleContinueButton():                                     │
│    → single page.evaluate() — find Continue button           │
│    → prepareForRequest() BEFORE click                       │
│    → page.mouse.click(x,y)                                   │
│    → network-first Continue → _dedupeDelta()               │
│    → DOM polling fallback if network fails                   │
└────────────────────────────────────────────────────────────┘
```

Key components:
- **Per-request correlation**: `windowOpen` flag + `expectedRequestIds` Set — only catches OUR request
- **postData filter**: Ignores requests with postData < 10 chars (not our prompt)
- **Multiple resolve protection**: `resolved` flag + `doResolve()` helper
- **cleanupState()**: Called on ALL exit paths (success, fallback, dry-run, exception)
- **6-layer dedupe**: prefix → suffix+word-boundary → paragraph → list-markers → code-fences → fallback

## Performance

| Metric | Before (Phase 0) | After (Phase 1) | Improvement |
|--------|-----------------|-----------------|-------------|
| Short answer (<50 chars) | ~15-20s (15s idle) | **1.5s** | -90% |
| Medium answer (200-500 chars) | ~15-20s | **2.8-9.9s** | -50% |
| Long answer (20k+ chars) | ~30-45s | **153.9s** (server gen time) | 0% (server bottleneck) |

The 15-second idle timeout has been **eliminated for all network-extracted answers**.

### Test Results (2026-04-05)

| Test | Answer | Answer Wait | Method |
|------|--------|-------------|--------|
| "What is 2+2?" | 9 chars | 1.5s | ✅ CDP network |
| "Briefly explain HTTP" | 345 chars | 2.8s | ✅ CDP network |
| "API explain (Russian)" | 1,324 chars | 9.9s | ✅ CDP network |
| JSON→YAML (71k input) | 21,705 chars | 153.9s | ✅ CDP network |
| Epic poem | 5,667 chars | 35.0s | ✅ CDP network |

## Limitations

### DeepSeek Free Tier
- **~13k tokens** soft limit per response — model truncates long answers automatically
- **Server sends `FINISHED`** in the SSE stream without showing a UI Continue button
- **Continue button does not appear** for free tier long responses — the code path exists but is not triggered
- The `parseDeepSeekBody` parser handles the **custom DeepSeek event-stream format** (not standard OpenAI SSE):
  - `data: {"v": {"response": {"fragments": [{"content": "..."}]}}}` — seed
  - `data: {"p": "response/fragments/-1/content", "o": "APPEND", "v": "text"}` — delta
  - `data: {"v": "char"}` — direct char delta
  - `data: {"p": "response/status", "o": "BATCH", "v": [...]}` — skip (metadata)
  - `data: {"p": "response/status", "o": "SET", "v": "FINISHED"}` — skip (status)
  - `event: close` — end of stream

### Why Real-Time Streaming (Phase 2) Was Rejected

Three approaches were tested via spike:

1. **`Network.streamResourceContent(requestId)`** → returns stream handle, BUT:
   - `Stream.read()` CDP method is **not available** in our Chromium version (Chromium 146)
   - `streamResourceContent` returns `stream: undefined`

2. **`Network.dataReceived` events** → fires during streaming, BUT:
   - `dataReceived.data` field is **empty** (no text data provided)
   - Only reports byte counts, not content
   - Requires `streamResourceContent` to be called first (which doesn't work)

3. **Fetch API interception in page context** → would work technically but:
   - Conflicts with DeepSeek's own JavaScript
   - Adds complexity and instability
   - Not worth the risk for free tier where the server already truncates responses

**Bottom line**: CDP can only get the response body AFTER server completes generation (`loadingFinished`). The bottleneck for long answers is **server-side generation time**, not network extraction latency.

### When Phase 2 Makes Sense

| Scenario | Approach | Expected Gain |
|----------|----------|---------------|
| **DeepSeek paid API** | Direct HTTP POST → stream SSE response | Real-time tokens, no browser needed |
| **Server-side integration** | Proxy through own backend | Full control of streaming |
| **Different Chromium** | Newer CDP with working `Stream.read()` | Progressive body reads |
| **Different LLM** | Providers that show Continue button UI | Continue logic already implemented |

## Files Changed

```
skills/ai-orchestrator/
├── ask-puppeteer.js          ← Phase 1 refactoring (+190 lines net)
└── ask-puppeteer.js.bak-20260405-110340  ← Original backup

Backup location:
  ~/.openclaw/workspace/skills/ai-orchestrator/ask-puppeteer.js.bak-20260405-110340
```

### Modified Functions

| Function | Change |
|----------|--------|
| `setupDeepSeekInterceptor()` | ~60 → ~165 lines — per-request correlation, parseDeepSeekBody, cleanupState |
| `sendPrompt()` | +5 lines — prepareForRequest() before sending |
| `waitForAnswer()` | ~150 → ~60 lines — network-first + DOM fallback split |
| `_waitForAnswerDOM()` | New ~140 lines — polling backoff, priority selectors |
| `handleContinueButton()` | Reworked — single evaluate, prepare before click, dedupe |
| `_dedupeDelta()` | New ~100 lines — 6-layer deduplication |
| `ensureBrowser()` | +10 lines — evaluateOnNewDocument before goto |

### Commits

```
c2d19f9  refactor(ai-orchestrator): Phase 1 network-first pipeline via CDP
e5d150f  fix(ai-orchestrator): fix parseDeepSeekBody for DeepSeek custom event-stream
```

## How to Revert

```bash
cd ~/.openclaw/workspace/skills/ai-orchestrator
git revert c2d19f9 e5d150f
# Or restore from backup:
cp ask-puppeteer.js.bak-20260405-110340 ask-puppeteer.js
pm2 restart deepseek-daemon
```
