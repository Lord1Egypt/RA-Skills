# 参考文档：fuxin-word — Word 文档编排规约

> **收敛说明**：本文档为 `fuxin-office` 唯一入口技能**内部参考文档**，承载「Word 文档编排」规约，
> **不作独立技能对外暴露**（无 frontmatter / Trigger / description）。由 `fuxin-office` 按需读取，
> 企业若需独立技能形式可另行封装。
>
> **产品分类**: `Word`
> **依赖**: FuxinAiService（端口见 `bridge.md`「运行端口」，由 `MCPServerPort.ini` 读取）+ Word 产品场景工具
> **需要确认**: 是（写操作；不写前二次确认，写后提示撤销；**保存操作 save_document/save_document_as 例外，需提前确认**——见 `../SKILL.md` 4.2）

---

## 功能概述

本规约通过 MCP 网关**直接调用 Word 产品的场景工具**（场景工具已在网关内部实现，
agent 只需传参直接调用，无需手动编排原子技能、管理会话或处理批次事务）。
覆盖 4 类文档编排任务：

1. **写报告** — 自动生成含标题、章节正文、表格、图片的文档，可选目录
2. **统一术语排版** — 批量查找替换 + 可选全文格式统一
3. **选区高亮批注** — 查找文本 → 高亮 → 添加批注
4. **清单审查** — 对清单项添加批注和/或插入汇总表

所有写操作由网关内部合并为事务，用户可**一次 Ctrl+Z 整组撤销**；
若需显式管理批次，见 `batch-undo.md`。

---

## 架构

```
用户 (VS Code Copilot)
    │ MCP 协议 (tools/call)
    ▼
FuxinAiService（端口见 `bridge.md`「运行端口」）
    │ 转发到 Word 产品
    ▼
fuxin-word 场景工具（网关内部实现）
    │
    ▼
FuxinOfficeWord App (Office 进程)
```

---

## 前置条件

1. **FuxinAiService 已启动**（端口由 `MCPServerPort.ini` 读取，见 `bridge.md`「运行端口」）
2. **Word 产品已注册**（产品名 `Word`），FuxinOfficeWord 应用已启动、插件已加载
3. **已打开一个活动文档**（所有工具都会修改文档内容）

### 预检

执行任何写操作前必须预检，完整预检流程见 `bridge.md`。本规约快速探活：

- 调用 `Word_get_document_info` / `Word_get_doc_status` 探活：成功且有活动文档 → 就绪
- 未安装 / 未就绪（网关不可达、产品未启动、插件未加载）/ 半就绪（无活动文档）/ 就绪，
  统一按 `bridge.md` 定稿文案逐字输出，**禁止**自行发明或改动文案

> 预检全程只读，禁止任何写入操作。预检失败时按 `bridge.md` 文案提示，禁止执行写操作。

### 场景收尾

> **三档区分**，按操作粒度输出，不可互相替代：
> - **单次操作成功**：单步操作完成 → `已在文档中完成「{操作名}」。请在福昕Office 中查看效果。`
> - **一组操作完成**：同一场景内多步/批量成组完成 → `本组修改已完成。如需撤销，请在福昕Office 中按一次「撤销」即可恢复整组操作。`
>
>     （若为该组写操作，还应追加写后撤销提示。）
> - **场景任务完成**：整个场景完全执行完毕后 → 输出下方定稿场景收尾文案。

每个场景工具执行完成后，若该场景已整体结束，按 `../SKILL.md` 汇总层「五、用户提示文案总则」对齐定稿输出统一收尾，**中途的单次/一组操作不提前输出场景完成文案**：

> `「{场景名}」已执行完毕。请检查文档是否符合预期。`

`{场景名}` 取本规约对应场景中文名（写报告 / 术语统一与排版 / 高亮批注 / 清单审查）。

写操作场景在收尾后追加固定撤销提示：

> 改好了。要撤回改动：回复「撤销」，或在福昕Office 按 Ctrl+Z。

---

## 工具列表

### 1. write_report（写报告）

| 参数 | 必填 | 说明 |
|------|------|------|
| `title` | ✅ | 报告标题 |
| `sections` | ✅ | 章节列表：`heading`、`level`(1-3)、`content`(简单模式) 或 `blocks`(高级模式)、`pageBreakBefore` |
| `blocks` | ❌ | 内容块：`text` / `table`(headers/rows/caption) / `image`(path) / `pageBreak` |
| `format` | ❌ | 全局格式：fontName、各级字号、bodyAlignment(0左/1中/2右/3两端)、firstLineIndent、lineSpacing(240/360/480) |
| `includeToc` / `tocMaxLevel` | ❌ | 目录开关（默认 false）/ 最大级别（默认 3） |

**调用示例**：
```json
{
  "title": "2026年第三季度项目总结报告",
  "includeToc": true,
  "sections": [
    {"heading": "一、总体概述", "level": 1, "content": "本季度进展顺利。"},
    {"heading": "二、关键数据", "level": 1, "blocks": [
      {"type": "table", "caption": "季度关键指标",
       "headers": ["指标", "目标", "实际"],
       "rows": [["营收", "100万", "120万"]]}
    ]}
  ]
}
```

### 2. unify_terminology（术语统一/排版整理）

| 参数 | 必填 | 说明 |
|------|------|------|
| `replacements` | ✅ | `[{find, replace, matchCase?, wholeWord?}]` |
| `applyFormat` / `format` | ❌ | 是否统一全文排版（默认 false）/ fontName、fontSize、lineSpacing、alignment |

**调用示例**：
```json
{
  "replacements": [{"find": "OFfice", "replace": "Office", "matchCase": true}],
  "applyFormat": true,
  "format": {"fontName": "宋体", "fontSize": 12, "lineSpacing": 360, "alignment": 3}
}
```

### 3. highlight_and_comment（高亮批注）

- 简单模式：`target` + `highlightColor` + `commentText` + `findAll`（默认 true）
- 高级模式：`targets: [{text, highlightColor?, commentText?, bold?, matchCase?, wholeWord?, findAll?}]`
- `commentAuthor` 默认 "AI助手"；不传 `commentText` 则仅高亮；`highlightColor=-1` 不高亮

**调用示例**：
```json
{
  "targets": [
    {"text": "AI001", "highlightColor": 1, "commentText": "请核对编号", "findAll": true},
    {"text": "合同", "highlightColor": 4}
  ],
  "commentAuthor": "审查助手"
}
```

### 4. checklist_review（清单审查）

| 参数 | 必填 | 说明 |
|------|------|------|
| `checklist` | ✅ | `[{item, status?, note?, …自定义字段}]` |
| `mode` | ❌ | `comment` / `summary_table`(默认) / `both` |
| `columns` | ❌ | 汇总表自定义列 `[{key, title}]`，默认三列 |
| `summaryTitle` / `highlightFound` / `highlightColor` | ❌ | 汇总标题 / 是否高亮命中项（默认 false）/ 颜色（默认 1 绿） |

**调用示例**：
```json
{
  "checklist": [
    {"item": "营业执照", "status": "已提供", "note": "在有效期内"},
    {"item": "资质证书", "status": "待补充"}
  ],
  "mode": "both",
  "summaryTitle": "文件清单审查汇总"
}
```

### 高亮颜色索引

-1=无 0=黄 1=绿 2=青 3=粉 4=蓝 5=红 6=深蓝 7=青绿 8=深绿 9=紫 10=深红 11=橄榄黄 12=灰 13=浅灰 14=黑

---

## 使用方式

agent 识别到对应 Trigger 关键词（由 `fuxin-office` 路由）后，按以下流程执行：

1. 确定使用的场景工具（四选一）
2. 预检 Word 链路（调用 `Word_get_path`；完整预检见 `bridge.md`）；
   预检失败按 `bridge.md` 文案提示，**禁止执行写操作**
3. **跨产品写前闸门**：若命中 `../SKILL.md`「五·一、跨产品写前闸门」（本产品非当前活跃 / 首次写），先按标准话术提示切换到 Word 窗口并等待口令，未通过前**不调用写工具**
4. 建立 MCP 会话（initialize → notifications/initialized）
5. 按上方参数表组装参数，一次调用场景工具；**每次调用都须在参数顶层携带埋点字段**：
   - `skill_id`：本技能标识，固定填 `fuxin-word`
   - `scenario_id`：本次使用的场景编号，`write_report` 填 `UC-WORD-S1`、`unify_terminology` 填 `UC-WORD-S2`、`highlight_and_comment` 填 `UC-WORD-S3`、`checklist_review` 填 `UC-WORD-S4`
   （网关据此关联到具体 Skill/场景用于调用统计；传入即回显，不传则不回显）
6. 需要验证结果时调用只读工具（`Word_get_doc_status` / `Word_get_document_text`）读取文档内容
7. 向用户报告执行结果（成功数、失败数、生成内容摘要）；若工具返回 `ok:false` 且为参数类错误（如 `sections不能为空`、`title不能为空`、缺 items/rows 等），**不得回显原始 error**，按 `bridge.md`「参数有误」定稿文案提示
8. 写成功后，按 `../SKILL.md` 汇总层 4.2 输出**写后撤销提示**（改好了。要撤回改动：回复「撤销」，或在福昕Office 按 Ctrl+Z。）；失败/取消按 `bridge.md`「错误 / 异常（统一展示）」文案输出。危险操作（删除页/清空/批量覆盖）仍按产品要求弹确认对话框后再执行。**保存操作例外**：调用 `Word_save_document` / `Word_save_document_as`（保存属不可逆、无撤销）前，先输出 `bridge.md` 「保存确认提示」并等待用户选择，用户确认后才真正保存，取消则不保存（取消/超时文案见「错误 / 异常（统一展示）」）

### 与其它编排规约协同

- **预检**：完整五层预检见 `bridge.md`
- **批次撤销**：写操作默认由网关合并为单事务；如需显式 begin/end/undo 批次见 `batch-undo.md`
- **文档问答**：对已生成的文档内容提问见 `doc-qa.md`
- **跨产品**：Word→Excel→PPT 跨应用分步执行，见 `../SKILL.md`（E2E 分步编排）