# 表情包 FTS5 SQLite 数据库

## 位置

```
${MEME_HOME:-auto}/meme-packs/<pack-id>/index.db
```

也可用 `MEME_PACK` 直接指向包根。未设 `MEME_HOME` 时：若存在 `~/.hermes/meme-packs` 则沿用，否则 `~/.agent-expression`。兼容 `HERMES_HOME` / `HERMES_MEME_PACK*`。

默认 `pack-id=official-001`。

## 表结构

### `memes`

| 列 | 类型 | 说明 |
|---|---|---|
| `path` | TEXT PK | 绝对路径 |
| `tag` | TEXT NOT NULL | 分类 |
| `file_name` | TEXT NOT NULL | 文件名 |
| `file_hash` | TEXT | SHA1（去重） |
| `caption` | TEXT | 视觉描述 |
| `keywords` | TEXT | 空格分隔关键词 |
| `mtime` | REAL | 文件 mtime |
| `captioned_at` | REAL | 打 caption 时间 |

### `memes_fts`（FTS5）

索引：`tag`、`caption`、`keywords`、`file_name`（`path` UNINDEXED）。

## CLI

```bash
python3 scripts/search-meme.py "无语" --pick -v
python3 scripts/search-meme.py --stats
```

实现见 `scripts/meme_db.py`。
