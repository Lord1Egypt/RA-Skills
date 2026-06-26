# builtin-tools 接口协议文档

## 通用协议

### 输入格式

所有脚本接受 JSON 输入，通过以下两种方式之一：

1. **命令行参数**（推荐）：`python script.py '{"key": "value"}'`
2. **stdin 管道**：`echo '{"key": "value"}' | python script.py`

### 输出格式

成功：
```json
{"status": "ok", "data": {...}, "message": "ok"}
```

失败（输出到 stderr）：
```json
{"status": "error", "code": 1, "message": "错误描述"}
```

### Exit Code

| Code | 含义 |
|------|------|
| 0 | 成功 |
| 1 | 参数错误 |
| 2 | 执行失败 |
| 3 | 不支持的操作系统 |

---

## 各脚本接口

### list_dir.py

```json
{
  "path": ".",           // 目录路径（默认当前目录）
  "ignore": ["*.log"],   // 忽略模式列表（可选）
  "show_hidden": false,  // 显示隐藏文件（默认 false）
  "max_depth": 1         // 最大递归深度（默认 1）
}
```

返回：
```json
{
  "path": "/absolute/path",
  "dirs": ["subdir1", "subdir2"],
  "files": ["file1.py", "file2.txt"],
  "total_dirs": 2,
  "total_files": 2,
  "entries": [
    {"name": "subdir1", "type": "dir"},
    {"name": "file1.py", "type": "file", "size": 1024}
  ]
}
```

### search_file.py

```json
{
  "pattern": "*.py",     // glob 模式（必填）
  "path": ".",           // 搜索根目录
  "recursive": true,     // 递归搜索
  "case_sensitive": false,
  "ignore_dirs": ["node_modules", ".git"],
  "max_results": 500
}
```

### read_file.py

```json
{
  "path": "file.txt",    // 文件路径（必填）
  "offset": 0,           // 起始行号
  "limit": 50,           // 读取行数
  "encoding": "utf-8"    // 文件编码
}
```

### write_file.py

```json
{
  "path": "file.txt",    // 文件路径（必填）
  "content": "text",     // 内容（必填）
  "encoding": "utf-8",
  "mkdirs": true,        // 自动创建父目录
  "append": false,       // 追加模式
  "newline": null        // 换行符（null=系统默认）
}
```

### replace_in_file.py

```json
{
  "path": "file.txt",    // 文件路径（必填）
  "old": "原文本",        // 原文本（必填）
  "new": "新文本",        // 替换文本
  "encoding": "utf-8",
  "count": 1             // 最大替换次数（默认 1）
}
```

### delete_file.py

```json
{
  "path": "file.txt",    // 文件路径（必填）
  "recursive": false     // 递归删除目录
}
```

### search_content.py

```json
{
  "pattern": "TODO",     // 正则表达式（必填）
  "path": ".",
  "case_sensitive": false,
  "glob": "*.py",       // 文件名过滤
  "context_before": 0,   // 上下文行数
  "context_after": 0,
  "max_results": 100,
  "output_mode": "content"  // "content" | "count" | "files"
}
```

### web_search.py

```json
{
  "query": "Python pathlib",  // 搜索查询（必填）
  "engine": "duckduckgo",    // 搜索引擎: "duckduckgo" | "duckduckgo_html"（默认 duckduckgo）
  "max_results": 10,         // 最大结果数
  "timeout": 30
}
```

返回：
```json
{
  "query": "Python pathlib",
  "engine": "duckduckgo",
  "results": [
    {"title": "...", "url": "https://...", "snippet": "..."}
  ],
  "total": 10
}
```

> 注：DuckDuckGo API 无需 Key，但依赖网络可达性。

### web_fetch.py

```json
{
  "url": "https://...",  // URL（必填）
  "extract": "section", // 提取特定章节（可选）
  "max_length": 50000,  // 最大文本长度
  "timeout": 30,
  "as_markdown": true   // 输出 Markdown 格式
}
```

### preview_url.py

```json
{
  "url": "https://..."   // URL（必填）
}
```

### install_binary.py

```json
{
  "type": "python",      // "python" | "node"（必填）
  "version": "3.13.12",  // 版本号（必填）
  "dest": null,          // 自定义安装目录
  "force": false         // 强制重新安装
}
```

### update_memory.py

```json
// 创建
{"action": "create", "title": "标题", "content": "内容", "category": "general", "memory_dir": null}

// 搜索
{"action": "search", "query": "关键词", "limit": 20, "memory_dir": null}

// 列出
{"action": "list", "memory_dir": null}

// 读取
{"action": "read", "file": "2026-04-13.md", "memory_dir": null}
```

### automation_update.py

```json
// 创建
{"mode": "create", "name": "任务名", "prompt": "执行内容",
 "rrule": "FREQ=DAILY;BYHOUR=9;BYMINUTE=0", "status": "active"}

// 列出
{"mode": "list"}

// 查看系统级命令
{"mode": "cron", "id": "task-name"}
```

### todo_write.py

```json
{
  "todos": [
    {"id": "1", "status": "in_progress", "content": "任务描述"},
    {"id": "2", "status": "pending", "content": "另一个任务"}
  ],
  "merge": false,        // 合并已有任务
  "path": null           // 自定义存储路径
}
```

status 取值：`pending` | `in_progress` | `completed` | `cancelled`
