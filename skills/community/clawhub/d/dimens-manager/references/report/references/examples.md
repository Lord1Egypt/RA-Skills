# dimens-manager 报表章节 接口案例

本文档聚焦维表智联当前已经落地的报表模块接口，按接口维度整理：

1. 报表列表 / 详情 / 增删改
2. 图表组件接口
3. 查询执行接口
4. 模板接口
5. 版本接口

当前 `dimens-cli` 已经封装了报表三条主链命令：

- `report list`
- `report info`
- `report create`
- `report update`
- `report copy`
- `report publish`
- `report delete`
- `report archive`
- `report validate`
- `report sort`
- `report move`
- `report query`
- `report query-widget`
- `report preview`
- `report widget-add`
- `report widget-update`
- `report widget-delete`
- `report widget-batch`
- `report widget-sort`

这里保留接口案例，是为了让 Skill 在解释“CLI 已支持什么、未支持什么”时能同时对齐后端真值与现有命令边界。

如果用户目标是“让 AI 一次生成一个可渲染的报表组件”，不要只给命令，还要联动 `recharts-widget-guide.md` 校验组件结构完整性，并按固定预检链推进：

`report create -> report preview -> report widget-add -> report query-widget -> report query`

更细的规则说明请分别查看：

- `usage.md`
- `capability-status.md`

---

## 1. 报表主资源接口

### 1.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/report/:projectId` |
| 入口角色 | 报表主资源入口 |

### 1.2 查询报表列表

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/report/:projectId/list` |
| 鉴权 | `Authorization: Bearer {token}` |

请求体：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `keyword` | `string` | 否 | 关键词 |
| `type` | `string` | 否 | 报表类型 |
| `status` | `number` | 否 | 状态 |
| `page` | `number` | 否 | 页码，默认 `1` |
| `size` | `number` | 否 | 每页条数，默认 `20` |

### 1.3 查询报表详情

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/report/:projectId/info?reportId=:reportId` |
| 鉴权 | `Authorization: Bearer {token}` |

查询参数：

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `reportId` | `string` | 是 |

返回重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.reportId` / `data.sheetId` | `string` | 报表 ID；项目菜单报表场景下二者通常是同一个值 |
| `data.projectId` | `string` | 所属项目 |
| `data.config` | `object` | 报表配置 |
| `data.widgets` | `array` | 组件列表 |
| `data.parameters` | `array` | 参数列表 |

### 1.4 新增报表

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/mul/project/:projectId/sheet/create` |

请求体重点：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | `string` | 是 | 报表名 |
| `type` | `string` | 是 | 固定为 `report` |
| `config.dashboardConfig` | `object` | 是 | 报表看板配置，至少包含 `id`、`title`、`widgets`、`parameters`、`createdAt` |

成功返回：

```json
{
  "code": 1000,
  "message": "success",
  "data": {
    "projectId": "PROJ1",
    "type": "report",
    "sheetId": "sh_xxx",
    "name": "销售漏斗"
  }
}
```

说明：服务端创建项目菜单报表时返回主键是 `sheetId`。CLI / SDK 为兼容报表命令，会把 `reportId` 归一化为同一个值，即 `reportId = sheetId`。不要按旧口径等待 `data.reportId`。

### 1.5 更新 / 删除 / 复制 / 发布 / 归档 / 排序 / 移动 / 校验

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/app/report/:projectId/update` | 更新报表 |
| `POST` | `/app/report/:projectId/delete` | 删除报表 |
| `POST` | `/app/report/:projectId/copy` | 复制报表 |
| `POST` | `/app/report/:projectId/publish` | 发布报表 |
| `POST` | `/app/report/:projectId/archive` | 归档报表 |
| `POST` | `/app/report/:projectId/sort` | 排序 |
| `POST` | `/app/report/:projectId/move` | 移动到其他项目 |
| `POST` | `/app/report/:projectId/validate` | 校验报表配置 |

Skill 在解释报表生命周期时，至少要把这些接口区分清楚，不要把“详情查询”和“发布/归档/校验”混成一个概念。

当前 CLI 已对齐的主资源命令示例：

```bash
dimens-cli report create --project-id PROJ1 --name "销售漏斗" --description "月度销售漏斗"

dimens-cli report update --project-id PROJ1 --report-id REPORT_1 --name "销售漏斗-更新"

dimens-cli report copy --project-id PROJ1 --report-id REPORT_1 --name "销售漏斗-副本"

dimens-cli report publish --project-id PROJ1 --report-id REPORT_1 --is-public true

dimens-cli report delete --project-id PROJ1 --report-id REPORT_1

dimens-cli report archive --project-id PROJ1 --report-id REPORT_1

dimens-cli report validate --project-id PROJ1 --config '{"widgets":[{"type":"line"}]}'

dimens-cli report sort --project-id PROJ1 --report-id REPORT_1 --target-index 2

dimens-cli report move --project-id PROJ1 --report-id REPORT_1 --target-project-id PROJ2
```

---

## 2. 图表组件接口

### 2.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/report/widget/:projectId` |
| 入口角色 | 图表组件入口 |

### 2.2 新增组件

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/report/widget/:projectId/add` |

请求体重点：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `reportId` | `string` | 是 | 报表 ID |
| `type` | `string` | 是 | 组件类型 |
| `title` | `string` | 否 | 组件标题 |
| `dataSource` | `object` | 是 | 数据源定义 |
| `layout` | `object` | 否 | 布局信息 |
| `dataMapping` | `object` | 否 | 字段映射 |
| `chartConfig` | `object` | 否 | 图表配置 |
| `orderNum` | `number` | 否 | 排序 |

成功返回：

```json
{
  "code": 1000,
  "message": "success",
  "data": {
    "widgetId": "widget_xxx"
  }
}
```

### 2.3 更新 / 删除 / 排序 / 批量覆盖

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/app/report/widget/:projectId/update` | 更新组件 |
| `POST` | `/app/report/widget/:projectId/delete` | 删除组件 |
| `POST` | `/app/report/widget/:projectId/sort` | 调整排序 |
| `POST` | `/app/report/widget/:projectId/batch` | 以 widgets 数组整批重建 |

`batch` 请求体重点：

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `reportId` | `string` | 是 |
| `widgets` | `array` | 是 |

Skill 在解释“组件为什么丢了”或“组件顺序为什么变了”时，必须知道存在 `batch` 这种整批覆盖写法。

当前 CLI 已对齐的组件命令示例：

```bash
dimens-cli report widget-add \
  --project-id PROJ1 \
  --report-id REPORT_1 \
  --type bar \
  --title "销售额" \
  --data-source '{"kind":"sheet","sheetId":"S1"}' \
  --layout '{"x":0,"y":0,"w":6,"h":4}'

dimens-cli report widget-update --project-id PROJ1 --widget-id widget_1 --title "销售额-更新"

dimens-cli report widget-delete --project-id PROJ1 --widget-id widget_1

dimens-cli report widget-batch --project-id PROJ1 --report-id REPORT_1 --widgets '[{"type":"line"}]'

dimens-cli report widget-sort --project-id PROJ1 --report-id REPORT_1 --widget-id widget_1 --target-order 3
```

### 2.4 多维表格报表组件成功案例

下面这个结构比“只有 `type + sheetId`”更接近真实可用写法：

```json
{
  "type": "line",
  "title": "销售趋势",
  "dataSource": {
    "mode": "sheet",
    "sheet": {
      "sheetId": "sh_x7HbTHMJ2nYfUHVM",
      "sheetName": "数据管理",
      "columns": [
        { "fieldId": "fld_2BsgRpRBh3Gz", "label": "名称", "type": "text" },
        { "fieldId": "fld_CU60W0OVXbEw", "label": "销售额", "type": "number" }
      ],
      "fieldIds": ["fld_2BsgRpRBh3Gz", "fld_CU60W0OVXbEw"],
      "recommendedMapping": {
        "nameKey": "name",
        "valueKey": "value"
      },
      "previewMapping": {
        "nameKey": "name",
        "valueKey": "value",
        "aggregation": "sum",
        "sort": {
          "key": "销售额",
          "order": "desc"
        },
        "limit": 5
      },
      "limit": 5
    }
  },
  "dataMapping": {
    "nameKey": "名称",
    "valueKey": "销售额",
    "limit": 5
  },
  "colSpan": 6,
  "height": 300,
  "showLegend": true,
  "showGrid": true,
  "showTooltip": true
}
```

这个案例的重点不是字段名本身，而是下面这几个层都要同时存在：

- 查询层的 `sheet.columns`
- 字段选择层的 `fieldIds`
- 规范映射层的 `recommendedMapping`
- 预览查询层的 `previewMapping`
- 前端渲染层的 `dataMapping`

---

## 3. 报表查询接口

### 3.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/report/query/:projectId` |
| 入口角色 | 报表查询入口 |

### 3.2 执行整个报表查询

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/report/query/:projectId` |

请求体：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `reportId` | `string` | 是 | 报表 ID |
| `parameterValues` | `object` | 否 | 参数值 |
| `widgetIds` | `string[]` | 否 | 仅查询指定组件 |

返回特点：

- 返回按 `widgetId` 聚合的结果
- 每个组件单独查询
- 查询日志会记录耗时、结果条数、成功/失败状态

当前 CLI 查询命令示例：

```bash
dimens-cli report query \
  --project-id PROJ1 \
  --report-id REPORT_1 \
  --params '{"month":"2026-04"}' \
  --widget-ids widget_1,widget_2
```

### 3.3.1 固定预检链命令示例

```bash
dimens-cli report preview \
  --project-id PROJ1 \
  --data-source '{"mode":"sheet"}' \
  --data-mapping '{"nameKey":"名称","valueKey":"销售额"}'

dimens-cli report query-widget \
  --project-id PROJ1 \
  --report-id REPORT_1 \
  --widget-id widget_1 \
  --params '{"month":"2026-04"}'
```

如果这两步都没有先执行，就不建议直接宣称组件一定能成功创建。

### 3.3 查询单个组件

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/report/query/:projectId/widget` |

请求体：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `reportId` | `string` | 是 | 报表 ID |
| `widgetId` | `string` | 是 | 组件 ID |
| `parameterValues` | `object` | 否 | 参数值 |
| `dataSource` | `object` | 否 | 临时覆盖组件数据源 |
| `dataMapping` | `object` | 否 | 临时覆盖数据映射 |

成功返回：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.data` | `array` | 组件查询结果 |
| `data.total` | `number` | 结果总数 |

失败返回：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.error` | `string` | 错误消息 |

### 3.4 数据预览

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/report/query/:projectId/preview` |

请求体：

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `dataSource` | `object` | 是 |
| `dataMapping` | `object` | 否 |
| `parameterValues` | `object` | 否 |

这条接口是 Skill 解释“为什么图表空白，但其实查询本身没问题”时很关键的一条辅助接口。

---

## 4. 报表模板接口

### 4.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/report/template` |
| 入口角色 | 报表模板入口 |

## 6. 这份文档的职责边界

这份文档只负责接口级案例总览，不再展开：

- 报表主资源、组件、查询、参数联动之间的业务分层
- 当前能力是否已 CLI 化

这些内容已经拆到独立 references 中，方便后续 Skill 精确引用。

### 4.2 模板列表

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/report/template/list` |

请求体：

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `category` | `string` | 否 |
| `keyword` | `string` | 否 |
| `page` | `number` | 否 |
| `size` | `number` | 否 |

### 4.3 模板详情

| 方法 | 路径 |
| --- | --- |
| `GET` | `/app/report/template/info?templateId=:templateId` |

### 4.4 模板分类

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/report/template/categories` |

### 4.5 应用模板到项目

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/report/template/:projectId/apply` |

请求体：

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `templateId` | `number` | 是 |
| `name` | `string` | 否 |

成功返回：

```json
{
  "code": 1000,
  "message": "success",
  "data": {
    "reportId": "report_xxx"
  }
}
```

---

## 5. 报表版本接口

### 5.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/report/version/:projectId` |
| 入口角色 | 报表版本入口 |

### 5.2 版本列表

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/report/version/:projectId/list` |

请求体：

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `reportId` | `string` | 是 |
| `page` | `number` | 否 |
| `size` | `number` | 否 |

### 5.3 版本详情

| 方法 | 路径 |
| --- | --- |
| `GET` | `/app/report/version/:projectId/info?versionId=:versionId` |

### 5.4 版本对比

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/report/version/:projectId/compare` |

请求体：

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `sourceVersionId` | `string` | 是 |
| `targetVersionId` | `string` | 是 |

---

## 6. Skill 输出要求

当用户提到报表、图表、数据源、参数联动时，Skill 至少要说清：

1. 当前问题属于报表主资源、组件、查询、模板还是版本。
2. 具体接口路径是什么。
3. 请求里哪些字段是核心入参，例如 `projectId`、`reportId`、`widgetId`、`parameterValues`。
4. 报表能打开但没数据时，不能只盯页面，要继续检查 query / widget / preview 这几层。
5. 对已封装能力优先给真实 CLI 命令；对未完全封装能力再回到 server 真实接口案例，不要混用两套口径。
