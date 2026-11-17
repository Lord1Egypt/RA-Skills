# 参考文档：fuxin-ppt — PowerPoint 演示编排规约

> **收敛说明**：本文档为 `fuxin-office` 唯一入口技能**内部参考文档**，承载「PowerPoint 演示编排」规约，
> **不作独立技能对外暴露**（无 frontmatter / Trigger / description）。由 `fuxin-office` 按需读取，
> 企业若需独立技能形式可另行封装。
>
> **产品分类**: `PowerPoint`
> **依赖**: FuxinAiService（端口见 `bridge.md`「运行端口」，由 `MCPServerPort.ini` 读取）+ PowerPoint 产品场景工具
> **需要确认**: 是（写操作；不写前二次确认，写后提示撤销；保存操作 save_document/save_document_as 例外，需提前确认）

---

## 功能概述

本规约通过 MCP 网关**直接调用 PowerPoint 产品的场景工具**（场景工具已在网关内部实现，
agent 只需传参直接调用，无需手动编排原子技能、管理会话或处理批次事务）。
覆盖 3 类演示文稿编排任务：

1. **生成汇报 Deck** — 自动生成含多页幻灯片的汇报演示文稿，每页配有标题/正文、格式美化及演讲者备注（≥3 页，每页有备注）
2. **整理已有演示稿** — 删除冗余页、复制模板页、应用布局模板、插入空白页（经 `generate_deck` + `layout=Blank` 实现）
3. **选区编辑助手** — 对选中的形状或文本按指令进行修改

所有写操作由网关内部合并为事务，用户可**一次 Ctrl+Z 整组撤销**；
若需显式管理批次，见 `batch-undo.md`。

---

## 架构

```
用户 (VS Code Copilot)
    │ MCP 协议 (tools/call)
    ▼
FuxinAiService（端口见 `bridge.md`「运行端口」）
    │ 转发到 PowerPoint 产品
    ▼
fuxin-ppt 场景工具（网关内部实现）
    │
    ▼
FuxinOfficePPT App (Office 进程)
```

---

## 前置条件

1. **FuxinAiService 已启动**（端口由 `MCPServerPort.ini` 读取，见 `bridge.md`「运行端口」）
2. **PowerPoint 产品已注册**（产品名 `PowerPoint`），FuxinOfficePPT 应用已启动、插件已加载
3. **已打开一个演示文稿**（所有工具都会修改演示稿内容）

### 预检

执行任何写操作前必须预检，完整预检流程见 `bridge.md`。本规约快速探活：

- 调用 `PowerPoint_get_document_info` / `PowerPoint_get_path` 探活：成功且有活动演示 → 就绪
- 未安装 / 未就绪 / 半就绪（无活动文档）统一按 `bridge.md` 文案输出，
  禁止自行发挥或改写文案
- **空演示文稿（0 页）也是活动文档**，不误判为无活动文档；判定以 `get_document_info` 的
  `docId`/`GetId` 是否非空为准

> 预检全程只读，禁止任何写入操作。预检失败时按 `bridge.md` 文案提示，禁止执行写操作。

### 场景收尾

> **三档区分**：按操作粒度分选，不可互相替代：
> - **单次操作成功** → `已在文档中完成「{操作名}」。请在福昕Office 中查看效果。`
> - **一组操作完成**（同一场景内多步/批量成组） → `本组修改已完成。如需撤销，请在福昕Office 中按一次「撤销」即可恢复整组操作。`
> - **场景任务完成**（整个场景完全收尾） → 输出下方定稿收尾。

每个场景完全执行完毕后，按 `../SKILL.md` 汇总层「五、用户提示文案总则」输出固定收尾，**单次/一组操作不提前套用场景完成文案**：

> `「{场景名}」已执行完毕。请检查文档是否符合预期。`

`{场景名}` 取对应场景中文名（生成汇报 / 整理演示 / 选区编辑）。

---

## 工具列表

### 只读工具

`get_document_info`（文档信息）/ `get_path` / `get_ppt_outline`（大纲）/ `get_slide_layouts`（布局模板列表）/
`get_slide_text`（指定页文本+备注，slideIndex 1基）/ `get_selected_text_range`（文本选区）

### 1. generate_deck（生成汇报 Deck）

| 参数 | 必填 | 说明 |
|------|------|------|
| `slides` | ✅ | 每页：`title`、`body`（`\n` 分行）、`notes`、`layout`(Blank/Title/Text/TitleOnly/TwoColumnText/SectionHeader/Table/Chart)、逐页样式覆盖（title*/body* 的 FontSize/Color/FontFace/X/Y/W/H） |
| `slides[].blocks` | ❌ | 灵活内容块数组：任意数量的 `text`（文本框）/`shape`（形状），支持精确坐标或 `edge` 锚定定位，用于复杂版式 |
| `startPosition` | ❌ | 插入起始位置（1基，默认末尾追加）。范围自动收敛：`≤0` 归为末位追加；大于「当前页数+1」自动 clamp 回末尾追加 |
| 全局默认 | ❌ | titleFontSize=40、bodyFontSize=18、字体 Pretendard、标题色 1F1F1F、正文色 333333 等 |

> 建议 ≥3 页，每页配 `notes` 演讲者备注。

> **edge 与坐标优先级**：显式 `x`/`y` 优先于 `edge` 锚定；`edge` 按页尺寸推算（16:9 = 13.333"×7.5"）。`startPosition` 支持插入到开头（1）或中间指定页，极端值（超范围/非正）自动收敛到末尾追加，不会污染其他页。

> **能力边界（重要）**：当前 SDK **无法在幻灯片上插入真实表格/图表/图片**。禁止向 `generate_deck` 传 `tableRows`/`tableData`/`table`/`chartData`/`chart`/`imagePath`/`image`（顶层或每页）——传入会返回失败（不会静默忽略）。若用户要求真表/真图/插图，应明确告知「当前仅支持版式与文本/形状，不支持表格/图表/图片数据」，或先用 `layout=Table/Chart` 插入空白版式页 + `blocks` 中 `text`/`shape` 近似绘制，再请用户手动填充。

**`blocks` 内容块字段**：
| 字段 | 说明 |
|------|------|
| `type` | `text`（默认）/`shape` |
| `text` | 文本内容（type=text） |
| `shapeType` | 形状类型 ShapeType 枚举名：Rectangle/Ellipse/Triangle/RightArrow 等（type=shape） |
| `x`/`y` | 左上角坐标（英寸）；省略时可用 `edge` 锚定 |
| `w`/`h` | 宽度/高度（英寸） |
| `edge` | 锚定边：top/bottom/left/right，可组合（斜杠分隔，如 `bottom/right`） |
| `fontSize`/`fontFace`/`color` | 文字字号/字体/颜色 RRGGBB（type=text） |
| `fillColor`/`noLine` | 填充色 RRGGBB / 是否无边框（type=shape） |

**调用示例**（title/body + 灵活 blocks 混用）：
```json
{
  "slides": [
    {"title": "项目汇报", "body": "本季度进展顺利", "notes": "开场介绍"},
    {
      "title": "封面",
      "layout": "Blank",
      "blocks": [
        {"type": "text", "text": "2025 年度报告", "x": 1, "y": 2, "w": 11, "fontSize": 40, "color": "1F1F1F"},
        {"type": "shape", "shapeType": "Ellipse", "x": 10, "y": 5, "w": 2, "h": 1.5, "fillColor": "4A90D9", "noLine": true},
        {"type": "text", "text": "底部居中备注", "edge": "bottom/left", "w": 8, "fontSize": 14, "color": "999999"}
      ],
      "notes": "封面页用 flexible blocks 排版"
    },
    {"title": "关键成果", "body": "营收 120 万\n用户 1.2 万", "notes": "逐项讲解"}
  ]
}
```

### 2. organize_deck（整理演示稿）

| 参数 | 说明 |
|------|------|
| `deleteSlides` | 删除页索引列表（1基，内部自动补偿偏移并从大到小删除） |
| `duplicateSlides` | 复制页 `[{slideIndex\|from+to, count=1, insertAfter}]`（insertAfter=副本插入到指定页之后，支持连续范围） |
| `moveSlides` | 移动页 `[{slideIndex\|from+to, insertAfter}]`（把页移动到指定页之后） |
| `applyTemplates` | 应用布局模板 `[{slideIndex, masterIndex=0, layoutIndex}]` |

> 可用 `PowerPoint_get_slide_layouts` 发现有效的 (masterIndex, layoutIndex) 组合。

> **插入空白页**：`organize_deck` 本身没有独立的「新增页」参数，插入空白页统一走
> `generate_deck` 的 `layout="Blank"` 实现——单页 `generate_deck`（`slides` 含一项
> `layout="Blank"`）即可在指定 `startPosition` 插入一个空白页（默认追加到末尾）。
> 需要「追加空白页」时，呼起 `generate_deck` 传 `{"slides":[{"layout":"Blank"}]}` 即可；
> 若需插入到指定位置，配合 `startPosition`（1基）。

**调用示例**：
```json
{
  "deleteSlides": [5, 2],
  "duplicateSlides": [{"slideIndex": 1, "count": 1}],
  "applyTemplates": [{"slideIndex": 3, "masterIndex": 0, "layoutIndex": 1}]
}
```

### 3. edit_selection（选区编辑）

参数 `edits` 数组，每项：`slideIndex`(1基,0=当前页) / `shapeId`(0=自动找第一个文本形状) /
`text` / `append`(默认false) / `fillColor`(RRGGBB) / `x`/`y`/`w`/`h`(英寸) / `noLine` / `notes`(该页备注)

**调用示例**：
```json
{
  "edits": [
    {"slideIndex": 1, "shapeId": 0, "text": "更新后的标题", "append": false, "fillColor": "1F1F1F"}
  ]
}
```

> 幻灯片标准尺寸 13.333"×7.5"（16:9），坐标单位为英寸，颜色为 "RRGGBB"。

---

## 使用方式

agent 识别到对应 Trigger 关键词（由 `fuxin-office` 路由）后，按以下流程执行：

1. 确定使用的场景工具（三选一）
2. 预检 PowerPoint 链路（调用 `PowerPoint_get_path`；完整预检见 `bridge.md`）；
   预检失败按 `bridge.md` 文案提示，**禁止执行写操作**
3. **跨产品写前闸门**：若命中 `../SKILL.md`「五·一、跨产品写前闸门」（本产品非当前活跃 / 首次写），先按标准话术提示切换到 PowerPoint 窗口并等待口令，未通过前**不调用写工具**
4. 建立 MCP 会话（initialize → notifications/initialized）
5. 按上方参数表组装参数，一次调用场景工具；**每次调用都须在参数顶层携带埋点字段**：
   - `skill_id`：本技能标识，固定填 `fuxin-ppt`
   - `scenario_id`：本次使用的场景编号，`generate_deck` 填 `UC-PPT-S1`、`organize_deck` 填 `UC-PPT-S2`、`edit_selection` 填 `UC-PPT-S3`
   （网关据此关联到具体 Skill/场景用于调用统计；传入即回显，不传则不回显）
6. 需要验证结果时调用只读工具（`PowerPoint_get_document_info` / `PowerPoint_get_ppt_outline`）读取内容
7. 向用户报告执行结果（成功数、失败数、生成内容摘要）
8. 不写前二次确认；写成功后按 `../SKILL.md` 汇总层 4.2 输出固定写后撤销提示（危险操作仍弹确认框）；失败/取消按 `bridge.md`「错误 / 异常（统一展示）」文案输出。**保存操作例外**：调用 `PowerPoint_save_document` / `PowerPoint_save_document_as`（保存属不可逆、无撤销）前，先输出 `bridge.md` 「保存确认提示」并等待用户选择，用户确认后才保存调用，取消则中止（取消/超时文案见「错误 / 异常（统一展示）」）

### 与其它编排规约协同

- **预检**：完整五层预检见 `bridge.md`
- **批次撤销**：写操作默认由网关合并为单事务；如需显式批次见 `batch-undo.md`
- **文档问答**：对演示稿内容提问见 `doc-qa.md`
- **跨产品**：Word→Excel→PPT 跨应用分步执行，见 `../SKILL.md`（E2E 分步编排）