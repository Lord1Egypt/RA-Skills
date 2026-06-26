# 仪表板组件取数流程

## 目标

从一个仪表板中获取一个或多个可取数组件的真实数据。

这个流程只用于用户明确要求某个具体组件、图表、表格、指标卡的数据，或者明确要求结合过滤/联动状态查看某个组件结果的场景。

## 适用场景

当用户提出以下需求时使用：

- 查看某个看板组件背后的真实数据
- 获取图表数据
- 获取表格组件数据
- 查看某个指标卡的数值
- 在指定过滤条件或联动上下文下取数组件

不要在整体看板分析、看板总结、日报、周报或经营概览场景主动进入本流程。

## 必要命令

- `resolve-dashboard-widgets`
- `get-widget-data`

## 可选辅助命令

- `get-dashboard-design-configure`：仅当需要完整配置细节时使用，不作为组件 id 解析的默认链路。

## 流程

### 第 1 步：先拿到 dashboard id

先确保已经知道 `dashboardId`。

它可能来自：

- 已发布资源流程
- `search-my-dashboards`
- `get-dashboards-by-subject`

### 第 2 步：优先解析组件清单

调用：

```bash
finebi-cli resolve-dashboard-widgets -d <dashboardId>
```

响应信息包括 `dashboardId`、`dashboardName` 和 `widgets`。

重点关注：

- `widgets[].widgetId`
- `widgets[].name`
- `widgets[].title`
- `widgets[].type`

### 第 3 步：检查组件清单

`resolve-dashboard-widgets` 已经把可取数组件整理成数组：

- `widgetId` 是后续 `get-widget-data` 使用的组件 id
- `name` 和 `title` 是组件展示名称

关键字段：

- `type = 1`：可取数的数据组件

如果需要完整配置细节，再调用：

```bash
finebi-cli get-dashboard-design-configure -d <dashboardId>
```

### 第 4 步：选择目标组件

当用户要看真实组件数据时：

- 只能选择 `type = 1` 的组件

如果有多个组件都可能符合：

- 展示 `widgetId`、`name` 或 `title`
- 必要时请用户确认

如果 `widgets` 为空：

- 说明该仪表板没有可通过 CLI 取数的组件，或当前账号无权限读取组件清单。
- 如果用户是在做整体分析，回到 PDF 链路。
- 如果用户需要组件精确数据，停止并说明缺少可取数组件，不要自写脚本继续找 id。

### 第 5 步：获取组件数据

基础调用：

```bash
finebi-cli get-widget-data -r <dashboardId> -w <widgetId>
```

如果用户明确给出了过滤条件或联动上下文，也可以在同一次命令里附加：

```bash
finebi-cli get-widget-data -r <dashboardId> -w <widgetId> --filter '<json>'
finebi-cli get-widget-data -r <dashboardId> -w <widgetId> --linkage '<json>'
```

这里：

- `reportId` 使用已知的 `dashboardId`
- `widgetId` 使用 `resolve-dashboard-widgets` 返回的 `widgets[].widgetId`
- `--filter` 和 `--linkage` 会在同一次 SDK 生命周期里先执行，再取目标组件数据

## 常见错误

### 错误 1：没解析组件清单就直接取数

不要猜测组件 id。

正确流程：

```text
先拿到 dashboard id
-> resolve-dashboard-widgets
-> 检查 widgets
-> 选择目标组件
-> get-widget-data
```

### 错误 2：继续手工解析完整配置

优先使用 `resolve-dashboard-widgets` 的扁平结果，不要让 agent 自己解析完整 `designConfigure`。

### 错误 3：对过滤控件取数

`type = 2` 的过滤控件不能作为 `get-widget-data` 的目标。

### 错误 4：把过滤或联动拆成另一条独立生命周期的命令

如果你想模拟“先过滤/联动，再取数”，应优先把 `--filter` 或 `--linkage` 直接附加到同一次 `get-widget-data` 调用里。

### 错误 5：组件清单为空后继续绕路

如果 `resolve-dashboard-widgets` 返回空列表，不要写脚本扫描页面或抓接口。应说明没有可取数组件候选，并根据用户目标回到 PDF 分析或请求补充信息。

## 推荐行为

1. 先确认 `dashboardId`
2. 确认用户已经明确指定某个组件、图表、表格或指标卡
3. 调用 `resolve-dashboard-widgets`
4. 确认返回组件均为 `type = 1` 的可取数组件
5. 保留组件 id 与标题，便于后续解释
6. 如果用户给了过滤条件或联动上下文，优先附加到同一次 `get-widget-data` 调用

## 简写版本

```text
先拿到 dashboard id
-> resolve-dashboard-widgets(dashboardId)
-> 检查 widgets
-> 选择目标组件
-> 如有需要，附加 filter/linkage
-> get-widget-data(reportId=dashboardId, widgetId=选中的 widgetId)
```
