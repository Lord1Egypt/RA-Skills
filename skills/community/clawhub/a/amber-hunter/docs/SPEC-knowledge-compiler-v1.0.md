# SPEC: Knowledge Compiler（知识编译器）v1.0

> 琥珀项目 · amber-hunter v1.2.38
> 基于 v1.2.17 insights 表的增量升级

---

## 1. 背景与目标

amber-hunter 已有 `insights` 表（v1.2.17）：将同 `category_path` 下的胶囊压缩成摘要，供 `/recall?use_insights=true` 优先返回。

**现状问题**：
- insight 输出是纯文本（100字），无 wikilinks，用户拿到摘要后无法点击跳转原始胶囊
- 只能手动触发 `/admin/generate-insights`，无自动编译
- 无"覆盖缺口"检测（哪些 topic 有胶囊但无 concept page）

**目标**：
1. insight 格式升级为带 `[[capsule_id:topic]]` wikilinks 的 markdown
2. 后台 daemon 自动触发编译（每 6 小时，或每新增 100 个胶囊）
3. 提供 `GET /concepts` 和 `GET /concepts/<path>` 端点，返回 wiki 格式 concept pages
4. 编译覆盖缺口检测：提示用户"dev/fastapi 有 5 条胶囊但无 concept page"

---

## 2. 数据模型

### 2.1 复用 `insights` 表（向后兼容）

`insights` 表新增两列（migration 无破坏）：

```sql
ALTER TABLE insights ADD COLUMN concept_slug TEXT;   -- e.g. "fastapi-best-practices"
ALTER TABLE insights ADD COLUMN wiki_content TEXT;   -- markdown + wikilinks
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | TEXT PK | insight ID |
| `capsule_ids` | TEXT (JSON) | 源胶囊 ID 数组 |
| `summary` | TEXT | 旧版纯文本摘要（兼容保留） |
| `path` | TEXT | category_path，如 `dev/python` |
| `concept_slug` | TEXT | 概念页 slug，如 `python-best-practices` |
| `wiki_content` | TEXT | 完整 markdown 内容（含 wikilinks） |
| `hotness_score` | REAL | |
| `created_at` | REAL | |
| `updated_at` | REAL | |

**向后兼容**：`summary` 列仍有值（取 wiki_content 的第一段），老 API 不受影响。

### 2.2 升级 `_generate_insight` prompt

**新 SYSTEM prompt**：
```
You are a memory analyst building a personal wiki for a second-brain system.
Given capsules from the same topic, generate a structured concept page in markdown.
Rules:
- Output valid markdown
- Each capsule reference: [[capsule_id:short_topic]]
- Include ## Key Insights, ## Decisions Made, ## Open Questions sections
- Keep total under 400 words
- First line is the H1 title: ## {topic_name}
```

**新 USER prompt**（模板变量：`{path}`、`{capsules_text}`）：
```
path: {path}

source capsules:
{capsules_text}

Generate a concept page for this topic. Include:
1. H1 title from path (e.g. ## Python Best Practices)
2. A brief overview paragraph
3. ## Key Insights section (bullet points)
4. ## Decisions & Conclusions section
5. ## Related Decisions (with [[capsule_id:topic]] wikilinks to each source capsule)
```

---

## 3. API 端点

### `GET /concepts`
返回所有 concept pages 列表（轻量）。

```json
{
  "concepts": [
    {
      "path": "dev/python",
      "concept_slug": "python-best-practices",
      "summary": "Python 开发的关键实践...",
      "capsule_count": 7,
      "hotness_score": 0.82,
      "updated_at": 1744560000.0
    }
  ],
  "total": 1
}
```

### `GET /concepts/<path>`
返回指定 path 的完整 concept page。

```json
{
  "path": "dev/python",
  "concept_slug": "python-best-practices",
  "wiki_content": "## Python Best Practices\n\n...\n\n## Related Decisions\n- [[abc123:use async FastAPI]]\n- [[def456:SQLAlchemy vs raw SQL]]",
  "capsule_ids": ["abc123", "def456", ...],
  "hotness_score": 0.82,
  "updated_at": 1744560000.0
}
```

### `POST /admin/compile`
手动触发指定 path 的编译（需认证）。

```
POST /admin/compile?path=dev/python
```

```json
{"compiled": true, "path": "dev/python", "concept_slug": "python-best-practices", "capsule_count": 7}
```

### `GET /admin/compile/status`
返回编译状态 + 覆盖缺口。

```json
{
  "last_compile_at": 1744560000.0,
  "compiled_paths": ["dev/python", "dev/fastapi"],
  "coverage_gaps": [
    {"path": "dev/docker", "capsule_count": 5, "reason": ">=3 capsules but no concept page"}
  ]
}
```

---

## 4. 后台编译 Daemon

**触发条件**（满足任一）：
- 每 6 小时周期性触发
- 每新增 100 个胶囊时触发（`_spawn_train_if_enabled` 风格）

**编译策略**：
- 每次编译最多处理 3 个 `category_path`
- 每个 path 取 top 20 个胶囊（按 hotness 排序）
- 跳过 7 天内已更新的 path
- 编译在独立线程中运行，不阻塞主请求

**覆盖缺口检测**：
```sql
SELECT category_path, COUNT(*) as cnt
FROM capsules
WHERE category_path != 'general/default'
GROUP BY category_path
HAVING cnt >= 3
-- NOT IN (SELECT path FROM insights WHERE wiki_content IS NOT NULL)
```

---

## 5. 部署与回滚

**涉及文件**：
- `amber_hunter.py` — 修改 `_generate_insight()`、新增 daemon、`/concepts/*` 端点
- `core/db.py` — 新增 migration 写 `concept_slug`/`wiki_content` 列
- `core/wiki_compiler.py`（新建）— 编译逻辑、daemon 线程管理

**版本号**：v1.2.37 → v1.2.38

**回滚**：删除 `concept_slug`/`wiki_content` 两列（SQLite `ALTER TABLE DROP COLUMN` 不支持，需重建表 — 但保留旧 `summary` 列仍可正常运作）

---

## 6. 验收标准

- [ ] `POST /admin/generate-insights` 生成的 insight 同时包含 `summary` 和 `wiki_content`
- [ ] `GET /concepts` 返回所有已有 concept page
- [ ] `GET /concepts/<path>` 返回带 wikilinks 的完整 markdown
- [ ] wikilinks 格式为 `[[capsule_id:topic]]`
- [ ] 后台 daemon 在启动 10 秒后自动编译一次（cold-start）
- [ ] 覆盖缺口通过 `GET /admin/compile/status` 返回
- [ ] `pytest tests/` 100% pass
- [ ] 版本号升至 v1.2.38
