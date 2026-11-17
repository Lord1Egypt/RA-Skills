# 参考文档：fuxin-excel — Excel 表格编排规约

> **收敛说明**：本文档为 `fuxin-office` 唯一入口技能**内部参考文档**，承载「Excel 表格编排」规约，
> **不作独立技能对外暴露**（无 frontmatter / Trigger / description）。由 `fuxin-office` 按需读取，
> 企业若需独立技能形式可另行封装。
>
> **产品分类**: `Excel`
> **依赖**: FuxinAiService（端口见 `bridge.md`「运行端口」，由 `MCPServerPort.ini` 读取）+ Excel 产品场景工具
> **需要确认**: 是（写操作；不写前二次确认，写后提示撤销；保存操作 save_document/save_document_as 例外，需提前确认）

---

## 功能概述

本规约通过 MCP 网关**直接调用 Excel 产品的场景工具**（场景工具已在网关内部实现，
agent 只需传参直接调用，无需手动编排原子技能、管理会话或处理批次事务）。
覆盖 3 类电子表格编排任务：

1. **从表抽取数据建新表** — 按列/范围抽取数据，在新 Sheet 中完整保留表头和数据行
2. **条件匹配高亮** — 按数值/文本/日期等条件筛选单元格并批量应用填充色、字体等格式
3. **批量建图** — 对数区域批量创建图表、绑定数据源、设置标题和系列方向

所有写操作由网关内部合并为事务，用户可**一次 Ctrl+Z 整组撤销**；
若需显式管理批次，见 `batch-undo.md`。

---

## 架构

```
用户 (VS Code Copilot)
    │ MCP 协议 (tools/call)
    ▼
FuxinAiService（端口见 `bridge.md`「运行端口」）
    │ 转发到 Excel 产品
    ▼
fuxin-excel 场景工具（网关内部实现）
    │
    ▼
FuxinOfficeExcel App (Office 进程)
```

---

## 前置条件

1. **FuxinAiService 已启动**（端口由 `MCPServerPort.ini` 读取，见 `bridge.md`「运行端口」）
2. **Excel 产品已注册**（产品名 `Excel`），FuxinOfficeExcel 应用已启动、插件已加载
3. **已打开一个工作簿**（所有工具都会修改工作簿内容）

### 预检

执行任何写操作前必须预检，完整预检流程见 `bridge.md`。本规约快速探活：

- 调用 `Excel_get_sheet_summary` / `Excel_get_path` 探活：成功且有活动文档 → 就绪
- 未安装 / 未就绪 / 半就绪（无活动文档）统一按 `bridge.md` 文案输出，
  **禁止**自行发挥或改动文案

> 预检全程只读，禁止任何写入操作。预检失败时按 `bridge.md` 文案提示，禁止执行写操作。

### 场景收尾

> **三档区分**：按操作粒度分选，不可互相替代：
> - **单次操作成功** → `已在文档中完成「{操作名}」。请在福昕Office 中查看效果。`
> - **一组操作完成**（同一场景内多步/批量成组） → `本组修改已完成。如需撤销，请在福昕Office 中按一次「撤销」即可恢复整组操作。`
> - **场景任务完成**（整个场景完全执行完毕） → 输出下方定稿收尾。

每个场景完全执行完毕后，按 `../SKILL.md` 汇总层「五、用户提示文案总则」输出固定收尾，**单次/一组操作不提前套用场景完成文案**：

> `「{场景名}」已执行完毕。请检查文档是否符合预期。`

`{场景名}` 取对应场景中文名（抽取数据 / 条件高亮 / 批量建图）。

---

## 工具列表

### 只读工具

`get_sheet_summary`（数据摘要：非空单元格数、最大行列）/ `get_cell_value`（row/col 0基）/
`get_selection_values`（选区或 ranges 二维数组）/ `get_document_text` / `get_path`

### 1. extract_data_to_new_sheet（抽取数据建新表）

| 参数 | 必填 | 说明 |
|------|------|------|
| `sourceRange` | ✅ | 源范围，如 "A1:D100" |
| `targetSheetName` | ✅ | 新工作表名 |
| `columns` | ❌ | 提取列：列字母或 0 基索引；不传=全部（工具默认值）。**语义区分**：缺省=全部列属工具默认行为；但用户若显式表达「不抽某列/不抽任何列」且与建表目标矛盾时属**歧义**，必须先追问澄清（见 `../SKILL.md` §4.1「缺参/歧义必追问」），**不得**静默按默认值执行 |
| `includeHeader` / `sourceSheet` | ❌ | 首行是否表头（默认 true）/ 源表名（空=活动表） |
| `sortBy` / `sortOrder` | ❌ | 排序列 / asc(默认)·desc |
| `numberFormats` | ❌ | 每列数字格式数组，如 ["#,##0","0.00",null] |
| `headerBold` / `headerColor` / `headerFontColor` / `activateTarget` | ❌ | 表头样式（默认加粗+4472C4 背景）/ 完成后激活目标表 |

**调用示例**：
```json
{
  "sourceRange": "A1:D100",
  "targetSheetName": "汇总",
  "columns": ["A", "B", "D"],
  "includeHeader": true,
  "sortBy": "B",
  "sortOrder": "desc",
  "activateTarget": true
}
```

### 2. highlight_by_condition（条件高亮）

参数 `rules` 数组，每项：
- `type`：`cellValue`(默认) / `textContains` / `dateOccurring` / `duplicateValues` / `topBottom` / `aboveBelowAverage`
- `range`（如 "A1:A100"）+ 按类型配套：`operator`+`value1`/`value2`、`text`+`textOperator`、`period`、`unique`、`rank`/`percent`/`bottom`、`averageScope`
- 样式：`backgroundColor`(默认FF0000)、`fontColor`、`bold`、`italic`、`underline`

**调用示例**：
```json
{
  "rules": [
    {"type": "cellValue", "range": "B2:B100", "operator": "greaterThan", "value1": 100, "backgroundColor": "FF0000"},
    {"type": "textContains", "range": "A2:A100", "text": "待办", "backgroundColor": "FFC000"}
  ]
}
```

### 3. batch_create_charts（批量建图）

参数 `charts` 数组，每项：
- `sourceRange`（如 "A1:B10"）、`chartType`(Bar2DClusterdCol 柱状图默认 / LineClusterd 折线 / PieNormal 饼图 / AreaClusterd 面积)
- `title`、`hasLegend`(默认 true)、`plotByRows`(默认 false=按列系列)
- `position`：`{row=0, col=0, width=400, height=300}`

**调用示例**：
```json
{
  "charts": [
    {"sourceRange": "A1:B10", "chartType": "Bar2DClusterdCol", "title": "月度营收", "position": {"row": 0, "col": 0}},
    {"sourceRange": "A1:C10", "chartType": "LineClusterd", "title": "趋势", "position": {"row": 0, "col": 5}}
  ]
}
```

> 范围格式为 A1 样式；`get_cell_value` 行列索引为 0 基。

---

## 使用方式

agent 识别到对应 Trigger 关键词（由 `fuxin-office` 路由）后，按以下流程执行：

1. 确定使用的场景工具（三选一）
2. 预检 Excel 链路（调用 `Excel_get_path`；完整预检见 `bridge.md`）；
   预检失败按 `bridge.md` 文案提示，**禁止执行写操作**
3. **缺参/歧义必追问**（`../SKILL.md` §4.1）：组装参数前，先判定用户指令是否缺必填参数或存在歧义。命中则**先追问澄清**，补齐后再继续；**不得**按工具默认值静默执行、**不得**臆造参数。
   - 典型歧义场景：`extract_data_to_new_sheet` 用户说「不抽任何列」与「建新表」矛盾 → 必须追问（不得套用 `columns` 不传=全部 的默认值）；`highlight_by_condition` 未指明范围/列 → 追问范围；`batch_create_charts` 未指明数据源范围 → 追问范围。
4. **跨产品写前闸门**：若命中 `../SKILL.md`「五·一、跨产品写前闸门」（本产品非当前活跃 / 首次写，如用户正用 Word 前台却下达 Excel 抽列指令），先按标准话术提示切换到 Excel 窗口并等待口令，未通过前**不调用写工具**
5. 建立 MCP 会话（initialize → notifications/initialized）
6. 按上方参数表组装参数，一次调用场景工具；**每次调用都须在参数顶层携带埋点字段**：
   - `skill_id`：本技能标识，固定填 `fuxin-excel`
   - `scenario_id`：本次使用的场景编号，`extract_data_to_new_sheet` 填 `UC-EXCEL-S1`、`highlight_by_condition` 填 `UC-EXCEL-S2`、`batch_create_charts` 填 `UC-EXCEL-S3`
   （网关据此关联到具体 Skill/场景用于调用统计；传入即回显，不传则不回显）
7. 需要验证结果时调用只读工具（`Excel_get_document_info` / `Excel_get_sheet_summary`）读取内容
8. 向用户报告执行结果（成功数、失败数、生成内容摘要）
9. 不写前二次确认；写成功后按 `../SKILL.md` 汇总层输出固定写后撤销提示（改好了。要撤回改动：回复「撤销」，或在福昕Office 按 Ctrl+Z。）；危险操作仍弹确认对话框；失败/取消按 `bridge.md`「错误 / 异常（统一展示）」文案。**保存操作例外**：调用 `Excel_save_document` / `Excel_save_document_as`（保存属不可逆、无撤销）前，先输出 `bridge.md` 「保存确认提示」并等待用户选择，用户确认后才保存，取消则中止（取消/超时文案见「错误 / 异常（统一展示）」）

### 与其它编排规约协同

- **预检**：完整五层预检见 `bridge.md`
- **批次撤销**：写操作间默认由网关合并为单事务；如需显式批次见 `batch-undo.md`
- **文档问答**：对工作簿内容提问见 `doc-qa.md`
- **跨产品**：Word→Excel→PPT 跨应用分步执行，见 `../SKILL.md`（E2E 分步编排）