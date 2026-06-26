# dimens-manager 画布生成校验清单

## 1. 目标

画布生成完成后，不能只看“JSON 能解析”或“命令返回 success”。必须确认这份数据能被前端渲染、能被保存为版本、能被再次读取，并且业务语义没有丢失。

固定校验链：

```text
生成 canvas.json
-> canvas validate --file ./canvas.json
-> canvas create 或 canvas save
-> canvas info
-> canvas versions
-> 必要时 canvas version 回查快照
```

如果任一步不通过，不能说“画布生成完成”。

## 2. 本地结构校验

保存前必须先执行：

```bash
dimens-cli canvas validate --file ./workflow-canvas.json
```

或：

```bash
dimens-cli canvas validate --data '<json>'
```

校验通过至少说明：

- 顶层 `nodes` 和 `edges` 是数组。
- 节点有稳定 `id`，且不重复。
- 节点 `type` 属于前端支持范围。
- 节点包含可渲染尺寸和坐标字段。
- 边的 `source/target` 都能找到节点。
- 边包含 handle、箭头和线条样式。
- 判断节点 `DIAMOND` 至少有两条出边，且分支边有 label。
- `INFOGRAPHIC`、`EMBEDDED_SHEET` 等特殊节点包含必要数据。
- 节点背景色是淡色或 `transparent`，不会出现黑色 / 深色背景。

## 3. 节点校验

每个节点必须满足：

| 字段 | 要求 |
| --- | --- |
| `id` | 非空、唯一、稳定英文短名 |
| `type` | 使用支持的节点类型，不发明新类型 |
| `position.x/y` | 数值 |
| `positionAbsolute.x/y` | 数值 |
| `width/height` | 正数 |
| `style.width/height` | 与顶层 `width/height` 一致 |
| `selected/dragging` | 布尔值，保存型 JSON 默认 `false` |
| `data.label` | 非空业务含义 |
| `data.backgroundColor` | 只能是淡色十六进制颜色或 `transparent` |
| `data.width/height` | 与顶层 `width/height` 一致 |
| `data.align` | `left / center / right` |
| `data.verticalAlign` | `top / center / bottom` |

背景色推荐：

| 用途 | 推荐值 |
| --- | --- |
| 默认节点 | `#ffffff`、`#f8fafc` |
| 输入 / 输出 | `#eff6ff`、`#eef2ff` |
| 判断 / 审批 | `#fff7ed`、`#fef3c7` |
| 成功 / 通过 | `#ecfdf5`、`#dcfce7` |
| 提醒 / 风险 | `#fefce8`、`#fff7ed` |
| 文档 / 说明 | `#ffffff`、`#f8fafc` |

禁止把下面颜色作为节点背景：

- `#000000`
- `#111111`
- `#111827`
- `#1f2937`
- `#0f172a`
- 其他接近黑色或高饱和深色的背景

如果需要强调节点，优先使用边框色、图标、标签、连线色或 `INFOGRAPHIC` 主题色，不要把整个节点背景改成深色。

特殊节点额外要求：

| 节点类型 | 额外要求 |
| --- | --- |
| `DIAMOND` | 至少两条出边，所有出边必须有分支 label |
| `INFOGRAPHIC` | `data.infographicSyntax` 必须以 `infographic <template-name>` 开头 |
| `MARKDOWN` | 建议提供 `data.markdownContent` |
| `EMBEDDED_SHEET` | 必须提供真实 `data.embeddedSheet.sheetId/viewId` |
| PPT 页 `SECTION` | 推荐 `1280 x 720`，比例必须是 `16:9` |
| PPT 内容节点 | 必须有 `parentNode` 指向页面 `SECTION`，且不能超出页面范围 |

## 4. 边校验

每条边必须满足：

| 字段 | 要求 |
| --- | --- |
| `id` | 非空 |
| `source` | 存在于节点 id 集合 |
| `target` | 存在于节点 id 集合 |
| `sourceHandle` | 非空，例如 `source-bottom` |
| `targetHandle` | 非空，例如 `target-top` |
| `type` | `default` 或 `smoothstep` |
| `animated` | 布尔值 |
| `selected` | 布尔值 |
| `zIndex` | 数值 |
| `markerEnd.type` | `arrowclosed` |
| `style.stroke` | 非空颜色 |
| `style.strokeWidth` | 正数 |

判断节点的出边必须写 `label`，例如：

- `是 / 否`
- `通过 / 驳回`
- `命中 / 未命中`
- `自动处理 / 人工处理`

## 5. 业务语义校验

结构校验通过不代表业务可读。生成后还要人工或 AI 自检：

- 每个节点只表达一个业务动作。
- `data.label` 是“动词 + 对象”或明确判断条件，不是“步骤 1 / 节点 A”。
- 主流程能看出起点、过程、终点。
- 异常路径能看出拒绝、退回、撤回、超时、转交或人工兜底。
- 数据沉淀节点能说明写入哪张表、哪个状态或哪个摘要。
- 文档节点能说明生成什么报告、合同、SOP 或知识条目。
- 画布里如果引用真实表格视图，不能虚构 `sheetId/viewId`。
- 审批工作流画布必须明确“这只是画布”，可执行审批仍要进入工作流章节。

## 6. 保存后回查

新建画布：

```bash
dimens-cli canvas create \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --name 业务流程画布 \
  --file ./workflow-canvas.json

dimens-cli canvas info SHEET_ID \
  --team-id TEAM_ID \
  --project-id PROJECT_ID

dimens-cli canvas versions SHEET_ID \
  --team-id TEAM_ID \
  --project-id PROJECT_ID
```

更新已有画布：

```bash
dimens-cli canvas info SHEET_ID \
  --team-id TEAM_ID \
  --project-id PROJECT_ID

dimens-cli canvas validate --file ./workflow-canvas.json

dimens-cli canvas save SHEET_ID \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --base-version VERSION \
  --file ./workflow-canvas.json \
  --summary AI生成业务画布

dimens-cli canvas info SHEET_ID \
  --team-id TEAM_ID \
  --project-id PROJECT_ID

dimens-cli canvas versions SHEET_ID \
  --team-id TEAM_ID \
  --project-id PROJECT_ID
```

必要时读取指定版本快照：

```bash
dimens-cli canvas version SHEET_ID \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --version VERSION
```

## 7. 完成判定

只有同时满足下面条件，才能说画布生成完成：

- `canvas validate` 通过。
- `canvas create` 或 `canvas save` 成功。
- `canvas info` 能读到目标画布和最新版本号。
- `canvas versions` 能看到版本记录。
- 如果是更新任务，保存后的版本号大于保存前版本号。
- 如果是 PPT 画布，每页都有 `SECTION`，内容节点都在页面内。
- 如果是业务流程画布，主路径、异常路径、数据沉淀都能读懂。
- 如果是审批画布，能看出发起、审批、通过、驳回、撤回、回写。

## 8. 常见不合格数据

| 问题 | 后果 | 修正 |
| --- | --- | --- |
| 节点只有 `id/type/position/data.label` | 前端可能不可见、尺寸丢失、拖拽异常 | 补齐可渲染字段模板 |
| 节点背景是黑色或深色 | 文字不可读，视觉压迫，和画布风格不一致 | 改成浅色背景，深色文字 |
| 边只有 `source/target` | 无箭头、无 handle、分支不可读 | 补 `sourceHandle/targetHandle/markerEnd/style` |
| `DIAMOND` 只有一条出边 | 判断节点没有业务意义 | 至少补两条分支边 |
| 分支边没有 label | 用户不知道条件结果 | 写“是/否/通过/驳回” |
| `INFOGRAPHIC` 没有 DSL | 信息图无法渲染 | 补 `data.infographicSyntax` |
| PPT 内容没有 `parentNode` | 页面内容散落在无限画布 | 挂到对应 `SECTION` |
| 引用虚构 `sheetId/viewId` | 嵌入表格不可用 | 先查询真实表格和视图 ID |
| 保存后不回查版本 | 无法确认写入成功 | 补 `canvas info/versions` |
