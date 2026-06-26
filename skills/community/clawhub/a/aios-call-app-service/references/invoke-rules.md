# AIOS 应用调用细则

## 命令

```bash
aios-apps-invoke-cli servercommand <applicationName> <commandName> <method> [jsonBody] -p <provider> -s <SessionId>
aios-apps-invoke-cli binding <applicationName> <commandName> <method> <jsonBody> -p <provider> -s <SessionId>
aios-apps-invoke-cli status
```

全局命令不可用时，可使用 `npx aios-apps-invoke-cli ...`。

## 必守规则

- `-p/-s` 分别来自 `provider`、当前 `SessionId` （上下文中的 `topic_id` ）
- 当前 CLI 只支持 `provider=hzg`
- 如果 ontology、用户或上下文指向其他 provider，直接停止并说明当前运行链路不支持
- 缺任意运行时参数都不要猜，直接停止并说明缺口
- `applicationName` 取自当前使用的 ontology 所在应用目录名；如果存在多个候选应用目录，直接停止并说明冲突
- 业务命令用 `servercommand`
- 内置数据服务用 `binding`
- 本体给了绑定端点时，优先按本体调用：
- `GetTableDataWithOffset -> TableBinding`
- `GetComboBindingOptions -> CandidatesBinding`
- `CalcBindingDataSource -> DataSourceBindings`
- `binding` 一律使用规范命令名，不使用 `TableBinding`、`CandidatesBinding` 等别名作为 CLI 入参
- 带 `[HOB_EXCLUDE]` 的命令一律不调用

## 请求体规则

- `servercommand`：`commandName` 用本体命令名，`method` 用本体 `verb`，`jsonBody` 严格按 `ServerCommand 兼容 schema` 章节处理
- `servercommand` 不新增字段，不遗漏字段，不修改字段类型
- CLI 请求体只发送当前链路实际需要的 OpenClaw 会话字段：`SessionId`
- `binding`：优先根据 ontology 中的 `*-bindings.md` 文档生成兼容 schema，不要手写或反推底层 HTTP 原始 body
- `DataSourceBindings` 一律用 `binding` 命令，`commandName` 固定为 `CalcBindingDataSource`
- 如果 `binding` 和 `servercommand` 都能勉强解释当前需求，优先按 ontology 明确标注的端点类型执行；ontology 没标明时停止，不要猜

### Binding 文档取数规则

- `TableBinding` 优先读取形如 `xxx-bindings.md` 的 `TableBindings` 段落
- `CandidatesBinding` 优先读取形如 `xxx-bindings.md` 的 `CandidatesBindings` 段落
- `TableBinding` 从文档中提取：
  - `page-name`
  - `view-name`
  - `list-view-location`
  - `table-name`
  - 列表格中的每一行 `column-name + guid`
- 如果 `TableBindings` 文档缺少上述任一必需字段，不要猜，直接停止并说明缺口
- `CandidatesBinding` 从文档中提取：
  - `page-name`
  - `TableName`
  - `column-type=ID` 对应的 `ColumnName`
  - `column-type=ID` 对应的 `GUID`
  - `column-type=text` 对应的 `ColumnName`
  - `column-type=text` 对应的 `GUID`
- 如果 `CandidatesBindings` 文档缺少 `ID` 列或 `text` 列，不要猜，直接停止并说明缺口
- `TableBinding` 和 `CandidatesBinding` 各自只读取自己所属段落，不要跨段落拼字段
- `DataSourceBindings` 优先读取形如 `binding-xxx.md` 的 `DataSourceBindings` 段落
- `DataSourceBindings` 从文档中提取：
  - `page-name`
  - `cell-location`
  - `table-name`
  - `Columns` 表中的每一行 `display-name + table-name + column-name`
  - `Query Params` 表中的每一行 `table-name + column-name`
- 如果 `DataSourceBindings` 存在多组候选，且当前上下文无法唯一定位具体数据源，直接停止并说明冲突

### ServerCommand 兼容 schema

根据 `argument-type` 不同，参数的组织方法也不同。

- `basic` ：基础类型，包含布尔值、字符串、时间日期、整数、小数等
  - 布尔值： `true`、1 均被视为 true；`false`、0 则被视为 false
  - 时间日期：OADate类型，计算方法： `datetime = 1899-12-30 + OADate`
- `object` ：对象类型，需要根据 `argument-sharp` 逐层完成该参数对象的组装工作
- `array` ：数组类型，直接组装数组，数组中的元素需要根据 `argument-sharp` 逐层完成该参数数组的组装工作
- `changeset` ：变更集类型，需要组装一个包含有三个属性（`AddRows`、`EditRows` 和`DeleteRows`）的变更集对象。这种做法通常用于包含有从表的业务实体更新或创建操作中，如`包含有订单明细行的订单修改`操作。
  - `AddRows` 属性：需要被添加的子表实体数组，需要根据 `argument-sharp` 逐层完成该属性数组的组装工作
  - `EditRows` 属性：需要被修改的子表实体数组，需要根据 `argument-sharp` 逐层完成该属性数组的组装工作
  - `DeleteRows` 属性：需要被删除的子表实体数组，需要根据 `argument-sharp` 逐层完成该属性数组的组装工作

如某 ServerCommand 的参数中 `Details` 的 `argument-type` 是 `changeset` 。当需要为 `Details` 添加一个从表实体，该实体的 `SKU` 属性值为 `bn`、`Amount` 属性值为 10 时，就该如此组织请求参数：`{"OrderName":"New-Name","Details":{"AddRows":[{"SKU":"bn","Amount":10}],"EditRows":[],"DeleteRows":[]}}` 。

> 兼容性：如果按 `object` 类型处理出错，可以换用 `array` 类型或 `changeset` 类型重试。

### TableBinding 兼容 schema

- `GetTableDataWithOffset` 的 `jsonBody` 优先生成如下兼容结构：

```json
{
  "columns": [
    {
      "column-name": "编号",
      "guid": "3261feec-650a-421c-b05f-7ea8b1bed3e5"
    }
  ],
  "table-name": "物品表",
  "view-name": "物品_库存物品信息表格",
  "list-view-location": "物品_库存|物品信息表格",
  "page-name": "物品_库存",
  "target-page": 1,
  "page-limit-row-count": 0
}
```

- 生成规则：
  - `columns <- bindings 文档表格中的 column-name + guid`
  - `table-name <- table-name`
  - `view-name <- view-name`
  - `list-view-location <- list-view-location`
  - `page-name <- page-name`
  - `target-page <- 1`
  - `page-limit-row-count <- 0`
- 如果已经拿到真实分页参数，可覆盖：
  - `target-page`
  - `page-limit-row-count`
- `columns` 保持 ontology 文档中的原顺序，不要重排

### TableBinding 到底层 HTTP body 的映射说明

- 兼容 schema 会由下游 SDK / 代理转换为底层请求体
- 等价映射关系如下：
  - `bindingInfos <- columns[].guid`
  - `currentRowInfo.currentTable <- table-name`
  - `currentRowInfo.viewname <- view-name`
  - `currentRowInfo.listviewLocation <- list-view-location`
  - `offsetConditionInfo.targetPage <- target-page`
  - `offsetConditionInfo.pageLimitRowCount <- page-limit-row-count`
  - `pageName <- page-name`
- 以下字段由下游固定补齐，不需要在 ontology 文档中查找，也不要手工追加到兼容 schema：
  - `demandRowCount=0`
  - `currentDataLength=0`
  - `needRowVersion=true`
  - `editorDataInfos=null`
  - `sortCommandID=null`
  - `orderByInfo=null`
  - `columnFilterQueries=null`
  - `totalRowBindingInfos=[]`

### CandidatesBinding 兼容 schema

- `GetComboBindingOptions` 的 `jsonBody` 优先生成如下兼容结构：

```json
{
  "id-column": {
    "column-name": "ID",
    "guid": "9c641cb4-c3a3-44ea-ad5e-495c9a5d3544"
  },
  "text-column": {
    "column-name": "编号",
    "guid": "41baffe3-3982-4237-bf62-b8d95ba76218"
  },
  "table-name": "物品表",
  "page-name": "采购单填写"
}
```

- 生成规则：
  - `id-column.column-name <- column-type=ID` 对应的 `ColumnName`
  - `id-column.guid <- column-type=ID` 对应的 `GUID`
  - `text-column.column-name <- column-type=text` 对应的 `ColumnName`
  - `text-column.guid <- column-type=text` 对应的 `GUID`
  - `table-name <- TableName`
  - `page-name <- page-name`
- 如果 `CandidatesBindings` 里存在多组候选绑定，且当前上下文无法唯一定位具体组件，直接停止并说明冲突

### CandidatesBinding 到底层 HTTP body 的映射说明

- 兼容 schema 会由下游 SDK / 代理转换为底层请求体
- 等价映射关系如下：
  - `tableName <- table-name`
  - `valueColumnBindingInfo <- id-column.guid`
  - `displayColumnBindingInfo <- text-column.guid`
  - `pageName <- page-name`
- 以下字段由下游固定补齐，不需要在 ontology 文档中查找，也不要手工追加到兼容 schema：
  - `itemQuery=null`
  - `offset=null`
  - `cacheSettingID=null`

### DataSourceBinding 兼容 schema

- `CalcBindingDataSource` 的 `jsonBody` 优先生成如下兼容结构：

```json
{
  "page-name": "出入库单填写",
  "cell-location": "1,0",
  "table-name": "出入库类型表",
  "columns": [
    {
      "response-name": "value",
      "table-name": "出入库类型表",
      "column-name": "ID"
    },
    {
      "response-name": "label",
      "table-name": "出入库类型表",
      "column-name": "名称"
    }
  ],
  "query-params": [
    {
      "table-name": "出入库类型表",
      "column-name": "出入库标记"
    }
  ],
  "params": {
    "出入库类型表.出入库标记": "入库"
  }
}
```

- 生成规则：
  - `page-name <- binding 文档 Information.page-name`
  - `cell-location <- DataSourceBindings 段落中的 cell-location`
  - `table-name <- DataSourceBindings 段落中的 table-name`
  - `columns[].response-name <- Columns 表中的 display-name`
  - `columns[].table-name <- Columns 表中的 table-name`
  - `columns[].column-name <- Columns 表中的 column-name`
  - `query-params[].table-name <- Query Params 表中的 table-name`
  - `query-params[].column-name <- Query Params 表中的 column-name`
  - `params` 只有在已知真实筛选值时生成，key 固定为 `query-params` 的 `table-name.column-name`
- 如果 `Query Params` 非空但当前问题没有提供或无法推导真实参数值，不要调用，直接说明缺少哪个 `table-name.column-name`
- 如果 `Query Params` 为“无”，不要生成 `params`

### DataSourceBinding 到底层 HTTP body 的映射说明

- 兼容 schema 会由下游 SDK / 代理转换为底层请求体
- 下游会先通过 `GetMetadata2` 使用 `page-name + cell-location` 定位运行态数据源 GUID，再调用 `CalcBindingDataSource`
- 等价映射关系如下：
  - `CommandId <- GetMetadata2 运行态数据源 GUID`
  - `Params <- query-params 顺序匹配运行态 Params，取值来自 jsonBody.params`
  - 返回行中的 `response-name` 会被映射为对应 `column-name`
- 不要直接调用 `GetMetadata2` 或手工拼接底层 `CommandId`

## 额外规则

- 如果 bindings 文档已经给出真实 `column-name`，必须保留真实列名，不要用 `guid` 顶替
- 只有在文档没有列名、但调试链路必须先跑通时，才允许临时用 `guid` 兼作 `column-name`，并且必须明确说明这是降级方案
- 生成 CLI 命令前，先在答案里或推理里完成这 4 个定值：`applicationName`、`commandName`、`provider`、`SessionId`
- 任一值不能唯一确定时，不要继续拼命令
- 需要底层 ID 时，先用本体定义的查询或绑定把展示文本解析成真实 ID，再发正式请求
- JSON 字符串统一双引号；shell 转义按当前 shell 处理
- 遇到 `invalid JSON param for body` 时，先检查 JSON 和引号
- 本体标成行 ID 的字段默认按 `int` 处理
- 不要只看字段名猜含义
