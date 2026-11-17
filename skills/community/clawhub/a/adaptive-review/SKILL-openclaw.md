---
name: adaptive-review-openclaw
description: Adaptive code review using local/self-hosted models via OpenAI-compatible API. No cloud API required. Routes to small/medium/large local models based on diff complexity.
---

# Adaptive Code Review (OpenClaw / Local LLM Edition)

Same adaptive routing logic as the cloud version, but targets local or self-hosted models via any OpenAI-compatible API endpoint (vLLM, SGLang, Ollama, LiteLLM, OpenClaw, etc.).

**Zero cloud API cost. Full privacy. Works offline.**

## Model Tiers

Configure these environment variables or hardcode your endpoints:

```bash
# Example: Ollama
ADAPTIVE_REVIEW_FAST_MODEL="qwen2.5:3b"
ADAPTIVE_REVIEW_FAST_ENDPOINT="http://localhost:11434/v1"

# Example: vLLM with larger model
ADAPTIVE_REVIEW_MEDIUM_MODEL="qwen2.5-coder:14b"
ADAPTIVE_REVIEW_MEDIUM_ENDPOINT="http://localhost:8000/v1"

# Example: OpenClaw router (picks best available)
ADAPTIVE_REVIEW_DEEP_MODEL="claude-proxy"
ADAPTIVE_REVIEW_DEEP_ENDPOINT="http://localhost:3456/v1"
```

| Depth | Default model | Fallback | Use case |
|-------|--------------|----------|----------|
| fast | qwen2.5:3b | Any <7B model | formatting, naming, obvious bugs |
| medium | qwen2.5-coder:14b | Any 7-30B model | standard code review |
| deep | Best available (70B+ or cloud proxy) | medium model | architecture, security, cross-module |

## Step 1: Collect Signals

Same as cloud version — pure git commands, no LLM calls:

```bash
BASE=$(git merge-base HEAD origin/main 2>/dev/null || echo "HEAD~1")
git diff --numstat $BASE..HEAD
```

Extract: **lines_changed**, **files_changed**, **dirs_changed**

Risk scan (code files only):
```bash
git diff $BASE..HEAD -- '*.ts' '*.js' '*.py' '*.go' '*.rs' '*.java' '*.c' '*.cpp' '*.rb' '*.sh' | grep -ciE '(password|secret|token|auth|session|cookie|sql|inject|exec\(|eval\(|lock|mutex|semaphore|atomic|concurrent|unsafe)'
```

## Step 2: Route

| Condition | Depth | Model tier |
|-----------|-------|------------|
| lines < 50 AND files <= 1 AND risk_hits == 0 | **fast** | small (3B) |
| lines < 200 AND dirs <= 1 AND risk_hits <= 2 | **medium** | medium (14B) |
| Everything else | **deep** | large (70B+) |

## Step 3: Execute Review

For each depth, call the configured endpoint with a review prompt.

### Fast review prompt
```
Review this diff for: formatting issues, naming conventions, obvious bugs, unused imports.
Be concise. Skip architecture analysis.

<diff>
{GIT_DIFF}
</diff>
```

### Medium review prompt
```
Review this code change for:
1. Correctness — logic errors, edge cases, off-by-one
2. Error handling — missing checks, silent failures
3. Code quality — readability, DRY, naming
4. Test coverage — are changes tested?

For each issue: file:line, what's wrong, severity (critical/important/minor).

<diff>
{GIT_DIFF}
</diff>
```

### Deep review prompt
```
Comprehensive code review:
1. Architecture — design decisions, separation of concerns, scalability
2. Security — injection, auth bypass, data exposure, unsafe operations
3. Performance — algorithmic complexity, unnecessary allocations, N+1 queries
4. Cross-module impact — breaking changes, API contract violations
5. Correctness — logic, edge cases, concurrency issues
6. Test adequacy — coverage, meaningful assertions, missing scenarios

For each issue: file:line, what's wrong, severity, suggested fix.
Flag anything that could cause production incidents.

<diff>
{GIT_DIFF}
</diff>
```

### Calling the API

Use curl or your preferred HTTP client to hit the OpenAI-compatible endpoint:

```bash
curl -s "$ENDPOINT/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "'$MODEL'",
    "messages": [{"role": "user", "content": "'$PROMPT'"}],
    "temperature": 0.3,
    "max_tokens": 2048
  }'
```

Or use the Agent tool to spawn a subagent that calls your local endpoint.

## Step 4: Report

```
## Adaptive Review: [FAST|MEDIUM|DEEP] (Local)
Model: {model_name} @ {endpoint}
Signals: {lines} lines, {files} files, {dirs} dirs, {risk_hits} risk hits

[review output]
```

## Overrides

- `/adaptive-review-openclaw --fast` — force small model
- `/adaptive-review-openclaw --deep` — force large model
- `/adaptive-review-openclaw --model qwen2.5:32b` — force specific model

## Compatible backends

Any OpenAI-compatible `/v1/chat/completions` endpoint:
- **Ollama** — easiest setup, `ollama serve`
- **vLLM** — best throughput for GPU servers
- **SGLang** — best for structured output
- **LiteLLM** — proxy to any backend
- **OpenClaw** — multi-model router with dashboard
- **text-generation-webui** — UI + API
- **llama.cpp server** — minimal, CPU-friendly
