---
name: ainative-api-discovery
description: Help agents discover and navigate AINative's 89+ API endpoints. Use when (1) Asking "what endpoints exist?", (2) Finding the right API for a task, (3) Looking up endpoint paths/methods, (4) Exploring API categories, (5) Getting code examples for specific endpoints. Closes #1516.
---

# AINative API Discovery

AINative exposes 89+ REST API endpoints at `https://api.ainative.studio`.

## Endpoint Categories

### Authentication & Users
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | Email/password login → JWT |
| `/api/v1/auth/register` | POST | Create account |
| `/api/v1/auth/refresh` | POST | Refresh JWT token |
| `/api/v1/auth/logout` | POST | Invalidate session |
| `/api/v1/users/me` | GET | Get current user profile |

### Chat & AI Completions
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/public/chat/completions` | POST | Chat completion (streaming + non-streaming) |
| `/api/v1/public/managed-chat` | POST | Managed chat with session tracking |
| `/api/v1/public/models` | GET | List available AI models |

### Memory (ZeroMemory)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/public/memory/v2/remember` | POST | Store a memory |
| `/api/v1/public/memory/v2/recall` | POST | Semantic search memories |
| `/api/v1/public/memory/v2/forget` | DELETE | Remove memories |
| `/api/v1/public/memory/v2/reflect` | GET | Get memory insights |
| `/api/v1/public/memory/v2/profile` | GET | Build user profile from memories |
| `/api/v1/public/memory/v2/graph` | GET | Memory knowledge graph |

### Credits & Billing
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/public/credits/balance` | GET | Get current credit balance |
| `/api/v1/public/credits/usage` | GET | Credit usage history |
| `/api/v1/billing/subscribe` | POST | Subscribe to a plan |
| `/api/v1/billing/invoices` | GET | List invoices |

### Developer Program (Echo)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/echo/register` | POST | Register as a developer |
| `/api/v1/echo/earnings` | GET | Get earnings summary |
| `/api/v1/echo/payouts` | GET | List payouts |
| `/api/v1/echo/markup` | PUT | Set your markup rate (0-40%) |

### ZeroDB (Vector/NoSQL/Storage)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/public/zerodb/vectors/upsert` | POST | Upsert vector embedding |
| `/api/v1/public/zerodb/vectors/search` | POST | Semantic vector search |
| `/api/v1/public/zerodb/tables` | GET/POST | List/create NoSQL tables |
| `/api/v1/public/zerodb/files/upload` | POST | Upload file |

### Admin & Monitoring
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/users` | GET | List all users (superuser) |
| `/admin/monitoring` | GET | System health metrics |
| `/admin/database` | GET | Database pool status |
| `/health` | GET | Health check (no auth) |

## Authentication

All public endpoints require an API key:
```bash
# Header format
X-API-Key: ak_your_key_here

# Or Bearer token (for user sessions)
Authorization: Bearer eyJ...
```

## Code Examples

### Python
```python
import requests

API_KEY = "ak_your_key"
BASE = "https://api.ainative.studio"

# Chat completion
resp = requests.post(f"{BASE}/v1/public/chat/completions",
    headers={"X-API-Key": API_KEY},
    json={"model": "claude-3-5-sonnet-20241022",
          "messages": [{"role": "user", "content": "Hello"}]}
)
print(resp.json()["choices"][0]["message"]["content"])

# Credit balance
balance = requests.get(f"{BASE}/api/v1/public/credits/balance",
    headers={"X-API-Key": API_KEY}).json()
print(f"Credits: {balance['remaining_credits']}")
```

### JavaScript/TypeScript
```typescript
const API_KEY = "ak_your_key";
const BASE = "https://api.ainative.studio";

const resp = await fetch(`${BASE}/v1/public/chat/completions`, {
  method: "POST",
  headers: { "X-API-Key": API_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({
    model: "claude-3-5-sonnet-20241022",
    messages: [{ role: "user", content: "Hello" }]
  })
});
const data = await resp.json();
```

### curl
```bash
curl -X POST https://api.ainative.studio/v1/public/chat/completions \
  -H "X-API-Key: ak_your_key" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","messages":[{"role":"user","content":"Hello"}]}'
```

## References

- `docs/api/API_REFERENCE.md` — Complete endpoint documentation
- `docs/api/API_ENDPOINTS_REFERENCE.md` — Full endpoint index
- `src/backend/app/api/v1/endpoints/` — Implementation source
