---
name: gh-bridge
description: "Agent-to-Human (A2H) verification and escrow platform. Agents request physical-world tasks from humans, define verification criteria (GPS, photos, timestamps, signatures), and Bridge handles escrow, proof verification, and dispute resolution. Escrow-by-Invariants: payment released only when ALL formal criteria pass."
metadata: {"openclaw":{"emoji":"🌉","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic"]}]}}
---

# Bridge

Request human help for physical-world tasks. Bridge verifies the work was done before releasing payment.

## Start the server

```bash
uvicorn bridge.app:app --port 8015
```

## Create a task with verification criteria

```bash
curl -s -X POST http://localhost:8015/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Pick up package at 123 Main St, photograph it",
    "budget_usdc": "25.00",
    "verification_criteria": [
      {"type": "gps_proof", "description": "At pickup location", "params": {"latitude": 37.7749, "longitude": -122.4194, "radius_m": 100}},
      {"type": "photo_proof", "description": "Photo of package", "params": {"min_photos": 1}}
    ]
  }' | jq
```

Escrow is locked automatically. Fee is 5% of budget.

## Submit proof and verify

```bash
curl -s -X POST http://localhost:8015/v1/tasks/TASK_ID/verify \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": "worker-1",
    "proofs": [
      {"type": "gps_proof", "data": {"latitude": 37.7749, "longitude": -122.4194}},
      {"type": "photo_proof", "data": {"photo_hashes": ["sha256:abc123"]}}
    ]
  }' | jq
```

If ALL criteria pass → escrow released. If any fail → escrow held.

## Dispute a task

```bash
curl -s -X POST http://localhost:8015/v1/tasks/TASK_ID/dispute \
  -H "Content-Type: application/json" \
  -d '{"reason": "GPS proof appears faked"}' | jq
```

Freezes escrow. No verification possible while disputed.

## Other endpoints

```bash
curl -s http://localhost:8015/v1/tasks | jq                    # List all tasks
curl -s http://localhost:8015/v1/tasks?status=posted | jq      # Filter by status
curl -s http://localhost:8015/v1/platforms | jq                 # Available platforms
curl -s http://localhost:8015/v1/stats | jq                    # Platform statistics
```

## Verification types

| Type | What it proves | How |
|------|---------------|-----|
| `gps_proof` | Worker was at location | Haversine distance < radius |
| `photo_proof` | Photos submitted | Unique hash count >= min |
| `timestamp_proof` | Done within deadline | Elapsed hours < max |
| `signature_proof` | Cryptographic signature | Non-empty signature present |

## Escrow model

- **Locked** at task creation (budget held)
- **Released** only if ALL criteria pass
- **Frozen** on dispute
- **Refunded** if deadline expires with no proof
