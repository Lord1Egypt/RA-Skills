# 钉钉表格 API 参考

> 本文档的工具名、必填参数和字段说明已按真实 MCP `tools/list` 对齐；出参部分以服务端描述和典型结果为主，实际字段以运行时返回为准。

> 临时覆盖规则：虽然 MCP 仍会返回 `append_rows` 的 schema，但当前 skill 统一把它视为不稳定能力。所有“追加行”场景请改用 `get_sheet + update_range`。

## 1. `create_workspace_sheet`

创建新的钉钉在线表格文件。

支持三种创建位置：

1. 传 `folderId`：创建到指定文件夹
2. 传 `workspaceId` 且不传 `folderId`：创建到知识库根目录
3. 两者都不传：创建到“我的文档”根目录

**必填参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `name` | string | 是 | 新表格标题 |
| `folderId` | string | 否 | 文件夹节点 ID 或链接 URL |
| `workspaceId` | string | 否 | 知识库 ID；若同时传 `folderId`，以 `folderId` 为准 |

**典型返回：**

```json
{
  "nodeId": "abc123def456",
  "title": "Q3 销售数据",
  "url": "https://alidocs.dingtalk.com/i/nodes/abc123def456"
}
```

## 2. `create_sheet`

在已有表格文件中创建一个新的工作表。

**必填参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `nodeId` | string | 是 | 表格文件 ID；可传 URL 或 `dentryUuid` |
| `name` | string | 是 | 工作表名称；重名时服务端会自动调整 |

**典型返回：**

```json
{
  "sheetId": "sheet_2",
  "name": "汇总"
}
```

## 3. `get_all_sheets`

获取指定表格中的所有工作表列表。

**必填参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `nodeId` | string | 是 | 目标电子表格标识；支持 URL 或 `dentryUuid` |

**典型返回：**

```json
{
  "sheets": [
    { "sheetId": "sheet_1", "name": "Sheet1" },
    { "sheetId": "sheet_2", "name": "汇总" }
  ]
}
```

## 4. `get_sheet`

获取指定工作表详情，例如行列数、最后非空行列等。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `nodeId` | string | 是 | 目标电子表格标识；支持 URL 或 `dentryUuid` |
| `sheetId` | string | 否 | 工作表 ID 或名称；建议先通过 `get_all_sheets` 获取 |

**典型返回：**

```json
{
  "sheetId": "sheet_1",
  "name": "Sheet1",
  "rowCount": 1000,
  "columnCount": 26,
  "lastNonEmptyRow": 128,
  "lastNonEmptyColumn": 7
}
```

## 5. `get_range`

读取指定工作表的指定范围数据。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `nodeId` | string | 是 | 表格标识；仅支持在线电子表格 |
| `sheetId` | string | 否 | 工作表 ID 或名称；不传时默认第一个工作表 |
| `range` | string | 否 | A1 范围，如 `A1:D10`；也可写成 `Sheet1!A1:D10` |

**说明：**

- 不传 `range` 时，返回目标工作表全部非空数据
- `range` 自带工作表前缀时，会覆盖单独传入的 `sheetId`
- 返回值通常包含 `values`、`formulas`、`displayValues`

**典型返回：**

```json
{
  "values": [["张三", 0.95], ["李四", 0.88]],
  "formulas": [["", ""], ["", ""]],
  "displayValues": [["张三", "95%"], ["李四", "88%"]]
}
```

## 6. `update_range`

更新表格指定区域内容，可同时设置单元格值、超链接和数字格式。

**必填参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `nodeId` | string | 是 | 表格文件 ID |
| `sheetId` | string | 是 | 工作表 ID 或名称 |
| `rangeAddress` | string | 是 | 目标区域，如 `A1:B3` |
| `values` | array | 否 | 二维数组；维度需与 `rangeAddress` 一致 |
| `hyperlinks` | array | 否 | 二维数组；每个元素为对象或 `null` |
| `numberFormat` | string | 否 | 数字格式，如 `0%`、`#,##0.00`、`yyyy/m/d` |

**`hyperlinks` 对象格式：**

```json
{
  "type": "path",
  "link": "https://www.dingtalk.com",
  "text": "DingTalk"
}
```

可选 `type`：

- `path`：外部链接
- `sheet`：工作表链接
- `range`：单元格区域链接

**典型返回：**

```json
{
  "success": true
}
```

## 7. `append_rows`

在指定工作表末尾追加若干行数据。

> 当前状态：**临时禁用直接调用**。保留本节仅用于说明远端 schema，实际使用时请改走 `get_sheet + update_range`。

**必填参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `nodeId` | string | 是 | 表格标识；支持 URL 或 `dentryUuid` |
| `sheetId` | string | 是 | 工作表 ID 或名称 |
| `values` | array | 是 | 二维数组；每个内层数组代表一行 |

**远端工具说明：**

- 服务端会自动定位最后一个有数据的行，并从下一行开始追加
- 如果工作表为空，则从第一行写入
- 追加列数应与现有表结构保持一致

**典型返回：**

```json
{
  "range": "A129:C131"
}
```

**当前推荐替代流程：**

1. 调用 `get_sheet(nodeId, sheetId)` 获取 `lastNonEmptyRow`
2. 根据待写入二维数组尺寸，计算下一段空白区域
3. 调用 `update_range(nodeId, sheetId, rangeAddress, values)`

典型示例：

```json
{
  "rangeAddress": "A129:C131",
  "values": [["李四", "88%", "跟进中"], ["王五", "91%", "完成"], ["赵六", "76%", "待处理"]]
}
```

## 8. `find_cells`

在指定工作表中查找匹配文本的所有单元格地址。

**必填参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `nodeId` | string | 是 | 表格标识；支持 URL 或 `dentryUuid` |
| `sheetId` | string | 是 | 工作表 ID 或名称 |
| `text` | string | 是 | 待查找文本；启用正则时作为正则表达式 |
| `range` | string | 否 | 限定查找范围，如 `A1:D100`、`A:A`、`1:1` |
| `matchCase` | boolean | 否 | 是否区分大小写，默认 `true` |
| `useRegExp` | boolean | 否 | 是否使用正则表达式，默认 `false` |
| `includeHidden` | boolean | 否 | 是否包含隐藏行列，默认 `false` |
| `matchEntireCell` | boolean | 否 | 是否完整单元格匹配，默认 `false` |
| `matchFormulaText` | boolean | 否 | 是否搜索公式文本，默认 `false` |

**典型返回：**

```json
{
  "matches": ["B2", "D8", "F10"]
}
```

## 常见工作流

### 创建表格并写入首屏数据

```bash
# 1. 创建表格
mcporter call dingtalk-sheets.create_workspace_sheet --args '{"name": "Q3 销售数据"}'

# 2. 获取工作表列表
mcporter call dingtalk-sheets.get_all_sheets --args '{"nodeId": "abc123"}'

# 3. 写入数据
mcporter call dingtalk-sheets.update_range --args '{"nodeId": "abc123", "sheetId": "Sheet1", "rangeAddress": "A1:C3", "values": [["姓名", "完成率", "状态"], ["张三", "95%", "完成"], ["李四", "88%", "跟进中"]]}'
```

### 读取整张工作表的非空数据

```bash
mcporter call dingtalk-sheets.get_range --args '{"nodeId": "abc123", "sheetId": "Sheet1"}'
```

### 查找并定位异常单元格

```bash
mcporter call dingtalk-sheets.find_cells --args '{"nodeId": "abc123", "sheetId": "Sheet1", "text": "ERROR", "matchCase": false}'
```
