# QMD Setup Guide

QMD (Query Model Database) is OpenClaw's built-in semantic search system using GPU-accelerated vector embeddings.

## How QMD Works

1. **Indexing**: Reads `MEMORY.md` and `memory/*.md` files
2. **Embeddings**: Converts text to vector representations (GPU-accelerated)
3. **Search**: Finds semantically similar content using cosine similarity

## Configuration

Add to `~/.openclaw/openclaw.json`:

```json
{
  "memory": {
    "qmd": {
      "enabled": true,
      "device": "cuda",
      "model": "sentence-transformers/all-MiniLM-L6-v2",
      "chunkSize": 512,
      "overlap": 50
    }
  }
}
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `enabled` | Enable QMD indexing | `true` |
| `device` | `cuda` or `cpu` | `cuda` |
| `model` | Sentence transformer model | `all-MiniLM-L6-v2` |
| `chunkSize` | Text chunk size for indexing | `512` |
| `overlap` | Chunk overlap for context | `50` |

## Requirements

### CUDA (Recommended)

```bash
# Check CUDA is available
nvidia-smi

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install sentence-transformers
pip install sentence-transformers
```

### CPU Fallback

If no GPU:
```json
{
  "memory": {
    "qmd": {
      "enabled": true,
      "device": "cpu"
    }
  }
}
```

Slower but works!

## Memory Search

Agents use QMD automatically via `memory_search`:

```python
# In your agent code, this happens automatically
results = memory_search(query="AgentBear project", maxResults=5)
```

Returns top-k semantically similar snippets with path and line numbers.

## How Tiered Memory Uses QMD

QMD handles **Tier 0** (hot memory):

```
memory/2026-03-14.md  →  QMD indexes  →  Semantic search
memory/2026-03-13.md  →  QMD indexes  →  Semantic search
```

Old files (14+ days) are archived to SQLite (Tier 1), removing them from QMD index.

This keeps QMD fast (smaller index) while preserving long-term memory in SQLite.

## Troubleshooting

### QMD Not Working

```bash
# Check OpenClaw health
openclaw doctor

# Restart gateway
openclaw gateway restart

# Check logs
openclaw logs memory
```

### High Memory Usage

- Reduce `chunkSize` (try 256)
- Enable archiving (moves old files out)
- Use CPU instead of CUDA

### Slow Search

- Ensure CUDA is enabled (`device: cuda`)
- Archive old files (reduces index size)
- Use smaller embedding model

## Models

Default: `sentence-transformers/all-MiniLM-L6-v2`
- Fast, good quality
- 384 dimensions

Alternatives:
- `sentence-transformers/all-mpnet-base-v2` - Better quality, slower
- `sentence-transformers/paraphrase-MiniLM-L3-v2` - Faster, smaller

## See Also

- Main skill: `SKILL.md`
- Archiver script: `scripts/memory_archiver.py`
- Tiered memory: `scripts/tiered_memory.py`
