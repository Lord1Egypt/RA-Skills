# 钉钉表格错误排查参考

## 常见错误速查

| 错误 / 现象 | 常见原因 | 处理方式 |
|------------|---------|---------|
| `Invalid credentials` | MCP URL 配置错误、令牌过期 | 重新从钉钉 MCP 广场获取 URL，更新 `mcporter config` 或 `DINGTALK_MCP_SHEETS_URL` |
| `Permission denied` | 对目标表格、文件夹或知识库没有对应权限 | 确认自己具备可读 / 可编辑 / 可创建权限 |
| `Document not found` | `nodeId` 无效、表格已删除、跨组织访问 | 重新确认 URL / `dentryUuid` 来源，并确保在同组织内操作 |
| “仅支持在线电子表格” | 把钉钉文档或其他类型节点传给了表格工具 | 改用真实表格 URL / `nodeId` |
| “找不到工作表” | `sheetId` 名称写错或目标表格已改名 | 先调用 `get_all_sheets` 再按返回值选择 |
| `Invalid parameter` | 参数类型、字段名或范围格式错误 | 对照真实 `inputSchema` 修正 |
| 维度不匹配 | `rangeAddress` 与 `values` / `hyperlinks` 行列数不一致 | 调整二维数组尺寸，使其与范围完全一致 |
| `append_rows` 返回 `ERROR` / `No provider available` | 上游 `append_rows` 服务临时不可用或不稳定 | 不要重试直接追加；改用 `get_sheet` 读取 `lastNonEmptyRow` 后，再走 `update_range` |
| 追加列对不齐 | `append_rows.values` 列数与现有结构不同 | 保持列数一致后再追加 |
| 查找结果为空 | 大小写、范围、公式模式或隐藏行列设置不对 | 调整 `matchCase` / `range` / `matchFormulaText` / `includeHidden` |
| 跨组织不支持 | DingTalk 表格 MCP 不支持跨组织操作 | 改为同组织文档后再执行 |

## 参数格式速查

| 参数 | 正确示例 | 错误示例 | 结果 |
|------|---------|---------|------|
| `nodeId` | `"https://alidocs.dingtalk.com/i/nodes/abc123"` | `"https://evil.com/i/nodes/abc123"` | 目标无效 |
| `nodeId` | `"abc123"` | `123` | 类型错误 |
| `sheetId` | `"Sheet1"` / `"sheet_1"` | `null`（在必填接口里） | 无法定位工作表 |
| `range` | `"A1:D10"` | `"A1-D10"` | A1 语法错误 |
| `rangeAddress` | `"A1:C3"` | `"1,1:3,3"` | 写入失败 |
| `values` | `[["1","2"],["3","4"]]` | `["1","2","3"]` | 不是二维数组 |
| `hyperlinks` | `[[{"type":"path","link":"https://...","text":"跳转"}]]` | `{"type":"path"}` | 不是二维数组 |
| `numberFormat` | `"0%"` | `0` | 类型错误 |

## 排查流程

```text
1. 先确认 MCP 凭证有效
2. 再确认 nodeId 是真实表格，而不是文档
3. 通过 get_all_sheets 确认目标 sheetId / 名称
4. 检查 range / rangeAddress 是否为合法 A1 表示法
5. 检查 values / hyperlinks 是否为二维数组，且维度匹配
6. 若是追加行，确认列数与现有数据结构一致
7. 若是查找，按需调整大小写、正则、隐藏单元格和公式搜索开关
```

## 本地脚本常见问题

| 现象 | 原因 | 处理方式 |
|------|------|---------|
| `import_sheet.py` 提示路径超出允许范围 | 文件不在工作区内 | 把文件移动到工作区，或调整 `OPENCLAW_WORKSPACE` |
| `import_sheet.py` 提示不支持的文件类型 | 只允许 `.csv` / `.tsv` | 转成 CSV / TSV 再导入 |
| `export_sheet.py` 提示输出类型不支持 | 只允许导出 `.csv` / `.tsv` | 修改输出文件后缀 |
| 导入报行列过多 | 本地文件超过脚本保护阈值 | 切分文件或按范围分批导入 |
