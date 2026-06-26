---
name: free-api-discovery
description: Discover which free or low-cost AI APIs are reachable from the current environment, verify them safely, and recommend a task-to-provider routing plan.
tags: [ai, api, discovery, llm, model, free, devops]
version: 1.0.1
---

# Free AI API Discovery and Routing

## When to use

- You need to find which AI APIs are reachable from the current environment.
- You want a low-cost fallback when a preferred provider is unavailable.
- You need a simple routing recommendation for chat, code, speech, or multimodal tasks.

## Workflow

1. Check network reachability.
   Probe candidate endpoints with a short timeout and record whether the host is reachable.
2. Verify credentials only after approval.
   Ask for the minimum key needed and avoid printing full secrets in logs.
3. Test one capability at a time.
   Confirm chat, model listing, speech, or image endpoints separately.
4. Recommend routing.
   Map each task type to the lowest-cost reliable provider that actually worked.

## Example reachability probe

```python
import socket
import ssl
import urllib.error
import urllib.request

socket.setdefaulttimeout(8)
ctx = ssl.create_default_context()

services = {
    "Groq": "https://api.groq.com",
    "OpenRouter": "https://openrouter.ai/api/v1",
    "DeepSeek": "https://api.deepseek.com",
    "Mistral": "https://api.mistral.ai/v1",
}

for name, url in services.items():
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=6) as resp:
            print(f"{name}: HTTP {resp.status}")
    except urllib.error.HTTPError as exc:
        print(f"{name}: HTTP {exc.code} (reachable, auth may be required)")
    except Exception as exc:
        print(f"{name}: not reachable ({exc})")
```

## Recommended output

- Reachable providers
- Providers that need valid credentials
- Best provider by task type
- Cost or quota notes
- Risks or missing coverage

## Guardrails

- Do not store API keys unless the user explicitly approves it.
- Mask secrets in notes and logs.
- Keep routing recommendations based on verified results, not assumptions.
- Treat provider availability and quotas as time-sensitive and re-check when needed.
