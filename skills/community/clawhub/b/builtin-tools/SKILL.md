---
name: builtin-tools
author: 王教成 Wang Jiaocheng (波动几何)
description: >
  跨平台基础工具集 — 16 个独立可组合的 Python 脚本，替代 Agent 平台缺失的基础工具能力。
  文件系统（浏览/搜索/读写/替换/删除）、内容搜索（正则）、网络（搜索/抓取/预览）、
  运行时安装、持久化记忆、定时任务、任务管理。
  纯 Python 标准库，零外部依赖，跨 Windows/macOS/Linux。
  自举设计：execute_command.py 可调度所有其他脚本，平台只需支持一条 Python 命令即可全量使用。
---

# builtin-tools — 跨平台基础工具集

## 定位

当宿主 Agent 平台缺少某个基础工具时，用本技能的脚本补足。
所有脚本纯 Python 标准库实现，零外部依赖，跨 Windows/macOS/Linux。

## 核心规则

1. **优先用宿主平台内置工具** — 仅在平台不支持时回退到本技能脚本
2. **通过 execute_command 调用** — 所有脚本接受 JSON 输入，输出 JSON 结果
3. **自举设计** — `execute_command.py` 可调度所有其他脚本，只需平台支持执行一条 Python 命令

## 脚本清单

| 脚本 | 功能 | 调用方式 |
|------|------|---------|
| `execute_command.py` | 自举入口 + 命令执行 + 管道串联 | 见下方详细说明 |
| `list_dir.py` | 目录浏览 | `python list_dir.py '{"path":".","ignore":["*.log"]}'` |
| `search_file.py` | 文件名搜索 | `python search_file.py '{"pattern":"*.py","recursive":true}'` |
| `read_file.py` | 读取文件 | `python read_file.py '{"path":"f.txt","offset":0,"limit":50}'` |
| `write_file.py` | 写入文件 | `python write_file.py '{"path":"f.txt","content":"hello"}'` |
| `replace_in_file.py` | 精确替换 | `python replace_in_file.py '{"path":"f.txt","old":"a","new":"b"}'` |
| `delete_file.py` | 删除文件 | `python delete_file.py '{"path":"f.txt"}'` |
| `search_content.py` | 正则内容搜索 | `python search_content.py '{"pattern":"TODO","path":"."}'` |
| `web_search.py` | 网页搜索 | `python web_search.py '{"query":"Python","engine":"duckduckgo"}'` |
| `web_fetch.py` | 网页抓取 | `python web_fetch.py '{"url":"https://..."}'` |
| `preview_url.py` | 浏览器预览 | `python preview_url.py '{"url":"https://..."}'` |
| `install_binary.py` | 运行时安装 | `python install_binary.py '{"type":"python","version":"3.13.12"}'` |
| `update_memory.py` | 持久化记忆 | `python update_memory.py '{"action":"create","title":"...","content":"..."}'` |
| `automation_update.py` | 定时任务 | `python automation_update.py '{"mode":"create","name":"...","prompt":"...","rrule":"..."}'` |
| `todo_write.py` | 任务管理 | `python todo_write.py '{"todos":[{"id":"1","status":"in_progress","content":"..."}]}'` |

## execute_command.py 详细用法

### 模式 1：执行系统命令

```json
{"mode": "command", "command": "ls -la", "timeout": 30, "cwd": "/tmp"}
```

### 模式 2：执行内置脚本

```json
{"mode": "script", "script": "list_dir", "params": {"path": "."}}
```

### 模式 3：打开 URL/文件

```json
{"mode": "open", "url": "https://example.com"}
```

### 模式 4：管道串联多个脚本

```json
{"mode": "pipe", "chain": ["search_file", "search_content"], "params": {"pattern": "*.py"}}
```

### 快捷模式

```bash
python execute_command.py search_file '{"pattern":"*.py"}'
python execute_command.py --command "echo hello"
```

## JSON 协议

所有脚本遵循统一协议：

- **输入**：JSON 字符串（命令行第一个参数 或 stdin）
- **输出**：`{"status":"ok","data":{...},"message":"ok"}` 或 `{"status":"error","code":N,"message":"..."}`
- **Exit Code**：0=成功, 1=参数错误, 2=执行失败, 3=不支持的平台

## 目录结构

```
builtin-tools/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── common.py               # 公共层（Shell执行/JSON协议/路径处理）
│   ├── execute_command.py      # 自举入口
│   ├── list_dir.py             # 目录浏览
│   ├── search_file.py          # 文件名搜索
│   ├── read_file.py            # 读取文件
│   ├── write_file.py           # 写入文件
│   ├── replace_in_file.py      # 精确替换
│   ├── delete_file.py          # 删除文件
│   ├── search_content.py       # 正则内容搜索
│   ├── web_search.py           # 网页搜索
│   ├── web_fetch.py            # 网页抓取
│   ├── preview_url.py          # 浏览器预览
│   ├── install_binary.py       # 运行时安装
│   ├── update_memory.py        # 持久化记忆
│   ├── automation_update.py    # 定时任务
│   └── todo_write.py           # 任务管理
└── references/
    └── protocol.md             # 接口协议详细文档
```

## 安全策略

- `execute_command.py` 不使用 `shell=True`（Windows 用 list 参数传递给 powershell.exe）
- `delete_file.py` 禁止删除根目录和用户主目录
- `replace_in_file.py` 默认限制替换次数（防止误操作）
- `install_binary.py` 下载后校验文件完整性
