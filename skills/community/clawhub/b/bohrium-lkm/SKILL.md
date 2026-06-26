---
name: bohrium-lkm
description: "Large Knowledge Model (LKM) via open.bohrium.com. Use when: user asks about searching scientific knowledge graphs, verifying claims with evidence, querying variable relationships, or batch OCR of papers. NOT for: general paper search (use bohrium-paper-search), knowledge base management (use bohrium-knowledge-base)."
---

# SKILL: Bohrium LKM (Large Knowledge Model)

## Overview

LKM endpoints on `open.bohrium.com` provide scientific knowledge graph search, claim verification with evidence chains, variable relationship queries, and batch paper OCR.

**Core capabilities:**

| Endpoint | Function |
|----------|----------|
| `/v1/lkm/search` | Knowledge graph semantic search |
| `/v1/lkm/claims/match` | Claim matching: find evidence supporting/refuting a scientific claim |
| `/v1/lkm/claims/:id/evidence` | Get detailed evidence chain for a specific claim |
| `/v1/lkm/variables/batch` | Batch query variable relationships (e.g., temperature vs. catalytic activity) |
| `/v1/lkm/papers/ocr/batch` | Batch paper OCR (extract structured content) |

**Use when:**

- Verifying whether a scientific conclusion has literature support
- Querying relationships between two variables (positive/negative/none)
- Searching knowledge nodes in a specific domain
- Batch OCR of papers for structured data extraction

**Don't use for:**

- General paper keyword search → `bohrium-paper-search`
- Knowledge base file management → `bohrium-knowledge-base`
- Single PDF parsing → `bohrium-pdf-parser`

**No CLI support** — HTTP API only.

## Auth configuration

```json
"bohrium-lkm": {
  "enabled": true,
  "apiKey": "YOUR_ACCESS_KEY",
  "env": {
    "ACCESS_KEY": "YOUR_ACCESS_KEY"
  }
}
```

## Common template

```python
import os, requests

AK = os.environ["ACCESS_KEY"]
BASE = "https://open.bohrium.com/openapi/v1/lkm"
H = {"accessKey": AK, "Content-Type": "application/json"}
```

---

## 1. Knowledge graph search — `/lkm/search`

```python
r = requests.post(f"{BASE}/search", headers=H, json={
    "query": "effect of temperature on lithium ion battery degradation",
    "limit": 10
})
data = r.json()
print(data)
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | yes | Natural language search query |
| `limit` | int | no | Max results |

---

## 2. Claim matching — `/lkm/claims/match`

Submit a scientific claim, get back evidence that supports or refutes it (with source papers and relevance scores).

```python
r = requests.post(f"{BASE}/claims/match", headers=H, json={
    "text": "Graphene oxide improves the mechanical strength of concrete",
    "limit": 5
})
data = r.json()
# data["data"]["variables"] contains matched claims
# data["data"]["papers"] contains related paper details
# data["data"]["new_claim_likely"] indicates if this might be a novel claim
for item in data.get("data", {}).get("variables", []):
    print(f"  Claim ID: {item['id']}")
    print(f"  Role: {item.get('role')}")  # premise / conclusion
    print(f"  Score: {item.get('score')}")
    print(f"  Content: {item.get('content')[:100]}...")
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | Scientific claim to verify |
| `limit` | int | no | Max matching results |

**Response fields:**

| Field | Description |
|-------|-------------|
| `data.new_claim_likely` | Whether this might be a novel claim (insufficient support/refutation) |
| `data.variables[]` | List of matched existing claims |
| `data.variables[].id` | Claim ID (use for evidence chain lookup) |
| `data.variables[].content` | Claim content (with data and references) |
| `data.variables[].role` | `premise` or `conclusion` |
| `data.variables[].score` | Relevance score |
| `data.variables[].provenance` | Source info (paper ID, version) |
| `data.papers` | Related paper details map (keyed by paper ID) |

---

## 3. Evidence chain — `/lkm/claims/:id/evidence`

Get detailed evidence for a specific claim ID (source papers, experimental data, reasoning paths).

```python
claim_id = "abc123"
r = requests.get(f"{BASE}/claims/{claim_id}/evidence", headers=H)
data = r.json()
for ev in data.get("data", []):
    print(f"  Paper: {ev.get('paper_title')}")
    print(f"  Evidence: {ev.get('text')}")
    print(f"  Type: {ev.get('evidence_type')}")
```

---

## 4. Variable batch query — `/lkm/variables/batch`

Batch query variable details by ID. Variable IDs can be obtained from `/lkm/search` or `/lkm/claims/match` responses.

```python
r = requests.post(f"{BASE}/variables/batch", headers=H, json={
    "ids": ["gcn_b2bf079b541a4fa0", "gcn_5cecd02c3d8a4e61"]
})
data = r.json()
for var in data.get("data", {}).get("variables", []):
    print(f"  ID: {var['id']}")
    print(f"  Content: {var.get('content')[:100]}...")
# data["data"]["not_found"] lists IDs that were not found
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ids` | string[] | yes | Variable/claim IDs (obtained from other LKM endpoints) |

---

## 5. Batch paper OCR — `/lkm/papers/ocr/batch`

Batch OCR extraction from papers.

```python
r = requests.post(f"{BASE}/papers/ocr/batch", headers=H, json={
    "paper_ids": ["doi:10.1038/s41586-021-03819-2", "doi:10.1126/science.abf3041"]
})
data = r.json()
for paper in data.get("data", []):
    print(f"  Paper: {paper.get('title')}")
    print(f"  Status: {paper.get('status')}")
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `paper_ids` | string[] | yes | Paper identifiers (DOI or internal ID) |

---

## curl examples

```bash
AK="YOUR_ACCESS_KEY"

# Knowledge graph search
curl -s -X POST "https://open.bohrium.com/openapi/v1/lkm/search" \
  -H "accessKey: $AK" -H "Content-Type: application/json" \
  -d '{"query":"lithium battery degradation mechanism","limit":10}' | jq .

# Claim matching
curl -s -X POST "https://open.bohrium.com/openapi/v1/lkm/claims/match" \
  -H "accessKey: $AK" -H "Content-Type: application/json" \
  -d '{"text":"MoS2 is a promising catalyst for hydrogen evolution","limit":5}' | jq .

# Evidence chain
curl -s -X GET "https://open.bohrium.com/openapi/v1/lkm/claims/abc123/evidence" \
  -H "accessKey: $AK" | jq .

# Variable batch query (IDs from search/claims results)
curl -s -X POST "https://open.bohrium.com/openapi/v1/lkm/variables/batch" \
  -H "accessKey: $AK" -H "Content-Type: application/json" \
  -d '{"ids":["gcn_b2bf079b541a4fa0","gcn_5cecd02c3d8a4e61"]}' | jq .

# Batch OCR
curl -s -X POST "https://open.bohrium.com/openapi/v1/lkm/papers/ocr/batch" \
  -H "accessKey: $AK" -H "Content-Type: application/json" \
  -d '{"paper_ids":["doi:10.1038/s41586-021-03819-2"]}' | jq .
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| claims/match returns nothing | Claim too vague | Use specific scientific phrasing with variables and relationships |
| variables/batch timeout | Too many pairs | Submit in batches of 10 or fewer |
| OCR status pending | Backend processing | Poll for results or wait for callback |

## Pairs well with

- **lkm** verify claim → **paper-search** to find original full paper
- **lkm** query variable relationships → **mol-search** for related molecular structures
- **lkm** batch OCR → **knowledge-base** to store extracted results
