# AI/LLM Builds Checklist — Architecture Critic

Specific checks for any build that includes AI calls, LLM integrations, or AI-assisted features. These failure modes are unique to AI components and routinely missed in standard code review.

---

## ⚡ Hot Path vs Async AI Calls

- [ ] **AI not in synchronous request path** — if AI call latency (2-30s) exceeds acceptable response time, move to async job queue
- [ ] **Loading states defined** — UI shows meaningful progress during AI calls; no blank screens or silent hangs
- [ ] **Timeout set** — all AI API calls have explicit timeouts; no infinite waits on provider outages
- [ ] **Streaming where appropriate** — long completions use streaming (`stream: true`) to unblock UI; not waiting for full response
- [ ] **Background job infrastructure** — if async, job queue (Redis/BullMQ/Inngest) chosen and failure/retry behavior defined
- [ ] **User feedback on delay** — if >3s expected, user sees progress indicator with context ("Analyzing document...")

---

## 🤖 Model Selection

- [ ] **Right model for the task** — GPT-4/Claude Sonnet not used where GPT-3.5/Haiku/Flash is sufficient; cost/quality tradeoff documented
- [ ] **Model version pinned** — specific model version specified (e.g., `claude-3-5-haiku-20241022`), not floating alias
- [ ] **Context window fit** — input + expected output fits within model's context window; no silent truncation
- [ ] **Multimodal requirement justified** — vision/audio models only used when the task actually requires them
- [ ] **Cost per call estimated** — token cost calculated for average and worst-case inputs; monthly cost at expected volume acceptable

---

## 🎯 Prompt Injection Surface Area

- [ ] **User content delimited** — user-supplied content wrapped in XML tags or clear delimiters: `<user_input>...</user_input>`
- [ ] **System prompt sealed** — instructions in system prompt; user input cannot override the system prompt via injection attempts
- [ ] **Sensitive data in prompts** — PII, financial data, credentials not included in prompts unless strictly necessary and encrypted at rest
- [ ] **Tool call allowlist** — if model can call tools/functions, only allowed tool names and schemas accepted; model can't invoke arbitrary functions
- [ ] **Recursive prompt injection** — if model processes external content (web pages, emails, documents), content treated as untrusted data, not instructions
- [ ] **Output sandboxing** — if AI output is rendered as HTML, it's sanitized; if executed as code, it's validated against schema

---

## 💰 Token Cost Estimation

- [ ] **Input token budget defined** — max prompt length calculated and enforced; dynamic content (retrieved docs) capped
- [ ] **Output token limit set** — `max_tokens` parameter set; no unbounded completions
- [ ] **Monthly cost projection** — `(avg_input_tokens + avg_output_tokens) × price_per_token × monthly_calls` calculated and within budget
- [ ] **Cost spike protection** — per-user or per-account monthly token budget enforced; runaway usage triggers alert or cutoff
- [ ] **Embedding costs** — if using embeddings, per-document and per-query costs calculated separately
- [ ] **Caching strategy** — identical or near-identical prompts cached (semantic cache or exact key); not re-running expensive calls

---

## 🌊 Streaming vs Batch Tradeoffs

- [ ] **Streaming justified** — streaming used for real-time UX (chat, live generation); not used for background processing where batch is simpler
- [ ] **Streaming error handling** — partial stream failures handled gracefully; partial output not stored as complete
- [ ] **Batch appropriate for bulk** — bulk operations (processing 1000 documents) use Anthropic/OpenAI batch APIs where available (60-70% cost reduction)
- [ ] **Stream cancellation** — client can cancel in-flight stream; server-side abort on client disconnect to stop token consumption
- [ ] **SSE/WebSocket choice justified** — Server-Sent Events for one-way streams; WebSockets only if bidirectional communication required

---

## 🛡️ Fallback When AI Is Unavailable

- [ ] **Provider outage handled** — `try/catch` around all AI calls; graceful degradation defined (cached response, simplified non-AI flow, clear error message)
- [ ] **Retry with backoff** — transient errors (429, 503) retried with exponential backoff; not retried on 400/invalid request errors
- [ ] **Circuit breaker** — if provider fails N times in window, circuit opens; system falls back without hammering provider
- [ ] **User-facing error message** — "AI features temporarily unavailable" message shown; not an opaque 500 error
- [ ] **Critical path independence** — core business functionality (checkout, auth, data read) works without AI; AI is enhancement, not dependency
- [ ] **Multi-provider fallback** — for critical AI features, fallback provider configured (Anthropic → OpenAI, or vice versa)

---

## ✅ Output Validation Before Use

- [ ] **Schema validation** — structured AI outputs (JSON) parsed and validated against Zod/JSON Schema before use
- [ ] **Never trust AI math** — calculated values (prices, scores, quantities) verified against ground truth; AI output not used as source of truth for financial data
- [ ] **Hallucination guards** — citations, URLs, product names from AI responses verified against known data before display
- [ ] **Length/format validation** — output length and format checked before storing; truncated or malformed output rejected
- [ ] **Injection in output** — AI-generated content rendered safely; no `dangerouslySetInnerHTML` with unvalidated AI text
- [ ] **Null/empty output handled** — empty completions, refusals, and content policy blocks handled explicitly; not treated as valid output

---

## 🚦 Rate Limit Handling

- [ ] **Per-provider rate limits known** — TPM (tokens/min), RPM (requests/min) limits documented for chosen tier
- [ ] **429 handled** — `Too Many Requests` response retried with `Retry-After` header honored; not ignored
- [ ] **Request queuing** — high-volume scenarios use queue to smooth request rate; not fire-and-forget loops
- [ ] **Per-user rate limits** — users cannot individually consume provider limits; per-user call/token budget enforced
- [ ] **Burst handling** — sudden traffic spike doesn't exhaust monthly token budget in hours; rate cap on endpoint

---

## ⚠️ Common AI Build Anti-Patterns

| Anti-Pattern | Risk | Correct Approach |
|---|---|---|
| `JSON.parse(aiOutput)` without try/catch | Malformed JSON crashes server | Validate + catch; retry if malformed |
| System prompt includes user's API keys | Keys visible in prompt logs | Never put credentials in prompts |
| All users share one token budget | One power user burns quota for all | Per-user token accounting |
| AI on hot path with no timeout | Provider latency spikes freeze UI | `Promise.race()` with timeout fallback |
| Prompt built with string concatenation | Prompt injection via user-controlled content | XML delimiters; structured message array |
| Model version as floating alias | Surprise behavior change on model update | Pin specific version; test before upgrading |
| AI output stored without validation | Garbage in, garbage out — downstream failures | Schema validate all structured outputs |
