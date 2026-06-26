# dimens-manager 多维表格章节 接口案例

本文档只负责接口级案例总览，覆盖：

1. 表列表 / 表树 / 表详情
2. 字段列表
3. 行分页 / 行详情
4. relation 字段的目标表与目标行追踪
5. CLI 当前实现与 server 真实接口的差异

字段设计模板请看 `field-design-patterns.md`。

`row/page` 的搜索、筛选、排序、`viewId` 继承案例请看 `row-filters.md`。

如果用户要的是“怎么一步步把系统搭出来”，请继续看 `build-flow.md`。

如果用户后续还要做报表，这份文档要和 `dimens-manager/references/report/overview.md` 一起看。表结构不是独立问题，字段设计会直接影响后面的 `report preview / query-widget / dataMapping` 是否能一次成功。

---

## 1. 查询表列表

### 1.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/project/:projectId/sheet/list` |
| 入口角色 | 项目资源列表入口 |

路径参数：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `projectId` | `string` | 是 | 项目 ID |

返回字段重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data[].sheetId` | `string` | 表 / 文档 / 报表 / 微模块 ID |
| `data[].name` | `string` | 资源名称 |
| `data[].type` | `string` | `sheet` / `document` / `report` / `micro_module` |
| `data[].config` | `object \| null` | 表结构、报表配置、模块配置等 |
| `data[].permission` | `object` | 当前用户对资源的可见和数据权限 |

### 1.2 CLI 命令

```bash
dimens-cli sheet list --project-id PUQUNFE --output json
```

CLI 入参：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--project-id` | 是，若 profile 无默认值 | 项目 ID |
| `--output` | 否 | `json` / `table` / `raw` |

本次实测结果确认：

- `PUQUNFE` 下能正常列出 `sheet/document/report/micro_module`
- 菜单里配置的 `sh_ja2IwgaBhV1jUWB4` 和 `sh_Zp60Au58FrE9FhVi` 都能从 `sheet list` 里找到

---

## 2. 查询表树

### 2.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/project/:projectId/sheet/tree` |
| 入口角色 | 项目资源树入口 |

### 2.2 CLI 命令

```bash
dimens-cli sheet tree --project-id PUQUNFE --output json
```

返回重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data[]` | `array` | 树节点列表 |
| `data[].children` | `array` | 子节点 |
| 其余字段 | 同 `sheet list` | 资源基本结构一致 |

当前实测结果：

- `sheet tree` 已正常返回
- 当前项目下资源都是平级节点，所以 `children` 为空数组

---

## 3. 查询表详情

### 3.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/:teamId/:projectId/sheet/:sheetId/info` |
| 入口角色 | 表详情入口 |

路径参数：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `teamId` | `string` | 是 | 团队 ID |
| `projectId` | `string` | 是 | 项目 ID |
| `sheetId` | `string` | 是 | 表 ID |

返回字段重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.sheetId` | `string` | 表 ID |
| `data.name` | `string` | 表名 |
| `data.type` | `string` | 资源类型 |
| `data.columns` | `array` | 字段定义 |
| `data.views` | `array` | 视图定义 |
| `data.readonlyColumns` | `string[]` | 只读字段列表 |

### 3.2 CLI 命令

```bash
dimens-cli sheet info \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_ja2IwgaBhV1jUWB4 \
  --output json
```

已实测的两个菜单表：

| sheetId | 名称 | 结论 |
| --- | --- | --- |
| `sh_ja2IwgaBhV1jUWB4` | `数据管理` | 详情可正常返回，包含 7 个字段、3 个视图 |
| `sh_Zp60Au58FrE9FhVi` | `工作表 2` | 详情可正常返回，包含 5 个字段、1 个视图 |

---

## 4. 查询字段列表

### 4.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/:teamId/:projectId/sheet/:sheetId/column/list` |
| 入口角色 | 字段列表入口 |

路径参数：

| 字段 | 类型 | 必填 |
| --- | --- | --- |
| `teamId` | `string` | 是 |
| `projectId` | `string` | 是 |
| `sheetId` | `string` | 是 |

返回字段重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `fieldId` | `string` | 字段 ID |
| `label` | `string` | 字段名称 |
| `type` | `string` | 字段类型 |
| `config` | `object \| null` | 字段配置 |
| `orderNum` | `number` | 排序 |
| `key` | `boolean` | 是否主字段 |
| `width` | `number` | 列宽 |
| `required` | `boolean` | 是否必填 |
| `unique` | `boolean` | 是否唯一 |

### 4.2 CLI 命令

```bash
dimens-cli column list \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_ja2IwgaBhV1jUWB4 \
  --output json
```

### 4.3 真实字段案例：`数据管理`

已实测字段：

| fieldId | label | type | 说明 |
| --- | --- | --- | --- |
| `fld_saLRjVbHVTf1` | 名称 | `text` | 主字段 |
| `fld_rbGLULtXWgvi` | 是的 | `text` | 普通文本字段 |
| `fld_Xpf9l7iI3LOi` | sef | `relation` | 关联到 `sh_Zp60Au58FrE9FhVi` |
| `__system_createTime` | 创建时间 | `system` | 系统字段 |
| `__system_updateTime` | 更新时间 | `system` | 系统字段 |
| `__system_createdBy` | 创建用户 | `system` | 系统字段 |
| `__system_updatedBy` | 更新用户 | `system` | 系统字段 |

relation 字段配置重点：

```json
{
  "fieldId": "fld_Xpf9l7iI3LOi",
  "type": "relation",
  "config": {
    "relationConfig": {
      "targetSheetId": "sh_Zp60Au58FrE9FhVi",
      "displayColumnId": "fld_COvhKXd8iLVQ",
      "bidirectional": false,
      "editViewFields": ["fld_COvhKXd8iLVQ"]
    }
  }
}
```

补充说明：

- `dimens-cli column create --type relation` 当前已支持把 `--target-sheet-id` 映射为 `config.relationConfig.targetSheetId`
- 推荐同时传 `--display-column-id`，避免 relation 展示值异常
- 如果后续仍出现“CLI 成功但字段未落库”，优先对照服务端最终入库结构核对 `config.relationConfig`

### 4.4 `select` 字段案例：`提交状态`

CLI 命令：

```bash
dimens-cli column create \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_ja2IwgaBhV1jUWB4 \
  --label 提交状态 \
  --type select \
  --options 待提交,提交中,已提交,已驳回
```

服务端 body：

```json
{
  "label": "提交状态",
  "type": "select",
  "config": {
    "options": [
      { "label": "待提交" },
      { "label": "提交中" },
      { "label": "已提交" },
      { "label": "已驳回" }
    ],
    "dataSourceType": "manual",
    "dictionaryId": null
  }
}
```

补充说明：

- `select` / `multiSelect` 当前先走自定义选项模式
- 创建这类字段时不能只传 `--type select`，还必须同时传 `--options`
- 技能生成字段方案时，也必须把候选项一并生成出来
- 同一个字段的选项 `id` 必须唯一，不能重复，否则前端下拉映射和后续统计都有概率异常

### 4.5 报表友好的字段组合案例

如果这张表后续还要接报表，建模时建议先按下面这种组合思路准备：

| 字段名 | 推荐类型 | 字段角色 | 说明 |
| --- | --- | --- | --- |
| 客户名称 | `text` | 维度字段 | 主展示字段，也可做分类标签 |
| 客户等级 | `select` | 维度字段 | 适合分组和统计 |
| 销售负责人 | `person` | 维度字段 | 不要退化成普通下拉 |
| 归属部门 | `department` | 维度字段 | 不要退化成普通下拉 |
| 跟进日期 | `date` | 维度字段 | 适合趋势图、按日/月统计 |
| 预计金额 | `number` | 指标字段 | 适合求和、排序、柱状图 |
| 成交金额 | `number` | 指标字段 | 适合求和、对比分析 |
| 客户备注 | `text` | 说明字段 | 只做补充说明，不直接做指标 |

这类组合的核心目标是：

- 维度字段要稳定、可读、可分组
- 指标字段必须是 `number`
- 说明字段只做详情展示，不直接进 `valueKey`

如果一开始就把这三层分清楚，后面进入 `dimens-manager/references/report/overview.md` 的固定预检链会顺很多。

## 5. 查询行分页

### 5.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/mul/:teamId/:projectId/sheet/:sheetId/row/page` |
| 入口角色 | 行分页入口 |

请求体：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `page` | `number` | 否 | 页码 |
| `size` | `number` | 否 | 每页条数 |
| `viewId` | `string` | 否 | 视图 ID |
| `keyword` | `string` | 否 | 关键词搜索 |
| `searchFieldIds` | `string[]` | 否 | 指定哪些字段参与关键词搜索 |
| `filters` | `array` | 否 | 字段过滤条件数组 |
| `filterMatchType` | `'and' \| 'or'` | 否 | 多条件命中关系，前端默认 `and` |
| `sortRule` | `object \| null` | 否 | 排序条件，前端真实口径是 `sortRule` |

返回字段重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.list` | `array` | 当前页行数据 |
| `data.list[].rowId` | `string` | 行 ID |
| `data.list[].data` | `object` | 行字段值 |
| `data.list[].version` | `number` | 行版本号 |
| `data.total` | `number` | 总条数 |
| `data.hasMore` | `boolean` | 是否还有更多 |
| `data.pagination` | `object` | 页码信息 |

### 5.2 CLI 命令

分析型取数不要直接猜筛选字段。先查字段：

```bash
dimens-cli column list \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_ja2IwgaBhV1jUWB4 \
  --output json
```

再用真实字段 ID 查询行分页：

```bash
dimens-cli row page \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_ja2IwgaBhV1jUWB4 \
  --page 1 \
  --size 10 \
  --keyword 华东 \
  --search-field-ids fld_customerName,fld_owner \
  --filters '[{"fieldId":"fld_status","operator":"equals","value":"成交"}]' \
  --filter-match-type and \
  --sort-rule '{"fieldId":"fld_amount","direction":"desc"}' \
  --output json
```

### 5.3 真实分页案例：`数据管理`

本次实测结果：

| 字段 | 值 |
| --- | --- |
| `total` | `78` |
| `page` | `1` |
| `size` | `10` |
| `hasMore` | `true` |

示例行：

```json
{
  "rowId": "28f202a6-b32d-47da-8d44-46914fff99b1",
  "data": {
    "fld_Xpf9l7iI3LOi": ["a11d4a83-d35e-4659-a7e3-67b5cbec8ffc"],
    "fld_rbGLULtXWgvi": "sdf 的",
    "fld_saLRjVbHVTf1": "sdf 水电费321312321"
  },
  "version": 76
}
```

### 5.5 平台真实使用口径

维表智联在行分页读取时，不是只传分页参数，而是会组合：

```ts
{
  page,
  size,
  keyword,
  searchFieldIds,
  filters,
  filterMatchType,
  sortRule
}
```

Skill 解释筛选、搜索、排序时应按这个请求结构说明。详细查询案例已经拆到 `row-filters.md`，这里不再重复展开。

### 5.4 真实分页案例：relation 目标表 `工作表 2`

```bash
dimens-cli row page \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_Zp60Au58FrE9FhVi \
  --page 1 \
  --size 10 \
  --output json
```

实测结果：

| 字段 | 值 |
| --- | --- |
| `total` | `4` |
| `hasMore` | `false` |

示例行：

```json
{
  "rowId": "a11d4a83-d35e-4659-a7e3-67b5cbec8ffc",
  "data": {
    "fld_COvhKXd8iLVQ": "s 的f水电费"
  }
}
```

---

## 6. 查询行详情

### 6.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/:teamId/:projectId/sheet/:sheetId/row/:rowId/info` |
| 入口角色 | 行详情入口 |

### 6.2 CLI 命令

```bash
dimens-cli row info \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_ja2IwgaBhV1jUWB4 \
  --row-id 28f202a6-b32d-47da-8d44-46914fff99b1 \
  --output json
```

### 6.3 relation 追踪案例

主表行详情：

```json
{
  "rowId": "28f202a6-b32d-47da-8d44-46914fff99b1",
  "data": {
    "fld_Xpf9l7iI3LOi": ["a11d4a83-d35e-4659-a7e3-67b5cbec8ffc"],
    "fld_rbGLULtXWgvi": "sdf 的",
    "fld_saLRjVbHVTf1": "sdf 水电费321312321"
  }
}
```

目标表行详情：

```bash
dimens-cli row info \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_Zp60Au58FrE9FhVi \
  --row-id a11d4a83-d35e-4659-a7e3-67b5cbec8ffc \
  --output json
```

```json
{
  "rowId": "a11d4a83-d35e-4659-a7e3-67b5cbec8ffc",
  "data": {
    "fld_COvhKXd8iLVQ": "s 的f水电费"
  }
}
```

这证明 relation 关联链路是通的：

1. 主表行里拿到关联目标 `rowId`
2. relation 配置里拿到 `targetSheetId`
3. 到目标表用 `row info` 成功取到目标内容

---

## 7. 当前 CLI 与平台接口的对齐说明

### 7.1 结论

当前 `row create`、`row update`、`row set-cell` 的 CLI 请求体已按 server 真实契约对齐。

仍需提醒的点：

- `row create` / `row update` 命令行参数仍然叫 `--values`，但 CLI 内部会映射为服务端需要的 `data`
- `row set-cell` 推荐使用 `--field-id`，旧参数 `--column-id` 仅保留兼容
- 行写入时，字段 key 应使用 `fieldId`，不要直接使用中文字段名

### 7.2 行创建

平台当前接口：

| 方法 | 路径 | 请求体 |
| --- | --- | --- |
| `POST` | `/app/mul/sheet/:sheetId/row/create` | `{ "data": { ... } }` |

CLI 当前实现：

| 命令 | 实际发送 |
| --- | --- |
| `dimens-cli row create --sheet-id ... --values '{...}'` | `{ "data": { ... } }` |

也就是说：

- `server` 当前真实入参是 `data`
- CLI 命令参数仍叫 `values`，但实际已映射为 `data`

### 7.3 行更新

server 当前接口：

| 方法 | 路径 | 请求体 |
| --- | --- | --- |
| `POST` | `/app/mul/sheet/:sheetId/row/:rowId/update` | `{ "data": { ... }, "version": 1 }` |

CLI 当前实现：

| 命令 | 实际发送 |
| --- | --- |
| `dimens-cli row update ... --values '{...}' --version 1` | `{ "data": { ... }, "version": 1 }` |

### 7.4 单元格更新

server 当前接口：

| 方法 | 路径 | 请求体 |
| --- | --- | --- |
| `POST` | `/app/mul/sheet/:sheetId/row/cell` | `{ "rowId": "...", "fieldId": "...", "value": ..., "version": 1 }` |

CLI 当前实现：

| 命令 | 实际发送 |
| --- | --- |
| `dimens-cli row set-cell ... --field-id ... --value ... --version 1` | `{ "rowId": "...", "fieldId": "...", "value": ..., "version": 1 }` |

因此 Skill 在解释“写接口为什么失败”时，必须明确区分：

- 当前 `server` 真实契约
- 当前 `dimens-cli` 已封装命令
- 两者是否已经完全对齐

补充说明：

- `row page`、`row info` 读取链路已经可以稳定使用
- `row/page` 说明时建议优先采用前端真实口径 `keyword / searchFieldIds / filters / filterMatchType / sortRule`
- `row create`、`row update`、`row set-cell` 当前已可按 server 契约写入，但调用前仍需先获取真实 `fieldId`
