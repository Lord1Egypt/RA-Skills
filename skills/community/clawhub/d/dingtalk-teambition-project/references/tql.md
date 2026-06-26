# 任务 TQL 参考

TQL（Task Query Language）用于查询 Teambition 任务。通过 `query_tasks.py --tql` 传入。

## 常用场景速查

### 个人任务

| 场景 | TQL |
|------|-----|
| 我的待办任务 | `executorId = me() AND isDone = false` |
| 我的逾期任务 | `executorId = me() AND isDone = false AND dueDate < startOf(d)` |
| 我的已完成 | `executorId = me() AND isDone = true` |
| 我今天截止的任务 | `executorId = me() AND dueDate >= startOf(d) AND dueDate <= endOf(d)` |
| 我本周截止的任务 | `executorId = me() AND dueDate >= startOf(w) AND dueDate <= endOf(w)` |
| 我创建的未完成任务 | `creatorId = me() AND isDone = false` |
| 我参与的任务 | `involveMembers = me()` |
| 即将逾期（未来3天截止） | `executorId = me() AND isDone = false AND dueDate <= endOf(d, 3d) AND dueDate >= startOf(d)` |

### 团队任务

| 场景 | TQL |
|------|-----|
| 未指派的任务 | `executorId = null AND isDone = false` |
| 高优先级未完成 | `priority = 0 AND isDone = false` |
| 本周创建的任务 | `created >= startOf(w) AND created <= endOf(w)` |
| 指定项目 | `projectId = 'xxx'` |
| 标题模糊搜索 | `title ~ '关键词'` |
| 全文搜索（标题+备注+短ID） | `text ~ '关键词'` |
| 上周更新 | `updated >= startOf(w, -1w) AND updated <= endOf(w, -1w)` |
| 过去7天更新 | `updated >= startOf(d, -7d) AND updated <= endOf(d)` |

## 字段说明

| 字段 | 支持的操作符 | 说明 |
|------|------------|------|
| `executorId` | `=` `!=` `IN` `NOT IN` | 执行人 ID，用 `me()` 表示当前用户，`null` 表示未指派 |
| `creatorId` | `=` `!=` `IN` `NOT IN` | 创建人 ID |
| `involveMembers` | `=` `!=` `IN` `NOT IN` | 参与者 ID |
| `isDone` | `=` `!=` | 是否完成（`true` / `false`） |
| `isArchived` | `=` `!=` | 是否归档（`true` / `false`） |
| `dueDate` | `=` `!=` `>` `>=` `<` `<=` | 截止时间 |
| `startDate` | `=` `!=` `>` `>=` `<` `<=` | 开始时间 |
| `accomplished` | `=` `!=` `>` `>=` `<` `<=` | 完成时间 |
| `created` | `=` `!=` `>` `>=` `<` `<=` | 创建时间 |
| `updated` | `=` `!=` `>` `>=` `<` `<=` | 更新时间 |
| `priority` | `=` `!=` `IN` `NOT IN` | 优先级（0=紧急 1=高 2=中 3=低） |
| `projectId` | `=` `!=` `IN` `NOT IN` | 项目 ID |
| `title` | `~` | 任务标题（模糊匹配） |
| `text` | `~` | 全文搜索（标题 + 备注 + 短ID） |
| `tagId` | `=` `!=` `IN` `NOT IN` | 标签 ID |
| `stageId` | `=` `!=` `IN` `NOT IN` | 任务列 ID |
| `taskflowstatusId` | `=` `!=` `IN` `NOT IN` | 任务状态 ID |
| `scenarioId` | `=` `!=` `IN` `NOT IN` | 任务类型 ID |
| `tasklistId` | `=` `!=` `IN` `NOT IN` | 任务分组 ID |
| `storyPoint` | `=` `!=` | Story Point |
| `cf:<fieldId>` (数字) | `=` `!=` `>` `>=` `<` `<=` | 自定义字段（数字类型） |
| `cf:<fieldId>` (文本) | `~` `!~` | 自定义字段（文本类型） |
| `cf:<fieldId>` (日期) | `=` `!=` `>` `>=` `<` `<=` | 自定义字段（日期类型） |
| `cf:<fieldId>` (多选) | `~` `!~` | 自定义字段（多选类型） |
| `cf:<fieldId>` (单选) | `=` `!=` `IN` `NOT IN` | 自定义字段（单选类型） |

## 时间函数

### 基础函数

| 函数 | 说明 |
|------|------|
| `startOf(d)` | 今天开始（00:00:00） |
| `endOf(d)` | 今天结束（23:59:59） |
| `startOf(w)` | 本周开始（周一） |
| `endOf(w)` | 本周结束（周日） |
| `startOf(M)` | 本月开始 |
| `endOf(M)` | 本月结束 |
| `startOf(y)` | 今年开始 |
| `endOf(y)` | 今年结束 |

### 时间偏移（以 `dueDate` 为例，其他时间字段同理）

| 场景 | TQL |
|------|-----|
| 今天 | `dueDate >= startOf(d) AND dueDate <= endOf(d)` |
| 昨天 | `dueDate >= startOf(d, -1d) AND dueDate <= endOf(d, -1d)` |
| 过去3天 | `dueDate >= startOf(d, -3d) AND dueDate <= endOf(d, -1d)` |
| 过去7天 | `dueDate >= startOf(d, -7d) AND dueDate <= endOf(d, -1d)` |
| 过去30天 | `dueDate >= startOf(d, -30d) AND dueDate <= endOf(d, -1d)` |
| 最近7天（含今天） | `dueDate >= startOf(d, -6d) AND dueDate <= endOf(d)` |
| 未来3天 | `dueDate >= startOf(d, 1d) AND dueDate <= endOf(d, 3d)` |
| 未来7天 | `dueDate >= startOf(d, 1d) AND dueDate <= endOf(d, 7d)` |
| 本周 | `dueDate >= startOf(w) AND dueDate <= endOf(w)` |
| 上周 | `dueDate >= startOf(w, -1w) AND dueDate <= endOf(w, -1w)` |
| 本月 | `dueDate >= startOf(M) AND dueDate <= endOf(M)` |
| 上月 | `dueDate >= startOf(M, -1M) AND dueDate <= endOf(M, null, -1M)` |
| 今年 | `dueDate >= startOf(y) AND dueDate <= endOf(y)` |
| 未填写 | `dueDate = null` |
| 已填写 | `dueDate != null` |
| 指定日期范围 | `dueDate >= '2026-03-01T00:00:00+08:00' AND dueDate <= '2026-03-31T23:59:59+08:00'` |

## 运算符

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `=` | 等于 | `isDone = false` |
| `!=` | 不等于 | `priority != 3` |
| `<` | 小于 | `dueDate < startOf(d)` |
| `<=` | 小于等于 | `dueDate <= endOf(w)` |
| `>` | 大于 | `dueDate > endOf(d)` |
| `>=` | 大于等于 | `dueDate >= startOf(w)` |
| `~` | 模糊匹配 | `title ~ '关键词'` |
| `IN` | 包含（多值匹配） | `priority IN (0, 1)` |
| `NOT IN` | 不包含 | `priority NOT IN (2, 3)` |
| `AND` | 与 | `isDone = false AND priority = 0` |
| `OR` | 或 | `priority = 0 OR priority = 1` |

## 排序

```
ORDER BY dueDate ASC       # 截止时间升序
ORDER BY dueDate DESC      # 截止时间降序
ORDER BY priority ASC      # 优先级升序（紧急在前）
ORDER BY updated DESC      # 最近更新在前
ORDER BY created DESC      # 最新创建在前
ORDER BY accomplished DESC # 最近完成在前
ORDER BY startDate ASC     # 开始时间升序
```

## 常用查询示例

```bash
# 我的逾期未完成任务，按截止时间升序
uv run scripts/query_tasks.py --tql "executorId = me() AND isDone = false AND dueDate < startOf(d) ORDER BY dueDate ASC"

# 我本周截止的任务
uv run scripts/query_tasks.py --tql "executorId = me() AND dueDate >= startOf(w) AND dueDate <= endOf(w)"

# 即将逾期（未来3天内截止的未完成任务）
uv run scripts/query_tasks.py --tql "executorId = me() AND isDone = false AND dueDate >= startOf(d) AND dueDate <= endOf(d, 3d)"

# 未指派的高优先级任务
uv run scripts/query_tasks.py --tql "executorId = null AND priority = 0 AND isDone = false"

# 过去7天更新过的我的任务，按更新时间降序
uv run scripts/query_tasks.py --tql "executorId = me() AND updated >= startOf(d, -7d) ORDER BY updated DESC"

# 我完成的且未归档的任务，按完成时间降序
uv run scripts/query_tasks.py --tql "isDone = true AND executorId = me() AND isArchived = false ORDER BY accomplished DESC"

# 标题或备注包含关键词的任务（全文搜索）
uv run scripts/query_tasks.py --tql "text ~ '需求评审'"

# SP 在 1-5 之间的我的任务
uv run scripts/query_tasks.py --tql "storyPoint >= 1 AND storyPoint <= 5 AND executorId = me()"

# 查询自定义字段（文本类型）包含关键词
uv run scripts/query_tasks.py --tql "cf:609e13e0cea6e8205508f350 ~ '上线'"
```

## 注意事项

- **必须使用 `me()`**：查询"我的"任务时，用 `executorId = me()` 而非硬编码用户 ID
- **时区**：TQL 中的时间函数基于用户时区自动处理，无需手动转换
- **字符串值**：字符串值用单引号包裹，如 `projectId = 'xxx'`
- **null 查询**：`field = null` 表示未填写，`field != null` 表示已填写
- **自定义字段**：使用 `cf:<fieldId>` 格式，fieldId 从 `get_custom_fields.py` 获取
- **优先级值**：`0`=紧急、`1`=高、`2`=中、`3`=低
