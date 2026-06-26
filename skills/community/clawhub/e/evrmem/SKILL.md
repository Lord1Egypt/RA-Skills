# evrmem Skill

## Name

`evrmem`

## Description

Local Chinese Vector Memory System. Provides semantic memory search and storage for AI agents using local Chinese embedding models (text2vec) and ChromaDB. Supports RAG-based context augmentation.

## When to Use

Use this skill when the user asks to:
- "Search memories" or "Find related memories"
- "Save this to memory"
- "Remember this information"
- "Search my knowledge base"
- "Find past notes about X"
- "Add this to my memory"
- "What do I know about X"
- "RAG retrieval" or "context augmentation"
- Query or recall previous learnings

## Prerequisites

Install evrmem and initialize:

```bash
pip install evrmem
evrmem init
```

For China users (mirror):

```bash
set HF_ENDPOINT=https://hf-mirror.com   # Windows
# or
export HF_ENDPOINT=https://hf-mirror.com   # Linux/Mac
evrmem init
```

## Core Workflow

### 1. Semantic Search (Most Common)

```python
from qmd.core.vector_db import vector_db

results = vector_db.search("React form warning", top_k=5)
for r in results:
    print(f"[{r['distance']:.3f}] {r['content'][:80]}")
```

Or via CLI:

```bash
evrmem search "React form warning"
evrmem search "deployment issue" --project myproject
```

### 2. Add Memory

```python
memory_id = vector_db.add_memory(
    "React StrictMode causes Form.useForm warning",
    metadata={"project": "mes-demo", "tags": "react,antd"}
)
```

Or via CLI:

```bash
evrmem add "Important finding about X" --project myproject --tags react,bug
```

### 3. Structured Query

```bash
# Query by project
evrmem query --project mes-demo

# Query by tag
evrmem query --tag react

# List all projects
evrmem query --list-projects

# List all tags
evrmem query --list-tags
```

### 4. RAG Retrieval

```python
result = vector_db.rag("how to fix the form warning", top_k=3)
print(result["context"])
```

Or via CLI:

```bash
evrmem rag "how to fix the form warning"
evrmem rag "how to fix the form warning" --prompt
```

### 5. Statistics

```bash
evrmem stats
```

## Configuration

Create `~/.evrmem/config.yaml`:

```yaml
vector_db:
  persist_directory: "~/.evrmem/data/qmd_memory"

embedding:
  model_name: "shibing624/text2vec-base-chinese"
  device: "cpu"  # or "cuda"
  cache_folder: "~/.evrmem/models"

rag:
  top_k: 5
  min_similarity: 0.5

logging:
  level: "WARNING"
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EVREM_DATA_DIR` | Data directory | `~/.evrmem/data/qmd_memory` |
| `EVREM_MODEL_NAME` | HuggingFace model name | `shibing624/text2vec-base-chinese` |
| `EVREM_LOCAL_MODEL` | Local model path (highest priority) | - |
| `EVREM_DEVICE` | Device for inference | `cpu` |
| `EVREM_TOP_K` | Default retrieval count | `5` |
| `EVREM_MIN_SIM` | Minimum similarity threshold | `0.5` |
| `EVREM_LOG_LEVEL` | Logging level | `WARNING` |
| `EVREM_LOCAL_FILES_ONLY` | Disable network access | `false` |
| `HF_ENDPOINT` | HuggingFace mirror endpoint | - |

## Response Format

When reporting search results, use this format:

```
## evrmem Search Results

**Query:** "user query"
**Results:** N memories found

| Score | Project | Content |
|-------|---------|---------|
| 0.723 | mes-demo | React StrictMode causes Form.useForm warning... |
| 0.681 | docs | Deployment script timeout issue... |

### Top Match
**Project:** mes-demo | **Tags:** react,antd

> React StrictMode causes Form.useForm warning...
```

When adding memory:

```
## Memory Saved

**ID:** abc123
**Project:** mes-demo
**Tags:** react
**Content:** React StrictMode causes Form.useForm warning...

Use `evrmem search "React StrictMode"` to retrieve later.
```

## Installation for Agent

If `evrmem` is not installed:

```python
import subprocess
subprocess.run(["pip", "install", "evrmem"], check=True)
# Initialize on first use (downloads ~400MB model)
subprocess.run(["evrmem", "init"], check=True)
```

For China users, set mirror before init:

```python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
subprocess.run(["evrmem", "init"], check=True)
```

## Edge Cases

- **Model download fails**: Set `HF_ENDPOINT=https://hf-mirror.com` before `evrmem init`
- **NumPy errors**: Run `pip install "numpy<2" --force-reinstall`
- **Offline/air-gapped**: Download model on connected machine, copy `~/.evrmem/models` to offline machine, set `EVREM_LOCAL_FILES_ONLY=true`
- **Empty search results**: Try broader terms or check if memories exist with `evrmem query --list-projects`
- **Similarity too low**: Adjust `--top-k` or lower `EVREM_MIN_SIM` threshold
- **Slow search**: Use CPU by default; set `EVREM_DEVICE=cuda` if GPU available
