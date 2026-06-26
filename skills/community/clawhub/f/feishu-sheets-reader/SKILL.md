---
name: skill-feishu-sheets
description: |
  飞书在线电子表格（Sheets）操作，包括创建、读取、写入、追加数据、管理工作表。
  当用户提到飞书电子表格、在线表格、电子表格时使用（不是多维表格 Bitable）。
  支持：创建表格、读写单元格、追加行、插入/删除行列、管理工作表。
---

# 飞书电子表格工具

统一使用 `feishu_sheets` 工具，通过 action 参数区分不同的表格操作。

## Token 提取

从 URL `https://xxx.feishu.cn/sheets/shtABC123` → `spreadsheet_token` = `shtABC123`

## 操作列表

### 创建电子表格

```json
{ "action": "create", "title": "新建表格" }
```

可选指定文件夹：
```json
{ "action": "create", "title": "新建表格", "folder_token": "fldcnXXX" }
```

返回：spreadsheet_token、url、title

### 写入数据

```json
{
  "action": "write",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "range": "A1:C3",
  "values": [["姓名", "年龄", "城市"], ["Alice", 25, "北京"], ["Bob", 30, "上海"]]
}
```

### 读取数据

```json
{
  "action": "read",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "range": "A1:C10"
}
```

### 追加数据

```json
{
  "action": "append",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "values": [["Charlie", 28, "深圳"]]
}
```

### 插入行/列

```json
{
  "action": "insert_dimension",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "dimension": "ROWS",
  "start_index": 5,
  "end_index": 7
}
```

### 删除行/列

```json
{
  "action": "delete_dimension",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx",
  "dimension": "ROWS",
  "start_index": 5,
  "end_index": 7
}
```

### 获取表格信息

```json
{ "action": "get_info", "spreadsheet_token": "shtABC123" }
```

返回：表格元数据，包含所有工作表的 sheet_id 和标题

### 新增工作表

```json
{
  "action": "add_sheet",
  "spreadsheet_token": "shtABC123",
  "title": "Sheet2"
}
```

### 删除工作表

```json
{
  "action": "delete_sheet",
  "spreadsheet_token": "shtABC123",
  "sheet_id": "0bxxxx"
}
```

## 范围格式

- 单个单元格：`A1`、`B5`
- 范围：`A1:C10`、`B2:D5`
- 整列：`A:A`、`B:D`
- 整行：`1:1`、`3:5`
- 带 sheet_id：`0bxxxx!A1:C10`

## 工作表 ID

- 从 URL 获取：`https://xxx.feishu.cn/sheets/shtABC123?sheet=0bxxxx`
- 通过 get_info 操作获取
- 默认第一个工作表的 ID 通常类似 `0bxxxx`

## 数据类型

支持的值类型：
- 字符串：`"你好"`
- 数字：`123`、`45.67`
- 公式：`{"type": "formula", "text": "=SUM(A1:A10)"}`
- 链接：`{"type": "url", "text": "点击这里", "link": "https://..."}`

## 配置

```yaml
channels:
  feishu:
    tools:
      sheets: true  # 默认：true
```

## 所需权限

- `sheets:spreadsheet` - 创建和管理电子表格
- `sheets:spreadsheet:readonly` - 读取电子表格数据
- `drive:drive` - 访问云空间

## API 参考

基础 URL：`https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/`

详细 API 文档请参阅 references/api-reference.md。
