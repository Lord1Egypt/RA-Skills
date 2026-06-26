# Candidates Review — P3 记忆候选审核机制

> Dreaming / auto-memory 产出的候选记忆不再直接写入，需人工确认后再归档。
> 最后更新：2026-05-17 | v1.13.1

---

## 一、背景与目的

传统流程中，Dreaming 和 auto-memory 自动将记忆写入 ARCHIVE.md/MEMORY.md，存在噪音污染风险。P3 机制引入人工审核层：

```
自动产出（Dreaming/auto-memory）
    ↓
memory/.candidates/YYYY-MM-DD.json（待审队列）
    ↓
用户确认（approve / reject）
    ↓
写入 ARCHIVE.md / MEMORY.md
```

**P3 含义**：Priority 3，第三优先级审核（低于 P1 即时生效、P2 自动归档）。

---

## 二、流程详解

### 2.1 候选来源

| 来源 | 说明 |
|------|------|
| **Dreaming** | 每日 UTC 03:00，扫描日志 → DeepSeek 分析 → 高分候选（minScore 0.8，max 10 items） |
| **auto-memory v3** | CST 18:30/22:30，MemOS Cloud → qwen3 过滤 → 候选条目 |
| **session-extract** | CST 22:00，JSONL 扫描 → MemOS extractor/reranker → 候选条目 |

### 2.2 候选文件格式

`memory/.candidates/YYYY-MM-DD.json`：
```json
{
  "pending": {
    "cand_001": {
      "date": "2026-05-17",
      "category": "偏好/习惯",
      "content": "用户偏好晚上工作，凌晨1点后效率最高",
      "source": "dreaming",
      "score": 0.92
    },
    "cand_002": {
      "date": "2026-05-17",
      "category": "技术/配置",
      "content": "升仕703F摩托车每8000km需要更换机油",
      "source": "auto-memory",
      "score": 0.87
    }
  },
  "approved": {},
  "rejected": {},
  "total_reviewed": 0
}
```

### 2.3 审核状态

| 状态 | 说明 |
|------|------|
| `pending` | 待审核，需用户确认 |
| `approved` | 已批准，写入 ARCHIVE.md |
| `rejected` | 已拒绝，不写入 |

---

## 三、审核命令

```bash
# 列出所有待审候选（按 score 倒序）
python3 scripts/candidates_review.py list

# 批准指定候选（写入 ARCHIVE.md）
python3 scripts/candidates_review.py approve --id cand_001

# 拒绝指定候选
python3 scripts/candidates_review.py reject --id cand_001

# 批准所有待审
python3 scripts/candidates_review.py approve-all

# 审核统计
python3 scripts/candidates_review.py stats
```

---

## 四、输出示例

### list 输出
```json
{
  "status": "ok",
  "pending_count": 2,
  "candidates": [
    {
      "id": "cand_001",
      "date": "2026-05-17",
      "category": "偏好/习惯",
      "content": "用户偏好晚上工作，凌晨1点后效率最高",
      "source": "dreaming",
      "score": 0.92
    },
    {
      "id": "cand_002",
      "date": "2026-05-17",
      "category": "技术/配置",
      "content": "升仕703F摩托车每8000km需要更换机油",
      "source": "auto-memory",
      "score": 0.87
    }
  ]
}
```

### approve 输出
```json
{
  "status": "approved",
  "id": "cand_001",
  "written_to": "/home/victor/.openclaw/workspace/ARCHIVE.md"
}
```

### stats 输出
```json
{
  "status": "ok",
  "pending": 2,
  "approved": 15,
  "rejected": 3,
  "total_reviewed": 18
}
```

---

## 五、approve-all 行为

`approve-all` 依次对每个 pending 候选执行 approve：
1. 读取当前 state
2. 写入 ARCHIVE.md（追加到末尾）
3. 从 pending 移到 approved
4. 重载 state（避免状态冲突）
5. 重复直到所有 pending 处理完毕

---

## 六、ARCHIVE.md 写入格式

批准后的条目写入 ARCHIVE.md 末尾，格式：
```markdown
<!-- candidate:cand_001 -->
- **偏好/习惯** (已审核 2026-05-17): 用户偏好晚上工作，凌晨1点后效率最高
```

---

## 七、与记忆架构的集成

```
Dreaming / auto-memory / session-extract
    ↓ 产出候选
memory/.candidates/YYYY-MM-DD.json
    ↓ 用户审核
ARCHIVE.md（完整条目）
    ↓
MEMORY.md（两阶段摘要）
    ↓
facts.sqlite（结构化查询）
```

候选审核是自动归档前的最后一层过滤，确保只有用户确认过的内容进入长期记忆。

---

## 八、状态文件位置

`memory/.candidates/review-state.json`（由 `candidates_review.py` 自动管理）

> ⚠️ 不要手动编辑此文件。