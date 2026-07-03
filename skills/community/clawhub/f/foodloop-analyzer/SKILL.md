---
name: foodloop-analyzer
description: >
  Reverse-engineer and analyze any FoodLoop AI deployment. Use when given a
  FoodLoop AI URL and asked to analyze, audit, trace, map, or inspect its
  workflow, API, or architecture.
---

# FoodLoop AI — Analyzer Skill

Reverse-engineers a FoodLoop AI deployment: maps routes, traces API endpoints, identifies the backend, and reconstructs the full user workflow.

## Workflow

### Step 1 — Identify Backend URL

Fetch the frontend's JS bundle and look for the backend host string:
```bash
curl -s "https://<frontend>/assets/$(curl -s 'https://<frontend>/' | grep -oP 'src="/assets/\K[^"]+')" | tr '"' '\n' | grep -E "https?://[^/]+\.(onrender|railway|vercel|render)" | sort -u
```

Or grep the JS for `api/` route strings directly:
```bash
curl -s "https://<frontend>/assets/<bundle>.js" | tr '"' '\n' | grep -E "^/api/" | sort -u
```

### Step 2 — Fetch OpenAPI Spec

Most FastAPI backends expose their spec at:
```
https://<backend>/openapi.json
```
This is the canonical source of truth — pull it first and extract all paths + schemas:
```bash
curl -s "https://<backend>/openapi.json" | python3 -c "
import sys, json
spec = json.load(sys.stdin)
for path, methods in spec['paths'].items():
    for method, details in methods.items():
        print(f'{method.upper():6} {path} — {details.get(\"summary\",\"?\")}')
for name, schema in spec.get('components',{}).get('schemas',{}).items():
    print(f'Schema: {name}: {list(schema.get(\"properties\",{}).keys())}')
"
```

### Step 3 — Map Pages

Probe common Next.js routes:
```bash
for route in "" "home" "scan" "analyze" "result" "dashboard" "about" "how-it-works" "login" "signup"; do
  curl -s -o /dev/null -w "$route → HTTP %{http_code}\n" "https://<frontend>/$route"
done
```

### Step 4 — Trace the User Workflow

Use the OpenAPI spec as reference. The core workflow is:

1. **Input** → `POST /api/analysis/text` or `POST /api/analysis/upload`
2. **Detect** → AI identifies leftovers (label, display_name, confidence, safety_flag)
3. **Clarify (optional)** → `POST /api/analysis/{id}/clarify`
4. **Recommend** → `POST /api/recipes/recommend/{analysis_id}` → Indonesian recipe list
5. **Cook** → `POST /api/recipes/sessions/{id}/start` → guided session
6. **Track** → `POST /progress`, `POST /finish`, `POST /stop`
7. **Remind** → Notifications via `GET /api/notifications/preview`
8. **Analyze** → Dashboard at `/api/dashboard/summary`
9. **Export** → `POST /api/pdf/generate/{recommendation_id}`

### Step 5 — Test the API

Test demo auth:
```bash
curl -s -X POST "https://<backend>/api/auth/demo" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'
```

Test text analysis:
```bash
curl -s -X POST "https://<backend>/api/analysis/text" \
  -H "Content-Type: application/json" \
  -d '{"text":"nasi sisa, telur, sayuran","condition":"segar"}'
```

### Step 6 — Check Config

```bash
curl -s "https://<backend>/api/config/status"
```

### Step 7 — Document Findings

Save the complete analysis to:
`~/.openclaw/workspace/foodloop_<domain>_<date>.md`

Include: architecture table, all endpoints, workflow steps, test results, and schema summaries.

## Analyze a Photo (from chat)

When the user sends a photo directly in chat, analyze it using the upload endpoint:

**Step 1 — Save the photo to a temp file:**
```bash
# If image is a base64 data URL (most common from chat):
python3 -c "
import sys, base64, re
data = sys.stdin.read()
# Handle data URL or raw base64
if data.startswith('data:'):
    header, data = data.split(',', 1)
img_bytes = base64.b64decode(data)
ext = 'jpg'
if 'png' in header.lower(): ext = 'png'
path = '/tmp/foodloop_upload.jpg'
with open(path, 'wb') as f:
    f.write(img_bytes)
print(path)
" <<< "$(cat /path/to/image_data_or_data_url)"

# Or if the photo is already saved to a known path, use it directly
```

**Step 2 — Upload and analyze the photo:**
```bash
curl -s -X POST "https://<backend>/api/analysis/upload" \
  -F "file=@/tmp/foodloop_upload.jpg" \
  -F "condition=segar"
```

The `condition` field is optional. Common values: `segar` (fresh), `ragu` (uncertain).

**Step 3 — Parse and present the results:**
```bash
curl -s "https://<backend>/api/analysis/{analysis_id}"
```

**Output format** — same `AnalysisResponse` as text analysis:
- `items[]` — detected leftovers with label, display_name, confidence, safety_flag
- `safety_level` — overall safety assessment
- `warnings[]` — food safety notes
- `recommendations[]` — Indonesian recipe suggestions with score, reason, ingredients, steps

**Supported image formats:** JPEG, PNG, WebP (detected automatically by backend from Content-Type)

## Key Endpoints (FastAPI/FoodLoop AI Backend)

| Method | Path | Summary |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/auth/demo` | Demo login |
| GET | `/api/auth/google/start` | Google OAuth start |
| POST | `/api/analysis/text` | Text analysis |
| POST | `/api/analysis/upload` | **Image upload analysis** |
| GET | `/api/analysis/{analysis_id}` | Get analysis result |
| POST | `/api/analysis/{analysis_id}/clarify` | Clarify detected items |
| POST | `/api/recipes/recommend/{analysis_id}` | Get recipe recommendations |
| GET | `/api/recipes/recommendation/{id}` | Get recommendation detail |
| POST | `/api/recipes/sessions/{id}/sessions` | Start cooking session |
| POST | `/api/recipes/sessions/{id}/finish` | Finish cooking session |
| POST | `/api/recipes/sessions/{id}/stop` | Stop cooking session |
| POST | `/api/recipes/sessions/{id}/progress` | Update step progress |
| GET | `/api/dashboard/summary` | Dashboard metrics |
| GET | `/api/notifications/preview` | Preview reminder messages |
| POST | `/api/pdf/generate/{id}` | Generate recipe PDF |
| GET | `/api/admin/summary` | Admin summary |

## Backend Detection Pattern

FoodLoop AI backends expose a FastAPI doc UI at `/docs`. If `/openapi.json` returns a valid spec, confirm it contains `"FoodLoop AI"` in the `info.title` field.

## Reference

For the complete API schema, endpoint parameters, request/response schemas, and live test examples, see [references/api_workflow.md](references/api_workflow.md).
