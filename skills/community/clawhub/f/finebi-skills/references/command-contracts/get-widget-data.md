# get-widget-data

## 用途

获取某个仪表板组件的真实数据载荷。

只有在已经明确以下两件事之后，才应该调用这个命令：

- `dashboardId`
- 通过 `resolve-dashboard-widgets` 解析出的可取数组件 `widgetId`

不要为了整体看板分析、看板总结、日报、周报或经营概览主动调用这个命令。

## CLI

基础调用：

```bash
finebi-cli get-widget-data -r <reportId> -w <widgetId>
```

可选地，在同一次 SDK 生命周期里先应用过滤或联动：

```bash
finebi-cli get-widget-data -r <reportId> -w <widgetId> --filter '<json>'
finebi-cli get-widget-data -r <reportId> -w <widgetId> --linkage '<json>'
```

## 输入契约

- `reportId`：仪表板 id
- `widgetId`：来自 `resolve-dashboard-widgets` 返回的 `widgets[].widgetId`
- `filter`：可选，在取数前先应用一次过滤条件
- `linkage`：可选，在取数前先应用一次联动状态，必须包含 `widgetId` 和 `payload`

### `filter` 结构

`--filter` 的 JSON 直接透传给 SDK 的 `filter.applyFilter(...)`。

示例：

```json
{
  "widgetId": "filterWidget",
  "value": {
    "type": 1,
    "value": ["华东"]
  }
}
```

### `linkage` 结构

`--linkage` 的 JSON 结构如下：

```json
{
  "widgetId": "sourceWidget",
  "payload": {
    "dId": "area",
    "fieldId": "field1",
    "text": "华东",
    "value": [
      {
        "dId": "area",
        "fieldId": "field1",
        "text": "华东"
      }
    ]
  }
}
```

## 必要前置查询

调用该命令前，必须先调用：

```bash
finebi-cli resolve-dashboard-widgets -d <dashboardId>
```

然后检查：

- `widgets`

`widgets` 是可取数组件数组：

- 每个 `widgets[].widgetId` 是后续传给 `get-widget-data -w` 的组件 id
- 每个 `widgets[].name` 或 `widgets[].title` 是组件展示名称
- 返回结果已经过滤为 `type = 1` 的可取数组件

只有需要完整配置细节时，才额外调用：

```bash
finebi-cli get-dashboard-design-configure -d <dashboardId>
```

## 重要组件语义

- `type = 1`：可取数的数据组件
- `resolve-dashboard-widgets` 已过滤掉不可取数组件
- 过滤控件不能作为 `get-widget-data` 的目标

## 返回契约

返回 `ToolResult<any>`，其中 `data` 为 FineBI 查询 SDK 返回的原始组件数据。

具体载荷会随组件类型和 FineBI 版本变化。

## 语义说明

- 不要猜测组件 id
- 不要自己解析完整 `designConfigure.reportWidgets` 来找组件 id
- `widgetId` 来自 `resolve-dashboard-widgets` 的 `widgets[].widgetId`
- 如果要模拟用户先过滤、再联动、再取数，可以把 `--filter` 和 `--linkage` 放到同一次命令里

## 常见后续链路

1. 确认 `dashboardId`
2. 调用 `resolve-dashboard-widgets`
3. 根据 `widgets[].name` 或 `widgets[].title` 匹配目标组件
4. 使用 `widgets[].widgetId` 作为 `widgetId`
5. 调用 `get-widget-data -r <reportId> -w <widgetId>`

如果用户已经明确给出了过滤条件或联动上下文，可在同一次命令里附加：

- `--filter '<json>'`
- `--linkage '<json>'`

## 应该做

- 在 `get-widget-data` 前先调用 `resolve-dashboard-widgets`
- 在推理过程中同时保留组件标题和组件 id
- 找不到唯一组件时，展示候选并请用户确认

## 不要做

- 不要用过滤控件 id 调用 `get-widget-data`
- 不要把组件名或图表标题直接当成 `widgetId`
- 如果还不知道组件 id，就不要跳过 `resolve-dashboard-widgets`
