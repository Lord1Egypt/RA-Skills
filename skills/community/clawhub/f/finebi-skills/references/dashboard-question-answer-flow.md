# 看板问答取数黄金链路

## 目标

当用户围绕 FineBI 看板、图表、指标卡或组件提问时，使用固定 CLI 链路定位 `dashboardId`，优先导出 PDF 做整体分析；只有用户明确要求某个具体组件、图表或指标卡的数据时，再定位 `widgetId` 并用真实组件数据回答。

这个流程用于降低自由度，避免 agent 在找不到 id 时脱离 skill 自写脚本、抓页面或猜接口。

## 硬约束

- 只使用 `finebi-cli` 和本 skill references 中列出的命令链路。
- 禁止自写 JS、Python、浏览器自动化、抓包脚本或临时 HTTP 调用来查找 `dashboardId`、`widgetId` 或组件数据。
- 禁止把用户输入的看板名、组件名或页面文案直接当成 id。
- 禁止在 CLI 链路失败后自建替代链路。
- 如果 CLI 能力不足，明确说明“缺少 CLI 能力”，不要继续绕路。

## 固定链路

```text
用户问题
-> 判断是否需要看板或组件真实数据
-> 读取 dashboard-id-resolution-flow.md
-> 只用 CLI 解析 dashboardId
-> 如果是整体仪表板分析，优先 export-dashboard-pdf 和 export-dashboard-excel
-> 只有明确要求具体组件数据时，才读取 dashboard-widget-data-flow.md
-> resolve-dashboard-widgets
-> 从 widgets 选择 widgetId
-> get-widget-data
-> 基于 PDF 或真实组件数据回答
```

## 第 1 步：判断是否需要看板数据

当用户问到以下内容时，通常需要走本流程：

- 某个看板里的指标、图表、表格或指标卡
- 某个组件背后的真实数据
- 某个经营问题需要从看板数据回答
- 需要解释趋势、排名、异常、占比或明细

如果只是询问 skill 能力或配置方式，不需要取数。

## 第 2 步：解析 dashboardId

读取并执行：

- `dashboard-id-resolution-flow.md`

允许使用的命令链路只有：

```text
第一优先级: 挂出目录或已发布入口
get-entry-tree -k <keyword>
-> get-published-subject-resources
-> dashboardId

第二优先级: 我的分析
search-my-dashboards
-> reportId
```

默认先查挂出目录；没有唯一命中时，再查“我的分析”。
调用 `get-entry-tree` 时，应优先从用户问题提取关键词并带 `-k`，避免拉取过大的目录树。

如果找不到唯一 `dashboardId`：

- 有候选时，展示候选并请用户确认。
- 没有候选时，询问用户看板来源或更准确的看板名。
- 不要写脚本继续搜索。

## 第 3 步：整体分析优先导出EXCEL

当用户意图是整体仪表板分析时，优先导出EXCEL再分析。

适用场景：

- 分析整个看板
- 生成日报、周报或经营分析
- 总结看板核心信息
- 识别整体趋势、异常、风险
- 用户没有明确指定某个组件、图表或指标卡

调用：

```bash
finebi-cli export-dashboard-excel -r <dashboardId>
```

规则：

- 整体看板分析和报告场景优先使用 EXCEL，因为 EXCEL 中按sheet导出来看板中所有组件的精确数据。
- 如果需要快速分析，或者需要仪表板快照，使用 PDF，因为 PDF 保留布局、标题、图表上下文和视觉关系
- 如果用户需要整体仪表板所有组件的精确数据，可以调用 `export-dashboard-excel`，不要改成逐个组件主动取数。
- Excel 导出结果中，每个 sheet 对应一个组件，sheet 名就是组件显示名。
- Excel 文件名、sheet 名、组件显示名和内容可能包含中文；读取 `.xlsx` 时使用 Excel 解析库并原样保留中文名称，不要按文本或 CSV 编码方式读取。
- 不要在整体分析场景一开始就逐个猜 `widgetId`。
- 不要为了补充整体看板数据而主动调用 `resolve-dashboard-widgets` 或 `get-widget-data`。
- 如果 PDF 已足够回答，就直接基于 PDF 输出分析。
- 如果 PDF 中的数值不够精确，先说明精度限制；详细数据或整体仪表板所有组件精确数据走 Excel，只有用户明确要求某个具体组件、图表或指标卡的数据时，再进入下一步解析 `widgetId`。
- 如果 PDF 导出失败，明确说明导出失败和错误；不要伪造 PDF 内容。

固定链路：

```text
整体仪表板分析
-> dashboardId
-> export-dashboard-excel
-> 基于 excel 进行整体分析
-> 如需贴近视觉效果的展示或者保留快照，导出 PDF
-> 如需具体组件数据，等待用户明确指定后再进入组件取数链路
```

## 第 4 步：组件级问题再解析 widgetId

只有用户明确要求某个具体组件、图表、表格或指标卡的数据时，才执行本步骤。

不要因为“整体看板数据”“整体分析”“总结看板”这类需求而主动解析组件列表。

读取并执行：

- `dashboard-widget-data-flow.md`

必须先调用：

```bash
finebi-cli resolve-dashboard-widgets -d <dashboardId>
```

然后只从 `widgets` 中选择组件：

- 使用 `widgets[].widgetId` 作为 `widgetId`
- 只选择 `type = 1` 的可取数组件
- 使用 `name`、`title` 或位置线索和用户问题匹配

如果找不到唯一 `widgetId`：

- 展示可取数组件候选，包含组件标题和组件 id。
- 请用户确认目标组件。
- 不要写脚本扫描页面或猜组件 id。

如果 `widgets` 为空：

- 说明当前 CLI 没有解析到可取数组件。
- 整体分析场景回到 PDF 结果回答。
- 精确组件数据场景停止并说明缺少可取数组件候选，不要继续绕路。

## 第 5 步：获取组件数据

调用：

```bash
finebi-cli get-widget-data -r <dashboardId> -w <widgetId>
```

如果用户明确给出过滤或联动上下文，按 `dashboard-widget-data-flow.md` 把 `--filter` 或 `--linkage` 附加到同一次 `get-widget-data` 调用。

## 第 6 步：回答用户问题

回答必须基于 `export-dashboard-pdf` 或 `get-widget-data` 的真实返回。

应该说明：

- 使用的看板或候选来源
- 使用的 PDF 快照或组件
- 关键数据结论
- 仍缺少的数据或需要用户确认的点

不要伪造：

- 指标值
- 趋势
- 组件 id
- 刷新时间
- 查询成功结果

## 失败分支

### 找不到 dashboardId

```text
停止
-> 展示候选或询问看板来源
-> 不写脚本
```

### 找不到 widgetId

```text
停止
-> 展示可取数组件候选
-> 请用户确认
-> 不写脚本
```

### PDF 导出失败

```text
停止
-> 说明 export-dashboard-pdf 的错误
-> 如用户明确需要具体组件数据，再询问是否改走组件取数链路
-> 不伪造 PDF 内容
```

### CLI 命令报错

```text
停止
-> 说明执行的 CLI 命令和错误
-> 不写脚本绕过
```

### CLI 缺少能力

```text
停止
-> 说明缺少 CLI 能力
-> 建议补 CLI 能力
-> 不自建临时代码链路
```

## 简写版本

```text
问题
-> dashboardId: dashboard-id-resolution-flow
-> 整体分析: export-dashboard-pdf -> PDF 分析
-> 明确具体组件数据: resolve-dashboard-widgets -> get-widget-data
-> 基于 PDF 或真实组件数据回答

任一步失败
-> 澄清或报告缺少 CLI 能力
-> 禁止写 JS/Python/浏览器自动化/抓包绕路
```
