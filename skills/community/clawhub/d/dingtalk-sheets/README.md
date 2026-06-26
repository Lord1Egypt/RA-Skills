# 钉钉表格操作技能 (dingtalk-sheets)

管理钉钉在线表格中的表格文件、工作表和单元格数据。支持创建表格、管理工作表、读取范围、更新单元格、查找单元格，以及通过 `get_sheet + update_range` 方式安全追加行。

## 功能特性

- ✅ 创建在线表格文件
- ✅ 新建工作表并获取全部工作表列表
- ✅ 获取工作表详情（行列数、最后非空行列等）
- ✅ 读取指定范围或整张工作表的非空数据
- ✅ 更新单元格值、超链接和数字格式
- ✅ 通过 `get_sheet + update_range` 在工作表末尾追加多行数据
- ✅ 在工作表内查找匹配文本
- ✅ 从本地 CSV / TSV 导入或导出表格数据

## 真实工具清单

当前已按 MCP 服务真实 `tools/list` 对齐以下工具：

- `create_workspace_sheet`
- `create_sheet`
- `get_all_sheets`
- `get_sheet`
- `get_range`
- `update_range`
- `append_rows`
- `find_cells`

> 临时说明：MCP 仍然会暴露 `append_rows`，但当前 skill 已把它视为上游不稳定能力。无论是文档指引还是本地脚本，都会优先改用 `get_sheet + update_range` 实现追加。

其中核心参数已根据真实服务返回的 `inputSchema` 重写，尤其包括：

- `nodeId` 同时支持 URL 与 `dentryUuid`
- `get_range.range` 支持 A1 表示法和工作表前缀
- `update_range` 的必填字段为 `nodeId`、`sheetId`、`rangeAddress`
- `find_cells` 支持 `matchCase`、`useRegExp`、`includeHidden`、`matchEntireCell`、`matchFormulaText`

## 快速开始

### 1. 安装技能

```bash
clawhub install dingtalk-sheets
```

### 2. 安装依赖

```bash
npm install -g mcporter
```

### 3. 配置凭证

访问 [钉钉 MCP 广场](https://mcp.dingtalk.com) 找到 **钉钉表格** 服务，获取 Streamable HTTP URL：


#### 3.1 添加 mcporter 配置
```bash
mcporter config add dingtalk-sheets --url "<你的_URL>"
```

#### 3.2 添加 openclaw 配置
然后在openclaw.json中添加凭证信息

```json
{
	"agents": {
		"defaults": {
			"skills": {
				"entries": {
					"dingtalk-sheets": {
						"enable": true,
						"env": {
							"DINGTALK_MCP_SHEETS_URL": "Your Streamable HTTP URL"
						}
					}
				}
			}
		}
	}
}
```

### 4. 使用示例

```bash
# 创建新表格
mcporter call dingtalk-sheets.create_workspace_sheet --args '{"name": "Q3 销售数据"}'

# 在已有表格中创建工作表
mcporter call dingtalk-sheets.create_sheet --args '{"nodeId": "https://alidocs.dingtalk.com/i/nodes/abc123", "name": "汇总"}'

# 获取所有工作表
mcporter call dingtalk-sheets.get_all_sheets --args '{"nodeId": "abc123"}'

# 读取 Sheet1 的 A1:D10
mcporter call dingtalk-sheets.get_range --args '{"nodeId": "abc123", "sheetId": "Sheet1", "range": "A1:D10"}'

# 更新 A1:C2
mcporter call dingtalk-sheets.update_range --args '{"nodeId": "abc123", "sheetId": "Sheet1", "rangeAddress": "A1:C2", "values": [["姓名", "完成率", "状态"], ["张三", "95%", "完成"]]}'

# 末尾追加行（当前推荐走 get_sheet + update_range）
mcporter call dingtalk-sheets.get_sheet --args '{"nodeId": "abc123", "sheetId": "Sheet1"}'
mcporter call dingtalk-sheets.update_range --args '{"nodeId": "abc123", "sheetId": "Sheet1", "rangeAddress": "A129:C129", "values": [["李四", "88%", "跟进中"]]}'

# 查找所有包含 OK 的单元格
mcporter call dingtalk-sheets.find_cells --args '{"nodeId": "abc123", "sheetId": "Sheet1", "text": "OK", "matchCase": false}'
```

## 方法列表

| 方法 | 说明 | 必填参数 | 备注 |
|------|------|---------|------|
| `create_workspace_sheet` | 创建新的在线表格文件 | `name` | 可选 `folderId` / `workspaceId` |
| `create_sheet` | 新建工作表 | `nodeId`, `name` | 重名会自动改名 |
| `get_all_sheets` | 获取所有工作表 | `nodeId` | 返回工作表 ID 与名称 |
| `get_sheet` | 获取工作表详情 | `nodeId` | `sheetId` 可传名称或 ID |
| `get_range` | 读取范围数据 | `nodeId` | `sheetId`、`range` 选填 |
| `update_range` | 更新指定区域 | `nodeId`, `sheetId`, `rangeAddress` | 可附带 `values` / `hyperlinks` / `numberFormat` |
| `append_rows` | 末尾追加数据 | `nodeId`, `sheetId`, `values` | MCP 仍会暴露，但当前 skill 临时禁用，改走 `get_sheet + update_range` |
| `find_cells` | 查找匹配单元格 | `nodeId`, `sheetId`, `text` | 支持多种匹配模式 |

完整参数说明请查看 [references/api-reference.md](references/api-reference.md)

## 本地文件脚本

`scripts/` 目录提供三个辅助脚本：

- `create_sheet.py`：创建新的表格文件，可选额外新建工作表
- `import_sheet.py`：导入工作区内 `.csv` / `.tsv` 到新表格或已有表格
- `export_sheet.py`：把指定工作表或范围导出为 `.csv` / `.tsv`

兼容旧仓库调用方式，仓库里仍保留了 `create_doc.py` / `import_docs.py` / `export_docs.py` 作为薄兼容入口，但推荐改用新的脚本名。

## 注意事项

- `nodeId` 支持文档 URL 和 `dentryUuid` 两种格式
- `sheetId` 支持工作表 ID 和名称两种格式
- `get_range` 不传 `range` 时，会返回目标工作表的全部非空数据
- `range` 自带工作表前缀时，会覆盖单独传入的 `sheetId`
- `update_range.values` / `hyperlinks` 的矩阵维度应与 `rangeAddress` 一致
- 追加写入时，先用 `get_sheet` 读取 `lastNonEmptyRow`，再用 `update_range` 写入下一段空白区域
- 追加写入的列数应与现有表结构保持一致
- 仅能操作当前用户有权限访问的表格，且不支持跨组织

## 目录结构

```text
dingtalk-sheets/
├── SKILL.md
├── package.json
├── README.md
├── references/
│   ├── api-reference.md
│   └── error-codes.md
├── scripts/
│   ├── create_sheet.py
│   ├── import_sheet.py
│   ├── export_sheet.py
│   ├── create_doc.py
│   ├── import_docs.py
│   └── export_docs.py
└── tests/
    └── test_security.py
```

## 开发

```bash
python tests/test_security.py -v
```

## 许可证

MIT License
