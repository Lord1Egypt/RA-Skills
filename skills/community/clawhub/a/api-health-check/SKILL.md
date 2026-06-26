---
name: api-health-check
description: Check the health and status of popular AI APIs and services — OpenAI, Anthropic, Pollinations, OpenRouter, Gemini, and more. Use when the user wants to know if an API is down, verify service status, or troubleshoot connectivity issues.
---

# API Health Check

Quickly checks if major AI APIs and services are operational. Perfect for troubleshooting or verifying service availability.

## APIs Checked

- OpenAI (api.openai.com)
- Anthropic (api.anthropic.com)
- Google Gemini (generativelanguage.googleapis.com)
- Pollinations (image.pollinations.ai, text.pollinations.ai)
- OpenRouter (openrouter.ai)
- Stability AI (api.stability.ai)
- Groq (api.groq.com)

## Usage

```
check api status
is openai down?
check pollinations health
```

## How it works

1. Makes lightweight HEAD/GET requests to API endpoints
2. Checks HTTP status codes and response times
3. Reports status: ✅ UP, ❌ DOWN, ⚠️ SLOW
4. Returns summary table of all services

## Script

```
python scripts/check_apis.py [specific_api_name]
```

Without arguments, checks all APIs. With argument, checks only that service.

## Output Example

```
API Health Status:
✅ OpenAI      - UP (234ms)
✅ Anthropic   - UP (189ms)
❌ Pollinations - DOWN (timeout)
✅ OpenRouter  - UP (412ms)
```