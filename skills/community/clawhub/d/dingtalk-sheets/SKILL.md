---
name: dingtalk-sheets
description: 管理钉钉在线表格中的表格文件、工作表和单元格数据。当用户想要创建表格、查看工作表、读取范围数据、写入单元格、追加行数据或查找单元格时使用。也适用于用户提到钉钉表格、电子表格、在线表格、工作表、单元格、报表、CSV 导入导出等关键词的场景。不要在用户需要操作钉钉文档正文、管理日程、发消息或处理审批流时触发。
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": [
          "mcporter"
        ],
        "env": [
          "DINGTALK_MCP_SHEETS_URL"
        ]
      },
      "primaryEnv": "DINGTALK_MCP_SHEETS_URL",
    }
  }
---

# 钉钉表格 Skill

## Overview

用户可能要求你创建钉钉在线表格、管理工作表、读取单元格范围、写入指定区域、末尾追加行，或在工作表里查找数据。表格操作有明显依赖关系：通常要先拿到 `nodeId`，再拿到 `sheetId`，最后才能精准读写。

## 临时覆盖规则：禁用 `append_rows`

即使 MCP `tools/list` 仍然暴露了 `append_rows`，当前也要把它视为**临时不可用**。原因是上游服务存在不稳定情况，可能返回成功退出码但实际写入失败，或直接报 provider 错误。

处理“末尾追加几行 / 继续追加流水 / 新增一批记录”时，必须改用下面的回退流程：

1. `get_sheet(nodeId, sheetId)` 读取 `lastNonEmptyRow`
2. 根据待写入数据的行列数，计算下一段空白区域的 `rangeAddress`
3. `update_range(nodeId, sheetId, rangeAddress, values)` 完成追加效果

只有在明确验证 `append_rows` 恢复稳定后，才允许恢复直接调用。

## 严格禁止

1. **禁止编造 `nodeId` / `sheetId`** -- 必须从工具返回值中提取，不能手写猜测
2. **禁止把钉钉文档当作钉钉表格处理** -- `get_range` / `update_range` 只支持在线电子表格，传文档类型会报错
3. **禁止忽略 `range` 与 `sheetId` 的覆盖关系** -- 当 `range` 自带 `sheetId!A1:D10` 前缀时，应以 `range` 里的工作表为准
4. **禁止在未确认目标工作表前直接写入** -- 不确定时先 `get_all_sheets`，必要时再 `get_sheet`
5. **禁止让 `update_range.values` 维度与 `rangeAddress` 不一致** -- 行列不匹配会导致写入失败或错位
6. **禁止直接调用 `append_rows`** -- 当前上游服务不稳定；所有追加请求都必须改走 `get_sheet + update_range`
7. **禁止在追加行时忽略列对齐** -- 追加写入的列数应与现有表格结构保持一致
8. **禁止暴露敏感 MCP URL** -- 凭证 URL 含访问令牌，只能写成占位符或环境变量名

## 可用方法列表

| 方法 | 用途 | 必填参数 | 关键说明 |
|------|------|---------|---------|
| `create_workspace_sheet` | 创建新的在线表格文件 | `name` | 可创建到文件夹、知识库根目录或“我的文档” |
| `create_sheet` | 在表格中创建工作表 | `nodeId`, `name` | 重名时会自动重命名 |
| `get_all_sheets` | 获取所有工作表 | `nodeId` | 返回工作表 ID 和名称 |
| `get_sheet` | 获取工作表详情 | `nodeId` | `sheetId` 选填，不传时按服务端默认解析 |
| `get_range` | 读取单元格范围 | `nodeId` | `sheetId` / `range` 选填；不传 `range` 时读全部非空数据 |
| `update_range` | 更新指定区域 | `nodeId`, `sheetId`, `rangeAddress` | 可同时写值、超链接、数字格式 |
| `append_rows` | 在工作表末尾追加行 | `nodeId`, `sheetId`, `values` | **当前临时禁用；不要直接调用，改用 `get_sheet` + `update_range`** |
| `find_cells` | 查找匹配单元格 | `nodeId`, `sheetId`, `text` | 支持正则、公式、忽略大小写、隐藏单元格等模式 |

## 关键参数规则

1. `nodeId` 支持两种格式：
   - `https://alidocs.dingtalk.com/i/nodes/{dentryUuid}`
   - 32 位字母数字 `dentryUuid`
2. `sheetId` 可传工作表 ID 或名称；不确定时先调 `get_all_sheets`
3. `range` 使用 A1 表示法，如 `A1:D10`
4. `range` 也可带工作表前缀，如 `Sheet1!A1:D10` 或 `{sheetId}!A1:D10`
5. `update_range.hyperlinks` 中每个单元格可传对象或 `null`
6. `update_range.numberFormat` 常见值：`General`、`@`、`#,##0`、`#,##0.00`、`0%`、`yyyy/m/d`

## 意图判断

用户说“创建一个表格 / 新建报表 / 建个在线表格”：
- 先用 `create_workspace_sheet`
- 若还要求建“汇总”“明细”等页签，再用 `create_sheet`

用户说“这个表格有哪些工作表 / 列一下 sheet”：
- 用 `get_all_sheets`

用户说“看看这个 sheet 有多少行 / 工作表详情 / 最后有数据的行列”：
- 用 `get_sheet`

用户说“读取 A1 到 D10 / 导出这个范围 / 看看整张表内容”：
- 用 `get_range`
- 如果没传 `range`，默认读取目标工作表全部非空数据

用户说“把这些数据写到 A1:C5 / 改单元格 / 设置百分比格式”：
- 用 `update_range`
- 先确认目标 `sheetId` 和 `rangeAddress`

用户说“在末尾追加几行 / 继续记流水 / 新增一批记录”：
- 先用 `get_sheet` 读取 `lastNonEmptyRow`
- 再用 `update_range` 写入下一段空白区域

用户说“找一下包含 XXX 的单元格 / 在公式里搜 / 忽略大小写查找”：
- 用 `find_cells`

## 核心工作流

创建表格并新建工作表：
1. `create_workspace_sheet(name, folderId?, workspaceId?)` → 提取 `nodeId`
2. `create_sheet(nodeId, name="汇总")` → 提取新增工作表标识
3. `get_all_sheets(nodeId)` → 回显当前工作表列表

读取指定范围：
1. `get_all_sheets(nodeId)` → 解析 `sheetId`
2. `get_range(nodeId, sheetId, range="A1:D10")` → 提取 `values / formulas / displayValues`

覆盖写入矩形区域：
1. `get_all_sheets(nodeId)` → 确认目标 `sheetId`
2. 组织 `values` 为二维数组，维度与 `rangeAddress` 保持一致
3. `update_range(nodeId, sheetId, rangeAddress, values, hyperlinks?, numberFormat?)`

末尾追加数据：
1. `get_all_sheets(nodeId)` → 确认目标 `sheetId`
2. `get_sheet(nodeId, sheetId)` → 提取 `lastNonEmptyRow`
3. 根据数据维度计算新的 `rangeAddress`
4. `update_range(nodeId, sheetId, rangeAddress, values)` → 提取实际写入范围

## 上下文传递规则

| 操作 | 从返回中提取 | 用于 |
|------|-------------|------|
| `create_workspace_sheet` | `nodeId` / `dentryUuid` | 后续所有表格操作 |
| `get_all_sheets` | `sheetId`, `name` | `get_sheet` / `get_range` / `update_range` / `find_cells` |
| `get_sheet` | 行列数、最后非空行列 | 判断读取范围或追加策略 |
| `get_range` | `values`, `displayValues`, `formulas` | 给用户展示数据或导出本地 |
| `find_cells` | A1 地址列表 | 二次读取、定位或修复数据 |

## CRITICAL: 参数格式

```jsonc
// [正确] nodeId 可传 URL 或 dentryUuid
{"nodeId": "https://alidocs.dingtalk.com/i/nodes/abc123"}
{"nodeId": "abc123"}

// [正确] rangeAddress 与 values 维度一致
{"rangeAddress": "A1:B2", "values": [["1", "2"], ["3", "4"]]}

// [错误] 2x2 数据写进 1 列范围
{"rangeAddress": "A1:A2", "values": [["1", "2"], ["3", "4"]]}

// [正确] 带工作表前缀的 range
{"range": "Sheet1!A1:D10"}
```

## 本地文件脚本说明

`scripts/` 目录中的辅助脚本会处理工作区内的本地表格文件：

- `create_sheet.py`：创建新的钉钉在线表格，可选追加创建一个工作表
- `import_sheet.py`：读取工作区内 `.csv` / `.tsv`，创建新表格或写入已有表格
- `export_sheet.py`：把钉钉表格指定工作表或范围导出为本地 `.csv` / `.tsv`

这些脚本都受以下规则约束：

- 仅允许访问工作区内路径
- 使用 `resolve_safe_path()` 防止目录遍历
- 限制文件大小、行列规模和扩展名
- 仅通过 `mcporter` 调用 MCP 服务，不直接发起业务 HTTP 请求

## 错误处理

1. 遇到错误：原样展示工具报错，不要编造“成功”
2. `Invalid credentials`：提示用户重新配置 `DINGTALK_MCP_SHEETS_URL`
3. `Permission denied`：提示用户确认目标表格或目标位置权限
4. “找不到工作表”：先 `get_all_sheets`，再根据名称或 ID 重试
5. “维度不匹配”：检查 `rangeAddress` 与 `values` / `hyperlinks` 的行列数
6. “跨组织不支持”：提示用户改为同组织内文档再操作

## 详细参考（按需读取）

- [references/api-reference.md](./references/api-reference.md) -- 真实工具入参与典型返回说明
- [references/error-codes.md](./references/error-codes.md) -- 常见错误与排查路径
