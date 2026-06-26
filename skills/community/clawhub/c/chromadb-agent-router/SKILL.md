---
name: semantic-router
description: Local semantic message routing for multi-agent systems. Routes messages to the correct agent based on embeddings + keyword + context scoring. No external APIs, no cloud dependencies, works on ARM64. 100% accuracy on benchmark with domain-augmented embeddings and action verb stratification.
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      python: ["chromadb", "numpy"]
    install:
      - id: python-deps
        kind: pip
        packages: ["chromadb", "numpy"]
        label: Install Python dependencies
---

# Semantic Router — Local Agent Message Routing

Route messages to the correct agent in a multi-agent system using a 3-layer scoring architecture:
1. **Embedding similarity** (ChromaDB) — semantic understanding
2. **Keyword scoring** — exact domain matches
3. **Action verb stratification** — "deploy" always → ops, "secure" → security

## Why This Exists

Most agent routers either:
- Call external APIs (latency, cost, privacy)
- Use simple keyword matching (inaccurate)
- Don't understand French/English bilingual queries

This router runs **entirely locally** in ~1.5ms per query with 100% accuracy.

## Quick Start

### 1. Define Your Routes

Create a routes configuration file (JSON or Python dict):

```python
ROUTES = {
    "ops": {
        "agent": "orion",
        "descriptions": [
            "Deploy and manage infrastructure and Docker containers",
            "Install, configure, and restart services",
            "DevOps operations, CI/CD, deployment pipelines",
        ],
        "keywords": ["deploy", "install", "docker", "compose", "container", "restart"],
        "action_verbs": ["déploie", "installe", "configure", "redémarre"],
    },
    "security": {
        "agent": "aegis",
        "descriptions": [
            "Security audits, vulnerability scanning, hardening",
            "Firewall rules, SSL certificates, access control",
        ],
        "keywords": ["security", "firewall", "ssl", "vulnerability"],
        "action_verbs": ["sécurise", "hardened"],
    },
    # ... add more routes
}
```

### 2. Initialize and Route

```python
from semantic_router import SemanticRouter

router = SemanticRouter(routes_config="routes.json")
router.initialize()  # Builds ChromaDB index (~6s cold start, then cached)

result = router.route("Deploy the new monitoring stack on the homelab")
# → {"route": "ops", "agent": "orion", "confidence": 0.94}
```

### 3. Use in OpenClaw

```bash
# Start the API server
python3 scripts/router-api.py --port 8321

# Route a message
curl -X POST http://localhost:8321/route \
  -H "Content-Type: application/json" \
  -d '{"message": "Check the firewall logs for suspicious activity"}'
```

## Architecture

```
Input Message
    │
    ├─► French Normalization (accent handling, verb mapping)
    │
    ├─► Layer 1: Embedding Similarity (ChromaDB)
    │   └─ cosine similarity against route descriptions
    │
    ├─► Layer 2: Keyword Scoring
    │   └─ exact/substring match with keyword-stealing avoidance
    │
    ├─► Layer 3: Action Verb Stratification
    │   └─ ops verbs → always override topic
    │   └─ topic verbs → override but route-specific
    │   └─ weak verbs → let embeddings decide
    │
    └─► Weighted Fusion → Route Selection
```

### Scoring Formula

```
final_score = (0.4 × centroid_sim) + (0.3 × max_example_sim) + (0.3 × keyword_score) + action_boost
```

Where `action_boost` is additive for matched action verbs, allowing override of embedding scores.

## Key Design Decisions

1. **No external API** — Everything runs locally via ChromaDB + default embeddings
2. **Keyword stealing prevention** — A keyword appears in exactly ONE route
3. **French normalization before action detection** — Normalize accents but detect verbs on original text
4. **Cache to disk** — Embeddings persist in `/tmp/semantic_router_cache/`
5. **Action verb stratification** — The breakthrough from 92.7% to 100%

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/route` | POST | Route a single message |
| `/batch` | POST | Route multiple messages |
| `/benchmark` | POST | Run accuracy benchmark |
| `/stats` | GET | Usage statistics |
| `/routes` | GET | List configured routes |
| `/health` | GET | Health check |

## Performance

| Metric | Value |
|--------|-------|
| Accuracy (benchmark) | 100% (41/41 messages) |
| Query latency | ~1.5ms (cached) |
| Cold start | ~6s (embed routes) |
| Memory | ~50MB |
| ARM64 compatible | ✅ (tested on Raspberry Pi 5) |

## Use Cases

- **Multi-agent orchestration** — Route user messages to specialized agents
- **Message bus routing** — Front-load balancer for agent mesh networks
- **Intent classification** — Classify support tickets, requests, commands
- **Bilingual routing** — French/English queries handled natively

## Files

```
semantic-router/
├── SKILL.md              ← This file
├── scripts/
│   ├── semantic_router.py    ← Core router library
│   └── router-api.py         ← REST API wrapper
└── references/
    └── ROUTING-RESEARCH.md   ← Design notes and benchmarks
```

## License

MIT — Use freely, attribution appreciated.
