# 知识库接口 — 按需信息通道

> 知识库是与「联网搜索」平行的信息获取/存储通道。
> 设计核心：**标准硬编码 + LLM负责格式翻译**，所有数据按标准写入，确保DB结构稳定可预期。
> 详见 `scripts/knowledge_schema.py`（标准定义）| `scripts/project_knowledge.py`（引擎实现）
> 知识库的读写行为受 `scripts/settings_manager.py` 全局配置控制（kb_collect_mode / kb_query_mode）。

---

## 核心原则

### 按需调用（与联网搜索一致）

知识库的读写**不是自动的**。遵循 search-integration.md 的按需模式：

| 操作 | 触发条件 | 对比例 |
|------|---------|--------|
| **读** | 用户要求查历史/查基准/查同类项目 **或** LLM判断需要参考历史数据 | 等同于联网搜索的"大模型自判→搜索"流程 |
| **写** | 用户明确说"存下来""记录这个""入库" | 非自动，用户决定写入时机 |
| **外部对接** | 用户要求"导入这个文件/数据库" | LLM按标准映射规则处理 |

> 按需行为的强弱受 `settings_manager.py` 全局配置控制：
> - `kb_collect_mode=auto` → 估算完成后自动向用户确认"是否写入知识库"
> - `kb_collect_mode=manual` → 仅用户明确要求时写入
> - `kb_query_mode=auto` → 估算前自动查询历史同类项目基准
> - `kb_query_mode=manual` → 仅用户明确要求时查询

### LLM的职责：格式翻译官

LLM **不创造字段**、**不自行决定映射规则**。职责只有一条：

```
识别源格式（CSV / SQLite / MD / Word / JSON / 文本）
  → 解析字段名和内容
  → 对照下方标准字段表，正确赋值
  → 调用 project_knowledge 的入口函数
```

### 平行通道架构

```
用户输入/指令
  ↓
【按需】选择以下通道（可并行）：
  ├── 联网搜索（参见 search-integration.md）
  ├── 知识库查询（本文件）
  │     ├── 查历史项目
  │     ├── 查任务基准
  │     ├── 查通用知识条目
  │     └── 对接外部数据库/文件
  └── 技能搜索（find-skills）
```

---

## 标准字段定义

### 知识条目字段（`knowledge_entries` 表）

以下字段是硬编码标准，LLM 必须严格对照赋值：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 标题 |
| `content` | string | ❌ | 内容（Markdown格式） |
| `source` | string | ❌ | 来源（URL/书名/报告名） |
| `entry_type` | string | ❌ | `note`(笔记) / `article`(文章) / `benchmark`(基准) / `industry`(行业) / `project_ref`(项目参考) / `imported`(导入) |
| `tags` | string | ❌ | 逗号分隔标签，如 `"AI,Agent,项目管理"` |
| `domain` | string | ❌ | `ai-enterprise` / `construction` / `software` / `manufacturing` / `event` / `research` / `general` |
| `ref_link` | string | ❌ | 引用链接 |

### 项目字段（`projects` 表 + 关联表）

| 字段 | 类型 | 说明 |
|------|------|------|
| `project_name` | string | 项目名称 |
| `description` | string | 项目描述 |
| `domain` | string | 领域分类（同上） |
| `phases` | list[dict] | 工作包列表，每项含 `name/o/m/p/deliverable` |
| `dependencies` | dict | 紧前关系 `{task_id: [(pred_id, dep_type)]}` |
| `cpm_result` | object | CPM计算结果 |
| `mc_results` | dict | 蒙特卡洛模拟结果 |

### 项目JSON标准格式（`wbs-v1`）

```json
{
  "format": "wbs-v1",
  "project": {
    "name": "项目名称",
    "description": "项目描述",
    "domain": "ai-enterprise",
    "total_duration": 30
  },
  "work_packages": [
    {
      "id": 1,
      "name": "1.1 需求调研",
      "phase": "1",
      "o": 3.0,
      "m": 5.0,
      "p": 8.0,
      "deliverable": "需求文档",
      "is_critical": true
    }
  ],
  "dependencies": [
    {"task": 2, "depends_on": 1, "type": "FS"}
  ]
}
```

---

## 接口函数

### 写入（按需，仅用户要求时）

| 函数 | 用途 | 调用时机 |
|------|------|---------|
| `save_knowledge(title, content, source, entry_type, tags, domain, ref_link)` | 存任意知识条目 | 用户说"存下这条记录" |
| `save_project(state)` | 存当前项目全量数据到知识库 | 用户说"把这个项目入库" |
| `save_knowledge_batch(entries)` | 批量存入 | 导入多条记录 |

### 读取（按需，用户要求或LLM主动参考）

| 函数 | 用途 | 调用时机 |
|------|------|---------|
| `search(query, limit, entry_type, domain)` | 全文搜索知识条目 | 查资料/确认已有知识 |
| `search_projects(query, domain, limit)` | 搜索历史项目 | 用户问"以前做过类似项目吗" |
| `get_benchmarks(task_pattern, domain)` | 获取同类任务OMP基准 | 新项目估算时参考历史数据 |
| `get_dependency_patterns(domain)` | 获取常用依赖类型分布 | 规划依赖关系时参考 |

### 外部对接（按需，用户要求时）

| 函数 | 用途 | 调用时机 |
|------|------|---------|
| `import_external_knowledge(db, table, mapping)` | 从外部SQLite导入 | 用户说"把这个数据库导入" |
| `connect_external(path)` | 连接外部SQLite（裸查询） | 用户说"帮我查这个数据库" |
| `export_knowledge(path)` | 导出知识库文件 | 用户说"备份知识库" |

---

## LLM格式解析指引

当用户要求对接外部数据时，LLM按以下流程处理：

### 第一步：识别源格式

| 源格式 | 判断依据 | 解析策略 |
|--------|---------|---------|
| **SQLite 数据库** | 文件扩展名 .db 或 .sqlite | 调用 `connect_external()` 查表结构 → 读列名 + 样例 |
| **CSV (.csv)** | 文件扩展名 | 读第一行表头 → 读前3行样例 |
| **Markdown (.md)** | 文件扩展名 | 检查是否有YAML frontmatter → 读内容 |
| **JSON (.json)** | 文件扩展名 | 读顶层字段 → 判断是条目还是列表 |
| **Word (.docx)** | 文件扩展名 | 提取文本内容 → 判断结构 |
| **Excel (.xlsx)** | 文件扩展名 | 读表头 + 前几行样例 |
| **纯文本** | 无格式标记 | 内容分析 → LLM提取结构信息 |

### 第二步：字段映射规则

**核心约束：标准字段是死的。LLM把外部字段名"翻译"到标准字段。**

标准映射对照表（硬编码，LLM据此做翻译）：

| 标准字段 | 外部常见名（中/英） |
|---------|------------------|
| `title` | title / name / subject / 标题 / 名称 / 主题 / 文件名(Obsidian) |
| `content` | content / body / text / description / 内容 / 正文 / 描述 |
| `tags` | tags / labels / label / tag / 标签 / 分类 |
| `domain` | domain / category / categories / 领域 / 类别 |
| `source` | source / url / link / 来源 / 来源链接 |
| `entry_type` | type / kind / entry_type / 类型 |
| `ref_link` | ref_link / reference / 引用链接 |

**示例：用户给一个CSV，列名是 `["项目名称", "描述", "标签"]`**
```
LLM解析：
  "项目名称" → title
  "描述"     → content
  "标签"     → tags
调用 save_knowledge(title=row["项目名称"], content=row["描述"], tags=row["标签"])
```

### 第三步：值合法性检查

LLM赋值后必须检查：

- `entry_type` 必须是 `note/article/benchmark/industry/project_ref` 之一
- `domain` 必须是 `ai-enterprise/construction/software/manufacturing/event/research/general` 之一
- `tags` 统一转为逗号分隔字符串
- OMP值必须满足 `O ≤ M ≤ P`
- 所有不应为空的字段不能留空

---

## 与联网搜索的协作

知识库查询和联网搜索是**平行通道**，可串行或并行使用：

| 场景 | 推荐通道组合 |
|------|------------|
| 查同类项目历史数据 | 先查知识库（`get_benchmarks`），不够再联网搜索 |
| 用户提供外部数据库要导入 | 只用知识库写入通道 |
| 用户问"以前有类似的吗" | 知识库搜索（`search_projects`） |
| 用户说"把这个和网上的资料结合起来看" | **并行**：知识库搜索 + 联网搜索，汇总后给结论 |

---

## 已知对接预置

`knowledge_schema.py` 中的 `TABLE_MAPPINGS` 预置了以下外部系统的字段映射：

| 系统 | 来源格式 | 自动检测 |
|------|---------|---------|
| **Obsidian** | Markdown + frontmatter | ✅ 文件名→title, body→content |
| **Notion导出** | CSV/Markdown | ✅ Name→title, Content→content |
| **Hugo** | Markdown + frontmatter | ✅ frontmatter.title→title |
| **Jira导出** | CSV | ✅ Summary→title, Description→content |

如果外部数据格式匹配以上预置，优先使用自动检测（`detect_table_mapping()`）。
如果不匹配，LLM按上述格式解析指引自行处理。
