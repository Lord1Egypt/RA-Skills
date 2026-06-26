# Gety CLI 参考文档

Gety 是一款 AI 驱动的本地文件搜索引擎。通过 CLI，可以在终端中搜索文档、获取内容，并管理连接器。

## 核心功能

### 1. 搜索文档

在所有已索引内容中搜索文档。

#### 常用选项

| 选项 | 说明 |
| --- | --- |
| `-n, --limit <n>` | 返回结果数量上限（默认：10）。 |
| `--offset <n>` | 分页偏移量（默认：0）。 |
| `--no-semantic-search` | 关闭语义搜索（默认开启）。 |
| `-c, --connector <name>` | 按连接器名称过滤，可重复传入或使用逗号分隔。 |
| `-e, --ext <ext>` | 按文件扩展名过滤，可重复传入或使用逗号分隔。 |
| `--match-scope <scope>` | 按匹配范围过滤：`title`、`content`、`semantic`。 |
| `--sort-by <default\|update_time>` | 排序字段：`default` 或 `update_time`。 |
| `--sort-order <ascending\|descending>` | 排序方向：`ascending` 或 `descending`。 |
| `--update-time-from <iso8601>` | 更新时间起点（ISO 8601）。 |
| `--update-time-to <iso8601>` | 更新时间终点（ISO 8601）。 |

#### 示例

```bash
gety search "meeting notes"
gety search "roadmap" -n 20 --offset 20
gety search "security review" -c "Folder: Work" -e pdf,docx
gety search "design system" --match-scope title,content --sort-by update_time --sort-order descending
```

### 2. 获取文档

根据连接器 ID 和文档 ID 获取指定文档的详细信息。

```bash
gety doc folder_1 doc_123
gety doc folder_1 doc_123 --json
```

### 3. 管理连接器

#### 3.1 列出连接器

```bash
gety connector list
gety connector list --json
```

#### 3.2 添加连接器

按目录路径新增连接器，可选指定显示名称。

```bash
gety connector add /path/to/docs --name "Folder: Docs"
```

#### 3.3 移除连接器

按连接器 ID 删除连接器。

```bash
gety connector remove folder_1
```

## JSON 输出

使用 `--json` 返回结构化结果，便于脚本处理。

```bash
gety search "roadmap" --json
gety doc folder_1 doc_123 --json
gety connector list --json
```

## 退出码（Exit Codes）

| Code | Meaning |
| --- | --- |
| `0` | Success（成功） |
| `1` | General error（通用错误） |
| `2` | Invalid arguments（参数无效） |
| `69` | Gety is not running（Gety 未运行） |
| `77` | Quota exceeded（配额超限） |

**处理建议：**
- 退出码 `69`：提示用户先启动 Gety 桌面应用，再重试。
- 退出码 `77`：告知用户当前搜索配额已耗尽，建议稍后重试或检查 Gety 订阅状态。
- 退出码 `2`：检查命令参数是否正确，可运行 `gety search --help` 查看用法。

## 查看帮助

```bash
gety --help
gety search --help
gety doc --help
gety connector --help
gety connector add --help
```
