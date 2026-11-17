# 向量嵌入表 `meme_embeddings`

用于 caption 语义检索（智谱 `embedding-3`，默认 2048 维）。

## Schema

```sql
CREATE TABLE meme_embeddings (
  path TEXT PRIMARY KEY,
  model TEXT NOT NULL,
  dim INTEGER NOT NULL,
  vector BLOB NOT NULL,   -- float32 little-endian
  text_hash TEXT,         -- sha1(caption+keywords+tag)
  embedded_at REAL
);
```

## 维护

```bash
export ZHIPU_API_KEY=...
python3 scripts/embed-memes.py
python3 scripts/embed-memes.py --stats
```

检索时若已有向量，`search-meme.py` / `search_meme` 优先余弦相似，否则回退 FTS。

实现见 `scripts/meme_embed.py`。
