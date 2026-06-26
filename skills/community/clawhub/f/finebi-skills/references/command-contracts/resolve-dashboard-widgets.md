# resolve-dashboard-widgets

## 用途

获取某个仪表板中所有可取数组件的 `widgetId`、组件展示名称和组件类型。

这个命令用于替代 agent 手工解析完整 `designConfigure.reportWidgets` 的过程。

不要为了整体看板分析、看板总结、日报、周报或经营概览主动调用这个命令。

## CLI

```bash
finebi-cli resolve-dashboard-widgets -d <dashboardId>
```

## 输入契约

- `dashboardId`：已解析出的仪表板 id

## 返回契约

返回 `ToolResult<ResolvedDashboardWidgetsData>`。

成功时类似：

```json
{
  "success": true,
  "data": {
    "dashboardId": "dashboard-id",
    "dashboardName": "经营看板",
    "widgets": [
      {
        "widgetId": "widget-key",
        "name": "销售额趋势",
        "title": "销售额趋势",
        "realWidgetId": "real-widget-id",
        "type": 1
      }
    ]
  }
}
```

## 重要字段

- `widgets[].widgetId`：后续传给 `get-widget-data -w` 的组件 id
- `widgets[].name`：组件展示名称
- `widgets[].title`：组件展示名称别名，方便按标题语义匹配
- `widgets[].type`：组件类型；当前返回列表只包含 `type = 1` 的可取数组件

## 常见后续链路

1. 先按 `dashboard-id-resolution-flow.md` 获取 `dashboardId`
2. 调用 `resolve-dashboard-widgets -d <dashboardId>`
3. 根据用户问题匹配 `widgets[].name` 或 `widgets[].title`
4. 如果候选不唯一，展示 `widgetId` 和名称请用户确认
5. 调用 `get-widget-data -r <dashboardId> -w <widgetId>`

如果 `widgets` 为空：

- 不要写脚本、抓页面或猜接口继续找组件 id
- 整体分析场景回到 `export-dashboard-pdf`
- 组件精确取数场景说明没有可取数组件候选

## 应该做

- 优先使用这个命令列出组件候选
- 只在用户明确要求具体组件、图表或指标卡数据时使用
- 返回结果已经过滤为 `type = 1` 的可取数组件
- 把 `widgetId` 和组件展示名称一起展示给用户
- 在找不到唯一组件时先澄清
- 在返回空列表时停止组件取数链路

## 不要做

- 不要在整体看板分析场景主动列组件或取组件数据
- 不要让 agent 自写 JS、Python 或抓包逻辑解析组件 id
- 不要把组件名称直接当作 `widgetId`
- 不要对不在返回列表里的组件 id 调用 `get-widget-data`
