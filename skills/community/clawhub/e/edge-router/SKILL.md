---
name: edge-router
description: Route AI agent compute tasks to the cheapest viable backend. Supports local inference (Ollama), cloud GPU (Vast.ai), and quantum hardware (Wukong 72Q). Use when an agent needs to decide where to run a task, optimize compute costs, check backend availability, or execute workloads across edge/cloud/quantum infrastructure.
---

# Edge Router

Routes tasks to cheapest available backend: local (free) → cloud GPU ($0.01) → quantum ($0.10).

## API

Base: `https://edge-router.gpupulse.dev/api/v1` (or localhost:3825)

### Route (recommend)
```bash
curl -X POST "$BASE/route" -H "Content-Type: application/json" \
  -d '{"task_type": "inference"}'
```

### Execute (route + run)
```bash
curl -X POST "$BASE/execute" -H "Content-Type: application/json" \
  -d '{"task_type": "inference", "payload": {"model": "llama3.2:1b", "prompt": "hello"}}'
```

### Task Types
- `inference` → local first, cloud fallback
- `training` → cloud GPU
- `quantum` → Wukong 72Q
- `auto` → cheapest available

### Other
- `GET /backends` — list + status
- `GET /stats` — routing statistics
- `GET /health` — health check
