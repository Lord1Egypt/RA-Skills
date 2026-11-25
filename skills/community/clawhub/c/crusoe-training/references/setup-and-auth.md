# Setup and Authentication

Shared by every sub-skill of `crusoe-training`.

## API key

- Created in the Crusoe Cloud Console → **Admin** → **Security** →
  **Intelligence API keys** → **Create**. One key authenticates all three
  APIs below.
- The user exports it themselves; never require it in chat:

```bash
export API_TOKEN='<your Intelligence API key>'
```

## The three hosts

| Purpose | Base URL | Auth |
|---|---|---|
| Fine-tuning, files, models (OpenAI-compatible) | `https://api.intelligence.crusoecloud.com/v1` | `Authorization: Bearer $API_TOKEN` |
| Inference (deployed models; OpenAI-compatible) | `https://api.inference.crusoecloud.com/v1` | same |
| Deployment management (Crusoe Cloud API) | `https://api.crusoecloud.com/v1/projects/{project_id}/foundry/selfserve/` | same |

Note the inference host differs from the fine-tuning host. For the OpenAI
Python client, `base_url` is the host root **without** `/chat/completions` —
the client appends the path itself.

## Python client

```python
from openai import OpenAI
import httpx, os

client = OpenAI(
    api_key=os.environ["API_TOKEN"],
    base_url="https://api.intelligence.crusoecloud.com/v1",
    http_client=httpx.Client(proxy=None, trust_env=False),
)
```

`trust_env=False` disables proxy discovery from environment variables, which
the docs prescribe. Requires `pip install openai httpx`.

For inference against a deployment, build a second client with
`base_url="https://api.inference.crusoecloud.com/v1"`.

## curl

```bash
# Fine-tuning / files
curl "https://api.intelligence.crusoecloud.com/v1/fine_tuning/jobs" \
  -H "Authorization: Bearer $API_TOKEN" -H "Accept: application/json"

# Inference
curl "https://api.inference.crusoecloud.com/v1/chat/completions" \
  -H "Authorization: Bearer $API_TOKEN" -H "Content-Type: application/json" \
  -d '{"model": "<deployment alias>", "messages": [...]}'
```

## Project ID

Deployment-management URLs embed a `{project_id}` path segment. Get it from
the Console URL while viewing the project
(`console.crusoecloud.com/.../projects/<project_id>/...`) — ask the user for
it; it is not exposed by the fine-tuning API.

## Hugging Face credentials (private adapter repos)

To deploy a private Hugging Face adapter, a credential must first be stored in
the project:

```
POST /v1/projects/{project_id}/foundry/credentials   # {name, description, credentials: {token}}
GET  /v1/projects/{project_id}/foundry/credentials   # list, to find credential_id
```

(Prefix: `https://api.crusoecloud.com`.) Public HF repos need no credential.

## First-call sanity check

Before any billable call, verify auth and list available base models:

```python
import httpx, os

resp = httpx.get(
    "https://api.intelligence.crusoecloud.com/v1/public/models",
    headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"},
)
print([m["id"] for m in resp.json()["data"]])
```

A 401 here means the key is wrong, expired, or from the wrong console region —
stop and fix before continuing.
