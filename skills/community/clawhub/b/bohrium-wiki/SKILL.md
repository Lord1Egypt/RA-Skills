---
name: bohrium-wiki
description: "Browse and search Bohrium SciencePedia (encyclopedia) via open.bohrium.com. Use when: user asks about finding scientific topics, reading encyclopedia-style entries, browsing by major/level/field hierarchy, or looking up a specific concept's article. NOT for: paper search (use bohrium-paper-search), knowledge base management (use bohrium-knowledge-base)."
---

# SKILL: Bohrium SciencePedia

## Overview

Access **Bohrium SciencePedia** through the `/v1/literature-sage/wiki_v2/*` endpoints on `open.bohrium.com` — a hierarchical encyclopedia of scientific topics organized as `major` → `level` → `field` → `topic`.

**Use when**:

- Getting a quick definition of a scientific term (more focused than web-search — encyclopedia-style entries)
- Browsing by discipline (e.g., all subfields under materials science)
- Retrieving the full article of a topic (intro / applications / background sections)

**Don't use for**:

- Paper search → `bohrium-paper-search`
- Managing your own knowledge base → `bohrium-knowledge-base`

**No CLI support** — HTTP API only.

## Auth configuration

```json
"bohrium-wiki": {
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
BASE = "https://open.bohrium.com/openapi/v1/literature-sage/wiki_v2"
H = {"accessKey": AK, "Content-Type": "application/json"}

# Optional global defaults
DEFAULTS = {"language": "en-US", "style": "Feynman"}
# language: "en-US" / "zh-CN"
# style: "Feynman" for accessible tone, or others
```

---

## Actions overview

| Action | Method | Purpose |
|--------|--------|---------|
| `info` | GET | Basic SciencePedia info |
| `major_levels` | POST | List all majors and their levels |
| `get_wiki_index` | POST | Fetch index for a given nodeId / fieldId |
| `get_level_wiki_index` | POST | List nodes filtered by `node_types` |
| `search_index_name` | POST | Keyword search of index entries |
| `level_fields` | POST | List fields under a set of level nodes |
| `article` | POST | Fetch the article body of a node / entry |

---

## 1. Info — `info`

```python
r = requests.get(f"{BASE}/info", headers={"accessKey": AK})
print(r.json())
```

---

## 2. Majors & levels — `major_levels`

```python
r = requests.post(f"{BASE}/major_levels", headers=H, json={**DEFAULTS})
for m in r.json().get("majors", []):
    levels = ", ".join(l["name"] for l in m.get("levels", []))
    print(f"- {m['name']} [{m['node_id']}]  levels: {levels}")
```

---

## 3. Search entries — `search_index_name`

```python
r = requests.post(f"{BASE}/search_index_name", headers=H, json={
    "name": "graphene",
    "node_types": ["field"],   # Filter: major / level / field / topic
    "style": "Feynman",
})
for i, n in enumerate(r.json().get("wiki_indices", []), 1):
    print(f"[{i}] [{n['node_type']}] {n['node_name']}  id={n['node_id']}")
```

---

## 4. All nodes under a level — `get_level_wiki_index`

```python
r = requests.post(f"{BASE}/get_level_wiki_index", headers=H, json={
    "node_types": ["major", "level"],
    **DEFAULTS,
})
for n in r.json().get("wiki_indices", [])[:50]:
    print(f"[{n['node_type']}] {n['node_name']}  ({n['node_id']})")
```

---

## 5. Index for a given node — `get_wiki_index`

```python
r = requests.post(f"{BASE}/get_wiki_index", headers=H, json={
    "node_id": "NODE_ID_HERE",
    # or "field_id": "FIELD_ID_HERE"
    **DEFAULTS,
})
print(r.json())
```

---

## 6. Bulk list fields under level — `level_fields`

```python
r = requests.post(f"{BASE}/level_fields", headers=H, json={
    "node_ids": ["LEVEL_NODE_ID1", "LEVEL_NODE_ID2"],
    "page_num": 1, "page_size": 10,
    **DEFAULTS,
})
for row in r.json().get("items", []):
    major = row.get("major", {}).get("name")
    level = row.get("level", {}).get("name")
    field = row.get("field", {}).get("name")
    print(f"- {major}/{level}/{field}  topics={row.get('topic_count')}")
```

---

## 7. Article body — `article`

```python
r = requests.post(f"{BASE}/article", headers=H, json={
    "node_id": "NODE_ID",         # or "entry_id": "ENTRY_ID"
    **DEFAULTS,
})
doc = r.json().get("document", {})
print(f"# {doc.get('article_name')}")
print(doc.get("main_content", "")[:2000])
```

**Common fields**: `document.article_name` / `document.main_content` / `document.applications` / `document.seo_title`.

---

## curl example

```bash
AK="YOUR_ACCESS_KEY"
BASE="https://open.bohrium.com/openapi/v1/literature-sage/wiki_v2"

# Search entries by keyword
curl -s -X POST "$BASE/search_index_name" \
  -H "accessKey: $AK" -H "Content-Type: application/json" \
  -d '{"name":"graphene","node_types":["field"],"style":"Feynman"}' \
  | jq '.wiki_indices[] | {node_name, node_type, node_id}'
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No matches for "..."` | Keyword not in index | Try synonyms; expand `node_types` to `["field","topic","major","level"]` |
| Empty `article` | Wrong nodeId/entryId or no body | First call `search_index_name` to obtain the correct `node_id` |
| All-English (or all-Chinese) results | Wrong `language` | Set `"language": "en-US"` or `"zh-CN"` |

## Pairs well with

- **wiki** for a baseline explanation of a concept → **paper-search** to go deep
- **wiki** to browse the discipline tree (`major_levels`) → pick a field → **scholar** to find leading researchers
