---
name: "finebi-openclaw-skill"
description: "一个用于 OpenClaw 的 FineBI 技能，支持 npx 直接运行和插件体系，提供数据分析和可视化功能"
version: 0.1.2
author: zsmj1994
tags:
  - finebi
  - data-analysis
  - visualization
  - business-intelligence
  - reporting
triggers:
  - 使用 FineBI 进行数据看板分析
  - 查询获取 FineBI 数据资产
  - 导出并分析 FineBI 报表数据
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins: ["node"]
      env: ["FINEBI_BASE_URL", "FINEBI_USERNAME", "FINEBI_PASSWORD"]
    primaryEnv: "FINEBI_BASE_URL"
runner: cli
entrypoint: finebi-skill
---

# FineBI 技能

## 技能介绍

该技能集成了 FineBI，能够通过自然语言实现数据分析、生成报告以及查询数据集等功能。

## 工具列表

### `get-dataset-info`
通过名称查询 FineBI 数据集信息。

**参数:**
- `dataset` (string, 必填): 要查询的数据集名称
- `filters` (object, 选填): 用于过滤的键值对

### `preview-dataset-data`
获取数据集的数据预览（限制最大不超过 10w 条数据）。

**参数:**
- `dataset` (string, 必填): 数据表的原始名称
- `page` (number, 选填): 页码，默认为 1
- `size` (number, 选填): 每页数据量，最大支持 100000，默认为 100

### `search-datasets`
根据关键字分⻚搜索 FineBI 数据集。

**参数:**
- `keyword` (string, 必填): 要搜索的关键字
- `page` (number, 选填): 页码，默认为 1

### `export-dashboard-excel`
将仪表板导出为 Excel 格式。

**参数:**
- `reportId` (string, 必填): 仪表板 ID
- `widgetId` (string, 选填): 组件 ID，用于导出特定的组件

### `export-dashboard-pdf`
将仪表板导出为 PDF 格式。响应中会返回文件路径，和文件名。

**参数:**
- `reportId` (string, 必填): 仪表板 ID

### `export-dashboard-image`
将仪表板导出为 PNG 格式的图片。

**参数:**
- `reportId` (string, 必填): 仪表板 ID

### `get-dashboard-user-info`
获取当前用户信息及其创建的仪表板。

**参数:** 无


### `get-dashboards-by-subject`
获取特定主题下的仪表板列表。

**参数:**
- `subjectId` (string, 必填): 主题 ID


---

## 🧩 扩展子技能（需手动加载）

本技能目录下包含 **4 个紧密关联的子技能**，提供高级自动化场景支持。

**⚠️ 重要**：子技能不会自动触发，需要在使用时手动读取对应 SKILL.md 文件。

| 子技能 | 功能描述 | 触发场景 | 文件路径 |
|--------|---------|---------|----------|
| **bi-report-to-doc** | 将 FineBI 仪表盘数据自动生成飞书云文档分析报告 | 经营周报/月报/异常分析报告自动生成 | `bi-report-to-doc/SKILL.md` |
| **skill-bi-briefing** | 将 FineBI 核心指标压缩成飞书群播报卡片，支持定时任务 | 日报/周报/月报/异常播报定时群同步 | `skill-bi-briefing/SKILL.md` |
| **skill-bi-skill-alert-to-task** | 监控 FineBI 指标阈值，自动创建飞书任务并通知负责人 | 库存/销售额/订单金额等阈值告警 | `skill-bi-skill-alert-to-task/SKILL.md` |
| **skill-bi-to-bitable** | 将 FineBI 数据集同步到飞书多维表格，支持追加/覆盖/增量模式 | 数据归档/定时同步/二次协作 | `skill-bi-to-bitable/SKILL.md` |

### 如何加载子技能

使用时通过 `read` 工具读取对应子技能的 SKILL.md：

```json
{
  "action": "read",
  "path": "~/.openclaw/workspace/skills/finebi-skill/bi-report-to-doc/SKILL.md"
}
```

或在主技能中根据用户意图自动推荐：

> 检测到您需要生成经营分析报告，推荐加载 `bi-report-to-doc` 子技能。

### 子技能快速索引

#### 1. bi-report-to-doc（报告生成）
**典型场景**：
- "把经营看板整理成飞书文档"
- "生成上月异常分析报告"
- "数据刷新后自动写周报"

**核心动作链**：
```
search-dashboards → get-dashboard-detail → export-dashboard-pdf/image 
→ 结构化提取 → create-doc → write-content
```

#### 2. skill-bi-briefing（群播报）
**典型场景**：
- "每天早上 9 点在群里发数据日报"
- "设置定时播报任务"
- "先发一条测试卡片看看"

**核心动作链**：
```
search-dashboards → get-dashboard-detail → preview-dataset-data 
→ 结构化播报对象 → send-message-card / create-cron-job
```

#### 3. skill-bi-skill-alert-to-task（阈值告警）
**典型场景**：
- "库存低于 20 就创建任务通知负责人"
- "销售额环比下降超过 30% 自动报警"
- "监控订单金额异常"

**核心动作链**：
```
search-datasets → get-dataset-info → preview-dataset-data 
→ 阈值判定 → create-task → send-private-message
```

#### 4. skill-bi-to-bitable（数据同步）
**典型场景**：
- "把 FineBI 数据同步到飞书多维表格"
- "每周自动追加新数据"
- "按主键增量更新"

**核心动作链**：
```
search-datasets → get-dataset-info → preview-dataset-data 
→ get-bitable-meta → 字段映射 → append/overwrite/upsert
```

---

## 常见工作流 (Common Workflows)

### 使用/获取数据集数据
如果需要提取某个表的数据，标准的工作流程是：
1. **第一步**：先使用 `search-datasets` 命令，根据表名查到表信息，在返回结果中获取对应表的 ID（通常为 `name` 字段，即表的原始名称）。
2. **第二步**：调用 `preview-dataset-data` 命令，传入查到的 ID，从而获取该数据集的具体数据记录。

### 导出 FineBI 仪表板为 PDF，然后分析导出的 PDF 文件生成报告 ⚠️

⚠️ **重要警告**：分析 PDF 时**必须且只能**使用 OpenClaw 内置的 `pdf` 工具！禁止使用任何其他方式读取 PDF 内容！

**工作流程**：
1. **导出 PDF**：调用 `export-dashboard-pdf` 命令，传入 `reportId` 参数，获取导出的 PDF 文件路径。
2. **复制到工作空间**：如果 PDF 在临时目录（如 `/tmp/` 或 `AppData/Local/Temp/`），必须先复制到工作空间目录（通常是 workspace）。
   - Windows: `Copy-Item <源路径> -Destination "C:\Users\dailer\.openclaw\workspace\"`
   - Linux/Mac: `cp <源路径> ~/workspace/`
3. **使用内置 pdf 工具分析** 📌：调用 `pdf` 工具读取 PDF 文件（传入本地文件路径），提取图表和数据内容。
4. **生成报告**：基于 PDF 内容生成 Markdown 格式的分析报告，包含核心主题、关键数据、趋势洞察和业务建议，最后发送给用户。


## 迁移的工具列表 (Migrated Tools)

### `report-list`
Migrated tool: reportList

**参数:**
- `subjectId`: 必填

### `report-info`
Migrated tool: reportInfo

**参数:**
- `reportIds`: 必填

### `report-consanguinity`
Migrated tool: reportConsanguinity

**参数:**
- `reportId`: 必填

### `report-check`
Migrated tool: reportCheck

**参数:**
- 无

### `package-list`
Migrated tool: packageList

**参数:**
- 无

### `package-structure`
Migrated tool: packageStructure

**参数:**
- `packId`: 必填
- `withTables`: 必填

### `data-folders`
Migrated tool: dataFolders

**参数:**
- 无

### `data-folder-tree`
Migrated tool: dataFolderTree

**参数:**
- `folderId`: 必填

### `data-table-preview`
Migrated tool: dataTablePreview

**参数:**
- `tableName`: 必填

### `data-table-structure`
Migrated tool: dataTableStructure

**参数:**
- `tableName`: 必填

### `data-model`
Migrated tool: dataModel

**参数:**
- `modelId`: 必填

### `data-query`
Migrated tool: dataQuery

**参数:**
- `body`: 必填

### `data-preview`
Migrated tool: dataPreview

**参数:**
- `body`: 必填

### `data-search-tables`
Migrated tool: dataSearchTables

**参数:**
- `body`: 必填

### `data-search-fields`
Migrated tool: dataSearchFields

**参数:**
- `body`: 必填

### `data-field-data`
Migrated tool: dataFieldData

**参数:**
- `body`: 必填

### `data-field-range`
Migrated tool: dataFieldRange

**参数:**
- `body`: 必填

### `spider-status`
Migrated tool: spiderStatus

**参数:**
- `taskInstanceId`: 必填

### `subject-folders`
Migrated tool: subjectFolders

**参数:**
- 无

### `subject-tree-root`
Migrated tool: subjectTreeRoot

**参数:**
- 无

### `subject-folder`
Migrated tool: subjectFolder

**参数:**
- `folderId`: 必填

### `subject-tree`
Migrated tool: subjectTree

**参数:**
- `folderId`: 必填

### `subject-crumb`
Migrated tool: subjectCrumb

**参数:**
- `folderId`: 必填

### `subject-content`
Migrated tool: subjectContent

**参数:**
- `subjectId`: 必填

### `subject-reports`
Migrated tool: subjectReports

**参数:**
- `subjectId`: 必填

### `subject-get`
Migrated tool: subjectGet

**参数:**
- `subjectIds`: 必填

### `subject-search`
Migrated tool: subjectSearch

**参数:**
- `body`: 必填

### `subject-groups-search`
Migrated tool: subjectGroupsSearch

**参数:**
- `body`: 必填

### `subject-consanguinity`
Migrated tool: subjectConsanguinity

**参数:**
- `subjectId`: 必填

