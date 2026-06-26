# 数据库 Schema

## chunks 表

| 字段 | 类型 | 说明 |
|------|------|------|
| rowid | INTEGER | 自增主键 |
| session_key | TEXT | session 标识，如 `agent:main:session:xxx` |
| turn_id | TEXT | 时间戳_role_seq，用于排序 |
| role | TEXT | `user` 或 `assistant` |
| content | TEXT | 消息纯文本内容 |
| created_at | INTEGER | 毫秒级时间戳 |
| content_hash | TEXT | MD5(content)，用于去重 |

## 索引

```sql
CREATE INDEX idx_session ON chunks(session_key);
CREATE INDEX idx_created ON chunks(created_at);
```

## FTS5 表（Python 3.9+）

```sql
CREATE VIRTUAL TABLE chunks_fts USING fts5(
    content,
    content_rowid=rowid,
    content=chunks
);
```

配合三个 trigger 实现自动同步：
- `chunks_ai`：INSERT 后同步
- `chunks_ad`：DELETE 后同步
- `chunks_au`：UPDATE 后同步

## 去重机制

`content_hash` 字段存储 `MD5(content)`，UNIQUE 约束确保同一内容不会被重复写入。
