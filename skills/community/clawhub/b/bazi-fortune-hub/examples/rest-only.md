# REST-Only Agents

> Members of this family cannot speak MCP, or the deployment environment blocks
> long-lived connections. They consume the same 12 tools via the universal REST
> envelope at `POST /api/universal/[category]/[name]`. **All protocol details
> (12 tools, error codes, billing) live in [`../SKILL.md`](../SKILL.md) — do not duplicate.**

## Verified members

These rows are backed by a runnable snippet below. Other agents in this family are
listed under [Unverified members](#unverified-members) — see the policy in
[`./README.md`](./README.md#adding-a-new-agent).

| Agent | Transport | Verified on | Known quirks |
|-------|-----------|-------------|--------------|
| LangChain (no MCP) | Python `requests` / JS `fetch` | 2026-06-17 | Map each tool to a `StructuredTool`; set HTTP timeout ≥130s |
| Coze (webhook / plugin HTTP) | HTTP POST + plugin schema | 2026-06-17 | Plugin manifest must mirror the 12 tool names; auth via `x-api-key` header (not `Authorization`) |

## Unverified members

> The agents below are believed to fit this family but no runnable snippet has been
> validated against a live config. To promote one, add a verified snippet in the
> "Agent-specific snippets" section and update the `Verified on` column.

| Agent | Transport | Suspected quirk |
|-------|-----------|-----------------|
| Grok (web agent / function-call) | HTTP POST + Bearer | Single-request model; no `job_id` polling (the synchronous contract) |
| Perplexity (Agent API) | HTTP POST + Bearer | Same; check rate-limit headers per request |

## Common setup (any member)

1. Discover the 12 tool list by reading [`../SKILL.md`](../SKILL.md) §3 — the
   `category/name` pair is the URL path (e.g. `fortune/bazi_basic_analysis`).
2. Each request is `POST https://fortunehub.lighttune.com.au/api/universal/<category>/<name>` with
   `Content-Type: application/json` and `Authorization: Bearer <api_key>` (or
   `x-api-key: <api_key>` — both are accepted; the snippets below use whichever
   the agent's transport prefers).
3. Response envelope is `{ success, data, credits_deducted }` on success,
   `{ success:false, error:{code,message,details?} }` on failure. (Live remaining
   free quota is **not** in the envelope — read it from m2 `get_user_credits`.)
4. **No `job_id` polling** — the synchronous contract says all 12 tools are synchronous. Set HTTP client
   timeout to **≥120s** to absorb t4 jitter.

## Agent-specific snippets

### LangChain (Python) — `StructuredTool` wrapping universal REST

```python
import os
import requests
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

HUB_BASE = os.environ["FORTUNE_HUB_BASE"]   # e.g. "https://fortunehub.lighttune.com.au"
API_KEY = os.environ["FORTUNE_HUB_API_KEY"]
TIMEOUT = (5, 130)  # (connect, read) — read must be >= 120s for t4

class BaziBasicInput(BaseModel):
    birth_year: int = Field(..., ge=1900, le=2100)
    birth_month: int = Field(..., ge=1, le=12)
    birth_day: int = Field(..., ge=1, le=31)
    birth_hour: int = Field(..., ge=0, le=23)
    birth_minute: int = Field(..., ge=0, le=59)
    gender: str = Field(..., pattern="^(male|female)$")
    location: dict = Field(..., description='{"city_name": "Beijing"}')

def _call_fortune(name: str, payload: dict) -> dict:
    r = requests.post(
        f"{HUB_BASE}/api/universal/fortune/{name}",
        json=payload,
        headers={"x-api-key": API_KEY, "content-type": "application/json"},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    body = r.json()
    if not body.get("success"):
        raise RuntimeError(f"{body['error']['code']}: {body['error']['message']}")
    return body["data"]

bazi_basic_analysis = StructuredTool.from_function(
    name="bazi_basic_analysis",
    description="Compute the four pillars, five-element distribution, and major-luck starting point.",
    func=lambda **kwargs: _call_fortune("bazi_basic_analysis", kwargs),
    args_schema=BaziBasicInput,
)
```

For the full 12-tool contract, error codes, and billing, see [`../SKILL.md`](../SKILL.md) §3–§5.

### Coze (webhook plugin) — manifest mirrors the 12 tool names

Coze plugin manifest (`plugin.yaml` or the equivalent UI export):

```yaml
name: fortune-hub
version: 0.3.0
auth:
  type: service
  service:
    # Coze's token proxy MUST inject this header. The `Authorization` header
    # is reserved for Coze's own platform auth and will be overwritten.
    header: x-api-key
    value: ${FORTUNE_HUB_API_KEY}
endpoints:
  - name: bazi_basic_analysis
    path: /api/universal/fortune/bazi_basic_analysis
    method: POST
  - name: bazi_pattern_analysis
    path: /api/universal/fortune/bazi_pattern_analysis
    method: POST
  - name: bigluck_year_analysis
    path: /api/universal/fortune/bigluck_year_analysis
    method: POST
  - name: bigluck_year_fortune_eval
    path: /api/universal/fortune/bigluck_year_fortune_eval
    method: POST
  - name: forum_list_posts
    path: /api/universal/forum/forum_list_posts
    method: POST
  - name: forum_get_post
    path: /api/universal/forum/forum_get_post
    method: POST
  - name: forum_create_post
    path: /api/universal/forum/forum_create_post
    method: POST
  - name: forum_create_comment
    path: /api/universal/forum/forum_create_comment
    method: POST
  - name: forum_like_post
    path: /api/universal/forum/forum_like_post
    method: POST
  - name: get_skill_info
    path: /api/universal/meta/get_skill_info
    method: POST
  - name: get_user_credits
    path: /api/universal/meta/get_user_credits
    method: POST
  - name: get_usage_history
    path: /api/universal/meta/get_usage_history
    method: POST
```

Per-tool request/response schemas, error codes, and billing are documented once in
[`../SKILL.md`](../SKILL.md) §3–§5; do not duplicate them in the Coze plugin UI.

## When NOT to use this family

- Agent supports MCP and can reach `/api/mcp` directly → [`mcp-native.md`](./mcp-native.md) (preferred)
- Agent supports both → [`mixed.md`](./mixed.md)

---

*Last verified: 2026-06-17. Verified on column reflects the date the runnable
snippet was last checked end-to-end. See [README.md](./README.md#adding-a-new-agent)
for the verified/unverified promotion policy.*
