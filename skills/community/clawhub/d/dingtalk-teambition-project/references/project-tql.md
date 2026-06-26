# 项目 TQL 参考

项目 TQL 用于查询 Teambition 项目。通过 `query_projects.py --tql` 传入。

## 常用场景速查

| 场景 | TQL |
|------|-----|
| 我参与的项目 | `involveMembers = me()` |
| 我创建的项目 | `creatorId = me()` |
| 名称模糊搜索 | `nameText ~ '电商'` |
| 名称或描述全文搜索 | `text ~ '关键词'` |
| 未归档项目 | `isSuspended = false` |
| 已归档项目 | `isSuspended = true` |
| 在回收站的项目 | `isArchived = true` |
| 今天创建 | `created >= startOf(d) AND created <= endOf(d)` |
| 本周创建 | `created >= startOf(w) AND created <= endOf(w)` |
| 今天更新 | `updated >= startOf(d) AND updated <= endOf(d)` |
| 过去7天创建 | `created >= startOf(d, -7d) AND created <= endOf(d, -1d)` |

## 字段说明

| 字段 | 支持的操作符 | 说明 |
|------|------------|------|
| `involveMembers` | `=` `!=` `IN` `NOT IN` | 项目成员 ID，用 `me()` 表示当前用户 |
| `creatorId` | `=` `!=` `IN` `NOT IN` | 创建人 ID，支持 `me()` |
| `nameText` | `=` `~` | 项目名称（`~` 模糊匹配，`=` 精确匹配） |
| `text` | `~` | 全文搜索（项目名称 + 项目描述） |
| `description` | `=` | 项目描述 |
| `isSuspended` | `=` | 是否已归档（`true` / `false`） |
| `isArchived` | `=` | 是否在回收站（`true` / `false`） |
| `isTemplate` | `=` | 是否是模板项目（默认已排除） |
| `visibility` | `=` | 可见性：`project`（私有）/ `organization`（企业公开）/ `org`（公开） |
| `created` | `=` `!=` `>` `>=` `<` `<=` | 创建时间 |
| `updated` | `=` `!=` `>` `>=` `<` `<=` | 更新时间 |
| `cf:<fieldId>` (数字) | `=` `!=` `>` `>=` `<` `<=` | 自定义字段（数字类型） |
| `cf:<fieldId>` (文本) | `=` `!=` | 自定义字段（文本类型） |
| `cf:<fieldId>` (日期) | `=` `!=` `>` `>=` `<` `<=` | 自定义字段（日期类型） |
| `cf:<fieldId>` (多选) | `=` `!=` `IN` `NOT IN` | 自定义字段（多选类型） |
| `cf:<fieldId>` (单选) | `=` `!=` `IN` `NOT IN` | 自定义字段（单选类型） |

## 时间偏移速查（以 `created` 为例，`updated` 同理）

| 场景 | TQL |
|------|-----|
| 今天 | `created >= startOf(d) AND created <= endOf(d)` |
| 昨天 | `created >= startOf(d, -1d) AND created <= endOf(d, -1d)` |
| 过去3天 | `created >= startOf(d, -3d) AND created <= endOf(d, -1d)` |
| 过去7天 | `created >= startOf(d, -7d) AND created <= endOf(d, -1d)` |
| 过去30天 | `created >= startOf(d, -30d) AND created <= endOf(d, -1d)` |
| 最近7天（含今天） | `created >= startOf(d, -6d) AND created <= endOf(d)` |
| 本周 | `created >= startOf(w) AND created <= endOf(w)` |
| 上周 | `created >= startOf(w, -1w) AND created <= endOf(w, -1w)` |
| 本月 | `created >= startOf(M) AND created <= endOf(M)` |
| 上月 | `created >= startOf(M, -1M) AND created <= endOf(M, null, -1M)` |
| 今年 | `created >= startOf(y) AND created <= endOf(y)` |
| 指定日期之后 | `created >= '2026-03-01T00:00:00+08:00'` |
| 指定日期范围 | `created >= '2026-03-01T00:00:00+08:00' AND created <= '2026-03-31T23:59:59+08:00'` |

## 常用查询示例

```bash
# 我参与的项目，按更新时间降序
uv run scripts/query_projects.py --tql "involveMembers = me() ORDER BY updated DESC"

# 按名称搜索未归档项目
uv run scripts/query_projects.py --tql "nameText ~ '产品开发' AND isSuspended = false"

# 过去7天创建的、我参与的、非模板项目，按更新时间降序
uv run scripts/query_projects.py --tql "isTemplate = false AND isArchived = false AND isSuspended = false AND involveMembers = me() AND created >= startOf(d, -7d) ORDER BY updated DESC"

# 今天有更新的我参与的项目
uv run scripts/query_projects.py --tql "involveMembers = me() AND updated >= startOf(d) AND updated <= endOf(d)"

# 查询企业公开项目
uv run scripts/query_projects.py --tql "visibility = organization AND isSuspended = false"

# 查询自定义字段包含关键词的项目
uv run scripts/query_projects.py --tql "cf:609e13e0cea6e8205508f350 ~ '上线' AND isArchived = false AND isTemplate = false"

# 组合条件：名称包含"开发"或"测试"且未归档
uv run scripts/query_projects.py --tql "(nameText ~ '开发' OR nameText ~ '测试') AND isSuspended = false"
```

## 最佳实践

1. **默认排除模板**：`query_projects.py` 已自动排除模板（`isTemplate = false`），无需手动添加
2. **必须使用 `me()`**：查询"我的"项目时，用 `involveMembers = me()` 而非硬编码用户 ID
3. **项目无 dueDate**：项目没有截止时间字段，只有 `created` 和 `updated`
4. **复杂条件加括号**：多个 OR 条件与 AND 组合时，用括号明确优先级，避免歧义
5. **合理排序**：时间相关查询建议加 `ORDER BY updated DESC` 或 `ORDER BY created DESC`
