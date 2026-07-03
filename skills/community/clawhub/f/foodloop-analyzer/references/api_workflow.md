# FoodLoop AI — Full API Workflow Reference

## Live Backend
`https://foodrecycler.onrender.com` — FastAPI backend, SQLite database

---

## 📸 Analyzing a Photo (from chat)

When the user sends a photo in chat, use the upload analysis endpoint.

### Step 1 — Save the photo

Images arrive as base64 data URLs or as file paths. Save to a temp file:

```python
import base64, sys, re

data = sys.stdin.read().strip()

# Strip markdown image syntax if wrapped
if data.startswith('```'):
    lines = data.split('\n')
    data = '\n'.join(lines[1:-1] if lines[-1] == '```' else lines[1:])

# Handle data URL (data:image/jpeg;base64,...) or raw base64
if data.startswith('data:'):
    header, data = data.split(',', 1)
    ext = 'jpg' if 'jpeg' in header.lower() or 'jpg' in header.lower() else 'png'
else:
    ext = 'jpg'

img_bytes = base64.b64decode(data + ('=' * (4 - len(data) % 4) % 4))
path = '/tmp/foodloop_photo.jpg'
with open(path, 'wb') as f:
    f.write(img_bytes)
print(path)
```

### Step 2 — Upload and analyze

```bash
curl -s -X POST "https://<backend>/api/analysis/upload" \
  -F "file=@/tmp/foodloop_photo.jpg" \
  -F "condition=segar"
```

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | binary | ✅ | Photo file (JPEG, PNG, WebP) |
| `user_id` | int | ❌ | User ID for tracking |
| `condition` | string | ❌ | Freshness: `segar` (fresh), `ragu` (uncertain), etc. |
| `clarification` | string | ❌ | Extra text context |

### Step 3 — Get results

The upload response returns the analysis directly. To re-fetch:
```bash
curl -s "https://<backend>/api/analysis/{analysis_id}"
```

Returns `AnalysisResponse` — same schema as text analysis (see below).

## All Endpoints (35 total)

### Health
| Method | Path | Summary |
|---|---|---|
| GET | `/api/health` | Health check — returns `{}` on 200 |

### Auth (`/api/auth/`)
| Method | Path | Summary | Request |
|---|---|---|---|
| POST | `/api/auth/demo` | Demo login (no password) | `{name, email, provider?, phone?, reminder_channel?}` |
| GET | `/api/auth/google/start` | Initiate Google OAuth | — |
| GET | `/api/auth/google/callback` | Google OAuth callback | `?code=` |

### Analysis (`/api/analysis/`)
| Method | Path | Summary | Request |
|---|---|---|---|
| POST | `/api/analysis/text` | Analyze text input | `TextAnalysisRequest` |
| POST | `/api/analysis/upload` | Analyze image upload | multipart: `{user_id?, condition?, clarification?, file}` |
| GET | `/api/analysis/{analysis_id}` | Get analysis by ID | path: `analysis_id` (int) |
| POST | `/api/analysis/{analysis_id}/clarify` | Clarify detected items | `{text}` |
| GET | `/api/analysis/history/user/{user_id}` | User's analysis history | path: `user_id` (int) |

### Recipes (`/api/recipes/`)
| Method | Path | Summary |
|---|---|---|
| GET | `/api/recipes` | List all recipes |
| GET | `/api/recipes/{recipe_key}` | Get specific recipe |
| POST | `/api/recipes/recommend/{analysis_id}` | Generate recommendations |
| GET | `/api/recipes/recommend/{analysis_id}` | Fetch recommendations |
| GET | `/api/recipes/recommendation/{recommendation_id}` | Get recommendation detail with full recipe |

### Cooking Sessions (`/api/recipes/sessions/`)
| Method | Path | Summary | Request |
|---|---|---|---|
| POST | `/{session_id}/sessions` | Start cooking session | `{user_id}` |
| GET | `/{session_id}` | Get session | — |
| POST | `/{session_id}/finish` | Finish session | `{current_step}` |
| POST | `/{session_id}/stop` | Stop/abandon session | `{problem_note, current_step}` |
| POST | `/{session_id}/progress` | Update step progress | `{current_step}` |
| GET | `/user/{user_id}` | User's session history | — |

### Notifications
| Method | Path | Summary |
|---|---|---|
| GET | `/api/notifications/preview` | Preview reminder messages (2 stages) |
| GET | `/api/notifications/preferences/{user_id}` | Get user preferences |
| POST | `/api/notifications/preferences` | Save preferences |
| POST | `/api/notifications/preferences/{user_id}/disable` | Disable reminders |
| POST | `/api/notifications/run-due` | Trigger due reminders (cron) |

### Dashboard
| Method | Path | Summary |
|---|---|---|
| GET | `/api/dashboard/summary` | Totals: analyses, recipes, completion rate |
| GET | `/api/dashboard/leftovers` | Most frequently detected leftover foods |
| GET | `/api/dashboard/recipes` | Most popular recipes |
| GET | `/api/dashboard/stop-reasons` | Why users stop cooking sessions |

### Feedback & Contact
| Method | Path | Summary | Request |
|---|---|---|---|
| POST | `/api/feedback/experience` | Save experience feedback | `{user_id, rating, context?}` |
| POST | `/api/contact/messages` | Submit contact message | `{user_id?, name, email, language?, topic, message}` |

### PDF
| Method | Path | Summary |
|---|---|---|
| POST | `/api/pdf/generate/{recommendation_id}` | Generate recipe PDF |
| GET | `/api/pdf/download/{recommendation_id}` | Download PDF |

### Bots
| Method | Path | Summary |
|---|---|---|
| POST | `/api/bots/telegram/webhook` | Telegram incoming webhook |
| POST | `/api/bots/telegram/set-webhook` | Set Telegram webhook URL |
| GET | `/api/bots/whatsapp/webhook` | WhatsApp webhook verification |
| POST | `/api/bots/whatsapp/webhook` | WhatsApp incoming messages |

### Admin
| Method | Path | Summary |
|---|---|---|
| GET | `/api/admin/summary` | Admin overview (totals, recent users, messages) |
| GET | `/api/config/status` | API configuration and status |

---

## Core Schemas

### TextAnalysisRequest
```json
{
  "user_id": 1,
  "text": "nasi sisa, telur, sayuran",
  "condition": "segar"
}
```

### AnalysisResponse
```json
{
  "id": 1,
  "input_type": "text",
  "condition": "segar",
  "source_text": "nasi sisa, telur, sayuran",
  "image_path": null,
  "safety_level": "eligible_with_freshness_check",
  "safety_notes": [],
  "items": [
    {
      "id": 1,
      "label": "cooked_rice",
      "display_name": "nasi sisa",
      "confidence": 0.98,
      "source": "openai_text",
      "is_safety_flag": false
    }
  ],
  "recommendations": [
    {
      "id": 1,
      "recipe_key": "kerupuk_nasi",
      "recipe_name": "Kerupuk Nasi",
      "score": 100,
      "reason": "Matched cooked_rice with Kerupuk Nasi...",
      "warnings": ["Inspect all leftovers first...", "Do not use cooked rice left at room temperature..."],
      "created_at": "2026-06-30T13:17:34.199369"
    }
  ],
  "created_at": "2026-06-30T13:17:33.698296"
}
```

### RecommendationDetailResponse
```json
{
  "id": 1,
  "analysis_id": 1,
  "recipe_key": "kerupuk_nasi",
  "recipe_name": "Kerupuk Nasi",
  "score": 100,
  "reason": "...",
  "warnings": ["..."],
  "detected_leftovers": ["cooked_rice"],
  "safety_level": "eligible_with_freshness_check",
  "safety_notes": ["..."],
  "recipe": {
    "recipe_key": "kerupuk_nasi",
    "name": "Kerupuk Nasi",
    "region": "Indonesia",
    "leftover_matches": ["cooked_rice"],
    "required_safety": [],
    "ingredients": ["..."],
    "steps": ["..."],
    "difficulty": "easy",
    "estimated_time": "30 min",
    "safety_notes": ["..."]
  }
}
```

### DashboardSummary
```json
{
  "total_analyses": 0,
  "total_food_ideas": 0,
  "top_leftover": null,
  "saved_recipe_count": 0,
  "recipes_started": 0,
  "recipes_finished": 0,
  "recipes_stopped": 0,
  "completion_rate": 0.0,
  "most_completed_recipe": null,
  "most_stopped_recipe": null,
  "reminder_reactivation_rate": 0.0
}
```

### NotificationReminderPreview
```json
[
  {
    "stage": 1,
    "subject": "Masih ada leftover yang bisa dicek?",
    "message": "Hai {name}, masih ada leftover yang bisa dicek hari ini? FoodLoop bisa bantu cari ide masakan yang aman."
  },
  {
    "stage": 2,
    "subject": "Ide cepat untuk leftover Anda",
    "message": "FoodLoop bisa bantu ubah leftover jadi resep sederhana. Ce..."
  }
]
```

---

## Live Test Examples

### Demo Auth
```bash
curl -s -X POST "https://foodrecycler.onrender.com/api/auth/demo" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","reminder_channel":"whatsapp"}'
```
→ Returns: `UserResponse` with user_id, name, email, provider

### Text Analysis
```bash
curl -s -X POST "https://foodrecycler.onrender.com/api/analysis/text" \
  -H "Content-Type: application/json" \
  -d '{"text":"nasi sisa, telur, sayuran","condition":"segar"}'
```
→ Returns: `AnalysisResponse` with detected items + 8 recipe recommendations

### Get Recommendations
```bash
curl -s "https://foodrecycler.onrender.com/api/recipes/recommend/1"
```
→ Returns: `RecommendationListResponse`

### Get Config Status
```bash
curl -s "https://foodrecycler.onrender.com/api/config/status"
```
→ Returns:
```json
{
  "database_url_type": "sqlite",
  "openai_configured": true,
  "text_analyzer_mode": "openai",
  "leftover_identifier_mode": "openai",
  "recipe_response_mode": "openai",
  "google_auth_configured": true,
  "missing_google_fields": []
}
```

---

## Architecture Summary

```
┌─────────────────────────────────────┐
│  Frontend (Next.js SPA, Vercel)     │
│  food-recycler.vercel.app           │
└──────────────┬──────────────────────┘
               │  HTTPS (no CORS key shown)
               ▼
┌─────────────────────────────────────┐
│  Backend (FastAPI, Render)          │
│  foodrecycler.onrender.com          │
│  ├── /api/analysis/*  (OpenAI)      │
│  ├── /api/recipes/*  (OpenAI)       │
│  ├── /api/auth/*     (JWT/Google)   │
│  ├── /api/dashboard/*               │
│  ├── /api/notifications/*           │
│  ├── /api/bots/telegram|whatsapp    │
│  └── /api/pdf/*                     │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │   SQLite (Render)   │
    │   - users           │
    │   - analyses        │
    │   - recipes         │
    │   - sessions        │
    │   - messages        │
    └─────────────────────┘
```
