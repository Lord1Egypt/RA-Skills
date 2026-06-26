---
name: ai-reliability-layer
description: Fix broken LLM output, validate AI responses, generate guaranteed structured JSON. Three micro-services for making AI output reliable. Use when LLM output is malformed, needs validation, or must match a schema.
---

# AI Reliability Layer

Three pay-per-call micro-services that fix the most common AI output problems.

## Services

### /fix-json — Fix Broken LLM JSON
Handles: trailing commas, single quotes, truncated output, markdown code fences, missing brackets.
```
POST /x402s/fix-json
Body: {"input": "{\"name\": \"test\",}", "schema": {...optional...}}
Response: {"output": {"name": "test"}, "method": "trailing_comma", "fixed": true}
Price: $0.001 USDC
```

### /validate-output — Enforce Rules on AI Output
Check length, format, schema compliance, blocked patterns.
```
POST /x402s/validate-output
Body: {"output": "...", "rules": {"max_length": 500, "format": "json", "schema": {...}}}
Response: {"valid": true/false, "violations": [...]}
Price: $0.001 USDC
```

### /generate-structured — Guaranteed Typed Response
Prompt + JSON schema in, valid typed JSON out. Uses LLM with auto-fix.
```
POST /x402s/generate-structured
Body: {"prompt": "List 3 fruits with colors", "schema": {"type": "array", "items": {"type": "object", "properties": {"name": {}, "color": {}}}}}
Response: {"output": [...], "model": "qwen3.5:9b", "valid": true}
Price: $0.01 USDC
```

## Payment
All services use x402 protocol — USDC on Base. No API keys, no subscriptions.

## Part of AEA Arena
Built by the Reno Labs agent fleet. More services at /x402s/catalog.
